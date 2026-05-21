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

    Use nmap NSE scripts for targeted service enumeration with --script <name> or --script <cat>:
    - Single script:   "nmap --script http-title -p 80 10.10.10.1"
    - Multiple:        "nmap --script http-title,http-headers -p 80,443 10.10.10.1"
    - With args:       "nmap --script smb-security-mode --script-args smbuser=guest -p 445 10.10.10.1"

    Service-to-script mapping — run these when the corresponding service is detected:
      HTTP / HTTPS / http-alt (80, 443, 8080…):
          http-title, http-headers, http-robots.txt
          e.g. "nmap --script http-title,http-headers,http-robots.txt -p 80 10.10.10.1"

      DNS / domain (53):
          dns-zone-transfer, dns-brute
          e.g. "nmap --script dns-zone-transfer,dns-brute -p 53 10.10.10.1"

      SMTP / SMTPS (25, 465, 587):
          smtp-commands, smtp-enum-users
          e.g. "nmap --script smtp-commands,smtp-enum-users -p 25 10.10.10.1"

      FTP (21):
          ftp-anon, ftp-ls
          e.g. "nmap --script ftp-anon,ftp-ls -p 21 10.10.10.1"

      SMB / NetBIOS (139, 445):
          smb-security-mode, smb2-security-mode
          e.g. "nmap --script smb-security-mode,smb2-security-mode -p 139,445 10.10.10.1"

      LDAP / LDAPS (389, 636):
          ldap-rootdse
          e.g. "nmap --script ldap-rootdse -p 389 10.10.10.1"

    Workflow: first run -sV to detect services, then re-scan open ports with the
    matching scripts above. Combine with -sV to keep version info:
      "nmap -sV --script http-title,http-headers -p 80,443 10.10.10.1"

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
