import dataclasses
import subprocess
from ipaddress import IPv4Address, IPv6Address

from nsak.core import NetworkInterface, IPAddress
from nsak.core.network import NetworkDiscoveryResultMap, NetworkDiscoveryResult, NetworkService, NetworkServiceEndpoint


@dataclasses.dataclass(frozen=True, kw_only=True)
class ARPScanResult:
    ip: IPAddress
    mac: str
    vendor: str


def parse_arp_scan_result(arp_scan_result_output: str) -> list[ARPScanResult]:
    """

    :param arp_scan_result_output:
    :return:
    """

    entries = []
    for line in arp_scan_result_output.splitlines():
        parts = line.split(None, 2)
        if len(parts) < 2:
            continue

        raw_ip, mac = parts[:2]
        try:
            ip = IPv4Address(raw_ip)
        except ValueError:
            ip = IPv6Address(raw_ip)
        vendor = parts[2] if len(parts) == 3 else ""
        arp_scan_result = ARPScanResult(ip=ip, mac=mac, vendor=vendor)
        entries.append(arp_scan_result)

    return entries


def discover_hosts(network_interface: NetworkInterface) -> NetworkDiscoveryResult:
    """
    Uses nmap to discover hosts on the provided network interfaces.

    :param network_interface:
    :return:
    """
    hosts: list[NetworkService] = []
    # --localnet: Generates addresses from the interface configuration
    # -x: Only prints results to the output (no headers, etc.)
    completed_process = subprocess.run([
        "/usr/sbin/arp-scan",
        "--interface", network_interface.name,
        "--localnet", "-x",
    ], capture_output=True, text=True, check=True)

    for arp_scan_result in parse_arp_scan_result(completed_process.stdout):
        host = NetworkService(
            endpoints=[
                NetworkServiceEndpoint(
                    ip=arp_scan_result.ip,
                    mac=arp_scan_result.mac,
                    extra_info=arp_scan_result.vendor,
                )
            ]
        )
        hosts.append(host)

    return NetworkDiscoveryResult(
        network_interface=network_interface,
        network_services=hosts
    )


def run(network_interfaces: list[NetworkInterface]) -> NetworkDiscoveryResultMap:
    """


    :param network_interfaces:
    :return:
    """
    results = dict()

    for network_interface in network_interfaces:
        results[network_interface] = discover_hosts(network_interface)

    # @TODO: It makes sense to create an own datastructure for host discovery results,
    # as it greatly diverges from the service discovery results and
    # forces a lot of fields to be optional with default None.
    return NetworkDiscoveryResultMap(results=results)
