import dataclasses
import logging
from dataclasses import asdict
from datetime import datetime
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


@dataclasses.dataclass(frozen=True)
class ContainerInfo:
    """
    Runtime container identity, parsed from the container runtime environment.
    """

    id: str | None = None
    name: str | None = None


def _get_container_info() -> ContainerInfo:
    """
    Return container ID and name if running inside a container.

    Checks for Podman (/run/.containerenv) first, then Docker (/.dockerenv + cgroup).
    The name field is only available for Podman.
    """
    containerenv = Path("/run/.containerenv")
    if containerenv.exists():
        container_id = None
        container_name = None
        for line in containerenv.read_text(encoding="utf-8").splitlines():
            if line.startswith("id="):
                container_id = line.split("=", 1)[1].strip('"')
            elif line.startswith("name="):
                container_name = line.split("=", 1)[1].strip('"')
        return ContainerInfo(id=container_id, name=container_name)

    if Path("/.dockerenv").exists():
        try:
            for line in (
                Path("/proc/self/cgroup").read_text(encoding="utf-8").splitlines()
            ):
                parts = line.rsplit("/", 1)
                if len(parts) > 1 and len(parts[-1]) >= 12:
                    return ContainerInfo(id=parts[-1][:12])
        except OSError:
            pass

    return ContainerInfo()


def _get_log_file(container: ContainerInfo) -> Path:
    """
    Return the log file path.

    Uses the container ID as part of the filename when running inside a container.
    """
    now = datetime.now().astimezone()
    now_formated = now.strftime("%Y_%m_%d_%H_%M_%S")

    logs_path = RUN_PATH / "logs"
    logs_path.mkdir(parents=True, exist_ok=True)
    if container.name:
        log_filename = f"{now_formated}_{container.name}.log"
    else:
        log_filename = f"{now_formated}.log"
    return logs_path / log_filename


@dataclasses.dataclass(kw_only=True)
class Config:
    """
    Class for loading and saving the configuration.
    """

    debug: bool
    device: Device
    container: ContainerInfo = dataclasses.field(
        default_factory=ContainerInfo, compare=False
    )

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
            container=_get_container_info(),
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
            container=_get_container_info(),
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

        log_file = _get_log_file(_config.container)
        logging.basicConfig(
            level=logging.DEBUG if _config.debug else logging.INFO,
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler(log_file),
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
