from __future__ import annotations

import dataclasses
import logging

from nsak.core.configuration.ai_configuration import AiConfiguration
from nsak.core.configuration.container_info import ContainerInfo
from nsak.core.configuration.email_configuration import EmailConfiguration
from nsak.core.configuration.loki_configuration import LokiConfiguration
from nsak.core.device import Device

logger = logging.getLogger(__name__)


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

    def save(self) -> None:
        """
        Shorthand proxy for ConfigManager save.
        """
        from .configuration_manager import ConfigurationManager

        ConfigurationManager.save(self)
