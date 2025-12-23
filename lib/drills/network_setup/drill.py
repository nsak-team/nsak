import logging
import os
import signal
import subprocess

logger = logging.getLogger(__name__)

def run(args: dict) -> dict[str, any]:
    interface = args["interface"]

    # start process
    proc = subprocess.Popen(
        [
            "ip",
            "addr", "replace", "10.0.0.1/24", "dev", interface,
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    logger.info(proc.stdout.read() + " 10.0.0.1/24 on" + interface)
    proc.wait()

    return {"pid": proc.pid}


def cleanup(result: dict) -> None:
    pid = result.get("pid")
    if not pid:
        return

    try:
        os.kill(pid, signal.SIGTERM)
    except ProcessLookupError:
        pass
