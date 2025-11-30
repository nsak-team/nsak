from nsak.core.drill import Drill, DrillLoader
from nsak.core.scenario.scenario import Scenario


def list_drills(scenario: Scenario) -> list[Drill]:
    """
    List all drills of a scenario.
    """
    drills: list[Drill] = []
    drill_loader = DrillLoader()
    for drill_name in scenario.drills:
        drill = drill_loader.load(drill_name)
        drills.append(drill)
    return drills
