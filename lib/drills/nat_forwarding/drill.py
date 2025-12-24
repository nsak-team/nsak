from pathlib import Path
import subprocess
import signal
import os


def enable_ip_forwarding():
    subprocess.run([
        "sysctl",
        "-w",
        "net.ipv4.ip_forward=1",
    ], check=True)


# todo forwarding rules get attached at the end if called twice ip tables get a mess of similiar rules

def add_nat_rules(ap_interface: str, uplink_interface: str):
    subprocess.run([
        "iptables", "-t", "nat",
        "-A", "POSTROUTING", "-o",
        uplink_interface, "-j",
        "MASQUERADE"
    ], check=True)
    subprocess.run([
        "iptables", "-A", "FORWARD",
        "-i", ap_interface, "-o",
        uplink_interface, "-j",
        "ACCEPT"
    ], check=True)
    subprocess.run([
        "iptables", "-A",
        "FORWARD", "-i",
        uplink_interface, "-o",
        ap_interface, "-m",
        "state",
        "--state", "RELATED,ESTABLISHED",
        "-j", "ACCEPT"
    ], check=True)


def run(args: dict) -> dict[str, any]:
    enable_ip_forwarding()
    add_nat_rules(args['interface'], args['uplink_interface'])
    return {
        "ip_forward": True,
        "interface": args["interface"],
        "uplink_interface": args["uplink_interface"],
    }
