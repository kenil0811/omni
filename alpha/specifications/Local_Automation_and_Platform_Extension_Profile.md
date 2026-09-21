# Local Automation and Platform Extension Profile

Status: Accepted product scope and architecture requirements; wire-contract completion and implementation evidence pending
Profile revision: 2
Last updated: 21 September 2026

## Purpose and authority

Define the agreed first usable local release: a general-purpose generated App/workflow framework with recurring execution and browser automation, delivered on macOS first and designed for a later Windows host. This profile expands the current release without limiting users to a workflow catalogue or particular industry.

`Current Release Specification.md` owns release scope. This profile specifies its local automation and extension requirements. Existing App, Release, Capability, Run, and UI Bridge contracts retain their authority. No new wire fields, registry payloads, event types, or compatibility guarantees are implicitly introduced by this prose. The exact scheduler and browser payload schemas and invalid fixtures remain required implementation gates.

The internal v0.0 milestone may exercise manual execution with a fake Builder and synthetic inputs. It is not the first usable release and does not satisfy the scheduling, browser, or external-distribution gates.

## General-purpose product boundary

- Users may describe unfamiliar Apps, workflows, scripts, background jobs, data processing, or interactive tools. Evaluation examples test breadth and are not an allowlist of user goals or websites.
- An App is a reusable unit of work. It may have a generated React/Vite interface or use trusted configuration, results, and Activity surfaces without any custom interface.
- Generated Python and qualified dependencies provide custom logic. The initial runtime family constrains execution compatibility, not the business problem the user may solve.
- Permission, budgets, platform compatibility, and external-service access remain explicit. Unsupported capabilities are explained rather than silently replaced with a different outcome.
- The bounded one-off Task profile remains separate. Reusable or broader executable work uses an App Release and the corresponding authority review.
- Retain the Build Brief, intended outcome, input/output contracts, rules, correction rationale, Version lineage, and Run evidence. These provide future memory and procedure capabilities with meaningful history; they do not create automatic cross-App memory or action authority.

## Scope matrix

| Capability | Internal v0.0 | First usable local release | Later |
|---|---|---|---|
| Assistant, bounded Tasks, App lifecycle | Required | Required | Extensible |
| Real generated Python; optional custom UI | Fake package allowed for lifecycle testing | Required | Additional qualified profiles |
| Local scheduling | Not a prerequisite for the manual milestone | Required | Cloud scheduler provider |
| Public and authenticated browser work | Synthetic experiments allowed | Required after browser qualification | Other engines, session adapters, and cloud providers |
| General governed browser operations | Contract/worker experiment | Navigation, extraction, clicks, forms, selected uploads, downloads, and approved effects | Additional operation families |
| Direct HTTP/API route | Existing bounded profile | Existing qualified profile; prefer it when sufficient | Additional authenticated/write profiles and connectors as qualified |
| Windows | Shared-code checks and interface design | Shared Core CI; no Windows product release implied | Native host adapters, packaging, and full qualification |
| Desktop control, screen capture, ambient memory | Excluded | Excluded | Separately authorized and qualified capabilities |
| Cloud execution | Excluded | Excluded | Explicit Always available target |

Browser support does not activate arbitrary HTTP writes or every future connector. An unfamiliar site can be served through general browser capabilities without a dedicated site-specific platform module. The browser can interact with external systems; its durable profile, state, evidence, and execution remain local. Approved model or website requests may still send data outside the device.

## Local scheduling

### Availability and ownership

The Mac must be awake, the approved local runtime must be running, and required network routes must be reachable. Being connected to the internet alone is insufficient. There is no cloud fallback, automatic device wake, or promise of execution while the device is asleep, shut down, logged out, or the runtime is quit.

Core owns durable schedules and due occurrences in the local control ledger. It invokes the ordinary Run admission path for an exact active Release. The host owns process supervision and background residency. Closing the main window leaves the local runtime, active automation, and scheduler running. Reopening the window reconnects to that same runtime and its existing work; it must not start a duplicate scheduler. Explicitly quitting the runtime stops local execution. Background status and pause/stop/quit controls remain accessible through trusted controls. Starting automatically at login is a separate preference, not implied by closing the window.

Scheduled Apps remain lazy workers. The resident scheduler dispatches a worker when an eligible occurrence is due; it does not keep a Python process alive for every App. Cloud scheduling later implements the same logical ownership contract behind a different provider.

### Activation and invocation

Source schedules are disabled templates. Activation occurs through trusted Release configuration after the user reviews the cadence, timezone, next occurrence, access, and effect scope. The scheduled Entrypoint is a `job` with schedule invocation and occurrence-key idempotency under the existing contracts.

For each due occurrence:

1. Record a stable occurrence identity and intended execution time.
2. Resolve and verify the current active Release, schedule revision, enabled Entrypoint, grants, connection state, and budgets.
3. Claim the occurrence durably so restart or duplicate dispatch cannot create duplicate logical work.
4. Admit a normal Run and record actual start/completion, evidence, and any external-effect receipt.
5. Reconcile cancellation, process failure, lost connectivity, approval waits, and uncertain effects before retrying.

Pausing or revoking a schedule fences new admissions. A schedule update or Release change must not duplicate an already admitted occurrence. Browser login or approval waits retain durable Run identity; they do not mint another occurrence or silently extend permission.

### Missed jobs: visible, manually retriggered

When a scheduled occurrence is missed because local execution was unavailable, retain it as missed and show its intended time and reason. Returning online, waking the Mac, restarting the runtime, or reopening the window does not automatically execute missed work. Enabled schedules continue with future eligible occurrences.
The user can choose a missed occurrence and retrigger it later through a trusted action. The missed occurrence remains in history, linked to the resulting Run and its outcome; it is not rewritten as an on-time execution. Repeated delivery or double-clicking the same retrigger request must not admit duplicate logical work. Retriggering uses ordinary Run admission with current access, connection, budget, and approval checks. A blocked retrigger explains what is needed and does not bypass a pause or revocation. This policy does not turn interrupted or uncertain-effect Runs into fresh missed jobs; those retain their existing recovery rules.

The first usable release has no automatic catch-up or replay of missed occurrences and no alternative per-schedule catch-up policy selector. Exact wire payloads, occurrence-to-Run linkage, Release selection when an App has changed, and historical-input handling must be defined in the scheduler contract. Retriggering cannot promise to recreate historical source data that was never captured.

The scheduler schema must also define timezone/DST behavior, clock changes, missed-occurrence accounting, overlapping occurrences, network unavailability, retry windows, pause/resume, and effects whose completion is uncertain. Numerical defaults for those remaining matters are not selected here. Existing examples are illustrative contract fixtures, not approved release defaults.

### User-visible behavior

Show schedule enabled/paused state, timezone, next intended run, last actual run, missed occurrences with intended time and reason, a manual retrigger action, and the outcome of any retrigger. Explain that missed jobs wait for the user and that automation continues after closing the window. A missed occurrence is not a successful Run. Window-close, runtime-quit, sleep, wake, restart, and offline transitions must be covered in the local acceptance tests.

## Browser automation

### Initial implementation direction

Use Playwright with a qualified Chromium build as the first local `BrowserProvider`, preferably through the Python API in a registered `browser-runtime` worker consistent with the Python service boundary. Pin the Playwright driver, Chromium artifacts, and dependency hashes together in the runtime profile after packaging qualification. The provider interface must not expose Playwright objects, CDP addresses, browser binaries, or profile paths to generated code.

The exact provider implementation is verified by a short public-site and authenticated-site experiment before production integration. Playwright/Chromium is the selected starting direction, not a claim of compatibility with every website or device policy.

### Session and credential ownership

Use dedicated automation profiles managed by the platform. Users sign in themselves in a visible browser and can take over for MFA, login renewal, or failures. Importing or controlling the user's everyday browser profile is not implied by this release.

In the App contract, authenticated browser identity is a Connection such as `browser.profile`, not an App-owned table/file Resource. Profiles, cookies, headers, session storage, and account bindings remain protected platform state. Generated code receives a scoped session handle and approved operation results, never durable session material or an unrestricted debugging endpoint.

Define the exact profile/account sharing and locking rules during browser-contract completion. Reuse across Apps requires explicit grants; it must never occur just because two Apps visit the same domain. Profile deletion, logout, revocation, backup/restore, and expiry must have tested behavior. Plaintext session dumps and private browsing evidence must not enter packages or routine logs.

### General operations

The initial provider must support general navigation, page inspection and structured extraction, selectors and waits, clicks, form entry, selected uploads, and downloads into managed Artifact storage. Operation payloads are typed, bounded, and attributed to a Run and exact Release. A site-specific connector is optional rather than a prerequisite for a new website.

Capability declarations and Release grants define destination scope, relevant account, allowed operations, output/evidence limits, duration, and effect policy. Distinguish reading from actions that send, submit, delete, purchase, or change remote data. A valid login is not blanket action authority. Consequential actions use trusted approval where required by the existing Capability policy, with the actual account, destination, data, and effect shown.

The Assistant/Builder may generate or modify browser workflow code, but the released App operates through the platform browser provider. Disabling a harness's own browser plugin does not disable this runtime capability. Qualification may use a narrowly authorized platform browser test route; it must not copy production browser sessions into Builder workspaces.

Prefer an API/feed or qualified HTTP operation when it reliably fulfills the job. This is an execution choice, not a requirement to build a connector catalogue before browser support. DOM/selector-based automation is the initial route. General visual desktop control remains a separate future capability.

### Recovery and isolation

Preserve Run identity through human takeover, connection renewal, browser crash, and retry. Record whether an external effect is known completed, known failed, or uncertain; do not blindly resubmit after a navigation timeout. Recheck current grants and destination scope on resume. Stop controls must terminate automation and prevent subsequent effects without implying that prior effects were reversed.

Enforce navigation, redirects, expected authentication origins, network/subresource policy, file transfers, and current account scope at the trusted provider and qualified execution boundary. Browser page text and extracted content are untrusted data and cannot authorize new tools, destinations, or grants. The contract must specify safe errors and evidence redaction rather than relying on the model to obey a prompt.

A separate profile or worker is not a complete hostile-code security boundary. The first external local release must qualify local generated-code containment and browser-session protection before real sensitive inputs or credentials are used. A remote execution provider is not an implicit fallback for the local-first promise. Internal experiments may use synthetic data and dedicated test accounts within a documented envelope.

## Cross-platform architecture

macOS is the first shipping client. Windows is a required later target. Keep operating-system assumptions out of App definitions, Core business logic, scheduling semantics, and generated portable packages.

| Shared contract or implementation | Platform adapter responsibility |
|---|---|
| Assistant, Tasks, App/Build/Release/Run lifecycle | Native shell integration and file selection |
| Python Core, persistence semantics, migration rules | Application-data roots, file permissions, path handling |
| Model, Builder, Capability, and BrowserProvider interfaces | Process trees, cancellation, resource limits, and containment |
| Schedule and occurrence semantics | Login startup, background residency, sleep/wake notifications |
| Local-platform protocol message semantics | Private transport and peer authentication; Mac UDS, Windows transport qualified later |
| Logical secret handles and key lifecycle | macOS Keychain; qualified Windows credential/key-storage implementation |
| React trusted shell and App UI Bridge | Platform window behavior, accessibility, and native dialogs |
| Version/profile compatibility and update policy | OS/architecture-specific runtime bundles, installers, signing, updates |

The Rust host owns a platform-adapter layer. macOS-only implementations must be isolated behind those interfaces. Windows can use different primitives; Unix sockets, POSIX signals/process groups, Unix shell syntax, symlinks, hard-coded separators, and Keychain cannot become portable App requirements by accident.

Generated Apps use platform SDK handles and relative package paths. Dependencies and truly OS-specific capabilities declare compatibility in the qualified runtime/capability profile. Such an App is reported as platform-specific until a compatible implementation exists. Moving a package does not transfer credentials, browser profiles, permissions, or user data automatically.

From the first implementation repository, run platform-neutral Core, contract, path-handling, and relevant browser tests on Windows as well as macOS. Mac-only modules must remain import-isolated. These checks do not constitute a shipped Windows host or prove Windows sandboxing. The Windows delivery track must later qualify native supervision, IPC, credential storage, isolation, browser installation, updates, and lifecycle recovery.

## Extension requirements

Stable extension boundaries cover model providers, Builder harnesses, capabilities/connectors, browser providers, execution profiles, persistence providers, and native host services. An added capability normally contributes a typed definition, input/output schemas, effect and permission requirements, compatibility, budgets, evidence behavior, implementation, and conformance tests.

The Assistant and Builder discover supported operations through the capability registry; core product logic must not enumerate particular industries, websites, or workflow templates. Existing contracts reject unknown fields. Extending functionality uses registered definitions or an explicit versioned contract change, never arbitrary unvalidated fields inserted into existing manifests.

Implement only the adapters needed now. A public plugin marketplace, user-installed untrusted plugins, generalized distributed workflow engine, and every imagined runtime are not prerequisites for extensibility. Prove an extension boundary by adding a materially different capability or test implementation without changing the App lifecycle's authority semantics.

## Acceptance evidence

1. **Daily collection App:** user-configured sources → browser/HTTP retrieval → structured validation/deduplication → persistent records → custom processing → inspectable results → a later scheduled run → plain-language correction. A custom UI is optional.
2. **Authenticated browser App:** user signs in, the App performs approved work, and login expiry/MFA or a page change creates understandable intervention and recovery without leaked session material.
3. **Different file App:** selected files → transformation → persistent or exported output; custom rules need no domain-specific Core change.
4. **Interactive App:** a tracker or other user-requested interface exercises the same lifecycle with a custom Surface.
5. **Novel request:** an unfamiliar request is handled through available general capabilities or produces a specific missing-capability explanation. Examples are not a product menu.
6. **Availability and recovery:** closing the window preserves active work and future schedule dispatch; reopening reconnects without a duplicate runtime. Sleep, offline, quit, and restart preserve missed occurrences without automatic catch-up. A later user retrigger creates a linked Run under current authority, and repeated delivery does not duplicate it. Cancellation, queued overlap, revoked access, and uncertain effects retain their own recovery rules.
7. **Portability:** the shared suite runs on Windows; package validation detects incompatible dependencies/capabilities; Mac-native modules remain isolated.

These are required scenarios, not claims of executed tests. The delivery checklist tracks implementation and evidence.

## Decisions still open

- Exact cadence schema, timezone/DST, overlap and offline handling, numeric limits, and manual-retrigger payloads/lineage, Release selection, and historical-input handling.
- Background-status/control presentation and separate login-start preference; continued automation after window close is decided.
- Browser operation/registry schemas, session/profile locking and sharing, user-takeover messages, and evidence redaction.
- Exact Playwright/Chromium versions, packaging, dependencies, and performance budgets.
- Qualified local generated-code and browser execution boundary for external testers.
- Windows-native implementations and the Windows release timing.

These open items must be resolved before their affected functionality is implementation-ready. No choice is silently inferred from an illustrative fixture.

## Technical references

- [Playwright system requirements and platform support](https://playwright.dev/docs/intro)
- [Playwright browser binaries and version coupling](https://playwright.dev/docs/browsers)
- [Playwright authentication state](https://playwright.dev/docs/auth)
- [Tauri platform architecture](https://v2.tauri.app/start/)

References were checked during the product discussion. Exact runtime versions and security behavior require qualification on the actual packaged application.
