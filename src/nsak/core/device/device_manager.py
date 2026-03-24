from nsak.core.device import Device
from nsak.core.device.device_loader import DeviceLoader
from nsak.core.resource.resource_manager import ResourceManager


class DeviceManager(ResourceManager[Device]):
    """
    A collection of methods to manage environments.
    """

    ResourceLoaderClass = DeviceLoader

    @classmethod
    def load(cls, name: str) -> Device:
        """
        Get a resource by name.
        """
        from nsak.core import config

        device = cls.get(name)
        config.device = device
        config.save()
        return device

    @classmethod
    def unload(cls) -> None:
        """
        Load the unknown device.
        """
        cls.load("unknown")
