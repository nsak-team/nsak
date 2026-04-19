from langchain_core.tools import Tool, tool

from ...drill.drill_manager import DrillManager


def generate_drill_tools() -> list[Tool]:
    """
    Register all NSAK drills as langchain tools for AI usage.
    """
    tools: list[Tool] = []
    drills = DrillManager.list()

    for drill in drills:
        entrypoint = DrillManager.get_drill_entrypoint(drill)
        tool(entrypoint, description=entrypoint.__doc__)

    return tools
