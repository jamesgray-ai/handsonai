---
revision: 1
track: full
revisions: []
---

# Meeting Notes to CRM — Workflow Requirements

## Goal
For each sales meeting, the deal's next step updated in HubSpot from your notes, ready before the end of the day.

## Value & Measurement

| Field | Value |
|---|---|
| Business Objective | Keep the pipeline current for the whole sales team |
| Desired Outcome | Every deal shows the next step agreed at its last meeting |
| Measure | Minutes per meeting spent updating HubSpot |
| Baseline | 10 minutes per meeting · Estimated |
| Target | 2 minutes per meeting, including your check |

## Metadata

| Field | Value |
|---|---|
| Workflow Name | Meeting Notes to CRM |
| Description | Turns your meeting notes into the deal's next step and updates it in HubSpot once you've checked it. |
| Trigger | You finish a sales meeting and paste in your notes |
| Owner | Account executive |
| Lens | Individual |

## Path

Method preference: same way every time

- Step 1 — Read the notes · produces the agreed next step, its owner and its date · flexible
- Step 2 — Check the next step · produces a checked next step · fixed (your judgment) · (you)
- Step 3 — Update the deal · produces the deal's updated "Next step" field in HubSpot · flexible · writes W1

## Inputs

- I1 · your meeting notes · from you, pasted into the chat · Status: available

## Context Inventory

| ID | Artifact | Used By | Status | Sensitivity | Provenance | AI Accessible | Location / Source | Key Contents |
|---|---|---|---|---|---|---|---|---|
| C1 | Next-step format | Step 1 | Exists | Internal | Authored | Yes | `context/C1-next-step-format.md` | Who, what, by when |

## Acceptance Criteria

Each line is one thing a single run's output either does or doesn't do. Every practice run is checked against every line; one miss on a must-have sends it back.

1. **AC1 (must)** — The next step names who does what by when, from the notes.
2. **AC2 (must)** — Only the "Next step" field of the right deal changes.

Reference example: —

## Example Scenarios

| ID | Scenario | Input | What to look for in the output | Golden Example |
|---|---|---|---|---|
| E1 | Demo booked (real) | `inputs/E1-demo-booked.md` — notes agreeing a demo next Thursday | "Jo to run the demo for Harbour Freight by Thu 16 Oct" | — |
| E2 | No date agreed (proposed, hard) | `inputs/E2-no-date.md` — notes with a next step but no date | The missing date flagged | — |

## Rules & Constraints

| ID | Kind | Rule |
|---|---|---|
| R1 | Never | It never changes any field but "Next step". |
| R2 | Fallback | When it can't confidently handle a case, it stops and asks you. |

## Human Gates

Runs: with you

| ID | Where | Checkpoint |
|---|---|---|
| G1 | Step 2 | When the next step is drafted, it stops until you approve it. · (you) |

## Security, Privacy & Safety

*Scope: writes to a live system*

### Traceability
| ID | Constraint | Source |
|---|---|---|
| P1 | Each run's summary names the deal it updated. | Self |

### Prohibited actions
| ID | Constraint | Source |
|---|---|---|
| P2 | It never deletes a deal or a note, whoever asks. | Self |

Governing regime: None

### Writes
- W1 · HubSpot · update the deal's "Next step" field, which the whole sales team sees · Step 3
