---
revision: 1
track: full
revisions: []
---

# Monthly Board Update — Workflow Requirements

## Goal
For each month's close, a two-page board update for the CEO, ready to edit by the fifth working day.

## Value & Measurement

| Field | Value |
|---|---|
| Business Objective | Keep the board informed with less executive time |
| Desired Outcome | The CEO starts from a complete draft instead of a blank page |
| Measure | Hours the CEO spends on the update |
| Baseline | 6 hours a month · Estimated |
| Target | 2 hours a month |

## Metadata

| Field | Value |
|---|---|
| Workflow Name | Monthly Board Update |
| Description | Drafts the monthly board update from the finance pack and the team updates, for the CEO to edit and send. |
| Trigger | Finance shares the month-end pack |
| Owner | Chief of staff |
| Lens | Organizational |
| Stakeholders | The CEO; the board; finance; department heads |

## Path

Method preference: some of each

- Step 1 — Pull the headline numbers · produces a table of the five headline numbers · uses C1 · fixed (your judgment)
- The AI plans this part
- Step 3 — Edit and send · produces the sent board update · fixed (your judgment) · (CEO)

### Step 1 — Pull the headline numbers
**Rule:** Revenue, gross margin, cash, burn and headcount, each against last month and plan.
**Expertise:** The narrative always goes in the same order: the numbers, then each department's update, then risks; each department's update is summarised from its own note before the risks are drawn from all of them.

## Inputs

- I1 · the month-end finance pack · from finance, by email · Status: available
- I2 · each department head's monthly note · from the shared team folder · Status: available

## Context Inventory

| ID | Artifact | Used By | Status | Sensitivity | Provenance | AI Accessible | Location / Source | Key Contents |
|---|---|---|---|---|---|---|---|---|
| C1 | Board update template | Step 1, the AI's part after Step 1 | Exists | Internal | Authored | Yes | `context/C1-board-template.md` | The sections and their order |
| C2 | Last month's board update | the AI's part after Step 1 | Exists | Confidential | Authored | Yes | `context/C2-last-month-update.md` | Tone and length to match |

## Acceptance Criteria

Each line is one thing a single run's output either does or doesn't do. Every practice run is checked against every line; one miss on a must-have sends it back.

1. **AC1 (must)** — Every headline number matches the finance pack.
2. **AC2 (must)** — Every department with a note has a summary of it.
3. **AC3** — The update fits on two pages.

Reference example: C2

## Example Scenarios

| ID | Scenario | Input | What to look for in the output | Golden Example |
|---|---|---|---|---|
| E1 | September close (real) | `inputs/E1-september-close.md` — the September pack and four notes | All five numbers right, four summaries | C2 |
| E2 | A missing note (proposed, hard) | `inputs/E2-missing-note.md` — the pack with one department's note missing | The gap flagged, not invented | — |

## Rules & Constraints

| ID | Kind | Rule |
|---|---|---|
| R1 | Never | It never invents a number or a department's news. |
| R2 | When | When the update is ready, you edit and send it yourself. · (CEO) |
| R3 | Fallback | When it can't confidently handle a case, it does its best and flags it. |

## Human Gates

Runs: with you

| ID | Where | Checkpoint |
|---|---|---|
| G1 | Step 3 | When the draft is ready, it stops until the CEO has edited it. · (CEO) |

## Security, Privacy & Safety

*Scope: handles data you'd be uncomfortable seeing outside the company*

### Boundaries
| ID | Constraint | Source |
|---|---|---|
| P1 | The draft and the finance pack stay in the leadership drive. | Self |

### Access
| ID | Constraint | Source |
|---|---|---|
| P2 | Only the CEO and the chief of staff see the draft. | Self |

Governing regime: None

### Writes
None
