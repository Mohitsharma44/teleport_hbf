"""Main module."""

import os
import sys
import socket
import struct
from ctypes import c_uint32
from datetime import datetime

from bcc import BPF
from prometheus_client import Counter
from teleport_test_hbf.logger import logger
import teleport_test_hbf.utils as utils

logger = logger("HBF", "/var/log/hbf.log")

class HBF:
    """
    Host Based Firewall using XDP
    """

    def __init__(
        self,
        iface,
        blocklist_file_path,
        time_threshold,
        port_threshold,
        hbf_timeout_seconds
    ) -> None:
        """
        Host Based Firewall using BPF and XDP

        Parameters
        ----------
        iface : str
            Interface to attach the firewall bpf program to
        blocklist_file_path : str
            Path to the file containing ip addresses that should be blocked by the firewall"
        """
        self.iface = iface
        self.blocklist_ips = []
        self.connections = {}
        self.new_connection_count = Counter("new_connections", "New connection count")
        self.blocklist_ips_path = blocklist_file_path
        self.allowed_parallel_connections = {
            "time_threshold": time_threshold,
            "port_threshold": port_threshold,
        }
        self.run_until = hbf_timeout_seconds
        self.stop = False
        self.b = BPF(src_file="/usr/config/bpf_programs/main.c")

    def loadBlocklistFile(self, blocklist_file_path) -> None:
        """
        Read the config files

        Parameters
        ----------
        blocklist_ips_path : str
            Path to the file containing ip addresses that should be blocked by the firewall
        """
        if os.path.exists(blocklist_file_path):
            with open(blocklist_file_path, "r") as fh:
                self.blocklist_ips = [x.strip() for x in fh.readlines()]
        logger.debug("Loading existing blocklist ips")
        for ip in self.blocklist_ips:
            packedIP = socket.inet_aton(ip)
            ip_int = struct.unpack("<L", packedIP)[0]
            self.b["blocklist"][c_uint32(ip_int)] = c_uint32(1)

    def parseBPFEvents(self, ctx, data, size):
        """
        Callback to parse BPF events
        """
        event = self.b["callers"].event(data)
        time_now = datetime.now().timestamp()
        src_ip = socket.inet_ntoa(struct.pack("<L", event.sourceIP))
        dst_port = socket.ntohs(event.destPort)

        # If we get connections on more than `port_threshold` ports within time `time_threshold`, blocklist the ip
        # Currently, we dont care about DOS or DDOS attacks
        if src_ip in self.connections:
            if dst_port in self.connections[src_ip]:
                self.connections[src_ip][dst_port] = time_now
            else:
                self.new_connection_count.inc()
                self.connections[src_ip].update({dst_port: time_now})
                if (
                    time_now - max(self.connections[src_ip].values())
                    < self.allowed_parallel_connections["time_threshold"]
                ):
                    logger.debug(f"Rapid connections have been detected from {src_ip} to port {dst_port}")
                    if (
                        len(self.connections[src_ip])
                        > self.allowed_parallel_connections["port_threshold"]
                    ):
                        logger.debug(f"Port Scanning detected from {src_ip}")
                        self.b["blocklist"][c_uint32(event.sourceIP)] = c_uint32(1)
                        logger.info(f"Blocked {src_ip}")
        else:
            self.connections = {src_ip: {dst_port: time_now}}

    def run(self):
        try:
            pid = utils.get_hbf_pid()
            if pid:
                logger.error(f"An instance of HBF is already running with pid: {pid}")
                sys.exit(2)
            self.b.attach_xdp(self.iface, self.b.load_func("packetwatch", BPF.XDP))
            self.loadBlocklistFile(self.blocklist_ips_path)
            self.b["callers"].open_ring_buffer(self.parseBPFEvents)
            utils.write_hbf_pid()
            while datetime.now().timestamp() < self.run_until and not self.stop:
                self.b.ring_buffer_poll(30)
            self.b.remove_xdp(self.iface)
        except:
            self.b.remove_xdp(self.iface)
        finally:
            utils.remove_hbf_pid()
