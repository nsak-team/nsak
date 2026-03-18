import logging

import nsak
from nsak.core import DeviceManager
from nsak.core.config import DEBUG, DEVICE_FILE, RUN_PATH
from nsak.core.device.device import Device
from nsak.core.device.device_loader import DeviceLoader


def setup() -> None:
    """
    Set up the nsak core.
    """
    if DEBUG:
        logging.basicConfig(level=logging.DEBUG)

    RUN_PATH.mkdir(parents=True, exist_ok=True)
    DEVICE_FILE.touch(exist_ok=True)
    try:
        nsak.core.config.LOADED_DEVICE = DeviceLoader.load_by_path(RUN_PATH)
    except Device.InvalidResourceError:
        DeviceManager.unload()
