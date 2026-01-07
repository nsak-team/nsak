import logging
import os
import signal

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

# todo change args to network interface class from core
def run(args: dict, state: dict | None = None) -> dict:
    """
    Rogue AP orchestration.
    """
    ap_if = args.get("ap_interface") or os.getenv("NSAK_AP_IF")
    uplink_if = args.get("uplink_interface") or os.getenv("NSAK_UPLINK_IF")

    if not ap_if:
        raise KeyError("ap_interface (or NSAK_AP_IF) is required")
    if not uplink_if:
        raise KeyError("uplink_interface (or NSAK_UPLINK_IF) is required")

    state = state or {}
    results = {}

    hostapd = run_drill("ap_mod", state=state)
    net = run_drill("network_setup", ap_if)
    dnsmasq = run_drill("dnsmasq", ap_if)
    nat = run_drill("nat_forwarding", {"interface": ap_if, "uplink_interface": uplink_if})
    sniff = run_drill("tshark_capture", ap_if)
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
