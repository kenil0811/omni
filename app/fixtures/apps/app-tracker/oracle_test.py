"""Independent oracle for app-tracker. Expected values come from EXPECTED.md.

Written before any App was generated. Never edit an assertion to match
generated output — a mismatch is a failed run.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from app_sdk import InvalidInput, RevisionConflict
from app_sdk.testing import harness

SEED = [
    {"title": "Draft the report", "status": "todo", "priority": 2},
    {"title": "Call the supplier", "status": "doing", "priority": 1},
    {"title": "File expenses", "status": "todo", "priority": 4},
    {"title": "Book travel", "status": "done", "priority": 3},
    {"title": "Review contract", "status": "todo", "priority": 1},
]


def _seed(app) -> list[str]:
    return [app.invoke("create_item", dict(item))["id"] for item in SEED]


def test_declares_required_entrypoints(app_dir: Path) -> None:
    with harness(app_dir) as app:
        declared = set(app.entrypoint_ids())
        required = {"create_item", "update_item", "list_items", "summarize"}
        assert required <= declared, f"declared: {sorted(declared)}"


def test_create_returns_first_revision(app_dir: Path) -> None:
    with harness(app_dir) as app:
        created = app.invoke("create_item", {"title": "Draft the report"})
        assert created["revision"] == 1
        assert created["id"]


def test_defaults_are_applied(app_dir: Path) -> None:
    with harness(app_dir) as app:
        created = app.invoke("create_item", {"title": "Only a title"})
        stored = app.table("items").get(created["id"])
        assert stored["status"] == "todo"
        assert stored["priority"] == 3
        assert stored["notes"] == ""


def test_list_and_filter(app_dir: Path) -> None:
    with harness(app_dir) as app:
        _seed(app)

        everything = app.invoke("list_items", {})
        assert everything["total"] == 5
        assert len(everything["items"]) == 5

        todo = app.invoke("list_items", {"status": "todo"})
        assert todo["total"] == 3
        assert {i["title"] for i in todo["items"]} == {
            "Draft the report",
            "File expenses",
            "Review contract",
        }


def test_list_is_ordered_by_priority_then_title(app_dir: Path) -> None:
    with harness(app_dir) as app:
        _seed(app)
        titles = [i["title"] for i in app.invoke("list_items", {})["items"]]
        assert titles == [
            "Call the supplier",
            "Review contract",
            "Draft the report",
            "Book travel",
            "File expenses",
        ]


def test_summarize_counts_every_status(app_dir: Path) -> None:
    with harness(app_dir) as app:
        _seed(app)
        assert app.invoke("summarize", {}) == {
            "total": 5,
            "by_status": {"todo": 3, "doing": 1, "done": 1},
        }


def test_summarize_reports_empty_buckets_as_zero(app_dir: Path) -> None:
    with harness(app_dir) as app:
        app.invoke("create_item", {"title": "Only one", "status": "todo"})
        assert app.invoke("summarize", {}) == {
            "total": 1,
            "by_status": {"todo": 1, "doing": 0, "done": 0},
        }


def test_update_advances_revision(app_dir: Path) -> None:
    with harness(app_dir) as app:
        created = app.invoke("create_item", {"title": "Draft the report"})
        updated = app.invoke(
            "update_item",
            {"id": created["id"], "revision": 1, "changes": {"status": "doing"}},
        )
        assert updated["revision"] == 2
        assert app.table("items").get(created["id"])["status"] == "doing"


def test_stale_revision_is_rejected_and_preserves_the_winner(app_dir: Path) -> None:
    with harness(app_dir) as app:
        created = app.invoke("create_item", {"title": "Draft the report"})
        app.invoke(
            "update_item",
            {"id": created["id"], "revision": 1, "changes": {"status": "doing"}},
        )

        with pytest.raises(RevisionConflict):
            app.invoke(
                "update_item",
                {"id": created["id"], "revision": 1, "changes": {"status": "done"}},
            )

        assert app.table("items").get(created["id"])["status"] == "doing"


@pytest.mark.parametrize(
    "payload",
    [
        {"title": ""},
        {"title": "Bad status", "status": "archived"},
        {"title": "Low priority", "priority": 0},
        {"title": "High priority", "priority": 9},
    ],
)
def test_invalid_creation_is_rejected(app_dir: Path, payload: dict) -> None:
    with harness(app_dir) as app:
        with pytest.raises(InvalidInput):
            app.invoke("create_item", payload)
        assert app.table("items").count() == 0


def test_invalid_update_is_rejected(app_dir: Path) -> None:
    with harness(app_dir) as app:
        created = app.invoke("create_item", {"title": "Draft the report"})
        with pytest.raises(InvalidInput):
            app.invoke(
                "update_item",
                {"id": created["id"], "revision": 1, "changes": {"status": "archived"}},
            )
        assert app.table("items").get(created["id"])["status"] == "todo"
