import os
from pathlib import Path

ENV_BASE_PATH = os.environ.get("NSAK_BASE_PATH", None)
ENV_LIBRARY_PATH = os.environ.get("NSAK_LIBRARY_PATH", None)

BASE_PATH = (
    Path(ENV_BASE_PATH) if ENV_BASE_PATH else Path(__file__).resolve().parents[3]
)
LIBRARY_PATHS = {Path(ENV_LIBRARY_PATH) if ENV_LIBRARY_PATH else BASE_PATH / "lib"}
DEBUG = True
DOCKER_CONTEXT = BASE_PATH
