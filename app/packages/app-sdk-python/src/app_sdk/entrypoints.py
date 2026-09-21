"""Entrypoint declaration.

One definition is the single source of truth for an App capability. The
platform projects it into the trusted fallback UI, an Assistant tool, the App
UI Bridge, and later MCP. Generated code writes the function once.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any, Literal

Kind = Literal["action", "query", "job"]


@dataclass(frozen=True)
class Entrypoint:
    id: str
    kind: Kind
    description: str
    fn: Callable[..., Any]
    input_schema: dict[str, Any] | None = field(default=None)
    output_schema: dict[str, Any] | None = field(default=None)


_REGISTRY: dict[str, Entrypoint] = {}


def entrypoint(
    id: str,
    kind: Kind = "action",
    description: str = "",
    input_schema: dict[str, Any] | None = None,
    output_schema: dict[str, Any] | None = None,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Declare a function as an App Entrypoint.

    The decorated function is called as ``fn(input: dict, ctx: Context)`` and
    must return a JSON-serializable dict.

        @entrypoint("import_files", kind="action", description="Import selected files")
        def import_files(input, ctx):
            ...
            return {"imported": 12}
    """

    def decorate(fn: Callable[..., Any]) -> Callable[..., Any]:
        if id in _REGISTRY and _REGISTRY[id].fn is not fn:
            raise ValueError(f"entrypoint {id!r} is already declared")
        _REGISTRY[id] = Entrypoint(
            id=id,
            kind=kind,
            description=description or (fn.__doc__ or "").strip().split("\n")[0],
            fn=fn,
            input_schema=input_schema,
            output_schema=output_schema,
        )
        return fn

    return decorate


def registry() -> dict[str, Entrypoint]:
    return dict(_REGISTRY)


def get(entrypoint_id: str) -> Entrypoint:
    if entrypoint_id not in _REGISTRY:
        known = ", ".join(sorted(_REGISTRY)) or "none"
        raise KeyError(f"no entrypoint {entrypoint_id!r}; declared: {known}")
    return _REGISTRY[entrypoint_id]


def clear() -> None:
    """Test-harness use only."""
    _REGISTRY.clear()
