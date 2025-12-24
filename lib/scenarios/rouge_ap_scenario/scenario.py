"""
scenario entrypoint for drill POC.
"""
import sys

from nsak.core import Drill, DrillLoader, DrillManager
from nsak.core.access_point.config import AccessPointConfig
from nsak.core.access_point.hostapd_manager import HostapdManager


def run() -> None:
    """
    Example Scenario, which runs the Hello World Drill.

    :return: None
    """

    hostapd_manager = HostapdManager()
    config = AccessPointConfig()
    hostapd_manager.start(config)

    print(f"[Scenario] Rouge AP active on {config.interface} with SSID {config.ssid}.")
    drill = DrillManager.get("dnsmasq")
    sys.stdout.write(f"[Scenario] Drill returned:\n\n")
    sys.stdout.write(DrillManager.execute(drill))


if __name__ == "__main__":
    run()
