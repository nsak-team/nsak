from pathlib import Path

BASE_PATH = Path(__file__).resolve().parents[3]
LIBRARY_PATHS = {
    BASE_PATH / "lib",
}
DEBUG = True
DOCKER_CONTEXT = BASE_PATH
