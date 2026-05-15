from __future__ import annotations

import dataclasses
import logging
from datetime import datetime
from zoneinfo import ZoneInfo

from nsak.core.configuration.ai_configuration import AiConfiguration
from nsak.core.configuration.container_info import ContainerInfo
from nsak.core.configuration.drawio_mcp_configuration import DrawioMCPConfiguration
from nsak.core.configuration.email_configuration import EmailConfiguration
from nsak.core.configuration.loki_configuration import LokiConfiguration
from nsak.core.device import Device

logger = logging.getLogger(__name__)

default_timezone = ZoneInfo("Europe/Zurich")


@dataclasses.dataclass(kw_only=True)
class Configuration:
    """
    Class for loading and saving the configuration.
    """

    from ..device.device_manager import DeviceManager

    debug: bool = dataclasses.field(default=True)
    device: Device = dataclasses.field(
        default_factory=DeviceManager.get_default,
    )
    container: ContainerInfo = dataclasses.field(
        default_factory=ContainerInfo.load,
    )
    email: EmailConfiguration | None = dataclasses.field(
        default=None,
    )
    ai: AiConfiguration | None = dataclasses.field(default=None)
    loki: LokiConfiguration | None = dataclasses.field(default=None)
    drawio_mcp: DrawioMCPConfiguration | None = dataclasses.field(default=None)

    datetime: str = dataclasses.field(
        default_factory=lambda: datetime.now(tz=default_timezone).isoformat()
    )
    running_scenario: str | None = dataclasses.field(default=None)

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

    def save(self) -> None:
        """
        Shorthand proxy for ConfigManager save.
        """
        from .configuration_manager import ConfigurationManager

        ConfigurationManager.save(self)
