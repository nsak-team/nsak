from ipaddress import ip_interface
from pathlib import Path
from typing import Any

from nsak.core.device.device import (
    Device,
    DeviceConfigration,
    EthernetConfiguration,
    IPConfiguration,
    NetworkConfiguration,
)
from nsak.core.resource.resource_loader import ResourceLoader


class DeviceLoader(ResourceLoader[Device]):
    """
    Finds and loads devices from the library paths.
    """

    ResourceClass = Device

    @classmethod
    def _parse_device_configuration(
        cls, data: dict[str, Any]
    ) -> DeviceConfigration | None:
        if "configuration" not in data:
            return None

        ethernets = data["configuration"].get("network", {}).get("ethernets", {})

        return DeviceConfigration(
            network=NetworkConfiguration(
                ethernets={
                    interface: EthernetConfiguration(
                        name=interface,
                        addresses={
                            ip: IPConfiguration(
                                ip=ip_interface(ip),
                                is_target=address.get("is_target", False),
                                is_management=address.get("is_management", False),
                            )
                            for ip, address in ethernet.get("addresses", {}).items()
                        },
                    )
                    for interface, ethernet in ethernets.items()
                }
            )
        )

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
            configuration=cls._parse_device_configuration(data),
        )
