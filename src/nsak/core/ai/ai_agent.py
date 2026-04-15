import asyncio
import base64
import logging
from pprint import pformat
from typing import Any, AsyncGenerator, Callable, Sequence

from langchain.agents import create_agent
from langchain_anthropic.chat_models import ChatAnthropic
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage
from langchain_core.tools import BaseTool
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_ollama.chat_models import ChatOllama
from langchain_openai.chat_models import ChatOpenAI

from nsak.core.ai.tools import (
    cli_tool,
    host_configuration,
    human_interaction_hook,
    send_email,
)
from nsak.core.configuration import config

logger = logging.getLogger(__name__)

PROVIDER_MAP: dict[str, Callable[[str, str, Any], BaseChatModel]] = {
    "ollama": lambda model, base_url, kwargs: ChatOllama(
        model=model, base_url=base_url, **kwargs
    ),
    "openai": lambda model, base_url, kwargs: ChatOpenAI(
        model=model, base_url=base_url, **kwargs
    ),
    "anthropic": lambda model, base_url, kwargs: ChatAnthropic(
        model_name=model, base_url=base_url, **kwargs
    ),
}

credentials = base64.b64encode(b"nsak:fec515d7-07bb-4a0a-b089-a0588465ccaf").decode()

mcp_client = MultiServerMCPClient(
    {
        "drawio": {
            "transport": "streamable_http",
            "url": "https://drawio.hiube.ch/mcp",
            "headers": {
                "Authorization": f"Basic {credentials}",
            },
        }
    }
)


class AiAgent:
    """
    Abstraction for an AiAgent.
    """

    system_prompt = "You are in a cybersecurity simulation and act as the purple team."

    def __init__(
        self,
        model: str,
        base_url: str,
        tools: Sequence[BaseTool | Callable[..., Any] | dict[str, Any]] | None = None,
    ) -> None:
        """
        Initializes the AiAgent and the connection to its backend model.
        """
        self.model = AiAgent.create_model(model, base_url)
        self.agent = create_agent(
            self.model,
            tools=tools,
            system_prompt=self.system_prompt,
        )

    @staticmethod
    def create_model(model: str, base_url: str) -> BaseChatModel:
        """
        Create a provider specific ChatModel from a model string.

        :param base_url:
        :param model:
        :return:
        """
        provider, _model = model.split(":", 1)
        kwargs = {"temperature": 0}

        create_model = PROVIDER_MAP.get(provider)

        if create_model is None:
            supported_providers = ", ".join(PROVIDER_MAP.keys())
            message = ValueError(
                f"Provider {provider} is not supported yet, valid options {supported_providers}."
            )
            raise ValueError(message)

        return create_model(_model, base_url, kwargs)

    async def ainvoke(self, prompt: str, role: str = "user") -> AIMessage:
        """
        Invoke a prompt.

        :param role:
        :param prompt:
        :return:
        """
        return self.agent.ainvoke({"messages": [{"role": role, "content": prompt}]})

    def invoke(self, prompt: str, role: str = "user") -> AIMessage:
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

            messages.append({"role": "user", "content": next_instruction})


async def create_ai_agent(interactive: bool = False) -> AiAgent:
    """
    Creates an AI-agent from the runtime configuration.
    """
    if config.ai is None:
        message = "ai is not configured. Run: nsak config set ai.model <provider:model:tag> and nsak config set ai.base_url <url>"
        raise RuntimeError(message)

    tools: list[BaseTool | Callable[..., Any] | dict[str, Any]] = [
        cli_tool,
        host_configuration,
        send_email,
    ]

    if interactive:
        tools.append(human_interaction_hook)

    try:
        mcp_tools = await mcp_client.get_tools()
        tools.extend(mcp_tools)
    except Exception as e:
        logger.warning("Failed to load MCP tools; continuing without them.", exc_info=e)

    return AiAgent(
        config.ai.model,
        config.ai.base_url,
        tools,
    )
