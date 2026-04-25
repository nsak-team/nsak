"""
Scenario entrypoint for Reconnaissance .
"""
from scapy.arch import get_if_addr

from nsak.core import DrillManager
from nsak.core.network import NetworkDiscoveryResultMap


def run(interface: str | None = None, subnet: str | None = None) -> None:
    """
    Scenario, which runs Reconnaissance attack.

    :return: None
    """
    if interface is None:
        discovered = DrillManager.execute("discover_network_interfaces")
        interface_name = discovered[0].name
    else:
        interface_name = interface

    if get_if_addr(interface_name) in ("0.0.0.0", ""):
        DrillManager.execute("dhcp_request", interface=interface_name)

    network_discovery_result_map: NetworkDiscoveryResultMap = DrillManager.execute(
        "discover_hosts",
        interface=interface_name,
        subnet=subnet,
    )
    DrillManager.execute("port_scan", discovery_result=network_discovery_result_map)
    print(network_discovery_result_map.display())
    print(network_discovery_result_map.as_table())

    # for iface, result in network_discovery_result_map.results.items():
    #     print(f"[{iface}]")
    #     for svc in result.network_services:
    #         for ep in svc.endpoints:
    #             print(f"  {ep.ip}  {ep.mac}  {ep.extra_info}")
