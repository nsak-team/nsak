from __future__ import annotations

import dataclasses
from pathlib import Path


@dataclasses.dataclass(frozen=True)
class ContainerInfo:
    """
    Runtime container identity, parsed from the container runtime environment.
    """

    id: str | None = None
    name: str | None = None

    @classmethod
    def load(cls) -> "ContainerInfo":
        """
        Return container ID and name if running inside a container.

        Checks for Podman (/run/.containerenv) first, then Docker (/.dockerenv + cgroup).
        The name field is only available for Podman.
        """
        containerenv = Path("/run/.containerenv")
        if containerenv.exists():
            container_id = None
            container_name = None
            for line in containerenv.read_text(encoding="utf-8").splitlines():
                if line.startswith("id="):
                    container_id = line.split("=", 1)[1].strip('"')
                elif line.startswith("name="):
                    container_name = line.split("=", 1)[1].strip('"')
            return ContainerInfo(id=container_id, name=container_name)

        if Path("/.dockerenv").exists():
            try:
                cgroup = Path("/proc/self/cgroup").read_text(encoding="utf-8")
                for line in cgroup.splitlines():
                    parts = line.rsplit("/", 1)
                    if len(parts) > 1 and len(parts[-1]) >= 12:
                        return ContainerInfo(id=parts[-1][:12])
            except OSError:
                pass

        return ContainerInfo()
