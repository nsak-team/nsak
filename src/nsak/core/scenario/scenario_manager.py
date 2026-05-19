import asyncio
import dataclasses
import importlib.util
import inspect
import logging
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, List

import yaml

from nsak.core import settings
from nsak.core.drill import Drill, DrillLoader
from nsak.core.resource import ResourceManager
from nsak.core.scenario import Scenario, ScenarioDependencies, ScenarioLoader
from nsak.core.settings import RUN_PATH

logger = logging.getLogger(__name__)


class ScenarioArgumentParsingError(ValueError):
    """
    Exception thrown when argument parsing fails.
    """

    pass


class ScenarioLifecycleError(Exception):
    """
    Exception thrown when a scenario cannot be started, stopped or killed.
    """

    pass


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


class ScenarioManager(ResourceManager[Scenario]):
    """
    A collection of methods to manage scenarios.
    """

    ResourceLoaderClass = ScenarioLoader

    @classmethod
    def _parse_arguments(cls, scenario: Scenario, **kwargs: Any) -> dict[str, Any]:  # noqa: ANN401
        """
        Parse arguments for drill execution.

        :param kwargs:
        :return:
        """
        arguments = {}
        for name, argument in scenario.interface.arguments.items():
            if argument.default is dataclasses.MISSING and (
                name not in kwargs or kwargs[name] is None
            ):
                message = f"Required argument {name} is missing."
                raise ScenarioArgumentParsingError(message)
            value = (
                kwargs.get(name) if kwargs.get(name) is not None else argument.default
            )
            if value is not None and type(value).__name__ not in argument.type:
                message = f"Invalid type {type(value)} for argument {name}, expected {argument.type}."
                raise ScenarioArgumentParsingError(message)
            arguments[name] = value
        return arguments

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
                settings.DOCKER_CONTEXT,
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
    def build_run_args(cls, scenario: Scenario, **kwargs: Any) -> list[str]:  # noqa: ANN401
        """
        Build run scenario args.
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

        args = [
            "/usr/sbin/sudo",
            "/usr/sbin/podman",
            "run",
            "--interactive",
            "--tty",
            "--privileged",
            "--network=host",
            f"--name={scenario.path.name}",
        ]
        # mounts (scenario-specific)
        for m in runtime.mounts:
            # ensure host dir exists
            os.makedirs(m.host_path, exist_ok=True)
            args += ["-v", f"{m.host_path}:{m.container_path}:{m.mode}"]
        # Fallback mount
        if not runtime.mounts:
            args += ["-v", f"{RUN_PATH.absolute()}:/nsak/run/:rw"]

        # env pass-through (scenario-specific)
        for key in runtime.env:
            val = os.environ.get(key)
            if val:
                args += ["-e", f"{key}={val!s}"]

        args.append(f"nsak/scenario/{scenario.path.name}")
        args.append(scenario.path.name)
        for key, value in kwargs.items():
            if value is not None:
                args.extend([f"--{key}", str(value)])

        return args

    @classmethod
    def run(cls, scenario: Scenario, **kwargs: Any) -> int:  # noqa: ANN401
        """
        Run a scenario image.
        """
        args = cls.build_run_args(scenario, **kwargs)
        completed_process = subprocess.run(args)  # noqa: S603
        return completed_process.returncode

    @classmethod
    def _running_container_ids(cls, scenario: Scenario) -> list[str]:
        """
        Return IDs of all running containers based on the scenario image.
        """
        image = f"nsak/scenario/{scenario.path.name}"
        result = subprocess.run(  # noqa: S603
            [
                "/usr/bin/sudo",
                "/usr/bin/podman",
                "ps",
                "-q",
                "--filter",
                f"ancestor={image}",
            ],
            capture_output=True,
            text=True,
        )
        return [cid for cid in result.stdout.splitlines() if cid]

    @classmethod
    def stop(cls, scenario: Scenario) -> None:
        """
        Stop all running containers based on the scenario image.
        """
        container_ids = cls._running_container_ids(scenario)
        if not container_ids:
            return
        completed_process = subprocess.run(  # noqa: S603
            ["/usr/bin/sudo", "/usr/bin/podman", "stop", *container_ids]
        )
        if completed_process.returncode != 0:
            message = f"Could not stop scenario {scenario.path.name}, return code: {completed_process.returncode}"
            raise ScenarioLifecycleError(message)

    @classmethod
    def kill(cls, scenario: Scenario) -> None:
        """
        Forcefully kill all running containers based on the scenario image (SIGKILL, last resort).
        """
        container_ids = cls._running_container_ids(scenario)
        if not container_ids:
            return
        completed_process = subprocess.run(  # noqa: S603
            ["/usr/bin/sudo", "/usr/bin/podman", "kill", *container_ids]
        )
        if completed_process.returncode != 0:
            message = f"Could not kill scenario {scenario.path.name}, return code: {completed_process.returncode}"
            raise ScenarioLifecycleError(message)

    @classmethod
    def kill_all(cls) -> None:
        """
        Forcefully kill all known scenario containers (SIGKILL, last resort).

        Attempts to kill every scenario; collects errors and raises after all attempts.
        """
        errors: list[str] = []
        for scenario in cls.list():
            try:
                cls.kill(scenario)
            except ScenarioLifecycleError as e:
                errors.append(str(e))
        if errors:
            raise ScenarioLifecycleError("\n".join(errors))

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
        from nsak.core.configuration import config

        if isinstance(scenario, str):
            scenario = cls.get(scenario)

        arguments = cls._parse_arguments(scenario, **kwargs)

        module_name = scenario.path.name
        spec = importlib.util.spec_from_file_location(
            module_name, scenario.path / "scenario.py"
        )
        if spec is None:
            raise Scenario.ResourceNotFoundError(scenario.name)
        module = importlib.util.module_from_spec(spec)
        if module is None:
            raise Scenario.ResourceNotFoundError(scenario.name)
        sys.modules[module_name] = module
        if spec.loader is None:
            raise Scenario.ResourceNotFoundError(scenario.name)
        spec.loader.exec_module(module)

        run_fn = getattr(module, "run", None)

        if run_fn is None:
            message = f"Scenario '{scenario.name}' has no 'run' function or coroutine."
            raise Scenario.InvalidResourceError(message)

        config.set_running_scenario(scenario.name)
        message = "EXEC %s SCENARIO: %s"

        if inspect.iscoroutinefunction(run_fn):
            logger.info(message, "ASYNC", scenario.name)
            result = asyncio.run(run_fn(**arguments))
        elif inspect.isfunction(run_fn):
            logger.info(message, "SYNC", scenario.name)
            result = run_fn(**arguments)
        else:
            message = f"Scenario '{scenario.name}.run' is not a function or coroutine."
            raise Scenario.InvalidResourceError(message)

        config.reset_running_scenario()
        # In the future the scenarios should always return a subclass of `ScenarioResult`,
        # afterward the typehint of this method could be changed accordingly.
        # This is already realized for `ai_reconnaissance` and `reconnaissance`.
        return result
