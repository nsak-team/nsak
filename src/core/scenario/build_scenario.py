import subprocess

from src.core import config
from src.core.config import BASE_PATH
from src.core.scenario import Scenario
from src.core.scenario.collect_dependencies import collect_dependencies


def build_scenario(scenario: Scenario) -> None:
    """
    Build a scenario for deployment.
    """
    dependencies = collect_dependencies(scenario)
    system_dependencies = " ".join(dependencies.system)
    python_dependencies = " ".join(dependencies.python)

    # @TODO: This is potentially insecure and we should replace it with a library:
    # - https://pypi.org/project/docker/
    # - https://pypi.org/project/podman/
    subprocess.run(  # noqa: S603
        [
            "/usr/bin/podman",
            "build",
            config.DOCKER_CONTEXT,
            "-t",
            scenario.path.name,
            "--build-arg",
            f"SYSTEM_DEPENDENCIES={system_dependencies}",
            "--build-arg",
            f"PYTHON_DEPENDENCIES={python_dependencies}",
            "--build-arg",
            f"SCENARIO_PATH={scenario.path.relative_to(BASE_PATH)}",
        ]
    )
