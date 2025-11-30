from src.core.scenario import Scenario, ScenarioLoader


def get_scenario(name: str) -> Scenario:
    """
    Get a scenario by name.
    """
    scenario_loader = ScenarioLoader()
    return scenario_loader.load(name)
