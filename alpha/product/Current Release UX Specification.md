# Current Release UX Specification

Status: Canonical first-usable-release specification
Last updated: 21 September 2026

## Purpose

Define the first complete experiences a non-technical user must be able to finish from one Assistant entry point:

> Ask for an outcome, receive either a direct answer, a bounded one-off Task result, or a proposed reusable App; inspect what happened; and turn proven work into an App when reuse is valuable.

> For reusable work, describe the capability, receive a working local preview built from real generated code, review its access, release and use it, inspect what happened, request a correction, publish a new Version, and roll back safely.

The product supports open-ended App/workflow goals; examples test breadth. The first usable release includes local schedules and public/authenticated browser automation. The internal v0.0 milestone may remain manual. Cloud deployment, desktop control, screen capture, voice, and broad procedural memory remain later.

## Initial product boundary

- Signed Mac application using the accepted three-region shell.
- Workspace Assistant as the primary entry point, with scripted Task, Builder, correction, and diagnosis roles.
- Plain-language request disposition: answer directly, `Do once`, or `Make reusable`.
- Platform-owned local Task Runner for bounded text-and-file work.
- Durable Task, Task Revision, Task Attempt, output Artifact, evidence, and Activity records.
- One standardized generated-App stack.
- One dedicated local workspace and dependency environment per App.
- Local App code, state, files, configuration, secrets, Run history, logs, and evidence.
- Remote Builder and runtime AI routes are allowed and disclosed.
- Real generated code runs under the qualified local execution profile; same-user execution without hostile-code containment is limited to disclosed internal non-sensitive experiments.
- Generated UI has no ambient filesystem, credential, network, or native authority.
- Manual and locally scheduled Runs, selected files, App storage, qualified HTTP, and general public/authenticated browser operation.
- Dedicated browser sign-in, takeover/resume/stop, protected account scope, and session-expiry recovery.
- Clear runtime availability and next/last/missed work; missed occurrences show their intended time, reason, manual retrigger action, and any subsequent outcome. There is no automatic catch-up.
- Automation continues after the main window closes, with accessible background status and pause/stop/quit controls.
- Apps may use trusted results/configuration/Activity without custom UI.
- Versioned Build, preview, Release, Run, correction, and rollback.

The v0 Task Runner receives only the submitted instruction and deliberately selected inputs. It may use the disclosed model route and a fixed set of platform-owned read, transform, analysis, and Artifact tools. It does not schedule work, browse or control the desktop, perform consequential external writes, read ambient files, or execute arbitrary generated code.

## Reference fixture

The one-off Task fixture is intentionally ordinary:

> Compare the files I selected, identify the differences and open questions, and give me a report I can save.

It exercises request disposition, selected-file provenance, model routing, Task attempts, output Artifacts, evidence, cancellation, and failure recovery without creating an App.

The primary App fixture is also intentionally ordinary:

> Build an App that imports files I choose, extracts records into a searchable table, lets me correct exceptions, and produces a summary report.

It exercises intent capture, file permission, schema generation, generated UI, local persistence, real code execution, manual Runs, evidence, correction, Versions, and rollback without requiring browser or cloud infrastructure.

Breadth is then tested with an interactive tracker, a recurring collection/structuring/storage/processing App using qualified HTTP or browser operations, an authenticated browser workflow with login recovery, and a novel user request. These are tests, not supported-workflow or website lists. See `../specifications/Local_Automation_and_Platform_Extension_Profile.md`.

## Recurring and browser journeys

For recurring work, the user describes the outcome, sources, and cadence; previews results; reviews destinations, account, data, effects, timezone, next run, and availability; then activates a schedule through trusted controls. Explain that closing the main window keeps automation running and that missed jobs wait for a user-initiated retrigger rather than running automatically on return. Activity retains each missed occurrence and any linked retrigger outcome. Explicit runtime quit stops local execution. Complete overlap/offline semantics, retrigger Release/input handling, background controls, and separate login-start presentation before the activation design is signed off.

For authenticated browser work, show a dedicated automation browser where the user signs in and can handle MFA or renewal. Show which App/account is active and provide takeover, resume, and stop. An expired session or ambiguous remote effect creates an actionable state, not an unexplained failure or silent resubmission. Use existing Run/approval/human-input semantics; exact provider messages remain a contract gate.

The same App shell supports background jobs without generated UI through configuration, results, and Activity. A later Windows client keeps the product concepts and adapts native interactions, dialogs, keyboard conventions, and lifecycle behavior.

## Experience principles

1. Start with the desired outcome, not a template, runtime, workflow, agent, or App type.
2. Ask only questions that change behavior, access, cost, or acceptance.
3. Use the lightest adequate result: answer, one-off Task, or reusable App.
4. Show a Task plan or working App preview early.
5. Keep code, manifests, dependencies, and raw logs behind progressive disclosure.
6. Show where execution happens and where persistent data will live.
7. Treat permissions, Build commands, and external data transfer as separate decisions.
8. Preserve every important state outside chat.
9. Make correction, failure diagnosis, retry, and rollback normal parts of the product.

## Shell

The accepted shell remains:

| Region | Purpose |
|---|---|
| Left | Folders and reusable Apps in the Workspace |
| Centre | Workspace start, Task detail and result, Build Brief, preview, selected App, Manage, Activity, Runs, and Versions |
| Right | Workspace Assistant, Task, Builder, correction, or execution diagnosis in an explicit scope |

The centre is the durable work surface. The right panel explains and changes durable objects; it does not become the only record of the work.

## Assistant request disposition

The Assistant begins with the outcome and chooses no durable object until one is useful:

| Result | Use when | User-facing commitment |
|---|---|---|
| Answer | No tool execution or durable operational result is needed | Respond now in a durable searchable Assistant Turn; optionally save an Artifact |
| Do once | The work is bounded and useful once | Create a Task, show inputs and relevant route, execute, and retain the result and evidence |
| Make reusable | The work needs repeated use, mutable state, an interface, triggers, or ongoing ownership | Open a Build Brief and follow the App lifecycle |

The Assistant may recommend a result without asking the user to classify every request. It must ask when the choice materially changes access, persistence, cost, or behavior. The user can switch from `Do once` to `Make reusable` before execution or promote a completed Task later.

A direct answer remains a durable Assistant Turn with its source links and route disclosure. It can be reopened and searched through Workspace history, cited into a later request, or deliberately saved as an Artifact; it does not become a Task merely to remain findable.

## One-off Task journey

| Stage | User experience | Durable result |
|---|---|---|
| 1. Request | Describe the outcome and deliberately attach files | Draft Task intent |
| 2. Confirm | Review material assumptions, selected inputs, named remote route, output form, and limits | Immutable Task Revision |
| 3. Execute | See a concise plan, current step, elapsed time, Stop, and expandable details | Task Attempt and ordered Activity |
| 4. Resolve | Supply missing information if needed; a question never implies approval | Human-input record linked to the Attempt |
| 5. Inspect | Review the result, output Artifacts, source references, duration, Cost, and errors | Attempt outcome and evidence |
| 6. Continue | Retry with a new Attempt, revise the Task, save an Artifact, or choose `Make reusable` | Preserved lineage to the next object |

A Task does not receive an App workspace, Version, Release, Entrypoint, or hidden generated interface. Promotion creates a normal Build Brief and App lifecycle; it does not relabel the Task as an App.

## Reusable App journey

| Stage | User experience | Durable result |
|---|---|---|
| 1. Request | Describe the App and optionally attach files | Draft intent |
| 2. Clarify | Answer a small set of material questions | Decisions and assumptions |
| 3. Brief | Review outcome, interface, data, access, test, and known limits | Editable Build Brief |
| 4. Build | See product milestones while the agent creates code, installs allowed dependencies, and runs checks | Build record and candidate Version |
| 5. Preview | Use the real generated interface against safe sample or selected data | Preview Release and test evidence |
| 6. Access review | Review folders, Connections, destinations, model routes, commands, and expected side effects | Grants and Release bindings |
| 7. Release | Activate the candidate as `On this Mac` | Active local Release |
| 8. Operate | Use the App and invoke a manual action | Run and outputs |
| 9. Inspect | See outcome, evidence, logs, cost, and errors in plain language | Run record and Artifacts |
| 10. Correct | Explain what is wrong from the App, record, or Run | Correction and candidate Version |
| 11. Compare | Review behavior, data, access, dependency, and test differences | Version comparison |
| 12. Roll back | Restore the previous working Version through a new Release pointer | Rollback Release and audit event |

## Task experience

The centre shows a Task as a durable object rather than leaving its execution inside the chat transcript. Its header shows purpose, state, execution location, and primary action. The body shows selected inputs, concise progress, result, output Artifacts, and expandable evidence. The Assistant remains scoped to that Task for explanation, revision, retry, or promotion.

The first release does not add Tasks to the left App browser or add a permanent global Activity destination. The Workspace start view shows recent Tasks and Apps; an on-demand searchable Workspace history finds older Assistant Turns, Tasks, and Apps; and Task deep links reopen the durable Task detail. A trusted overflow lets the user delete a Task and its retained copies and outputs without deleting selected source files. This preserves an Assistant-first entry without turning one-off work into navigation clutter.

## Build experience

The Builder may create files, edit code, install approved dependencies, execute build and test commands, and start a preview inside the App's managed local workspace. The user approves a bounded Build plan and command policy rather than each routine command. Commands remain visible and cancellable; a new prompt appears only for a new executable family, network destination, external file scope, credential, privilege boundary, or materially higher risk. The product records normalized milestones and retains technical output for diagnosis.

The first supported runtime is deliberately standardized. Horizontal breadth comes from what users can build, not from supporting every framework and language immediately.

The product manages:

- App workspace creation;
- runtime and dependency versions;
- local port allocation;
- environment configuration;
- process start, stop, restart, and health;
- logs and crash state;
- package validation;
- Versions, Releases, and rollback;
- deletion and cleanup.

The user is not expected to open a terminal.

## Permission model

The interface separates:

- permission for a Task Attempt to use selected inputs, a named model route, bounded platform tools, and an output location;
- permission for the Builder to perform a bounded Build plan and command family inside the App workspace;
- permission for a released App to read a selected folder or file;
- permission to use a Connection or secret;
- permission to send data to a model, API, or website;
- permission to perform a consequential external action.

A Task Runner's authority, a Builder's temporary construction authority, and a released App's runtime authority are separate. Completing or promoting a Task does not transfer its file access or model disclosure into an App Release.

Every trusted approval shows the exact action, acting account or principal, destination or recipient, data leaving the device, one-time or reusable scope and frequency, reversibility, cost or limit, and what happens next. A typed answer to a question is never treated as approval.

## Deployment communication

The v0 Task review shows `On this Mac` execution and local Task history, while identifying any remote model or service route used for processing. A Task is not silently uploaded for cloud execution.

The App Release review shows `On this Mac` as the available first target and explains:

- code and persistent App data remain on the Mac;
- selected request data may be sent to named AI providers, websites, or APIs;
- the App is unavailable when its local runtime is unavailable;
- no platform cloud silently keeps the App running.

`Always available` may appear as a future target only when it is clearly labelled unavailable. It must not imply implemented cloud hosting.

## States

| State | Required behavior |
|---|---|
| Planning | Show the proposed Task boundary, inputs, route, output, and material limits |
| Building | Show completed, current, and remaining product milestones |
| Waiting for user | Preserve the Task Attempt, Build, or Run and present the exact question |
| Needs command approval | Show the bounded Build-plan change, affected command family, purpose, working directory, network/file/credential scope, and risk |
| Needs access | Open a trusted file, Connection, or capability flow |
| Running | Show current action, elapsed time, Stop, and technical details |
| Failed | Preserve logs and evidence; offer retry, revision, repair, or revert as applicable |
| Degraded | Explain what remains usable |
| Offline | Keep local data usable and identify affected network work |
| Completed | Show output, evidence, duration, cost, and next action |

## Acceptance criteria

The first slice passes only when:

- a non-technical tester can start from the Assistant without choosing an object type;
- the Assistant can distinguish a direct answer, a bounded Task, and work that needs an App, with an understandable override;
- direct answers, older Tasks, and Apps can be reopened through searchable Workspace history without placing Tasks in the App browser;
- a tester can complete, inspect, retry, and reopen at least three materially different text-and-file Tasks;
- every Task Attempt records exact selected inputs, execution profile, remote route, outputs, evidence, cost, and terminal state;- a successful Task can seed an App Build Brief without losing its source lineage or inheriting authority;
- a non-technical tester can create at least three materially different Apps without terminal use;
- generated code is real, locally stored, buildable, and restartable;
- the App reopens with its code, data, configuration, and Activity intact;
- a failed Build or Run provides enough evidence for the Builder to attempt a repair;
- a correction produces a new Version rather than mutating the active one;
- rollback restores a working Release without deleting later history;
- requested local files and external routes are understandable before use;
- the shell remains usable when a Task Attempt, generated UI, or App code fails;
- no unsupported browser, desktop action, schedule, cloud execution, memory, observation, or autonomy behavior is implied.

## Next slice

After these Task and App lifecycles work, advance three independent tracks according to evidence: local automation adapters, local Workspace context and memory, and the `Always available` App target. Within the automation track, add schedules and missed-run semantics, expand the narrow v0 HTTP fixture into policy-qualified public-web retrieval, then add connectors and deterministic browser automation. Scoped desktop action remains later than those more reliable routes.

## References

- `Product Vision and Principles.md`
- `Roadmap and Scope.md`
- `Mac Experience Architecture and Screen Specification.md`
- `../architecture/System Architecture.md`
- `../architecture/Deployment and Execution Architecture.md`
- `../specifications/Specifications Index.md`
