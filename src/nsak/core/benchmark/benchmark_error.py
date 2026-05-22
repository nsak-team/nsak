import traceback
from types import TracebackType
from typing import Any


class BenchmarkError(Exception):
    """
    Represents an error during a benchmark run.
    """

    def __init__(self, exception: Exception, *args: Any) -> None:  # noqa: ANN401
        """
        Init the Benchmark Error.
        """
        super().__init__(*args)
        self.exception: Exception = exception
        self.tb: TracebackType | None = exception.__traceback__

    def __str__(self) -> str:
        """
        Return exception and traceback as a string.
        """
        lines = [
            "Traceback (most recent call last):",
            *traceback.format_tb(self.tb),
            f"{type(self.exception).__name__}: {self.exception}",
        ]

        return "\n".join(lines)
