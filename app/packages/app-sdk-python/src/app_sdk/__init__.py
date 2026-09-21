"""Alpha App SDK — the only supported route from generated code to the platform.

An App declares Entrypoints and uses the Context it is handed:

    from app_sdk import entrypoint

    @entrypoint("summarize", kind="query", description="Count records by status")
    def summarize(input, ctx):
        rows = ctx.resources.table("items").all()
        return {"total": len(rows)}

Generated code never receives database paths, credentials, network clients, or
platform internals — only logical handles on `ctx`.

NOTE: this is the development stub used for EXP-BUILDER (plan step 1). Its
shape matches the accepted SDK boundary, but it runs in-process against local
SQLite instead of the platform service. See docs/PLAN.md.
"""

from __future__ import annotations

from .artifacts import ArtifactRef, Artifacts
from .context import Context
from .entrypoints import Entrypoint, entrypoint, get, registry
from .errors import AppError, ExternalUnavailable, InvalidInput, UnsupportedInput
from .resources import (
    FileStore,
    Page,
    RecordNotFound,
    ResourceError,
    Resources,
    RevisionConflict,
    Table,
)

__all__ = [
    "AppError",
    "ArtifactRef",
    "Artifacts",
    "Context",
    "Entrypoint",
    "ExternalUnavailable",
    "FileStore",
    "InvalidInput",
    "Page",
    "RecordNotFound",
    "ResourceError",
    "Resources",
    "RevisionConflict",
    "Table",
    "UnsupportedInput",
    "entrypoint",
    "get",
    "registry",
]

__version__ = "0.0.1"
