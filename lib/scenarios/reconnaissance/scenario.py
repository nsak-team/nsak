"""
Scenario entrypoint for Reconnaissance .
"""
from nsak.core import DrillManager
from nsak.core.network import NetworkDiscoveryResultMap


def run(interface: str) -> None:
    """
    Scenario, which runs Reconnaissance attack.

    :return: None
    """
    # discover subnets
    # ip address assignment dhcp
    # ip address assignment static
    # SNMP Ports/Interfaces auf switch und router

    interfaces = DrillManager.execute(
        "get_network_interfaces" )
    interface_name = interfaces[0].name,

    network_discovery_result_map: NetworkDiscoveryResultMap = DrillManager.execute(
        "discover_hosts",
        interface=interface_name,
    )
    DrillManager.execute(
        "port_scan",
        discovery_result=network_discovery_result_map,
    )
    print(network_discovery_result_map.display())
    print(network_discovery_result_map.as_table())

    # for iface, result in network_discovery_result_map.results.items():
    #     print(f"[{iface}]")
    #     for svc in result.network_services:
    #         for ep in svc.endpoints:
    #             print(f"  {ep.ip}  {ep.mac}  {ep.extra_info}")
