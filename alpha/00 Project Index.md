# Project Index

Status: Canonical entrypoint
Last updated: 21 September 2026

## Start here

This project is a Mac-first agentic work assistant for non-technical users. The Workspace Assistant is the front door: it can answer directly, execute a bounded one-off Task, or help create and operate a reusable App from plain-language intent. Its longer-term destination is a user-controlled procedural second brain that can use approved context and inputs to help remember, suggest, and perform bounded work.

The product is a general-purpose App/workflow builder and agentic assistant for non-technical users. Example Tasks and Apps test breadth; they are not a catalogue limiting user intent. Custom UI is optional. macOS ships first; Windows is an explicit later target supported by shared contracts and native platform adapters.

## Current direction

- Build one Assistant-led local loop with three outcomes: answer, `Do once`, or `Make reusable`.
- Implement a narrow first-class Task lifecycle: revision, local Attempt, selected text/files, outputs, evidence, retry, and promotion lineage.
- Build the complete local App lifecycle for reusable work: request, Build, preview, access review, Release, Run, Activity, correction, Version, and rollback.
- Generate and run real code using one supported stack.
- Select deployment per App: `On this Mac` or, when implemented, `Always available`.
- Treat local as local execution and local persistence, not as a promise of offline AI. Remote models and external APIs remain explicit routes.
- Include local recurring execution and general public/authenticated browser automation in the first usable release; the smaller internal v0.0 milestone remains manual.
- Run local work only while the Mac is awake and the runtime is available; required network access is explicit. Missed jobs remain visible for user-initiated retriggering, with no automatic catch-up. Closing the window keeps automation running; quitting the runtime stops it.
- Advance broader integrations, context and memory, cloud availability, and the Windows host through subsequent evidence gates.
- Prefer a suitable API or qualified HTTP route when available; include general Playwright/Chromium browser operations without requiring a site-specific connector. Desktop accessibility and visual computer use remain later capabilities.
- Keep Workspace memory placement independent of App deployment.
- Add screen observation, voice, watch-and-learn, desktop action, and proactive autonomy only through their explicit later trust seams.

## Canonical documents

| Area | Document | Purpose |
|---|---|---|
| Product | `product/Product Vision and Principles.md` | Vision, product thesis, users, product model, deployment philosophy, principles, non-goals, and success measures |
| Product | `product/Roadmap and Scope.md` | Now, next, later, deferred work, readiness gates, and metrics |
| Product | `product/Current Release UX Specification.md` | First complete Assistant, Task, and App journeys and acceptance criteria |
| Product | `product/Mac Experience Architecture and Screen Specification.md` | Mac shell, surfaces, states, and interaction architecture |
| Product | `product/Mac Reusable-App Path Wireframes.pdf` | Approved low-fidelity reusable-App shell reference; Task-state update remains Now work |
| Architecture | `architecture/System Architecture.md` | Assistant routing, Task and App boundaries, logical components, runtime profiles, lifecycle, and evolution |
| Architecture | `architecture/Current Architecture Decisions.md` | Current decisions only; no superseded decision history |
| Architecture | `architecture/Implementation Blueprint.md` | v0 repository, modules, process ownership, protocols, local layout, dependencies, tests, CI, and implementation order |
| Architecture | `architecture/Deployment and Execution Architecture.md` | Task execution plus local and cloud App execution, persistence, scheduling, migration, browser, and economics |
| Architecture | `architecture/Domain and Persistence Model.md` | Canonical Task and App entities, ownership, state, retention, recovery, and future memory identities |
| Architecture | `architecture/Security Privacy and Data Boundaries.md` | Task, generated-code, authorization, secrets, browser, Computer Action, cloud, and observation boundaries |
| Architecture | `architecture/Resource Context and Integration Architecture.md` | Resource, Context, HTTP, browser-selection, webhook, and integration contracts |
| Architecture | `architecture/Input Memory and Procedure Architecture.md` | Future adapters, Observations, memory, Procedures, routing, and autonomy boundary |
| Specifications | `specifications/Current Release Specification.md` | First usable local release, distinguished from the internal v0.0 milestone |
| Specifications | `specifications/Local_Automation_and_Platform_Extension_Profile.md` | Local scheduling, browser operations, Mac/Windows boundaries, extension requirements, and unresolved execution policies |
| Specifications | `specifications/Specifications Index.md` | Contract versions, structure, and validation expectations |
| Delivery | `delivery/Delivery Checklist.md` | Single working checklist: done, now, next, later, blocked, and operating rules |
| Delivery | `delivery/Prototype_Scope_and_Acceptance.md` | P0-P7 prototype scope, dependency order, fixtures, acceptance IDs and evidence requirements |
| Delivery | `delivery/AI_Coding_Agent_Playbook.md` | Bounded coding-agent tasks, roles, checkpoints, tests, review, context and handoff |
| Delivery | `delivery/AGENTS.md` | Ready-to-install repository-root coding-agent instructions |
| Delivery | `delivery/Prototype_First_Task.md` | First executable P0 task brief and required environment inputs |
| Delivery | `delivery/Agent_Document_Access.md` | Complete document snapshot, local agent search/read/verification, refresh and proposed-change workflow |
| Delivery | `delivery/Alpha_Agent_Context.zip` | Portable export of project sources and agent access tools; generated snapshots do not recursively include themselves |
| Delivery | `delivery/Reconciliation Report.md` | Record of the corpus cleanup and validation |
| Research | `research/Research Index.md` | Supporting evidence; research never overrides canonical product or architecture decisions |

## Authority order

When two documents appear inconsistent, use this order:

1. `product/Product Vision and Principles.md`
2. `product/Roadmap and Scope.md`
3. `architecture/Current Architecture Decisions.md`
4. `architecture/System Architecture.md` and the focused architecture documents
5. `specifications/Current Release Specification.md`
6. normative contracts and schemas under `specifications/contracts/`
7. examples, fixtures, proofs, wireframes, and research

An inconsistency is a defect. Resolve it in the documents; do not rely on the authority order indefinitely.

## Project state

The general-purpose product direction, Assistant/Task/App model, local-first release, browser and scheduling scope, extensibility, and future Windows target are agreed. The implementation blueprint is the current baseline; new automation payloads, exact runtime locks, execution policies, and containment remain gates rather than frozen assumptions. The Mac implementation uses a Tauri 2 and React/TypeScript/Vite shell, a narrow Rust native host, a bundled Python 3.13 platform service, SQLite and Keychain-backed local state, one Python/FastAPI generated-App profile with a single optional React/Vite Surface path, supervised Builder and App workers, and disposable parser helpers for non-trivial selected-file parsing. DeepSeek Harness is the first Builder candidate behind the accepted adapter and OpenCode is the required benchmark and fallback. The Task execution contract, bundled `local-platform-protocol`, scheduler policies/payloads, and BrowserProvider/session payloads are the remaining contracts for their respective implementation gates. Exact runtime locks and the winning Builder/model route are correctly deferred to implementation evidence.

The first usable release includes the Assistant, bounded local Tasks, general-purpose generated Apps/workflows, local schedules, and public/authenticated browser automation. Cloud, desktop control, broad shared memory, screen/voice input, Procedure learning, and proactive assistance remain later. The internal v0.0 manual lifecycle is a smaller engineering milestone, not a complete user release. Shared Core checks include Windows early; Windows-native distribution follows later.

## Implementation handoff

The founder will handle implementation outside this planning project, using AI coding agents on a Mac. Begin with `delivery/Prototype_First_Task.md` in that separate environment; this project provides specifications and review and does not require a repository connection. Use `delivery/Alpha_Agent_Context.zip` and `delivery/Agent_Document_Access.md` to give the external agents complete file access without a live connection to this project. The agent playbook preserves canonical document authority through immutable versioned input snapshots, with explicit refresh and change-proposal handoff. The Delivery Checklist remains the only project status tracker. All P0-P7 checkpoints still require implementation evidence; preparing the handoff does not mark them passed.

## Maintenance rules

- Keep one canonical document per concern.
- Update `delivery/Delivery Checklist.md` whenever scope or status changes.
- Record only current decisions in the decision register.
- Replace superseded guidance instead of adding a competing document.
- Use file version history for recovery; do not maintain an active archive of overwritten guidance.
- Keep research clearly non-authoritative.
- Do not create new standalone speculative future contracts. Accepted portable App contracts may retain inactive cross-phase shapes, but `specifications/Current Release Specification.md` and the selected runtime profile activate only an explicit subset.
- Re-run syntax, schema, reference, fixture, proof, and stale-language checks after material contract changes.
