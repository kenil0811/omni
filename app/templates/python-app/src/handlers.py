"""Entrypoint handlers for this App.

Each handler takes (input: dict, ctx: Context) and returns a JSON-serializable
dict. Use ctx.resources for state, ctx.artifacts for outputs, ctx.log for
progress. Raise app_sdk.InvalidInput / UnsupportedInput for user-facing errors.
"""

from __future__ import annotations

from app_sdk import entrypoint


@entrypoint("example", kind="action", description="Replace with what this does.")
def example(input: dict, ctx) -> dict:
    ctx.log("replace this handler")
    return {"ok": True}
