import asyncio
import logging
from pprint import pformat
from typing import Any, AsyncGenerator, Awaitable, Callable, Iterable, Sequence

from langchain.agents import create_agent
from langchain.agents.middleware import AgentMiddleware
from langchain.agents.structured_output import ToolStrategy
from langchain_anthropic.chat_models import ChatAnthropic
from langchain_core.callbacks import AsyncCallbackHandler
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import ToolMessage
from langchain_core.outputs import LLMResult
from langchain_core.tools import BaseTool
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_ollama.chat_models import ChatOllama
from langchain_openai.chat_models import ChatOpenAI
from langgraph.prebuilt.tool_node import ToolCallRequest
from langgraph.types import Command

from nsak.core.ai.tools import (
    cli_tool,
    generate_drill_tools,
    host_configuration,
    human_interaction_hook,
    send_email,
)
from nsak.core.configuration import Configuration, config

logger = logging.getLogger(__name__)


class TrackToolCallMiddleware(AgentMiddleware):  # type: ignore
    """
    Tool tracking middleware.
    """

    def __init__(self, tools_available: Iterable[str]) -> None:
        """
        Init tool tracking middleware.
        """
        self.tools_called: dict[str, list[str]] = {
            tool: [] for tool in set(tools_available)
        }

    async def awrap_tool_call(
        self,
        request: ToolCallRequest,
        handler: Callable[[ToolCallRequest], Awaitable[ToolMessage | Command[Any]]],
    ) -> ToolMessage | Command[Any]:
        """
        Track async tool calls.
        """
        tool_name = request.tool_call["name"]
        tool_args = request.tool_call["args"]

        self.tools_called.setdefault(tool_name, [])
        self.tools_called[tool_name].append(str(tool_args))

        return await handler(request)

    def wrap_tool_call(
        self,
        request: ToolCallRequest,
        handler: Callable[[ToolCallRequest], ToolMessage | Command[Any]],
    ) -> ToolMessage | Command[Any]:
        """
        Track sync tool calls.
        """
        tool_name = request.tool_call["name"]
        tool_args = request.tool_call["args"]

        self.tools_called.setdefault(tool_name, [])
        self.tools_called[tool_name].append(str(tool_args))

        return handler(request)


class UsageCallback(AsyncCallbackHandler):  # type: ignore
    """
    Track token usage and tool calls.
    """

    def __init__(self) -> None:
        """
        Init token usage.
        """
        self.prompt_tokens = 0
        self.completion_tokens = 0
        self.total_tokens = 0

    async def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:  # noqa: ANN401
        """
        Capture the token usage.
        """
        if response.llm_output is None:
            # Fallback: sum usage from generations (present when streaming)
            for generations in response.generations:
                for gen in generations:
                    if not hasattr(gen, "message"):
                        continue
                    _usage = getattr(gen.message, "usage_metadata", None)
                    if _usage is None:
                        logger.warning("No usage metadata in on_llm_end!")
                        return
                    self.prompt_tokens += _usage.get("input_tokens", 0)
                    self.completion_tokens += _usage.get("output_tokens", 0)
                    self.total_tokens += _usage.get("total_tokens", 0)
            return

        usage: dict[str, int] = (
            response.llm_output.get("token_usage")
            or response.llm_output.get("usage")
            or {}
        )
        if usage is None:
            logger.warning("No token usage in on_llm_end!")
            return
        prompt = usage.get("prompt_tokens") or usage.get("input_tokens", 0)
        completion = usage.get("completion_tokens") or usage.get("output_tokens", 0)
        self.prompt_tokens += prompt
        self.completion_tokens += completion
        self.total_tokens += usage.get("total_tokens") or (prompt + completion)


def create_chat_ollama(
    model: str, base_url: str, api_key: str | None, kwargs: dict[str, Any]
) -> BaseChatModel:
    """
    Create ChatOllama instance.
    """
    if api_key is not None:
        kwargs.update({"Authorization": f"Bearer {api_key}"})

    return ChatOllama(model=model, base_url=base_url, **kwargs)


PROVIDER_MAP: dict[
    str, Callable[[str, str, str | None, dict[str, Any]], BaseChatModel]
] = {
    "ollama": create_chat_ollama,
    "openai": lambda model, base_url, api_key, kwargs: ChatOpenAI(
        model=model, base_url=base_url, api_key=api_key, **kwargs
    ),
    "openwebui": lambda model, base_url, api_key, kwargs: ChatOpenAI(
        model=model, base_url=base_url, api_key=api_key, **kwargs
    ),
    "anthropic": lambda model, base_url, api_key, kwargs: ChatAnthropic(
        model_name=model,
        base_url=base_url,
        api_key=api_key,
        **kwargs,
    ),
}


class AiAgent:
    """
    Abstraction for an AiAgent.
    """

    system_prompt: str = """
    You are in a cybersecurity simulation and act as the purple team.

    Tool calling rules:
    - Working directory: %(working_directory)s
    - Only send emails if requested
    """ % {"working_directory": str(config.work_path.absolute())}

    def __init__(
        self,
        provider: str,
        model: str,
        base_url: str,
        api_key: str | None,
        tools: Sequence[BaseTool | Callable[..., Any] | dict[str, Any]] | None = None,
        middleware: Sequence[AgentMiddleware] | None = None,
        debug: bool = False,
        system_prompt: str | None = None,
        response_format: Any = None,  # noqa: ANN401
    ) -> None:
        """
        Initializes the AiAgent and the connection to its backend model.
        """
        self.usage = UsageCallback()

        if system_prompt is not None:
            self.system_prompt = system_prompt

        if tools is None:
            tools = []

        self.track_tool_call_middleware = TrackToolCallMiddleware(
            tools_available=[tool.name for tool in tools]  # type: ignore
        )

        middlewares: list[AgentMiddleware] = [self.track_tool_call_middleware]
        if middleware is not None:
            middlewares.extend(list(middleware))

        if model == "gpt-oss:120b" and response_format is not None:
            # Hack for gpt-oss:120b as langchain uses ProviderStrategy for this model, which fails.
            response_format = ToolStrategy(response_format)

        self.model = AiAgent.create_model(
            provider,
            model,
            base_url,
            api_key,
            callbacks=[self.usage],
        )
        self.agent = create_agent(
            self.model,
            tools=tools,
            middleware=middlewares,
            system_prompt=self.system_prompt,
            debug=debug,
            response_format=response_format,
        )

    @staticmethod
    def create_model(
        provider: str,
        model: str,
        base_url: str,
        api_key: str | None = None,
        **kwargs: Any,  # noqa: ANN401
    ) -> BaseChatModel:
        """
        Create a provider specific ChatModel from a model string.
        """
        # Temperature is not supported by opus 4.7, so we removed it for convenience
        # Temperature means something like "creativity" and usually leads to less predictable and consistent results.
        # In the context of our bachelor thesis we want the agent to behave as consistent as possible.
        # kwargs.update({"temperature": 0})

        create_model = PROVIDER_MAP.get(provider)

        if create_model is None:
            supported_providers = ", ".join(PROVIDER_MAP.keys())
            message = ValueError(
                f"Provider {provider} is not supported yet, valid options {supported_providers}."
            )
            raise ValueError(message)

        return create_model(model, base_url, api_key, kwargs)

    async def ainvoke(self, prompt: str, role: str = "user") -> dict[str, Any] | Any:  # noqa: ANN401
        """
        Invoke a prompt.

        :param role:
        :param prompt:
        :return:
        """
        return await self.agent.ainvoke(
            {"messages": [{"role": role, "content": prompt}]}, reasoning=True
        )

    def invoke(self, prompt: str, role: str = "user") -> dict[str, Any] | Any:  # noqa: ANN401
        """
        Invoke a prompt.
        """
        return asyncio.run(self.ainvoke(prompt, role))

    async def run(self, prompt: str) -> AsyncGenerator[str, None]:
        """
        Run the AI-agent with the given prompt.
        """
        result = await self.ainvoke(prompt)
        for message in result.get("messages", []):
            role = type(message).__name__.replace("Message", "")

            if isinstance(message.content, str):
                content = message.content
            else:
                content = pformat(message.content)

            yield f"[{role}]\n{content}\n"

    async def run_interactive(
        self,
        prompt: str,
    ) -> AsyncGenerator[str, None]:
        """
        Run the agent in a continuous interactive loop, maintaining conversation history.

        After each agent response the human operator is prompted for the next instruction.
        The loop ends when the operator enters an empty line or the 'exit' string.

        :param prompt: The initial prompt to start the session.
        """
        message = f"ai_agent:[Prompt] {prompt}"
        logger.info(message)
        stop_command = "exit"
        messages: list[Any] = [{"role": "user", "content": prompt}]

        while True:
            prev_count = len(messages)
            result = await self.agent.ainvoke({"messages": messages})
            messages = result.get("messages", messages)

            for message in messages[prev_count:]:
                role = type(message).__name__.replace("Message", "")
                if isinstance(message.content, str):
                    content = message.content
                else:
                    content = pformat(message.content)
                if content:
                    yield f"[{role}]\n{content}\n"

            next_instruction = input(
                f"\n[Next instruction (empty or '{stop_command}' to stop)]\n> "
            ).strip()
            if not next_instruction or next_instruction.lower() == stop_command.lower():
                break

            message = f"ai_agent:[Prompt] {next_instruction}"
            logger.info(message)
            messages.append({"role": "user", "content": next_instruction})


async def get_mcp_tools(config: Configuration) -> list[BaseTool]:
    """
    Setup MCP Tools.
    """
    mcp_tools = []
    mcp_configs = {}

    if config.drawio_mcp is not None:
        mcp_configs.update(
            {
                "drawio": {
                    "transport": "streamable_http",
                    "url": config.drawio_mcp.url,
                    "headers": {
                        "Authorization": f"Basic {config.drawio_mcp.basic_auth}",
                    },
                }
            }
        )

    mcp_client = MultiServerMCPClient(mcp_configs)

    try:
        mcp_tools = await mcp_client.get_tools()
    except Exception as e:
        logger.warning("Failed to load MCP tools; continuing without them.", exc_info=e)

    return mcp_tools


async def create_ai_agent(
    interactive: bool = False,
    tools: list[BaseTool | Callable[..., Any] | dict[str, Any]] | None = None,
    system_prompt: str | None = None,
    response_format: Any = None,  # noqa: ANN401
    load_drill_tools: bool = False,
    load_mcp_tools: bool = False,
) -> AiAgent:
    """
    Creates an AI-agent from the runtime configuration.
    """
    if config.ai is None:
        message = "The AI is not configured. Run:`nsak config set ai` for the interactive setup."
        raise RuntimeError(message)

    if tools is None:
        tools = [
            cli_tool,
            host_configuration,
            send_email,
        ]

        if load_drill_tools:
            tools.extend([*generate_drill_tools()])

        if load_mcp_tools:
            tools.extend([*await get_mcp_tools(config)])

    middleware: list[AgentMiddleware] = []

    if interactive:
        tools.append(human_interaction_hook)

    return AiAgent(
        config.ai.provider,
        config.ai.model,
        config.ai.base_url,
        config.ai.api_key,
        tools,
        middleware,
        debug=False,
        system_prompt=system_prompt,
        response_format=response_format,
    )
