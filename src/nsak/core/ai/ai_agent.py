import logging
import shlex
import subprocess
from pprint import pformat
from typing import Any, Callable, Generator

from langchain.agents import create_agent
from langchain_anthropic.chat_models import ChatAnthropic
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage
from langchain_core.tools import tool
from langchain_ollama.chat_models import ChatOllama
from langchain_openai.chat_models import ChatOpenAI
from lazy_object_proxy import Proxy

from nsak.core import config
from nsak.core.email.email_backend import email_backend
from nsak.core.settings import AI_MODEL, OLLAMA_BASE_URL

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


@tool  # type: ignore[misc]
def host_configuration() -> dict[str, Any]:
    """
    Returns the host network configuration as a dictionary.

    Use this tool first to understand the local network setup before running any scans or attacks.

    The returned dictionary has the following structure:
    {
        "debug": bool,
        "device": {
            "id": str,
            "name": str,
            "description": str,
            "configuration": {
                "network": {
                    "ethernets": {
                        "<interface_name>": {
                            "name": str,
                            "is_up": bool,        # False means the interface is DOWN, skip it
                            "is_target": bool,    # True means this interface is used for attacks/scans
                            "is_management": bool # True means this interface is used for device access
                            "addresses": {
                                "<cidr>": {
                                    "ip": str,        # e.g. "10.10.10.5/24" - use this as nmap source IP
                                    "is_target": bool,
                                    "is_management": bool,
                                }
                            },
                        }
                    }
                }
            }
        }
    }

    Guidance:
    - Use `is_target=True` interfaces/IPs when running nmap scans or attacks
    - Skip interfaces where `is_up=False`
    - Use `is_management=True` interfaces for device access or data extraction
    - `configuration` may be None if the device has not been configured yet
    """
    return config.asdict()


@tool  # type: ignore[misc]
def human_interaction_hook(question: str) -> str:
    """
    Ask the human operator a question and return their answer.

    Use this tool when you need information, confirmation, or guidance that
    cannot be determined from the available tools or the current context.

    Args:
        question: The question or request to present to the human operator.

    Returns
    -------
        The human operator's response as a string.
    """
    return input(f"[Human Input Required]\n{question}\n> ")


@tool  # type: ignore[misc]
def send_email(subject: str, message: str) -> None:
    """
    Send an email notification to the configured receiver.

    Use this tool to alert the human operator about findings, incidents, or
    completed tasks that require their attention outside the current session.

    Args:
        subject: A short, descriptive subject line for the email, which is added to the subject prefix `NSAK - AI Agent:`.
        message: The full body of the email.
    """
    subject = f"NSAK - AI Agent: {subject}"
    email_backend.send(subject, message)


@tool  # type: ignore[misc]
def cli(command: str, timeout: int = 120) -> tuple[int, str, str]:
    """
    Run an arbitrary CLI command and return its output.

    Use nmap for network scanning, e.g.:
    - "nmap -sV 10.10.10.1" (service version detection)
    - "nmap -sC -sV -oN output.txt 10.10.10.1" (default scripts + versions)
    - "nmap -p 1-1000 10.10.10.1" (port range)

    Args:
        command: Full CLI command string to execute.
        timeout: Max seconds to wait (default 120, increase for large scans).

    Returns
    -------
        Tuple of (exit_code, stdout, stderr).
        Exit code 0 means success. Check stderr on failure.
    """
    try:
        completed_process = subprocess.run(  # noqa: S603
            shlex.split(command),
            capture_output=True,
            text=True,
            check=True,
            timeout=timeout,
        )
        return (
            completed_process.returncode,
            completed_process.stdout,
            completed_process.stderr,
        )
    except subprocess.TimeoutExpired as e:
        returncode = -1
        stdout = str(e.stdout) or ""
        stderr = f"Command timed out after {timeout}s"
        return (
            # Special return code
            returncode,
            stdout,
            stderr,
        )
    except subprocess.CalledProcessError as e:
        return (
            e.returncode,
            e.stdout,
            e.stderr,
        )
    except Exception as e:
        logger.exception("An error occurred during CLI tool usage.", exc_info=e)
        raise e


class AiAgent:
    """
    Abstraction for an AiAgent.
    """

    tools = (
        cli,
        host_configuration,
        send_email,
    )
    system_prompt = "You are in a cybersecurity simulation and act as the purple team."

    def __init__(
        self, model: str, base_url: str, human_interaction: bool = True
    ) -> None:
        """
        Initializes the AiAgent and the connection to its backend model.
        """
        tools = list(self.tools)
        if human_interaction:
            tools.append(human_interaction_hook)

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
        provider, _model, _tag = model.split(":")
        kwargs = {"temperature": 0}

        create_model = PROVIDER_MAP.get(provider)

        if create_model is None:
            supported_providers = ", ".join(PROVIDER_MAP.keys())
            message = ValueError(
                f"Provider {provider} is not supported yet, valid options {supported_providers}."
            )
            raise ValueError(message)

        return create_model(":".join([_model, _tag]), base_url, kwargs)

    def invoke(self, prompt: str, role: str = "user") -> AIMessage:
        """
        Invoke a prompt.

        :param role:
        :param prompt:
        :return:
        """
        return self.agent.invoke({"messages": [{"role": role, "content": prompt}]})

    def run(self, prompt: str) -> Generator[str]:
        """
        Run the AI-agent with the given prompt.
        """
        result = self.invoke(prompt)
        for message in result.get("messages", []):
            role = type(message).__name__.replace("Message", "")

            if isinstance(message.content, str):
                content = message.content
            else:
                content = pformat(message.content)

            yield f"[{role}]\n{content}\n"

    def run_interactive(
        self,
        prompt: str,
    ) -> Generator[str]:
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
            result = self.agent.invoke({"messages": messages})
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


def create_ai_agent() -> AiAgent:
    """
    Creates an AI-agent from the system settings.
    """
    if OLLAMA_BASE_URL is None:
        message = "NSAK_OLLAMA_BASE_URL no set"
        raise RuntimeError(message)
    if AI_MODEL is None:
        message = "NSAK_AI_MODEL no set"
        raise RuntimeError(message)
    return AiAgent(AI_MODEL, OLLAMA_BASE_URL)


ai_agent: AiAgent = Proxy(create_ai_agent)
