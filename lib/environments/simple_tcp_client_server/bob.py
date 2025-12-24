# bob.py
from connection import run_server

HOST = "0.0.0.0"
PORT = 5000

if __name__ == "__main__":
    run_server(HOST, PORT, label="Bob")
