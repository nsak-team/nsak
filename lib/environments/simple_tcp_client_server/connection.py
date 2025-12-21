import socket
import time

def run_server(host, port, label):
    """Start a TCP server that waits for a client and then enters a send/receive loop."""
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((host, port))
                s.listen(1)
                print(f"[{label}] Waiting for connection on {host}:{port}...")
                conn, addr = s.accept()
                print(f"[{label}] Connected by {addr}")
                communicate(conn, label)
        except Exception as e:
            print(f"[{label}] Connection error: {e}. Retrying...")
            time.sleep(1)


def run_client(target_host, target_port, label):
    """Start a TCP client that connects to a server and then enters a send/receive loop."""
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                print(f"[{label}] Connecting to {target_host}:{target_port}...")
                s.connect((target_host, target_port))
                communicate(s, label)
        except Exception as e:
            print(f"[{label}] Connection error: {e}. Retrying...")
            time.sleep(1)


def communicate(conn, label):
    """Infinite loop sending and receiving messages."""
    counter = 0
    with conn:
        while True:
            # send message
            msg = f"{label} says hello #{counter}"
            print(f"[{label}] Sending: {msg}")
            conn.sendall(msg.encode())

            # receive response
            data = conn.recv(1024)
            if not data:
                print(f"[{label}] Peer disconnected")
                break

            print(f"[{label}] Received: {data.decode()}")

            counter += 1
            time.sleep(1)
