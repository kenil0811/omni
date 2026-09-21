"""Order Intake — reference implementation (oracle self-test only)."""

from __future__ import annotations

import csv
import io
from pathlib import Path

from app_sdk import InvalidInput, entrypoint

STATUSES = ("new", "paid", "cancelled")
COLUMNS = ("order_id", "customer", "amount", "status")


def _problem(row: dict) -> str | None:
    """Why this row cannot be imported, or None when it is fine."""
    order_id = (row.get("order_id") or "").strip()
    if not order_id:
        return "order_id is empty"
    if not (row.get("customer") or "").strip():
        return "customer is empty"
    raw_amount = (row.get("amount") or "").strip()
    if not raw_amount:
        return "amount is empty"
    try:
        amount = float(raw_amount)
    except ValueError:
        return f"amount {raw_amount!r} is not a number"
    if amount < 0:
        return "amount is negative"
    status = (row.get("status") or "").strip()
    if status not in STATUSES:
        return f"status {status!r} is not one of {', '.join(STATUSES)}"
    return None


def _report(counts: dict[str, int], imported: int, exceptions: int) -> str:
    lines = [
        "# Order intake",
        "",
        f"Imported: {imported}",
        f"Exceptions: {exceptions}",
        "",
        "| Status | Count |",
        "|---|---|",
    ]
    lines += [f"| {status} | {counts.get(status, 0)} |" for status in STATUSES]
    return "\n".join(lines) + "\n"


@entrypoint(
    "import_files",
    kind="action",
    description="Import selected CSV files and write a summary report.",
)
def import_files(input: dict, ctx) -> dict:
    table = ctx.resources.table("orders")
    imported = 0
    exceptions: list[dict] = []

    for raw_path in input.get("files") or []:
        path = Path(str(raw_path))
        if not path.exists():
            raise InvalidInput(f"{path.name} does not exist")
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as exc:
            raise InvalidInput(f"{path.name} could not be read: {exc}") from exc

        reader = csv.DictReader(io.StringIO(text))
        if not reader.fieldnames or not set(COLUMNS) <= set(reader.fieldnames):
            raise InvalidInput(f"{path.name} does not have the expected columns")

        # Header is line 1, so the first data row is line 2.
        for line, row in enumerate(reader, start=2):
            problem = _problem(row)
            if problem:
                exceptions.append({"file": path.name, "row": line, "reason": problem})
                continue
            order_id = row["order_id"].strip()
            if table.get(order_id) is not None:
                exceptions.append(
                    {
                        "file": path.name,
                        "row": line,
                        "reason": f"order {order_id} was already imported",
                    }
                )
                continue
            table.insert(
                {
                    "id": order_id,
                    "order_id": order_id,
                    "customer": row["customer"].strip(),
                    "amount": float(row["amount"].strip()),
                    "status": row["status"].strip(),
                    "source_file": path.name,
                }
            )
            imported += 1

    counts: dict[str, int] = {}
    for record in table.all():
        counts[record["status"]] = counts.get(record["status"], 0) + 1

    report = ctx.artifacts.write(
        "report.md", _report(counts, imported, len(exceptions)), "text/markdown"
    )
    ctx.log(f"{imported} imported, {len(exceptions)} rejected")
    return {"imported": imported, "exceptions": exceptions, "report": report.name}


@entrypoint(
    "list_orders", kind="query", description="List imported orders, optionally filtered by status."
)
def list_orders(input: dict, ctx) -> dict:
    table = ctx.resources.table("orders")
    status = input.get("status")
    orders = table.all() if status is None else table.all(where={"status": str(status)})
    return {"orders": orders, "total": len(orders)}
