# Specifications Index

Status: Canonical
Last updated: 21 September 2026

## Purpose

This area contains the implementation contract for Assistant-led Task execution plus portable App packages, Releases, generated interfaces, Capabilities, Runs, and Builder integration. `Current Release Specification.md` defines what is being implemented now. Detailed contracts, schemas, examples, invalid fixtures, and executable proofs support it.

## Current contract versions

| Contract | Version | Status | Responsibility |
|---|---|---|---|
| App Contract | 0.1 revision 5 | Accepted | Portable Source App Manifest |
| Package Layout | 0.1 revision 3 | Accepted | Source package, sealed Version, index, locks, provenance, and validation |
| Resolved App Manifest | 0.1 revision 4 | Accepted | Deterministic compiler output and execution requirements |
| Release Resolution Record | 0.1 revision 5 | Accepted | Local/cloud target plus concrete Resources, Connections, runtime, schedule, policy, and limit bindings |
| Capability Protocol | 0.1 revision 6 | Accepted | Governed operations, approval, idempotency, budgets, evidence, and receipts |
| HTTP Action Profile | 0.1 revision 2 | Accepted | Reviewed bounded HTTP operation family |
| Run Event Kernel | 0.1 revision 3 | Accepted | Ordered Run state and evidence ledger |
| App UI Bridge | 0.1 revision 3 | Accepted | Scoped generated-interface interaction; v0 activates one React/Vite Surface path plus trusted fallback |
| Builder Harness Interface | 0.1 | Accepted; adapters qualifying | Portable Builder lifecycle, qualification gates, and package handoff |
| Local Automation and Platform Extension Profile | 2 | Accepted scope and manual-retrigger/window-close policy; detailed wire payloads and remaining semantics pending | First-release scheduling/browser, native-platform boundaries, extensibility, and acceptance gates |

## Folder structure

| Folder | Contents |
|---|---|
| `contracts/` | Normative Markdown contracts and JSON Schemas |
| `examples/` | Valid Source, Resolved, Release, Capability, Bridge, and Run examples |
| `fixtures/` | Invalid structural and semantic mutation sets |
| `proofs/` | Executable adaptor or contract proofs |

When implementation begins, machine-readable schemas, examples, invalid fixtures, and proofs move into the monorepo's versioned `packages/contracts/` tree defined by `../architecture/Implementation Blueprint.md`. This library index remains the human entrypoint and records the tagged implementation source; it must not retain a divergent second copy.

## Current Release entrypoint

Read `Current Release Specification.md` before implementing individual contracts. The first slice activates only a subset of the broader contract surface:

- Assistant request disposition to answer, one-off Task, or reusable App;
- local Task execution from typed text and deliberately selected files through a fixed platform profile, with non-trivial parsing isolated in a registered resource-bounded helper;
- Task revisions, Attempts, output Artifacts, evidence, retry, and promotion lineage;
- local deployment;
- real generated code in the selected Python 3.13/FastAPI plus optional React/Vite managed runtime profile;
- manual Runs and locally scheduled Jobs;
- general Playwright/Chromium browser operations, protected authenticated profiles, takeover and recovery;
- minimal App-scoped table CRUD/filter/cursor and Artifact-backed file Resources;
- selected files;
- remote models and the existing qualified HTTP/API profile, without limiting browser work to site-specific connectors;
- one React/TypeScript/Vite generated Surface path or trusted fallback through the App UI Bridge; native-view declarations remain inactive in v0;
- Version, Release, Activity, correction, and rollback.

Local schedules and general browser automation are first-usable-release scope under `Local_Automation_and_Platform_Extension_Profile.md`; their exact payloads and policies are still implementation gates. Desktop control, cloud deployment, public webhook ingress, observation, broad memory, and autonomy remain later. The internal v0.0 milestone may remain manual. Shared Core checks include Windows early; Windows-native release is later.

## Immediate contract gap

The accepted App contracts do not model a one-off Task because App Runs are correctly bound to an App Version, Release, and Entrypoint. Before implementing `Do once`, define and accept a Task and Task Attempt contract covering:

- immutable Task Revision and selected-input identity;
- resolved execution snapshot and profile version;
- Attempt state and ordered event ledger;
- model and tool routes, authority, policy, budgets, and placement;
- human input, cancellation, timeout, retry, outputs, Artifacts, evidence, and cost;
- promotion lineage without authority transfer;
- any explicit Task profile of protected-operation behavior.

Do not generate a hidden App or forge Release identity to close this gap. The contract should share terminology and implementation primitives with the Run Event and Capability contracts where semantics truly match, while remaining independently identifiable in v0.

The repository paths, generated-type locations, version registry, and validation gates for this contract are fixed by `../architecture/Implementation Blueprint.md`; the remaining work is the normative Task semantics and fixtures, not another repository-design exercise.

## Immediate internal protocol gaps

Before the trusted-skeleton implementation, define and accept one versioned `local-platform-protocol` bundle containing the Core IPC, Host-control, and worker-bootstrap schemas, with complete examples, invalid fixtures, compatibility behavior, size and deadline limits, authentication fields, error envelopes, and lifecycle tests. The three surfaces ship atomically in v0 rather than creating an internal compatibility matrix. This is a repository-owned internal contract defined by the implementation blueprint, not a portable App-package contract or another library specification layer.

## Immediate automation contract gaps

Before enabling local schedules, complete the cadence/timezone schema, occurrence identity/claim and exact Release semantics, manual-retrigger payloads/lineage and historical-input handling, overlap/offline behavior, pause/revocation, recovery, and state examples. The accepted behavior shows missed jobs for later user-initiated retriggering without automatic catch-up, and keeps automation running after window close. Existing schedule settings examples are illustrative and cannot override that policy.

Before enabling the BrowserProvider, complete typed general operations, Connection/session handles, profile locks/sharing, sign-in/takeover/resume messages, destination/egress/effect rules, evidence redaction, file-transfer boundaries, errors, and invalid fixtures. Reuse the Capability and Run contracts; do not invent new Run states or pass Playwright objects through the SDK.

Existing machine-readable App/Release/Capability shapes already reserve generic capabilities, Connections, and schedules. This scope revision does not change their schemas or prove provider conformance. The internal protocol must add the registered browser worker through its next accepted bundle definition.

## Prototype implementation and evidence

`../delivery/Prototype_Scope_and_Acceptance.md` maps these contracts to staged implementation and acceptance IDs. `../delivery/AI_Coding_Agent_Playbook.md` requires independent fixture expectations, executable checks, exact source versions and explicit blocked/not-run evidence. Neither document defines new wire fields. Task and local-platform contracts are P0 work; scheduler/browser payloads must be complete before their P5 activation.

## Validation expectations

A contract is implementation-ready only when it has:

1. normative behavior and field definitions;
2. a strict structural schema where appropriate;
3. at least one valid complete example;
4. invalid examples and expected error behavior;
5. state, authentication, security, and compatibility rules;
6. executable structural and semantic validation;
7. contract tests for provider adapters.

JSON, YAML, and JSONL parsing alone is not semantic validation.

## Planned specifications

Create these only when their phase begins. Accepted portable App contracts may retain inactive cross-phase vocabulary, but that vocabulary is not an active runtime promise:

- local process/runtime provider interface;
- cloud worker and Device Bridge contracts;
- Resource and Context wire contracts beyond current manifest shapes;
- Observation payload schemas;
- Memory Claim and Procedure contracts;
- typed cross-App interfaces.

Task/Attempt, scheduler, and BrowserProvider contracts are immediate current-release work and are excluded from the deferred list above. Do not design other future schemas merely to make the document set appear complete.
