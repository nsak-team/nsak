from __future__ import annotations

import os
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from nsak.core.device.device import Device


def parse_list(env_var: str, default: list[str] | None = None) -> list[str]:
    """
    Parse a comma separated list of strings.

    :param default:
    :param env_var:
    :return:
    """
    raw = os.environ.get(env_var, None)
    if raw is None:
        return default or []
    return [item.strip() for item in raw.split(",") if item.strip()]


ENV_BASE_PATH = os.environ.get("NSAK_BASE_PATH", None)
ENV_LIBRARY_PATH = os.environ.get("NSAK_LIBRARY_PATH", None)
ENV_RUN_PATH = os.environ.get("NSAK_RUN_PATH", None)

BASE_PATH = (
    Path(ENV_BASE_PATH) if ENV_BASE_PATH else Path(__file__).resolve().parents[3]
)
LIBRARY_PATHS = {Path(ENV_LIBRARY_PATH) if ENV_LIBRARY_PATH else BASE_PATH / "lib"}
DEBUG = True
DOCKER_CONTEXT = BASE_PATH
RUN_PATH = Path(ENV_RUN_PATH) if ENV_RUN_PATH else BASE_PATH.joinpath("run")
DEVICE_FILE = RUN_PATH / "device.yaml"
LOADED_DEVICE: Device = None  # type: ignore
