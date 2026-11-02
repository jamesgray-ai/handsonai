---
revision: 1
track: light
revisions: []
---

# Prospect Snapshot — Workflow Requirements

## Goal
For each new prospect, a half-page snapshot for you, ready before your first call.

## Value & Measurement

| Field | Value |
|---|---|
| Business Objective | Better first calls with new prospects |
| Desired Outcome | You open every first call knowing what the prospect does and what they announced lately |
| Measure | Minutes of preparation per first call |
| Baseline | 25 minutes · Estimated |
| Target | 5 minutes |

## Metadata

| Field | Value |
|---|---|
| Workflow Name | Prospect Snapshot |
| Description | Turns a prospect's website and recent news into a half-page snapshot, for you to read before your first call. |
| Trigger | You book a first call and paste in the prospect's website and news |
| Owner | You |
| Lens | Individual |

## Path

Method preference: same way every time

- Step 1 — Read what you pasted · produces what the prospect does and its recent news · flexible
- Step 2 — Write the snapshot · produces a half-page snapshot · uses C1 · flexible

## Inputs

- I1 · the prospect's website pages and two or three recent news articles · from the web, copied and pasted into the chat by you · Status: available

## Context Inventory

| ID | Artifact | Used By | Status | Sensitivity | Provenance | AI Accessible | Location / Source | Key Contents |
|---|---|---|---|---|---|---|---|---|
| C1 | Snapshot format | Step 2 | Exists | Internal | Authored | Yes | `context/C1-snapshot-format.md` | The four headings and the length |

## Acceptance Criteria

Each line is one thing a single run's output either does or doesn't do. Every practice run is checked against every line; one miss on a must-have sends it back.

1. **AC1 (must)** — The snapshot states only what the pasted pages say.
2. **AC2** — The snapshot fits in half a page.

Reference example: —

## Example Scenarios

| ID | Scenario | Input | What to look for in the output | Golden Example |
|---|---|---|---|---|
| E1 | A logistics firm (real) | `inputs/E1-logistics-firm.md` — a freight company's about page and two news items | What they do, two news points, half a page | — |
| E2 | A thin website (proposed) | `inputs/E2-thin-website.md` — a one-page site and no news | A short snapshot that says little is public | — |

## Rules & Constraints

| ID | Kind | Rule |
|---|---|---|
| R1 | Never | It never adds a fact that isn't in what you pasted. |
| R2 | Fallback | When it can't confidently handle a case, it does its best and flags it. |

## Human Gates

Runs: with you

No human gates — the workflow runs end-to-end with final review only.

## Security, Privacy & Safety

No sensitivity constraints — personal data only, read-only, human-triggered.

Governing regime: None

### Writes
None
