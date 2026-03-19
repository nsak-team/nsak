import dataclasses

from scapy.interfaces import NetworkInterface

from .types import IPInterface

# Interface flag to check if an interface is UP, where UNKNOWN is considered UP.
IFF_UP = 0x1


@dataclasses.dataclass(frozen=True, kw_only=True)
class IPConfiguration:
    """
    Represents an ip configuration on an interface.
    """

    ip: IPInterface
    is_target: bool
    is_management: bool


@dataclasses.dataclass(frozen=True, kw_only=True)
class EthernetConfiguration:
    """
    Represents an ethernet node.
    """

    name: str
    addresses: dict[str, IPConfiguration]

    # The underlying scapy NetworkInterface object is marked as private because it might change in future versions.
    _network_interface: NetworkInterface | None

    @property
    def ip(self) -> IPInterface | None:
        """
        Return the first ip address.

        :return:
        """
        if not self.ips:
            return None
        return self.ips[0]

    @property
    def ips(self) -> list[IPInterface]:
        """
        Return the first ip address.

        :return:
        """
        return [address.ip for address in self.addresses.values()]

    @property
    def is_up(self) -> bool:
        """
        Checks if an interface is not in state DOWN e.g., UP or UNKNOWN.

        :return:
        """
        if self._network_interface is None:
            return False
        return bool(self._network_interface.flags & IFF_UP)

    @property
    def is_target(self) -> bool:
        """
        Determine if an interface is a target interface, where attacks can be run.

        :return:
        """
        if self.name in ["lo", "::1"]:
            return False

        for address in self.addresses.values():
            if address.is_target:
                return True

        return False

    @property
    def is_management(self) -> bool:
        """
        Determine if an interface is a management interface, where nsak is being accessed or data can be extracted.

        :return:
        """
        if self.name in ["lo", "::1"]:
            return False

        for address in self.addresses.values():
            if address.is_management:
                return True

        return False


@dataclasses.dataclass(frozen=True, kw_only=True, eq=True)
class NetworkConfiguration:
    """
    Represents the networking part of the configuration, heavily inspired by netplan.
    """

    ethernets: dict[str, EthernetConfiguration]

    @property
    def target_ethernets(self) -> dict[str, EthernetConfiguration]:
        """

        :return:
        """
        return {
            name: ethernet
            for name, ethernet in self.ethernets.items()
            if ethernet.is_target
        }

    @property
    def management_ethernets(self) -> dict[str, EthernetConfiguration]:
        """

        :return:
        """
        return {
            name: ethernet
            for name, ethernet in self.ethernets.items()
            if ethernet.is_management
        }
