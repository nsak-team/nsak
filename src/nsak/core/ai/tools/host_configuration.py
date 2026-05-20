from typing import Any

from langchain.tools import tool

from nsak.core.configuration import config
from nsak.core.configuration.configuration_serializer import ConfigurationSerializer


@tool  # type: ignore[misc]
def host_configuration() -> dict[str, Any]:
    """
    Returns the host network configuration as a dictionary.

    Use this tool first to understand the local network setup before running any scans or attacks.

    The returned dictionary has the following structure:
    {
        "debug": bool,
        "device": {
            "id": str,
            "name": str,
            "description": str,
            "configuration": {
                "network": {
                    "ethernets": {
                        "<interface_name>": {
                            "name": str,
                            "is_up": bool,        # False means the interface is DOWN, skip it
                            "is_target": bool,    # True means this interface is used for attacks/scans
                            "is_management": bool # True means this interface is used for device access
                            "addresses": {
                                "<cidr>": {
                                    "ip": str,        # e.g. "10.10.10.5/24" - use this as nmap source IP
                                    "is_target": bool,
                                    "is_management": bool,
                                }
                            },
                        }
                    }
                }
            }
        }
    }

    Guidance:
    - Use `is_target=True` interfaces/IPs when running nmap scans or attacks
    - Skip interfaces where `is_up=False`
    - Use `is_management=True` interfaces for device access or data extraction
    - `configuration` may be None if the device has not been configured yet
    """
    return ConfigurationSerializer.serialize(config.scrub())
