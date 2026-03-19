import shutil

import nsak.core.config
from nsak.core.config import DEVICE_FILE, RUN_PATH
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
        device = cls.get(name)
        source_file = device.path / "device.yaml"
        shutil.copy(source_file, DEVICE_FILE)
        nsak.core.config.LOADED_DEVICE = DeviceLoader.load_by_path(RUN_PATH)
        return device

    @classmethod
    def get_loaded(cls) -> Device | None:
        """
        Return the active device.
        """
        return nsak.core.config.LOADED_DEVICE

    @classmethod
    def unload(cls) -> None:
        """
        Unload the loaded device.
        """
        with open(DEVICE_FILE, "r+") as file:
            file.truncate(0)
        nsak.core.config.LOADED_DEVICE = None
