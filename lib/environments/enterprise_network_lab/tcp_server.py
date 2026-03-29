"""
Simple TCP server for MITM demonstration.
Logs each message with counter, timestamp, source and content.
"""

import datetime
import socket

HOST = "0.0.0.0"
PORT = 8080

counter = 0

print(f"[*] Listening on {HOST}:{PORT} ...")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((HOST, PORT))
    srv.listen()

    while True:
        conn, addr = srv.accept()
        with conn:
            while True:
                data = conn.recv(4096)
                if not data:
                    break
                counter += 1
                ts = datetime.datetime.now().strftime("%H:%M:%S")
                print(
                    f"[{counter:04d}] {ts}  from {addr[0]}:{addr[1]}"
                    f"  →  {data!r}"
                )
