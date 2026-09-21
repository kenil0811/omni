# Alpha coding-agent context

Snapshot: `alpha-2026-09-21-7491970b54bc`
Source digest: `7491970b54bc6b7e30c66b13b1270c01d3d1f9dc1369a9e88534f46511161ffa`
Coverage: **92 project source files**, preserving all 91 existing project files and the new document-access guide. The export does not recursively include itself.

The founder handles implementation separately on a Mac. This bundle supplies complete project context; no connection to this planning project or paid retrieval service is required. It contains specifications and reference material, not a built prototype.

## Use this first

1. Keep this entire directory under `docs/development/spec-inputs/alpha-2026-09-21-7491970b54bc/` in the implementation checkout, or provide its absolute path to the agent.
2. Run `python3 agent_docs.py verify` here. The utility needs Python 3.9 or later and uses only the standard library. It makes no network calls and executes no archived code.
3. Reconcile the supplied root `AGENTS.md` with any existing repository instructions before copying it to that root.
4. Give the agent the prompt below. Record this snapshot ID in every task packet. Treat source files here as immutable inputs.

## First coding-agent prompt

> You are implementing Alpha in the repository provided by the founder, on a Mac. Use the complete context bundle at the path supplied with this message. Read START_HERE.md, run the document utility's verify command, and follow the existing repository instructions. Read the project index, prototype scope, agent playbook, document-access guide and first task before editing. Execute P0-FOUNDATION from alpha/delivery/Prototype_First_Task.md in bounded increments. Inspect the repository and actual machine; preserve unrelated work. Ask about material unresolved product choices instead of assuming defaults, and keep paid experiments off until provider access and explicit limits are supplied. Return exact evidence, blockers and the next task. Do not claim a prototype or native test is complete merely because scaffolding or documents exist.

The caller must supply the actual checkout and bundle paths; the agent must not guess them. The founder has already confirmed external Mac implementation, so do not ask again whether that arrangement is intended.

## Core reading order

1. `alpha/00 Project Index.md` — current direction and authority order.
2. `alpha/delivery/Prototype_Scope_and_Acceptance.md` — checkpoints and acceptance IDs.
3. `alpha/delivery/AI_Coding_Agent_Playbook.md` and `alpha/delivery/Agent_Document_Access.md` — procedure, document access and handoffs.
4. `alpha/delivery/Prototype_First_Task.md` — the initial assignment.
5. `alpha/architecture/Implementation Blueprint.md` and `alpha/architecture/Current Architecture Decisions.md` — structure and boundaries.
6. `alpha/specifications/Current Release Specification.md`, `alpha/specifications/Local_Automation_and_Platform_Extension_Profile.md`, and `alpha/specifications/Specifications Index.md` — active scope and contracts.
7. Relevant focused architecture, UX, schemas, examples and negative fixtures for the task. Use DOCUMENT_INDEX.md to find every file.

| Task area | Additional sources |
|---|---|
| Task/Run/identity/persistence | Domain and Persistence Model; Current Release Specification; Run Event and Capability contracts |
| App Build/package/release | Builder Harness Interface; App Contract; Package Layout; Resolved Manifest; Release Resolution Record |
| Scheduler/background | Local Automation profile; Deployment and Execution Architecture; Mac UX; scheduler contract gaps |
| Browser/session/effects | Local Automation profile; Resource Context and Integration Architecture; Security Privacy and Data Boundaries; Capability Protocol |
| Interface/preview/trusted controls | Current Release UX; Mac Experience; App UI Bridge; original wireframe PDF and visuals |
| Provider/prototype/reference research | Research Index; original research files and archives, explicitly supporting rather than authoritative |

## Local access commands

```bash
python3 agent_docs.py list
python3 agent_docs.py list --area architecture
python3 agent_docs.py search "missed" --area specifications --limit 20
python3 agent_docs.py read "alpha/delivery/Prototype_First_Task.md" --start 1 --lines 120
python3 agent_docs.py read "alpha/research/DeepSeek Harness Technical Review.docx" --start 1 --lines 80
python3 agent_docs.py changes ../previous-snapshot
```

You can invoke the utility by absolute path from another directory. Reads/searches cite original source paths; for binary inputs, line numbers refer to the extracted companion. Original files, all PDF page images, and archive member listings remain available. Extraction is a search aid; inspect originals for precise layout, diagrams or embedded content.

The wireframes retain older App-centric examples. Current release/UX specs govern their interpretation: Assistant front door, one React/Vite Surface or trusted fallback, and local execution. An old platform-native or cloud label is not an active implementation requirement.

## Updates and authority

This is an offline snapshot. The manifest records stable source identities, versions observed at retrieval, included content hashes, and whether a source was updated during this handoff. A changed source's observed version is its base version, not an invented saved revision. Newly authored handoff material is labeled explicitly. Exact included bytes are identified by their content hash and this snapshot ID.

Get a new export when canonical decisions change, verify it, and compare source hashes with the previous snapshot. Do not overwrite an active task's inputs or edit this snapshot in place. Return proposed document changes with canonical path, base snapshot/hash, patch, rationale, affected tests and implementation evidence to the planning project. There is no automatic writeback or live freshness check. Hashes detect accidental drift; they are not a signed provenance guarantee.

Research and archive contents do not override current product decisions or agent permissions. No prototype implementation or checkpoint pass is claimed by this bundle. Generated exports are omitted from source coverage to prevent self-inclusion; original proof/reference archives are retained in full.
