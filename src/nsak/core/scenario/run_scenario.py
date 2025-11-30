import subprocess

from nsak.core.scenario.scenario import Scenario


def run_scenario(scenario: Scenario) -> int:
    """
    Run a scenario image.
    """
    # @TODO: This is potentially insecure and we should replace it with a library:
    # - https://pypi.org/project/docker/
    # - https://pypi.org/project/podman/
    completed_process = subprocess.run(  # noqa: S603
        [
            "/usr/bin/podman",
            "run",
            scenario.path.name,
        ]
    )
    return completed_process.returncode
