"""
Scenario entrypoint for Reconnaissance .
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
    print(network_discovery_result_map.display())
    print(network_discovery_result_map.as_table())





    # for iface, result in network_discovery_result_map.results.items():
    #     print(f"[{iface}]")
    #     for svc in result.network_services:
    #         for ep in svc.endpoints:
    #             print(f"  {ep.ip}  {ep.mac}  {ep.extra_info}")
