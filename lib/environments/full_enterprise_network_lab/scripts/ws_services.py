#!/usr/bin/env python3
"""
ws_services.py — Windows-like service banner simulator for workstations.

Simulates:
  3389/tcp  RDP   — X.224 Connection Confirm (realistic enough for nmap -sV)
  5985/tcp  WinRM — HTTP 401 Negotiate/Basic challenge (WS-Management)

Usage:
  python3 ws_services.py --hostname WS01 --domain LAB
"""
import argparse
import socket
import threading
import time


def handle_rdp(conn: socket.socket, addr: tuple, hostname: str, domain: str) -> None:
    """
    Minimal RDP negotiation — sends X.224 Connection Confirm.
    nmap -sV will fingerprint this as 'Microsoft Terminal Service'.
    """
    try:
        conn.settimeout(5)
        data = conn.recv(1024)
        if not data:
            return

        # X.224 Connection Confirm PDU
        # Negotiate Response: type=2 (NegotiateResponse), flags=0, length=8
        # Selected protocol: PROTOCOL_RDP (0x00000000)
        x224_cc = bytes([
            0x03, 0x00, 0x00, 0x13,        # TPKT: version=3, reserved=0, length=19
            0x0e,                           # X.224: LI=14
            0xd0,                           # X.224: type=Connection Confirm (0xD0)
            0x00, 0x00,                     # DST-REF
            0x00, 0x00,                     # SRC-REF
            0x00,                           # CLASS
            0x02,                           # RDP_NEG_RSP type=2
            0x00,                           # flags
            0x08, 0x00,                     # length=8
            0x00, 0x00, 0x00, 0x00,        # selected protocol: PROTOCOL_RDP
        ])
        conn.sendall(x224_cc)
        time.sleep(0.5)

    except (socket.timeout, BrokenPipeError, ConnectionResetError, OSError):
        pass
    finally:
        conn.close()


def handle_winrm(conn: socket.socket, addr: tuple, hostname: str, domain: str) -> None:
    """
    WinRM (WS-Management) HTTP endpoint.
    Returns HTTP 401 with Negotiate + Basic auth challenge.
    curl -s http://192.168.10.100:5985/wsman reveals this.
    """
    try:
        conn.settimeout(5)
        req = conn.recv(4096).decode(errors="ignore")
        if not req:
            return

        # Detect if it's a proper HTTP request or a raw probe
        is_http = req.startswith(("GET ", "POST ", "HEAD ", "OPTIONS "))

        if is_http:
            body = (
                '<?xml version="1.0" encoding="UTF-8"?>'
                '<f:WSManFault xmlns:f="http://schemas.microsoft.com/wbem/wsman/1/wsmanfault" '
                'Code="500" Machine="' + hostname + '.' + domain.lower() + '.local">'
                '<f:Message>The WS-Management service cannot complete the operation '
                'within the time specified.</f:Message></f:WSManFault>'
            )
            response = (
                "HTTP/1.1 401 Unauthorized\r\n"
                "Content-Type: application/soap+xml;charset=UTF-8\r\n"
                f"Server: Microsoft-HTTPAPI/2.0\r\n"
                f"WWW-Authenticate: Negotiate\r\n"
                f"WWW-Authenticate: Basic realm=\"{hostname}\"\r\n"
                f"X-Content-Type-Options: nosniff\r\n"
                f"Content-Length: {len(body)}\r\n"
                "Connection: close\r\n"
                "\r\n"
                + body
            )
        else:
            response = "HTTP/1.1 400 Bad Request\r\nContent-Length: 0\r\nConnection: close\r\n\r\n"

        conn.sendall(response.encode())

    except (socket.timeout, BrokenPipeError, ConnectionResetError, OSError):
        pass
    finally:
        conn.close()


def serve(port: int, handler, hostname: str, domain: str) -> None:
    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("0.0.0.0", port))
    srv.listen(20)
    print(f"[{hostname}] Listening on :{port}", flush=True)
    while True:
        conn, addr = srv.accept()
        threading.Thread(
            target=handler,
            args=(conn, addr, hostname, domain),
            daemon=True,
        ).start()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Windows service banner simulator")
    parser.add_argument("--hostname", default="WORKSTATION", help="NetBIOS hostname")
    parser.add_argument("--domain",   default="LAB",         help="Domain/workgroup name")
    args = parser.parse_args()

    services = [
        (3389, handle_rdp,    "RDP"),
        (5985, handle_winrm,  "WinRM"),
    ]
    for port, handler, name in services:
        threading.Thread(
            target=serve,
            args=(port, handler, args.hostname, args.domain),
            daemon=True,
        ).start()

    print(f"[{args.hostname}] Service banners running (RDP:3389, WinRM:5985)", flush=True)
    while True:
        time.sleep(60)
