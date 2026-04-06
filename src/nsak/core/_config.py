import dataclasses
import logging
from dataclasses import asdict
from ipaddress import IPv4Interface, IPv6Interface
from pathlib import Path, PosixPath
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


def _get_container_id() -> str | None:
    """
    Return the container ID if running inside a container, else None.

    Checks for Podman (/run/.containerenv) first, then Docker (/.dockerenv + cgroup).
    """
    containerenv = Path("/run/.containerenv")
    if containerenv.exists():
        for line in containerenv.read_text(encoding="utf-8").splitlines():
            if line.startswith("id="):
                return line.split("=", 1)[1].strip('"')

    if Path("/.dockerenv").exists():
        try:
            for line in (
                Path("/proc/self/cgroup").read_text(encoding="utf-8").splitlines()
            ):
                parts = line.rsplit("/", 1)
                if len(parts) > 1 and len(parts[-1]) >= 12:
                    return parts[-1][:12]
        except OSError:
            pass

    return None


@dataclasses.dataclass(kw_only=True)
class Config:
    """
    Class for loading and saving the configuration.
    """

    debug: bool
    device: Device
    container_id: str | None = dataclasses.field(default=None, compare=False)

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
            container_id=_get_container_id(),
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
            container_id=_get_container_id(),
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

        logs_path = RUN_PATH / "logs"
        logs_path.mkdir(parents=True, exist_ok=True)
        log_filename = (
            f"nsak_{_config.container_id}.log" if _config.container_id else "nsak.log"
        )
        logging.basicConfig(
            level=logging.DEBUG if _config.debug else logging.INFO,
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler(logs_path / log_filename),
            ],
        )
        return _config

    def asdict(self) -> dict[str, Any]:
        """
        Serializes the config object to a python dictionary.
        """
        return asdict(self)

    def save(self) -> None:
        """
        Persists the given runtime config to the file.
        """
        RUN_PATH.mkdir(parents=True, exist_ok=True)
        path = RUN_PATH / "config.yaml"

        with open(path, "w") as file:
            yaml.safe_dump(self.asdict(), file)


config: Config = Proxy(lambda: Config.load())
