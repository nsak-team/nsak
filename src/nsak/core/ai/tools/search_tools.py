from langchain.tools import tool
from langchain_core.tools import BaseTool


def make_search_tools(all_tools: list[BaseTool]) -> BaseTool:
    """
    Factory that returns a search_tools tool with closure over all_tools.

    The agent uses this to discover tools before performing tasks instead of
    receiving all tools at once.
    """

    @tool  # type: ignore[misc]
    def search_tools(query: str) -> str:
        """Search available tools by keyword. Always call this before performing a task.

        Examples
        --------
        - search_tools("reconnaissance") — find network scanning and host discovery tools
        - search_tools("diagram") or search_tools("drawio") — find diagram creation tools
        - search_tools("email") — find email tools
        - search_tools("port") — find port scanning tools

        Args:
            query: Keyword to search for in tool names and descriptions.

        Returns
        -------
            A list of matching tools with their descriptions.
        """
        matches = [
            f"- {t.name}: {t.description}"
            for t in all_tools
            if query.lower() in t.name.lower()
            or query.lower() in (t.description or "").lower()
        ]
        return "\n".join(matches) if matches else f"No tools found for '{query}'."

    return search_tools
