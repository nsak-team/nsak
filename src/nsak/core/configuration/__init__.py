from lazy_object_proxy import Proxy

from .ai_configuration import AiConfiguration
from .configuration import Configuration
from .configuration_manager import ConfigFieldInfo, ConfigurationManager
from .email_configuration import EmailConfiguration, EmailEncryptionType

config: Configuration = Proxy(lambda: ConfigurationManager.load())

__all__ = (
    "AiConfiguration",
    "ConfigFieldInfo",
    "Configuration",
    "ConfigurationManager",
    "EmailConfiguration",
    "EmailEncryptionType",
    "config",
)
