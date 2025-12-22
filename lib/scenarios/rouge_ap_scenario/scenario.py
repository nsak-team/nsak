from nsak.core.drill.drill_manager import DrillManager


def run(args: dict, state: dict | None = None) -> dict:
    """
    Rogue AP orchestration.
    """
    state = state or {}
    results = {}

    ap_if = args["ap_interface"]
    uplink_if = args["uplink_interface"]

    # Start ap_mod (AP mode)
    hostapd = DrillManager.execute(
        DrillManager.get("ap_mod"),
        state=state,
    )
    results["ap_mod"] = hostapd

    # Network setup set static Ip for nsak to work as Gateway (Nsak is AP, DHCP, DNS)
    net = DrillManager.execute(
        DrillManager.get("network_setup"),
        {
            "interface": ap_if,
            "address": "10.0.0.1/24",
        },
        state=state,
    )
    results["network"] = net

    # DHCP + DNS (with dnsmasq range and lease time)
    dnsmasq = DrillManager.execute(
        DrillManager.get("dnsmasq"),
        {
            "interface": ap_if,
        },
        state=state,
    )
    results["dnsmasq"] = dnsmasq

    # todo add Nat rules to forward the packets to Gateway

    nat = DrillManager.execute(
        DrillManager.get("nat_forwarding"),
        {
            "interface": ap_if,
            "uplink_interface": uplink_if
        }, state=state,
    )
    results["nat"] = nat

    # todo Traffic sniffing
    # sniff = DrillManager.execute(
    #     DrillManager.get("tshark_capture"),
    #     {
    #         "interface": ap_if,
    #         "capture_filter": "port 53",
    #     },
    #     state=state,
    # )
    # results["sniff"] = sniff

    return results


def cleanup(state: dict) -> None:
    """
    Stop all running drills.
    """
    for name in reversed(["sniff", "nat", "dnsmasq", "network", "ap_mod"]):
        result = state.get(name)
        if not result:
            continue
        DrillManager.clear(
            DrillManager.get(name if name != "sniff" else "tshark_capture"),
            result,
        )
