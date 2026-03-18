"""
Scenario entrypoint for MITM with arp spoofing and transparent tcp proxy.
"""
from typing import Any

from nsak.core import DrillManager, DeviceManager
from nsak.core.network import NetworkDiscoveryResultMap
from nsak.core.network.configuration import NetworkConfiguration


def run(
        network_interfaces: list[NetworkConfiguration] | None = None,
        *args: Any, **kwargs: Any
) -> None:
    """
    Scenario, which runs MITM attack, based on arp spoofing.

    :return: None
    """

    if not network_interfaces:
        loaded_device = DeviceManager.get_loaded()
        network_interfaces = loaded_device.configuration.network.target_ethernets.values()

    network_discovery_result_map: NetworkDiscoveryResultMap = DrillManager.execute(
        "discover_hosts",
        network_interfaces=network_interfaces,
    )
    DrillManager.execute(
        "transparent_tcp_proxy",
        network_discovery_result_map=network_discovery_result_map,
    )
    DrillManager.execute(
        "arp_spoof",
        network_discovery_result_map=network_discovery_result_map
    )
