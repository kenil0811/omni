# Alpha — agent instructions

Read `docs/PLAN.md` first. It says what we are doing now and why. The `alpha/` directory is the specification: `alpha/00 Project Index.md` gives the authority order; `alpha/architecture/Implementation Blueprint.md` is the target shape. Read the spec sections relevant to your step before editing. Do not reconstruct requirements from memory.

## Before editing

- Check `git status`, the current branch, and the current step in `docs/PLAN.md`. Preserve unrelated work.
- Read neighboring code and the relevant spec/contract. Search; do not assume filenames.
- If a needed input, decision, or credential is missing, say exactly what is missing and continue with what does not depend on it. Do not invent defaults for product behavior, budgets, or authority.

## Build rules

- One bounded step with an observable outcome. No speculative modules, empty scaffolding, or catch-all `utils.py`.
- Keep the accepted stack: Tauri 2 + React/TS shell, bundled Python core, Python/FastAPI generated Apps, SQLite/Artifacts/Keychain. Do not swap it without evidence and a note in `docs/PLAN.md`.
- Generated code stays outside Core. Generated UI gets no native privileges. Secrets, database paths, and browser session material never enter generated packages, fixtures, or logs.
- Versions are immutable; rollback moves a Release pointer; code rollback never implies data rollback. Tasks never become hidden Apps.
- Missed scheduled jobs stay visible for manual retrigger; never auto catch up. Window close keeps automation running; explicit quit stops it.
- Builders are reached only through `BuilderHarness`. The Claude Code CLI adapter is dev-only and profile-gated; it is never bundled or offered to users.
- Unknown authority fields fail closed. Do not hand-edit generated contract types.

## Verification

- Use real SQLite / processes / browsers for integration claims; deterministic fakes for isolated units.
- Never weaken an assertion, disable a check, hardcode a fixture answer, swallow an error, or widen authority to get green. Preserve failing cases and report them.
- Never claim a command ran, a package built, or a test passed without its output. Missing tools and skipped tests are "not run," not "pass."
- No paid or credentialed calls in default checks.

## Finish

- Record what changed, what was verified (exact commands + results), what is blocked, and the next step in the relevant `docs/tasks/<id>.md`; tick `docs/PLAN.md`.
- Do not push, publish, or spend without being asked.
- Final message: what changed, what passed, what is blocked, what decision (if any) is needed. Do not claim more than the evidence shows.
