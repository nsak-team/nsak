from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import subprocess
import signal
import os
import logging
from typing import Any, Optional

@dataclass
class HostapdConfig:
    ssid: str = "bfh−open"
    interface: str = "wlan0"
    channel: int = 6
    country_code: str = "CH"
    hw_mode: str = "g"

logger = logging.getLogger(__name__)

_config_dir_path = Path("/run/nsak/hostapd")
_process: Optional[subprocess.Popen[str]] = None


def _write_hostapd_config(ap_config: HostapdConfig) -> Path:
    """
    Writes a minimal hostapd configuration file.
    """
    _config_dir_path.mkdir(parents=True, exist_ok=True)
    path = _config_dir_path / "hostapd.conf"

    lines: list[str] = []
    for key, value in asdict(ap_config).items():
        if value is None:
            continue
        lines.append(f"{key}={value}")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def is_running() -> bool:
    return _process is not None and _process.poll() is None


def start(ap_config: HostapdConfig) -> int:
    """
    Start hostapd. Returns PID.
    """
    global _process

    if is_running():
        logger.warning("hostapd is already running (pid=%s)", _process.pid if _process else None)
        return _process.pid  # type: ignore[return-value]

    cfg_path = _write_hostapd_config(ap_config)

    # Capture output for debugging
    _process = subprocess.Popen(
        ["/usr/sbin/hostapd", str(cfg_path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )  # noqa: S603
    logger.info("[Scenario] Starting hostapd %s", ap_config.interface)
    return _process.pid


#  todo use explicit arguments, maybe with the same data structure as used in MITM scenario
def run() -> dict[str, Any]:
    """
    Scenario entrypoint: create config, start hostapd, return result for cleanup.
    """
    ap_config = HostapdConfig()

    cfg_path = _write_hostapd_config(ap_config)
    pid = start(ap_config)

    logger.info("[Scenario] Rogue AP active on %s with SSID %s", ap_config.interface, ap_config.ssid)
    logger.info("----------------------------------------------------")

    return {
        "pid": pid,
        "config_path": str(cfg_path),
        "interface": ap_config.interface,
        "ssid": ap_config.ssid,
    }


def cleanup(result: dict) -> None:
    """
    Stop hostapd gracefully; fall back to SIGKILL if needed.
    """
    global _process

    pid = result.get("pid")
    if not pid and _process is not None:
        pid = _process.pid

    if not pid:
        return

    try:
        os.kill(pid, signal.SIGTERM)
    except ProcessLookupError:
        _process = None
        return

    # Wait shortly and use SIGKILL if still alive
    if _process is not None:
        try:
            _process.wait(timeout=3)
        except subprocess.TimeoutExpired:
            try:
                os.kill(pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
        finally:
            _process = None
