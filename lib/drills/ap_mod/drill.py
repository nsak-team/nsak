from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
import subprocess
import signal
import os
import logging
from typing import Any, Optional

from lib.drills.ap_mod.config import AccessPointConfig

logger = logging.getLogger(__name__)

_config_dir_path = Path("/run/nsak/hostapd")
_process: Optional[subprocess.Popen[str]] = None


def _write_hostapd_config(config: AccessPointConfig) -> Path:
    """
    Writes a minimal hostapd configuration file.
    """
    _config_dir_path.mkdir(parents=True, exist_ok=True)
    path = _config_dir_path / "hostapd.conf"

    lines: list[str] = []
    for key, value in asdict(config).items():
        if value is None:
            continue
        lines.append(f"{key}={value}")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def is_running() -> bool:
    return _process is not None and _process.poll() is None


def start(config: AccessPointConfig) -> int:
    """
    Start hostapd. Returns PID.
    """
    global _process

    if is_running():
        logger.warning("hostapd is already running (pid=%s)", _process.pid if _process else None)
        return _process.pid  # type: ignore[return-value]

    cfg_path = _write_hostapd_config(config)

    # Capture output for debugging
    _process = subprocess.Popen(
        ["/usr/sbin/hostapd", str(cfg_path)],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )  # noqa: S603

    logger.info("hostapd started with PID %s (cfg=%s)", _process.pid, cfg_path)
    return _process.pid


def run() -> dict[str, Any]:
    """
    Scenario entrypoint: create config, start hostapd, return result for cleanup.
    """
    config = AccessPointConfig()

    cfg_path = _write_hostapd_config(config)
    pid = start(config)

    logger.info("[Scenario] Rogue AP active on %s with SSID %s", config.interface, config.ssid)
    return {
        "pid": pid,
        "config_path": str(cfg_path),
        "interface": config.interface,
        "ssid": config.ssid,
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
