# Delivery Checklist

Status: Canonical working tracker
Last updated: 21 September 2026

## How to use this checklist

This is the single status source for product and implementation work. Every item has one state: `Done`, `Now`, `Next`, `Later`, or `Blocked`. Move an item rather than copying it between sections. A document, prototype, or test result is complete only when its evidence is linked or named here.

`Prototype_Scope_and_Acceptance.md` defines checkpoint scope and acceptance IDs. `AI_Coding_Agent_Playbook.md` defines agent procedure and evidence. `AGENTS.md` is the repository-root instruction handoff; `Prototype_First_Task.md` is the P0 starter packet. Their existence means planning is complete, not implementation. Repository task/evidence records link back here; they do not replace this tracker.

## Operating principles

- Keep user goals open-ended: no predefined workflow, industry, or website catalogue. Qualify execution capabilities and dependencies explicitly.
- Treat an App as reusable work with optional custom UI; preserve intent, rules, corrections, and evidence.
- Ship Mac first, keep shared logic portable, and exercise it on Windows early.
- Distinguish the manual internal v0.0 milestone from the usable local release, which includes schedules and browser automation.
- Use direct answers for explanation, Tasks for bounded one-off work, and Apps for reusable or ongoing capability.
- Generate real code, but support one managed App stack first.
- Select local or cloud deployment per App and keep the package portable.
- Make execution, persistence, external routes, permissions, cost, and failure understandable.
- Separate Task Runner authority, Builder authority, released-App authority, user approval, observed evidence, and Computer Action authority.
- Treat versions, Activity, repair, and rollback as product features.
- Prefer APIs, HTTP, and supported connectors before deterministic browser automation; browser automation before accessibility action; and accessibility action before visual computer use.
- Keep future seams where replacement would be expensive; do not implement future systems merely because they are envisioned.

## Done

- [x] Agree the horizontal product vision and long-term procedural second-brain direction.
- [x] Agree that the Assistant is the front door and the user does not choose an implementation object first.
- [x] Agree that direct answers, bounded one-off Tasks, and reusable Apps are distinct outcomes.
- [x] Define Task, Task Revision, Task Attempt, retry, evidence, and promotion lineage without creating a hidden App.
- [x] Keep accepted App Runs Release-bound while reserving a later shared execution kernel.
- [x] Select single-tenant execution for the first usable local App execution.
- [x] Agree per-App deployment: 'On this Mac' and 'Always available'.
- [x] Define local as local execution and persistence while permitting disclosed remote AI and API calls.
- [x] Define cloud as cloud execution and persistence with always-on scheduling and supported remote access.
- [x] Agree that real generated code runs locally; synthetic internal experiments may use the disclosed same-user boundary, while external local use requires qualified containment.
- [x] Defer live bidirectional local/cloud synchronization.
- [x] Include local scheduling and public/authenticated browser automation in the first usable release.
- [x] Confirm local work requires an awake Mac and available runtime.
- [x] Select visible missed occurrences with user-initiated retriggering and no automatic catch-up.
- [x] Keep automation and scheduling running after window close; distinguish explicit runtime quit and separate login startup.
- [x] Select Playwright/Chromium as the starting BrowserProvider, with dedicated sign-in profiles and human takeover.
- [x] Require extensible provider/capability boundaries and a later Windows host.
- [x] Keep cloud deployment, broad memory, observation, desktop action, and autonomy in explicit later phases.
- [x] Decouple local Workspace memory from cloud App deployment.
- [x] Reserve a governed Computer Action seam separate from screen observation and other capture.
- [x] Consolidate the product vision, roadmap, architecture, decisions, release scope, and market assessment.
- [x] Reconcile early notes against current architecture and decisions.
- [x] Reorganize specifications into contracts, examples, fixtures, and proofs.
- [x] Remove superseded reviews, duplicate design files, the active archive, and replaced assessments.
- [x] Retain the earlier 85-file review as dated evidence; apply the subsequent founder-approved scheduling/browser/extensibility/Windows revision and record its separate validation in `Reconciliation Report.md`.
- [x] Select Tauri 2 with React, TypeScript, and Vite for the Mac shell.
- [x] Define the trusted local boundary: narrow Rust native host, bundled Python platform service, and private mediated IPC.
- [x] Select the first generated-App profile: Python 3.13/FastAPI/Pydantic/Uvicorn with `uv`, plus optional React/TypeScript/Vite static UI built with Node.js LTS and pnpm.
- [x] Define the initial local workspace, separate Builder/App process groups, managed toolchains, and same-user trust limitation.
- [x] Select DeepSeek Harness as the first Builder candidate and OpenCode as the required benchmark adapter and fallback.
- [x] Select SQLite control and per-App Resource stores, a content-addressed Artifact area, and Keychain-backed secrets for the local profile.
- [x] Update the implementation blueprint with local scheduling ownership, a browser worker, adapted Windows CI, and explicit remaining contract/policy gates.
- [x] Define the prototype scope, P0-P7 checkpoint sequence, acceptance matrix, AI coding-agent playbook, root instruction file, and P0 handoff; no checkpoint implementation is claimed.
- [x] Confirm that the founder will manage AI-agent implementation outside this planning project, on a Mac; repository access is handled in that environment.
- [x] Define complete project-document access through `Agent_Document_Access.md` and the versioned `Alpha_Agent_Context.zip` handoff with indexed originals, text/visual companions, integrity checks and a refresh/change-proposal workflow.

## Now — implementation foundation

Handoff `Prototype_First_Task.md` and its referenced source contents to the founder's coding agent in the separate Mac environment. No P checkpoint is currently verified as implemented. The receiving agent inspects its repository and machine during P0; paid experiments additionally require model access and a spend limit. This planning project does not await a repository connection.

Follow dependencies rather than treating all uncertainty reduction as one serial chain. The internal v0.0 gate proves the Assistant/Task path and one deterministic App lifecycle. Short real-Builder, browser, containment, and packaging experiments may happen early. Full integrated qualification uses the proven lifecycle, and the first usable release also passes recurring/browser acceptance.

- [ ] In the separate Mac coding environment, install and verify the context bundle; inspect the provider-provided repository, applicable instructions, actual OS/architecture and available CI runners; record the input snapshot identity.
- [ ] Define and accept the Task and Task Attempt wire contract, schema, examples, invalid fixtures, and semantic tests.
- [ ] Define and accept one versioned `local-platform-protocol` bundle containing Core IPC, Host-control, and worker-bootstrap schemas, complete examples, invalid fixtures, and compatibility tests.
- [ ] Initialize the monorepo from the revised blueprint, with dependency boundaries, contract generation, Mac-native adapters, and shared Core/contract Windows CI.
- [ ] Move machine-readable accepted schemas, invalid fixtures, and proofs into the repository contract package; update the Library index to point to the tagged source rather than keep divergent copies.
- [ ] Prototype Assistant request disposition and the `Answer`, `Do once`, and `Make reusable` handoff.
- [ ] Implement the bounded local Task Runner with selected text/files, named model route, fixed tools, budgets, cancellation, Artifacts, and evidence.
- [ ] Implement the disposable registered parser-helper worker for every non-trivial PDF, office, archive, image, native-library, decompression, or conversion path; prove limits, cleanup, and malformed-output handling.
- [ ] Prototype durable direct answers, searchable Workspace history, Task detail, progress, result, retry, revision, deletion, and promotion states in the existing centre surface.
- [ ] Build the trusted-skeleton spike: Tauri/Rust host, bundled Python service, authenticated private IPC, durable test event, restart, cancellation, and crash recovery.
- [ ] Pin exact runtime-profile versions and artifact hashes after clean arm64 and x86_64 packaging tests.
- [ ] Package or securely install the managed CPython, `uv`, Node.js, and pnpm toolchains without prerequisites.
- [ ] Implement the per-App workspace layout, separate builder/parser-helper/App process groups, leases, environment allowlists, orphan reconciliation, lazy App-worker start/idle-stop, and cleanup.
- [ ] Replace the fake proof's toy manifest with a conforming package and pass the internal v0.0 lifecycle gate.
- [ ] Run early bounded real-generation/repair and containment feasibility experiments with non-sensitive fixtures.
- [ ] Implement DeepSeek Harness and OpenCode through the same interface; run P4 creation/correction/repair qualification, then complete recurring/public/authenticated browser scoring after P5 dependencies exist.
- [ ] Select and pin the default Builder adapter and initial model route only after the full P4/P5 benchmark evidence; retain all attempts, interventions and costs.
- [ ] Implement SQLite repositories, migrations, the minimal v0 App-scoped Table CRUD/filter/cursor and Artifact-backed file Resource profile, Artifact storage, and Keychain secret references.
- [ ] Implement structural and semantic validators for the current contracts.
- [ ] Implement finite Task, Build, Run, process, storage, output, network, model, retry, and cost budgets for the internal profile; retain exact usage evidence.
- [ ] Implement the existing qualified HTTP/API profile, usable by manual or scheduled Apps; retain its profile limits.
- [ ] Complete timezone/DST, overlap/offline behavior, retrigger payloads/lineage and Release/Input semantics, background controls, and separate login-start presentation before scheduler activation.
- [ ] Define scheduler schemas, occurrence/idempotency semantics, examples, invalid fixtures, and recovery tests.
- [ ] Implement durable local schedules, visible missed occurrences with manual retriggering and no automatic catch-up, pause/resume, and lazy dispatch through normal Run admission.
- [ ] Verify window-close continuation, reconnect without duplicate scheduler, explicit runtime quit, and accessible background controls.
- [ ] Verify missed occurrences survive wake/restart without automatic execution; later manual retrigger links to the missed occurrence, rechecks authority, and deduplicates repeated requests.
- [ ] Define BrowserProvider/Connection payloads, profile locks/sharing, takeover/resume, effect policy, evidence redaction, and invalid fixtures.
- [ ] Package a registered Playwright/Chromium browser worker with dedicated public/authenticated profiles and general operations.
- [ ] Prove public collection and authenticated browser workflows, including sign-in, MFA/expiry, changed pages, transfers, cancellation, and uncertain-effect recovery.
- [ ] Prove a recurring collection/structuring/storage/processing App across fresh runs and a plain-language correction.
- [ ] Test shared code and relevant browser behavior on Windows without claiming Windows-native release readiness.
- [ ] Implement one end-to-end local fixture: selected files to structured table and report.
- [ ] Implement one end-to-end one-off Task fixture: selected files to an evidence-backed saved report.
- [ ] Implement Build Brief, Build progress, the single React/Vite Surface path or trusted fallback, preview, access review, Local Release, Run, Activity, correction, Version comparison, and rollback.
- [ ] Implement bounded Build-plan approval, risk-scope re-approval, command visibility, cancellation, logs, process supervision, and health reporting.
- [ ] Keep durable secrets outside generated source and ordinary logs.
- [ ] Validate three materially different Apps without terminal intervention.
- [ ] Validate three materially different one-off Tasks without hidden App creation or ambient access.

## Next - external-test readiness and subsequent tracks

- [ ] Qualify local generated-code containment and protected browser sessions before the external local release.
- [ ] Encrypt local state and verify backup and restore.
- [ ] Sign, notarize, update, uninstall, and recover the Mac application safely.
- [ ] Expand beyond the v0 HTTP fixture to policy-qualified public-web retrieval, structured extraction, rate limits, and resilient multi-source research.
- [ ] Add scoped local folders and initial email, calendar, drive, and notification Connections.
- [ ] Add local user-approved Context and memory search without requiring Cloud App deployment.
- [ ] Add provenance, correction, revocation, export, deletion, and explicit cross-object grants for retained Context.
- [ ] Implement the `Always available` cloud target with tenancy, identity, secrets, scheduler, queue, workers, metering, export, and deletion when demand clears the cloud gate.
- [ ] Implement explicit local-to-cloud and cloud-to-local migration.
- [ ] Add supported remote clients for Cloud Apps.
- [ ] Implement and qualify windows-native IPC, process supervision/containment, credentials, paths, background lifecycle, browser/runtime installation, signing, updates, and recovery before Windows distribution.
- [ ] Calibrate production budgets and plan limits from measured Task, Build, and Run usage.
- [ ] Run recurring weekly user-research sessions with non-technical testers and track reuse, correction, trust, and retention.

## Later

- [ ] Add a Device Bridge only for proven cloud workflows that need scoped online Mac capabilities.
- [ ] Add on-demand screen context and push-to-talk voice.
- [ ] Add explicit watch-and-learn sessions and reviewable Procedure extraction.
- [ ] Compile confirmed Procedures into Workflows, Agents, or Apps.
- [ ] Add opt-in proactive suggestions, shadow mode, supervised execution, and only then bounded autonomy.
- [ ] Evaluate capable local models where quality, latency, hardware, and support burden are acceptable.
- [ ] Add scoped Computer Action through accessibility or application automation only after API, connector, and deterministic browser routes prove insufficient.
- [ ] Add visual computer use only after deterministic Computer Action and its trust controls are proven.

## Deferred unless evidence changes the priority

- [ ] Continuous ambient screen monitoring.
- [ ] Always-listening voice.
- [ ] Native mobile execution.
- [ ] Live active-active local/cloud synchronization.
- [ ] Arbitrary generated languages and frameworks.
- [ ] Public anonymous App hosting.
- [ ] Marketplace and third-party extension ecosystem.
- [ ] Enterprise regional placement and high-availability commitments.
- [ ] Autonomous high-impact actions.
- [ ] Blanket or indefinite desktop-control grants.

## Blocked decisions

These are blocked on short implementation spikes or product evidence, not on more speculative architecture:

| Decision | Evidence needed | Resolves |
|---|---|---|
| Coding-environment verification | External Mac implementation is confirmed; receiving agent records repository baseline, actual OS/architecture and available runners | P0 evidence and native qualification; no repository connection required here |
| Live experiment allowance | Approved model/provider access, external routes and explicit spend/attempt limits | Credentialed Builder/model experiments |
| Exact runtime-profile locks | Clean packaged Build, preview, Run, restart, and uninstall on supported Mac architectures | Patch versions and runtime artifacts |
| Default Builder and model | DeepSeek/OpenCode three-fixture scorecard covering quality, latency, cost, cancellation, resume, evidence, and cleanup | Initial construction route |
| Model onboarding | BYOK usability test and measured cost of limited product-funded credits | Credential and billing experience |
| External generated-code envelope | Local filesystem/network escape, browser-session separation, performance, package-size, and disclosure tests; remote execution is not an implicit local-mode fallback | Sensitive-data and broader external testing |
| External tester channel | Signing, update, diagnostics, consent, recovery, and support test | First distribution |
| Scheduler contract and lifecycle | Accepted manual-only recovery and window-close continuation; cadence/timezone/overlap/offline, retrigger lineage/Release/input semantics and lifecycle evidence | Schedule activation |
| Browser contracts and profile | Public/authenticated experiments, session locking/takeover, egress/effects, redaction, clean packaging | Browser activation |
| Windows native host | Shared CI plus later native IPC, credential, containment, installer and recovery evidence | Windows distribution |
| Cloud provider stack | Demonstrated always-on demand and measured workload shapes | Cloud availability track |

## Definition of done for the first usable local release

A non-technical tester can begin with the Assistant, complete, stop, reopen, inspect, retry, revise, and promote at least three materially different one-off Tasks. The same tester can request, preview, release, use, close, reopen, inspect, correct, and roll back at least three materially different Apps without a terminal. The App evidence includes recurring collection/processing, authenticated browser work with recovery, and an App without custom UI. Testers understand local availability, continued automation after window close, and visible missed jobs that they can manually retrigger without automatic catch-up. Shared Core/contract checks pass on Windows; this does not claim a released Windows host. Task history, App code, and operational data persist locally; every remote route and material permission is understandable; failures preserve useful evidence; and the shell recovers when Task execution, generated code, or generated UI fails.

## Update discipline

After each meaningful implementation or product decision:

1. update the affected canonical document;
2. move the checklist item to its new state;
3. add the verification evidence;
4. run relevant contract and stale-reference checks;
5. delete or replace superseded guidance rather than creating a parallel plan.
