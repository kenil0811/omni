# Alpha — working plan

Last updated: 21 September 2026

## End goal (unchanged)

Everything in `alpha/` still defines what Alpha is and what "done" means:

- `alpha/product/Product Vision and Principles.md` — the product.
- `alpha/architecture/Implementation Blueprint.md` — the target repository, process, and trust shape.
- `alpha/delivery/Prototype_Scope_and_Acceptance.md` — the acceptance IDs (CONTRACT-01 … TRUST-01) that must eventually pass.

This plan changes **the order we reach that shape and how much ceremony surrounds each step**. It does not change scope, authority boundaries, contracts, or the definition of done.

## What changed and why

| Before (bundle as written) | Now | Why |
|---|---|---|
| P0 contracts → P1 IPC → P2 Tasks → P3 fake App lifecycle → **P4 real Builder** | **Real Builder first**, then packaging, then an ugly vertical slice, then the rest | The riskiest assumption (an LLM Builder produces working Apps from a Build Brief) was tested last. Now it is tested in week 1. |
| DeepSeek Harness first adapter, requires API key | Dev-only **Claude Code CLI adapter** first (uses the founder's own subscription via the locally installed `claude` binary); DeepSeek adapter second, when an API key exists | Zero marginal cost. Same `BuilderHarness` interface; the product ships neither adapter until one qualifies. |
| Snapshot manifests, hash verification, 13-field task packets, 12-field evidence bundles, Coordinator/Implementer/Reviewer/Verifier roles | `AGENTS.md` rules + this file + one short `docs/tasks/<id>.md` per experiment with a results section | The rules were good; the ceremony would cost more agent context than the code. |
| Full UDS/boot-secret IPC before any product behavior | Loopback HTTP + token first; harden to the blueprint's design once containment is decided | The blueprint itself admits same-user generated code is uncontained; elaborate IPC auth protects little until that changes. |
| React/Vite generated Surface, x86_64, Windows CI, OpenCode adapter in first release | Deferred until the Python/trusted-fallback path works on arm64 | Halves first-release scope. Custom UI was already optional in the spec. |

Stack is unchanged except one EXP-BUILDER-driven refinement: Tauri 2 + React/TS shell, bundled Python core, Python generated Apps as SDK-declared Entrypoint functions (FastAPI/Uvicorn live once in the platform `app-runtime` worker), SQLite + content-addressed Artifacts + Keychain.

## Sequence

Each step ends when its results file in `docs/tasks/` says what was observed. "Green scaffolding" is not done.

| # | Step | Outcome | Go/no-go question |
|---|---|---|---|
| 1 | **EXP-BUILDER** | Bare Python script drives the Claude Code CLI to generate the three fixture Apps into the template; runs their tests; records pass rate, repair attempts, turns, cost. Independent oracle for the 12-row dedup fixture. | Does a frontier agent produce a working Python App from our Build Brief ≥ 8/10 times, with ≤ 2 repair rounds? If not, fix the Brief/template/contract *before* building infrastructure on them. |
| 2 | **EXP-PACKAGE** | Tauri app launches a bundled relocatable CPython, WebView shows a response from it. arm64, ad-hoc signed, no Apple Developer account. Also record what a tester sees on first open of a quarantined copy. | Can we ship Python inside a Tauri app without asking users to install anything? |
| 3 | **Vertical slice** | Shell → Core (loopback HTTP + token) → real Builder → run the generated App's Entrypoints in a supervised `app-runtime` subprocess → results in the shell. Real SQLite. No Versions/rollback yet. | Can a person type a request and use the result without a terminal? |
| 4 | **Tasks** | Answer / Do once path: Task, Revision, Attempt, fixed tools, parser-helper subprocess with rlimits, output Artifacts, cancel/retry. | Blueprint P2 content. |
| 5 | **Versions, Releases, rollback, correction** | Immutable Version, Release pointer, correction Build, compare, rollback. | Blueprint P3 content. |
| 6 | **Scheduler** | Durable occurrences, visible missed jobs, manual retrigger, window-close continuation. | Blueprint P5 (schedule part). |
| 7 | **Browser** | Playwright/Chromium worker; public sites first, then dedicated-profile sign-in + takeover. | Blueprint P5 (browser part). |
| 8 | **Harden to blueprint** | Private UDS IPC + boot secret, `packages/contracts/` with generated types, worker registry, containment decision, DeepSeek/other adapter qualification, x86_64, Windows CI, Developer ID signing + notarization (needs the $99 Apple Developer account; only required to distribute beyond hand-held testers). | Blueprint P0/P1 protocol gates, P6, P7. |

Steps 1 and 2 are independent and can run in parallel. Nothing in step 3+ starts until step 1 has a results file.

## Builder policy

- `BuilderHarness` (see `alpha/specifications/contracts/Builder Harness Interface.md`) stays the only way Core talks to any Builder.
- `workers/builder/adapters/claude_code_cli.py` — **dev-only**. Shells out to the locally installed `claude` binary in headless mode. Refuses to load unless `config/policies/internal-prototype.toml` enables it. Never bundled, never offered to users. Exists to answer EXP-BUILDER and to drive development until a shippable adapter qualifies.
- `workers/builder/adapters/deepseek.py` — second adapter, same fixtures, when a DeepSeek API key is available.
- `workers/builder/adapters/fake.py` — deterministic contract control for fast tests.
- Default shipped adapter is chosen only after both real adapters run the identical fixture set (the spec's two-adapter rule stands; only the order changed).

## Repository layout

All code lives under `app/`. `alpha/` is the spec; `docs/` is plan and results. Inside `app/` we follow the blueprint's monorepo layout but create a directory only when a step needs it.

```text
omni/
├── AGENTS.md
├── alpha/                      spec (read-only by convention)
├── docs/
│   ├── PLAN.md
│   └── tasks/<id>.md           one file per step/experiment, results inline
└── app/                        the product
    ├── Justfile
    ├── pyproject.toml          uv workspace root
    ├── uv.lock
    ├── .python-version         3.13
    ├── fixtures/apps/…         briefs, data, oracles           (step 1)
    ├── templates/python-app/   generated-App template          (step 1)
    ├── packages/app-sdk-python/ SDK — stub in step 1, real from step 3
    ├── tools/exp_builder/      EXP-BUILDER runner              (step 1)
    ├── packaging/macos/        EXP-PACKAGE spike               (step 2)
    ├── apps/desktop/           Tauri + React shell             (step 2/3)
    ├── services/core/          Python platform service         (step 3)
    ├── workers/builder/        BuilderHarness adapters         (step 3)
    ├── workers/app-runtime/    runs a generated App            (step 3)
    ├── workers/parser-helper/                                  (step 4)
    ├── workers/browser-runtime/                                (step 7)
    ├── packages/contracts/     schemas moved from alpha/       (step 5/8)
    └── config/                 runtime profiles, policies      (step 3)
```

## Working rules

See `AGENTS.md`. The short version: read before editing, one bounded step at a time, real components for integration claims, never weaken a test to pass, never claim something ran without its output, keep secrets and session data out of the repo.

## Status

- [x] 1 EXP-BUILDER — `docs/tasks/EXP-BUILDER.md` — **go**: 15/15 passed, 0 repairs, ~$0.50–1.00 and 1–3 min per App build
- [x] 2 EXP-PACKAGE — `docs/tasks/EXP-PACKAGE.md` — **go**: 80 MB .app, Python ready in ~260 ms, runs with nothing installed, no orphans; first-open-after-download check is manual and open
- [ ] 3 Vertical slice
- [ ] 4 Tasks
- [ ] 5 Versions / Releases / rollback
- [ ] 6 Scheduler
- [ ] 7 Browser
- [ ] 8 Harden to blueprint

## Decisions made here (21 Sep 2026)

1. Re-sequence: Builder and packaging evidence before infrastructure. End goal unchanged.
2. Dev-only Claude Code CLI Builder adapter, isolated and profile-gated, not part of the product.
3. Generated Apps stay Python. TS-based generated Apps (e.g. an agent-native-style runtime) are revisited only if step 1 fails on Python.
4. Borrow agent-native's pattern, not its dependency: one Entrypoint definition in the App SDK is projected to the trusted-fallback UI, an Assistant tool, the App UI Bridge, and later MCP.
5. arm64 first; x86_64, Windows CI, React/Vite generated Surface, OpenCode deferred.
6. The `alpha/` bundle is kept as-is (incomplete snapshot: manifest, readable/, visuals/, PDF, docx, zips missing). It is the spec, read directly; `agent_docs.py` is not used.
7. No Apple Developer account for now (founder decision). Builds are ad-hoc signed and run locally; testers use System Settings → Privacy & Security → Open Anyway once. Developer ID signing and notarization move to step 8, required only before distributing to people who can't be walked through that. Not an App Store product (unchanged from spec D-024).
8. Generated Apps are SDK-declared Entrypoint functions with no web framework; FastAPI/Uvicorn live in the platform `app-runtime` worker (founder-approved on EXP-BUILDER evidence). Applied to D-032, the release spec, blueprint, system/deployment architecture, roadmap, specs index, project index, and checklist.
