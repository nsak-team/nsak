"""
Scenario entrypoint for Reconnaissance .
"""
from scapy.arch import get_if_addr

from nsak.core import DrillManager
from nsak.core.network import NetworkDiscoveryResultMap


def _print_enumeration_findings(findings: dict[str, list[str]]) -> None:
    if not findings:
        print("\n### Service Enumeration: no findings ###\n")
        return
    print("\n### Service Enumeration Findings: ###\n")
    for endpoint, lines in findings.items():
        print(f"  {endpoint}:")
        for line in lines:
            print(f"    {line}")
    print("\n### -------------------------------- ###\n")


def run(interface: str | None = None, subnet: str | None = None) -> None:
    """
    Scenario, which runs Reconnaissance attack.
    1. If no interface is specified, scan all active physical interfaces
    2. If no interface is specified, scan all active physical interfaces
    3. Discover network on ifc and subnet
    :return: None
    """
    if interface is None:
        discovered = DrillManager.execute("discover_network_interfaces")
        interfaces_to_scan = [iface.name for iface in discovered]
    else:
        interfaces_to_scan = [interface]

    all_results = {}
    for iface_name in interfaces_to_scan:
        if get_if_addr(iface_name) in ("0.0.0.0", ""):
            DrillManager.execute("dhcp_request", interface=iface_name)

        result: NetworkDiscoveryResultMap = DrillManager.execute(
            "discover_hosts",
            interface=iface_name,
            subnet=subnet,
        )
        all_results.update(result.results)

    network_discovery_result_map = NetworkDiscoveryResultMap(results=all_results)
    DrillManager.execute("port_scan", discovery_result=network_discovery_result_map)
    print(network_discovery_result_map.display())
    print(network_discovery_result_map.as_table())

    findings: dict[str, list[str]] = DrillManager.execute(
        "enumerate_services", discovery_result=network_discovery_result_map
    )
    _print_enumeration_findings(findings)
