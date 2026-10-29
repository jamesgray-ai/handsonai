# Weekly Status Report — a finished framework run

> **Internal test fixture, not published.** The registry and folder tests use this folder (`scripts/test-compose-registry.sh`, `scripts/test-worked-example-folder.sh`); nothing on the playbook site links it or ships it. It will be replaced by James's real end-to-end run.

This folder is what a program manager named Maya ends up with after taking one small workflow through the five steps of the AI Workflow Framework (Analyze, Deconstruct, Design, Build and Test) in the Claude desktop app, until it's live. Every file is hand-written in the formats the five skills write.

`Documents/` holds Maya's two folders, kept apart as the framework keeps them on Claude desktop:

- **`Documents/ai-workspace/`** is her working folder, the one she selected in every framework chat. It holds `registry/` (the AI Registry bundle every step reads and writes), `REGISTRY.md` (the view the registry tools generate from it) and `framework/`, the framework folder: `framework/ai-opportunity-report.md` (Analyze's report) and `framework/weekly-status-report/`, the workflow's record: `requirements.md`, `design-plan.md`, `build-record.md` and `test-results.md`, with `inputs/` (the practice inputs), `context/` (the steps' copies of the files the workflow reads), `package/` (the kept copy of the skill Build made) and `history/` (round 1 of Test, kept when round 2 opened).
- **`Documents/status-reports/`** is the workflow's folder, where it runs, outside the working folder: the two files it reads each week (the last report before it went live, and Maya's tone guide) and the five reports it has saved since it went live on 2026-06-08. It holds no framework file, and it keeps no run log: on Claude desktop, the workflow carries a flag line in each run's summary instead.

## Open it

- **The Claude desktop app:** select `Documents/ai-workspace` in a new chat for any framework step. For the workflow itself, install the skill (below) and open a chat in `Documents/status-reports`. Never select both folders in the same chat.
- **Claude on the web, ChatGPT or Copilot Cowork:** put `ai-workspace/` in your Google Drive or OneDrive, connected with writes on, and say where it is when a step asks. The registry and the workflow's record read the same there.
- **Claude Code or Codex:** your workspace is the working folder, holding `registry/` and `framework/` in the same layout; open a session in `Documents/ai-workspace`.

Install the Hands-on AI plugin first if you have not — https://handsonai.info/ai-workflow-framework/skills/ has the steps for every platform.

You do not need HubSpot. The skill works from a pasted tracker export, and the five files in `Documents/ai-workspace/framework/weekly-status-report/inputs/` are exactly what to paste (each file's first two lines are for the framework; paste from the line that starts `# Tracker export`).

## Three things to try

1. **Watch the skills find where it is.** In a new chat with `Documents/ai-workspace` selected, say: *continue my workflow. My files are in ai-workspace.* The skill finds one workflow, Weekly Status Report, sees that it's live, and tells you how to change it or re-check it.
2. **Regenerate the dashboard.** In the same kind of chat, say: *run the indexing-registry skill*. The registry check reports no errors and one warning: Weekly Status Report's re-check date, 2026-09-08, has passed. `REGISTRY.md` doesn't change; it's already current, and shows the workflow as Live. Then say *generate my dashboard* and open `registry-dashboard.html`.
3. **Re-check it yourself.** Install the skill (below), then in a new chat with `Documents/ai-workspace` selected, say: *test the workflow I built. My files are in ai-workspace.* Test opens round 3, a re-check of the live workflow: it moves round 2's results into `history/`, hands you the practice inputs to run in a chat opened in `Documents/status-reports`, and compares the results with round 2.

## Try a practice run

In a chat opened in `Documents/status-reports`, say *practice run* and paste `Documents/ai-workspace/framework/weekly-status-report/inputs/E2-blocked-heavy-week.md` from its `# Tracker export` line. Expect the first line "Practice run: nothing will be sent or changed.", a report with its four sections in order (Wins, In Progress, Blockers, Next Week), the ownerless blocker marked "owner needed", and a stop for your review. Nothing is saved: a practice run shows the report in its closing block instead.

## Install the skill

`Documents/ai-workspace/framework/weekly-status-report/package/skills/weekly-status-report/` is the kept copy of the skill Build saved into Maya's Claude skills. To install it the way she did, zip that folder and add it in Claude under Customize, then Skills — see the skills setup page above. It uses only the portable `name` and `description` fields, so it loads on any platform that takes Agent Skills.
