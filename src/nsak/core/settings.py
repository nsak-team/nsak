import os
from pathlib import Path


def get_base_path() -> Path:
    """
    Returns the default base path.

    :return:
    """
    base_path = os.environ.get("NSAK_BASE_PATH", None)

    if base_path is not None:
        return Path(base_path)

    return Path(__file__).resolve().parents[3]


BASE_PATH = get_base_path()
RUN_PATH = BASE_PATH / "run"
LIBRARY_PATHS = {BASE_PATH / "lib"}
DOCKER_CONTEXT = BASE_PATH
