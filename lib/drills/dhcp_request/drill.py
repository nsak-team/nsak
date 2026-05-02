import logging
import subprocess

logger = logging.getLogger(__name__)


def run(interface) -> None:
    """
    Request dynamic IP address

    param: interface
    Returns: None
    """
    proc = subprocess.run(
        [
            "dhclient",
            interface
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
