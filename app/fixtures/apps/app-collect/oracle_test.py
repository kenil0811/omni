"""Independent oracle for app-collect. Expected values come from EXPECTED.md.

Written before any App was generated. Never edit an assertion to match
generated output — a mismatch is a failed run.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from app_sdk.testing import harness

DATA = Path(__file__).parent / "data"

WATCHED_AFTER_1 = {"A-1002", "A-1004", "A-1005"}
WATCHED_AFTER_2 = {"A-1002", "A-1004", "A-1005", "A-1006", "A-1011"}


def _refs(records: list[dict]) -> set[str]:
    return {str(r.get("ref") or r.get("id")) for r in records}


def test_declares_required_entrypoints(app_dir: Path) -> None:
    with harness(app_dir) as app:
        declared = set(app.entrypoint_ids())
        assert {"collect", "list_records"} <= declared, f"declared: {sorted(declared)}"


def test_snapshot_1_dedupes_and_reports_invalid_rows(app_dir: Path, serve_dir) -> None:
    url = serve_dir(DATA)
    with harness(app_dir) as app:
        result = app.invoke("collect", {"source_url": url("snapshot-1.json")})

        assert result["fetched"] == 12
        assert result["stored"] == 8
        assert len(result["invalid"]) == 2, result["invalid"]
        assert {str(i.get("ref")) for i in result["invalid"]} == {"A-1009", "A-1010"}
        for item in result["invalid"]:
            assert str(item.get("reason", "")).strip(), "each invalid row needs a reason"

        records = app.table("records").all()
        assert len(records) == 8
        assert _refs(records) == {f"A-100{n}" for n in range(1, 9)}


def test_watch_rule_applies(app_dir: Path, serve_dir) -> None:
    url = serve_dir(DATA)
    with harness(app_dir) as app:
        app.invoke("collect", {"source_url": url("snapshot-1.json")})
        watched = [r for r in app.table("records").all() if r.get("watched")]
        assert _refs(watched) == WATCHED_AFTER_1


def test_watch_threshold_is_configurable(app_dir: Path, serve_dir) -> None:
    url = serve_dir(DATA)
    with harness(app_dir, config={"watch_above": 200}) as app:
        app.invoke("collect", {"source_url": url("snapshot-1.json")})
        watched = [r for r in app.table("records").all() if r.get("watched")]
        assert _refs(watched) == {"A-1002", "A-1005"}


def test_recollecting_same_snapshot_creates_nothing(app_dir: Path, serve_dir) -> None:
    url = serve_dir(DATA)
    with harness(app_dir) as app:
        app.invoke("collect", {"source_url": url("snapshot-1.json")})
        second = app.invoke("collect", {"source_url": url("snapshot-1.json")})

        assert second["stored"] == 0, "a repeated run must not create records"
        assert second["updated"] == 0, "nothing changed, so nothing to update"
        assert app.table("records").count() == 8


def test_snapshot_2_updates_in_place_and_adds_two(app_dir: Path, serve_dir) -> None:
    url = serve_dir(DATA)
    with harness(app_dir) as app:
        app.invoke("collect", {"source_url": url("snapshot-1.json")})
        result = app.invoke("collect", {"source_url": url("snapshot-2.json")})

        assert result["fetched"] == 10
        assert result["stored"] == 2, "A-1011 and A-1012 are new"
        assert result["updated"] == 1, "A-1006 changed price"

        records = app.table("records").all()
        assert len(records) == 10, "no duplicate may be created for a seen ref"
        assert _refs(records) == {f"A-100{n}" for n in range(1, 9)} | {"A-1011", "A-1012"}

        changed = next(r for r in records if str(r.get("ref") or r.get("id")) == "A-1006")
        assert float(changed["price"]) == 130.0
        assert changed["watched"] is True

        watched = [r for r in records if r.get("watched")]
        assert _refs(watched) == WATCHED_AFTER_2


def test_list_records_filters_by_watched(app_dir: Path, serve_dir) -> None:
    url = serve_dir(DATA)
    with harness(app_dir) as app:
        app.invoke("collect", {"source_url": url("snapshot-1.json")})
        app.invoke("collect", {"source_url": url("snapshot-2.json")})

        everything = app.invoke("list_records", {})
        assert everything["total"] == 10
        assert len(everything["records"]) == 10

        only_watched = app.invoke("list_records", {"watched": True})
        assert only_watched["total"] == 5
        assert _refs(only_watched["records"]) == WATCHED_AFTER_2

        not_watched = app.invoke("list_records", {"watched": False})
        assert not_watched["total"] == 5


def test_unreachable_source_fails_cleanly(app_dir: Path) -> None:
    from app_sdk import AppError

    with harness(app_dir) as app:
        with pytest.raises((AppError, OSError)):
            app.invoke("collect", {"source_url": "http://127.0.0.1:1/never.json"})
