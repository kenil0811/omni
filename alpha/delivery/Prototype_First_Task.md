# Prototype First Task - P0 Foundation

Status: Ready for handoff to the founder's separate Mac coding environment; local repository inspection remains P0 work
Task ID: P0-FOUNDATION
Last updated: 21 September 2026

## Assignment

Establish an executable, contract-first implementation foundation for Alpha. Do not implement the full product in this task. The next milestone is P1, the trusted Host/Core skeleton.

Receive and verify `Alpha_Agent_Context.zip` using its `START_HERE.md` and `agent_docs.py`. It supplies the complete project sources and searchable/visual companions. Read `AGENTS.md`, `AI_Coding_Agent_Playbook.md`, `Prototype_Scope_and_Acceptance.md`, `Agent_Document_Access.md`, and the current implementation blueprint. Use the bundled input manifest to identify source versions and hashes. Links without accessible contents are insufficient.

## Confirmed execution arrangement

The founder will manage coding outside this planning project, using AI coding agents on a Mac. No repository needs to be created, connected or disclosed here to finish the handoff. The coding agent should inspect the repository it is given in that environment and record the actual Mac architecture, macOS version and available runners; Mac access does not itself prove any tests have passed.

Provide this task, the root `AGENTS.md`, the playbook, prototype scope, and the referenced canonical source contents to that agent. This planning project can review returned diffs, checkpoint reports, failures and proposed design changes. Paid model experiments still need explicit access and limits in the coding environment.

## Inputs to inspect in the coding environment

| Input | Required action if absent |
|---|---|
| Founder-provided repository/path, existing branch and applicable instructions | Resolve locally with the founder if not supplied to the coding agent; no repository access is required in this planning project |
| Confirmed Mac development environment and any additional CI runners | Inspect actual macOS/architecture/toolchains and Windows runner availability; only claim the environments actually tested |
| Current canonical source snapshot with identities/digests | Obtain it through supplied access; do not reconstruct the architecture from this brief |
| Existing decisions and allowed external package sources | Preserve accepted stack; flag material unresolved choices, licensing conflicts or unavailable packages |
| Model credentials/provider and experiment budget, if live experiments are requested | Continue deterministic work without them; no paid/live qualification until explicitly supplied |

## Input reading list

Use the project index and read the current versions of:

- `../architecture/Implementation Blueprint.md`
- `../architecture/Current Architecture Decisions.md`
- `../architecture/Domain and Persistence Model.md`
- `../architecture/Security Privacy and Data Boundaries.md`
- `../specifications/Current Release Specification.md`
- `../specifications/Specifications Index.md`
- `../specifications/Local_Automation_and_Platform_Extension_Profile.md`
- `AGENTS.md`, `AI_Coding_Agent_Playbook.md`, `Run Event`, `Task`, `App`, and Builder contracts referenced by those documents;
- accepted machine-readable schemas/examples/invalid fixtures and the existing adapter proof, explicitly treated as limited prior evidence.

These relative paths describe canonical Alpha documents. In a repository, resolve them through the snapshot manifest rather than assuming this file's original folder layout was copied.

## Ordered work

1. **Inspect and record.** Report repository status, existing instructions, baseline commit, available OS/toolchains and source versions. Preserve user changes. List only material missing inputs and finish read-only analysis while awaiting them.
2. **Define a focused plan.** Map P0 to exact files and checks. Resolve contradictions in current sources before dependent code; propose concrete choices for any undefined product or authority behavior. Do not choose production timeouts, spend caps or scheduler semantics silently.
3. **Stage canonical inputs and contract ownership.** Create the immutable snapshot/input manifest. Map accepted machine-readable assets into the blueprint's `packages/contracts/` layout without editing their meaning. Record the repository commit for the canonical index cutover; do not delete the original source before that mapping is verified.
4. **Complete the immediate contracts.** Draft Task/Attempt/events and one atomic local-platform protocol bundle for Core IPC, Host control and worker bootstrap. Define exact fields, states, auth/version/error/deadline/size semantics, valid examples, invalid structural and semantic cases, compatibility rules and validators. Use the accepted decisions; present unanswered material choices before implementing their behavior. Do not introduce a new App Run state or a hidden Task App.
5. **Initialize minimal workspaces and tools.** Add root Python/TypeScript/Rust workspace configuration, pinned resolver/toolchain inputs, relevant locks, the contract package, testkit and only the files needed for executable P0 checks. Mark provisional runtime candidates as provisional until packaged qualification; do not call them qualified locks. Install the provided root instructions after reconciling existing ones.
6. **Implement real verification entrypoints.** Make bootstrap, generation, deterministic checks and the relevant CI matrix executable. Run valid/invalid contract cases, semantic validators, clean regeneration and import/dependency boundary checks. Missing product components are not passing tests. Paid Builder calls are excluded.
7. **Review and hand off.** Produce the P0 evidence record, independent review where available, exact remaining blockers, and a P1 task packet grounded in the files now present. Update or supply the canonical checklist patch. Advance only within the user's authorized sequence and after P0's exit evidence exists.

## Scope boundaries

Allowed: repository setup in the confirmed location, contract work, fixtures/validators, source mapping, lock/configuration files, contributor setup, CI, input snapshots and evidence. Drafting a small operational task record is part of this work.

Not included: broad UI implementation, real App generation, browser or schedule activation, cloud infrastructure, external distribution, model spending, production credentials, general memory, new orchestration frameworks or an entire future folder tree. Bounded feasibility experiments are separate explicit packets; they may proceed early once their inputs and limits are supplied.

## P0 acceptance

- Actual repository and input snapshot are identified; unrelated work remains intact.
- Accepted source contracts retain a verified mapping; new Task/protocol definitions have concrete valid/invalid cases and semantic checks.
- Relevant Python/TypeScript/Rust tooling is locked and reproducible to the extent exercised; native qualification is reported separately.
- "Just generate" leaves no diff on its second run.
- Applicable "just check" steps execute real validators/checks and reject an intentionally invalid fixture or forbidden dependency in an isolated test; no placeholder "success" steps.
- Shared Windows and native Mac CI scopes are explicit. Required jobs without runners are blocked/not run, not green by omission. P0 cannot be called fully passed until its required checks actually execute.
- No secret, raw private session or paid test is introduced into default setup/checks.
- Reviewer findings, unresolved decisions and observed failures are retained; no claimed product behavior is based solely on scaffold files.
- Handoff names the exact P1 dependencies and the next smallest vertical outcome.

## Required final response from the coding agent

Report briefly: what was created or changed, exact verification results, blocked checks or decisions, evidence locations, and the P1 handoff. Do not say the product is implemented or ready for users.
