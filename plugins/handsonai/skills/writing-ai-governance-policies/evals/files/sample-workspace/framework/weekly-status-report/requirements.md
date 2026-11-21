---
revision: 1
track: full
revisions: []
---

# Weekly Status Report — Workflow Requirements

## Goal
For each Friday, a one-page Markdown status report to the leadership team, ready for Maya to review and share by 10am.

## Value & Measurement

| Field | Value |
|---|---|
| Business Objective | Keep leadership informed with less program-management overhead |
| Desired Outcome | Maya gets her Friday mornings back, and leadership still has the week's picture before the 11am sync |
| Measure | Minutes Maya spends producing the report, from opening the tracker to sharing the report |
| Baseline | — · Unknown |
| Target | — |

## Metadata

| Field | Value |
|---|---|
| Workflow Name | Weekly Status Report |
| Description | Drafts the Friday leadership status report from the team's project tracker (progress, blockers and next week's focus), ready for Maya's review by 10am. |
| Trigger | Maya starts it on Friday mornings |
| Starts | you |
| Owner | Maya R. (Program Manager) |
| Lens | Individual |

## Path

Method preference: AI works it out each time
Path: none — the AI plans each run from the goal

## Inputs

- I1 · this week's task updates: each task whose status changed or that gained a comment in the last seven days · from C1, through the HubSpot connection · Status: available

## Context Inventory
*The sources it uses, what we call its context.*

| ID | Artifact | Used By | Status | Sensitivity | Provenance | AI Accessible | Location / Source | Key Contents |
|---|---|---|---|---|---|---|---|---|
| C1 | HubSpot project tracker | All | Exists | Internal | Authored | Yes | HubSpot list "Q2 Delivery Tracker" | Tasks, statuses, owners and comments |
| C2 | Last status report | All | Exists | Internal | Authored | Yes | `context/C2-report-2026-05-22.md` | The report of 2026-05-22: the four sections, their order and their length, which every report follows |
| C3 | Tone guide | All | Needs Creation | Internal | Authored | No | Create as `context/C3-tone-guide.md` | Maya's voice: direct, no hedging, leading with what changed |

## Acceptance Criteria

Each line is one thing a single run's output either does or doesn't do. Every practice run is checked against every line; one miss on a must-have sends it back.

1. **AC1 (must)** — Every status the report states matches the tracker.
2. **AC2** — The report uses the four sections from C2, in this order: Wins, In Progress, Blockers, Next Week.
3. **AC3 (must)** — Every blocker names its owner and the next action, or is marked "owner needed".
4. **AC4** — The report is under 400 words, in plain language with no task IDs or tracker terms.

Reference example: C2

## Example Scenarios
*The practice runs: each input it's tested on, and what should happen.*

| ID | Scenario | Input | What to look for in the output | Golden Example |
|---|---|---|---|---|
| E1 | Typical week (real) | `inputs/E1-typical-week.md` — the tracker export for the week of 2026-06-01: nine updated tasks, one blocker | Every section filled, and the one blocker with its owner and next action; no status the tracker doesn't support | C2 |
| E2 | Blocked-heavy week (proposed, hard) | `inputs/E2-blocked-heavy-week.md` — four blockers, one of them with no owner | Each blocker with its owner and next action, and the ownerless one marked "owner needed"; no owner guessed for it | — |
| E3 | Quiet week (proposed) | `inputs/E3-quiet-week.md` — two updates and no blockers | A short report that says it was a quiet week; nothing padded or invented | — |

## Rules & Constraints
*Its rules: what it always does, never does, and does when something happens.*

| ID | Kind | Rule |
|---|---|---|
| R1 | Never | It never states a status the tracker doesn't support, and never hedges with words like "appears to" or "may have". |
| R2 | Always | It always includes every task marked Blocked, even when the task didn't change this week. |
| R3 | When | When the tracker shows little or nothing new, it says it was a quiet week and never pads the report. |
| R4 | Always | It always writes in the voice of the tone guide: direct, and leading with what changed. |
| R5 | Never | It never comments on trends across quarters; it reports on the current quarter's tracker only. |
| R6 | When | When the report is approved, you share it with leadership yourself. · (you) |
| R7 | Fallback | When it can't tell a task's status from the tracker, it stops and asks you which it is. |

## Human Gates
*The checkpoints: where a person checks or approves the work.*

Runs: with you

| ID | Where | Checkpoint |
|---|---|---|
| G1 | When a task's status is unclear in the tracker | When a task's status is unclear in the tracker, it stops until you say which it is. · (you) |
| G2 | After the draft is ready | When the draft is ready, it stops until you approve or edit it. · (you) |

## Security, Privacy & Safety

No sensitivity constraints — personal data only, read-only, human-triggered.

Governing regime: None

### Writes
None
