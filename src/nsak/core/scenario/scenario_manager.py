import importlib.util
import subprocess
import sys
from typing import Any, List

from nsak.core import config
from nsak.core.drill import Drill, DrillLoader
from nsak.core.scenario import Scenario, ScenarioDependencies, ScenarioLoader
from nsak.core.scenario.scenario_loader import ScenarioNotFoundError


class ScenarioManager:
    """
    A collection of methods to manage scenarios.
    """

    @classmethod
    def list(cls) -> list[Scenario]:
        """
        Lists all available scenarios.
        """
        return ScenarioLoader.load_all()

    @classmethod
    def get(cls, name: str) -> Scenario:
        """
        Get a scenario by name.
        """
        return ScenarioLoader.load(name)

    @classmethod
    def build(cls, scenario: Scenario) -> None:
        """
        Build a scenario for deployment.
        """
        dependencies = cls.collect_dependencies(scenario)
        system_dependencies = " ".join(dependencies.system)
        python_dependencies = " ".join(dependencies.python)

        # @TODO: This is potentially insecure and we should replace it with a library:
        # - https://pypi.org/project/docker/
        # - https://pypi.org/project/podman/
        subprocess.run(  # noqa: S603
            [
                "/usr/sbin/sudo",
                "/usr/sbin/podman",
                "build",
                "--network=host",
                config.DOCKER_CONTEXT,
                "-t",
                f"nsak/scenario/{scenario.path.name}",
                "--build-arg",
                f"SYSTEM_DEPENDENCIES={system_dependencies}",
                "--build-arg",
                f"PYTHON_DEPENDENCIES={python_dependencies}",
                "--build-arg",
                f"SCENARIO={scenario.path.name}",
            ]
        )

    @classmethod
    def run(cls, scenario: Scenario, env_file: str | None = None) -> int:
        """
        Run a scenario image.
        """
        # @TODO: This is potentially insecure and we should replace it with a library:
        # - https://pypi.org/project/docker/
        # - https://pypi.org/project/podman/
        args = [
            "/usr/sbin/sudo",
            "/usr/sbin/podman",
            "run",
            "-d",
            "--rm",
            "--privileged",
            "--network=host",
            f"--name={scenario.path.name}",
            f"nsak/scenario/{scenario.path.name}",
        ]
        if env_file is not None:
            args.extend(["--env-file", env_file])
        completed_process = subprocess.run(args)  # noqa: S603
        return completed_process.returncode

    @classmethod
    def collect_dependencies(cls, scenario: Scenario) -> ScenarioDependencies:
        """
        List all dependencies including sub dependencies for a scenario.
        """
        system_dependencies = scenario.dependencies.system
        python_dependencies = scenario.dependencies.python
        for drill in cls.list_drills(scenario):
            system_dependencies.update(drill.dependencies.system)
            python_dependencies.update(drill.dependencies.python)
        return ScenarioDependencies(
            system=system_dependencies,
            python=python_dependencies,
        )

    @classmethod
    def list_drills(cls, scenario: Scenario) -> List[Drill]:
        """
        List all drills of a scenario.
        """
        drills: list[Drill] = []
        drill_loader = DrillLoader()
        for drill_name in scenario.drills:
            drill = drill_loader.load(drill_name)
            drills.append(drill)
        return drills

    @classmethod
    def execute(cls, scenario: Scenario | str, *args: Any, **kwargs: Any) -> Any:  # noqa: ANN401
        """
        Load the scenarios entrypoint and execute it.
        """
        if isinstance(scenario, str):
            scenario = cls.get(scenario)

        module_name = scenario.path.name
        spec = importlib.util.spec_from_file_location(
            module_name, scenario.path / "scenario.py"
        )
        if spec is None:
            raise ScenarioNotFoundError(scenario.name)
        module = importlib.util.module_from_spec(spec)
        if module is None:
            raise ScenarioNotFoundError(scenario.name)
        sys.modules[module_name] = module
        if spec.loader is None:
            raise ScenarioNotFoundError(scenario.name)
        spec.loader.exec_module(module)
        return module.run(*args, **kwargs)
