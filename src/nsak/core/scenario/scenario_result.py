from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class ScenarioResult(ABC):
    """
    Base class representing the result of a scenario.
    """

    @abstractmethod
    def display(self) -> str:
        """
        Returns a human-readable representation of the result, usually for stdout.
        """

    @abstractmethod
    def as_markdown(self) -> str:
        """
        Returns a Markdown representation of the result, usually for storing in a file.
        """


@dataclass(frozen=True, kw_only=True)
class AIScenarioResult(ScenarioResult, ABC):
    """
    Specifies AI specific metadata.
    """

    provider: str
    model: str
    tools_called: dict[str, list[str]]

    prompt_tokens: int
    completion_tokens: int

    @property
    def total_tokens(self) -> int:
        """
        Returns the total number of tokens consumed.
        """
        return self.prompt_tokens + self.completion_tokens
