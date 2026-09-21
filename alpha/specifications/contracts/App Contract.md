# App Contract

Specification version: 0.1, revision 5
API version: `alpha.platform/v0.1`
Status: Accepted design baseline
Last updated: 21 September 2026

Revision 5 separates verified webhook payloads from typed Entrypoint input, fixes v0 ingress to authenticated JSON `POST`, makes at-least-once delivery explicit, and clarifies that HTTP Action Profiles authorize bounded request families rather than literal calls or broad API access. It does not expose generated servers, public App routes, or Builder-certified risk. The 18 September scope clarification does not change the schema: this contract governs one durable execution artifact inside the broader agentic workspace, not observation capture or the entire second-brain product model.

`alpha.platform/v0.1` is the portable App-package API version, not a promise that every shape is active in the first product release. The first usable runtime profile includes manual/scheduled Entrypoints, minimal table/file Resources, the existing qualified HTTP route, general browser Capabilities with protected Connections, Python handlers, and an optional React/Vite Surface or trusted fallback. The exact scheduler/browser payloads and execution policies still require qualification under `../Local_Automation_and_Platform_Extension_Profile.md`. Webhooks, agent Components, Context requests, native-view Surfaces, and generic authenticated/write HTTP remain inactive. Browser operations use Capabilities; this revision adds no browser Component kind.

## Purpose

The App Contract is the stable boundary between an open-ended AI Builder and the managed platform. It lets the Builder create broad applications while giving the platform enough information to validate, package, preview, publish, execute, govern, observe, modify, and roll back them consistently.

Text, files, and future screen, voice, browser, watch-session, or connected-source inputs enter through trusted platform input and Context boundaries. They are not App Manifest fields and do not grant runtime authority. The Assistant or Builder may use approved input evidence to propose an App, but the resulting package still passes through this contract and the normal Version, Release, Grant, Run, and Capability lifecycle.

This revision retains the portable source declarations exercised across the accepted current and future breadth fixtures:

1. Website monitoring.
2. File or invoice reconciliation.
3. Assisted outreach with human approval before external action.
4. Authenticated event capture through platform-managed webhook ingress.
5. A reviewed generic HTTP write to an unfamiliar API without a bespoke connector.

Only the subset named by `../Current Release Specification.md` is implementation scope now. Broader fixtures preserve compatibility and negative-test evidence. Local schedules and browser Capabilities are now first-release obligations; webhook, Context, native-view, and generic write shapes remain inactive. Old schedule values and native-view examples are not executable release defaults.

The keywords MUST, MUST NOT, SHOULD, SHOULD NOT, and MAY describe normative requirements.

This small source vocabulary is not a connector catalogue. A generic governed HTTP or browser Capability can integrate an unfamiliar external system without adding a domain-specific manifest primitive or dedicated connector. Unrestricted raw network access remains prohibited.

## Governing principles

1. Builders author a concise portable Source App Manifest at `app.yaml`.
2. The platform compiler creates an explicit canonical Resolved App Manifest at `app.resolved.json`.
3. Production executes only a sealed App Version and its resolved manifest.
4. A Release binds the portable version to Workspace Resources, Connections, Grants, configuration, policies, and runtime providers.
5. Capability declarations request authority; they never grant authority.
6. The source contract contains logical needs, not credentials, production values, provider identities, or mutable data.
7. Unknown fields are rejected. Namespaced extensions and App-to-App exports are deferred from this revision.
8. v0 Apps are available only to authenticated Workspace members.
9. Backend Components use Python 3.13. Custom interfaces are written in TypeScript and compiled to isolated browser bundles.
10. Safe preview execution may begin automatically, but it cannot imply publication authority or permission for consequential external effects.
11. Breadth comes from custom code, custom interfaces, and governed generic I/O. New domain APIs do not require new top-level manifest fields.
12. Input adapters, Observation capture, raw-memory storage, and capture permissions remain platform concerns outside the App package. An App may later request a typed capture-related Capability only if a future contract explicitly introduces one.

## What revision 5 excludes

The previous draft exposed fields that are not needed by the accepted journey. They are removed from the Source App Manifest rather than retained as speculative options.

| Removed source concept | Reason |
|---|---|
| Builder-authored service-provider requirements | The compiler derives runtime, Capability client, and UI host requirements from Component kinds; Releases bind providers |
| `workflow` Component | Deterministic v0 orchestration can run in Python until a separate workflow engine is justified |
| General event-bus, API, App-to-App, and agent-task invocation kinds | They are not required by the accepted v0 journey |
| Anonymous ingress, synchronous generated responses, and public routes | v0 webhooks are authenticated event sources owned by the platform, not generated servers |
| Object store, index, queue, key-value, Workspace Resources, and browser-profile Resources | Tables and file stores cover the fixtures; browser identity is a Connection |
| Autonomy presets | Access and approval are expressed per Capability; one broad preset obscures authority |
| Conditional approval language | `always` and `first-use` cover the accepted fixtures; richer conditions belong in the Capability Protocol |
| Custom metrics and App event declarations | Mandatory Run events and evidence cover the walking slice |
| App-to-App exports | Explicitly outside the first slice |
| General namespaced extensions | Deferred until a real extension cannot be represented by the core |
| Builder-declared effect classes | The compiler derives effects authoritatively from Capabilities and Resource modes |
| Keyed concurrency and checkpoint controls | Not required to prove the first lifecycle |
| Context writes and project, agent, run, or external Context scopes | The fixtures require only bounded reads from user, Workspace, or App Context |

These concepts may return in later contract revisions. Their absence from v0.1 is not a rejection of the long-term architecture.

## Contract layers

### Source App Manifest

The Builder-authored portable declaration. It defines the App's identity, Components, user surfaces, Entrypoints, logical state, external Connections, requested Capabilities, Context reads, approval requests, evidence needs, and tests.

It MUST NOT contain:

- Platform App, App Version, Release, Workspace, user, or provider identifiers.
- Raw secrets, tokens, cookies, private keys, or credential-shaped configuration.
- Workspace-specific Resource or Connection bindings.
- Actual configuration values or production data.
- Effective Grants, policy decisions, active schedules, or Release state.

### Resolved App Manifest

The platform compiler converts the source manifest into a canonical `app.resolved.json`. It MUST:

- Materialize every default and fixed v0 policy.
- Resolve registry metadata for Capabilities, Connections, SDKs, and Component kinds.
- Derive authoritative effects, risk classes, approval minima, runtime requirements, and service-interface requirements.
- Verify all logical references and package paths.
- Record exact Component and dependency-lock digests.
- Preserve logical Resource, Connection, Context, and provider references without adding Workspace bindings.
- Record the compiler version and registry snapshot used.

The same valid source package, compiler version, and registry snapshot MUST produce identical resolved bytes. Builders MUST NOT edit the resolved manifest. Runtime MUST NOT infer omitted source defaults.

### App Version record

After validation, the platform seals the package and creates an immutable App Version containing at least:

| Field | Meaning |
|---|---|
| `app_id` | Stable platform identity |
| `app_version_id` | Immutable version identity |
| `parent_version_id` | Parent version when modifying or repairing |
| `source_manifest_digest` | Digest of canonical parsed `app.yaml` |
| `resolved_manifest_digest` | Digest used by execution |
| `package_digest` | Digest of complete sealed package |
| `contract_version` | Contract version used for validation |
| `compiler_version` | Exact compiler version |
| `registry_snapshot_id` | Registry metadata used for resolution |
| `created_by` | Principal and Build identity |
| `validation_set_id` | Exact test and validator result set |
| `created_at` | Platform timestamp |

### Release binding

A Release selects one App Version for `preview` or `active` use and binds:

- Workspace and environment.
- Configuration revision.
- Logical Resources to managed Resource identities.
- Logical Connection requirements to Workspace Connections.
- Context selectors to permitted Context Sources.
- Capability Grants and approval policy.
- Runtime and model providers.
- Budgets, concurrency limits, and schedule values.
- Webhook endpoint identities, verification profiles, replay policy, and ingress providers.
- Approved HTTP Action Profile revisions for eligible generic writes.

Preview Releases MUST use reduced authority and test data or explicitly approved sample access. Moving to an active Release MUST revalidate all changed bindings, permissions, tests, and package compatibility.

## Required package structure

Only referenced files are required:

```text
app.yaml
schemas/
components/
ui/
agents/
tests/
assets/
...
```

The platform adds `app.resolved.json` while sealing the package.

Every path MUST be relative to the package root, use forward slashes, remain inside the package, and point to immutable package content. Absolute paths, `..`, backslashes, device names, and symbolic-link escapes are invalid.

## Top-level manifest

```yaml
apiVersion: alpha.platform/v0.1
kind: AppManifest
metadata: {}
spec: {}
```

Only these four fields are allowed.

### `metadata`

Required portable identity:

| Field | Required | Meaning |
|---|---|---|
| `name` | Yes | Stable lowercase package name |
| `displayName` | Yes | User-facing name |
| `description` | Yes | Plain-language outcome |
| `labels` | No | Non-authoritative discovery metadata |

## Source `spec`

Required sections are `compatibility`, `components`, `entrypoints`, and `tests`. All other sections may be omitted and compile to empty or fixed defaults.

### Source defaults

Defaults are contract behavior and MUST be materialized by the compiler:

| Omitted source field | Resolved declaration |
|---|---|
| `configuration` | `null` |
| `surfaces`, `triggers`, `resources`, `connections`, `capabilities`, or `context` | Empty array |
| `policies` | No requested approvals plus the fixed v0 policies below |
| `observability` | No additional evidence capture or redaction |
| Entrypoint `capabilities`, `resourceAccess`, or `context` | Empty array |
| `execution.retry` | One attempt with `none` strategy |
| `execution.concurrency` | `singleton` |
| `execution.budgets` | No App-specific requested ceiling; an explicit effective Release budget is still required |

The compiler also materializes `enabled: false` for every source Trigger and `scope: app` plus `lifecycle: retain` for every source Resource. Changing a default that affects behavior requires a compatible contract revision or new API version.

### Compatibility

`compatibility.sdk` declares the Platform SDK range required by the package. The `apiVersion` already declares contract compatibility, so a duplicate platform API range is not authored.

Release activation MUST fail if the SDK, fixed Component runtime, or contract version is unsupported.

### Configuration

`configuration` may reference:

- `schema`: JSON Schema for user-editable configuration.
- `uiSchema`: Optional platform-native presentation hints.
- `defaults`: Optional safe defaults.

The section is optional. Actual values live in a versioned Release configuration revision. Secret values are forbidden and MUST be represented as Connection requirements.

### Components

Components are implementation units. v0.1 supports:

| Kind | Purpose | Compiler-derived runtime |
|---|---|---|
| `handler-bundle` | Deterministic backend logic and orchestration | Python 3.13 worker and Capability client |
| `agent` | Bounded reasoning or drafting step | Release-bound model runner and Capability client |
| `native-view` | Declarative interface built from platform components | Platform native UI host |
| `micro-frontend` | Custom App interface | Compiled TypeScript bundle in browser isolation |

Every Component declares `id`, `kind`, and `source`. `handler-bundle` and `micro-frontend` Components MUST also declare `dependencyLock`. Agent and native-view Components are declarative package content and do not require dependency locks.

Components do not select concrete runtimes, model providers, Capability clients, or UI hosts. The compiler derives typed service requirements and the Release binds approved providers. Components MUST NOT import one another through hidden filesystem paths.

A micro-frontend accesses the platform only through the App UI Bridge. It MUST NOT receive direct network access, credentials, database handles, or control-plane clients.

### Surfaces

Surfaces declare App-owned interface routes. An App may have no Surface when it operates entirely through background Runs and notifications.

Supported kinds are:

- `native-page`
- `micro-frontend`

Every Surface declares `id`, `kind`, `componentRef`, `title`, and an App-relative `route`. It may list Entrypoints and Resources available through that surface.

Apps may declare several routes and their own internal navigation. Activity, Access, Configure, and Versions are platform-owned controls and MUST NOT be declared or impersonated by App Surfaces.

### Entrypoints

Every Run begins from one Entrypoint against one exact App Version. Supported kinds are:

- `action`: user-initiated work that may change state or request an effect.
- `query`: read-only retrieval for an interface or Builder interaction.
- `job`: longer work that may be started manually or by schedule.

Each Entrypoint declares:

- `id`, `kind`, `componentRef`, and `handler`.
- Input and output JSON Schema paths.
- Allowed invocation channels: `ui`, `chat`, `manual`, `schedule`, or `webhook`.
- Capability, Resource, and Context references.
- Execution timeout and optional retry, concurrency, and budget requests.
- Idempotency behavior.
- Outcome evaluation and human-review behavior.

Only `handler-bundle` and `agent` Components may implement Entrypoints. A `query` MUST NOT request write Resource modes or consequential Capabilities. A scheduled Entrypoint MUST be a `job`, include `schedule` in `invocation`, and use `occurrence-key` idempotency. A webhook Entrypoint follows the same `job` and `occurrence-key` rules and includes `webhook` in `invocation`.

Execution state and outcome state are separate. `humanReview` controls outcome review, not authorization for an external effect. Capability approval remains separately enforced.

### Triggers

v0.1 supports `schedule` and authenticated `webhook` Triggers. Every Trigger targets exactly one `job` Entrypoint. Source Triggers are templates and the compiler fixes them as disabled; only a Release may activate them.

A schedule Trigger declares a settings schema for user-editable cadence, local time, and timezone. Each scheduled occurrence has a stable identity used for idempotency and safe retry.

A webhook Trigger declares:

- plain-language `purpose`;
- a `payloadSchema` for the verified external JSON body;
- an `identity` or safe `declarative` normalization rule;
- the v0 method `POST` and media type `application/json`;
- a registered verifier and logical Connection reference;
- requested maximum payload bytes, event rate, and occurrence-deduplication window.

`identity` normalization requires the payload schema to equal the target Entrypoint input schema. `declarative` normalization references a package mapping that the trusted compiler validates against both schemas and the trusted ingress service evaluates without code execution, external access, models, or secret access. When a provider payload needs complex transformation, the Entrypoint may deliberately accept that validated payload and transform it inside the normal sandboxed Run.

The verifier is a registry-owned definition such as `webhook.hmac-sha256`; it is not executable code supplied by the Builder. Its Connection MUST exist, MUST carry a verification scope accepted by the connector definition, and MUST use `fail` or `disable-dependent-entrypoints` when unavailable. The trusted compiler resolves verifier metadata and the Release supplies the endpoint identity, verification profile, normalization binding, source constraints, timestamp tolerance, replay policy, quarantine policy, evidence policy, and ingress provider.

Ingress verifies, validates, normalizes, durably records one occurrence, acknowledges receipt, and only then requests a normal Run. Delivery is at least once. Provider delivery identity is preferred; a bounded payload digest may be used when no stable provider identity exists. Deduplication reduces repeats but is not an exactly-once guarantee, so handlers SHOULD remain idempotent. Generated code never executes in the internet request path. Endpoint URIs, verification secrets, delivery attempts, and mutable occurrence state never enter the source package.

### Resources

v0.1 supports App-scoped managed Resources:

| Kind | Purpose | Required kind-specific field |
|---|---|---|
| `table` | Structured records, drafts, exceptions, and history | `schemaRef` |
| `file-store` | Uploaded files and generated file artifacts | `acceptedMediaTypes` |

Every Resource declares `id`, `kind`, `schemaVersion`, and `classificationHint`. The compiler fixes scope to `app` and lifecycle to `retain`.

Within v0.1, updates may keep the schema unchanged or make backward-compatible additive changes. Breaking schema migrations and automatic data rollback are deferred and MUST block Release activation.

### Connections

A Connection is a logical requirement for external authentication or delivery. It declares:

- `id` and registered `connector` type.
- Requested connector scopes.
- Behavior when no approved binding exists.
- Plain-language purpose.

Allowed unavailable behavior is:

- `fail`: block the Release or invocation until a Connection is bound.
- `use-unconnected-mode`: continue through a connector-defined public or unauthenticated mode.
- `disable-dependent-capabilities`: keep the Entrypoint available, expose the Capability as unavailable through the SDK, and require the handler to continue without it.
- `disable-dependent-entrypoints`: keep the App active but disable Entrypoints that reference Capabilities dependent on the Connection.

The unavailable behavior completely defines whether a Connection is mandatory; a separate `required` flag is intentionally omitted. A Release maps the requirement to a Workspace-owned Connection. The App never receives the underlying credential.

### Capabilities

A Capability declaration contains `id`, registered `capability`, optional `connectionRef`, plain-language `purpose`, and capability-specific `constraints`.

The Capability registry defines request and result schemas, constraint fields, effect and risk classes, audit requirements, approval minima, and idempotency requirements. The compiler derives effect summaries from Capabilities and Resource access; the Builder does not classify its own risk.

The registry MUST include generic governed integration definitions such as HTTP request and browser interaction. A generic HTTP declaration may constrain destinations, methods, path patterns and parameters, query parameters, request fields, payload size, response size, rate, redirect behavior, and an optional `connectionRef`. The trusted provider or egress layer injects approved credentials and records evidence. A dedicated product-specific connector is not required merely because the destination API is new to the platform.

For an eligible recurring generic HTTP write, the trusted compiler may derive a portable HTTP Action Profile candidate from the exact Capability reference, Connection reference, purpose, normalized constraints, Capability definition digest, and profile-schema digest. The candidate represents one bounded family of requests, not one literal call or an entire API. Its digest does not grant authority and contains no Workspace binding. It lets Release resolution prove that a separately reviewed Workspace and App-scoped profile describes the same operation. The Builder may propose the underlying fields but cannot assign the authoritative effect class, risk, approval minimum, review decision, or trusted user-facing permission summary.

Registry policy may forbid generic access for high-risk effect classes or require a dedicated typed Capability where normalized targets, provider idempotency, specialised approvals, or stronger support guarantees are necessary.

Runtime authority is the intersection of platform policy, Workspace policy, environment policy, Release Grants, App Version declarations, Entrypoint references, Run limits, and user decisions. Any layer may narrow authority. No layer may widen it, and explicit denial wins.

### Context

v0.1 permits read-only declarations from `user`, `workspace`, or `app` Context. Each declaration contains `id`, `scope`, logical `selector`, plain-language `purpose`, whether it is required, and an optional maximum age.

The Release binds selectors to permitted Context Sources. Every Run records the exact Context Snapshot used. Context writes and other scopes are deferred.

### Policies

The Source Manifest may request Capability approvals only:

```yaml
policies:
  approvalRequests:
    - capabilityRef: email-send
      mode: always
```

Supported modes are `always` and `first-use`. A Capability registry or Workspace policy may require a stricter mode. The compiler also materializes these fixed v0 policies:

- `audience: workspace-members`
- `selfModification: propose-only`
- `directNetwork: false`

The App cannot relax them.

`directNetwork: false` prohibits raw sockets and direct outbound network access from generated workers. It does not prohibit the generic governed HTTP or browser Capabilities supplied through the Platform SDK.

### Observability

The platform always records Run lifecycle, Capability, authority, approval, cost, error, and artifact events. The source manifest may request additional evidence capture:

- `inputs`
- `outputs`
- `capability-results`
- `screenshots`

JSON Pointer redaction paths may be declared for allowed payload fields. Redaction MUST NOT conceal that an action occurred, who initiated it, when it occurred, its effect class, policy decision, or provider receipt.

### Tests and outcomes

Every package declares at least one test. Supported kinds are:

| Kind | Use |
|---|---|
| `unit` | Deterministic Component logic |
| `fixture` | Known input/output behavior |
| `outcome` | Domain-level acceptance evaluation |
| `health` | Post-Release operational health |

`requiredFor` may include `build`, `preview`, and `release`. Package schema, static, secret, policy, compatibility, and dependency checks are mandatory platform validation gates and are not repeated as Builder-authored tests.

Every App MUST declare at least one `fixture` or `outcome` test required for `preview`, and at least one `fixture`, `outcome`, or `health` test required for `release`. The same test may satisfy both requirements. A unit test alone can never justify a Preview or active Release.

Model-based or human outcome evaluation does not change a Run's execution state. A technically completed Run may remain `Not evaluated` or `Needs review`.

## Semantic validation

JSON Schema validates structure. The package service MUST additionally:

1. Verify identifier uniqueness in every declaration collection.
2. Resolve every Component, Entrypoint, Resource, Connection, Capability, Context, test, and package-path reference.
3. Enforce Component, Surface, Entrypoint, Trigger, Resource, retry, idempotency, and test kind rules.
4. For a webhook, require a `job` target, `webhook` invocation, `occurrence-key` idempotency, a valid payload-to-input normalization, an existing verifier Connection, and a registered compatible verifier.
5. Validate Capability constraints and connector scopes against the selected registry snapshot.
6. Derive authoritative effect, risk, audit, evidence, and minimum approval requirements.
7. Derive an HTTP Action Profile candidate only when a generic write's complete authority-neutral shape can be normalized; otherwise materialize no candidate.
8. Reject any Entrypoint that references authority not declared at App level.
9. Verify reproducible dependency locks and scan package contents.
10. Reject secrets, unsafe binaries, direct network behavior, path escapes, and hidden imports.
11. Verify that preview execution can be reduced to available test data and approved sample access.
12. Materialize fixed policies, service requirements, runtime profiles, defaults, and derived metadata.
13. Run mandatory platform validation and all required package tests.
14. Canonicalize the result, record digests, and seal the App Version.

## Standard validation errors

| Code | Meaning |
|---|---|
| `AC_SCHEMA_INVALID` | Source structure fails JSON Schema validation |
| `AC_UNKNOWN_FIELD` | A non-contract field is present |
| `AC_DUPLICATE_ID` | An identifier repeats within its declaration collection |
| `AC_UNKNOWN_REFERENCE` | A logical reference does not exist |
| `AC_INVALID_PATH` | A package path is missing, absolute, or escapes the package |
| `AC_COMPONENT_KIND_INVALID` | A Component is used for an incompatible Surface or Entrypoint |
| `AC_TRIGGER_INVALID` | Schedule or webhook target, invocation, schema, verification reference, or idempotency is invalid |
| `AC_QUERY_HAS_EFFECT` | A query requests write access or a consequential Capability |
| `AC_CAPABILITY_UNKNOWN` | A Capability is not registered |
| `AC_CAPABILITY_CONSTRAINT_INVALID` | Capability constraints fail their registered schema |
| `AC_CONNECTION_UNKNOWN` | A Connection or connector reference is invalid |
| `AC_CONNECTION_FALLBACK_INVALID` | Unavailable behavior conflicts with connector requirements |
| `AC_APPROVAL_REQUIRED` | Requested authority is missing the minimum approval declaration |
| `AC_RUNTIME_UNSUPPORTED` | The derived runtime or required SDK is unavailable |
| `AC_DEPENDENCY_UNLOCKED` | Executable code lacks a reproducible lock |
| `AC_SECRET_MATERIAL_DETECTED` | Credential-like material appears in the package |
| `AC_PERMISSION_UNDECLARED` | Implementation behavior requests undeclared authority |
| `AC_SCHEMA_CHANGE_UNSUPPORTED` | A Resource change is not backward compatible in v0.1 |
| `AC_TEST_FAILED` | A required package or platform validation fails |

## Versioning

- `apiVersion` versions the source vocabulary and semantics.
- Breaking changes create a new major API version.
- Compatible optional fields may be added in a minor revision.
- App Versions record exact contract, compiler, registry snapshot, SDK, runtime, Component, and dependency versions.
- Release activation repeats compatibility and policy checks even when the package was valid at Build time.

## Explicit v0.1 exclusions

- Public App interfaces and anonymous ingress; only authenticated platform-managed webhook ingress is supported.
- Native mobile packaging and general desktop control.
- Backend runtimes other than Python 3.13.
- Workflow-engine Components, general event buses, synchronous generated endpoints, anonymous ingress, or public APIs.
- Raw unbrokered outbound network access. Governed generic HTTP and browser access remain supported Capabilities.
- Workspace-shared Resources and breaking Resource migrations.
- App-to-App exports or cross-Workspace access.
- Context writes and non-user, non-Workspace, or non-App Context scopes.
- Conditional approval expressions.
- Automatic production self-modification.
- Marketplace signing, third-party extension namespaces, and provider-specific model configuration.
- The Capability wire protocol and Run Event Kernel, which are governed by separate specifications.

## Remaining adjacent work

The Package Layout, Resolved App Manifest, Release Resolution Record, Capability Protocol, and accepted Run Event Kernel now answer the package, canonicalization, authority, operation, approval, and minimum Run-evidence questions that were open when revision 3 was accepted.

The remaining walking-slice contracts are:

1. The narrow App UI Bridge for native and custom interfaces.
2. The Build and Run sandbox profiles selected from adapter and execution proof rather than source-manifest fields.
3. The first physical-topology and reliability defaults that constrain the accepted contracts.

The Builder Harness Interface v0.1 is accepted as the design baseline after a proof with pinned DeepSeek and deterministic fake adapters. An internal thin slice may implement the bounded App lifecycle with constrained or fake adapters while external distribution and every enabled custom-code, remote, or consequential-action path remain subject to their specific readiness gates.
