import logging
import subprocess

logger = logging.getLogger(__name__)


def run(interface: str):
    # start process
    gateway_ip = "10.0.0.1/24"
    proc = subprocess.run(
        [
            "ip", "addr",
            "replace", gateway_ip,
            "dev", interface,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    logger.info(f"{proc.stdout} {gateway_ip} on {interface}")
