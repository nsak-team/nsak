import dataclasses

from nsak.core import ScenarioLoader
from nsak.core.scenario.scenario import ScenarioArgument, ScenarioInterface


def test_scenario_loader_interface() -> None:
    """
    Tests if the scenario loader correctly loads the interface.

    This test could be improved by mocking the scenario library, but is good enough for now.
    """
    # Arrange
    expected_interface = ScenarioInterface(
        arguments={
            "interface": ScenarioArgument(
                type="str",
                default=dataclasses.MISSING,
            ),
        },
        return_type="None",
    )

    # Act
    scenario = ScenarioLoader.load("mitm")

    # Assert
    assert scenario.interface == expected_interface
