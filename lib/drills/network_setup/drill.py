from pathlib import Path
import subprocess
import signal
import os


def run(args: dict) -> dict[str, any]:
    interface = args["interface"]
    address = args["address"]

    # start process
    proc = subprocess.Popen(
        [
            "ip",
            "addr", "add", interface, address
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    return {"pid": proc.pid}


def cleanup(result: dict) -> None:
    pid = result.get("pid")
    if not pid:
        return

    try:
        os.kill(pid, signal.SIGTERM)
    except ProcessLookupError:
        pass
