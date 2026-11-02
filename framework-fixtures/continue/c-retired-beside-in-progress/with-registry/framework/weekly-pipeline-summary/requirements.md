---
revision: 1
track: light
revisions: []
---

# Weekly Pipeline Summary — Workflow Requirements

## Goal
For each week, a one-page Markdown summary of open deals for you, ready to review before the Monday sales meeting.

## Value & Measurement

| Field | Value |
|---|---|
| Business Objective | Run a shorter, better-prepared Monday sales meeting |
| Desired Outcome | You walk into Monday's meeting knowing which deals moved and which are stuck |
| Measure | Minutes spent preparing the summary each week |
| Baseline | 60 minutes a week · Estimated |
| Target | 10 minutes a week, including review |

## Metadata

| Field | Value |
|---|---|
| Workflow Name | Weekly Pipeline Summary |
| Description | Summarises your open deals every Friday from HubSpot, for you to review before the Monday sales meeting. |
| Trigger | Every Friday afternoon, you ask for this week's summary |
| Owner | Sales lead |
| Lens | Individual |

## Path

Method preference: same way every time

- Step 1 — Pull the open deals · produces a list of open deals with stage and close date · fixed (your judgment)
- Step 2 — Write the summary · produces a one-page Markdown summary · uses C1 · flexible
- Step 3 — Review it · produces the reviewed summary · fixed (your judgment) · (you)

## Inputs

- I1 · this week's open deals · from HubSpot, through the HubSpot connection · Status: available

## Context Inventory

| ID | Artifact | Used By | Status | Sensitivity | Provenance | AI Accessible | Location / Source | Key Contents |
|---|---|---|---|---|---|---|---|---|
| C1 | Last quarter's summary | Step 2 | Exists | Internal | Authored | Yes | `context/C1-last-quarter-summary.md` | The layout and headings the summary follows |

## Acceptance Criteria

Each line is one thing a single run's output either does or doesn't do. Every practice run is checked against every line; one miss on a must-have sends it back.

1. **AC1 (must)** — Every open deal over $10,000 appears with its stage and close date.
2. **AC2 (must)** — The summary states no figure that isn't in HubSpot.
3. **AC3** — The summary fits on one page.

Reference example: —

## Example Scenarios

| ID | Scenario | Input | What to look for in the output | Golden Example |
|---|---|---|---|---|
| E1 | A normal week (real) | `inputs/E1-normal-week.md` — an export of twelve open deals | Every deal over $10,000, with its stage and close date | — |
| E2 | A deal with no close date (proposed, hard) | `inputs/E2-missing-close-date.md` — an export where one large deal has no close date | The deal is listed and flagged, with no invented date | — |

## Rules & Constraints

| ID | Kind | Rule |
|---|---|---|
| R1 | Never | It never invents a figure or a date. |
| R2 | Fallback | When it can't confidently handle a case, it does its best and flags it. |

## Human Gates

Runs: with you

| ID | Where | Checkpoint |
|---|---|---|
| G1 | Step 3 | When the summary is ready, it stops until you have reviewed it. · (you) |

## Security, Privacy & Safety

No sensitivity constraints — personal data only, read-only, human-triggered.

Governing regime: None

### Writes
None
