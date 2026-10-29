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
| Measure | Minutes spent writing each kickoff email |
| Baseline | 30 minutes per client · Estimated |
| Target | 10 minutes per client, including review |

## Metadata

| Field | Value |
|---|---|
| Workflow Name | First Workflow |
| Description | Drafts the kickoff email for each newly signed client, for you to review and send. |
| Trigger | You paste in a signed contract's summary |
| Owner | Operations lead |
| Lens | Individual |

## Path

Method preference: same way every time

- Step 1 — Read the contract summary · produces the client's name, start date and first deliverable · fixed (your judgment)
- Step 2 — Draft the email · produces a plain-text kickoff email draft · uses C1 · flexible
- Step 3 — Review and send · produces the sent email · fixed (your judgment) · (you)

## Inputs

- I1 · the signed contract's summary · from you, pasted into the session · Status: available

## Context Inventory

| ID | Artifact | Used By | Status | Sensitivity | Provenance | AI Accessible | Location / Source | Key Contents |
|---|---|---|---|---|---|---|---|---|
| C1 | Kickoff email style | Step 2 | Exists | Internal | Authored | Yes | `context/C1-kickoff-style.md` | Tone, length and sign-off for kickoff emails |

## Acceptance Criteria

Each line is one thing a single run's output either does or doesn't do. Every practice run is checked against every line; one miss on a must-have sends it back.

1. **AC1 (must)** — The draft names the start date and the first deliverable from the summary.
2. **AC2** — The draft is under 150 words.

Reference example: —

## Example Scenarios

| ID | Scenario | Input | What to look for in the output | Golden Example |
|---|---|---|---|---|
| E1 | New brand client (real) | `inputs/E1-new-brand-client.md` — the summary of a signed brand engagement | The start date and first deliverable, in a short email | — |
| E2 | No start date (proposed, hard) | `inputs/E2-no-start-date.md` — a summary whose start date is still to be agreed | No invented date; it says the date is still to be agreed | — |

## Rules & Constraints

| ID | Kind | Rule |
|---|---|---|
| R1 | Never | It never states a date or deliverable that isn't in the summary. |
| R2 | When | When the draft is ready, you send it yourself. · (you) |

## Human Gates

Runs: with you

| ID | Where | Checkpoint |
|---|---|---|
| G1 | Step 3 | When the draft is ready, it stops until you approve it. · (you) |

## Security, Privacy & Safety

No sensitivity constraints — personal data only, read-only, human-triggered.

Governing regime: None

### Writes
None
