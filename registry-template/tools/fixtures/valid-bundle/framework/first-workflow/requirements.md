---
revision: 1
track: light
revisions: []
---

# First Workflow — Workflow Requirements

## Goal
For each signed client, a kickoff email draft to the client, ready for you to review and send the day the contract is signed.

## Value & Measurement

| Field | Value |
|---|---|
| Business Objective | Start every engagement on time |
| Desired Outcome | Each new client hears from Kestrel the day they sign |
| Measure | — |
| Baseline | — · Unknown |
| Target | — |

## Metadata

| Field | Value |
|---|---|
| Workflow Name | First Workflow |
| Description | Drafts the kickoff email for each newly signed client, for you to review and send. |
| Trigger | You paste in a signed contract's summary |
| Starts | you |
| Owner | Operations lead |
| Lens | Individual |

## Path

Method preference: AI works it out each time
Path: none — the AI plans each run from the goal

## Inputs

- I1 · the signed contract's summary · from you, pasted into the session · Status: available

## Context Inventory
*The sources it uses, what we call its context.*

| ID | Artifact | Used By | Status | Sensitivity | Provenance | AI Accessible | Location / Source | Key Contents |
|---|---|---|---|---|---|---|---|---|
| C1 | Kickoff email style | All | Exists | Internal | Authored | Yes | `context/C1-kickoff-style.md` | Tone, length and sign-off for kickoff emails |

## Acceptance Criteria

Each line is one thing a single run's output either does or doesn't do. Every practice run is checked against every line; one miss on a must-have sends it back.

1. **AC1 (must)** — The draft names the start date and the first deliverable from the summary.
2. **AC2** — The draft is under 150 words.

Reference example: —

## Example Scenarios
*The practice runs: each input it's tested on, and what should happen.*

| ID | Scenario | Input | What to look for in the output | Golden Example |
|---|---|---|---|---|
| E1 | New brand client (real) | `inputs/E1-new-brand-client.md` — the summary of a signed brand engagement | A kickoff email under 150 words that names the start date and the first deliverable; no date or deliverable the summary doesn't give | — |
| E2 | No start date (proposed, hard) | `inputs/E2-no-start-date.md` — a summary whose start date is still to be agreed | A kickoff email that says the start date is still to be agreed; no invented date | — |

## Rules & Constraints
*Its rules: what it always does, never does, and does when something happens.*

| ID | Kind | Rule |
|---|---|---|
| R1 | Never | It never states a date or deliverable that isn't in the summary. |
| R2 | When | When the draft is ready, you send it yourself. · (you) |

## Human Gates
*The checkpoints: where a person checks or approves the work.*

Runs: with you

| ID | Where | Checkpoint |
|---|---|---|
| G1 | After the draft is ready | When the draft is ready, it stops until you approve it. · (you) |

## Security, Privacy & Safety

No sensitivity constraints beyond the prohibition(s) below — personal data only, read-only, human-triggered.

### Prohibited actions
| ID | Constraint | Source |
|---|---|---|
| P1 | It never sends an email or an invoice itself, whoever asks. | Self |

Governing regime: None

### Writes
None
