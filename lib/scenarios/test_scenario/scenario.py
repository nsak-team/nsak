"""
scenario entrypoint for drill POC.
"""

import sys
from pathlib import Path
from nsak.core import DrillManager

# takes the absolut path from here. scenarios.test-scenario.scenarios.py
BASE = Path(__file__).resolve().parents[2]
DRILLS = BASE / "drills"


def run() -> None:
    """
    Example Scenario, which runs the Hello World Drill.

    :return: None
    """
    drill = DrillManager.get("hello_world")
    sys.stdout.write(f"[Scenario] Drill returned:\n\n")
    sys.stdout.write(DrillManager.execute(drill))


if __name__ == "__main__":
    run()
