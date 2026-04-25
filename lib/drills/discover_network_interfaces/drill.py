import os

from scapy.interfaces import NetworkInterface
from nsak.core.network.utils import get_network_interfaces

IFF_RUNNING = 0x40

def run() -> list[NetworkInterface]:
    """Return physical interfaces with an active link, excluding virtual and disconnected ones."""
    return [iface for iface in get_network_interfaces() if os.path.exists(f"/sys/class/net/{iface.name}/device") and iface.flags & IFF_RUNNING]
