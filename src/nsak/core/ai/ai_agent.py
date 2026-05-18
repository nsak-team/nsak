import asyncio
import logging
from pprint import pformat
from typing import Any, AsyncGenerator, Callable, Sequence

from langchain.agents import create_agent
from langchain.agents.middleware import (
    AgentMiddleware,
    HumanInTheLoopMiddleware,
    LLMToolSelectorMiddleware,
)
from langchain_anthropic.chat_models import ChatAnthropic
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage
from langchain_core.tools import BaseTool
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_ollama.chat_models import ChatOllama
from langchain_openai.chat_models import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver
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

type StreamChunk = tuple[str, bool, dict[str, Any] | None, list[str] | None]


class AiAgent:
    """
    Abstraction for an AiAgent.
    """

    system_prompt = "You are in a cybersecurity simulation and act as the purple team."

    def __init__(
        self,
        provider: str,
        model: str,
        base_url: str,
        api_key: str | None,
        tools: Sequence[BaseTool | Callable[..., Any] | dict[str, Any]] | None = None,
        middleware: Sequence[AgentMiddleware] | None = None,
        debug: bool = False,
    ) -> None:
        """
        Initializes the AiAgent and the connection to its backend model.
        """
        self.model = AiAgent.create_model(provider, model, base_url, api_key)
        self.agent = create_agent(
            self.model,
            tools=tools,
            system_prompt=self.system_prompt,
            debug=debug,
            checkpointer=InMemorySaver(),
            middleware=middleware or [],
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

    async def run(
        self, prompt: str, interactive: bool = False
    ) -> AsyncGenerator[str, None]:
        """
        Run the AI-agent with the given prompt.
        """
        if interactive:
            async for chunk in self._run_interactive(prompt):
                yield chunk
        else:
            result = await self.ainvoke(prompt)
            for message in result.get("messages", []):
                if not isinstance(message, AIMessage):
                    continue
                content = (
                    message.content
                    if isinstance(message.content, str)
                    else pformat(message.content)
                )
                if content:
                    yield f"[AI]\n{content}\n"

    async def _run_interactive(self, prompt: str) -> AsyncGenerator[str, None]:
        """
        Run the agent in a continuous interactive loop, yielding streamed response tokens.

        After each agent response the operator is prompted for the next instruction.
        The loop ends when the operator enters an empty line or 'exit'.

        Interrupt handling:
        - human_interaction_hook: operator is asked to provide a free-text response
        - send_email: operator is asked to approve or reject the pending email

        After resolving an interrupt the agent stream resumes automatically.
        """
        logger.info("ai_agent:[Prompt] %s", prompt)
        stop_command = "exit"
        agent_config = {"configurable": {"thread_id": str(config.run_uuid)}}

        while True:
            interrupted = False
            interrupt_value = None
            ai_started = False
            tokens = []
            async for text, is_interrupt, i_value, _ in self._stream_chunks(
                {"messages": [{"role": "user", "content": prompt}]}, agent_config
            ):
                if is_interrupt:
                    interrupted = True
                    interrupt_value = i_value
                else:
                    if not ai_started:
                        tokens.append(
                            "[ Ai !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ]"
                        )
                        ai_started = True
                tokens.append(text)

            if interrupted:
                resume_command = self._handle_interrupt(interrupt_value)
                if resume_command is not None:
                    async for text, _, _, _ in self._stream_chunks(
                        resume_command, agent_config
                    ):
                        tokens.append(text)
            yield "".join(tokens)
            next_instruction = input(
                f"\n[Next instruction (empty or '{stop_command}' to stop)]\n> "
            ).strip()
            if not next_instruction or next_instruction.lower() == stop_command.lower():
                break

            logger.info("ai_agent:[Prompt] %s", next_instruction)
            # Langgraph stores the msg content over thread_id,
            # messages.append({"role": "user", "content": next_instruction})
            prompt = next_instruction

    async def _stream_chunks(
        self, input_data: dict[str, Any] | Command, agent_config: dict[str, Any]
    ) -> AsyncGenerator[StreamChunk, None]:
        """
        Yield (text, is_interrupt, interrupt_value, allowed_decisions) from the agent stream.

        LangGraph produces two event types via stream_mode=["updates", "messages"]:
        - "messages": a single LLM token — yielded with is_interrupt=False
        - "updates" with "__interrupt__": middleware halted a tool call — yielded with
          is_interrupt=True, interrupt_value returns a complete value-Dict to work with multiple tool calls
        """
        async for chunk in self.agent.astream(
            input_data,
            config=agent_config,
            stream_mode=["updates", "messages"],
            version="v2",
        ):
            if chunk["type"] == "messages":
                token, _ = chunk["data"]
                if token.content:
                    yield token.content, False, None, None
            elif chunk["type"] == "updates" and "__interrupt__" in chunk["data"]:
                interrupt_data = chunk["data"]["__interrupt__"]
                value = interrupt_data[0].value
                action_name = value["action_requests"][0]["name"]
                allowed = value["review_configs"][0]["allowed_decisions"]

                logger.info(
                    "\n%s\n Tool: %s\n   Args: %s\n   Allowed: %s\n%s",
                    "=" * 50,
                    action_name,
                    value["action_requests"][0]["args"],
                    allowed,
                    "=" * 50,
                )

                yield f"\nInterrupt: {action_name}", True, value, allowed

        yield "\n", False, None, None

    @staticmethod
    def _decide_for_tool(tool_name: str, allowed: list[str]) -> dict[str, Any] | None:
        match tool_name:
            case "human_interaction_hook":
                response = input("\nYour response: ").strip()
                if not response:
                    return None
                return {"type": "respond", "message": response}
            case "send_email":
                choice = input("\nApprove or reject email? [approve/reject]: ").strip()
                if choice not in ("approve", "reject"):
                    return None
                return {"type": choice}
            case _:
                proceed = (
                    input(f"\nProceed with '{tool_name}'? [y/n]: ").strip().lower()
                )
                if proceed != "y":
                    return None
                return {"type": allowed[0] if allowed else "proceed"}

    def _handle_interrupt(
        self, interrupt_value: dict[str, Any] | None
    ) -> Command | None:
        """Return a resume Command for the given interrupt type, or None to skip."""
        if interrupt_value is None:
            return None

        action_requests: list[dict[str, Any]] = interrupt_value["action_requests"]
        review_configs: list[dict[str, Any]] = interrupt_value["review_configs"]
        decisions: list[dict[str, Any]] = []

        for req, conf in zip(action_requests, review_configs, strict=False):
            tool_name: str = req["name"]
            allowed: list[str] = conf.get("allowed_decisions", [])
            decision = self._decide_for_tool(tool_name, allowed)
            if decision is None:
                return None
            decisions.append(decision)
        return Command(resume={"decisions": decisions}) if decisions else None


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
) -> AiAgent:
    """
    Creates an AI-agent from the runtime configuration.
    """
    if config.ai is None:
        message = "The AI is not configured. Run:`nsak config set ai` for the interactive setup."
        raise RuntimeError(message)
    provider = config.ai.provider
    if provider is None:
        message = "AI provider not set. Run: nsak config set ai.provider <ollama|openai|anthropic|openwebui>"
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

    always = ["cli_tool", "send_email", "host_configuration"]
    if interactive:
        always.append("human_interaction_hook")

    class DebugToolSelectorMiddleware(LLMToolSelectorMiddleware):  # type: ignore[misc]
        async def awrap_model_call(self, request: Any, handler: Any) -> Any:  # noqa: ANN401
            logger.info(
                "All registered tools (%d): %s",
                len(request.tools),
                [t.name for t in request.tools if hasattr(t, "name")],
            )
            return await super().awrap_model_call(request, handler)

        def _process_selection_response(
            self,
            response: dict[str, Any],
            available_tools: list[Any],
            valid_tool_names: list[str],
            request: Any,  # noqa: ANN401
        ) -> Any:  # noqa: ANN401
            result = super()._process_selection_response(
                response, available_tools, valid_tool_names, request
            )
            selected = [t.name for t in result.tools if hasattr(t, "name")]
            logger.info("Tools after selection (%d): %s", len(selected), selected)
            return result

    middleware.append(
        DebugToolSelectorMiddleware(
            max_tools=5,
            always_include=always,
            system_prompt="Your goal is to select the most relevant tools. Log your selection reasoning.",
        )
    )

    if interactive:
        # We use langchains build in `HumanInTheLoopMiddleware` middleware together with our `human_interaction_hook`
        tools.append(human_interaction_hook)
        middleware.append(
            HumanInTheLoopMiddleware(
                interrupt_on={
                    "cli_tool": True,
                    "human_interaction_hook": {"allowed_decisions": ["respond"]},
                    "send_email": {"allowed_decisions": ["approve", "reject"]},
                },
                description_prefix="Tool execution pending approval",
            )
        )

    return AiAgent(
        provider,
        config.ai.model,
        config.ai.base_url,
        config.ai.api_key,
        tools=[*tools, *dynamic_tools],
        middleware=middleware,
        debug=True,
    )
