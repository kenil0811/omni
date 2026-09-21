"""Tests for this App. They run against the real SDK harness, not mocks."""

from __future__ import annotations

from pathlib import Path

from app_sdk.testing import harness

APP_DIR = Path(__file__).resolve().parents[1]


def test_example_entrypoint() -> None:
    with harness(APP_DIR) as app:
        assert "example" in app.entrypoint_ids()
        assert app.invoke("example", {}) == {"ok": True}
