# Weekly Status Report — Workflow Requirements

## Goal
Every Friday morning, produce a one-page leadership status report from the team's
HubSpot project tracker — progress, blockers, and next week's focus — ready for
Maya's review by 10am. Consumed by the leadership team; posted after Maya approves.

## Value & Measurement

| Field | Value |
|---|---|
| Business Objective | Keep leadership informed with less PM overhead |
| Desired Outcome | Maya gets her Friday mornings back, and leadership still has the week's picture before the 11am sync |
| Measure | Minutes Maya spends producing the report, door to door |
| Baseline | Unknown — must measure before go-live |
| Target | Under 25 min, including her review |
| Readable When | After four runs — one month. The same four runs establish the baseline that is missing today |

## Metadata

| Field | Value |
|---|---|
| Workflow Name | Weekly Status Report |
| Description | Drafts the Friday leadership status report from the team's project tracker — progress, blockers, and next week's focus — ready for Maya's review by 10am |
| Trigger | Manual — Maya starts it Friday mornings |
| Owner | Maya R. (Program Manager) |
| Lens | Individual |
| Definition Type | Step-Driven |

---

## Steps Overview

1. Pull updates — collect this week's task changes and comments from the HubSpot tracker
2. Draft report — synthesize progress, blockers, and next-week focus into the report format
3. Review — Maya reviews the draft and edits or approves
4. Save & log — save the approved report and log the run

## Step Details

### Step 1 — Pull Updates
- **Goal:** Collect every task updated in the last 7 days, including status, owner, and comments.
- **Inputs:** HubSpot project tracker (C1); current date.
- **Outputs:** Structured list of updated tasks with status, owner, and notable comments.
- **External Action:** None (read-only).
- **Rules & Edge Cases:**
  - Include tasks whose status changed OR that gained comments this week.
  - A task marked "Blocked" is always included, even with no change this week.
  - If the tracker returns nothing (holiday week), proceed — the report says so plainly rather than inventing activity.
- **Context Needed:** C1

### Step 2 — Draft Report
- **Goal:** Produce the one-page report in the standard format, in Maya's voice.
- **Inputs:** Step 1 output; report template and past reports (C2); tone guide (C3).
- **Outputs:** Complete draft — Wins / In Progress / Blockers / Next Week — under 400 words.
- **External Action:** None (read-only).
- **Rules & Edge Cases:**
  - Every blocker must name an owner and the unblocking action.
  - No task IDs or HubSpot jargon in the report — plain language for leadership.
  - If a blocker has no clear owner, flag it as "owner needed" rather than guessing.
  - If a task's status is ambiguous in the tracker, stop and ask Maya (G2) rather than guessing.
  - Light weeks: say "quiet week" honestly; never pad.
- **Context Needed:** C2, C3

### Step 3 — Review
- **Goal:** Maya confirms accuracy and tone before anything is shared.
- **Inputs:** The draft from Step 2.
- **Outputs:** Approved (possibly edited) report.
- **External Action:** None (read-only).
- **Rules & Edge Cases:**
  - Nothing is posted or shared without Maya's explicit approval.
- **Context Needed:** —

### Step 4 — Save & Log
- **Goal:** Save the approved report and record the run.
- **Inputs:** Approved report.
- **Outputs:** Report saved as `status-report-YYYY-MM-DD.md`; one row appended to the run log.
- **External Action:** Writes two files in Maya's own project folder (the report and the run-log row); no external system.
- **Rules & Edge Cases:**
  - Never overwrite a previous week's report.
- **Context Needed:** —

## Sequence

- **Sequential steps:** 1 → 2 → 3 → 4
- **Parallel steps:** None
- **Critical path:** All four steps

---

## Context Inventory

| ID | Artifact | Used By | Status | Sensitivity | Provenance | AI Accessible | Location / Source | Key Contents |
|---|---|---|---|---|---|---|---|---|
| C1 | HubSpot project tracker | 1 | Exists | Internal | Authored | Yes | HubSpot list "Q2 Delivery Tracker" | Tasks, statuses, owners, comments |
| C2 | Report template + 3 past reports | 2 | Exists | Internal | Authored | Yes | Project folder `context/past-reports/` | Format, section order, length; E1's golden example |
| C3 | Tone guide | 2 | Needs Creation | Internal | Authored | No | Create as `context/tone-guide.md` — does not exist yet | Maya's voice: direct, no hedging, lead with what changed |

## Acceptance Criteria

1. **AC1 (must)** — Every status the report states matches the tracker; nothing is invented
2. **AC2** — The report uses the four sections from C2 in order: Wins, In Progress, Blockers, Next Week
3. **AC3** — Maya could send the report without rewording it

Reference example: C2

## Example Scenarios

| ID | Scenario | Input | What to look for in the output | Golden Example |
|---|---|---|---|---|
| E1 | Typical week (real) | `outputs/weekly-status-report/inputs/E1-typical-week.md` — the week of 2026-06-01: 9 updated tasks, 1 blocker | All sections populated; blockers named with owners; tests R1, G1 | C2 (report of 2026-05-22) |
| E2 | Blocked-heavy week (proposed) | `outputs/weekly-status-report/inputs/E2-blocked-heavy-week.md` — 4+ blockers incl. one with no owner | Every blocker names an owner and a next action, or is flagged "owner needed"; sections stay in template order; tests R1 and the Step 2 ownerless-blocker edge case | — |
| E3 | Quiet week (proposed) | `outputs/weekly-status-report/inputs/E3-quiet-week.md` — 2 updates, no blockers | Short honest report; no padding or invented activity; tests R2 (nothing invented when there is little to report) | — |

## Rules & Constraints

| ID | Type | Rule |
|---|---|---|
| R1 | Must do | State every blocker with an owner and the next action |
| R2 | Must never do | Invent a status the tracker doesn't support, or hedge ("appears to be", "may have") |
| R3 | Scope | The current quarter's tracker only; no cross-quarter trend commentary |
| R4 | Tone / format / length | C3's voice; C2's template; under 400 words |
| R5 | Fallback | When a task's status is ambiguous, stop and ask Maya rather than guessing (also recorded as G2) |

## Human Gates

| ID | Where | What requires human input |
|---|---|---|
| G1 | Step 3 | Maya reviews and approves the draft before it is saved or shared |
| G2 | Step 2 | Maya resolves any task whose status the tracker leaves ambiguous |

## Security, Privacy & Safety

No sensitivity constraints — internal project data only, read-only against the tracker, human-triggered.

## Optimization Notes
Original process had separate "summarize updates" and "format report" steps —
collapsed into Step 2 (one pass for AI). Considered adding a "post to leadership
channel" step; declined for v1 — Maya prefers to post manually until trust is
established (revisit in Improve).
