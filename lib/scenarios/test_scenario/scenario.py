"""
scenario entrypoint for drill POC.
"""

import importlib.util
import sys
from pathlib import Path

# takes the absolut path from here. scenarios.test-scenario.scenarios.py
BASE = Path(__file__).resolve().parents[2]
DRILLS = BASE / "drills"


def run() -> None:
    """
    Example Scenario, which runs the Hello World Drill.

    :return: None
    """
    drill = "hello_world"
    drill_path = DRILLS / drill / "drill.py"

    spec = importlib.util.spec_from_file_location(
        "drill-module", drill_path
    )  # return spec of module
    if spec is None or spec.loader is None:
        message = "Failed to load drill module."
        raise Exception(message)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    sys.stdout.write(f"[Scenario] Drill returned: {module.run()}")


if __name__ == "__main__":
    run()
