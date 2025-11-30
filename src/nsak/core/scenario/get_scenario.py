from nsak.core.scenario.scenario import Scenario
from nsak.core.scenario.scenario_loader import ScenarioLoader


def get_scenario(name: str) -> Scenario:
    """
    Get a scenario by name.
    """
    scenario_loader = ScenarioLoader()
    return scenario_loader.load(name)
