from dataclasses import dataclass


@dataclass
class AccessPointConfig:
    """
    dataclass for config file for hostapd.
    """

    ssid: str
    interface: str = "wlan0"
    channel: int = 6
    country_code: str = "CH"
    hw_mode: str = "g"
