"""Independent oracle for app-files. Expected values come from EXPECTED.md.

Written before any App was generated. Never edit an assertion to match
generated output — a mismatch is a failed run.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from app_sdk.testing import harness

DATA = Path(__file__).parent / "data"
FILE_A = str(DATA / "orders-a.csv")
FILE_B = str(DATA / "orders-b.csv")


def test_declares_required_entrypoints(app_dir: Path) -> None:
    with harness(app_dir) as app:
        declared = set(app.entrypoint_ids())
        assert {"import_files", "list_orders"} <= declared, f"declared: {sorted(declared)}"


def test_imports_valid_rows_and_reports_exceptions(app_dir: Path) -> None:
    with harness(app_dir) as app:
        result = app.invoke("import_files", {"files": [FILE_A, FILE_B]})

        assert result["imported"] == 7
        assert len(result["exceptions"]) == 2, result["exceptions"]

        flagged = {(e["file"], e["row"]) for e in result["exceptions"]}
        assert flagged == {("orders-b.csv", 3), ("orders-b.csv", 4)}, (
            "expected the empty amount on line 3 and the bad status on line 4"
        )
        for item in result["exceptions"]:
            assert str(item.get("reason", "")).strip(), "each exception needs a reason"

        stored = app.table("orders").all()
        assert len(stored) == 7
        assert {str(r.get("order_id") or r.get("id")) for r in stored} == {
            "A-1",
            "A-2",
            "A-3",
            "A-4",
            "A-5",
            "B-1",
            "B-4",
        }


def test_records_carry_source_file_name_only(app_dir: Path) -> None:
    with harness(app_dir) as app:
        app.invoke("import_files", {"files": [FILE_A, FILE_B]})
        for record in app.table("orders").all():
            source = str(record["source_file"])
            assert source in {"orders-a.csv", "orders-b.csv"}, source
            assert "/" not in source, "store the file name, not a path"


def test_list_orders_filters_by_status(app_dir: Path) -> None:
    with harness(app_dir) as app:
        app.invoke("import_files", {"files": [FILE_A, FILE_B]})

        everything = app.invoke("list_orders", {})
        assert everything["total"] == 7
        assert len(everything["orders"]) == 7

        paid = app.invoke("list_orders", {"status": "paid"})
        assert paid["total"] == 3
        assert {str(o.get("order_id") or o.get("id")) for o in paid["orders"]} == {
            "A-1",
            "A-3",
            "B-1",
        }

        assert app.invoke("list_orders", {"status": "new"})["total"] == 3
        assert app.invoke("list_orders", {"status": "cancelled"})["total"] == 1


def test_report_artifact_is_written_and_readable(app_dir: Path) -> None:
    with harness(app_dir) as app:
        result = app.invoke("import_files", {"files": [FILE_A, FILE_B]})

        name = result["report"]
        assert name, "import_files must return the report artifact name"
        body = app.artifacts.read(str(name)).decode("utf-8")

        assert "7" in body, "the report should state how many were imported"
        assert "2" in body, "the report should state how many were rejected"
        lowered = body.lower()
        assert "paid" in lowered and "new" in lowered and "cancelled" in lowered


def test_single_file_import(app_dir: Path) -> None:
    with harness(app_dir) as app:
        result = app.invoke("import_files", {"files": [FILE_A]})
        assert result["imported"] == 5
        assert result["exceptions"] == []
        assert app.invoke("list_orders", {"status": "paid"})["total"] == 2


def test_missing_file_is_rejected_by_name(app_dir: Path) -> None:
    from app_sdk import AppError

    with harness(app_dir) as app:
        with pytest.raises(AppError) as caught:
            app.invoke("import_files", {"files": [str(DATA / "not-here.csv")]})
        assert "not-here.csv" in str(caught.value)
