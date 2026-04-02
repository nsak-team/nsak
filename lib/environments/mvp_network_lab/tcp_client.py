"""
Simple TCP client for MITM demonstration.
Sends numbered messages in a loop to the server.
"""

import socket
import time

HOST = "192.168.10.101"
PORT = 8080
INTERVAL = 2  # seconds between messages

print(f"[*] Sending to {HOST}:{PORT} every {INTERVAL}s ...")

counter = 0
while True:
    counter += 1
    msg = f"message {counter} from ws1\n"
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(msg.encode())
        print(f"[{counter:04d}] sent: {msg.strip()}")
    except ConnectionRefusedError:
        print(f"[{counter:04d}] connection refused — server down?")
    time.sleep(INTERVAL)
