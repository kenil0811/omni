# Current Release Specification

Status: Canonical implementation scope
Last updated: 21 September 2026

## Release objective

Deliver a Mac application in which a non-technical user starts with one Assistant, can receive a direct answer, execute a bounded one-off Task from text and selected files, or create a reusable App. The user can inspect every execution, and can turn proven Task intent into an App Build without starting over.

For the App path, the user can receive a working local preview generated as real code, release and operate it, inspect its Activity, correct it, and roll back safely.

This specification governs the first usable local release. The internal v0.0 manual lifecycle is a smaller engineering milestone. External distribution requires the additional readiness gates in `../product/Roadmap and Scope.md`. `Local_Automation_and_Platform_Extension_Profile.md` defines the current scheduling, browser, and Mac/Windows requirements, including unresolved policy choices.

## Prototype delivery

`../delivery/Prototype_Scope_and_Acceptance.md` defines the P0-P7 implementation checkpoints, fixture journeys and acceptance IDs for this scope. P0-P3 prove the internal deterministic lifecycle; P4-P6 prove integrated local behavior with real providers; P7 adds the external-test gate. Passing the smaller milestones does not remove any requirement from this release.

## Included

- Workspace shell and Assistant as the primary entry point, with scoped Task, Builder, correction, and diagnosis roles.
- Request disposition to direct answer, `Do once`, or `Make reusable`.
- First-class Task, immutable Task Revision, Task Attempt, outputs, evidence, and promotion lineage.
- One platform-owned local Task execution profile for typed text and deliberately selected files.
- Fixed task tools for bounded read, transform, analysis, and Output-Artifact creation.
- One supported generated-App stack.
- Tauri 2 Mac host with a React/TypeScript/Vite trusted shell and a bundled Python platform service.
- Dedicated local workspace and dependency environment per App.
- Text intent and deliberately selected file inputs.
- Real generated code, dependency installation, Build commands, tests, and preview.
- Local App code, Resource data, files, configuration, secrets, Runs, logs, and evidence.
- Remote Builder and runtime model routes.
- Manual action, query, and Job Entrypoints, plus locally scheduled Job Entrypoints.
- Local scheduler residency and availability reporting while the Mac is awake and the approved runtime is running.
- General browser navigation, extraction, clicks, forms, selected uploads, downloads, and approved effects through Playwright/Chromium behind a BrowserProvider.
- Dedicated public/authenticated automation profiles, protected Connection bindings, user sign-in/takeover, and session-expiry recovery.
- Platform-neutral Core/contracts with Mac-native adapters and shared Windows CI; Windows distribution comes later.
- Minimal App-scoped table create/get/list/update/delete with optimistic revisions, declared exact filters and stable cursors, plus Artifact-backed file-store Resources.
- The existing bounded allowlisted HTTP/API profile, usable by manual or scheduled Apps where qualified; broader web work can use the general browser provider without a site-specific connector.
- One isolated React/TypeScript/Vite micro-frontend Surface profile, plus a trusted fallback for Apps with no custom Surface.
- Build, immutable Version, local Release, Run, Activity, correction, and rollback.
- Plain-language access and deployment review.

## Not included in the first usable release

- Windows-native distribution before its separate qualification;
- operating-system accessibility automation or visual desktop control;
- cloud deployment;
- authenticated public webhook ingress;
- live local/cloud synchronization;
- screen or voice input;
- shared memory, watch-and-learn, memory promotion, or Procedure compilation;
- arbitrary programming stacks;
- public or anonymous Apps;
- unsupported high-impact actions;
- aggregation, relationship expansion, Resource Transaction Domains, general Resource migrations, shared Context/memory SDK access, and generic authenticated/write HTTP.

## Task execution profile

The first Task profile is not a generated App runtime. It must define:

- exact platform Task Runner and tool versions;
- supported input media types, sizes, counts, and classification ceiling;
- named model/provider routes and required disclosure;
- fixed read, transform, analysis, and output tools;
- output Artifact types and safe destination rules;
- time, token, storage, and cost ceilings;
- cancellation, timeout, retry, and failure semantics;
- event, evidence, redaction, retention, and deletion behavior.

The profile rejects schedules, browser or desktop control, ambient filesystem reads, arbitrary generated-code or shell execution, Connections, external writes, and automatic memory promotion. A request requiring those capabilities must be routed to the App path or reported as unsupported in this release.

## Runtime profile

The prototype supports one runtime-profile family:

- backend: Python 3.13, FastAPI, Pydantic 2, and Uvicorn;
- Python dependency management: `uv` with committed `uv.lock`;
- optional custom interface: React, TypeScript, and Vite compiled to static assets;
- frontend dependency management: qualified Node.js LTS and pnpm with committed `pnpm-lock.yaml`;
- integration: the versioned platform SDK, App UI Bridge, and platform component kit;
- validation: manifest and semantic validation, dependency-lock validation, Ruff, Pytest, frontend typecheck, Vitest where applicable, Build, and smoke test;
- production: a supervised Python App worker plus optional static interface assets and separately managed browser workers; Node is not a generated App server dependency;
- browser: jointly pinned Playwright driver and Chromium artifacts, qualified for installation, launch, session protection, recovery, and bounded resource use;
- health: platform-defined startup, heartbeat, readiness, shutdown, and process-exit signals;
- authority: an allowlisted environment and logical Resource, Artifact, Connection, model, and Capability handles only;
- target: qualified arm64 and x86_64 macOS packages, with exact toolchain artifacts pinned by digest;
- budgets: finite Build and Run time, storage, process, output, model, and network limits recorded in the runtime-profile revision.

The Mac product uses Tauri 2 and a React/TypeScript/Vite trusted shell. A small Rust host owns native access and mediates a bundled Python 3.13 platform service over private local IPC. Builder workers and released App workers are separate supervised process groups; generated interfaces receive no Tauri commands or direct platform-service connection.

Exact patch versions, commands, dependency allowlists, templates, and numeric budgets live in a versioned runtime-profile lock in the implementation repository. They are finalized by the first clean packaging spike rather than copied into multiple product documents.

The portable App Contract remains capable of describing Python, TypeScript, declarative, native-view, and micro-frontend components. The v0 runtime profile accepts only the Python backend profile and the React/TypeScript/Vite micro-frontend Surface path; it rejects native-view declarations and all other inactive combinations with a clear compatibility result. Apps without a custom Surface use the trusted platform fallback.

## Builder profile

The first real Builder adapter implemented is DeepSeek Harness. OpenCode is the mandatory second-adapter comparator and fallback. Both execute through `contracts/Builder Harness Interface.md`; neither may become a package dependency, Release authority, or source of canonical Build state.

Before selecting the default, the adapters must build, modify, interrupt/resume, and repair the same three fixture families: selected-file processing/reporting, a tracker/dashboard, and recurring web collection with structured persistence through qualified HTTP/browser routes. Public and authenticated browser cases must be exercised. Bounded real-generation feasibility may start before the complete fake lifecycle; integrated release qualification still requires it. Selection is based on completion without terminal intervention, repair success, checkpoint recovery, evidence quality, latency, model and compute cost, process cleanup, and adherence to the workspace and output boundary.

The initial DeepSeek profile disables harness-native browser use, computer use, Code Mode, autonomous subagents, and unapproved third-party plugins. This does not disable the platform BrowserProvider used by released Apps. Synthetic browser validation must use a separately authorized platform test route rather than production credentials in the Builder workspace. The exact Harness and model versions are pinned only after this qualification; the earlier `0.1.5rc1` adapter proof is interface evidence, not the production version selection.

## Local App workspace

Every App has a managed directory containing source, dependencies, generated assets, temporary files, and technical logs. Durable App data and secret material are stored through platform-owned Resource and Connection adapters rather than embedded in source.

The Builder may edit the App workspace and run commands covered by a user-approved bounded Build plan and command policy. Ordinary commands inside that envelope remain visible, cancellable, and attributable without repeated prompts. The product asks again when a command introduces a new executable family, network destination, external file scope, credential, privilege boundary, or materially higher risk. A released App starts with narrower resolved configuration. The product manages runtime installation, dependencies, ports, process lifecycle, health, and cleanup.

## Required Task lifecycle

1. Accept the request through the Workspace Assistant.
2. Choose direct answer, `Do once`, or `Make reusable`; ask only when the choice changes material consequences. A direct answer remains a durable searchable Assistant Turn and may be cited or saved as an Artifact without becoming a Task.
3. For `Do once`, create a Task and immutable Task Revision containing confirmed intent, exact selected inputs, constraints, output expectation, classification, and provenance.
4. Resolve the Task execution snapshot: profile version, local placement, model route, fixed tools, policy, authority, budgets, and retention.
5. Create and execute one Task Attempt.
6. Record ordered state, human-input waits, outputs, evidence, usage, cost, errors, and terminal outcome.
7. Reopen the Task with history intact.
8. Retry through a new Attempt or change instructions or inputs through a new Task Revision.
9. Create a Build Brief from the chosen revision and Attempt evidence when the user selects `Make reusable`; transfer no Task authority.

## Required App lifecycle

1. Create App intent.
2. Maintain an editable Build Brief.
3. Create or resume a Build.
4. Generate code and package assets.
5. Validate contracts and dependency locks.
6. Run required formatting, type, unit, and smoke checks.
7. Launch a preview Release.
8. Review access and deployment.
9. Seal an immutable App Version.
10. Activate an `On this Mac` Release.
11. Invoke a manual Run or activate a reviewed local schedule and admit its due occurrence through the normal Run path.
12. Record output, evidence, logs, duration, cost, and terminal state.
13. Create a correction Build and candidate Version.
14. Compare and release or reject the candidate.
15. Roll back through a new Release pointer.

## Deployment resolution

The first Task execution snapshot uses:

```json
{
    "executionLocation": "device",
    "persistentStateLocation": "device",
    "executionProfile": "platform-task-runner",
    "availability": "while-device-runtime-available"
}
```

A named remote model binding may coexist with this local snapshot. It does not change Task-history or output persistence placement.

The first active Release uses:

```json
{
    "target": "local",
    "persistentStateLocation": "device",
    "defaultExecutionLocation": "device",
    "scheduleAuthority": "device",
    "availability": "while-device-runtime-available"
}
```

Remote model and API service bindings are compatible with this local profile. They do not change the location of persistent product state.

## Authority requirements

- Builder access is scoped to the App workspace plus deliberately selected input.
- Task Runner access is scoped to the exact Task Revision, deliberately selected inputs, model route, fixed platform tools, output policy, and finite budgets.
- Non-trivial document, archive, image, and native-library parsing runs through the registered resource-bounded parser-helper worker; only bounded plain-text and JSON reads occur inside Core.
- Task promotion creates a new Build and authority review; it carries provenance, not permissions.
- Publication requires a valid candidate Version and trusted user action.
- Released code receives only declared configuration, logical Resources, Connection references, model route, and Capabilities.
- Generated UI uses the App UI Bridge.
- Durable secrets never appear in packages, prompts by default, ordinary logs, fixtures, or exports.
- File access outside the App workspace requires trusted selection or a persisted scoped grant.
- External effects use Capability policy, approval where required, idempotency, and receipts.

## Required execution states

Task Attempt states are:

- `queued`
- `running`
- `awaiting-approval`
- `awaiting-input`
- `succeeded`
- `failed`
- `cancelled`
- `timed-out`

App Run states, as defined by the accepted Run Event Kernel, are:

- `queued`
- `running`
- `awaiting-approval`
- `awaiting-input`
- `succeeded`
- `failed`
- `cancelled`
- `timed-out`

The implementation may expose friendlier labels such as `Completed`. State transitions and terminal outcome remain durable and reconstructable. `Interrupted` or `uncertain` may describe a recovery condition but are not accepted terminal Run states in revision 3 of the Run Event Kernel.

## Required user-facing surfaces

- Workspace start, Assistant request composer, recent work, searchable Workspace history for durable Assistant Turns, Tasks, and Apps, and the App browser.
- Task detail, progress, result, output Artifacts, evidence, retry, revision, deletion, and `Make reusable`.
- New App and Build Brief.
- Build progress and technical details.
- Preview.
- App.
- Manage: Access, Configuration, local schedule controls, browser Connections, Versions, Delete.
- Runtime availability, next/last/missed schedule occurrence, login or approval needed, browser takeover, and resume/stop states.
- Activity and Run detail.
- Correction and Version comparison.
- Trusted Build-plan/command, file, Connection, approval, Release, rollback, and deletion flows. Approval review names the exact action, account or principal, destination or recipient, data leaving the device, scope and frequency, reversibility, cost or limit, and next effect.

## Acceptance tests

### Breadth

- Complete a selected-file comparison or synthesis Task and produce a saved report.
- Complete a materially different text-and-file extraction Task.
- Route a request that needs repetition or mutable state into the App lifecycle rather than stretching the Task profile.
- Build a local file-processing App.
- Build a tracker/dashboard App.
- Build a recurring collection App: approved public sources to browser/HTTP retrieval, structured deduplicated storage, custom processing, results, a later local scheduled run, and correction.
- Build an authenticated browser App with user sign-in, scoped operations, protected session state, and takeover after expiry/MFA.
- Demonstrate useful operation without a custom UI as well as an interactive App.
- Treat these examples as breadth tests; do not add a workflow or website allowlist to product intent.
- Attempt one unfamiliar request and report unsupported capability honestly.

### Lifecycle

- Restart the Mac product and reopen Task intent, Attempt history, outputs, and evidence.
- Cancel a Task Attempt and retry it as a new Attempt.
- Change Task instructions or selected inputs and create a new Task Revision.
- Promote a completed Task into a Build Brief without carrying its grants or hiding the source lineage.
- Delete a Task and its retained copies and outputs without deleting deliberately selected source files outside platform storage.
- Restart the Mac product and reopen the App with state intact.
- Cancel and resume or restart a Build safely.
- Fail a dependency installation and diagnose it.
- Crash generated UI without losing shell recovery.
- Crash an App process and show clear health and logs.
- Correct behavior through a new Version.
- Roll back to a previous Version.
- Delete the App and clean its owned state without deleting shared Connections or source files.

### Trust

- Confirm that a Task receives only the selected inputs, named model route, fixed tools, output location, and budgets in its snapshot.
- Reject Task access to ambient files, shell execution, browser or desktop control, Connections, external writes, and automatic memory promotion.
- Prevent generated UI from accessing native or storage interfaces directly.
- Confirm selected files are the only external local files supplied.
- Confirm durable secrets are absent from packages and logs.
- Show remote model/API route before first material use.
- Reject a Capability outside the Release binding.
- Recheck browser account, destination, grants, and effect approval after takeover or resume.
- Qualify local generated-code containment and browser-session protection before real sensitive data or credentials are used externally.

### Portability

- Persist a Task independently of any App, Version, or Release identity.
- Validate that promotion creates a Build lineage edge rather than converting the Task into an App.
- Validate Source and Resolved Manifests and package index.
- Produce a Release Resolution Record with the required deployment fields.
- Export the App package without operational data or credentials.
- Demonstrate that deployment-specific paths and provider identities exist only in Release bindings.
- Run shared Core/contract/path tests on Windows; isolate Mac-native imports and qualify browser behavior on both platforms as the provider is implemented.
- Declare incompatible OS-dependent dependencies/capabilities rather than claiming every App is automatically portable.

### Scheduling, browser, and extension readiness

Follow `Local_Automation_and_Platform_Extension_Profile.md`. Complete typed scheduler and browser-provider schemas, registry entries, examples, invalid fixtures, and semantic tests before enabling those capabilities. Existing generic App/Release/Capability shapes remain valid; prose does not silently add wire fields or declare new payloads executable.

Missed jobs remain visible with intended time and reason and can be retriggered whenever the user chooses, subject to current authority and availability. No missed work executes automatically on wake, reconnect, or restart. Closing the main window keeps active automation and the scheduler running; reopening reconnects to the existing runtime, while explicit runtime quit stops local execution. Complete timezone/DST, overlap/offline, retrigger payload/lineage and Release/input semantics, numeric limits, background-control/login-start presentation, browser session sharing/locking, exact runtime versions, and local containment before their affected activation gates.

Schedule recovery must cover sleep, wake, network loss, quit, restart, paused/revoked schedules, duplicate dispatch, approval waits, and uncertain external effects. No cloud execution, device wake, or automatic missed-run catch-up is implied; manual retriggering must preserve missed-occurrence history and deduplicate repeated requests.

## Contract set

The implementation uses the current versions listed in `Specifications Index.md`, including:

- App Contract revision 5;
- Package Layout revision 3;
- Resolved App Manifest revision 4;
- Release Resolution Record revision 5;
- Capability Protocol revision 6;
- Run Event Kernel revision 3;
- App UI Bridge revision 3;
- Builder Harness Interface v0.1;
- HTTP Action Profile revision 2.

The Task and Task Attempt contract is the immediate missing product execution contract. It must be defined, schematized, fixture-tested, and accepted before the one-off execution slice is implementation-ready. It extends or profiles protected-operation and evidence behavior explicitly; it must not manufacture App, Release, or Run identifiers to reuse the accepted App contracts.

One versioned `local-platform-protocol` bundle containing Core IPC, Host-control, and worker-bootstrap schemas, complete examples, invalid fixtures, and compatibility tests is also an immediate pre-code internal contract. Its parts ship atomically in v0. It defines implementation transport and launch authority; it does not become a portable App contract or alter the Task/App product model.

Schemas define structural validation. Semantic validators and contract tests remain required implementation deliverables; example files alone are not evidence that all semantic rules execute.
