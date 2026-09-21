# AI Coding Agent Playbook

Status: Development execution instructions for the local prototype
Revision: 1
Last updated: 21 September 2026

## Purpose

Enable AI coding agents to implement Alpha in small, inspectable increments with durable context and verifiable results. This playbook governs agents building the product. The product's own Builder harness has separate runtime authority under `../specifications/contracts/Builder Harness Interface.md`; development-agent access must never become generated-App authority.

Use `Prototype_Scope_and_Acceptance.md` for milestones and acceptance IDs, `../architecture/Implementation Blueprint.md` for boundaries and paths, and `Delivery Checklist.md` for project status. The root `AGENTS.md` is the concise executable entrypoint to this procedure, not a second architecture document.

## Where implementation happens

The founder manages implementation in a separate coding environment on a Mac. This project supplies specifications, task briefs and review; it does not need a repository connection to complete planning. Apply this playbook in the receiving repository with its actual instructions and permissions. Provide canonical source contents through the immutable input snapshot, and return checkpoint evidence or proposed document changes here for review as needed. Do not imply that a coding agent has access to this project's files or can update them automatically.

## Working rules

1. Implement one bounded task packet at a time. It must identify the checkpoint, user-visible outcome, dependencies, contract versions, allowed paths, forbidden scope, acceptance IDs, required commands and evidence.
2. Read the relevant current contracts and neighboring code before editing. Use repository search, not assumed filenames, interfaces or undocumented vendor behavior.
3. Preserve uncommitted user work and unrelated changes. Inspect branch/status/diff before work; use an isolated branch/worktree when appropriate. Never reset, delete or overwrite unrelated work to make a task easier.
4. Keep the architecture's ownership and authority boundaries intact. Generated code stays outside Core; trusted operations stay out of generated UI; secrets stay out of source, prompts, fixtures and ordinary logs.
5. Prefer a complete vertical slice over many disconnected placeholders. Do not create future modules, generic frameworks or empty scaffold files simply because a diagram names them.
6. Make uncertainty explicit. Stop the affected branch of work for an unanswered material product, authority, irreversible data or spending decision. Continue independent authorized work and present concrete options once the decision is necessary.
7. Ordinary reversible implementation choices within the accepted contract do not require repeated founder approval. A completed internal checkpoint can advance automatically within an already authorized milestone sequence.
8. Do not change requirements, assertions, fixture expectations or permissions merely to obtain a passing test. A contract defect gets a reasoned change proposal and regression evidence.
9. Use the pinned toolchains and committed locks. Do not silently upgrade dependencies, regenerate all locks, invent a provider API, or add a second framework. Check official version-matched documentation/source when an integration needs verification.
10. Report observed results. Never claim a command was run, an app was packaged, a Mac was tested, or a live provider worked without evidence from that action.

## Source authority and context delivery

The latest explicit founder decision takes precedence over older project prose. Existing system/developer instructions, access controls and applicable repository instructions still govern agent execution. The project index supplies document authority order; disagreements are recorded and repaired, not silently settled by whichever document is easiest to implement.

Agents need actual document contents, not links they cannot open. `Agent_Document_Access.md` defines the complete `Alpha_Agent_Context.zip` export, its index/manifest, local read/search/verify commands and refresh/change-proposal loop. This is a file-based snapshot, not automatic live access to this project. At repository initialization:

- Extract the complete context bundle under `docs/development/spec-inputs/<snapshot-id>/` and verify it with the supplied utility. Preserve all source paths and the manifest; load only relevant documents into each task context. Keep snapshots immutable by workflow and include their identity in task records.
- Record canonical source path, file/version identity when available, byte digest and retrieval time in an input manifest. The checkout records which snapshot is in use; filenames and timestamps alone are not freshness checks.
- This bundle is an immutable implementation input, not a second editable product specification. Never fix a canonical product decision by editing only the snapshot. Update the canonical source first, create a new snapshot and rerun affected checks.
- `AGENTS.md` is an operational repository instruction file. Amend it with the playbook when the execution procedure changes; it may not quietly widen product authority.
- Accepted machine-readable schemas/examples/invalid fixtures move to `packages/contracts/` with explicit source mapping. After cutover, the repository is their implementation source and the specification index points to the exact commit/tag. Old document copies are marked frozen; no two mutable schema authorities.
- If an agent cannot read the required snapshot or discover the actual contract version, it reports that blocker. It must not reconstruct requirements from memory or a task title.

Keep the task's input list focused. Load broader sources when an implementation question crosses their boundary. Do not make every agent reread all research archives; research is evidence, not an instruction source.

## Roles and coordination

Roles are responsibilities, not a requirement for a paid orchestration platform or a fixed number of agents. One agent can work sequentially. Distinct sessions can improve review independence when available.

| Role | Responsibility | Must not do |
|---|---|---|
| Coordinator | Select the next ready packet, identify dependencies and decisions, assign ownership, maintain evidence links and founder-facing status | Treat an author summary as test evidence or approve unresolved product choices |
| Implementer | Make the smallest complete change, add relevant checks, run available verification, provide a handoff | Declare its untested or unreviewed work independently verified |
| Reviewer | Read the packet, base-to-head diff, contracts and tests; challenge requirements, edge cases, authority and scope | Rewrite acceptance criteria to match the implementation or merely repeat its summary |
| Verifier | Reproduce required checks on the reported commit/environment, inspect outputs and compare independent expected results | Infer native or live-provider success from mocks |

Review and verification may be done by AI. Product validation ultimately requires observing actual users. A fresh review session receives the task packet, source snapshot, exact diff and evidence, not only the implementer's explanation. If independent review is unavailable, label the self-review honestly and leave the independent milestone review pending; never manufacture a second-agent endorsement.

Parallel work is optional and requires non-overlapping ownership and stable shared contracts. One writer owns each shared schema, migration sequence, lockfile or generated registry at a time. Use separate branches/worktrees, a named integration owner and explicit dependency commit references. A coordinator merges/integrates one change at a time and reruns affected checks against the combined result. Work cannot evade a blocked contract by implementing both sides privately in parallel.

## Mandatory task packet

Store bounded implementation tickets in `docs/development/tasks/`. They are work/evidence records, not a competing project roadmap. Reference their evidence from the canonical checklist.

```text
Task ID and checkpoint:
Outcome and non-goals:
```
Base commit / current branch:
Canonical input snapshot and relevant source versions:
Accepted decisions; open decisions blocking this task:
Dependencies and evidence that they passed:
Owned paths; shared files requiring coordination:
Contract versions and permitted changes:
Acceptance IDs and independent expected behavior:
Required checks and exact commands available at this baseline:
Target environments; checks that require Mac/Windows/live access:
Authorized external routes, credentials and budget reference:
Stop conditions and rollback/recovery approach:
Deliverables and evidence location:
```

A task should have one reviewable outcome. Split it if changes span unrelated lifecycles or cannot be checked independently. Avoid arbitrary line-count limits: reviewability and dependency coherence matter more than file size.

## Per-task execution loop

1. **Inspect.** Read root/nested instructions, status, diff, task inputs and current implementations. Confirm repository/machine identity and available permissions. Do not install or execute repo code before inspecting its setup instructions.
2. **Restate.** Give a short outcome, boundaries, acceptance checks and any blocking question. State which parts can proceed. Do not ask for permission already supplied.
3. **Establish baseline.** Run the relevant existing checks once where useful; distinguish pre-existing failures from regressions. A missing command is a missing command, not a pass.
4. **Define the observable contract.** For new state/authority/process behavior, write the smallest meaningful failing case or independent fixture expectation before the implementation. UI copy and other low-impact edits need appropriate inspection, not ceremonial tests.
5. **Implement.** Keep commits/patches scoped. Use real storage/process boundaries for integration work. Temporary doubles must be named, injectable, profile-gated and incapable of being mistaken for production providers.
6. **Verify.** Run targeted tests first, then the applicable task gate. Exercise a concrete failure path. Preserve failures and investigate; do not loop blindly until a flaky test turns green.
7. **Review.** Inspect the full diff, migrations, dependency/contract changes, error handling, logs and authority. Run fresh reviewer/verification sessions at checkpoint boundaries where available.
8. **Handoff.** Record exact changes, evidence, limitations and next dependencies. Update the canonical checklist if accessible; otherwise provide a precise status/evidence patch and label synchronization pending.

Do not continue an endless autonomous repair loop. A packet declares finite attempts/time/spend where relevant. At the limit, checkpoint work, retain evidence and report the blocker. Hardcoded success, swallowed exceptions, disabled tests or wider privileges are never acceptable escape routes.

## Checkpoint and review policy

Every P checkpoint produces one gate record tied to an exact commit and input snapshot. Passing requires all required cases, no unresolved blocking findings, and sufficient environment evidence. Map every acceptance ID due at that checkpoint to an actual test or retained observation; a missing ID makes the gate incomplete. Results use `pass`, `fail`, `blocked`, or `not run` as evidence labels; these do not replace the checklist's project states.

Blocking findings include broken advertised acceptance behavior, data loss/corruption, duplicate logical execution/effects, unauthorized access, secret leakage, inability to cancel/recover, changed contracts without migration/compatibility analysis, and missing required environment tests. Cosmetic findings can be tracked separately when they do not obstruct the journey.

The founder is needed for unresolved product meaning, materially changed trust/data scope, new spending beyond authorization, public release or other unapproved consequential actions. The founder is not a mandatory approver of every file, test, internal checkpoint, commit or routine repair. Existing session authorization governs any merge/push or external action; the playbook does not invent permission or revoke permission already given.

Agent-produced gate records are evidence and review conclusions. They are not proof of market demand, usability or operating-system security beyond the cases actually exercised.

## Testing and validation matrix

| Layer | Use actual components for | Test doubles are appropriate for | Required negative or recovery focus |
|---|---|---|---|
| Contract/domain | Exact schemas, semantic validators, state transitions and generated types | Clock/ID generation and bounded provider outcomes | Invalid fields/references, invalid transitions, terminal-state immutability, idempotency |
| Persistence | Temporary SQLite databases, migrations, CAS, Artifact filesystem | External services outside the transaction | Busy/conflict, interrupted commit/write, failed migration and unchanged data |
| Host/IPC/workers | Rust and Python processes, private transport, real descendants | Synthetic bounded worker behavior | Wrong identity/version, invalid launch, deadline/cancel/crash, orphan reconciliation |
| Task/Builder/model | Shared adapter contract plus separately authorized real provider runs | Deterministic model and conforming fake Builder for fast tests | Retry/revision lineage, denied authority, failed build/repair, retained usage/evidence |
| Browser | Actual Chromium and local controlled public/authenticated sites; explicit real-network qualification | Website errors, test identity and effect receipts controlled by fixture server | Expiry/takeover, redirects, denied destinations, profile isolation, uncertain submit and stop |
| Scheduler | Real ledger/admission integration and injected clock; actual Mac lifecycle for native checks | Clock advancement, network availability and deterministic jobs | Missed work without auto-catch-up, duplicate claim/retrigger, close/reopen, sleep/quit/restart |
| UI/Surface | Rendered trusted UI/Bridge, generated frame and actual event origins | Provider/read models for isolated component states | Wrong nonce/origin/source/method, denied native access, clear failed/blocked/missed states |
| Packaging/platform | Clean locked builds, actual packaged Mac, Windows shared suites | None for claiming the environment run | No hidden developer-runtime dependency, path/case issues, unsupported compatibility |
| End-user acceptance | Actual product and a non-implementer user at the external gate | Synthetic business data | No terminal/source intervention, recovery understanding, accurate privacy/availability expectations |

Do not require 100% line coverage or thousands of tests that mirror functions. Test user-observable invariants and costly failure modes. Use property/state-machine tests where they expose real sequences, and retain seeds. A log line saying "terminated" is not evidence that child processes are gone. A screenshot is not evidence of persisted data or successful external effects.

### Command contract

Implement the blueprint's `just` commands as their dependencies arrive. `just check` must not return success while required checks are placeholders or silently skipped. CI must declare which checkpoint capabilities exist so absent future components are reported as not yet implemented, not quietly counted as passing.

| Command | Purpose and scope |
|---|---|
| `just bootstrap` | Verify/install approved repository-local tools from pinned sources; document prerequisites and network use |
| `just generate` | Generate types/registries; a second generation produces no diff |
| `just dev` | Start the trusted development topology with explicit fixture/internal policy |
| `just test` | Deterministic default suite, isolated from paid/live external services |
| `just check` | Applicable formatting, lint/types, contracts, boundaries, tests and builds across implemented workspaces |
| `just test-integration` | Real storage, IPC, process and recovery suites; declared OS requirements |
| `just qualify-builders` | Explicit credentialed comparison with declared cost/attempt caps; never hidden in default checks |
| `just package-mac` | Locked package for the declared Mac architecture |
| `just verify-package` | Inventory/hash/launch/recovery checks; signing checks report unavailable/not run until configured |

Browser and scheduler tests join the existing suite interfaces as implemented. New command names require a documented need; do not create a parallel suite that bypasses `just check`.

### Continuous integration

Start with contract generation/fixtures, source formatting/types, dependency boundaries and safe fast tests. Add real SQLite/Artifact, IPC/worker, parser, UI/Bridge, browser and scheduler gates with the corresponding slice. Shared Core/contracts/path tests run on Windows from the initial repository; native Mac jobs execute on an actual Mac runner. A Linux-only environment cannot mark native gates passed.

Use locked dependencies and isolated temporary state. Default PR checks use local fixtures with no user keys or paid model calls. Live qualification is an explicit job with secrets supplied through the approved environment and bounded spending; forks/untrusted changes must not receive credentials automatically. Preserve sanitized failure evidence and enough metadata to reproduce it.

Full packaged/architecture/recovery checks run at relevant checkpoints or release candidates, not on every copy edit. After sufficient verification, stop optional testing and move to the next authorized outcome.

## Evidence and handoff format

Small sanitized machine-readable results and summaries belong under `docs/development/evidence/<task-id>/`; bulky recordings/build logs may be CI artifacts with durable identity, digest and retention recorded in the gate summary. Evidence needed for a milestone must survive an expiring chat/session. Never commit credentials, raw production browser state or selected personal files.

```text
Task/checkpoint; base and final commit:
Outcome and changed paths:
Input snapshot / contract and fixture versions:
Environment and runtime inventory:
Checks: exact command, exit code, test IDs, pass/fail/blocked/not-run:
Artifact/evidence locations and digests:
Independent expected result versus observed result:
Failures, skips, limitations and unresolved decisions:
Reviewer findings and resolution; verification independence:
Remaining risk and rollback/recovery instructions:
Canonical checklist update or pending synchronization patch:
Next ready task and dependency evidence:
```

The agent's final message to the founder is short: what changed, what passed, what remains blocked, and the next decision if any. Detailed evidence remains linked. Preserve context in these records before session handoff; conversation memory is not the project ledger.

## Change control without unnecessary bureaucracy

- **Routine implementation:** agent decides within the accepted task, tests it, records it and proceeds.
- **Contract change:** identify consumers, compatibility, migrations, fixture updates and authority implications before implementing; get the required product decision only where behavior is unresolved or scope changes.
- **Architecture change:** present the failed assumption, observed evidence, minimal alternative and effect on Mac/Windows/portability. Do not silently replace a selected framework or move domain truth into a vendor harness.
- **Acceptance change:** keep the original failure, explain the incorrect expectation and obtain a decision if the product promise changes. The implementer cannot weaken the evaluation to hide a defect.
- **Environment blocker:** report the exact missing access/tool/machine and checks blocked; finish portable or read-only work where possible. Never fabricate a result or silently switch execution location.

## Initial handoff

Use `Prototype_First_Task.md`. Repository initialization and contract completion are the first work packet; live experiments wait for their environment, credentials and spending authority. This playbook creates no automatic jobs and grants no external-service access by itself.
