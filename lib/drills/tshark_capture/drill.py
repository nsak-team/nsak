import logging
import subprocess

from nsak.core.config import RUN_PATH

logger = logging.getLogger(__name__)
captures_dir = RUN_PATH / "captures"
captures_dir.mkdir(parents=True, exist_ok=True)

pcap_path = captures_dir / "rogue_ap.pcap"

def run(interface: str) -> subprocess.Popen:
    proc = subprocess.Popen([
        "tshark",
        "-i", interface,
        "-n",
        "-w", pcap_path
    ])
    logger.info("tshark pcap capture started")
    return proc

def cleanup(proc: subprocess.Popen) -> None:
    proc.terminate()
