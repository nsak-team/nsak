import os
from pathlib import Path


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

RUN_PATH = Path(ENV_RUN_PATH) if ENV_RUN_PATH else Path("/run/nsak")
BASE_PATH = (
    Path(ENV_BASE_PATH) if ENV_BASE_PATH else Path(__file__).resolve().parents[3]
)
LIBRARY_PATHS = {Path(ENV_LIBRARY_PATH) if ENV_LIBRARY_PATH else BASE_PATH / "lib"}
DEBUG = True
DOCKER_CONTEXT = BASE_PATH

TARGET_INTERFACES = parse_list("TARGET_INTERFACES")
MANAGEMENT_INTERFACES = parse_list("MANAGEMENT_INTERFACES")
MANAGEMENT_NETWORKS = parse_list("NSAK_MANAGEMENT_NETWORKS")
