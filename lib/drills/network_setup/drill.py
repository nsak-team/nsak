import logging
import subprocess

logger = logging.getLogger(__name__)


def run(interface: str, gateway_ip: str = "10.0.0.1/24") -> None:
    """
    Configure NSAK as the default gateway for the provided subnet on the given interface.

    This is used in other drill like the nat forwarding drill.
    """

    # start process
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
    logger.info("----------------------------------------------------")
