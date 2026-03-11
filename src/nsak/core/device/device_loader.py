from pathlib import Path
from typing import Any

from nsak.core.device.device import Device
from nsak.core.resource.resource_loader import ResourceLoader


class DeviceLoader(ResourceLoader[Device]):
    """
    Finds and loads devices from the library paths.
    """

    ResourceClass = Device

    @classmethod
    def _to_resource(cls, data: dict[str, Any], path: Path) -> Device:
        """
        Creates a Device object from a dict containing the device's metadata.
        """
        return cls.ResourceClass(
            id=str(data["metadata"]["id"]),
            name=str(data["metadata"]["name"]),
            path=path,
            author=str(data["metadata"]["author"]),
            repository=str(data["metadata"]["repository"]),
        )
