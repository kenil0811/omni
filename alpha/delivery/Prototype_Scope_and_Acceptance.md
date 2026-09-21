# Prototype Scope and Acceptance

Status: Execution plan for the approved local prototype; implementation and qualification pending
Revision: 1
Last updated: 21 September 2026

## Objective

Prove that a non-technical person can describe useful work, receive a working reusable App, inspect it, run it again, and correct it without maintaining code or using a terminal. Prove that the same platform supports a materially different App without domain-specific changes to Core.

The prototype is a general-purpose framework, not a scraper product or a catalogue of approved workflows. Collection, file processing, and a tracker are evaluation cases. Assistant answers and bounded one-off Tasks remain part of the first usable release. Custom App UI is optional. The long-term second brain remains the destination, not a prerequisite for this prototype.

This document owns prototype sequence and acceptance identifiers. `Delivery Checklist.md` remains the only project status tracker. `../architecture/Implementation Blueprint.md` owns structure and technology. `../specifications/Current Release Specification.md` and its referenced contracts own runtime behavior. `AI_Coding_Agent_Playbook.md` owns implementation-agent procedure. A conflict is reported and resolved; this plan does not silently override those documents.

## Three distinct completion claims

| Claim | Required result | Insufficient evidence |
|---|---|---|
| Internal v0.0 lifecycle | P0-P3: real host/Core/storage/workers, Assistant/Task path, deterministic conforming Builder, one complete manual App lifecycle | A standalone SDK double, toy manifest, static UI, or only unit tests |
| Integrated local prototype | P0-P6: real model and Builder integration, three materially different Apps and Tasks, local schedules, public/authenticated browser work, correction and recovery | A hardcoded fixture selected by prompt keywords, only fake adapters, or only an unbundled developer launch |
| Ready for external testers | P7 in addition to the integrated prototype: qualified local containment, protected sessions, encryption/recovery, signed distribution and user acceptance | An internal same-user demo or a developer-supervised happy path |

P0-P6 may use synthetic fixtures and dedicated test accounts. External use, sensitive inputs, production browser sessions, and public distribution require their existing gates. Passing a subset must be reported by its exact claim, never simply as "the prototype is done."

## Scope

| Required for the integrated prototype | Deliberately later |
|---|---|
| Mac host; local runtime and durable state; shared Core/contract checks on Windows | Windows-native product, installers and native qualification |
| Assistant front door; answer, bounded Task, or reusable App | Ambient capture, voice, proactive autonomous execution |
| Real generated Python; optional React/Vite Surface or trusted results UI | Additional generated runtime families, plugin marketplace |
| Build, preview, access review, Version, Release, Run, Activity, correction, rollback | Cloud execution, device bridge, local/cloud synchronization |
| App-scoped table/file Resources, selected input, Artifacts and provenance | Shared cross-App memory, general Resource migration engine |
| Reviewed HTTP profile and general BrowserProvider operations | Desktop accessibility/visual computer use and connector catalogue |
| Dedicated browser sign-in, takeover, resume/stop and session-expiry recovery | Importing everyday-browser sessions by default |
| Durable local schedules, missed-job history and manual retriggering | Automatic catch-up or replay of missed jobs |
| Automation continues after window close; explicit runtime quit stops work | An implicit promise to wake the Mac or run while it is off |

The Mac must be awake and the runtime running; required network routes must be available. Future eligible occurrences proceed normally. Missed work does not execute on wake, reconnect, restart, or window reopen. Starting at login remains a separate unresolved preference.

## Reference journeys and fixtures

Fixture data is synthetic, versioned, resettable, and independent of the generated App. Fixture choices below are test inputs, not product defaults or restrictions. The verifier owns expected results separately from Builder-generated tests. Every real-generation evaluation retains the prompt, fixture revision, model/adapter versions, final package digest, attempts, corrections, actual usage and all failures.

### APP-COLLECT: first real App journey

Request: collect records from selected sources, normalize and deduplicate them, store them, apply a user-specified rule, and make the results inspectable. Create recurring execution only after preview and trusted schedule/access review.

Use a controlled public test site, then an authenticated variant that requires user sign-in. Implement those sites in the testkit; they are test environments, not production connectors. Include navigation, pagination, selectors, changed markup and transfer fixtures. After local provider tests, use an explicitly selected public site or owned test deployment for a real-network check; localhost success alone does not establish external browser compatibility.

The deterministic dataset starts with 12 source rows: eight distinct valid records, two duplicates and two invalid records. The expected output is eight records and two explained invalid-row results, with provenance. A second snapshot adds two distinct valid records and changes one existing record under an explicit fixture rule: expected current records become ten, with no duplicate creation. Computed results are independently checked. These values belong to fixture assertions, never special cases in Core or the generated App.

Required journey:

1. Describe the work in the Assistant and clarify material ambiguity.
2. Review the Build Brief and bounded Build plan; generate a candidate using a real Builder.
3. Validate and preview against disposable fixture state; a failed preview does not change the active Release or production data.
4. Review local execution, selected routes/accounts, data, effects and limits; release through trusted controls.
5. Run, inspect structured results and evidence, close/reopen the window, and find the same App and state.
6. Apply a plain-language correction to the processing rule; obtain a new candidate Version and compare it before activation.
7. Roll back code through the Release lifecycle without pretending this rolls back Resource data.
8. Activate a local schedule and observe a new occurrence running through the ordinary Run path.
9. Make execution unavailable across an occurrence; return and see a missed job with time and reason. Confirm no automatic catch-up. Retrigger it later and inspect the linked Run.
10. Exercise sign-in expiry, human takeover, stopped page structure and uncertain external effects using the controlled authenticated variant.

APP-COLLECT must remain useful without custom UI. An optional generated UI cannot hide missing platform configuration, results or Activity support.

### APP-FILES: different data and execution shape

Selected synthetic files -> validation/transformation -> reviewable records and exception output -> saved/exported report. Reopen with state intact; revise a transformation through a Build; preserve selected source files when deleting the App. At least one supported non-trivial document format exercises the parser-helper boundary; unsupported formats are explained. Do not imply support for every document type.

### APP-TRACKER: interactive shape

A generated React/Vite tracker supports create, edit, declared filters, summaries and reopen. Exercise optimistic revision conflicts and a UI/logic-only correction over compatible stored data. Test an incompatible schema change as an explicit rejected/blocked path; do not quietly add the deferred general migration framework to satisfy the fixture.

### TASK-REPORT, TASK-EXTRACT and TASK-COMPARE

Use the existing three Task families: selected documents to an evidence-backed report; semi-structured input to a validated table plus exceptions; comparison/synthesis of selected sources. The bounded Task Runner uses fixed tools and never creates a hidden App. Exercise cancellation, a new Attempt for retry, a new Revision for changed intent, reopen and promotion into a Build without transferring authority.

### NOVEL-REQUEST

After implementation is frozen for an evaluation, supply a materially different request and changed fixture data. It should produce a working App using available capabilities or explain a specific missing capability. An honest unsupported result passes the capability-boundary assertion but does not count as successful breadth. Do not modify Core with a fixture-specific handler to manufacture a pass.

## Build order and checkpoint exits

The P identifiers refine the blueprint's existing implementation phases. They do not create a second architecture or status list. Each checkpoint uses the evidence and review procedure in the playbook. A failing dependency blocks dependent integration; it does not block unrelated authorized work.

| Checkpoint | Dependencies and work | Exit evidence |
|---|---|---|
| P0 - executable foundation | Confirm repository and Mac test environment; load versioned canonical inputs; define Task/Attempt and atomic local-platform contracts; initialize only needed monorepo paths, locks, contract generation and CI; define test fixtures and policy/budget inputs | Clean setup on a declared machine; structural/semantic negative fixtures; clean regeneration; enforced dependency rules; Mac/Windows test matrix; explicit decision register; no fabricated service stubs counted as behavior |
| P1 - trusted skeleton | P0 protocol gate; Launch uses bundled Python, authenticates private IPC, bootstraps Workspace, relays durable events, supervises a real worker; minimum necessary SQLite/Artifact infrastructure | Packaged Mac launch, durable event survives restart, rejected invalid/unauthenticated message, killed process tree, event reconnect without duplicated state; no reliance on user-installed runtimes |
| P2 - Assistant and bounded Task | P0 Task gate and P1; answer/disposition, text/JSON Task first, then helper for chosen complex-file fixture; fake model control followed by one authorized real route | TASK-REPORT vertical path, evidence/outputs, cancel/retry/revise/reopen/delete/promotion; no hidden App or inherited authority; later breadth completes at P6 |
| P3 - deterministic App lifecycle | P1 and accepted App contracts; P2 promotion integration; conforming fake Builder through real worker; validate/compile/seal/preview/release/run; minimum Resources, Activity, correction and rollback | One complete file App, immutable Version identity, preview isolation, real storage and process evidence, valid package, denied invalid package; P0-P3 establish internal v0.0 only |
| P4 - real construction and repair | P3 for integration; implement DeepSeek and OpenCode against one interface; run identical authorized creation/correction/repair/cancel cases and retain cost/quality failures | Real candidate packages pass platform and independent fixture checks; no manual source patch concealed as Builder success; preliminary scorecard. Browser-dependent scores and final default selection wait for P5 |
| P5 - local automation | P1/P3 runtime foundation; approved scheduler and browser contracts before activation; real Builder from P4 for integrated journey | APP-COLLECT public/authenticated variants; BROWSER and SCHEDULE cases below; real background lifecycle; complete both Builder scorecards on automation cases before selecting the default |
| P6 - breadth and packaged recovery | P2-P5; all three Tasks/Apps, NOVEL-REQUEST, failure injection, clean packaging, shared windows CI, diagnostics and bounded resource usage | Complete acceptance matrix with exact build/machines, no terminal during user journeys, retained results and limitations; integrated local prototype claim only |
| P7 - external-test readiness | P6 plus qualified local containment, session protection, encryption/key recovery, signing/notarization/update/rollback, approved onboarding and diagnostic export | External-test gate evidence, approved distribution, direct non-technical-user observation and remaining failure report; never infer user adoption from engineering tests |

P0 may implement schema validators, fixtures and build tooling needed to make its gate executable. It does not require the product to exist before repository initialization. Each later ticket adds only the modules needed by its vertical slice; a directory diagram is not an instruction to create every folder up front.

## Early feasibility experiments

These may occur before P3, under a bounded task packet with approved environment and cost. They are time/attempt/budget limited experiments, not a second product implementation. Extract only exercised interfaces and verified code into the product.

| Experiment | Question | Minimum evidence and consequence |
|---|---|---|
| EXP-PACKAGE | Can the selected Host/Core/runtime boundary package and launch on the available Mac? | Exact machine/OS/artifact versions; launch and restart; identify native/toolchain blockers before broad UI work |
| EXP-BUILDER | Can each candidate generate and repair a conforming small App? | Same fixture and limits, real provider receipts and artifact; do not pick a winner from mocked output |
| EXP-BROWSER | Can packaged Chromium support dedicated sign-in, general operations and human takeover behind the provider boundary? | Controlled public/authenticated fixture, expiry and cleanup; do not import production sessions |
| EXP-CONTAIN | Can a local boundary constrain generated code and protect browser sessions? | Explicit attack cases and actual denial evidence; if it fails, keep the build internal and reconsider the boundary rather than silently switching to cloud |

Early EXP results do not replace integrated checkpoints. A failed feasibility result can justify a proposed architecture change with evidence; an agent cannot rewrite the accepted design merely to make its experiment pass.

## Acceptance matrix

Every row is required by its checkpoint. Expected negatives pass only when the intended denial and preserved state are observed. "Not run," an unavailable machine, a missing credential or a mocked provider is not a pass for an integration requirement.

| ID | Required observation | Gate |
|---|---|---|
| CONTRACT-01 | Valid complete records pass; malformed/unknown authority fields and semantic-invalid references fail with defined errors; generated code regenerates without drift | P0 onward |
| HOST-01 | Exact packaged Host/Core handshake succeeds; wrong version/token, oversized input and unregistered worker launch fail without secret leakage | P1 |
| HOST-02 | Core crash, event gap and reconnect preserve durable state; worker cancellation terminates descendants; reopening does not create a second Core/scheduler | P1; scheduler repeat P5 |
| TASK-01 | Bounded Task produces expected Artifact/evidence; retry and revision have distinct identities; promotion carries provenance but no grant; deletion preserves external source files | P2 |
| TASK-02 | Ambient file, generated-code, browser, shell and external-write attempts are refused; malformed/over-limit complex input is contained by the helper | P2 |
| APP-01 | Conforming package traverses Build -> Preview -> Version/Release -> Run -> results; user-selected input, intended outcome and evidence remain linked | P3 |
| APP-02 | Failed Build/preview cannot replace the active Release or mutate its data; Versions are immutable; correction creates new Version; rollback preserves data and checks compatibility | P3 |
| SURFACE-01 | Generated UI has no Tauri privileges; invalid origin, source window, nonce, method or payload is rejected; trusted fallback works with no custom UI | P3/P6 |
| BUILDER-01 | Real creation, correction and repair work through the same adapter contract; all attempts/costs retained; fake output is clearly labeled; no direct publication authority | P4/P5 |
| DATA-01 | Independent fixture oracle matches counts, values, provenance and deduplication across repeated runs; restart preserves state; wrong digest/partial write is detected | P3/P5 |
| BROWSER-01 | General navigation/extraction/click/form/upload/download operations work on controlled sites through scoped SDK handles; a new site needs no Core connector | P5 |
| BROWSER-02 | User signs in within a dedicated profile; expiry/MFA requires visible takeover; resume rechecks authority; no cookie/profile/debugging endpoint reaches generated code, package or normal logs | P5; hostile-code protection qualified P7 |
| BROWSER-03 | Stop and revocation prevent new operations; denied destination/redirect/file scope stays denied; a timed-out submit with uncertain completion is not blindly repeated | P5 |
| SCHEDULE-01 | A due enabled occurrence admits ordinary Release-bound work; repeated delivery does not duplicate logical admission; approved timezone/overlap/offline semantics are honored | P5 |
| SCHEDULE-02 | Closing the main window preserves an active Run and later scheduled dispatch; reopen attaches to the same runtime; explicit quit stops local execution | P5, actual Mac |
| SCHEDULE-03 | Sleep/quit/unavailable interval yields visible missed occurrence(s) with intended time/reason; wake/reconnect/restart performs zero automatic catch-up; future eligible occurrences continue | P5 |
| SCHEDULE-04 | Later manual retrigger links to missed history, rechecks current authority and deduplicates repeated request delivery; revoked/paused/changed Release and unavailable-input cases follow the approved contract | P5 |
| RECOVERY-01 | Crash before/after admission, cancelled worker, locked SQLite, interrupted Artifact, failed migration and state revision preserve defined invariants; uncertain effects remain visible | P6 |
| PORTABLE-01 | Shared Core/contracts/path tests pass on Windows; Mac-only imports remain isolated; incompatible App dependencies are reported; no Windows-native readiness claim | P0 onward; P6 evidence |
| PACKAGE-01 | Clean locked build and managed toolchain inventory; install, launch, preview, Run, close/reopen and quit on each claimed Mac architecture without developer runtimes | P6; signed/update checks P7 |
| BREADTH-01 | Three Task families and three materially different Apps work through shared lifecycle; at least one no-UI App and one generated UI; holdout request reported honestly | P6 |
| USER-01 | A person outside implementation completes the journeys without shell/source intervention; record interventions, failures and understanding of background/missed-job behavior | P7 before external-ready claim |
| TRUST-01 | Generated-code filesystem/network isolation, Cross-App/session separation, encryption/key recovery and distribution controls pass actual boundary tests | P7 |

Testing authority is layered: SDK-denial tests at P2/P5 prove mediated behavior. They do not prove hostile same-user Python is contained. TRUST-01 is separately required before real sensitive inputs or external distribution.

## Evaluation and evidence rules

Deterministic correctness is binary: every required invariant passes; unresolved data loss, duplicate effect, authorization bypass, missing cancellation or corrupted lineage blocks the affected gate. A flaky rerun does not erase the failure. Preserve the failing seed and fix or explicitly block it.

Builder evaluation uses identical fixture requests and declared limits for both candidates. At minimum report a clean create, a requested correction and an induced repair for each App family. Set the actual run count and spending cap before credentialed runs; do not silently spend to reach a flattering success rate. A single successful attempt establishes feasibility only. Publish all attempts and separate model/harness repair from developer source intervention. Select a default only after the required scorecard and hard gates; if neither passes, record neither as qualified. Retain the other conforming adapter as a tested fallback if it clears the minimum gate; an unqualified adapter is not a working fallback.

Measure launch/first-progress latency, Build-to-preview time, App cold start, idle and peak memory, package size, disk growth, cancellation latency, model tokens and provider cost on named machines. Product performance targets and numeric spend limits remain decisions; fixture-local timeout values must be explicitly labeled and cannot become commercial defaults by accident.

Each checkpoint evidence bundle contains base/final commit, input-spec identities, machine/OS/toolchain, exact commands and exit codes, test cases and raw sanitized results, package/fixture hashes, recording where useful, failures/skips, limitations and reviewer disposition. Keep credentials, real browsing state and personal source data out of the bundle. See the playbook for the compact handoff format.

## Confirmed handoff arrangement

Coding will be managed by the founder outside this planning project, using AI coding agents on a Mac. Repository selection and access are handled in that coding environment and are not a blocker to this project's planning work. The receiving agent records the actual repository, hardware, OS, toolchains and CI capabilities during P0. No implementation or test pass is inferred from this confirmation.

## Remaining decisions and coding-environment checks

| Input or decision | Needed before | Safe work while pending |
|---|---|---|
| Founder-managed repository, existing instructions and baseline; inspect in the separate coding environment | Repository mutation there | Planning and document review here need no repository connection |
| Mac development environment; inspect actual hardware/OS and any additional runners or testable architectures | Native/package qualification | Implement in the supplied Mac environment; report additional unavailable checks honestly |
| Approved model/provider access and explicit experiment spend cap | Any paid or credentialed live experiment | Deterministic fakes, local fixtures and uncredentialed contract work |
| Scheduler cadence/timezone/DST, overlap/offline rules, retrigger Release/input selection and retry limits | Scheduler activation | Contract options and independent test scenarios; no hidden defaults |
| Browser session sharing/locks, takeover/effect payloads and provider bounds | Browser integration | Dedicated synthetic fixture experiment under a declared temporary profile |
| Background-control and login-start presentation | Final lifecycle UX | Window-close continuation and explicit quit are already decided |
| Containment choice, onboarding model billing and external distribution route | External testing | Internal synthetic prototype only |

Bring concrete options and implications when a decision becomes necessary. Do not ask the founder to select routine file names, internal helper functions or test tooling already fixed by the blueprint. Do not start dependent behavior before an unanswered material product choice is resolved.

## Next executable handoff

Use `Prototype_First_Task.md` for P0. `Agent_Document_Access.md` explains how to install, search, verify and refresh the complete Alpha_Agent_Context.zip input snapshot in the separate Mac coding environment. Install `AGENTS.md` at the authorized repository root after reconciling existing instructions. The first task ends with a reviewable foundation and an explicit remaining decision list; it does not implement the entire product in one agent session.
