import logging
import shlex
import subprocess

from langchain.tools import tool

logger = logging.getLogger(__name__)


@tool  # type: ignore[misc]
def cli_tool(command: str, timeout: int = 120) -> tuple[int, str, str]:
    """
    Run an arbitrary CLI command and return its output.

    Use nmap for network scanning, e.g.:
    - "nmap -sV 10.10.10.1" (service version detection)
    - "nmap -sC -sV -oN output.txt 10.10.10.1" (default scripts + versions)
    - "nmap -p 1-1000 10.10.10.1" (port range)

    Use `apt install` if a cli tool is missing.

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
        returncode = -1
        stdout = ""
        stderr = f"An error occurred during CLI tool usage: {e}"
        return (
            # Special return code
            returncode,
            stdout,
            stderr,
        )
