from nsak.core.scenario import ScenarioManager


def test_scenario_manager() -> None:
    """
    Tests if the scenario manager lists any scenario at all.

    This test could be improved by mocking the scenario library, but is good enough for now.
    """
    # Arrange

    # Act
    scenario_list = ScenarioManager.list()

    # Assert
    assert len(scenario_list) > 0

    # Act
    scenario = ScenarioManager.get(scenario_list[0].id)

    # Assert
    assert scenario is not None
