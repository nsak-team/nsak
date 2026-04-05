import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


def get_base_path() -> Path:
    """
    Returns the default base path.

    :return:
    """
    base_path = os.getenv("NSAK_BASE_PATH", None)

    if base_path is not None:
        return Path(base_path)

    return Path(__file__).resolve().parents[3]


def get_library_paths() -> set[Path]:
    """
    Returns a list of library paths.

    :return:
    """
    library_paths = {BASE_PATH / "lib"}

    library_path = os.getenv("NSAK_LIBRARY_PATH", None)

    if library_path is not None:
        library_paths.add(Path(library_path))

    return library_paths


BASE_PATH = get_base_path()
RUN_PATH = BASE_PATH / "run"
LIBRARY_PATHS = get_library_paths()
DOCKER_CONTEXT = BASE_PATH
OLLAMA_BASE_URL = os.getenv("NSAK_OLLAMA_BASE_URL", None)
AI_MODEL = os.getenv("NSAK_AI_MODEL", None)
