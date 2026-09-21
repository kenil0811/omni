"""Execution context handed to an Entrypoint."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .artifacts import Artifacts
from .resources import Resources


@dataclass
class Context:
    """What a running Entrypoint is allowed to see.

    Generated code receives logical handles only: no database paths, no
    credentials, no platform internals.
    """

    app_id: str
    run_id: str
    entrypoint_id: str
    resources: Resources
    artifacts: Artifacts
    config: dict[str, Any] = field(default_factory=dict)
    _logs: list[str] = field(default_factory=list, repr=False)

    def log(self, message: str) -> None:
        """Record a bounded progress message for Activity."""
        self._logs.append(str(message)[:2000])

    @property
    def logs(self) -> list[str]:
        return list(self._logs)

    def selected_files(self) -> list[Path]:
        """Files the user deliberately selected for this Run."""
        return [Path(p) for p in self.config.get("selected_files", [])]
