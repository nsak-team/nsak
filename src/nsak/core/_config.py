import dataclasses
import logging
from dataclasses import asdict
from ipaddress import IPv4Interface, IPv6Interface
from pathlib import PosixPath
from typing import Any, Self, cast

import yaml
from lazy_object_proxy import Proxy
from yaml import SafeDumper, ScalarNode

from .device import Device
from .settings import RUN_PATH


def represent_as_string(dumper: SafeDumper, data: Any) -> ScalarNode:  # noqa: ANN401
    """
    Used for serializing objects to strings (e.g., IPInterface or PosixPath).

    :param dumper:
    :param data:
    :return:
    """
    return dumper.represent_str(str(data))


yaml.add_representer(IPv6Interface, represent_as_string, Dumper=SafeDumper)
yaml.add_representer(IPv4Interface, represent_as_string, Dumper=SafeDumper)
yaml.add_representer(PosixPath, represent_as_string, Dumper=SafeDumper)

CONFIG_FILE = RUN_PATH / "config.yaml"


@dataclasses.dataclass(kw_only=True)
class Config:
    """
    Class for loading and saving the configuration.
    """

    debug: bool
    device: Device

    @classmethod
    def init(cls, **kwargs: Any) -> Self:  # noqa: ANN401
        """
        Initialize the config from data.
        """
        from .device.device_loader import DeviceLoader

        _config = cls(
            debug=kwargs.get("debug") or False,
            device=DeviceLoader.config_to_resource(
                cast(dict[str, Any], kwargs.get("device")), CONFIG_FILE
            ),
        )
        return _config

    @classmethod
    def init_default(cls) -> Self:
        """
        Initialize the default config.
        """
        from .device.device_manager import DeviceManager

        _config = cls(
            debug=True,
            device=DeviceManager.get("unknown"),
        )
        _config.save()
        return _config

    @classmethod
    def load(cls) -> Self:
        """
        Loads the config from file.
        """
        path = CONFIG_FILE
        try:
            with open(path) as file:
                data = yaml.safe_load(file) or {}
            _config = cls.init(**data)
        except (FileNotFoundError, TypeError):
            _config = cls.init_default()
        if _config.debug:
            logging.basicConfig(level=logging.DEBUG)
        return _config

    def save(self) -> None:
        """
        Persists the given runtime config to the file.
        """
        RUN_PATH.mkdir(parents=True, exist_ok=True)
        path = RUN_PATH / "config.yaml"
        data = asdict(self)

        with open(path, "w") as file:
            yaml.safe_dump(data, file)


config = Proxy(lambda: Config.load())
