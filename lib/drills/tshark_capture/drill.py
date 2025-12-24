import logging
import os
import signal
import subprocess

from nsak.core.config import RUN_PATH

logger = logging.getLogger(__name__)
run_path = RUN_PATH / "rouge_ap.pcap"

def run(interface: str) -> subprocess.Popen:
    proc = subprocess.Popen([
        "tshark",
        "-i", interface,
        "-n",
        "-w", run_path
    ])
    logger.info("tshark pcap capture started")
    return proc

def cleanup(proc: subprocess.Popen) -> None:
    proc.terminate()
