import logging
import subprocess
from pathlib import Path

from nsak.core.settings import RUN_PATH

logger = logging.getLogger(__name__)
captures_dir = RUN_PATH / "captures"
captures_dir.mkdir(parents=True, exist_ok=True)

pcap_path = captures_dir / "rogue_ap.pcap"

def run(interface: str) -> tuple[subprocess.Popen, Path]:
    """
    Capture packages with tshark.
    """
    proc = subprocess.Popen([
        "tshark",
        "-i", interface,
        "-n",
        "-w", pcap_path
    ])
    logger.info("tshark pcap capture started")
    logger.info("----------------------------------------------------")
    return proc, pcap_path

def cleanup(proc: subprocess.Popen) -> None:
    proc.terminate()
