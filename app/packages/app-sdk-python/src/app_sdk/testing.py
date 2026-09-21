"""Local harness that loads a generated App and invokes its Entrypoints.

Used by the independent fixture oracles and by an App's own tests. It stands in
for the platform's App runtime worker: it gives the App a disposable workspace,
real SQLite Resources, and a real Artifact store, then calls the declared
Entrypoint exactly as the platform would.
"""

from __future__ import annotations

import importlib
import sys
import tempfile
import uuid
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from types import ModuleType
from typing import Any

from . import entrypoints as _entrypoints
from .artifacts import Artifacts
from .context import Context
from .resources import Resources, Table


class AppLoadError(RuntimeError):
    """The package could not be loaded well enough to invoke it."""


def _read_manifest(app_dir: Path) -> dict[str, Any]:
    manifest_path = app_dir / "app.yaml"
    if not manifest_path.exists():
        raise AppLoadError(f"no app.yaml in {app_dir}")
    try:
        import yaml  # type: ignore[import-untyped]
    except ModuleNotFoundError as exc:  # pragma: no cover
        raise AppLoadError("PyYAML is required to read app.yaml") from exc
    data = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise AppLoadError("app.yaml must parse to a mapping")
    return data


def _handler_modules(manifest: dict[str, Any]) -> list[str]:
    """Module names named by entrypoint handlers, e.g. 'handlers.collect'."""
    modules: list[str] = []
    for entry in (manifest.get("spec") or {}).get("entrypoints") or []:
        handler = str(entry.get("handler", ""))
        if "." in handler:
            module = handler.rsplit(".", 1)[0]
            if module and module not in modules:
                modules.append(module)
    return modules


class LoadedApp:
    """A generated App, loaded and ready to invoke."""

    def __init__(self, app_dir: Path, workspace: Path, config: dict[str, Any]) -> None:
        self.app_dir = Path(app_dir)
        self.workspace = Path(workspace)
        self.manifest = _read_manifest(self.app_dir)
        self.name = str((self.manifest.get("metadata") or {}).get("name", "app"))
        self.artifacts = Artifacts(self.workspace / "artifacts")
        self.resources = Resources(self.workspace / "resources.sqlite3", self.artifacts)
        self.config = dict(config)
        self._modules: list[ModuleType] = []
        self._load()

    def _load(self) -> None:
        src = self.app_dir / "src"
        added = str(src if src.is_dir() else self.app_dir)
        sys.path.insert(0, added)
        self._path_entry = added
        modules = _handler_modules(self.manifest)
        if not modules:
            raise AppLoadError("app.yaml declares no entrypoint handlers")
        # Import fresh: a module left in sys.modules by an earlier load would
        # skip execution (so no Entrypoints register) or re-run its decorators.
        preloaded = set(sys.modules)
        for name in modules:
            sys.modules.pop(name, None)
        errors: list[str] = []
        for name in modules:
            try:
                self._modules.append(importlib.import_module(name))
            except Exception as exc:  # noqa: BLE001 - reported to the runner
                errors.append(f"{name}: {type(exc).__name__}: {exc}")
        # Anything the App pulled in belongs to this load, not the next one.
        self._owned_modules = set(sys.modules) - preloaded
        if errors and not self._modules:
            raise AppLoadError("could not import handler modules -> " + "; ".join(errors))
        self.import_errors = errors

    def entrypoint_ids(self) -> list[str]:
        return sorted(_entrypoints.registry())

    def invoke(self, entrypoint_id: str, input: dict[str, Any] | None = None) -> Any:
        """Call one Entrypoint the way the platform would."""
        entry = _entrypoints.get(entrypoint_id)
        ctx = Context(
            app_id=self.name,
            run_id=str(uuid.uuid4()),
            entrypoint_id=entrypoint_id,
            resources=self.resources,
            artifacts=self.artifacts,
            config=dict(self.config),
        )
        self.last_context = ctx
        return entry.fn(dict(input or {}), ctx)

    def table(self, name: str) -> Table:
        """Inspect a Resource table directly. Oracle use."""
        return self.resources.table(name)

    def close(self) -> None:
        self.resources.close()
        if self._path_entry in sys.path:
            sys.path.remove(self._path_entry)
        for name in getattr(self, "_owned_modules", set()):
            sys.modules.pop(name, None)


@contextmanager
def harness(
    app_dir: str | Path,
    config: dict[str, Any] | None = None,
    workspace: str | Path | None = None,
) -> Iterator[LoadedApp]:
    """Load an App in a disposable workspace.

    with harness("path/to/app", config={"threshold": 100}) as app:
        result = app.invoke("collect", {"source": url})
        assert app.table("records").count() == 8
    """
    _entrypoints.clear()
    tmp: tempfile.TemporaryDirectory[str] | None = None
    if workspace is None:
        tmp = tempfile.TemporaryDirectory(prefix="alpha-app-")
        workspace_path = Path(tmp.name)
    else:
        workspace_path = Path(workspace)
        workspace_path.mkdir(parents=True, exist_ok=True)
    app: LoadedApp | None = None
    try:
        app = LoadedApp(Path(app_dir), workspace_path, config or {})
        yield app
    finally:
        if app is not None:
            app.close()
        _entrypoints.clear()
        if tmp is not None:
            tmp.cleanup()
