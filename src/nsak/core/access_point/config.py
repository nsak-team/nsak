from dataclasses import dataclass


@dataclass
class AccessPointConfig:
    """
    dataclass for config file for hostapd.
    """

    ssid: str = "BFH-Open"
    interface: str = "wlp59s0"
    channel: int = 6
    country_code: str = "CH"
    hw_mode: str = "g"
