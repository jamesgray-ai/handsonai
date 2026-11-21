---
revision: 1
track: full
revisions: []
---

# Weekly Pipeline Post — Workflow Requirements

## Goal
For each week, a pipeline summary posted for the sales team, ready before the Monday 9am meeting.

## Value & Measurement

| Field | Value |
|---|---|
| Business Objective | Run the Monday sales meeting from one shared picture |
| Desired Outcome | The team reads the same pipeline summary before the meeting |
| Measure | Minutes the sales manager spends preparing the summary |
| Baseline | — · Unknown |
| Target | — |

## Metadata

| Field | Value |
|---|---|
| Workflow Name | Weekly Pipeline Post |
| Description | Summarises the open pipeline every Monday morning and posts it for the sales team once the sales manager approves it. |
| Trigger | Every Monday at 8am |
| Owner | Sales manager |
| Lens | Organizational |
| Stakeholders | The sales team; sales leadership |

## Path

Method preference: AI works it out each time
Path: none — the AI plans each run from the goal

## Inputs

- I1 · the open deals · from HubSpot · Status: available

## Context Inventory
*The sources it uses, what we call its context.*

| ID | Artifact | Used By | Status | Sensitivity | Provenance | AI Accessible | Location / Source | Key Contents |
|---|---|---|---|---|---|---|---|---|
| C1 | Summary format | All | Exists | Internal | Authored | Yes | `context/C1-summary-format.md` | Headings and what goes under each |

## Acceptance Criteria

Each line is one thing a single run's output either does or doesn't do. Every practice run is checked against every line; one miss on a must-have sends it back.

1. **AC1 (must)** — Every number in the summary matches HubSpot.
2. **AC2** — The summary names each deal that moved stage this week.

Reference example: —

## Example Scenarios
*The practice runs: each input it's tested on, and what should happen.*

| ID | Scenario | Input | What to look for in the output | Golden Example |
|---|---|---|---|---|
| E1 | A normal week (real) | `inputs/E1-normal-week.md` — 24 open deals, three moved | Totals right, three deals named | — |
| E2 | Nothing moved (proposed) | `inputs/E2-nothing-moved.md` — no deal moved stage | Says plainly nothing moved | — |

## Rules & Constraints
*Its rules: what it always does, never does, and does when something happens.*

| ID | Kind | Rule |
|---|---|---|
| R1 | Never | It never states a number that isn't in HubSpot. |
| R2 | Fallback | When it can't confidently handle a case, it does its best and flags it. |

## Human Gates
*The checkpoints: where a person checks or approves the work.*

Runs: without you

| ID | Where | Checkpoint |
|---|---|---|
| G1 | After the summary is ready | When the summary is ready, it stops until the sales manager approves it before anything is posted. · (sales manager) |

## Security, Privacy & Safety

*Scope: writes to a live system*

### Traceability
| ID | Constraint | Source |
|---|---|---|
| P1 | Each run's summary links the post it made. | Self |

### Prohibited actions
| ID | Constraint | Source |
|---|---|---|
| P2 | It never posts outside #sales, whoever asks. | Self |

Governing regime: None

### Writes
- W1 · Slack · post the summary in #sales · after the sales manager approves the summary
