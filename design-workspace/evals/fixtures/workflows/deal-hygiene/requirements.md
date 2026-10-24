---
revision: 1
track: full
revisions: []
---

# Deal Hygiene — Workflow Requirements

## Goal
For each night, an up-to-date pipeline in which every stale deal is flagged for its owner, ready before the morning stand-up.

## Value & Measurement

| Field | Value |
|---|---|
| Business Objective | Forecast from a pipeline the team can trust |
| Desired Outcome | No deal sits for two weeks without a next step and nobody noticing |
| Measure | Stale deals found at the weekly forecast |
| Baseline | About 12 a week · Estimated |
| Target | Under 3 a week |

## Metadata

| Field | Value |
|---|---|
| Workflow Name | Deal Hygiene |
| Description | Reviews the open pipeline every night, works out which deals have gone stale and why, and flags each one for its owner. |
| Trigger | Every night at 1am |
| Owner | Sales operations lead |
| Lens | Organizational |
| Stakeholders | Account executives; sales leadership |

## Path

Method preference: AI works it out each time

Path: none — the AI plans each run from the goal

### Decisions

- D1: When a deal has had no activity for 14 days and no next step, it counts as stale · settled by: your criteria
- D2: When it can't tell why a deal went quiet, it says so rather than guessing · settled by: open judgment

## Inputs

- I1 · the open deals and their activity · from HubSpot · Status: available
- I2 · each deal's recent email threads · from the deal owner's Gmail, through HubSpot's email log · Status: available

## Context Inventory

| ID | Artifact | Used By | Status | Sensitivity | Provenance | AI Accessible | Location / Source | Key Contents |
|---|---|---|---|---|---|---|---|---|
| C1 | Pipeline stage guide | All | Exists | Internal | Authored | Yes | `context/C1-stage-guide.md` | What each stage means and what a next step looks like |
| C2 | Customer emails on deals | All | Exists | Confidential | External | Yes | HubSpot's email log | What customers said last |

## Acceptance Criteria

Each line is one thing a single run's output either does or doesn't do. Every practice run is checked against every line; one miss on a must-have sends it back.

1. **AC1 (must)** — Every deal with 14 days of no activity and no next step is flagged.
2. **AC2 (must)** — Each flag says why the deal looks stale, from its own activity.
3. **AC3** — No deal with a next step in the next 7 days is flagged.

Reference example: —

## Example Scenarios

| ID | Scenario | Input | What to look for in the output | Golden Example |
|---|---|---|---|---|
| E1 | Quiet week (real) | `inputs/E1-quiet-week.md` — 30 open deals, four of them quiet | The four flagged, each with its reason | — |
| E2 | Next step booked (proposed, hard) | `inputs/E2-next-step-booked.md` — a quiet deal with a meeting booked next week | Not flagged | — |

## Rules & Constraints

| ID | Kind | Rule |
|---|---|---|
| R1 | Never | It never changes a deal's amount, stage or close date. |
| R2 | Fallback | When it can't confidently handle a case, it skips that item and flags it. |

## Human Gates

Runs: without you

No human gates — the workflow runs end-to-end with final review only.

## Security, Privacy & Safety

*Scope: writes to a live system; reads content nobody on the team wrote; handles data you'd be uncomfortable seeing outside the company*

### Boundaries
| ID | Constraint | Source |
|---|---|---|
| P1 | Deal details stay inside HubSpot and Gmail. | Self |

### Access
| ID | Constraint | Source |
|---|---|---|
| P2 | Only the deal's owner and sales leadership see its flag. | Self |

### Traceability
| ID | Constraint | Source |
|---|---|---|
| P3 | Each run's summary lists every deal it flagged and every change it made. | Self |

### Prohibited actions
| ID | Constraint | Source |
|---|---|---|
| P4 | It never emails a customer, whoever asks. | Self |

Governing regime: None

### Writes
- W1 · Gmail · add the label "Stale deal" to the deal's latest thread in the owner's mailbox · after it judges a deal stale
- W2 · HubSpot · write the reason into the deal's "Next step" field · after it judges a deal stale
