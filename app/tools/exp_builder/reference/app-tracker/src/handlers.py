"""Work Tracker — reference implementation (oracle self-test only)."""

from __future__ import annotations

from app_sdk import InvalidInput, entrypoint

STATUSES = ("todo", "doing", "done")


def _clean(payload: dict, *, partial: bool) -> dict:
    """Validate a create (partial=False) or a set of changes (partial=True)."""
    cleaned: dict = {}

    if "title" in payload:
        title = payload["title"]
        if not isinstance(title, str) or not title.strip():
            raise InvalidInput("title is required")
        cleaned["title"] = title.strip()
    elif not partial:
        raise InvalidInput("title is required")

    if "status" in payload:
        status = payload["status"]
        if status not in STATUSES:
            raise InvalidInput(f"status must be one of {', '.join(STATUSES)}")
        cleaned["status"] = status
    elif not partial:
        cleaned["status"] = "todo"

    if "priority" in payload:
        priority = payload["priority"]
        if isinstance(priority, bool) or not isinstance(priority, int) or not 1 <= priority <= 5:
            raise InvalidInput("priority must be a whole number from 1 to 5")
        cleaned["priority"] = priority
    elif not partial:
        cleaned["priority"] = 3

    if "notes" in payload:
        notes = payload["notes"]
        if not isinstance(notes, str):
            raise InvalidInput("notes must be text")
        cleaned["notes"] = notes
    elif not partial:
        cleaned["notes"] = ""

    return cleaned


@entrypoint("create_item", kind="action", description="Add an item to the tracker.")
def create_item(input: dict, ctx) -> dict:
    record = ctx.resources.table("items").insert(_clean(input, partial=False))
    return {"id": record["id"], "revision": record["revision"]}


@entrypoint("update_item", kind="action", description="Change an item, rejecting a stale revision.")
def update_item(input: dict, ctx) -> dict:
    item_id = input.get("id")
    if not item_id:
        raise InvalidInput("id is required")
    if "revision" not in input:
        raise InvalidInput("revision is required so concurrent edits are not lost")
    # Validate before writing, so a rejected change leaves the record untouched.
    changes = _clean(input.get("changes") or {}, partial=True)
    if not changes:
        raise InvalidInput("no changes were supplied")
    record = ctx.resources.table("items").update(
        str(item_id), changes, revision=int(input["revision"])
    )
    return {"id": record["id"], "revision": record["revision"]}


@entrypoint("list_items", kind="query", description="List items, optionally filtered by status.")
def list_items(input: dict, ctx) -> dict:
    table = ctx.resources.table("items")
    status = input.get("status")
    items = table.all() if status is None else table.all(where={"status": str(status)})
    items.sort(key=lambda item: (item.get("priority", 3), item.get("title", "")))
    return {"items": items, "total": len(items)}


@entrypoint("summarize", kind="query", description="Count items by status.")
def summarize(input: dict, ctx) -> dict:
    items = ctx.resources.table("items").all()
    by_status = {status: 0 for status in STATUSES}
    for item in items:
        status = item.get("status")
        if status in by_status:
            by_status[status] += 1
    return {"total": len(items), "by_status": by_status}
