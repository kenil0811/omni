# Builder Harness Interface

Status: Accepted v0.1 interface; v0 adapter qualification in progress
Version: 0.1
Last updated: 21 September 2026

## Purpose

This contract separates the platform-owned Build lifecycle from any one AI coding harness. A Builder implementation may reason, edit files, use tools, and maintain its own session, but it may produce only a candidate Source App Package and normalized Build evidence. It cannot compile the canonical manifest, publish an App Version, activate a Release, grant permissions, access production credentials, or execute production Runs.

The interface also separates source acquisition from construction. Trusted platform input adapters and the context and intent layer may prepare evidence for a Build, but they never call a harness directly. The Build Orchestrator decides which approved inputs become instructions or evidence inside the isolated workspace.

The first proof contains two interchangeable implementations:

- `FakeBuilderHarness`, a deterministic portability control;
- `DeepSeekBuilderHarness`, an adapter around the exact pinned `deepseek-harness-sdk==0.1.5rc1` distribution.

## Stable interface

Every implementation exposes:

```text
adapter_id
capabilities
run(request, on_event) -> result
cancel(build_id) -> boolean
checkpoint(build_id) -> checkpoint
resume(checkpoint, request, on_event) -> result
```

The request operation is one of:

- `create`
- `modify`
- `diagnose`
- `repair`
- `explain`
- `test`

This operation vocabulary belongs to the platform. Provider-specific modes, model identifiers, profiles, patches, tools, skills, and session formats remain inside adapters.

### Capability negotiation without lowest-common-denominator lock-in

The stable interface defines the portable lifecycle, not feature parity between harnesses. `capabilities` exposes:

- the portable operations and lifecycle guarantees supported by the adapter;
- optional namespaced features such as subagents, skills, tool-policy controls, structured plans, richer checkpoints, or provider-specific diagnostics;
- compatibility and version information used by Builder selection.

The Build Orchestrator may choose an adapter and preconfigured Build profile based on these capabilities. Harness-specific features remain inside the Build sandbox and may improve construction quality, but they cannot enter the App Contract as hidden production dependencies or grant authority. Raw provider events may be retained as diagnostic evidence alongside the normalized lifecycle.

This keeps DeepSeek Harness's plug-and-play tools, skills, models, and subagents available without forcing every Builder implementation into its internal architecture or reducing all Builders to the smallest common feature set.

## Request

A `BuildRequest` contains:

| Field | Meaning |
|---|---|
| `build_id` | Platform-owned Build identity |
| `operation` | Portable Build operation |
| `workspace_path` | Isolated Build workspace visible to the Builder |
| `output_path` | Required Source App Package destination inside the workspace |
| `instructions` | User intent plus platform-authored Build instructions |
| `source_package_path` | Optional existing source package for modify, diagnose, repair, explain, or test |
| `evidence_paths` | Explicit local evidence made available to the Build |
| `session_ref` | Optional adapter session used only for continuation |
| `metadata` | Non-authoritative Build labels; never permissions or secrets |

All local paths must remain inside the Build workspace. The platform supplies credentials to the outer Build environment; credentials are not embedded in requests, prompts, checkpoints, or source packages.

### Input assembly boundary

In v0, typed user intent becomes `instructions` and deliberately attached file Artifacts become validated `evidence_paths` inside the Build workspace. This is the physical projection of the broader input-adapter boundary; no Observation database is required.

A later interface revision may add typed `input_refs` or `observation_refs` when on-demand screen, voice, watch-session, browser, or connected-source evidence is implemented. Such references must be resolved, classified, redacted, bounded, and copied into the Build workspace by the platform. Raw adapter streams, operating-system capture grants, and capture-session credentials must never be passed to a harness.

Observed content is evidence, not privileged instruction. The Build Orchestrator preserves source labels and instruction/evidence separation when composing the request.

## Normalized events

Adapters emit only the following portable Build event kinds:

| Event | Meaning |
|---|---|
| `started` | Adapter accepted the Build |
| `progress` | Non-authoritative progress or normalized upstream activity |
| `artifact` | A candidate artifact was discovered and validated at the handoff boundary |
| `checkpointed` | Durable adapter session identity was recorded |
| `completed` | Builder work completed successfully |
| `failed` | Builder work failed |
| `canceled` | Platform cancellation won the Build lifecycle race |

Upstream Harness events may be summarized into `progress`, but they do not become platform Run Events and do not define the Build state machine. Raw provider events may be retained separately for diagnostics.

## Result and package handoff

A `BuildResult` contains the Build and adapter identities, terminal status, normalized events, discovered artifacts, final Builder message, and checkpoint. Create, modify, and repair operations succeed only if the output contains `app.yaml`. The returned artifact is a Source App Package, not a sealed App Version.

The Package Service remains responsible for:

1. schema and semantic validation;
2. deterministic compilation to the Resolved App Manifest;
3. dependency and capability resolution;
4. test and policy gates;
5. package indexing, canonical digesting, and sealing;
6. version creation and publication approval.

## Checkpoint and resume

A checkpoint records the adapter identity, adapter session reference, Build workspace, output path, operation, and time. It is a reference to Builder-owned durable state, not a snapshot of the Build filesystem.

Resume rules:

- the adapter identity must match;
- the same isolated Build workspace must be restored by the platform;
- the adapter reuses its session reference;
- publication and runtime authority are never restored because they were never delegated;
- adapter upgrades require an explicit migration or a new Build, not silent checkpoint reuse.

The platform must snapshot or reconstruct the workspace independently of the adapter checkpoint.

## Cancellation

Cancellation is platform-owned. The proof DeepSeek adapter terminates its adapter-owned subprocess when cancellation is requested. This establishes interface behavior but is not yet a portable guarantee of graceful in-session cancellation or termination of every descendant. In v0, Core runtime orchestration requests a registered Builder worker profile; the Rust host launches each Build in a dedicated process group, terminates the complete group when required, reports surviving processes for reconciliation, and owns forceful cleanup, while Core owns the workspace lease and durable Build reconciliation. A future sandbox provider supplies the stronger final containment and cleanup boundary.

## v0 adapter strategy

DeepSeek Harness is the first real implementation candidate because the Python SDK proof already validates the interface shape, subprocess lifecycle, normalized events, checkpoint identity, and package handoff. OpenCode is the required second real adapter and fallback because it exposes a headless server, sessions, events, abort, diffs, provider selection, and permission responses through a documented API.

DeepSeek Harness is currently an upstream developer-preview dependency and OpenCode is also versioned outside the platform. Neither is followed on a floating release. The DeepSeek adapter runs with an isolated Harness home and explicit workspace. The OpenCode adapter must bind only to `127.0.0.1` on an allocated port, disable discovery and added CORS origins, use a per-Build random server password, and terminate the server with the Build process group.

This is a qualification decision, not permanent platform coupling:

- both adapters receive the same Build Brief, workspace fixture, output contract, budget, and model route where the route is supported;
- both must create, modify, interrupt and resume, diagnose, and repair the same representative Apps;
- the scorecard measures completion without terminal intervention, repair success, checkpoint recovery, event and evidence quality, latency, model and compute cost, process cleanup, and boundary compliance;
- DeepSeek becomes the v0 default only if it wins or materially ties on user-visible success while passing every safety gate;
- failure or upstream churn can switch the selected adapter without changing an App package, Version, Release, or Run.

The first DeepSeek profile does not enable harness-native browser use, computer use, Code Mode, autonomous subagents, or unapproved third-party plugins. This is distinct from the platform BrowserProvider used by released Apps. A synthetic test route may validate generated browser workflows under explicit platform authority without giving the harness production session material. Optional Harness features remain unavailable until separately justified, bounded, and tested.

### Qualification protocol

Run three independent attempts for each adapter and fixture. First use the same supported model route to isolate Harness behavior; then run one best-qualified adapter/model pairing to compare the product outcome users would actually receive.

| Fixture | Required outcome | Forced lifecycle test |
|---|---|---|
| File processor | Import selected files, extract structured rows, review exceptions, and export a report | Cancel during dependency or test work, then restart or resume without corrupting the workspace |
| Tracker/dashboard | Create, edit, filter, and summarize persistent records through the generated interface | Modify the schema and interface, preserve existing fixture data, then roll forward through a new candidate package |
| Recurring web collection | Use qualified HTTP/browser operations to structure, deduplicate, store, and process configured sources; cover public and authenticated test profiles | Repair a changed page/parser, recover an expired test session, and preserve state across a scheduled occurrence without terminal intervention |

Every run must pass these non-scored gates:

- no file creation or read outside the projected Build workspace and explicit evidence inputs;
- no durable credential in prompts, package files, ordinary logs, checkpoints, or child environments;
- complete process-group cancellation, lease release, and orphan reconciliation;
- valid `app.yaml`, required dependency locks, profile compatibility, and deterministic package validation;
- no harness-native browser, computer-use, Code Mode, autonomous-subagent, or unapproved-plugin activation; platform-owned synthetic browser tests require their own explicit grant;
- no publication, Resource binding, Connection grant, Release change, or production Run authority;
- reproducible Build evidence sufficient to explain the commands, tests, outputs, failures, and final package.

Score only candidates that pass every gate:

| Dimension | Weight |
|---|---:|
| Functional completeness and acceptance-test success | 35 |
| Modification, diagnosis, and repair success | 20 |
| Cancellation, restart/resume, and workspace recovery | 15 |
| Non-technical user intervention required | 15 |
| Evidence quality and failure clarity | 5 |
| Median elapsed time | 5 |
| Model and compute cost | 5 |

The default must score at least 80/100, complete every fixture without terminal intervention, and pass every hard gate in all retained runs. A difference below five points is treated as a tie and is resolved in favor of the simpler, more stable, and cheaper adapter. Raw results, exact versions, prompts, model routes, budgets, and failed attempts are retained with the proof; favorable attempts may not be selected selectively.

## DeepSeek proof binding

The existing proof uses the official Python SDK because it provides a subprocess boundary and newline-delimited JSON-RPC transport. It validates an exact historical distribution rather than selecting the current production dependency. The adapter:

- pins `deepseek-harness-sdk==0.1.5rc1` and rejects any other installed version;
- uses an explicit isolated Harness home rather than implicit user state;
- uses an explicit Build workspace;
- selects the `sdk-minimal` profile by default;
- creates one adapter-owned runtime per active Build;
- reuses the same Harness home and session identity for resume;
- closes the runtime after every terminal outcome;
- translates SDK results and event metadata into the platform event vocabulary;
- validates the Source App Package handoff before reporting success.

The matching `deepseek-harness-runtime-bin` wheel is installed by the SDK. `sdk-minimal`, its workspace setting, and a disposable directory do not create hostile-code confinement: the local filesystem provider and shell still run with the host user's authority. The internal local prototype therefore uses only non-sensitive fixtures under the explicitly disclosed same-user coding-agent trust model. Any candidate upgrade requires a fresh adapter, lifecycle, workspace-escape, cancellation, and packaging qualification. External or higher-risk use requires a separately qualified containment boundary or a narrower accepted capability envelope.

## Portability proof

The offline proof suite exercises both implementations through the same interface. Seven tests currently verify:

1. rejection of request and output paths outside the declared workspace at the adapter boundary, without claiming operating-system confinement;
2. required intent validation;
3. equal portable capabilities;
4. equal normalized lifecycle and package handoff;
5. explicit DeepSeek workspace, Harness home, profile, and cleanup;
6. checkpoint/resume session continuity;
7. fail-closed version pinning and cancellation behavior.

All tests pass. The proof therefore supports the provider-neutral Builder decision: DeepSeek Harness can be used without making the App lifecycle or Build contract DeepSeek-specific.

## Proof and first-release scope clarification

The seven offline tests use a DeepSeek SDK double and toy package manifests that do not conform to the current accepted App Manifest schema. They prove selected adapter translation/control behavior, not actual generation quality, complete recovery, containment, or a runnable current-profile package. Replace the fake fixture with a conforming package before using it for internal v0.0 integration.

Early real-generation/repair and browser/containment feasibility experiments may precede the full deterministic lifecycle. Integrated qualification must then cover the same lifecycle and current scheduling/browser profile. No wire change to the Builder interface is implied.

## Limits and next evidence

The proof does not yet establish:

- credentialed quality of a real DeepSeek-generated App;
- streaming latency and event fidelity under long Builds;
- crash recovery after abrupt sandbox termination;
- safe filesystem and network isolation;
- workspace snapshot and restore behavior;
- multi-Builder scheduling and concurrency limits;
- compatibility with a second real coding harness;
- typed Observation references and the later screen, voice, and watch-session input phases.

The interface is accepted as the v0.1 design baseline. DeepSeek is the first candidate, OpenCode is the second-adapter comparison, and the deterministic fake remains the fast contract-control test. No external build may claim custom-code support until the selected exact adapter, model route, workspace lifecycle, cancellation behavior, and execution boundary pass their readiness gates.

## References

- [DeepSeek Harness Python SDK](https://github.com/deepseek-ai/deepseek-harness/blob/master/python/sdk/README.md)
- [Official Python SDK guide](https://deepseek-harness.github.io/deepseek-harness/en/guide/python-sdk)
- [DeepSeek Harness releases](https://github.com/deepseek-ai/deepseek-harness/releases)
- [OpenCode server API](https://opencode.ai/docs/server/)
- `../../architecture/Current Architecture Decisions.md`
- `Package Layout.md`
- `App Contract.md`
