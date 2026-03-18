import dataclasses
from pathlib import Path

from nsak.core.network.configuration import NetworkConfiguration
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
