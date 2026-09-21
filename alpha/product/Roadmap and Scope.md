# Roadmap and Scope

Status: Canonical
Last updated: 21 September 2026

## Delivery rule

Build the smallest complete user loop, validate it with real users, and widen the capability envelope only when the preceding dependency is usable and supportable. The product remains horizontal; the roadmap limits implementation scope rather than user intent.

The first usable local release includes schedules and browser automation. After that release, broader automation, memory, Windows delivery, and cloud availability are separate evidence-gated tracks. Cloud is not a prerequisite for useful local memory, and memory is not a prerequisite for cloud deployment. Observation and desktop action still require their own later trust gates.

The concrete execution sequence is in `../delivery/Prototype_Scope_and_Acceptance.md`, with agent procedure in `../delivery/AI_Coding_Agent_Playbook.md` and current status only in `../delivery/Delivery Checklist.md`. Those checkpoints refine this roadmap rather than creating a parallel product plan.

## Now — Phase 0: corpus and implementation foundation

- Maintain one canonical product vision, architecture, decision register, release specification, and delivery checklist.
- Prove the selected Tauri 2, Rust-host, Bundled-Python-service, and private-IPC boundary with a packaged Mac spike.
- Pin the selected Python (SDK Entrypoints, hosted by the platform App runtime) and React/Vite generated-App profile through one clean Build, preview, Run, restart, and cleanup cycle.
- Preserve the DeepSeek Harness and OpenCode adapter boundary; run bounded real-generation/repair and local-containment feasibility spikes early. Full integrated qualification still follows a working lifecycle.
- Define local scheduler semantics and the platform BrowserProvider contract. Implement the accepted policy: show missed jobs for user-initiated retriggering without automatic catch-up, and keep automation running after window close.
- Isolate Mac-native services behind interfaces and establish shared Core/contract Windows CI.
- Define the Assistant request-disposition model and the Task, Task Revision, and Task Attempt contract.
- Keep the App package independent of local or cloud providers.
- Establish Task execution, Build, validation, Release, Run, logging, versioning, and rollback contracts.
- Implement contract validation and reproducible test fixtures.

Exit condition: the repository and documentation identify one implementable thin slice with no contradictory deployment, execution, or product claims.

### Internal v0.0 evidence gate

For deterministic lifecycle integration, prove one sequence: Assistant disposition; direct answer or selected-file Task; durable Revision, Attempt, result, retry, reopen, and promotion; then a deterministic fake Builder producing one known App through one Version, local Release, manual Run, minimal table/file Resource, single React/Vite Surface path or trusted fallback, correction, and rollback. Complex file formats use the parser-helper boundary from the first Task slice. This gate is an internal milestone. It does not delay bounded real-Builder, browser, packaging, or containment feasibility experiments, and it does not substitute for first-release recurring/browser acceptance.

## Now — Phase 1: local working prototype

The first user-facing release is a Mac application in which the Assistant is the front door. It can:

- accept a plain-language request without requiring the user to choose an App or workflow type;
- answer directly when no execution is needed;
- perform a limited one-off Task from typed text and deliberately selected files through a platform-owned local Task Runner;
- preserve Task instructions, input references, attempts, outputs, Artifacts, evidence, costs, and failures;
- let the user turn a successful Task into an App Build without losing its lineage;
- accept a plain-language App request and deliberately attached files;
- clarify material uncertainty and maintain an editable Build Brief;
- generate real code using one supported application stack;
- create a dedicated local workspace and dependency environment per App;
- build, validate, preview, release, start, stop, and repair the App;
- persist App code, data, configuration, secrets, Runs, logs, and evidence locally;
- provide a generated interface where useful, or trusted configuration/results/Activity for Apps without custom UI;
- use one generated React/Vite Surface profile or the trusted No-Surface fallback, not a second native-view DSL;
- lazy-start App workers for active Runs or Surfaces and stop them after the bounded idle policy;
- support manual and scheduled local Runs, file input, App storage, remote model calls, and the qualified HTTP/API route;
- support general public and authenticated browser work through a platform-owned Playwright/Chromium provider, dedicated user-connected profiles, human takeover, and governed actions;
- show schedule availability, missed occurrences, login/action needed, results, and recovery;
- keep portable Core/product logic independent of Mac-native implementations and run shared checks on Windows;
- show access, execution location, failures, technical logs, Versions, and rollback;
- prevent generated UI from receiving ambient native or credential access.

The v0 Task Runner can analyze, transform, extract, and create bounded output Artifacts. Non-trivial document, archive, image, native-library, decompression, and conversion work executes in a disposable resource-limited parser helper rather than the trusted Core. The Task Runner cannot schedule work, control a browser or desktop, use ambient files, perform consequential external writes, create durable memory automatically, or run arbitrary generated code. Those limits apply to Tasks even though a released App may use the separately reviewed capabilities included in its Release.

The internal v0.0 milestone does not require scheduling or browser operation. The first usable release does require both, as specified by `../specifications/Local_Automation_and_Platform_Extension_Profile.md`. Desktop control, cloud deployment, screen capture, voice, and general memory remain outside this release.

Exit condition: non-technical testers can complete materially different Tasks and create, operate, correct, reopen, and recover materially different Apps without a terminal, including a recurring collection/processing App and an authenticated browser App. Users understand local runtime availability, continued automation after window close, and visible missed jobs with manual retriggering and no automatic catch-up. External testing passes local containment, credential, encryption, recovery, and distribution gates.

## Next — Track A: useful local automation and action adapters

- Extend the already-shipped local scheduler and browser provider based on observed workflows and reliability.
- Expand qualified HTTP profiles, public-web retrieval, extraction, and service integrations as needed; new websites are not required to have a dedicated connector.
- Add email, calendar, cloud-drive, and notification Connections where general browser/API routes are insufficient or less reliable.
- Extend scoped local folder and file capabilities, browser recovery, and evidence handling.
- Introduce governed Computer Action only for proven jobs that need operating-system accessibility or application automation; visual desktop control remains later.

APIs and qualified HTTP routes are preferred when suitable. Deterministic browser automation is already part of the first usable release. Site access and technical eligibility remain explicit.

Exit condition: new, materially different workflows use extension interfaces without domain-specific changes to the App lifecycle core.

## Next — Track B: local context and memory

- User-approved Workspace preferences, instructions, and durable context stored locally by default.
- Search across approved Task results, App data, Artifacts, and Activity.
- Explicit cross-App and cross-Task context grants.
- Evidence-backed Memory claims with provenance, correction, revocation, export, and deletion.
- Assistant use of exact Context snapshots without silently widening access.
- Repeated-work hypotheses and Procedure history only after basic memory is understandable.

Remote inference may help derive or retrieve memory when disclosed, but it does not become the durable memory authority. Cloud deployment of an App is neither required for nor equivalent to Workspace memory.

Exit condition: approved local context demonstrably reduces repeated explanation, and users can inspect, correct, exclude, and delete what is retained.

## Next — Track C: Always available deployment

- Cloud deployment target selected per App.
- Cloud-authoritative state, secrets, logs, and Run history.
- Managed scheduler, queue, and ephemeral workers.
- Isolated cloud execution for generated code and browser jobs.
- Responsive remote access to cloud Apps.
- Explicit local-to-cloud deployment or migration flow.
- Usage limits, metering, retention, export, and deletion.
- Compatibility checks for device-dependent Resources and Capabilities.

Do not allocate one permanent server or VM per App by default. Apps are packages, state, interfaces, triggers, and jobs; workers exist when work is active.

Exit condition: eligible Apps remain useful with the Mac offline and are accessible from another device without creating a second product model.

## Next — Track D: Windows delivery

- Keep Core, contracts, scheduling, App definitions, and browser-provider interfaces shared from the Mac implementation.
- Run the platform-neutral test suite on Windows early.
- Implement and qualify Windows-native IPC, process supervision and containment, credential storage, data paths, background lifecycle, and file access.
- Qualify Windows runtime/browser bundles, installer, signing, updates, accessibility, and recovery before claiming Windows support.
- Report platform-specific App dependencies or capabilities explicitly; a shared package never carries credentials or access grants between devices.

Exit condition: the same representative Apps run through a qualified Windows host without changing their portable business logic.

## Later — contextual inputs, procedure learning, and bounded autonomy

- On-demand screen context.
- Push-to-talk voice.
- Explicit watch-and-learn sessions.
- Reviewable Procedure extraction.
- Guide and shadow modes.
- Compilation of confirmed Procedures into checklists, Workflows, Agents, or Apps.
- Supervised Procedure execution may use an already-qualified Computer Action capability, but observation or Procedure inference never supplies its authority.
- Opt-in proactive suggestions and bounded autonomy.
- Increasing use of capable local models where quality is sufficient.

Every new collection or autonomy boundary requires a fresh value, privacy, usability, and security review.

## Deferred until evidence justifies them

- continuous ambient monitoring;
- always-listening voice;
- native mobile execution;
- live active-active local/cloud synchronization;
- unrestricted App-to-App access;
- arbitrary generated technology stacks;
- public anonymous application hosting;
- marketplace and third-party extension ecosystem;
- enterprise collaboration, regional placement, and high-availability commitments;
- autonomous high-impact actions;
- blanket or indefinite desktop-control grants.

## Evaluation fixtures

Fixtures validate breadth; they do not outline product positioning.

1. **One-off file Task:** compare or summarize selected files and produce a reviewable report without creating an App.
2. **Local file application:** import selected files, extract structured data, review exceptions, and create a report.
3. **Personal or operational tracker:** maintain records, forms, filters, calculations, and a dashboard.
4. **Recurring collection application:** retrieve user-configured public sources through qualified HTTP or browser operations, structure/deduplicate/store data, apply custom processing, and run again on a local schedule with evidence and correction.
5. **Authenticated browser workflow:** connect a dedicated signed-in profile, perform approved read/form/file operations, handle login expiry or MFA through takeover, and review consequential effects under current policy.
6. **Novel request challenge:** choose answer, Task, or App appropriately for an unfamiliar request without adding domain logic to the platform core.

## Readiness gates

### Internal prototype gate

- isolated App workspaces;
- a bounded platform-owned Task execution profile with explicit inputs, routes, budgets, outputs, and cancellation;
- deterministic build and launch behavior;
- a bounded Build-plan/command policy that re-prompts only when executable, network, file, credential, privilege, or material-risk scope expands;
- no embedded durable credentials;
- build validation, logs, cancellation, Versions, and rollback;
- non-sensitive test data only until local persistence and recovery are proven.

### Memory gate

- memory authority and storage placement are explicit and independent of App deployment;
- exact source provenance and Context selection evidence;
- correction, revocation, export, and deletion propagation;
- no automatic promotion of inferred claims to trusted fact;
- no cross-App or cross-Task retrieval without a visible grant.

### External tester gate

- signed and updateable application;
- encrypted local state and verified backup/restore;
- understandable permissions and outbound disclosures;
- resource, time, network, and model budgets;
- crash recovery and safe uninstall;
- the external local release has qualified a local generated-code execution boundary and protected browser-session handling; a remote microVM is not an implicit fallback for this local-first release;
- every enabled generated-code, browser, or cloud route has passed its specific containment and recovery tests.

### Cloud gate

- tenant isolation;
- cloud secrets and identity;
- durable scheduling, retries, deduplication, and dead-letter handling;
- metering and quotas;
- export and deletion;
- clear distinction between cloud-capable and device-dependent operations.

### Observation and autonomy gate

- visible collection controls and exclusions;
- provenance and retention;
- prompt-injection treatment of observed content;
- review before memory promotion;
- no authority inferred from demonstration;
- shadow or supervised execution before autonomy;
- separately scoped Computer Action authority, a visible active state, and an immediate stop control before any desktop effect.

## Product metrics

- time from request to useful preview;
- time from request to a useful one-off Task result;
- cold startup, first-progress, generated-App cold-start, idle-memory, package-size, disk-growth, and restart/recovery budgets;
- percentage of eligible one-off Tasks completed without an App Build;
- successful promotion of proven Tasks into reusable Apps without re-entering intent;
- percentage of Builds reaching a working Release;
- repeat use of released Apps;
- correction and repair success without developer intervention;
- Run reliability and understandable failure recovery;
- permission and deployment comprehension;
- cloud cost per active App and per useful Run;
- user trust, retention, and deletion confidence.
