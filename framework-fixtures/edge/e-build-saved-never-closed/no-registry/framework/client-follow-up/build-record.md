---
live_checks:
  gmail-draft: "done: a draft addressed to you in Gmail Drafts"
skills_on: yes
write_block: "off"
schedule: none
fingerprints:
  client-follow-up: sha256:5f1c0a9e
  follow-up-style.md: sha256:9b2d47c3
  test-run.sh: sha256:c03e8f11
bare_run:
  client-follow-up: done
run_folders: []
change_requests: []
---

# Client Follow-Up — Build Record

## What was built
- A skill, client-follow-up, that reads your call notes and drafts the follow-up email in Gmail Drafts for you to review and send. It lives in `.claude/skills/client-follow-up/` in this workspace. Start it with "draft my client follow-up"; say "practice run" to try it with nothing saved or changed.
- Nothing is waiting.
- The kept copy: none yet.
- An older version: none that you know of.

## What it can access
**Gmail (your work account).** It reads nothing in your mailbox. It can change one thing: it creates drafts in Gmail Drafts, which you can delete. Sending is left off on purpose. It never sends an email, whoever asks. It stops for your approval before you send each draft.

## Parts
| Task | Build Output | Context ID | Artifact | Path or location | Status | Saved | Built rev | Last built after round | Check | Ruling |
|---|---|---|---|---|---|---|---|---|---|---|
| — | The workflow's place | — | this workspace | `.` | Created | yes | — | — | project auto memory kept; Test told | — |
| T1 | — | — | Gmail connection | Claude Code connector (Gmail) | Created | yes | 1 | 0 | read-back: the Gmail connection answers and create-draft is available | — |
| T2 | New skill: S1 | C1 | client-follow-up skill | `.claude/skills/client-follow-up/SKILL.md` | Created | yes | 1 | 0 | E1: AC1, AC2, AC3 met | — |
| T2 | — | C1 | Follow-up style guide (runtime copy) | `.claude/skills/client-follow-up/references/follow-up-style.md` | Created | yes | 1 | 0 | read back | — |
| KW | — | — | flag, re-check and time-saved lines | `.claude/skills/client-follow-up/SKILL.md` | Created | yes | 1 | 0 | each line found in the built text | — |

## Also
- Practice-run instruction: the skill's first line under the cue "practice run" saves nothing outside `practice/[input]-[run]/`.
- Quick real check: a draft addressed to you in Gmail Drafts; you deleted it (undone).
- Bare run: the plain model missed the owner on each next step; the skill's instructions cover only that.
- Put back the kept copy: no kept copy yet.
