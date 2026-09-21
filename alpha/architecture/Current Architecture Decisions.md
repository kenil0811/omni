# Current Architecture Decisions

Status: Canonical current-state register
Last updated: 21 September 2026

## Purpose

This register contains only decisions that currently govern the product. Superseded proposals and completed decision reviews are removed from the active corpus rather than retained as competing guidance. Library version history remains the recovery mechanism.

## D-001 — Keep the product horizontal

**Decision:** Capabilities are general-purpose and users choose what to build. Example Apps validate breadth and recurring value but do not define a vertical product.

**Consequence:** The implementation may constrain supported runtimes and adapters without constraining the user's domain.

## D-002 — Make the Assistant the front door and Apps the first reusable object

**Decision:** The user starts with the Workspace Assistant rather than choosing an object type. The Assistant may answer directly, create a bounded one-off Task, or open the App lifecycle. Apps are the first implemented reusable unit of interface, mutable data, repeated execution, permissions, Activity, Versions, and recovery. Builder is one of the Assistant's roles.

**Consequence:** Not every request becomes an App. Observation, Procedures, Workflows, and Agents still arrive after useful bounded execution and compose with the same governance principles.

## D-003 — Select deployment per App

**Decision:** Every Release targets either `On this Mac` or `Always available`. A user may operate both kinds of App in one Workspace.

**Consequence:** Deployment is not an account-wide privacy mode and not a separate product edition. Task execution and Workspace-memory placement are governed separately rather than inheriting an unrelated App's Release target.

## D-004 — Define local by execution and persistence, not by offline inference

**Decision:** An `On this Mac` Release executes locally and keeps persistent App code, data, secrets, logs, and history local. It may call remote AI models, websites, APIs, and user-selected external services.

**Consequence:** The platform promises no silent cloud persistence of operational App data, not zero network egress. Each external route remains visible.

## D-005 — Make cloud Apps cloud-authoritative

**Decision:** An `Always available` Release executes and persists operational state in cloud so schedules survive an unavailable Mac and supported clients can reach the App remotely.

**Consequence:** Cloud identity, tenant isolation, secrets, retention, export, deletion, quotas, and metering are required before this target ships.

## D-006 — Keep one portable App Version

**Decision:** App packages declare logical Resources, Connections, Entrypoints, Capabilities, runtime requirements, interfaces, and tests. Machine paths, user data, credentials, and deployment-provider identities are excluded.

**Consequence:** A Release Resolution Record binds the package to local or cloud providers without regenerating the App.

## D-007 — Run real generated code locally

**Decision:** The initial Builder may create code, install approved dependencies, run commands, and launch Apps in managed local workspaces. A local VM is not a prerequisite for the prototype.

**Consequence:** The early trust model is similar to a coding agent operating under the user's macOS account. Bounded Build-plan approval, command visibility, risk-scope re-approval, workspace separation, secret isolation, process supervision, backup, and rollback are mandatory; stronger isolation is an external-test gate rather than a claim supplied by same-user process separation.

## D-008 — Support one generated-App stack first

**Decision:** The prototype supports one standardized application architecture and toolchain.

**Consequence:** Operational reliability is tractable while user use cases remain broad. Additional runtimes require explicit qualification.

## D-009 — Separate Build and released-App authority

**Decision:** Temporary Builder access to an App workspace does not become runtime access. A Release receives only resolved Resources, Connections, Capabilities, configuration, and model routes.

**Consequence:** Building, publishing, reading data, using secrets, and performing external effects remain distinct authority changes.

## D-010 — Use immutable Versions and explicit Releases

**Decision:** Every material change creates a candidate App Version. A Release activates one exact Version for one deployment target. Rollback moves the Release pointer.

**Consequence:** Production code is not silently self-modified, and repair remains reviewable and reversible.

## D-011 — Preserve a typed App UI Bridge

**Decision:** Generated UI performs scoped reads, invokes Entrypoints, follows operations, exchanges Artifacts through trusted flows, opens shell destinations, and receives filtered events through a versioned Bridge.

**Consequence:** Generated interfaces receive no direct database, file, credential, native API, or internal-service access.

## D-012 — Broker capabilities and secrets

**Decision:** External systems, device capabilities, and consequential effects are authorized against the current user and exact execution authority: a Task Attempt snapshot or an App Release and Grant. Policy, destination, effect, approval, and budget remain explicit. Durable secrets remain in platform-owned storage.

**Consequence:** Generated code requests an operation or receives narrowly scoped material; it does not own broadly reusable credentials by default.

## D-013 — Make local scheduling honest

**Decision:** Local schedules are part of the first usable release. Work executes only while the Mac is awake and the approved local runtime is running, with network access when required. There is no implicit cloud fallback or automatic wake.

**Consequence:** Core owns durable occurrences and admits ordinary Release-bound Runs. The UI shows next/last/missed work and why it could not run. Missed occurrences remain visible and can be retriggered when the user chooses; recovery never automatically catches them up. Closing the main window leaves automation and the scheduler running; explicitly quitting the runtime stops local execution. Activation depends on the completed scheduler and lifecycle contracts.

## D-014 — Use shared cloud control and ephemeral workers

**Decision:** Cloud Apps use a shared control plane, durable scheduler and queue, cloud state, and ephemeral or strongly isolated workers for generated-code and browser jobs.

**Consequence:** Do not operate one permanently running VM per App by default. Cost follows active storage and work.

## D-015 — Defer live local/cloud synchronization

**Decision:** Deployment movement is an explicit compatibility-checked migration or clone. Schedule authority and selected state move deliberately.

**Consequence:** Active-active conflict resolution, duplicate effects, and encrypted synchronization do not burden the initial product.

## D-016 — Treat device-dependent cloud steps explicitly

**Decision:** A cloud App may later request a scoped operation from a registered Mac. If that device is unavailable, the step becomes `waiting_for_device`.

**Consequence:** `Always available` describes the cloud scheduler and cloud-capable work, not magical access to offline local files.

## D-017 — Introduce integration and computer-use capability in tiers

**Decision:** Prefer approved APIs or feeds, then direct HTTP retrieval, service connectors, deterministic browser automation, scoped operating-system accessibility actions, and only later visual agentic computer use.

**Consequence:** Browser operation is part of the first usable release; the internal manual milestone may precede it. Desktop action remains later. Broad functional coverage is assembled from narrow grants rather than one blanket desktop permission.

## D-018 — Treat authenticated browser state as a protected Connection

**Decision:** Browser identity and protected session state are platform-owned Connection bindings, not a browser-profile Resource exposed to App code. Profiles, cookies, uploads, downloads, destinations, and material effects are isolated and separately governed from ordinary App code.

**Consequence:** Local sessions remain local unless the user deliberately chooses a cloud browser route. Site policy and access restrictions can make an automation ineligible even when technically possible.

## D-019 — Keep remote model routes explicit and provider-neutral

**Decision:** Assistant Task, Builder, and published App runtime model routes are separately bound. One or more remote providers may be supported first; capable local models may be added behind the same interface.

**Consequence:** The product does not claim device-only inference, and it never changes provider, data category, or billing owner silently.

## D-020 — Keep mutable data outside App Versions

**Decision:** App Versions declare schemas and migrations; Resources hold user data. Local adapters may use SQLite and files, while cloud adapters may use managed relational and object storage.

**Consequence:** Packages are portable, shareable without personal data by default, and recoverable independently of mutable state.

## D-021 — Preserve evidence and reconstructability

**Decision:** Every execution is reconstructable. An App Run is attributable to its user or Trigger, Version, Release, configuration, relevant context, model route, Capability operations, outputs, costs, and state events. A Task Attempt records the equivalent Task revision, execution profile, inputs, authority snapshot, routes, outputs, costs, and events without pretending to be an App Run.

**Consequence:** User-visible Activity, technical logs, audit, evidence, and telemetry remain related but distinct. App and Task wire contracts may remain separate until a shared execution kernel is proven.

## D-022 — Normalize future inputs as Observations

**Decision:** Screen, voice, browser context, watch sessions, and connected-source inputs terminate at a trusted Observation boundary.

**Consequence:** Captured content is untrusted evidence. Capture permission grants neither memory promotion nor action authority.

## D-023 — Build the second brain after useful bounded execution, not after cloud

**Decision:** First prove the Assistant, limited Tasks, and reusable Apps. After that gate, advance useful automation, local context and memory, and cloud availability as independent tracks with explicit dependencies. Add screen or voice observation, Procedure compilation, and bounded proactivity only after the applicable execution and trust foundations are useful.

**Consequence:** Cloud deployment is not a prerequisite for local Workspace memory. Future architecture seams cannot expand or block the current Task-and-App slice.

## D-024 — Distribute Mac-first outside the App Store initially

**Decision:** Target a signed and notarized direct Mac distribution so the product can manage generated code, child processes, local workspaces, and updates under explicit user consent.

**Consequence:** Store distribution may be reconsidered only if its sandbox and policy constraints remain compatible with the product.

## D-025 — Develop through gated vertical slices

**Decision:** Define the minimum safe boundary, build one complete slice, observe use and failure, revise contracts, and widen one capability class at a time.

**Consequence:** Internal prototypes may use a broader trusted-code posture than external releases, while external distribution, browser profiles, cloud tenancy, observation, and autonomy each require their own readiness gate.

## D-026 — Make one-off Tasks first-class without hiding an App

**Decision:** A Task is a durable request with immutable revisions and one or more attributable Task Attempts. v0 Task Attempts use a platform-owned local execution profile for typed text, deliberately selected files, named model routes, bounded tools, and output Artifacts. They do not create an implicit App, App Version, Release, or Entrypoint.

**Consequence:** Small work stays lightweight while retaining evidence, cancellation, retry, and lineage. Repeated or stateful work can seed an App Build, but promotion creates the App's normal contracts and authority rather than relabelling the Task.

## D-027 — Keep Task Attempts and App Runs distinct at the contract boundary

**Decision:** Existing App Run, Release, and Capability contracts remain App-specific. The first Task contract defines a Task execution snapshot and Attempt ledger that reuse the same principles for policy, budgets, approvals, Artifacts, evidence, and recovery. A later generalized execution kernel may unify common mechanics only after both paths are implemented.

**Consequence:** v0 does not generate a hidden platform App per Task or weaken exact App Run identity merely to reuse a schema.

## D-028 — Keep Workspace memory placement independent

**Decision:** Workspace Context and memory have an explicit storage and processing placement separate from any App Release. The first useful memory profile may persist locally while using disclosed remote inference. Cloud synchronization or cloud-authoritative memory is a later user-visible choice.

**Consequence:** Users do not have to cloud-deploy Apps to receive durable Assistant context, and moving one App does not silently move Workspace memory.

## D-029 — Reserve a governed Computer Action capability

**Decision:** Future desktop action is an outbound governed capability, not an input adapter and not a consequence of screen-capture consent. It uses scoped application, window, operation, data, time, and effect grants; a visible active state; evidence; approvals for material effects; and an immediate stop control.

**Consequence:** The architecture can later operate desktop applications while v0 implements no desktop control. Accessibility and deterministic selectors precede visual clicking, and observation never supplies action authority.

## D-030 — Use Tauri 2 for the Mac shell

**Decision:** The Mac application uses Tauri 2 with a React, TypeScript, and Vite trusted interface. A small Rust host owns native windows, Tauri capability configuration, file and folder selection, Keychain access, application updates, top-level process supervision, and the bridge to the trusted platform service. Electron, Next.js, and a native Swift rewrite are not part of v0.

**Consequence:** The trusted shell uses the system WebView; the separately managed Playwright/Chromium automation worker has its own qualified browser artifacts. Only the trusted shell receives narrowly allowlisted Tauri commands. Generated App interfaces receive no Tauri capability and communicate only through the App UI Bridge.

## D-031 — Split the trusted local core from untrusted workers

**Decision:** The local trusted core consists of the Tauri/Rust host and one bundled Python platform service. The Python service owns Assistant routing, Task and App domain services, persistence, package validation, model adapters, and Build orchestration. It is reached only through a versioned local IPC adapter; the Rust host mediates browser-interface access. Builder sessions and generated App runtimes execute as separate supervised process groups with distinct homes, workspaces, environments, identities, and logs.

**Consequence:** Python provides the fastest route for AI and data functionality while Rust remains the narrow native trust boundary. A Builder crash or App crash cannot become a shell crash, and neither worker receives the platform service's database connection, Keychain handle, bearer material, or ambient environment. macOS uses a private Unix-domain transport; a later Windows host may implement the same contract over a named pipe.

## D-032 — Standardize the first generated-App stack

**Decision:** The first App profile uses Python 3.13 Entrypoint functions declared through the App SDK for backend logic; the platform `app-runtime` worker hosts them with FastAPI, Pydantic 2, and Uvicorn, so generated packages contain no web framework, server, or port (revised 21 Sep 2026 on EXP-BUILDER evidence: 15/15 generated Apps needed none); `uv` and `uv.lock` for Python dependency resolution; and React, TypeScript, and Vite for an optional custom interface compiled to static assets. Frontend Builds use the current qualified Node.js LTS and pnpm with `pnpm-lock.yaml`. The generated App imports a versioned platform SDK and component kit rather than storage, Keychain, Tauri, or internal-service APIs directly.

**Consequence:** The App remains real code and can express broad workflows, data processing, forms, tables, dashboards, and custom logic, but v0 does not promise arbitrary frameworks. React/Vite static assets are the only generated Surface implementation in v0; Apps without one use the trusted fallback, and portable native-view declarations are rejected by the v0 runtime profile. Node is a Build dependency rather than a production App-server requirement. Exact patch versions and dependency hashes are fixed in the repository's runtime-profile lock and may change only through a qualified profile revision.

## D-033 — Ship managed toolchains rather than require developer setup

**Decision:** External test builds must include or install through a signed, hash-verified product flow the architecture-specific CPython runtime, `uv`, Node.js LTS, pnpm, and selected Builder adapter. A user is not required to install Python, Node.js, Docker, Homebrew, or command-line developer tools. Internal development may use equivalent pinned local toolchains.

**Consequence:** The installer is larger, but first-use reliability and reproducibility take priority over download size. Runtime artifacts and Builder versions are inventory items with provenance, compatibility, and rollback metadata.

## D-034 — Use DeepSeek Harness as the first Builder candidate behind the adapter

**Decision:** Implement the DeepSeek Harness adapter first because the interface and lifecycle proof already exist. Implement OpenCode as the required second real adapter and benchmark both through the same Build requests. DeepSeek is the presumptive v0 Builder only if it passes the quality, recovery, containment, latency, and cost gate; failure promotes the better conforming adapter without changing App contracts.

**Consequence:** Harness-native models, tools, skills, sessions, subagents, and diagnostics may improve a Build but remain adapter-private. Harness-native browser use, computer use, Code Mode, autonomous subagents, and third-party plugins are disabled in the initial profile. Released Apps use the separately governed platform BrowserProvider; a synthetic validation route never imports production sessions into a Build. Every upstream version is pinned and requalified; Harness sessions never become platform truth or released-App dependencies.

## D-035 — Keep the Task Runner smaller than a coding harness

**Decision:** Direct answers and v0 Task Attempts use a platform-owned typed loop rather than DeepSeek Harness or OpenCode. The Python service may use the open-source Pydantic AI core for provider adapters, structured output, streaming, and fixed typed tools, but platform records remain authoritative for lifecycle, policy, approval, budgets, evidence, persistence, and retry.

**Consequence:** A one-off Task does not inherit file editing, shell access, browser use, plugins, subagents, or coding-agent state. Pydantic AI is replaceable implementation plumbing behind platform interfaces, not the Task domain model or permission system.

## D-036 — Use SQLite, an owned Artifact store, and Keychain locally

**Decision:** The Python platform service uses SQLite with WAL and explicit migrations for the local control ledger, plus separately owned SQLite Resource stores per App and a content-addressed file area for packages and Artifacts. SQLAlchemy 2 and Alembic are the initial persistence tools. Durable provider secrets and wrapping keys use macOS Keychain. SQLCipher-compatible database encryption and encrypted Artifact payloads are required before the external-tester gate; the internal prototype uses non-sensitive fixtures until that gate passes.

**Consequence:** Mutable data remains outside App Versions, an App can be deleted or exported without exposing unrelated state, and the cloud profile can later bind the same logical repositories to PostgreSQL and object storage. Generated code receives Resource and Artifact handles, never database paths, encryption keys, or raw connections.

## D-037 — Do not select the cloud vendor stack during the local slice

**Decision:** Preserve implementation ports for control persistence, object storage, secrets, schedules, queues, sandbox workers, and model routes, but choose and operate no cloud stack until measured local use demonstrates an always-available need. The likely cloud shape remains a modular Python service, PostgreSQL, S3-compatible object storage, managed scheduling and queues, and qualified ephemeral sandbox workers.

**Consequence:** v0 does not acquire fixed infrastructure cost or premature provider coupling. The local architecture is not allowed to depend on SQLite paths, local process identifiers, or Tauri APIs in portable App packages, so this deferral does not create a rewrite requirement.

## D-038 — Implement v0 as a contract-first modular monorepo

**Decision:** The first implementation uses one monorepo, one trusted modular-monolith Python service, one narrow Tauri/Rust host, and separate supervised Builder, parser-helper, released-App, and browser-runtime workers. Domain modules have explicit owners and dependency direction. Synchronous same-database work uses direct services and transactions; durable operations or outbox facts are reserved for real process, human/provider wait, restart, asynchronous-consumer, or external-effect boundaries. Machine-readable contracts, SDKs, worker packages, generated-App templates, fixtures, configuration, and packaging live in the exact structure defined by `Implementation Blueprint.md`. The platform Task Runner remains bounded trusted Core code rather than a coding-harness worker.

**Consequence:** v0 gains one reproducible build and clear boundaries without local microservice, broker, container, or orchestration overhead. Scheduling and browser execution are current-release modules/providers. Future cloud, observation, memory, and Computer Action areas preserve ports without empty implementation modules. Native services have Mac implementations behind interfaces that support a later Windows host. The repository structure may grow inside an owned boundary, but changes to process ownership, dependency direction, trust, or contract authority require an architecture update first.

## D-039 — Isolate non-trivial selected-file parsing from Core

**Decision:** Core may parse only bounded plain UTF-8 and JSON directly. PDF, Office, archive, image, native-library, decompression, and other non-trivial parsing or conversion executes through a disposable registered `parser-helper` worker with one selected-file handle, no network or shell, finite CPU/memory/time/expansion/output budgets, and a validated normalized result.

**Consequence:** The first Task slice does not make complex untrusted parsers part of the durable trusted service. Parser failure, exhaustion, malformed output, or hostile input can terminate a helper without corrupting Core, while Tasks remain a fixed platform profile rather than arbitrary code execution.

## D-040 — Lazy-start local App workers

**Decision:** A local App runtime starts for a manual or scheduled Run or active custom Surface and stops after a profile-defined idle period when no Run, human/provider wait, or open Surface remains. The approved resident Core includes the local scheduler and dispatches the exact worker just in time. Closing the main window keeps Core and active automation running. Reopening reconnects to the existing runtime; explicit runtime quit stops local execution. Login startup remains a separate preference.

**Consequence:** Workspace size does not imply one idle Python process per App. Cold-start and idle thresholds become measured runtime-profile budgets rather than an undefined always-running assumption.

## D-041 — Keep the v0 Resource profile minimal

**Decision:** The active local Resource profile supports App-scoped table create/get/list/update/delete with optimistic revisions, declared exact filters, stable cursor pagination, and Artifact-backed file namespaces. Aggregation, reference expansion, transaction-domain objects, a general Resource migration framework, Context access, and cloud providers are inactive.

**Consequence:** Portable contracts may retain broader vocabulary, but the first implementation builds only what the Task-to-App evidence slice requires. Any expansion needs a fixture, profile revision, and tests.

## D-042 — Version v0 internal protocols as one bundle

**Decision:** Core IPC, Host-control, and worker-bootstrap schemas live under one `local-platform-protocol` version and ship atomically in v0. App package/SDK/Bridge, database schema, runtime profile, and Builder adapter retain independent versions because they have distinct compatibility boundaries.

**Consequence:** Startup still fails closed on an incompatible bundle, but the first desktop product avoids a three-way internal compatibility matrix for components that are released together.

## D-043 — Preserve general-purpose creation and extensibility

**Decision:** Users may request arbitrary business goals supported by the available execution capabilities; no workflow, industry, or website catalogue limits product intent. Generated code and qualified dependencies implement custom logic. Apps may run as background workflows with trusted results/Activity and no custom UI.

**Consequence:** Model, Builder, capability, browser, runtime, persistence, and native-platform interfaces are explicit and versioned at real compatibility boundaries. New capabilities declare schemas, effects, permissions, compatibility, budgets, evidence, and conformance checks. Retain intent, rules, corrections, and execution history for later second-brain use without automatically granting memory access.

## D-044 — Include a general local BrowserProvider in the first usable release

**Decision:** Start with Playwright/Chromium behind a platform BrowserProvider. Support public and user-authenticated browser work, general navigation/extraction/forms/file operations, dedicated profiles, user sign-in/takeover, and approved effects. Browser access is not limited to a list of prebuilt site connectors.

**Consequence:** Protected Connection state stays outside generated code and packages. The browser worker has separately qualified lifecycle, network/file/effect control, credentials, cancellation, and recovery. Prefer suitable APIs when available. Browser capability does not imply desktop control or cloud execution.

## D-045 — Ship macOS first with explicit Windows extension boundaries

**Decision:** Share Core product logic, App/Workflow definitions, scheduling semantics, provider contracts, and React interfaces. Isolate native IPC, process control/containment, credential storage, paths, startup/sleep behavior, file access, signing, and updates behind host adapters.

**Consequence:** Run the shared suite on Windows early. Windows-native distribution remains a later qualification track. Generated Apps declare incompatible dependencies/capabilities rather than assuming every package runs everywhere. See `../specifications/Local_Automation_and_Platform_Extension_Profile.md`.

## Decisions still required

1. Pin the exact runtime-profile versions after the first clean packaging build.
2. Qualify the current DeepSeek Harness release against OpenCode and select the first default Builder/model route.
3. Decide whether the initial model experience is bring-your-own-key only or includes limited product-funded credits.
4. Decide the first external-test distribution and update endpoint after signing and notarization are proven.
5. Define and validate the first Task and Task Attempt wire contract before implementing one-off execution.
6. Define and version the `local-platform-protocol` bundle containing Core IPC, Host-control, and worker-bootstrap schemas and invalid fixtures before the trusted-skeleton implementation.
7. Choose and qualify the external generated-code containment/envelope before sensitive-data or broader external testing.
8. Choose the first cloud provider stack only when the cloud track begins.
9. Complete timezone/DST, overlap/offline, manual-retrigger linkage/Release/input semantics, and background-control/login-start presentation before enabling local schedules. Manual retriggering without automatic catch-up and continued execution after window close are accepted decisions.
10. Complete BrowserProvider payloads, session-sharing/locking and takeover semantics, evidence redaction, and exact Playwright/Chromium packaging qualification.
11. Qualify local generated-code and browser-session isolation for the external local release; choose Windows-native adapters when its delivery track begins.
