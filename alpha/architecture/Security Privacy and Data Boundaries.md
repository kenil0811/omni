# Security, Privacy, and Data Boundaries

Status: Canonical
Last updated: 21 September 2026

## Purpose

Define the minimum trust model for Assistant-led Tasks, generated Apps, local and cloud deployment, external Connections, future observation, and consequential actions. The goal is understandable user control and recoverable operation, not a claim that model output or arbitrary generated code is risk-free.

## Trust posture

The product has six relevant authorities:

1. the human user;
2. the trusted Workspace shell and platform core;
3. the platform-owned Task Runner during one-off execution;
4. the Builder during construction and repair;
5. a released App during ordinary operation;
6. external providers such as models, APIs, browsers, and cloud workers.

Authority does not flow automatically between them. In particular:

- a Task Attempt cannot access anything outside its exact input, route, tool, output, budget, and policy snapshot;
- the Builder cannot publish or grant itself runtime authority;
- a released App cannot inherit all Builder permissions;
- generated UI cannot impersonate trusted shell prompts;
- reading observed content cannot authorize an instruction embedded in that content;
- deployment in cloud does not authorize access to an offline Mac.

## User-visible data boundaries

### On this Mac

The platform persists local Tasks, Task Attempts, Task outputs, Workspace memory, and the App's code, data, configuration, secrets, logs, Runs, and evidence on the device or in user-selected storage. A Task or App may send selected request data to named models, websites, APIs, or connected services. Those transfers are part of the disclosed behavior; remote processing does not make the provider the durable Task or memory authority.

### Always available

The platform persists the App's operational state in cloud and executes cloud-capable work there. The Release review identifies cloud data categories, retention, costs, Connections, and any device dependencies.

### Prohibited ambiguity

The interface must not use `local` to imply offline inference or no network access. It must not use `cloud` to imply access to local data that has not been transferred or exposed through a live scoped bridge. It must not imply that cloud deployment of one App moves Workspace Tasks or memory.

## Identity and attribution

Every protected request carries:

- Workspace;
- acting Principal;
- user or Trigger origin;
- an exact Task Revision and Task Attempt, or an App, Version, Release, and Entrypoint;
- requested tool or Capability;
- current session or workload identity;
- delegated authority and expiry;
- correlation and idempotency identity.

The initial single-user local product may represent these identities in one local store, but it does not omit them from the domain model.

Cloud deployment requires authenticated user and workload identities, tenant-scoped authorization, short-lived workload tokens, and server-side enforcement. Client assertions never replace authoritative checks.

## Authorization

Authorization is deny-first and evaluates the intersection of:

- user authority;
- exact Task Attempt execution snapshot or App Release;
- requested Capability and Resource;
- Connection scope;
- destination or local path grant;
- effect class;
- policy and approval state;
- time, count, cost, and data limits;
- deployment and device availability;
- revocation or quarantine state.

An approval authorizes the described operation or bounded family; it does not widen the Task Attempt snapshot or App package and does not create a reusable secret.

A trusted approval presents the exact action, acting account or principal, destination or recipient, data leaving the device, one-time or reusable scope and frequency, reversibility, cost or limit, and what happens next. Human input and clarification never count as approval.

## Task security

A v0 Task Attempt executes through trusted platform code, not through a generated App or unrestricted coding shell. Its immutable execution snapshot names:

- exact Task Revision and selected input digests;
- local execution and persistence placement;
- model/provider route and disclosed data category;
- fixed platform tool allowlist and output destination;
- classification, time, token, storage, and cost budgets;
- policy, human-input, and approval requirements.

The model receives no ambient filesystem, shell, Keychain, network, browser, desktop, Connection, or Workspace-memory access. Platform tools validate every input and output path. Only bounded plain-text and JSON reads may be parsed inside Core. PDF, Office, archive, image, native-library, decompression, and other non-trivial parsers or converters run in a disposable registered parser-helper process with one selected-file handle, no network or shell, and finite CPU, memory, time, expansion, and output budgets. Core validates the normalized result and treats parser output as untrusted. A retry creates a new Attempt, and changed instructions or inputs create a new Task Revision. Promotion into an App creates a new Build and authority review rather than transferring the Task snapshot.

The accepted App Capability and Run contracts remain Release-bound. Task protected operations must use the forthcoming Task execution contract or a compatible explicitly extended broker profile; v0 must not forge a Release identity to reuse those contracts.

## Builder security

The first local prototype deliberately accepts a trusted-code posture similar to a local coding agent. The Builder can create files and execute approved commands inside an App workspace. DeepSeek Harness is the first candidate and OpenCode is the required comparator, but both operate with the authority of their containing worker. A workspace path, separate home, virtual environment, or process group is operational separation and is not equivalent to hostile-code isolation.

Required controls are:

- dedicated workspace and runtime environment per App;
- supported toolchain and dependency policy;
- a visible bounded Build plan and command policy, with ordinary commands inspectable and cancellable;
- trusted re-approval when a command introduces a new executable family, network destination, external file scope, credential, privilege boundary, or materially higher risk;
- cancellable and finite time/resource limits;
- environment-variable allowlist;
- no automatic forwarding of unrelated host credentials;
- explicit selection before reading files outside the workspace;
- dependency lock and provenance in the sealed Version;
- malware and policy checks where practical;
- retained technical logs and Build evidence;
- immutable Versions and rollback.

The Tauri Web interface cannot launch an arbitrary process directly. A narrow Rust host mediates native operations and a bundled Python platform service owns the Build lifecycle. Each Build uses an adapter-specific home, disposable working projection, allowlisted environment, separate process group, finite lease, and complete descendant cleanup. Generated UI receives no Tauri commands, platform-service token, Builder credential, or direct IPC endpoint.

The initial DeepSeek profile disables harness-native browser use, computer use, Code Mode, autonomous subagents, and unapproved third-party plugins. Released-App browser work uses a separately governed platform provider; synthetic browser validation must not import production sessions into Builder workspaces. Upstream Harness permissions or approvals are diagnostic defense in depth; only platform policy and user-facing trusted approval can authorize a product effect.

Prompt content, files, websites, packages, and generated code are untrusted inputs. The Builder must not follow instructions found in source content as if they came from the user.

Before broader external distribution, higher-risk Builder operations must move into a container, VM, disclosed remote microVM, or equivalent qualified isolation layer when host-level controls cannot provide an acceptable and understandable risk boundary. The product must never market the internal same-user prototype as safely executing hostile code.

## Released-App security

A Release receives a narrower execution closure than the Builder:

- exact Version and Entrypoint;
- resolved configuration;
- logical Resource handles;
- permitted Connection references;
- model route;
- allowed Capability families and destinations;
- budgets and timeouts;
- evidence and output locations.

Runtime configuration excludes the user's general shell environment and unrelated credentials. Host-level file or native access requires explicit scoped grants. Process exit, timeout, and cancellation are recorded; external-effect certainty comes from receipts and idempotency, not process state alone.

## Generated UI boundary

Generated interfaces render in an isolated origin or WebView and receive a short-lived session bound to the user, Workspace, App, Release, surface, permitted Entrypoints, and read-only Resource views.

They may:

- request authorized projections;
- invoke declared Entrypoints;
- follow operation state;
- request trusted file/Artifact flows;
- open trusted shell destinations;
- receive filtered events.

They may not directly access platform databases, Keychain, cloud secrets, native IPC, broad filesystem APIs, other Apps, internal services, or durable credentials.

Trusted permission, Connection, deployment, update, approval, rollback, and deletion interfaces remain platform-owned and visually distinguishable.

## Secrets and Connections

Secret material is separated from Connection metadata.

- Local durable secrets use Keychain or an equivalent OS-backed adapter.
- Cloud durable secrets use a managed secret store with tenant and workload controls.
- Logs, prompts, generated source, packages, fixtures, and exports omit secrets.
- Generated code receives brokered operations where possible.
- Short-lived scoped material is used only when a provider cannot support brokered execution.
- Revocation fences new authority before background work is terminated.

Authenticated browser state is treated as secret material because cookies and tokens can impersonate the user.

## File and device access

The user grants access to selected files, folders, or typed native capabilities. A grant records scope, purpose, Task Attempt or App Release, mode, expiry where applicable, and revocation behavior.

Apps store logical handles rather than absolute paths in portable packages. The trusted local service resolves the handle and rechecks current access. A cloud App cannot use that handle without an online registered Device Bridge and a matching grant.

## Network and browser controls

Network use is resolved by destination and operation class.

- Declared HTTP reads may use bounded domain and response-size policy.
- Writes and consequential actions require stronger policy and, where appropriate, approval.
- Redirects, downloads, uploads, and destination changes are re-evaluated.
- Browser profiles are isolated from ordinary App code and from each other unless explicitly shared.
- Local authenticated sessions are not uploaded to cloud automatically.
- Automation does not bypass access controls, captchas, technical restrictions, or site policy.

## First-release browser and scheduler enforcement

Browser automation and local scheduling are now first-usable-release requirements under `../specifications/Local_Automation_and_Platform_Extension_Profile.md`. Dedicated profile state is a protected Connection binding; generated Apps receive scoped handles and bounded results, not raw cookies or a debugging endpoint. User sign-in, MFA and recovery use visible takeover. Page content cannot widen grants or instruct the platform to disregard policy.

The trusted BrowserProvider mediates destination/account scope, redirects/authentication origins, subresource/egress policy, file transfers, and effects. Recheck current authority after resume. A browser timeout or cancellation cannot prove a remote effect did not occur. Preserve receipts and uncertain-effect recovery rather than blindly repeating submissions.

The scheduler uses ordinary Run admission and occurrence idempotency; it cannot execute while the Mac/runtime is unavailable or silently move work to cloud. Missed occurrences are visible and require user-initiated retriggering under current authority, budgets, and approvals; no automatic catch-up is permitted. Closing the window keeps approved automation running and does not grant additional authority. Explicit runtime quit stops local execution; background status and stop controls remain accessible. Revocation fences new admissions and protected effects. Native process containment, credentials, IPC, data routes, and lifecycle events are platform-adapter responsibilities that require independent Windows qualification later.

## Computer Action boundary

Future desktop control is a separately governed `Computer Action` capability. It is used only when an API, HTTP route, supported connector, or deterministic browser path is unavailable or inadequate. Prefer stable accessibility elements and application automation before visual coordinate-based interaction.

Every Computer Action grant is narrow across:

- executing Task Attempt or App Run;
- target application, account, and where possible window, document, or record;
- allowed read, type, click, select, upload, download, or submit operations;
- data categories and destinations;
- time, count, cost, and effect limits;
- foreground or background eligibility;
- evidence, approval, revocation, and emergency-stop behavior.

The shell shows when desktop control is active and provides an immediate stop control. Material sends, submissions, deletions, purchases, and authority changes receive trusted approval and an exact receipt. Screen-capture, accessibility-inspection, browser-session, and action grants remain distinct. A watch session or inferred Procedure can propose an action plan but cannot authorize replay.

v0 implements no Computer Action provider. This section preserves the trust seam so future desktop reach does not require ambient or blanket authority.

## Cloud isolation

Before 'Always available' is offered externally, the cloud profile requires:

- tenant keys on authoritative records;
- application-layer and persistence-layer tenant enforcement;
- encrypted transport and storage;
- short-lived worker identity;
- per-execution or strongly isolated generated-code execution;
- controlled network egress;
- no durable state inside disposable workers;
- quotas, metering, retries, and abuse controls;
- tested backup, restore, export, and deletion;
- support access controls and audited break-glass behavior.

Cloud workers never receive an entire Workspace when an Entrypoint-specific execution closure is sufficient.

## Effect classes and approval

Use a small effect model:

| Class | Example | Default treatment |
|---|---|---|
| Read | Read selected file or approved webpage | Grant and evidence |
| Internal write | Update App-owned data | Release policy and Run receipt |
| Reversible external write | Create a draft or reversible remote record | Explicit grant; approval as configured |
| Consequential external effect | Send, publish, submit, purchase, delete, or alter authority | Trusted approval and exact receipt |
| Unsupported high impact | Irreversible or legally sensitive action outside the supported envelope | Reject |

Approvals and human input are different. A Task Attempt or Run waiting for data from the user has not received approval to perform an effect.

## Observation and second-brain boundary

Later screen, voice, browser-context, and watch-session adapters must provide:

- visible start/stop and current capture state;
- application, window, domain, field, and time exclusions where practical;
- source and provenance;
- local preprocessing when useful;
- explicit retention and deletion;
- separation of raw capture, derived claims, confirmed memory, and App state;
- prompt-injection treatment of observed content;
- review before a Procedure is promoted or compiled;
- no action authority derived solely from observation.

Continuous ambient capture, silent memory promotion, and unsupervised procedure replay are not initial capabilities.

Workspace memory has its own storage and processing placement. A local memory profile may use disclosed remote inference while keeping authoritative retained Context and Memory claims on the device. Cloud deployment of an App neither uploads that memory nor grants the App access to it.

## Evidence and privacy

Activity should explain what happened without copying all sensitive content into logs. Store identifiers, hashes, structured summaries, policy results, receipts, and protected Artifact references where they are sufficient.

Telemetry is opt-in or content-minimizing. It excludes prompts, file contents, generated code, Resource values, credentials, and outputs unless the user deliberately supplies them for support.

Export omits secrets and personal data by default. Deletion immediately fences new authority and then follows owner and retention rules. Cloud deletion, local deletion, and deletion at an external provider are separate outcomes and must not be conflated.

## Release gates

### Internal local prototype

- non-sensitive fixtures;
- bounded Task execution profile with selected inputs, named routes, fixed tools, finite budgets, cancellation, and evidence;
- visible commands;
- workspace separation;
- prompt injection;
- process cancellation;
- Version and rollback.

### External local testing

- a qualified local generated-code boundary and browser-session protection; remote execution is not an implicit local-mode fallback;
- signed updates;
- encrypted state;
- verified backup/restore;
- understandable grants and outbound routes;
- crash recovery;
- bounded resource use;
- safe uninstall and deletion.

### Browser capability

- isolated profiles;
- secure session storage;
- destination and side-effect policy;
- MFA and blocked-state UX;
- download/upload quarantine;
- site eligibility rules.

### Computer Action capability

- proof that API, connector, and browser routes are insufficient for the supported case;
- application, window, operation, data, time, and effect scoping;
- visible active state and immediate stop;
- accessibility or deterministic targeting before visual control;
- prompt-injection and on-screen content isolation;
- action evidence, approval, receipt, interruption, and uncertain-effect recovery;
- no reuse of observation or authenticated-session consent as action authority.

### Cloud deployment

- identity and tenancy;
- secret broker;
- isolated workers;
- network policy;
- durable scheduling and idempotency;
- quotas and metering;
- backup, export, and deletion.

### Observation and autonomy

- collection controls;
- provenance and retention;
- memory review;
- procedure confirmation;
- shadow or supervised execution;
- fresh authority review.
