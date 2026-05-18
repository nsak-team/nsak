import logging
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(os.getenv("NSAK_ENV_FILE", None))

logger = logging.getLogger()


def get_base_path() -> Path:
    """
    Returns the default base path.

    :return:
    """
    base_path = os.getenv("NSAK_BASE_PATH", None)

    if base_path is not None:
        return Path(base_path).absolute()

    return Path(__file__).resolve().parents[3].absolute()


def get_run_path() -> Path:
    """
    Returns the run path.

    :return:
    """
    run_path = os.getenv("NSAK_RUN_PATH", None)

    if run_path is not None:
        return Path(run_path).absolute()

    return (get_base_path() / "run").absolute()


def get_library_paths() -> set[Path]:
    """
    Returns a list of library paths.

    :return:
    """
    library_paths = set()

    default_path = (BASE_PATH / "lib").absolute()
    if default_path.exists():
        library_paths.add(default_path)

    library_path = os.getenv("NSAK_LIBRARY_PATH", None)
    if library_path is not None:
        _library_path = Path(library_path).absolute()
        if not _library_path.exists():
            message = (
                f"Library path '{library_path}' in NSAK_LIBRARY_PATH does not exist!"
            )
            logger.warning(message)
        library_paths.add(_library_path)

    return library_paths


BASE_PATH = get_base_path()
RUN_PATH = get_run_path()
BENCHMARK_PATH = RUN_PATH.joinpath("benchmarks")
LIBRARY_PATHS = get_library_paths()
CONFIG_FILE = (RUN_PATH / "config.yaml").absolute()
DOCKER_CONTEXT = BASE_PATH
