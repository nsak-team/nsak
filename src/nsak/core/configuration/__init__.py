from lazy_object_proxy import Proxy

from .ai_configuration import AiConfiguration
from .configuration import Configuration
from .configuration_manager import ConfigFieldInfo, ConfigurationManager
from .drawio_mcp_configuration import DrawioMCPConfiguration
from .email_configuration import EmailConfiguration, EmailEncryptionType
from .loki_configuration import LokiConfiguration

config: Configuration = Proxy(lambda: ConfigurationManager.load())

__all__ = (
    "AiConfiguration",
    "ConfigFieldInfo",
    "Configuration",
    "ConfigurationManager",
    "DrawioMCPConfiguration",
    "EmailConfiguration",
    "EmailEncryptionType",
    "LokiConfiguration",
    "config",
)
