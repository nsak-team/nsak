import importlib.util
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, List

import yaml

from nsak.core import config
from nsak.core.drill import Drill, DrillLoader
from nsak.core.scenario import Scenario, ScenarioDependencies, ScenarioLoader
from nsak.core.scenario.scenario_loader import ScenarioNotFoundError


# TODO: Keep flexibility low with default mount /runtime/<scenario-name>
@dataclass(frozen=True)
class RuntimeMount:
    """
    Describes a host container bind mount during scenario execution.
    """

    host_path: str
    container_path: str
    mode: str = "rw"


@dataclass(frozen=True)
class RuntimeSpec:
    """
    Describes environment variables and runtime mounts.

    required for scenario container execution.
    """

    env: list[str]
    mounts: list[RuntimeMount]


def load_manifest(path: Path) -> dict[str, Any]:
    """
    Loads the manifest from the yaml file path.

    :param path:
    :return: dict[str, Any] from yaml
    """
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def parse_runtime(manifest: dict[str, Any]) -> RuntimeSpec:
    """
    Parse the runtime manifest and return a RuntimeSpec object.

    :param manifest:
    :return: RuntimeSpec
    """
    runtime = manifest.get("runtime") or {}
    env = list(runtime.get("env") or [])
    mounts_raw = list(runtime.get("mounts") or [])
    mounts = [
        RuntimeMount(
            host_path=m["host_path"],
            container_path=m["container_path"],
            mode=m.get("mode", "rw"),
        )
        for m in mounts_raw
    ]
    return RuntimeSpec(env=env, mounts=mounts)


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
                "/usr/bin/sudo",
                "/usr/bin/podman",
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
    def run(cls, scenario: Scenario) -> int:
        """
        Run a scenario image.
        """
        # @TODO: This is potentially insecure and we should replace it with a library:
        # - https://pypi.org/project/docker/
        # - https://pypi.org/project/podman/
        manifest = load_manifest(scenario.path / "scenario.yaml")
        runtime = parse_runtime(manifest)
        # ensure clean container
        subprocess.run(  # noqa: S603
            ["/usr/bin/sudo", "/usr/bin/podman", "rm", "-f", scenario.path.name],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        cmd = [
            "/usr/bin/sudo",
            "/usr/bin/podman",
            "run",
            "-d",
            "--privileged",
            "--network=host",
            f"--name={scenario.path.name}",
            "-e",
            "PYTHONPATH=/nsak",  # set env path for python
        ]

        # mounts (scenario-specific)
        for m in runtime.mounts:
            # ensure host dir exists
            os.makedirs(m.host_path, exist_ok=True)
            cmd += ["-v", f"{m.host_path}:{m.container_path}:{m.mode}"]

        # env pass-through (scenario-specific)
        for key in runtime.env:
            val = os.environ.get(key)
            if val:
                cmd += ["-e", f"{key}={val!s}"]

        # image name
        cmd.append(f"nsak/scenario/{scenario.path.name}")

        completed_process = subprocess.run(  # noqa: S603
            cmd,
            text=True,
            capture_output=True,
        )

        if completed_process.returncode != 0:
            error_msg = (
                f"podman run failed rc= {completed_process.returncode} | stdout:{completed_process.stdout} "
                f"stderr: {completed_process.stderr} "
            )

            raise RuntimeError(error_msg)

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
