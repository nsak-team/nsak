import sys
from typing import cast

from langchain_ollama.llms import OllamaLLM

from nsak.core.settings import OLLAMA_BASE_URL


class AiAgent:
    """
    Abstraction for an AiAgent.
    """

    def __init__(self, model: str, base_url: str) -> None:
        """
        Initializes the AiAgent and the connection to its backend model.
        """
        self.model = OllamaLLM(
            model=model,
            # temperature=0.7,
            # num_predict=256,
            base_url=base_url,
        )

    def invoke(self, prompt: str) -> str:
        """
        Invoke a prompt.

        :param prompt:
        :return:
        """
        return cast(str, self.model.invoke(prompt))


def run_ai_agent(prompt: str) -> str:
    """

    :return:
    """
    if OLLAMA_BASE_URL is None:
        message = "NSAK_OLLAMA_BASE_URL no set"
        raise RuntimeError(message)
    ai_agent = AiAgent("qwen2.5-coder", OLLAMA_BASE_URL)
    result = ai_agent.invoke(prompt)
    return result


if __name__ == "__main__":
    _input = sys.argv[1]
    result = run_ai_agent(_input)
    sys.stdout.write(result)
