# Mac Reusable-App Path Wireframes

## Page 1 / Scope

Status: Reusable-App shell and lifecycle reference. Scope updated 21 September 2026.

Current release: General-purpose Apps and workflows, local schedules, and public/authenticated browser automation. Custom interfaces are optional. macOS first; Windows later.

Local availability: The Mac must be awake and the runtime running. Automation continues after window close. Missed jobs remain visible for manual retriggering; there is no automatic catch-up. Explicit runtime quit stops local work. Network access is required when needed.

Still to prototype: Workspace Assistant and Task journeys; schedule activation and missed-run recovery; browser sign-in, takeover, resume/stop, and uncertain-effect recovery.

Later examples: Cloud availability, device-wait, broad connector/notification features, desktop control, and ambient memory remain later capabilities.

The following eight wireframes preserve the existing App shell and lifecycle reference.
New automation states require focused prototypes before implementation sign-off.

Scope revision: local automation and platform extensibility

## Page 2 / Wireframe 01 "Approved primary shell"

01 Approved primary shell
Review focus: App tree, App tabs, collapsed Builder

Acme Workspace v    Opportunity Monitor

Apps +

v RESEARCH
- Opportunity Monitor (1)
- Competitor Watch

v OPERATIONS
- Invoice Reconciliation (!)
- Outreach Assistant (12)

v UNFILED
- New App

Opportunity Monitor
Monitors approved sources and keeps a searchable opportunity history.
[Edit with AI] [Run now] [ACTIVE]
BUILDER

App  Manage  Activity

Opportunities
Search records

Company               Match       Source          Updated
Northstar Packaging   Strong      DealSource      Today 09:07
Beacon Analytics      Strong      MarketList      Today 09:06
Cedar Health Services Possible    PrivateMarket   Today 09:05
Riverside Components  No match    DealSource      Today 09:03

LOW-FIDELITY WIREFRAME - APPROVED APP-FIRST SHELL

## Page 3 / Wireframe 02 "New App and evolving Build Brief"

02 New App and evolving Build Brief
Review focus: creation stays inside an App draft

Acme Workspace v    New App

Apps +

v RESEARCH
- Opportunity Monitor (1)
- Competitor Watch

v OPERATIONS
- Invoice Reconciliation (!)
- Outreach Assistant (12)

v UNFILED
- New App

New App [DRAFT]
Describe the outcome; implementation choices remain hidden.

App  Manage  Activity

Check these websites every Monday, extract new listings into searchable history, and alert me when a listing matches my criteria.

BUILD BRIEF

Outcome
Searchable history with match alerts
Ready

Interface
Table, filters, record detail
Proposed

Inputs
Websites and match criteria
Needs answer

Recurring work
Every Monday at 09:00
Assumed

Access
Read sources and write App data
Review later

Test
Two sources and five records
Ready

BUILDER
New App

I understand the outcome.
Which sources require sign-in before I test them?

Describe a change or ask a question...
[Send]

LOW-FIDELITY WIREFRAME - APPROVED APP-FIRST SHELL


## Page 4 / Wireframe 03 "Build progress and candidate preview"

03 Build progress and candidate preview
Review focus: working result before publication

Acme Workspace v    Opportunity Monitor

Apps +

v RESEARCH
- Opportunity Monitor (1)
- Competitor Watch

v OPERATIONS
- Invoice Reconciliation (!)
- Outreach Assistant (12)

v UNFILED
- New App

Opportunity Monitor
Candidate version 1 with sample data.
[Publish] [Request changes] [PREVIEW]

App  Manage  Activity

BUILD
- Designing App
- Preparing interface
- Connecting sources
- Testing sample
o Checking access
o Preview ready

New opportunities
5 sample records

Northstar Packaging   Strong
Beacon Analytics      Strong
Riverside Components  No
Cedar Health Services Possible

Preview review
Working output, two assumptions, no publication yet

BUILDER
Opportunity Monitor

The sample run found five records.
Two assumptions still need review before publication.

Describe a change or ask a question...
[Send]

LOW-FIDELITY WIREFRAME - APPROVED APP-FIRST SHELL


## Page 5 / Wireframe 04 "Generated App surfaces"

04 Generated App surfaces
Review focus: native and custom UI inside the same App tab

Acme Workspace v    Opportunity Monitor

Apps +

v RESEARCH
- Opportunity Monitor (1)
- Competitor Watch

v OPERATIONS
- Invoice Reconciliation (!)
- Outreach Assistant (12)

v UNFILED
- New App

Opportunity Monitor
The generated interface owns this tab; the shell remains stable.
[Edit with AI] [Run now] [ACTIVE]

App  Manage  Activity

PLATFORM-NATIVE
Opportunity table

Northstar Packaging   Open
Beacon Analytics      Open
Cedar Health Services Open

Standard table, record and evidence patterns

ISOLATED CUSTOM UI
Reconciliation workspace

[Source file] [Target file] [Run]

Exceptions
Amount mismatch   Review
Missing invoice   Review
Duplicate line    Review

Custom layout; same Bridge and trusted controls

BUILDER

LOW-FIDELITY WIREFRAME - APPROVED APP-FIRST SHELL

## Page 6 / Wireframe 05 "App Activity and Run detail"

05 App Activity and Run detail
Review focus: traceability stays inside the selected App

Acme Workspace v    Opportunity Monitor

Apps +

v RESEARCH
- Opportunity Monitor (1)
- Competitor Watch

v OPERATIONS
- Invoice Reconciliation (!)
- Outreach Assistant (12)

v UNFILED
- New App

Opportunity Monitor
Runs, approvals, errors, and changes for this App.
[ACTIVE]

App  Manage  Activity

RUNS

Run 1842
Completed - review

Run 1841
Waiting for approval

Run 1840
Completed

Run 1839
Failed

Run 1842
Completed - needs review

14 records added; one source skipped

TIMELINE

- 09:00 Started by schedule
- 09:02 Two sources opened
- 09:05 14 records written
- 09:07 Completed

Evidence: sources, changes, screenshots, model use, receipts

BUILDER
Run 1842

Run 1842 finished with one source skipped.
Its sign-in expired. I can guide you through repair.

Describe a change or ask a question...
[Send]

LOW-FIDELITY WIREFRAME - APPROVED APP-FIRST SHELL

## Page 7 / Wireframe 06 "Manage - Access and approval"

06 Manage - Access and approval
Review focus: plain-language authority within the App

Acme Workspace v    Opportunity Monitor

Apps +

v RESEARCH
- Opportunity Monitor (1)
- Competitor Watch

v OPERATIONS
- Invoice Reconciliation (!)
- Outreach Assistant (12)

v UNFILED
- New App

Opportunity Monitor
Access, configuration, versions, and App-specific connections.
[ACTIVE]

App  Manage  Activity

Access
Configure
Versions

Access

This App reads three approved websites, writes only to its own data, runs every Monday, and sends internal alerts. It cannot contact companies or access other Apps.

Reads                                       3 websites - 2 signed in
Writes
External actions
Schedule and budget

Approval required
Allow this App to send an internal alert after each matching run?

Recipients: Workspace opportunity team

[Cancel] [Approve]

BUILDER

LOW-FIDELITY WIREFRAME - APPROVED APP-FIRST SHELL

## Page 8 / Wireframe 07 "Correction and version comparison"

07 Correction and version comparison
Review focus: safe evolution through a candidate

Acme Workspace v    Opportunity Monitor

Apps +

v RESEARCH
- Opportunity Monitor (1)
- Competitor Watch

v OPERATIONS
- Invoice Reconciliation (!)
- Outreach Assistant (12)

v UNFILED
- New App

Opportunity Monitor
[Publish candidate] [Keep current] [CANDIDATE]
Candidate version 8 created from a record correction.

App  Manage  Activity

Behavior change

CURRENT - VERSION 7
Missing price -> 0

CANDIDATE - VERSION 8
Missing price -> Unknown

Regression replay

18 recorded examples replayed
18 passed - compatible output - no new access

Change summary

Behavior                One extraction rule changed
Data                    No migration
Access                  No change
Cost                    No material change

BUILDER
Record correction

Correction captured.
Missing asking price will now remain Unknown. Regression tests passed.

Describe a change or ask a question...
[Send]

LOW-FIDELITY WIREFRAME - APPROVED APP-FIRST SHELL

## Page 9 / Wireframe 08 "Manage - Connections and this Mac"

08 Manage - Connections and this Mac
Review focus: App-scoped recovery and device access

Acme Workspace v    Invoice Reconciliation

Apps +

v RESEARCH
- Opportunity Monitor (1)
- Competitor Watch

v OPERATIONS
- Invoice Reconciliation (!)
- Outreach Assistant (12)

v UNFILED
- New App

Invoice Reconciliation
One approved device capability is currently unavailable.
WAITING

App  Manage  Activity

Access
Configure
Versions

Connections used by this App

Accounting workspace
Healthy - used today

Approved Invoices folder
Waiting for this Mac

Waiting for this Mac
Invoice Reconciliation needs the approved Invoices folder on Kenil's Mac. Cloud work is preserved; no files move until this Mac reconnects and confirms access.
[Review on this Mac]

First transfer disclosure
Shows what leaves this Mac, why this App needs it, and whether consent can be remembered.

LOW-FIDELITY WIREFRAME - APPROVED APP-FIRST SHELL
```
