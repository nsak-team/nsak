import tempfile
from pathlib import Path

from .config import AccessPointConfig


class HostapdManager:
    """
    Hostapd manager class.

        - writes a hostapd configuration file
        - starts a hostapd process
        - stops a hostapd process
        - logging

        expectation:
            - hostapd is in PATH via container via apt installed
            - Wifi interfaces existed and is configured for AP-Mode
    """

    def __init__(self, config_dir: Path | None = None) -> None:
        if config_dir is None:
            config_dir = Path(tempfile.mkdtemp(prefix="nsak-"))
        self._config_dir = config_dir

        # todo how can I open a process?
        """ vllt als subprocess """

    def _write_hostapd_config(self, config: AccessPointConfig) -> Path:
        """
        Writes a minimal hostapd configuration file.
        """
        self._config_dir.mkdir(parents=True, exist_ok=True)
        path = self._config_dir / "hostapd.conf"

        lines = [
            f"interface={config.interface}",
            "driver=nl80211",
            f"ssid={config.ssid}",
            f"hw_mode={config.hw_mode}",
            f"channel={config.channel}",
            f"country_code={config.country_code}",
        ]

        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return path
