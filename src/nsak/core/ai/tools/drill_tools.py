from langchain_core.tools import BaseTool, StructuredTool

from ...drill.drill_manager import DrillManager


def generate_drill_tools() -> list[BaseTool]:
    """
    Register all NSAK drills as langchain tools for AI usage.
    """
    tools: list[BaseTool] = []
    drills = DrillManager.list()

    for drill in drills:
        entrypoint = DrillManager.get_drill_entrypoint(drill)
        tools.append(
            StructuredTool.from_function(
                func=entrypoint,
                name=drill.id,
                description=entrypoint.__doc__ or drill.name,
            )
        )

    return tools
