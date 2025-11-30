from src.core.scenario import Scenario, ScenarioLoader


def list_scenarios() -> list[Scenario]:
    """
    Lists all available scenarios.
    """
    scenario_loader = ScenarioLoader()
    return scenario_loader.load_all()
