# Run Event Kernel

Specification version: 0.1, revision 3
API version: `alpha.platform.run-events/v0.1`
Status: Accepted design baseline
Last updated: 16 September 2026

## Purpose

The Run Event Kernel defines the minimum append-only evidence needed to operate the first complete platform slice:

`Invoke → Execute → Wait for approval or input when required → Produce output → Verify outcome → Inspect → Correct`

It is deliberately a kernel rather than a general telemetry system. It records stable platform facts from the Runner, Capability Broker, Resource service, model service, evaluators, scheduler, and control plane. Logs, traces, screenshots, model payloads, provider details, and large outputs remain referenced Artifacts or protected evidence.

## Scope

Revision 3 covers:

- Run identity and immutable execution inputs.
- Ordered execution-state transitions.
- Normalized product milestones.
- child, retry, replay, and repair relationships.
- exact Context selections.
- model calls and usage.
- managed Resource operations.
- inline and durable Capability operations.
- approval requests and decisions.
- structured human-input requests and responses.
- budget reservation, charge, settlement, and release.
- Artifacts and evidence.
- structured errors and retry classification.
- outcome verification independent of execution state.

It does not define Build events, general distributed tracing, custom App events, metrics aggregation, Resource contents, Capability wire records, or long-term analytics schemas.

## Governing principles

1. The ledger is append-only. Corrections create new Events; they never rewrite earlier Events.
2. Every Event belongs to one Run.
3. The ledger assigns one strictly increasing `sequence` per Run. Sequence, not timestamp, is authoritative for ordering.
4. Producers supply an idempotent source Event identity. Retrying ingestion cannot duplicate a logical Event.
5. Events store typed facts and immutable references. They do not store credentials, authority tokens, raw secrets, or unrestricted provider payloads.
6. Execution state and outcome verification state remain independent.
7. A terminal Run state cannot transition to another state. Retry, replay, and repair create related Runs; they never rewrite history.
8. Mandatory authority, approval, budget, lifecycle, and error facts cannot be removed by App observability settings.
9. Ordinary users consume platform-derived timelines and summaries. Generated Apps cannot author trusted audit summaries.
10. Large or sensitive content is stored as an Artifact or protected evidence and referenced by digest.
11. Human input and approval remain separate: an input response cannot grant authority, widen a budget, or change a Release.

## Event envelope

Every Event validates against `run-event.schema.json` and contains:

| Field | Meaning |
|---|---|
| `apiVersion` | Exact Event API version |
| `eventId` | Ledger-assigned immutable Event identity |
| `runId` | Run that owns the Event |
| `sequence` | Strictly increasing Run-local order |
| `observedAt` | When the source observed the fact |
| `recordedAt` | When the ledger durably recorded it |
| `type` | Registered Event type |
| `visibility` | `user`, `operator`, or `restricted` projection class |
| `source` | Trusted producer plane, service, and idempotent source Event identity |
| `correlation` | Optional Component, Capability operation, model call, Resource operation, approval, parent Event, or worker lease references |
| `payload` | Type-specific facts |

`observedAt` may precede `recordedAt`. User-facing order always follows `sequence`. Clocks are not used to resolve concurrent producer order.

## Source identity and ingestion

The ledger accepts Events only from authenticated platform services. Generated code can cause facts through the SDK, but it cannot assign trusted Event types or write directly to the ledger.

The tuple `(source.service, source.sourceEventId)` is idempotent. Reuse with identical canonical content returns the existing Event. Reuse with different content fails as `RE_SOURCE_EVENT_CONFLICT`.

The ledger assigns `eventId`, `sequence`, and `recordedAt`. A producer supplies `observedAt`, `type`, `visibility`, `correlation`, and `payload`.

## Run execution state

The accepted states are:

`queued | running | awaiting-approval | awaiting-input | succeeded | failed | cancelled | timed-out`

Allowed transitions are:

| From | To |
|---|---|
| `queued` | `running`, `cancelled`, `timed-out` |
| `running` | `awaiting-approval`, `awaiting-input`, `succeeded`, `failed`, `cancelled`, `timed-out` |
| `awaiting-approval` | `running`, `failed`, `cancelled`, `timed-out` |
| `awaiting-input` | `running`, `failed`, `cancelled`, `timed-out` |

`succeeded`, `failed`, `cancelled`, and `timed-out` are terminal. A Run resumed after approval or input remains the same Run and receives a new worker lease; it does not depend on the suspended worker remaining alive. Retrying a terminal Run creates a new Run with an explicit `retry-of` relationship.

## Outcome verification state

Outcome verification is:

`not-evaluated | passed | failed | needs-review`

A Run may be `succeeded` while its outcome is `failed`, `needs-review`, or `not-evaluated`. Execution reaches a terminal state independently; outcome evaluation may complete later and append an allowed post-terminal Event. Evaluators may be schema, deterministic, model, human, or policy based. An outcome transition references the evidence used.

## Registered Event types

| Type | Required fact |
|---|---|
| `run.created` | Exact App Version, Release resolution, Run projection, principals, trigger, and input identity |
| `run.state.changed` | Valid execution-state transition and reason |
| `run.milestone` | Normalized phase and progress state for product UI |
| `run.related` | Parent, child, retry, replay, or repair relationship |
| `context.selected` | Exact permitted Context revision and digest actually used |
| `model.call` | Model route, lifecycle, usage, cost, and content digests without raw prompts |
| `resource.operation` | Managed Resource action, lifecycle, affected count, and change evidence |
| `capability.operation` | Broker operation lifecycle, authority/effect identity, provider evidence, and receipt |
| `approval.requested` | Exact approval scope, digests, material-facts reference, and expiry |
| `approval.decided` | Approver, decision, scope, exact digests, and decision identity |
| `human-input.requested` | Typed question identity, safe explanation, response-schema digest, requesting Component, and expiry |
| `human-input.received` | Responding Principal, validated response digest, authorized Artifact references, and receipt time |
| `budget.changed` | Reservation, charge, settlement, release, and remaining amount by dimension |
| `artifact.recorded` | Immutable content identity, media type, size, role, and retention class |
| `evidence.recorded` | Evidence kind, subject, Artifact reference, and content digest |
| `outcome.changed` | Independent outcome state, evaluator, evidence, and reason |
| `run.error` | Stable code, safe message, phase, retryability, and protected details reference |

## Normalized milestones

Milestones use four broad phases:

- `prepare`
- `execute`
- `validate`
- `finalize`

Their state is `started`, `completed`, or `blocked`. An optional `componentRef` connects a milestone to one resolved Component. The platform may derive user text such as “Reading sources” or “Checking results” from the App, Component kind, and milestone; App code does not write trusted audit prose.

## Capability operation projection

`capability.operation` projects the accepted Capability Protocol into the Run ledger. Its states are:

`accepted | authorized | waiting-approval | executing | completed | denied | failed | cancelled | replayed`

The Event references the authoritative Broker operation and receipt rather than duplicating the full wire record. It records:

- Capability reference, registered name, definition digest, and registry-owned execution mode.
- Release resolution digest.
- authorization and effect digests once calculated.
- provider binding and exact deployment evidence once selected or invoked.
- result digest, terminal receipt reference, or structured error fact.

Approval and budget Events remain separate so they can be queried and projected without interpreting Broker-specific payloads.

## Human input suspension

An adaptive Run may request structured human input when it encounters a material ambiguity that cannot be resolved safely from its declared inputs or permitted Context.

v0 permits one active human-input request per Run. The trusted Run service records `human-input.requested`, moves the Run from `running` to `awaiting-input`, releases the worker lease, and presents the state to the user as `Waiting for you`. The response is validated against the pinned response-schema digest, authorized against the App and Run, recorded as `human-input.received`, and used to resume the same Run under a new fenced worker lease.

Human input is not approval. A response cannot grant a Capability, widen authority, increase a budget, change a Release, override policy, or substitute for a trusted approval. If the request expires, the responding user loses access, the Release is revoked, or the Run is cancelled, Run Control resolves the request through normal policy without retaining worker compute.

## Model and Resource operations

`model.call` records a bounded model invocation. Raw prompts, chain-of-thought, and provider credentials are never Event payloads. Input and output digests, approved evidence references, token usage, cost, route, and provider deployment are sufficient for v0 reconstruction and cost inspection.

`resource.operation` records changes to platform-managed tables and file stores required by the walking slice. Record-level contents remain in the Resource. Change sets, snapshots, or exported rows are referenced as Artifacts when evidence or rollback analysis requires them.

## Artifacts and evidence

An Artifact is immutable stored content. Evidence is the claim that an Artifact or digest supports a Run, operation, decision, output, or error.

- `artifact.recorded` proves content identity and storage metadata.
- `evidence.recorded` links evidence to a subject such as a Run, Capability operation, record, validation, or model call.

An evidence Event must not imply that referenced content is safe for every viewer. `visibility`, Workspace classification policy, and Artifact access checks still apply.

## Budgets and costs

v0 budget dimensions match the Release Resolution Record:

- `modelCalls`
- `browserSeconds`
- `capabilityCalls`
- `costMicrousd`

Every change records one action (`reserved`, `charged`, `settled`, or `released`), a non-negative amount, and the remaining Run balance. Capability receipts and model usage remain the authoritative sources for the charge; the ledger Event is their normalized projection.

## Run relationships

Relationships are explicit rather than inferred from matching inputs:

- `child-of` — subordinate work created by another Run.
- `retry-of` — another Run retries a failed or timed-out Run.
- `replay-of` — another Run intentionally re-executes recorded inputs.
- `repair-of` — a diagnostic or repair Run relates to a failed Run.

The related Run must exist in the same Workspace. Cross-Workspace relationships are invalid in v0.

## Visibility and redaction

| Visibility | Intended projection |
|---|---|
| `user` | Safe for authorized App users and ordinary Run inspection |
| `operator` | Operational detail available to permitted Workspace operators |
| `restricted` | Security, credential-generation, policy, or protected diagnostic evidence |

Visibility does not replace authorization. The API applies Workspace, App, Run, Artifact, and evidence policy before returning an Event. Secret-shaped fields are prohibited even in `restricted` Events; protected material is referenced, not embedded.

## Derived read models

The ledger is the evidence source, not the direct product interface. v0 derives:

1. **Run summary** — execution state, outcome state, elapsed time, cost, outputs, and next action.
2. **User timeline** — milestones, approvals, important operations, outputs, and errors.
3. **Access and action view** — Capabilities used, targets, approvals, and receipts.
4. **Cost view** — budget reservations, actual usage, and remaining limits.
5. **Technical trace** — Components, worker leases, providers, related Runs, and protected diagnostics.

Read models can be rebuilt from the ledger plus referenced control-plane records.

## Validation rules

In addition to JSON Schema validation, the ledger enforces:

1. `runId` exists and belongs to the authenticated Workspace.
2. `run.created` is the first Event and establishes the initial `queued` state.
3. source Event identity is unique or canonically identical.
4. `run.state.changed` follows the allowed transition table.
5. no Event is appended after terminal state except evidence, Artifact, relationship, outcome, and delayed accounting Events explicitly tied to prior work.
6. Context, Component, Capability, Resource, provider, Release, and App Version references belong to the Run projection.
7. approval digests and operation identity match the Capability operation.
8. a human-input response matches one active request, comes from an authorized Principal, validates against the pinned response schema, and cannot carry an authority decision.
9. budget changes cannot make remaining balance negative.
10. Event payloads contain no credentials, authority tokens, raw secrets, or undeclared opaque provider payloads.
11. `observedAt` and `recordedAt` are valid UTC instants; sequence remains authoritative.

## Standard errors

| Code | Meaning |
|---|---|
| `RE_SCHEMA_INVALID` | Event fails the structural schema |
| `RE_RUN_NOT_FOUND` | Run does not exist or is outside the authenticated Workspace |
| `RE_SOURCE_UNTRUSTED` | Producer is not authorized for this Event type |
| `RE_SOURCE_EVENT_CONFLICT` | Source Event identity was reused with different content |
| `RE_SEQUENCE_INVALID` | Run-local Event sequence is missing, duplicated, or out of order |
| `RE_STATE_TRANSITION_INVALID` | Execution-state transition is not permitted |
| `RE_TERMINAL_RUN_CLOSED` | Event type is not allowed after terminal execution |
| `RE_REFERENCE_OUTSIDE_PROJECTION` | Referenced object is not in the Run projection |
| `RE_APPROVAL_MISMATCH` | Approval identity or digest differs from the operation |
| `RE_HUMAN_INPUT_MISMATCH` | Human input does not match one active request or its pinned schema |
| `RE_HUMAN_INPUT_UNAUTHORIZED` | Responding Principal is not authorized for the App and Run |
| `RE_BUDGET_INVALID` | Budget Event conflicts with the finite Run balance |
| `RE_SECRET_MATERIAL_REJECTED` | Event contains prohibited secret material |

## Canonicalization and retention

Events use Unicode NFC and RFC 8785 canonical JSON. Digests are lowercase SHA-256 prefixed by `sha256:`. The ledger retains the canonical Event bytes and Event API version.

Retention follows Workspace policy but must preserve the minimum audit facts required by an active Release and its regulatory or contractual obligations. Deleting an Artifact may leave a tombstoned evidence reference and digest; it does not rewrite the historical Event.

## Reference files

- `run-event.schema.json` — strict schema for one Event.
- `../examples/reference-run-events.jsonl` — one complete approval-gated Run timeline.
- `../examples/reference-run-human-input-events.jsonl` — one complete adaptive Run suspension and resume timeline.
- `../fixtures/run-event-invalid-fixtures.yaml` — structural and semantic failure cases.

## Explicit deferrals

- Build-event schema and Builder token streaming.
- OpenTelemetry trace and span mapping.
- App-authored custom Events.
- public analytics and user-defined metrics.
- full Resource change-data capture.
- general workflow-step taxonomy.
- cross-Workspace or marketplace audit exchange.
- cryptographic ledger anchoring and external notarization.

These are added only when an implementation or product requirement exercises them.
