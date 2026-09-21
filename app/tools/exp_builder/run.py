#!/usr/bin/env python3
"""EXP-BUILDER runner — plan step 1.

Drives a Builder adapter over the fixture Build Briefs and checks the result
against an independent oracle the Builder never sees.

    uv run python tools/exp_builder/run.py app-collect --runs 5
    uv run python tools/exp_builder/run.py --all --runs 5

Writes one directory per run under docs/tasks/EXP-BUILDER/runs/ and a
results.json summary. See docs/tasks/EXP-BUILDER.md.

The Builder here is the locally installed `claude` CLI. It is a development
tool for this experiment, not a product component: it is never bundled and
never offered to users. See docs/PLAN.md.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import statistics
import subprocess
import sys
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

APP_ROOT = Path(__file__).resolve().parents[2]
REPO_ROOT = APP_ROOT.parent
TEMPLATE = APP_ROOT / "templates" / "python-app"
FIXTURES = APP_ROOT / "fixtures" / "apps"
DEFAULT_OUT = REPO_ROOT / "docs" / "tasks" / "EXP-BUILDER" / "runs"

# Entrypoints each brief pins. Checked before the oracle so a missing one is
# reported as a contract miss rather than an assertion failure.
REQUIRED_ENTRYPOINTS: dict[str, set[str]] = {
    "app-collect": {"collect", "list_records"},
    "app-files": {"import_files", "list_orders"},
    "app-tracker": {"create_item", "update_item", "list_items", "summarize"},
}

ALLOWED_TOOLS = [
    "Read",
    "Write",
    "Edit",
    "Glob",
    "Grep",
    "Bash(uv run pytest:*)",
    "Bash(uv run python:*)",
    "Bash(python3:*)",
    "Bash(ls:*)",
    "Bash(cat:*)",
]

MAX_FEEDBACK_CHARS = 4000


@dataclass
class CheckResult:
    name: str
    passed: bool
    detail: str = ""

    def short(self) -> str:
        return f"{self.name}={'pass' if self.passed else 'FAIL'}"


@dataclass
class RunResult:
    fixture: str
    index: int
    passed: bool = False
    repair_rounds: int = 0
    turns: int = 0
    cost_usd: float = 0.0
    wall_seconds: float = 0.0
    builder_error: str = ""
    checks: list[dict[str, Any]] = field(default_factory=list)
    failure_category: str = ""
    workspace: str = ""


# --------------------------------------------------------------------------
# prompts


def build_prompt(fixture: str) -> str:
    brief = (FIXTURES / fixture / "brief.md").read_text(encoding="utf-8")
    required = ", ".join(sorted(REQUIRED_ENTRYPOINTS[fixture]))
    return f"""You are building an App for the Alpha platform. Everything you need
is in this directory.

Read SDK.md first — it is the complete API available to you. There is no other
platform API: no database connection, no credentials, no network client.

Then build the App described by the brief below.

Requirements:
- Declare exactly these Entrypoint ids: {required}. Use the input and output
  keys the brief specifies, exactly as written. A caller depends on them.
- Update app.yaml to describe the App: metadata, every entrypoint with its
  handler, and any table resources you use.
- Write the handlers in src/. Replace the placeholder `example` entrypoint.
- Write real tests in tests/ using `app_sdk.testing.harness`, covering the
  behaviour the brief describes including the failure cases.
- Run your tests with `uv run pytest tests/` from this directory and make them
  pass before you finish.
- Only the Python standard library and app_sdk. Do not add dependencies.
- Work only inside this directory.

--- BRIEF ---

{brief}
"""


def build_repair_prompt(feedback: str) -> str:
    return f"""The App does not pass its checks yet. Fix it.

{feedback}

Re-read SDK.md and the brief if you need to. Work only inside this directory.
Run `uv run pytest tests/` and make your tests pass before you finish.
Do not weaken or delete a test to make it pass.
"""


# --------------------------------------------------------------------------
# builder


def invoke_builder(workspace: Path, prompt: str, max_turns: int, log: Path) -> dict[str, Any]:
    """Run the Claude Code CLI headless in `workspace`. Returns its JSON result."""
    command = [
        "claude",
        "-p",
        prompt,
        "--output-format",
        "json",
        "--permission-mode",
        "acceptEdits",
        "--max-turns",
        str(max_turns),
        "--allowedTools",
        *ALLOWED_TOOLS,
    ]
    started = time.monotonic()
    completed = subprocess.run(
        command,
        cwd=workspace,
        capture_output=True,
        text=True,
        timeout=3600,
        check=False,
    )
    elapsed = time.monotonic() - started
    payload: dict[str, Any]
    try:
        payload = json.loads(completed.stdout or "{}")
    except json.JSONDecodeError:
        payload = {"_unparsed_stdout": completed.stdout[-4000:]}
    payload["_exit_code"] = completed.returncode
    payload["_stderr"] = completed.stderr[-4000:]
    payload["_wall_seconds"] = round(elapsed, 1)
    log.write_text(json.dumps(payload, indent=2)[:400_000], encoding="utf-8")
    return payload


# --------------------------------------------------------------------------
# checks


def _pytest(
    target: str, env_extra: dict[str, str] | None = None
) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    env.update(env_extra or {})
    return subprocess.run(
        [
            "uv",
            "run",
            "--project",
            str(APP_ROOT),
            "pytest",
            target,
            "-q",
            "--no-header",
            "-p",
            "no:cacheprovider",
        ],
        cwd=APP_ROOT,
        capture_output=True,
        text=True,
        env=env,
        timeout=900,
        check=False,
    )


def check_manifest(workspace: Path, fixture: str) -> CheckResult:
    import yaml

    manifest_path = workspace / "app.yaml"
    if not manifest_path.exists():
        return CheckResult("manifest", False, "app.yaml is missing")
    try:
        manifest = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        return CheckResult("manifest", False, f"app.yaml does not parse: {exc}")
    if not isinstance(manifest, dict):
        return CheckResult("manifest", False, "app.yaml is not a mapping")

    entries = (manifest.get("spec") or {}).get("entrypoints") or []
    declared = {str(e.get("id")) for e in entries if isinstance(e, dict)}
    missing = REQUIRED_ENTRYPOINTS[fixture] - declared
    if missing:
        return CheckResult(
            "manifest",
            False,
            f"app.yaml does not declare required entrypoints: {sorted(missing)}"
            f" (declared: {sorted(declared)})",
        )
    for entry in entries:
        if "." not in str(entry.get("handler", "")):
            return CheckResult(
                "manifest",
                False,
                f"entrypoint {entry.get('id')!r} needs handler '<module>.<function>'",
            )
    return CheckResult("manifest", True, f"declares {sorted(declared)}")


def check_app_tests(workspace: Path) -> CheckResult:
    tests = workspace / "tests"
    if not tests.is_dir() or not any(tests.glob("test_*.py")):
        return CheckResult("app_tests", False, "the App has no tests of its own")
    result = _pytest(str(tests))
    tail = (result.stdout + result.stderr)[-MAX_FEEDBACK_CHARS:]
    return CheckResult("app_tests", result.returncode == 0, tail)


def check_oracle(workspace: Path, fixture: str) -> CheckResult:
    oracle = FIXTURES / fixture / "oracle_test.py"
    result = _pytest(str(oracle), {"ALPHA_APP_DIR": str(workspace)})
    output = result.stdout + result.stderr
    # A skipped or uncollected oracle exits 0. That is not a pass: it means the
    # oracle never examined the App.
    if "no tests ran" in output or "skipped" in output.lower():
        return CheckResult("oracle", False, "the oracle did not run:\n" + output[-2000:])
    if " passed" not in output:
        return CheckResult(
            "oracle", False, "the oracle reported no passing test:\n" + output[-2000:]
        )
    return CheckResult("oracle", result.returncode == 0, output[-MAX_FEEDBACK_CHARS:])


def oracle_summary(detail: str) -> str:
    """Failing oracle test names and assertion messages only — not its source.

    The Builder must not see the oracle. Repair feedback stands in for what the
    product would tell a user: what went wrong, not the answer key.
    """
    lines: list[str] = []
    for line in detail.splitlines():
        stripped = line.strip()
        if stripped.startswith(("FAILED", "ERROR")) or stripped.startswith("E "):
            lines.append(stripped[:300])
    return "\n".join(lines[:40])[:MAX_FEEDBACK_CHARS] or detail[-1500:]


def collect_feedback(checks: list[CheckResult]) -> str:
    parts: list[str] = []
    for check in checks:
        if check.passed:
            continue
        if check.name == "oracle":
            parts.append(
                "An independent check of the App's behaviour failed. You cannot see"
                " that check; these are the failures it reported. Re-read the brief"
                " — the expected values come from it.\n\n" + oracle_summary(check.detail)
            )
        elif check.name == "app_tests":
            parts.append("Your own tests failed:\n\n" + check.detail)
        else:
            parts.append(check.detail)
    return "\n\n".join(parts)


def categorize(checks: list[CheckResult], builder_error: str) -> str:
    if builder_error:
        return "builder_error"
    by_name = {c.name: c for c in checks}
    if not by_name.get("manifest", CheckResult("manifest", True)).passed:
        return "contract_miss"
    if not by_name.get("app_tests", CheckResult("app_tests", True)).passed:
        return "own_tests_failed"
    if not by_name.get("oracle", CheckResult("oracle", True)).passed:
        return "behaviour_wrong"
    return ""


# --------------------------------------------------------------------------
# one run


def run_once(fixture: str, index: int, out_dir: Path, repairs: int, max_turns: int) -> RunResult:
    run_dir = out_dir / fixture / str(index)
    if run_dir.exists():
        shutil.rmtree(run_dir)
    run_dir.mkdir(parents=True)
    workspace = run_dir / "app"
    shutil.copytree(TEMPLATE, workspace)

    result = RunResult(fixture=fixture, index=index, workspace=str(workspace))
    started = time.monotonic()
    prompt = build_prompt(fixture)

    for attempt in range(repairs + 1):
        payload = invoke_builder(workspace, prompt, max_turns, run_dir / f"builder-{attempt}.json")
        result.turns += int(payload.get("num_turns") or 0)
        result.cost_usd += float(payload.get("total_cost_usd") or 0.0)
        if payload.get("is_error") or payload.get("_exit_code") not in (0, None):
            result.builder_error = str(
                payload.get("result") or payload.get("_stderr") or "builder exited non-zero"
            )[:2000]

        checks = [check_manifest(workspace, fixture)]
        if checks[0].passed:
            checks.append(check_app_tests(workspace))
            checks.append(check_oracle(workspace, fixture))
        result.checks = [asdict(c) for c in checks]
        result.repair_rounds = attempt

        if all(c.passed for c in checks):
            result.passed = True
            break
        if attempt == repairs:
            break
        prompt = build_repair_prompt(collect_feedback(checks))

    result.wall_seconds = round(time.monotonic() - started, 1)
    result.failure_category = categorize(
        [CheckResult(**c) for c in result.checks], result.builder_error
    )
    (run_dir / "result.json").write_text(json.dumps(asdict(result), indent=2), encoding="utf-8")
    return result


# --------------------------------------------------------------------------
# reporting


def summarize(results: list[RunResult]) -> str:
    rows = [
        "| Fixture | Runs | Pass | Avg repairs | Avg turns | Avg wall | Avg cost |",
        "|---|---|---|---|---|---|---|",
    ]
    for fixture in sorted({r.fixture for r in results}):
        group = [r for r in results if r.fixture == fixture]
        passed = [r for r in group if r.passed]
        rows.append(
            f"| {fixture} | {len(group)} | {len(passed)} "
            f"| {statistics.mean([r.repair_rounds for r in group]):.1f} "
            f"| {statistics.mean([r.turns for r in group]):.0f} "
            f"| {statistics.mean([r.wall_seconds for r in group]):.0f}s "
            f"| ${statistics.mean([r.cost_usd for r in group]):.2f} |"
        )
    failures = [r for r in results if not r.passed]
    if failures:
        rows.append("")
        rows.append("| Fixture | Run | Category |")
        rows.append("|---|---|---|")
        for item in failures:
            rows.append(f"| {item.fixture} | {item.index} | {item.failure_category} |")
    return "\n".join(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fixtures", nargs="*", choices=sorted(REQUIRED_ENTRYPOINTS), default=None)
    parser.add_argument("--all", action="store_true", help="run every fixture")
    parser.add_argument("--runs", type=int, default=5)
    parser.add_argument("--repairs", type=int, default=2, help="repair rounds allowed per run")
    parser.add_argument("--max-turns", type=int, default=40)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()

    selected = sorted(REQUIRED_ENTRYPOINTS) if args.all else list(args.fixtures or [])
    if not selected:
        parser.error("name at least one fixture, or pass --all")
    if shutil.which("claude") is None:
        parser.error("the `claude` CLI is not on PATH; install it and log in")

    args.out.mkdir(parents=True, exist_ok=True)
    results: list[RunResult] = []
    for fixture in selected:
        for index in range(1, args.runs + 1):
            print(f"-- {fixture} run {index}/{args.runs}", flush=True)
            result = run_once(fixture, index, args.out, args.repairs, args.max_turns)
            checks = ", ".join(CheckResult(**c).short() for c in result.checks)
            print(
                f"   {'PASS' if result.passed else 'FAIL'}"
                f" repairs={result.repair_rounds} turns={result.turns}"
                f" {result.wall_seconds}s ${result.cost_usd:.2f} [{checks}]",
                flush=True,
            )
            results.append(result)

    (args.out / "results.json").write_text(
        json.dumps([asdict(r) for r in results], indent=2), encoding="utf-8"
    )
    table = summarize(results)
    (args.out / "results.md").write_text(table + "\n", encoding="utf-8")
    print("\n" + table)
    return 0 if all(r.passed for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
