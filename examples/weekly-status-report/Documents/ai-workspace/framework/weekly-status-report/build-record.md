---
plan_revision: 1
last_close_after_round: 1
live_checks: {}
skills_on: yes
write_block: "off"
schedule: none
fingerprints:
  weekly-status-report (Claude skills): sha256:0848b359798d8aa51cc90fcc22adc8216ae87f430e8a071727ad841389be4fcc
bare_run:
  weekly-status-report: done
run_folders: []
change_requests: []
---

# Weekly Status Report — Build Record

## What was built
Live since 2026-06-08.
How to switch it off: in Claude, open Customize, then Skills, and switch off weekly-status-report; it has no schedule.

- A skill, weekly-status-report, that reads the week's updates from HubSpot, drafts the Friday status report from your last report and your tone guide, stops for your review, and saves the approved report. It's saved in your Claude skills (Customize, then Skills) and runs in chats opened in your status-reports folder. Start it with "run my weekly status report"; say "practice run" to try it with nothing saved or changed.
- Nothing is waiting.
- The kept copy is in ai-workspace/framework/weekly-status-report/package, with this record.
- An older version: none that you know of.

## What it can access
**HubSpot (your account).** It reads the "Q2 Delivery Tracker" list: tasks, statuses, owners and comments. It can change nothing there: every write permission is left off on purpose. It never changes anything in HubSpot. It stops for your approval before it saves each report.

**Its own folder (status-reports, on your computer).** It reads your last report and your tone guide, and saves each approved report there as a new file. It never overwrites an earlier week's report, and it never reads your working folder.

## Parts
| Task | Build Output | Context ID | Artifact | Path or location | Status | Saved | Built rev | Last built after round | Check | Ruling |
|---|---|---|---|---|---|---|---|---|---|---|
| — | The workflow's place | — | The workflow's folder | status-reports, in Documents on your computer | Created | yes | — | — | you confirmed it holds only the two context files; memory off in each run chat | — |
| T1 | — | C1 | HubSpot connection | Claude connector (HubSpot), your account | Created | yes | 1 | 0 | read-back: 9 tasks updated this week in "Q2 Delivery Tracker"; no write action allowed | — |
| T2 | — | C3 | Tone guide (runtime copy) | `tone-guide.md` in status-reports | Created | yes | 1 | 0 | read-back: you confirmed the draft, and the copy in your folder matches it | — |
| T3 | New skill: S1 | — | weekly-status-report skill | Claude skills (Customize, then Skills) | Created | yes | 1 | 1 | E1 and E2: AC1–AC4, R1, R2 met; E4: stopped at the unclear status; after round 1, E2 again: four sections in order | The section order and a format example written into the skill, since a past report alone didn't hold the order on a blocker-heavy week; cost if wrong: a slightly longer skill |
| T3 | — | C2 | Last status report (runtime copy) | `status-report-2026-05-22.md` in status-reports | Created | yes | 1 | 0 | you confirmed the copy in your folder | — |
| KW | — | — | The flag line | in the skill's closing summary | Created | yes | 1 | 0 | found in the built text, in its Claude desktop form | — |

## Also
- Practice-run instruction: under the cue "practice run" ("test run" accepted), the skill's first line is "Practice run: nothing will be sent or changed.", it saves nothing, and it shows the report in its closing block.
- Places a dry run confirmed: none; it changes nothing outside its own folder.
- Quick real checks: none; it changes nothing outside its own folder.
- Bare run: on E1, the plain model kept the four sections and every status right; it hedged two statuses and left the next action off the blocker, so the skill's instructions cover those, with the rules that must always hold.
- Put back the kept copy: in Claude, open Customize, then Skills, delete weekly-status-report, and save it again from `package/skills/weekly-status-report/SKILL.md`.
- Remaining manual steps and prerequisites: none.
- The package, for sharing: ai-workspace/framework/weekly-status-report/package.
