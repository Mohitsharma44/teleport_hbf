"""Console script for teleport_test_hbf."""
import os
import signal
from datetime import datetime
import click
import teleport_test_hbf.utils as utils
import logging
from teleport_test_hbf.teleport_test_hbf import HBF

@click.group()
@click.pass_context
def main(ctx):
    pass


@main.command()
@click.argument("iface", envvar="HBF_IFACE", default="eth0", required=False)
@click.argument(
    "blocklist_file_path",
    envvar="HBF_BLOCKLIST_FILE_PATH",
    default="config/blocklist_ips.txt",
    required=False,
)
@click.argument(
    "time_threshold",
    envvar="HBF_TIME_THRESHOLD",
    default=1,
    required=False,
)
@click.argument(
    "port_threshold",
    envvar="HBF_MAX_PORTS",
    default=5,
    required=False,
)
@click.argument(
    "hbf_timeout_seconds",
    envvar="HBF_TIMEOUT_SECONDS",
    default=300,
    required=False,
)
def start(
    iface, blocklist_file_path, time_threshold, port_threshold, hbf_timeout_seconds
):
    """
    Start the HBF
    """
    click.echo("A rudimentary Host Based Firewall using BPF and XDP")
    hbf = HBF(
        iface=iface,
        blocklist_file_path=blocklist_file_path,
        time_threshold=time_threshold,
        port_threshold=port_threshold,
        hbf_timeout_seconds=datetime.now().timestamp() + hbf_timeout_seconds,
    )
    hbf.run()


@main.command()
def stop():
    """
    Stop the HBF
    """
    # This will be better architected if we can have a shareable queue or cache or db of some kind
    # which will be shared between the "cli" and the "daemon"
    pid = utils.get_hbf_pid()
    if pid:
        click.echo(click.style('Stopping HBF.', fg='red'))
        os.kill(int(pid), signal.SIGTERM)
        utils.remove_hbf_pid()


@main.command()
@click.option("--ip", multiple=True)
def block(ip):
    """
    Dynamically add ips to blocklist (Not implemented, yet!)
    """
    # This will be better architected if we can have a shareable queue or cache or db of some kind
    # which will be shared between the "cli" and the "daemon"
    print(f"Will blocklist: {ip}")


if __name__ == "__main__":
    main()
