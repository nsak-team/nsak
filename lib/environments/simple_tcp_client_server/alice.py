from connection import run_client

BOB_HOST = "10.10.10.20"
BOB_PORT = 5000

if __name__ == "__main__":
    run_client(BOB_HOST, BOB_PORT, label="Alice")
