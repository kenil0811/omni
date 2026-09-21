# Independent Product and Architecture Review — Reconciled Assessment

Review date: 21 September 2026
Reconciled into the canonical baseline: 21 September 2026
Perspective: Staff engineer and senior software architect
Status: Historical non-authoritative assessment of the earlier 21 September baseline; see current-scope clarification below
Last updated: 21 September 2026

## Subsequent scope clarification

This review predates the founder's explicit confirmation of a general-purpose App/workflow builder with local scheduling, public/authenticated browser automation, extensibility, and a later Windows host. Those decisions now govern the first usable release under `../specifications/Local_Automation_and_Platform_Extension_Profile.md`. The smaller manual v0.0 milestone remains internal.

The prior sequencing and scope descriptions below are retained as dated review history, not the current delivery plan. In particular, browser/schedule deferral and delaying all real feasibility until the fake lifecycle are superseded. Its security, recovery, usability, and weak-evidence findings remain relevant. A subsequent founder decision selects visible missed jobs with user-initiated re-triggering and no automatic catch-up, plus continued automation after window close.

## How to use this document

This is a dated independent critique, not a product specification, architecture authority, delivery plan, or second checklist. Current truth lives in `../00 Project Index.md`, the canonical product and architecture documents, `../specifications/Current Release Specification.md`, and `../delivery/Delivery Checklist.md`.

The review is retained because its challenge to scope, trust, and sequencing materially improved the project. Its original action language has been replaced by the reconciliation record below so resolved findings cannot continue to compete with current decisions.

## Executive verdict

The product direction is coherent and relevant: one Assistant chooses among a durable answer, a bounded one-off Task, and a reusable App, while preserving a path toward a user-controlled procedural second brain. That is stronger than positioning the product as another prompt-to-app tool.

The architecture is directionally sound. Its strongest qualities are explicit authority boundaries, local/cloud honesty, immutable history, evidence, cancellation, recovery, correction, and rollback. Tauri/Rust plus a Python modular monolith is a credible Mac-first implementation shape, and deferring the cloud provider is correct.

The main risk remains unchanged: documentation maturity is far ahead of product evidence. Even after scope correction, this is a substantial desktop platform. The project should proceed only through the ordered evidence gates now recorded in the roadmap, blueprint, and delivery checklist. A horizontal product does not justify a horizontal implementation explosion.

### Current assessment

| Area | Assessment | Current meaning |
|---|---|---|
| Product model | Strong | Assistant -> answer/Task/App is coherent and differentiated |
| Horizontal positioning | Reasonable but unproven | User freedom is preserved; fixtures and cohorts must still produce repeat-use evidence |
| Architecture boundaries | Strong | Authority, placement, lifecycle, evidence, and recovery are explicit |
| v0 sequencing | Improved | An internal v0.0 gate now precedes real Builders and HTTP breadth |
| Security | Honest but externally blocked | Same-user generated code is not containment; an external envelope still requires evidence |
| UX | Specified but partly unproven | App shell evidence exists; Assistant/Task screens still need prototype and usability proof |
| Contracts | Strong design evidence | Portable vocabulary is broader than the current runtime profile by design |
| Implementation readiness | Ready for the pre-code contracts and narrow spikes | Not ready for broad v0 construction or external sensitive-data testing |
| Product evidence | Weak | No real Alpha product, repeated user use, performance data, or credentialed Builder scorecard yet |

## Review scope and evidence

The reconciled `\alpha` corpus contains 85 files in 9 folders: 30 Markdown, 30 JSON, 2 JSONL, 13 YAML, 7 Word documents, 1 PDF, and 2 ZIP archives. The review covered canonical product, architecture, security, UX, delivery, specifications, schemas, examples, fixtures, proofs, and the nine-page reusable-App wireframe artifact.

Fresh corpus checks are recorded in `../delivery/Reconciliation Report.md`. The important evidence limitation remains: the documents and reference assets are serious design work, but the repository, full semantic validators, packaged Mac runtime, real Builder comparison, and user evidence do not yet exist. The seven-test Builder proof establishes adapter shape, not model quality, containment, or production readiness.

## What should remain unchanged

1. The Assistant is the front door; users begin with an outcome, not an implementation object.
2. A direct answer, a one-off Task, and a reusable App are distinct results.
3. Task promotion preserves lineage but never transfers authority.
4. The product remains horizontal; fixtures constrain evaluation, not user intent.
5. "On this Mac" means local execution and durable product state, not offline inference or zero network transfer.
6. Cloud availability is selected per App and remains a later track.
7. Observation, memory promotion, Procedure inference, and authority action remain separate.
8. Tauri 2/Rust host, React/TypeScript/Vite shell, bundled Python modular monolith, SQLite, Artifact storage, and Keychain remain the v0 technology direction.
9. Builder and App execution remain supervised workers; neither becomes platform truth.
10. Immutable Versions, explicit Releases, evidence, correction, and rollback remain product features rather than backend details.

## Reconciliation disposition

| Review finding | Disposition | Canonical result |
|---|---|---|
| The architecture had outrun product evidence | Accepted | Roadmap and checklist now require ordered evidence gates and recurring non-technical user validation without turning the product vertical |
| The documented v0 was too large | Accepted | Internal v0.0 proves Assistant/Task plus one deterministic fake-Builder App before real Builders or HTTP breadth |
| Same-user generated code was not safely contained | Accepted as an unresolved external gate | Internal work uses non-sensitive fixtures; external sensitive-data testing must qualify a local VM, restricted profile, remote microVM, or no-arbitrary-code envelope |
## Reconciliation disposition

| Review finding | Disposition | Canonical result |
|---|---|---|
| The architecture had outrun product evidence | Accepted | Roadmap and checklist now require ordered evidence gates and recurring non-technical user validation without turning the product vertical |
| The documented v0.0 was too large | Accepted | Internal v0.0 proves Assistant/Task plus one deterministic fake-Builder App before real Builders or HTTP breadth |
| Same-user generated code was not safely contained | Accepted as an unresolved external gate | Internal work uses non-sensitive fixtures; external sensitive-data testing must qualify a local VM, restricted profile, remote microVM, or no-arbitrary-code envelope |
| Non-trivial parsers were inside trusted Core | Accepted and corrected | A disposable registered parser-helper worker is part of the first file-Task slice |
| Assistant-first UX was missing from wireframe evidence | Partly corrected, still open evidence | The PDF is explicitly scoped to the reusable-App path; Workspace/Task states are specified and remain prototype/checklist work |
| Internal protocols were independently versioned | Accepted and corrected | Core IPC, Host-control, and worker bootstrap form one atomically shipped `local-platform-protocol` bundle in v0 |
| Outbox/saga semantics were over-applied | Accepted and corrected | Direct services and one transaction handle synchronous work; durable operations/outbox exist only for real async, process, wait, restart, or external-effect boundaries |
| Logical domain catalogue could become an implementation checklist | Accepted and corrected | The blueprint now names a bounded physical v0 inventory; future catalogue entities are explicitly dormant |
| Resource platform was too broad | Accepted and corrected | v0 is limited to App-scoped CRUD, optimistic revisions, exact declared filters, stable cursors, and Artifact-backed files |
| Two generated UI strategies doubled scope | Accepted and corrected | v0 implements one React/Vite Surface path plus trusted no-Surface fallback; native-view declarations are inactive portable vocabulary |
| App process lifetime was undefined | Accepted and corrected | Workers lazy-start for a Run or active Surface and idle-stop under the runtime profile; Core alone is resident by default |
| Per-command approval would be unusable | Accepted and corrected | Users approve a bounded Build plan; re-approval occurs only when executable, network, file, credential, privilege, or material-risk scope expands |
| Direct-answer persistence was unclear | Accepted and corrected | Answers remain durable searchable Assistant Turns and may be cited or saved as Artifacts without becoming Tasks |
| Older Task discovery was weak | Accepted and corrected | On-demand searchable Workspace history covers Assistant Turns, Tasks, and Apps without putting Tasks in the App browser |
| Approval sheets lacked material facts | Accepted and corrected | Trusted approvals name action, principal/account, destination/recipient, outbound data, scope/frequency, reversibility, cost/limit, and next effect |
| npm lockfiles conflicted with pnpm baseline | Corrected | Package Layout revision 3 and the reconciliation example use `pnpm-lock.yaml` |
| The maintenance rule conflicted with portable future shapes | Corrected | New speculative contracts remain prohibited; accepted portable contracts may retain inactive shapes while the release profile activates an explicit subset |
| App Contract revision heading was stale | Corrected | The Revision 5 heading now names revision 5 |
| Wireframes showed future capabilities as if current | Corrected at artifact scope level | The PDF and Mac specification state that schedules, monitoring, alerts, Connections, and device-wait examples do not enter v0 |

## Material risks still open

### Product evidence

The platform remains horizontal, but launch learning still needs concrete recurring jobs and a recruitable cohort. This is not a recommendation to hard-code a vertical product. It is a requirement to test the same Answer/Task/App loop repeatedly with people who move semi-structured information, reconcile exceptions, maintain small operational datasets, and produce outputs.

The key proof is not that the system can generate an App once. It is that non-technical users understand the routing, receive value faster than ordinary chat or coding tools, correct failures, reopen work, reuse the result, and trust the boundary.

### Generated-code containment

Directory separation, virtual environments, process groups, CSP, import checks, and environment allowlists are operational controls, not hostile-code containment. A process running as the signed-in user can attempt access beyond the SDK. This is acceptable only for an explicitly disclosed internal non-sensitive spike.

Before broader or sensitive-data testing, the product must choose and qualify one envelope:

- local VM or Virtualization.framework-backed execution;
- a materially restricted generated-code/runtime profile;
- disclosed remote microVM execution; or
- an external release with no arbitrary generated-code execution.

The decision needs filesystem/network escape tests, performance and package-size measurements, update and recovery behavior, and understandable user disclosure.

### Supply chain, encryption, backup, and update trust

Lockfiles improve reproducibility but do not make dependencies trustworthy. The implementation still needs qualified resolver ownership, registry/source allowlists, pnpm lifecycle-script policy, Python build/native-extension policy, provenance and vulnerability checks, and explicit dependency-denial behavior.

Before users rely on local-only data, the product also needs a tested encryption key hierarchy, consistent backup/restore across control data, App Resources, Artifacts, packages, and Keychain references, plus updater signing-key rotation, rollback authorization, partial-update recovery, and runtime-profile compatibility.

### Performance and usability budgets

The runtime profile must turn "finite" into measured targets for shell/Core readiness, Task first progress and completion, Build-to-preview time, App cold start, idle memory, installer/toolchain size, dependency staging, disk growth, and restart/recovery. The blueprint correctly leaves the numbers to evidence; the gate itself is no longer optional.

### UX evidence

The reusable-App wireframes remain useful for shell composition, but they are not proof of the differentiating Assistant/Task experience. Before implementation sign-off, prototype and test Workspace start, disposition, Task pre-run review, running/waiting, result/evidence, retry/revision, searchable history, and `Make reusable` promotion.

## Ordered next evidence

`../delivery/Delivery Checklist.md` is the sole live work list. At a high level, its order is:

1. accept the Task execution contract and bundled local-platform protocol;
2. prove packaged Host/Core IPC, restart, event, worker, and parser-helper boundaries;
3. complete the Assistant/Task path with a fake model;


**File Breadcrumb:** `Users > kshah > Documents > Alpha Agent Context > alpha-2026-09-21-7491970b54bc > alpha > research > Independent Architecture Review 2026-09-21.md > # Independent Product and Architecture Review — Reconciled Assessment > ## Ordered next evidence`

1. accept the Task execution contract and bundled local-platform protocol;
2. prove packaged Host/Core IPC, restart, event, worker, and parser-helper boundaries;
3. complete the Assistant/Task path with a fake model;
4. pass the internal v0.0 deterministic App lifecycle;
5. qualify real DeepSeek and OpenCode adapters;
6. complete breadth, recovery, performance, and UX evidence;
7. choose the external generated-code envelope before sensitive-data or broader testers.

This sequence is not a separate plan. It summarizes the canonical checklist and exists here only to preserve the review's rationale.

## Final conclusion

The project is not architecturally confused; it is ambitious and unusually disciplined. The answer/Task/App model, authority boundaries, local/cloud semantics, recovery model, and long-term second-brain direction form a credible foundation.

The honest verdict is still conditional. The opportunity is real, but the product has not yet proved usefulness, speed, comprehension, trust, or repeat use. Success depends less on adding architecture and more on refusing to skip the narrow evidence gates. If the team attempts to implement the full portable catalogue as v0, scope and security will dominate. If it proves the Task-first loop, one deterministic App, real Builder behavior, and an explicit external trust envelope in that order, the existing foundation is strong enough to continue.

## External technical references

These references informed the dated review; verify current platform behavior before implementation:

- [Tauri: Embedding External Binaries](https://v2.tauri.app/develop/sidecar/)
- [Tauri: Capabilities and security boundaries](https://v2.tauri.app/security/capabilities/)
- [Tauri: macOS code signing and notarization](https://v2.tauri.app/distribute/sign/macos/)
- [Apple: App Sandbox](https://developer.apple.com/documentation/security/app-sandbox)

