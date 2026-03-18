import dataclasses
from pathlib import Path

from nsak.core.network.configuration import EthernetConfiguration, NetworkConfiguration
from nsak.core.resource import (
    InvalidResourceError,
    MultipleResourcesFoundError,
    Resource,
    ResourceError,
    ResourceNotFoundError,
)


@dataclasses.dataclass(frozen=True, kw_only=True, eq=True)
class DeviceConfigration:
    """
    Represents the device configuration.
    """

    raw: object
    network: NetworkConfiguration


@dataclasses.dataclass(frozen=True, kw_only=True, eq=True)
class Device(Resource):
    """
    Represents a device.
    """

    id: str
    name: str
    path: Path
    author: str
    repository: str
    configuration: DeviceConfigration | None = None

    @property
    def network(self) -> NetworkConfiguration | None:
        """
        Shortcut for accessing network configurations.
        """
        if self.configuration is None:
            return None

        return self.configuration.network

    @property
    def ethernets(self) -> dict[str, EthernetConfiguration]:
        """
        Shortcut for accessing ethernets.
        """
        if self.network is None:
            return {}

        return self.network.ethernets

    def get_ethernet(self, name: str) -> EthernetConfiguration:
        """
        Gets an ethernet configuration by interface name.

        :param name:
        :return:
        """
        if name not in self.ethernets:
            interfaces = ", ".join(self.ethernets.keys())
            message = (
                f"Could not find interface {name}, available options: {interfaces}"
            )
            raise ValueError(message)
        return self.ethernets[name]


class DeviceError(ResourceError):
    """
    Base class for device errors.
    """

    ResourceType = Device


class InvalidDeviceError(InvalidResourceError, DeviceError):
    """
    Exception raised when a device is invalid.
    """


class DeviceNotFoundError(ResourceNotFoundError, DeviceError):
    """
    Exception raised when a device is not found.
    """


class MultipleDevicesFoundError(MultipleResourcesFoundError, DeviceError):
    """
    Exception raised when multiple devices with the same folder name are found.
    """


# Avoids circularity issues
Device.ResourceError = DeviceError
Device.InvalidResourceError = InvalidDeviceError
Device.ResourceNotFoundError = DeviceNotFoundError
Device.MultipleResourcesFoundError = MultipleDevicesFoundError
