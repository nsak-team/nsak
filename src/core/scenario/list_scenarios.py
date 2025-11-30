from src.core.scenario.scenario import Scenario
from src.core.scenario.scenario_loader import ScenarioLoader


def list_scenarios() -> list[Scenario]:
    """
    Lists all available scenarios.
    """
    scenario_loader = ScenarioLoader()
    return scenario_loader.load_all()
