import asyncio
import logging
from pprint import pformat
from typing import Any, AsyncGenerator, Callable, Sequence

from langchain.agents import create_agent
from langchain.agents.middleware import AgentMiddleware
from langchain_anthropic.chat_models import ChatAnthropic
from langchain_core.language_models import BaseChatModel
from langchain_core.tools import BaseTool
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_ollama.chat_models import ChatOllama
from langchain_openai.chat_models import ChatOpenAI

from nsak.core.ai.tools import (
    cli_tool,
    generate_drill_tools,
    host_configuration,
    human_interaction_hook,
    send_email,
)
from nsak.core.configuration import Configuration, config

logger = logging.getLogger(__name__)


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

    system_prompt = "You are in a cybersecurity simulation and act as the purple team."

    dynamic_tools: Sequence[BaseTool | Callable[..., Any] | dict[str, Any]] = []

    def __init__(
        self,
        provider: str,
        model: str,
        base_url: str,
        api_key: str | None,
        tools: Sequence[BaseTool | Callable[..., Any] | dict[str, Any]] | None = None,
        dynamic_tools: Sequence[BaseTool | Callable[..., Any] | dict[str, Any]]
        | None = None,
        middleware: Sequence[AgentMiddleware] | None = None,
        debug: bool = False,
        response_format: object = None,
    ) -> None:
        """
        Initializes the AiAgent and the connection to its backend model.
        """
        if dynamic_tools:
            self.dynamic_tools = dynamic_tools

        self.model = AiAgent.create_model(provider, model, base_url, api_key)
        self.agent = create_agent(
            self.model,
            tools=tools,
            middleware=middleware or [],
            system_prompt=self.system_prompt,
            debug=debug,
            # checkpointer=InMemorySaver(),
            response_format=response_format,
        )

    @staticmethod
    def create_model(
        provider: str, model: str, base_url: str, api_key: str | None = None
    ) -> BaseChatModel:
        """
        Create a provider specific ChatModel from a model string.
        """
        # Temperature means something like "creativity" and usually leads to less predictable and consistent results.
        # In the context of our bachelor thesis we want the agent to behave as consistent as possible.
        kwargs = {"temperature": 0}

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
            {"messages": [{"role": role, "content": prompt}]}
        )

    def invoke(self, prompt: str, role: str = "user") -> dict[str, Any] | Any:  # noqa: ANN401
        """
        Invoke a prompt.

        :param role:
        :param prompt:
        :return:
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
    interactive: bool = False, response_format: object = None
) -> AiAgent:
    """
    Creates an AI-agent from the runtime configuration.
    """
    if config.ai is None:
        message = "The AI is not configured. Run:`nsak config set ai` for the interactive setup."
        raise RuntimeError(message)

    tools: list[BaseTool | Callable[..., Any] | dict[str, Any]] = [
        cli_tool,
        host_configuration,
        send_email,
    ]

    dynamic_tools: list[BaseTool | Callable[..., Any] | dict[str, Any]] = [
        *generate_drill_tools(),
        *await get_mcp_tools(config),
    ]

    middleware: list[AgentMiddleware] = []

    if interactive:
        # We use langchains build in `HumanInTheLoopMiddleware` middleware together with our `human_interaction_hook`
        tools.append(human_interaction_hook)
        # middleware.append(HumanInTheLoopMiddleware(
        #     interrupt_on={
        #         "cli_tool": True,
        #         "human_interaction_hook": {"allowed_decisions": ["respond"]},
        #         "send_email": {"allowed_decisions": ["approve", "reject"]},
        #     },
        #     description_prefix="Tool execution pending approval",
        # ))

    return AiAgent(
        config.ai.provider,
        config.ai.model,
        config.ai.base_url,
        config.ai.api_key,
        tools,
        dynamic_tools,
        middleware,
        debug=True,
        response_format=response_format,
    )
