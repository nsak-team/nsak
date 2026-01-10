import dataclasses

from scapy.all import conf
from scapy.interfaces import NetworkInterface as ScapyNetworkInterface

from nsak.core.config import MANAGEMENT_INTERFACES, TARGET_INTERFACES

# Interface flag to check if an interface is UP, where UNKNOWN is considered UP.
IFF_UP = 0x1


class NetworkInterfaceNotFoundError(Exception):
    """
    Exception raised when a network interface is not found.
    """

    def __init__(self, name: str) -> None:
        """
        Adds the interface name to the exception and sets a default message.
        """
        self.name = name
        message = f"NetworkInterface '{name}' not found."
        super().__init__(message)


@dataclasses.dataclass(frozen=True, kw_only=True)
class NetworkInterface:
    """
    Represents an interface.
    """

    # The underlying scapy NetworkInterface object is marked as private because it might change in future versions.
    _network_interface: ScapyNetworkInterface

    @property
    def name(self) -> str:
        """
        Returns the name of the interface.

        :return:
        """
        return str(self._network_interface.name)

    @property
    def nsak_ip(self) -> str:
        """
        Returns the main IP address of this device on the network interface.

        :return:
        """
        return str(self._network_interface.ip)

    @property
    def nsak_ips(self) -> list[str]:
        """
        Returns all IP addresses of this device on the network interface.

        :return:
        """
        return [str(ip) for ip in self._network_interface.ips]

    @property
    def is_up(self) -> bool:
        """
        Checks if an interface is not in state DOWN e.g., UP or UNKNOWN.

        :param iface:
        :return:
        """
        return bool(self._network_interface.flags & IFF_UP)

    @property
    def is_target(self) -> bool:
        """
        Determine if an interface is a target interface, where attacks can be run.

        :return:
        """
        # @TODO: Add logic to configure target interfaces, so that we don't run exploits on unwanted networks
        return self.name != "lo" and self.name not in TARGET_INTERFACES

    @property
    def is_management(self) -> bool:
        """
        Determine if an interface is a management interface, where nsak is being accessed or data can be extracted.

        :return:
        """
        # @TODO: Add logic to configure management interfaces.
        return self.name in MANAGEMENT_INTERFACES


def get_network_interfaces() -> list[NetworkInterface]:
    """
    Return all available network interfaces.

    :return:
    """
    network_interfaces: list[NetworkInterface] = []
    for network_interface in conf.ifaces.values():
        nsak_network_interface = NetworkInterface(
            _network_interface=network_interface,
        )
        network_interfaces.append(nsak_network_interface)

    return network_interfaces


def get_target_network_interfaces() -> list[NetworkInterface]:
    """
    Return all target network interfaces.

    :return:
    """
    return [iface for iface in get_network_interfaces() if iface.is_target]


def get_network_interface(name: str) -> NetworkInterface:
    """
    Return a network interface by name.

    :param name:
    :return:
    """
    for network_interface in get_network_interfaces():
        if network_interface.name == name:
            return network_interface

    raise NetworkInterfaceNotFoundError(name)
