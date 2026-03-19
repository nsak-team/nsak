import logging
import os
import signal
from typing import Any

logger = logging.getLogger(__name__)

from nsak.core.drill.drill_manager import DrillManager

def _disabled_drills() -> set[str]:
    """
    helper function to set env var for drill disabling.
    :return:
    """
    raw = os.getenv("NSAK_DISABLE_DRILLS", "")
    return {d.strip() for d in raw.split(",") if d.strip()}

DISABLED = _disabled_drills()

def run_drill(name: str, *args, **kwargs):
    """
    helper function to disable certain drills

    :param name:
    :param args:
    :param kwargs:
    :return:
    """
    if name in DISABLED:
        logger.info("Skipping drill %s (disabled via NSAK_DISABLE_DRILLS)", name)
        return None
    return DrillManager.execute(DrillManager.get(name), *args, **kwargs)

def run(wlan_interface: str, uplink_interface: str) -> dict[str, Any]:
    """
    Rogue AP orchestration.
    """
    if not wlan_interface:
        raise KeyError("ap_interface (or NSAK_AP_IF) is required")
    if not uplink_interface:
        raise KeyError("uplink_interface (or NSAK_UPLINK_IF) is required")

    state = {}
    results = {}

    hostapd = run_drill("ap_mod", state=state)
    net = run_drill("network_setup", wlan_interface)
    dnsmasq = run_drill("dnsmasq", wlan_interface)
    nat = run_drill("nat_forwarding", {"interface": wlan_interface, "uplink_interface": uplink_interface})
    sniff = run_drill("tshark_capture", wlan_interface)
    results["hostapd"] = hostapd
    results["net"] = net
    results["dnsmasq"] = dnsmasq
    results["nat"] = nat
    results["sniff"] = sniff

    signal.pause()  # keep scenario alive after all drills are up

    return {
        "processes": {
            "dnsmasq_pid": results["dnsmasq"]["pid"],
            "hostapd_pid": results["hostapd"]["pid"],
            "tshark_pid": results["tshark"]["pid"],
        },
        "state": state,
    }


def cleanup(state: dict) -> None:
    """
    Stop all running drills.
    """
    for name in reversed(["sniff", "nat", "dnsmasq", "network", "ap_mod"]):
        result = state.get(name)
        if not result:
            continue
        DrillManager.clean_up(
            DrillManager.get(name if name != "sniff" else "tshark_capture"),
        )
