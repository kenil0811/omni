"""Source Watch — reference implementation (oracle self-test only)."""

from __future__ import annotations

import json
import urllib.error
import urllib.request

from app_sdk import ExternalUnavailable, InvalidInput, entrypoint

DEFAULT_WATCH_ABOVE = 100


def _check(row: dict) -> tuple[dict | None, dict | None]:
    """Return (record, problem). Exactly one is not None."""
    ref = row.get("ref")
    if not isinstance(ref, str) or not ref.strip():
        return None, {"ref": None, "reason": "ref is missing or empty"}
    title = row.get("title")
    if not isinstance(title, str) or not title.strip():
        return None, {"ref": ref, "reason": "title is empty"}
    price = row.get("price")
    if isinstance(price, bool) or not isinstance(price, (int, float)):
        return None, {"ref": ref, "reason": "price is not a number"}
    if price < 0:
        return None, {"ref": ref, "reason": "price is negative"}
    return {
        "ref": ref,
        "title": title,
        "price": float(price),
        "category": row.get("category"),
    }, None


@entrypoint(
    "collect", kind="job", description="Fetch the listing feed and store one record per item."
)
def collect(input: dict, ctx) -> dict:
    url = input.get("source_url")
    if not url:
        raise InvalidInput("source_url is required")

    try:
        with urllib.request.urlopen(str(url), timeout=30) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, OSError, TimeoutError) as exc:
        raise ExternalUnavailable(f"could not reach {url}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise ExternalUnavailable(f"{url} did not return JSON: {exc}") from exc

    rows = payload.get("rows") or []
    threshold = ctx.config.get("watch_above", DEFAULT_WATCH_ABOVE)
    table = ctx.resources.table("records")

    stored = 0
    updated = 0
    invalid: list[dict] = []
    seen: set[str] = set()

    for row in rows:
        record, problem = _check(row if isinstance(row, dict) else {})
        if problem is not None:
            invalid.append(problem)
            continue
        assert record is not None
        if record["ref"] in seen:
            continue  # same item twice in one feed
        seen.add(record["ref"])
        record["watched"] = record["price"] > threshold

        existing = table.get(record["ref"])
        if existing is None:
            table.insert({"id": record["ref"], **record})
            stored += 1
        else:
            changes = {k: v for k, v in record.items() if existing.get(k) != v}
            if changes:
                table.update(record["ref"], changes, revision=existing["revision"])
                updated += 1

    ctx.log(f"{len(rows)} rows: {stored} new, {updated} updated, {len(invalid)} skipped")
    return {"fetched": len(rows), "stored": stored, "updated": updated, "invalid": invalid}


@entrypoint(
    "list_records", kind="query", description="List stored records, optionally only flagged ones."
)
def list_records(input: dict, ctx) -> dict:
    table = ctx.resources.table("records")
    watched = input.get("watched")
    records = table.all() if watched is None else table.all(where={"watched": bool(watched)})
    return {"records": records, "total": len(records)}
