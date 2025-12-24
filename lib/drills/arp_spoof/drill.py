import subprocess


def arp_spoof(iface: str, target_ip: str, spoof_ip: str) -> subprocess.Popen:
    """
    Start arp spoofing on the provided interface.

    :param iface:
    :param target_ip:
    :param spoof_ip:
    :return:
    """
    return subprocess.Popen(["arpspoof", "-i", iface, "-t", target_ip, spoof_ip])


def run(iface: str, target_ip: str, spoof_ip: str) -> subprocess.Popen:
    """
    Start arp spoofing on the provided interface.
    """
    return arp_spoof(iface, target_ip, spoof_ip)
