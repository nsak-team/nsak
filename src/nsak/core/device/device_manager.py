from nsak.core.device import Device
from nsak.core.device.device_loader import DeviceLoader
from nsak.core.resource.resource_manager import ResourceManager


class DeviceManager(ResourceManager[Device]):
    """
    A collection of methods to manage environments.
    """

    ResourceLoaderClass = DeviceLoader
