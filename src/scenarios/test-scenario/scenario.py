"""
scenario entrypoint for drill POC

"""

import importlib.util
from pathlib import Path

# takes the absolut path from here. scenarios.test-scenario.scenario.py
BASE = Path(__file__).resolve().parents[2]
DRILLS = BASE / "drills"

# function to run the scenario in a container
def run():
    """
    Execute scenario
    :return: None
    print output
    """
    drill = "hello"
    drill_path = DRILLS / drill / "drill.py"

    spec = importlib.util.spec_from_file_location("drill-module",drill_path) # return spec of module
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    print("[Scenario] Drill returned:", module.run())

if __name__ == "__main__":
    run()