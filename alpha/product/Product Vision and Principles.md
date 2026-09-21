# Product Vision and Principles

Status: Canonical
Last updated: 21 September 2026

## Vision

Build a persistent agentic work assistant that makes non-technical people AI-first.

The user begins with an outcome, not an object type. The Workspace Assistant may answer directly, carry out a bounded one-off Task, or help create a durable App when the work needs an interface, state, repetition, or ongoing operation. Apps are the first durable reusable execution object, not the front door and not the final limit of the product.

Over time, the same Assistant may use user-authorized files, connected services, browser activity, screen context, voice, and explicit demonstrations to retain useful context, recognize repeated work, and help compile approved procedures into Apps, Workflows, or Agents. The primary long-term value is helping with the work between the work: moving and reconciling information, preparing inputs, operating routine processes, and coordinating actions across tools.

The long-term destination is a user-controlled procedural second brain: a system that does not merely answer questions, but can remember relevant context, maintain useful tools, and perform bounded work with evidence and permission.

## The problem

Powerful coding agents, automation platforms, and agent frameworks already let technical users create software and automate work. Most non-technical users cannot comfortably manage repositories, terminals, runtimes, dependencies, credentials, deployment, logs, failures, or security boundaries. The product opportunity is reducing the effort needed to organize, repeat, correct, and maintain work created with AI. Existing assistants and builders already overlap with this space; usefulness must be demonstrated through the complete operating experience.

The product closes that gap through a maintained interface over real generated software and governed execution.

## General-purpose builder and extensibility

The initial App/workflow framework is an intentional starting product for the long-term second brain. Users can request widely different tools, processing pipelines, recurring jobs, automations, and interactive Apps. The platform must not restrict them to a catalogue of predefined workflows, websites, or industries. Generated code and qualified dependencies provide the flexibility to implement unfamiliar requirements.

An App may be a background workflow with trusted results and Activity screens; a custom interface is optional. The first usable local release includes recurring execution and general browser automation, including user-connected authenticated sessions. Local work requires an awake Mac and a running runtime, with network access when needed. Missed jobs remain visible for the user to retrigger later, with no automatic catch-up. Automation continues after closing the main window; explicitly quitting the runtime stops local execution.

macOS ships first and Windows is a required later target. Stable platform, capability, provider, and runtime interfaces isolate native implementation details from portable product logic. Preserve goals, rules, correction rationale, and execution evidence alongside code so later memory and proactive assistance can build on useful work. Broad memory and desktop observation remain separate later capabilities.

One initial execution stack is an implementation boundary, not a restriction on user goals. New capabilities must be addable through registered definitions, adapters, qualified dependencies, or versioned profiles. See `../specifications/Local_Automation_and_Platform_Extension_Profile.md`.

## Product thesis

1. The Assistant is the front door. It should understand the outcome before asking the user to choose chat, automation, agent, workflow, or App concepts.
2. Not every request should become an App. A direct answer is enough when no execution is needed; a Task is enough for bounded one-off execution; an App is appropriate when the capability needs reuse, state, an interface, triggers, or ongoing ownership.
3. A Task is durable and inspectable even when it runs only once. It retains its instructions, selected inputs, execution attempts, outputs, evidence, cost, and failures, and can seed a reusable object later.
5. The same App package should be deployable on the user's Mac or in cloud without being rewritten.
6. Local deployment serves users and use cases that require local files, device capabilities, low platform cost, or no persistent product data in cloud.
7. Cloud deployment serves users and use cases that value always-on operation, stronger compute, and access from multiple devices.
8. Remote AI models are compatible with both modes. Local deployment governs execution and persistent product data; it is not a promise of offline inference.
9. Workspace memory has its own placement and consent boundary. Useful local memory must not require an App to be cloud-deployed.
10. The Assistant becomes more valuable as Tasks, Apps, approved context, and adapters accumulate, but ambient observation and proactive behavior come only after bounded execution is useful and trustworthy.

## Positioning

The product sits between several existing categories:

- coding agents provide power but assume technical operation;
- hosted App builders simplify creation but commonly centre on hosted external applications;
- automation tools connect services but expose workflow concepts and brittle configuration;
- second-brain products retain information but often stop at retrieval;
- chat assistants help in the moment but rarely create durable user-owned operational systems.

The product combines the most useful parts of those categories behind one non-technical Assistant and Workspace experience. It is not positioned as a vertical solution. Example Tasks and Apps are validation fixtures, not the definition of the market.

## Intended users

The product is horizontal, initially oriented toward individuals, operators, knowledge workers, and small teams that can identify useful work but do not want to become software developers.

No single profession or workflow defines the platform. Early evaluation must nevertheless use concrete work and recurring patterns; horizontal scope is not permission to avoid a testable capability boundary.

## Product model

### Workspace Assistant

The enduring conversational interface and primary entry point. It helps the user understand the Workspace, answer questions, perform Tasks, create and modify Apps, diagnose execution, and later work with approved cross-App context. It recommends the lightest suitable result-answer, Task, or reusable capability-without forcing the user to classify the request. `Builder` is a role the Assistant adopts, not a separate product persona.

### Task

A bounded request to do something once. A Task records intent, deliberately supplied inputs, constraints, attempts, outputs, evidence, cost, and required human decisions. In v0 it uses a platform-owned Task Runner with text and selected files; it does not silently generate a hidden App or acquire ongoing authority.

A Task may later be promoted, with user review, into a Procedure, Workflow, App, or Agent. Promotion preserves lineage but creates the target object's normal version, permission, and activation lifecycle.

### App

A durable reusable user-facing capability with an interface, configuration, data, Entrypoints, permissions, Versions, Releases, Runs, and evidence. Apps may be interactive tools, data applications, automations, research systems, agents, or combinations of these.

### App Version and Release

Every material change creates an immutable candidate Version. A Release activates one Version against one deployment target and its concrete Resources, Connections, schedules, runtime, and policy. Rollback changes the active Release rather than rewriting history.

### Run

One attributable App execution of one Entrypoint against an exact Version and Release. A Run records state, inputs, relevant context, actions, outputs, costs, evidence, errors, and required human decisions. A one-off Task uses a Task Attempt rather than inventing an App Release; both follow the same control principles even while their wire contracts remain distinct.

### Resource and Connection

Resources hold mutable App data and files. Connections represent access to external systems. Generated code never owns durable credentials or receives ambient access to unrelated user data.

### Observation, Memory, and Procedure

Future input adapters produce provenance-preserving Observations. Derived claims and retained memory remain separate from raw capture and authoritative App state. A demonstrated or inferred Procedure is reviewable evidence, not automatic authority to act.

## Core user loop

1. The user describes a desired outcome to the Assistant.
2. The Assistant asks only questions that materially affect behavior, access, cost, or acceptance.
3. The Assistant answers directly, proposes `Do once`, or proposes `Make reusable`. The user can change the choice whenever the consequences differ.
5. Reusable work enters the Builder, which creates real code and a working preview.
6. The user reviews the App and its requested access, then releases it to `On this Mac` or, when available, `Always available`.
7. The user operates the App and inspects Activity.
8. A useful Task can seed a Build; corrections to an App create a new Version with regression evidence and a rollback path.


Deployment is selected per App. One-off Task execution and Workspace memory are not forced to inherit an App's deployment choice. In v0, Task execution and durable Workspace state are local, while named remote model or service calls remain explicit. Later cloud Task execution or memory synchronization requires its own visible placement and retention choice.

### On this Mac

- generated code and platform services execute on the Mac;
- persistent App state, databases, files, secrets, logs, and history remain on the Mac or in storage explicitly selected by the user;
- remote AI models, websites, APIs, and user-selected external services may still receive the minimum data required for their task;
- schedules operate while the local runtime is available, including after window close; missed occurrences remain visible for manual retriggering and are not automatically caught up;
- the platform does not silently persist the App's operational data in its cloud.

### Always available

- generated code and platform services execute in cloud;
- App state, secrets, logs, and history are stored in the cloud deployment;
- schedules remain active independently of the Mac;
- the App can be reached from supported remote clients;
- usage, retention, export, and deletion are explicit.

The same user may operate some Apps locally and others in cloud. The first product does not implement live bidirectional synchronization between the two. Deployment or migration is explicit.

## Product principles

1. **Outcome before object type.** Start with what the user wants to accomplish; do not require them to choose an App, workflow, agent, or automation first.
2. **Assistant first, durable objects when useful.** Answer directly, use a Task for bounded one-off execution, and create an App for reuse or ongoing operation.
3. **Real software, maintained for the user.** Generate and run genuine App code, while the product manages environments, processes, versions, logs, and recovery.
## Deployment philosophy

### On this Mac

- generated code and platform services execute on the Mac;
- persistent App state, databases, files, secrets, logs, and history remain on the Mac or in storage explicitly selected by the user;
- remote AI models, websites, APIs, and user-selected external services may still receive the minimum data required for their task;
- schedules operate while the local runtime is available, including after window close; missed occurrences remain visible for manual retriggering and are not automatically caught up;
- the platform does not silently persist the App's operational data in its cloud.

### Always available

- generated code and platform services execute in cloud;
- App state, secrets, logs, and history are stored in the cloud deployment;
- schedules remain active independently of the Mac;
- the App can be reached from supported remote clients;
- usage, retention, export, and deletion are explicit.

The same user may operate some Apps locally and others in cloud. The first product does not implement live bidirectional synchronization between the two. Deployment or migration is explicit.

## Product principles

1. **Outcome before object type.** Start with what the user wants to accomplish; do not require them to choose an App, workflow, agent, or automation first.
2. **Assistant first, durable objects when useful.** Answer directly, use a Task for bounded one-off execution, and create an App for reuse or ongoing operation.
3. **Real software, maintained for the user.** Generate and run genuine App code, while the product manages environments, processes, versions, logs, and recovery.
4. **Horizontal intent, bounded capability.** Do not constrain users to a vertical; stage the technical capability envelope so it remains supportable.
5. **Useful execution before ambient observation.** Prove Tasks and Apps before passive capture or proactive behavior.
6. **Durable objects over chat residue.** Important intent, data, decisions, permissions, Task Attempts, Versions, Runs, and evidence live outside the transcript.
7. **Local and cloud are placement choices, not different products.** Keep App packages portable, bind App placement at Release, and keep memory placement independent.
8. **No silent boundary changes.** Data persistence, execution location, model/provider route, credential owner, and billing owner never change invisibly.
9. **Plain-language control.** Users see purpose, access, consequences, costs, health, and recovery without learning infrastructure vocabulary.
10. **Observable and reversible by default.** Attempts and Runs have receipts; changes have Versions; failures preserve evidence; rollback is normal.
11. **Authority is explicit.** Building, reading data, executing code, using credentials, observing, and performing consequential actions are distinct permissions.
12. **Adapters feed a trusted core.** Browser, file, email, voice, screen, and future sources do not become independent product silos.
13. **Architecture follows evidence.** Reserve stable seams for future capability without implementing every future system now.

## Explicit non-goals for the initial product

- a vertical application for one business process;
- a public consumer App-hosting platform;
- a visual workflow editor as the primary experience;
- passive screen monitoring or always-listening voice;
- automatic procedure replay based only on observation;
- unrestricted browser or desktop control;
- fully local AI inference as a launch requirement;
- support for arbitrary languages and frameworks;
- live local/cloud synchronization;
- autonomous high-impact actions without user control.

## Success measures

The first product succeeds when non-technical testers can repeatedly:

- ask for help without first choosing a product object;
- complete a useful one-off Task from text or selected files and understand its result;
- create a useful App without developer help;
- reach a working result quickly;
- understand where it runs and where its data is persisted;
- operate and correct it after creation;
- recover from failure or roll back safely;
- return to use an App for real work;
- turn a proven Task into a reusable App without starting over.

The number of Tasks, generated Apps, prompts, modalities, or future architecture components is not success by itself.
