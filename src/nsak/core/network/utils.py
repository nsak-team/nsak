import logging

from scapy.all import conf
from scapy.interfaces import NetworkInterface

logger = logging.getLogger(__name__)


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


def get_network_interfaces() -> list[NetworkInterface]:
    """
    Return all available network interfaces.

    :return:
    """
    return list(conf.ifaces.values())


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


def get_network_interface_or_none(name: str) -> NetworkInterface | None:
    """
    Return a network interface by name or None if the interface cannot be found.
    """
    try:
        return get_network_interface(name)
    except NetworkInterfaceNotFoundError:
        # We ignore this error for now
        # logger.info(f"Network interface {name} is not available.")
        pass
    return None
