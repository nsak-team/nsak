import logging
from typing import Any

from langchain.agents.middleware import AgentMiddleware
from langchain.agents.middleware.types import wrap_model_call
from langchain_core.tools import BaseTool

logger = logging.getLogger(__name__)


def make_progressive_disclosure(
    all_tools: list[BaseTool], core_tools: set[str]
) -> AgentMiddleware:
    """Returns middleware that starts the agent with a minimal core tool set.

    Unlocks additional tools as the agent calls search_tools("keyword").
    """
    all_tools_map = {t.name: t for t in all_tools}

    @wrap_model_call  # type: ignore[misc]
    async def progressive_disclosure(request: Any, handler: Any) -> Any:  # noqa: ANN401
        active = set(core_tools)

        for msg in getattr(request, "messages", []):
            for tc in getattr(msg, "tool_calls", []):
                name = (
                    tc.get("name")
                    if isinstance(tc, dict)
                    else getattr(tc, "name", None)
                )
                if name != "search_tools":
                    continue
                args = (
                    tc.get("args", {})
                    if isinstance(tc, dict)
                    else getattr(tc, "args", {})
                )
                query = args.get("query", "").lower()
                for tool_name, t in all_tools_map.items():
                    if (
                        query in tool_name.lower()
                        or query in (t.description or "").lower()
                    ):
                        active.add(tool_name)

        filtered = [t for t in request.tools if hasattr(t, "name") and t.name in active]
        logger.info("Active tools (%d): %s", len(filtered), [t.name for t in filtered])
        return await handler(request.override(tools=filtered))

    return progressive_disclosure
