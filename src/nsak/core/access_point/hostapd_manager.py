import logging
import subprocess
import tempfile
from dataclasses import asdict
from pathlib import Path
from typing import Optional

from .config import AccessPointConfig

logger = logging.getLogger(__name__)


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

    def __init__(self, config_dir_path: Path | None = None) -> None:
        if config_dir_path is None:
            config_dir_path = Path(tempfile.mkdtemp(prefix="nsak-"))
        self._config_dir_path = config_dir_path
        self._process: Optional[subprocess.Popen[bytes]] = None

    def _write_hostapd_config(self, config: AccessPointConfig) -> Path:
        """
        Writes a minimal hostapd configuration file.
        """
        self._config_dir_path.mkdir(parents=True, exist_ok=True)
        path = self._config_dir_path / "hostapd.conf"
        lines = []

        for key, value in asdict(config).items():
            lines.append(f"{key}={value}")

        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return path

    def is_running(self) -> bool:
        """
        :return: True if hostapd is running
        """
        return self._process is not None

    def start(self, config: AccessPointConfig) -> None:
        """
        Starts a hostapd process.

        :return: ProcessId
        """
        if self.is_running():
            logger.warning("hostapd is already running")
            return

        cfg_path = self._write_hostapd_config(config)
        self._process = subprocess.Popen(["/usr/sbin/hostapd", str(cfg_path)])  # noqa: S603

        logger.info("hostapd started with PID %s", self._process.pid)

    def stop(self) -> None:
        """
        Stops a hostapd process.

        :return:
        """
        if self._process is None:
            logger.debug("hostapd stop requested, but no process is running")
            return

        self._process.terminate()
        logger.info("hostapd stopped with PID %s", self._process.pid)
