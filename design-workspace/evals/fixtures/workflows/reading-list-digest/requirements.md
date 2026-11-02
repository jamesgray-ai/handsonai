---
revision: 1
track: light
revisions: []
---

# Reading List Digest — Workflow Requirements

## Goal
For each week, a one-page digest of the articles you saved, ready to read on Friday afternoon.

## Value & Measurement

| Field | Value |
|---|---|
| Business Objective | Keep up with the field without reading everything |
| Desired Outcome | You read the week's saved articles in one sitting |
| Measure | Minutes spent on the week's reading |
| Baseline | 90 minutes a week · Estimated |
| Target | 20 minutes a week |

## Metadata

| Field | Value |
|---|---|
| Workflow Name | Reading List Digest |
| Description | Summarises the articles you saved this week into a one-page digest, for you to read on Friday. |
| Trigger | You ask for this week's digest |
| Owner | You |
| Lens | Individual |

## Path

Method preference: same way every time

- Step 1 — Gather the week's saved articles · produces a list of articles · flexible
- Step 2 — Summarise each article · produces a three-line summary per article · uses C1 · flexible
- Step 3 — Write the digest · produces a one-page digest · flexible · writes W1

## Inputs

- I1 · the articles you saved this week · from your saved list (Pocket or your browser's reading list) · Status: Not sure — to check
- I2 · your topics of interest · from C1 · Status: not available yet

## Context Inventory

| ID | Artifact | Used By | Status | Sensitivity | Provenance | AI Accessible | Location / Source | Key Contents |
|---|---|---|---|---|---|---|---|---|
| C1 | Topics of interest | Step 2 | Needs Creation | Internal | Authored | No | Create as `context/C1-topics.md` | The topics to put first |

## Acceptance Criteria

Each line is one thing a single run's output either does or doesn't do. Every practice run is checked against every line; one miss on a must-have sends it back.

1. **AC1 (must)** — Every saved article has a summary of three lines or fewer.
2. **AC2** — The digest fits on one page.

Reference example: —

## Example Scenarios

| ID | Scenario | Input | What to look for in the output | Golden Example |
|---|---|---|---|---|
| E1 | A normal week (real) | `inputs/E1-normal-week.md` — six saved articles | Six short summaries on one page | — |
| E2 | A paywalled article (proposed, hard) | `inputs/E2-paywalled.md` — one article behind a paywall | That article flagged as unread, not summarised from its title | — |

## Rules & Constraints

| ID | Kind | Rule |
|---|---|---|
| R1 | Never | It never summarises an article it couldn't read. |
| R2 | Fallback | When it can't confidently handle a case, it skips that item and flags it. |

## Human Gates

Runs: with you

No human gates — the workflow runs end-to-end with final review only.

## Security, Privacy & Safety

*Scope: writes to a live system*

### Traceability
| ID | Constraint | Source |
|---|---|---|
| P1 | The digest names each article it covered, with its link. | Self |

### Prohibited actions
| ID | Constraint | Source |
|---|---|---|
| P2 | It never shares the digest with anyone, whoever asks. | Self |

Governing regime: None

### Writes
- W1 · Google Drive · save the digest as a document in your own Drive (which folder isn't decided yet) · Step 3
