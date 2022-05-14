#!/usr/bin/env python

"""Tests for `teleport_test_hbf` package."""


from ipaddress import ip_address
import unittest
import subprocess
import requests
import time
import socket
import fcntl
import struct
from click.testing import CliRunner

from teleport_test_hbf import teleport_test_hbf
from teleport_test_hbf import cli


def get_ip_address(ifname):
    """
    Obtain the IP address on the interface

    Parameters
    ----------
    ifname : string
        interface name

    Returns
    -------
    string
        IP address on the interface
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ip_addr = socket.inet_ntoa(
        fcntl.ioctl(
            s.fileno(), 0x8915, struct.pack("256s", bytes(ifname[:15], 'utf-8'))  # SIOCGIFADDR
        )[20:24]
    )
    s.close()
    return ip_addr


class TestTeleport_test_hbf(unittest.TestCase):
    """Tests for `teleport_test_hbf` package."""

    @classmethod
    def setUpClass(cls):
        """
        Start multiple httpd container on different ports
        """
        print("\n Starting HTTP server containers")
        for i in range(1, 9):
            subprocess.call(
                f"docker run -d --name web{i} -p 810{i}:80 httpd > /dev/null 2>&1",
                shell=True,
            )
        print("\n Starting HBF container")
        subprocess.call(f"cd setup && docker-compose up -d", shell=True)

    # def setUp(self):
    #     """
    #     Start multiple httpd container on different ports
    #     """
    #     print("\n Starting HTTP server containers")
    #     for i in range(1, 9):
    #         subprocess.call(f'docker run -d --name web{i} -p 810{i}:80 httpd > /dev/null 2>&1', shell=True)

    @classmethod
    def tearDownClass(cls):
        """
        Tear down all web containers
        """
        for i in range(1, 9):
            subprocess.call(f"docker rm -f web{i} > /dev/null 2>&1", shell=True)
        subprocess.call(f"cd setup && docker-compose down", shell=True)

    def test_portScan(self):
        """
        Test portScan
        """
        ip_address = get_ip_address("eth0")
        print(f"Got IP Address: {ip_address}")
        for i in range(1, 9):
            resp = requests.get(f"http://{ip_address}:810{i}", timeout=0.5)
            if i % 6 == 0:
                print("Status Code: ", resp.status_code)
                assert resp.status_code != 200
            time.sleep(0.5)

    def test_command_line_interface(self):
        """Test the CLI"""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert "HBF" in result.output
        help_result = runner.invoke(cli.main, ["--help"])
        assert help_result.exit_code == 0
        assert "--help  Show this message and exit." in help_result.output
