import logging
import os
import signal
import subprocess

logger = logging.getLogger(__name__)

def run_tshark(interface: str):
    proc = subprocess.Popen([
        "tshark",
        "-i", interface,
        "-n",
        "-w", "/tmp/rogue_ap.pcap"
    ])
    return proc


def run(args: dict) -> dict[str, any]:
    proc = run_tshark(args["interface"])
    logger.info("tshark pcap capture started")

    return {
        "pid": proc.pid,
        "pcap": "/tmp/rogue_ap.pcap",
        "interface": args["interface"],
    }


def cleanup(result: dict) -> None:
    pid = result.get("pid")
    if pid:
        os.kill(pid, signal.SIGINT)
    logger.info("tshark pcap capture stopped")
