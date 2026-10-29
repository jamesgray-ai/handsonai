---
plan_revision: 1
last_close_after_round: 0
live_checks: {}
skills_on: yes
write_block: "off"
schedule: none
fingerprints:
  weekly-pipeline-summary: sha256:5f1c0a9e
  last-quarter-summary.md: sha256:9b2d47c3
  test-run.sh: sha256:c03e8f11
bare_run:
  weekly-pipeline-summary: done
run_folders: []
change_requests: []
---

# Weekly Pipeline Summary — Build Record

## What was built
- A skill, weekly-pipeline-summary, that reads your open deals in HubSpot and writes the Friday summary for you to review. It lives in `.claude/skills/weekly-pipeline-summary/` in this workspace. Start it with "write my weekly pipeline summary"; say "practice run" to try it with nothing saved or changed.
- Nothing is waiting.
- The kept copy: none yet.
- An older version: none that you know of.

## What it can access
**HubSpot (your sales account).** It reads open deals: name, amount, stage and close date. It can change nothing: every write tool is left off on purpose. It never changes a deal. It stops for your review before you share the summary.

## Parts
| Task | Build Output | Context ID | Artifact | Path or location | Status | Saved | Built rev | Last built after round | Check | Ruling |
|---|---|---|---|---|---|---|---|---|---|---|
| — | The workflow's place | — | this workspace | `.` | Created | yes | — | — | project auto memory kept; Test told | — |
| T1 | — | — | HubSpot connection | Claude Code connector (HubSpot) | Created | yes | 1 | 0 | read-back: 12 open deals | — |
| T2 | New skill: S1 | C1 | weekly-pipeline-summary skill | `.claude/skills/weekly-pipeline-summary/SKILL.md` | Created | yes | 1 | 0 | E1: AC1, AC2, AC3 met | — |
| T2 | — | C1 | Last quarter's summary (runtime copy) | `.claude/skills/weekly-pipeline-summary/references/last-quarter-summary.md` | Created | yes | 1 | 0 | read back | — |
| KW | — | — | flag, re-check and time-saved lines | `.claude/skills/weekly-pipeline-summary/SKILL.md` | Created | yes | 1 | 0 | each line found in the built text | — |

## Also
- Practice-run instruction: the skill's first line under the cue "practice run" saves nothing outside `practice/[input]-[run]/`.
- Bare run: the plain model missed the owner on each next step; the skill's instructions cover only that.
- Put back the kept copy: no kept copy yet.
