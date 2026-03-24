from ipaddress import ip_interface
from pathlib import Path
from typing import Any

from nsak.core.device.device import (
    Device,
    DeviceConfigration,
)
from nsak.core.network.configuration import (
    EthernetConfiguration,
    IPConfiguration,
    NetworkConfiguration,
)
from nsak.core.network.utils import (
    get_network_interfaces,
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
        network = data["configuration"].get("network") or {}
        if network == "auto":
            ethernets = {}
            for interface in get_network_interfaces():
                ethernets[interface.name] = {
                    "addresses": {
                        ip: {
                            "is_target": True,
                            "is_management": False,
                        }
                        for ips in interface.ips.values()
                        for ip in ips
                    }
                }
        else:
            ethernets = network.get("ethernets") or {}

        return DeviceConfigration(
            raw=data["configuration"],
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
            ),
        )

    @classmethod
    def _to_resource(cls, id: str, data: dict[str, Any], path: Path | str) -> Device:
        """
        Creates a Device object from a dict containing the device's metadata.
        """
        if isinstance(path, str):
            path = Path(path)

        return cls.ResourceClass(
            id=id,
            name=str(data.get("name") or ""),
            description=str(data.get("description") or ""),
            path=path,
            author=str(data.get("author") or ""),
            repository=str(data.get("repository") or ""),
            configuration=cls._parse_device_configuration(data),
        )
