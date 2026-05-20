from __future__ import annotations

import logging
import uuid
from copy import deepcopy
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from nsak.core.configuration.ai_configuration import AiConfiguration
from nsak.core.configuration.container_info import ContainerInfo
from nsak.core.configuration.drawio_mcp_configuration import DrawioMCPConfiguration
from nsak.core.configuration.email_configuration import EmailConfiguration
from nsak.core.configuration.loki_configuration import LokiConfiguration
from nsak.core.device import Device
from nsak.core.settings import RUN_PATH

logger = logging.getLogger(__name__)


def get_default_timezone() -> ZoneInfo:
    """
    Return the default timezone.
    """
    return ZoneInfo("Europe/Zurich")


@dataclass(kw_only=True)
class Configuration:
    """
    Class for loading and saving the configuration.
    """

    from ..device.device_manager import DeviceManager

    debug: bool = field(default=True)
    device: Device = field(
        default_factory=DeviceManager.get_default,
    )
    container: ContainerInfo = field(
        default_factory=ContainerInfo.load,
    )
    run_uuid: uuid.UUID = field(default_factory=uuid.uuid4)
    email: EmailConfiguration | None = field(
        default=None,
    )
    ai: AiConfiguration | None = field(default=None)
    loki: LokiConfiguration | None = field(default=None)
    drawio_mcp: DrawioMCPConfiguration | None = field(default=None)

    timezone: ZoneInfo = field(default_factory=get_default_timezone)
    timestamp: datetime = field(init=False)
    running_scenario: str | None = field(default=None)

    def __post_init__(self) -> None:
        """
        Initialize fields, which have dependencies to other fields.
        """
        self.timestamp = self.now()

    def set_running_scenario(self, scenario: str) -> None:
        """
        Set the name of the currently running scenario for logging.
        """
        from nsak.core.configuration import ConfigurationManager

        self.running_scenario = scenario
        ConfigurationManager.update_loki_handler(self)

    def reset_running_scenario(self) -> None:
        """
        Reset the running scenario name to none.
        """
        from nsak.core.configuration import ConfigurationManager

        self.running_scenario = None
        ConfigurationManager.update_loki_handler(self)

    def reset_run_uuid(self) -> uuid.UUID:
        """
        Set a new run uuid and return it.

        Used when multiple runs are executed in the same cli command.
        """
        self.run_uuid = uuid.uuid4()
        return self.run_uuid

    def save(self) -> None:
        """
        Shorthand proxy for ConfigManager save.
        """
        from .configuration_manager import ConfigurationManager

        ConfigurationManager.save(self)

    def now(self) -> datetime:
        """
        Returns the current timestamp in the configured timezone.
        """
        return datetime.now(tz=self.timezone)

    @property
    def work_path(self) -> Path:
        """
        Current working directory.
        """
        directories = [
            "work_paths",
            f"{self.timestamp.strftime('%Y-%m-%d-%H:%M:%S')}",
        ]
        work_path = RUN_PATH.joinpath(*directories)
        work_path.mkdir(mode=0o777, parents=True, exist_ok=True)

        return work_path

    def scrub(self) -> Configuration:
        """
        Return a scrubbed copy of the config.
        """
        scrubbed = deepcopy(self)

        scrubbed.ai = None
        scrubbed.email = None
        scrubbed.loki = None
        scrubbed.drawio_mcp = None

        return scrubbed
