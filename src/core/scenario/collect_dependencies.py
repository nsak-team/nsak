from src.core.scenario.list_drills import list_drills
from src.core.scenario.scenario import Scenario, ScenarioDependencies


def collect_dependencies(scenario: Scenario) -> ScenarioDependencies:
    """
    List all dependencies including sub dependencies for a scenario.
    """
    system_dependencies = scenario.dependencies.system
    python_dependencies = scenario.dependencies.python
    for drill in list_drills(scenario):
        system_dependencies.update(drill.dependencies.system)
        python_dependencies.update(drill.dependencies.python)
    return ScenarioDependencies(
        system=system_dependencies,
        python=python_dependencies,
    )
