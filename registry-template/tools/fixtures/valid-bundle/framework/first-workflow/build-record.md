---
plan_revision: 1
last_close_after_round: 1
live_checks: {}
skills_on: yes
write_block: "off"
schedule: none
fingerprints:
  .claude/skills/some-skill/SKILL.md: sha256:0d6f1c2a
  framework/.bin/test-run.sh: sha256:7a41e0b9
bare_run:
  some-skill: done
run_folders: []
change_requests: []
---

# First Workflow — Build Record

## What was built
Live since 2026-07-01.
How to switch it off: delete `.claude/skills/some-skill/` from this workspace; it has no schedule.

- A skill, some-skill, that drafts the kickoff email from a signed contract's summary for you to review and send. It lives in `.claude/skills/some-skill/`. Say "practice run" to try it with nothing saved or changed.
- Nothing is waiting.
- The kept copy: the installed folder, under Git.
- An older version: none that you know of.

## What it can access
**No connections.** It reads only what you paste and its style guide, and changes nothing.

## Parts
| Task | Build Output | Context ID | Artifact | Path or location | Status | Saved | Built rev | Last built after round | Check | Ruling |
|---|---|---|---|---|---|---|---|---|---|---|
| — | The workflow's place | — | this workspace | `.` | Created | yes | — | — | project auto memory kept; Test told | — |
| T1 | New skill: S1 | C1 | some-skill | `.claude/skills/some-skill/SKILL.md` | Created | yes | 1 | 1 | E1, E2: AC1, AC2, R1 met | — |
| KW | — | — | flag and re-check lines | `.claude/skills/some-skill/SKILL.md` | Created | yes | 1 | 0 | each line found in the built text | — |

## Also
- Practice-run instruction: under the cue "practice run", it saves only in `practice/[input]-[run]/`.
