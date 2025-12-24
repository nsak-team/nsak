import logging
from pathlib import Path
import subprocess
import signal
import os

logger = logging.getLogger(__name__)


def enable_ip_forwarding():
    subprocess.run([
        "sysctl",
        "-w",
        "net.ipv4.ip_forward=1",
    ], check=True)


# todo forwarding rules get attached at the end if called twice ip tables get a mess of similiar rules, right
#  now the config is non permanent

def add_nat_rules(interface: str, uplink_interface: str):
    subprocess.run([
        "iptables", "-t", "nat",
        "-A", "POSTROUTING",
        "-o", uplink_interface,
        "-j", "MASQUERADE"
    ], check=True)
    subprocess.run([
        "iptables", "-A", "FORWARD",
        "-i", interface,
        "-o", uplink_interface,
        "-j", "ACCEPT"
    ], check=True)
    subprocess.run([
        "iptables", "-A", "FORWARD",
        "-i", uplink_interface,
        "-o", interface,
        "-m", "state", "--state",
        "RELATED,ESTABLISHED", "-j", "ACCEPT"
    ], check=True)
    logger.info("NAT rules enabled on [AP-INTERFACE]" + interface + "[UPLINK-INTERFACE] " + uplink_interface)


def run(args: dict):
    enable_ip_forwarding()
    add_nat_rules(args['interface'], args['uplink_interface'])
