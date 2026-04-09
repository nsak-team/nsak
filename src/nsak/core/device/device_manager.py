from nsak.core.device import Device
from nsak.core.device.device_loader import DeviceLoader
from nsak.core.resource.resource_manager import ResourceManager


class DeviceManager(ResourceManager[Device]):
    """
    A collection of methods to manage environments.
    """

    ResourceLoaderClass = DeviceLoader
    default_device = "unknown"

    @classmethod
    def get_default(cls) -> Device:
        """
        Get the default resource.
        """
        return cls.get(cls.default_device)

    @classmethod
    def load(cls, name: str) -> Device:
        """
        Load a resource by name and store it in the config.
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
        cls.load(cls.default_device)
