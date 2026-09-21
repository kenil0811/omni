# EXP-BUILDER — can a frontier coding agent build our Apps from a Build Brief?

Status: **done — passed, 15/15**
Plan step: 1
Blocks: step 3 (vertical slice)

## Question

Given a plain-language Build Brief and the App SDK, does the Builder produce an
App that passes an independent oracle it never sees — and how many repair rounds
does it take?

## Not the question

Not a product feature. Not a qualification of the shipped Builder. Not a
containment test. No Tauri, no IPC, no platform service, no UI.

## Built

| Path | What |
|---|---|
| `app/packages/app-sdk-python/` | SDK: `@entrypoint`, tables with optimistic revisions and exact-match filters, Artifacts, errors, and `testing.harness` which loads an App and invokes it the way the platform will |
| `app/templates/python-app/` | What the Builder starts from: `app.yaml`, `src/handlers.py`, `tests/`, and `SDK.md` (the full API reference it reads) |
| `app/fixtures/apps/app-collect/` | Brief, `snapshot-1/2.json`, `EXPECTED.md`, oracle — HTTP collection, dedupe, in-place update, configurable rule |
| `app/fixtures/apps/app-files/` | Brief, two CSVs, `EXPECTED.md`, oracle — file import, exceptions with line numbers, report Artifact |
| `app/fixtures/apps/app-tracker/` | Brief, `EXPECTED.md`, oracle — CRUD, filters, ordering, summary, optimistic revision conflict |
| `app/tools/exp_builder/run.py` | The runner: copy template → Builder → checks → ≤2 repair rounds → results |
| `app/tools/exp_builder/reference/` | Hand-written Apps used **only** to prove the oracles are right. Never shown to the Builder |
| `app/tools/exp_builder/selftest_test.py` | Proves the checks discriminate |

## How a run works

1. Copy `templates/python-app` into a fresh workspace under `docs/tasks/EXP-BUILDER/runs/<fixture>/<n>/app`.
2. Run `claude -p "<prompt>" --output-format json --permission-mode acceptEdits --max-turns 40` with `cwd` = that workspace. The prompt is the brief plus the required Entrypoint ids. The Builder sees the template and `SDK.md`; it cannot reach the oracle, which lives outside its cwd.
3. Checks, in order — a later one runs only if the previous passed:
   - `manifest` — `app.yaml` parses and declares every required Entrypoint with a `<module>.<function>` handler
   - `app_tests` — the App's own tests pass
   - `oracle` — the independent oracle passes
4. On failure, up to **2** repair rounds. Feedback carries the App's own test output in full, but for the oracle only the failing test names and assertion lines — never its source. This mirrors what the product would tell a user: what went wrong, not the answer key.
5. Record pass/fail, repair rounds, turns, wall time, cost, and a failure category (`contract_miss`, `own_tests_failed`, `behaviour_wrong`, `builder_error`).

Runs: **5 per fixture** (15 total). Record the actual count if subscription limits cut it short.

## Success threshold (fixed before running)

- ≥ 4/5 runs per fixture pass all three checks within 2 repair rounds.

Below threshold → fix the brief, template, or SDK shape and rerun. Patching
generated code by hand to make a run pass is recorded as a failure.

## Verification so far

Run on macOS 26.6.2 arm64, Python 3.13.9, uv 0.12.17, claude 2.1.278.

| Command | Result |
|---|---|
| `uv run pytest -q` | **9 passed, 29 skipped** — oracles skip without an App under test, by design |
| `uv run pytest tools/exp_builder/selftest_test.py -q` | **9 passed** |
| `ALPHA_APP_DIR=…/reference/app-collect uv run pytest fixtures/apps/app-collect/oracle_test.py -q` | **8 passed** |
| `ALPHA_APP_DIR=…/reference/app-files uv run pytest fixtures/apps/app-files/oracle_test.py -q` | **7 passed** |
| `ALPHA_APP_DIR=…/reference/app-tracker uv run pytest fixtures/apps/app-tracker/oracle_test.py -q` | **14 passed** |
| `uv run ruff check .` / `ruff format --check .` | clean, 26 files formatted |

What that establishes: all 29 oracle assertions pass against a correct App, and
the runner's checks reject the untouched template for every fixture, a missing
`app.yaml`, an App with no tests, and an oracle that skipped instead of running.
So a failed EXP-BUILDER run means the Builder missed, not that the harness is
broken.

Two bugs were found this way and fixed: the harness re-ran Entrypoint decorators
on reload, and a skipped oracle exited 0 and would have been recorded as a pass.

## Results

Run 21 Sep 2026 by the founder on macOS 26.6.2 arm64, claude 2.1.278. Builder
model: Opus 5 (1M context), with Haiku 4.5 handling small side calls.
`docs/tasks/EXP-BUILDER/runs/results.json` has every run.

| Fixture | Runs | Pass | Avg repairs | Avg turns | Avg wall | Avg cost |
|---|---|---|---|---|---|---|
| app-collect | 5 | 5 | 0.0 | 16 | 123s | $0.81 |
| app-files | 5 | 5 | 0.0 | 17 | 97s | $0.77 |
| app-tracker | 5 | 5 | 0.0 | 12 | 67s | $0.58 |

Cost is the CLI's API-equivalent figure. It was billed against the
subscription, not paid, but it is the right number for product economics:
**about $0.50–$1.00 and 1–3 minutes per App build.**

Checked after the run, beyond the oracle:

- **No hardcoding.** No generated handler contains a fixture value (`A-1009`,
  `orders-b`, seed titles, snapshot names).
- **No escape.** No builder log or workspace references the oracle, the
  reference Apps, `EXPECTED.md`, or `fixtures/`.
- **Stayed inside the SDK.** Only stdlib plus `app_sdk`; no `sqlite3`,
  `subprocess`, `os.environ`, or third-party HTTP. `socket` appears only to catch
  a timeout type. Every `pyproject.toml` kept `dependencies = []`.
- The generated Apps are 99–191 lines of handlers with 166–298 lines of their own
  tests.

## Decision

**Go.** The threshold (≥4/5 per fixture) is met at 5/5 with zero repairs. The
Build Brief + template + SDK shape is not the bottleneck, and Python generated
Apps are fine: TS / agent-native-style Apps are not revisited (plan decision 3).

What this does **not** show, read honestly:

1. **It was too easy.** Zero repairs in 15 runs means these fixtures sit below the
   Builder's ceiling. They cannot distinguish two good Builders, and never
   exercised the repair loop.
2. **Create only.** The spec's Builder scorecard also needs a plain-language
   *correction* of an existing App and an *induced repair*. Neither ran.
3. **Briefs were perfect.** Every brief pinned Entrypoint ids and output keys. In
   the product the Assistant writes the brief from a vague request; that step is
   untested.
4. No browser, no custom UI, no schedule — those arrive with steps 6 and 7.

## Finding for the spec

No generated App used FastAPI, and none needed to. Because an Entrypoint is a
plain function with `(input, ctx)`, the HTTP/IPC server belongs in the
platform's `workers/app-runtime`, which hosts whatever Entrypoints a package
declares. Generated Apps then need no web framework, no ports, and no server
lifecycle. That shrinks every generated package, removes a class of Builder
mistakes, and makes the runtime the one place transport security lives.

Proposed change: `alpha/specifications/Current Release Specification.md` §Runtime
profile and D-032 say the generated backend is "Python 3.13, FastAPI, Pydantic 2,
and Uvicorn". Amend to: generated backend is Python 3.13 functions declared
through the App SDK; FastAPI/Uvicorn live in the platform `app-runtime` worker.
**Approved by the founder and applied 21 Sep 2026** (see `docs/PLAN.md` decision 8).

## Limitations

- One Builder (Claude Code CLI) on one machine. A second adapter is a separate
  comparison, per `docs/PLAN.md`.
- The CLI loads user-level Claude Code settings; a user `CLAUDE.md` could
  influence generation. Note it if results look odd.
- Briefs pin exact Entrypoint ids and output keys. That is deliberate — the
  product's Assistant would too — but it means this measures build quality, not
  the Assistant's ability to write a good brief. That is a later question.
