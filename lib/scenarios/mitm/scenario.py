"""
Scenario entrypoint for MITM with arp spoofing and transparent tcp proxy.
"""
from nsak.core import DrillManager
from nsak.core.network import NetworkDiscoveryResultMap


def run(interface: str) -> None:
    """
    Scenario, which runs MITM attack, based on arp spoofing.

    :return: None
    """
    network_discovery_result_map: NetworkDiscoveryResultMap = DrillManager.execute(
        "discover_hosts",
        interface=interface,
    )
    DrillManager.execute(
        "transparent_tcp_proxy",
        network_discovery_result_map=network_discovery_result_map,
    )
    DrillManager.execute(
        "arp_spoof",
        network_discovery_result_map=network_discovery_result_map
    )
