import subprocess
from typing import Any, List

from nsak.core.environment import Environment, EnvironmentLoader
from nsak.core.network import get_network_interface
from nsak.core.network.network_interface import NetworkInterfaceNotFoundError
from nsak.core.scenario import Scenario, ScenarioLoader, ScenarioManager

ENVIRONMENT_SIMULATION_IFACE = "nsak0"
ENVIRONMENT_SIMULATION_IFACE_SETUP = f"""
A dummy interface named {ENVIRONMENT_SIMULATION_IFACE} is required for simulation.

Create a dummy interface for simulation:
sudo ip link add {ENVIRONMENT_SIMULATION_IFACE} type dummy
sudo ip link set {ENVIRONMENT_SIMULATION_IFACE} up

Verify that the interface was created successfully and is in state UP or UNKNOWN:
ip link show {ENVIRONMENT_SIMULATION_IFACE}
"""
ENVIRONMENT_SIMULATION_IFACE_DOWN = f"""
The dummy interface {ENVIRONMENT_SIMULATION_IFACE} is DOWN, use the following command to bring it up:
sudo ip link set {ENVIRONMENT_SIMULATION_IFACE} up

Verify that the interface is in state UP or UNKNOWN:
ip link show {ENVIRONMENT_SIMULATION_IFACE}
"""


class EnvironmentManager:
    """
    A collection of methods to manage environments.
    """

    @classmethod
    def list(cls) -> List[Environment]:
        """
        Lists all environments.
        """
        return EnvironmentLoader.load_all()

    @classmethod
    def get(cls, name: str) -> Environment:
        """
        Get an environment by name.
        """
        return EnvironmentLoader.load(name)

    @classmethod
    def list_scenarios(cls, environment: Environment | str) -> List[Scenario]:
        """
        List all available scenarios of an environment.

        :param environment:
        :return:
        """
        if isinstance(environment, str):
            environment = cls.get(environment)

        scenarios = ScenarioLoader.load_all()
        return [
            scenario
            for scenario in scenarios
            if environment.path.name in scenario.environments
        ]

    @classmethod
    def _verify_simulation_network_interface(cls) -> None:
        try:
            dummy_network_interface = get_network_interface(
                ENVIRONMENT_SIMULATION_IFACE
            )
        except NetworkInterfaceNotFoundError as e:
            raise RuntimeError(ENVIRONMENT_SIMULATION_IFACE_SETUP) from e

        if not dummy_network_interface.is_up:
            raise RuntimeError(ENVIRONMENT_SIMULATION_IFACE_DOWN)

    @classmethod
    def simulate(
        cls,
        environment: Environment | str,
        scenario: Scenario | str,
        *args: Any,  # noqa: ANN401
        **kwargs: Any,  # noqa: ANN401
    ) -> Any:  # noqa: ANN401
        """
        Simulate a scenario in an environment.
        """
        cls._verify_simulation_network_interface()

        if isinstance(environment, str):
            environment = cls.get(environment)
        if isinstance(scenario, str):
            scenario = ScenarioManager.get(scenario)

        compose_files = [
            environment.path / "compose.yaml",
            scenario.path / "environments" / environment.path.name / "compose.yaml",
        ]

        # @TODO: This is potentially insecure and we should replace it with a library:
        # - https://pypi.org/project/docker/
        # - https://pypi.org/project/podman/
        return subprocess.run(  # noqa: S603
            [
                "/usr/sbin/sudo",
                "/usr/sbin/podman-compose",
                *[
                    file_arg
                    for compose_file in compose_files
                    for file_arg in ("-f", str(compose_file))
                ],
                "up",
                "--pull",
                "--force-recreate",
            ],
            # cwd=str(environment.path),
        )
