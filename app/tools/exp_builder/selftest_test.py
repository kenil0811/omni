"""The runner's checks must discriminate before the experiment is worth running.

A reference App must pass every check; the untouched template must fail. If
these do not hold, an EXP-BUILDER result says nothing about the Builder.
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent))

from run import (  # noqa: E402
    REQUIRED_ENTRYPOINTS,
    TEMPLATE,
    check_app_tests,
    check_manifest,
    check_oracle,
    oracle_summary,
)

REFERENCE = Path(__file__).parent / "reference"
FIXTURES = sorted(REQUIRED_ENTRYPOINTS)


@pytest.mark.parametrize("fixture", FIXTURES)
def test_reference_passes_manifest_and_oracle(fixture: str) -> None:
    app = REFERENCE / fixture
    manifest = check_manifest(app, fixture)
    assert manifest.passed, manifest.detail
    oracle = check_oracle(app, fixture)
    assert oracle.passed, oracle.detail


@pytest.mark.parametrize("fixture", FIXTURES)
def test_untouched_template_fails_every_fixture(tmp_path: Path, fixture: str) -> None:
    workspace = tmp_path / "app"
    shutil.copytree(TEMPLATE, workspace)

    manifest = check_manifest(workspace, fixture)
    assert not manifest.passed, "the placeholder template must not satisfy a brief"
    assert "entrypoint" in manifest.detail.lower()

    oracle = check_oracle(workspace, fixture)
    assert not oracle.passed, "the oracle must reject the placeholder template"


def test_missing_manifest_is_reported(tmp_path: Path) -> None:
    result = check_manifest(tmp_path, "app-files")
    assert not result.passed
    assert "app.yaml" in result.detail


def test_app_without_tests_fails_that_check(tmp_path: Path) -> None:
    workspace = tmp_path / "app"
    shutil.copytree(TEMPLATE, workspace)
    shutil.rmtree(workspace / "tests")
    result = check_app_tests(workspace)
    assert not result.passed
    assert "no tests" in result.detail


def test_oracle_feedback_does_not_leak_the_answer_key() -> None:
    """Repair feedback carries failure lines, never the oracle's source."""
    detail = (
        "fixtures/apps/app-collect/oracle_test.py:44: in test_snapshot_1\n"
        "    assert result['stored'] == 8\n"
        "E   assert 9 == 8\n"
        "FAILED fixtures/apps/app-collect/oracle_test.py::test_snapshot_1 - assert 9 == 8\n"
    )
    summary = oracle_summary(detail)
    assert "E   assert 9 == 8" in summary or "E assert 9 == 8" in summary
    assert "FAILED" in summary
    assert "in test_snapshot_1\n" not in summary
