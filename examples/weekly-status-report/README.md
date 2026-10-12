# Weekly Status Report — a finished framework run

This folder is the complete project a program manager named Maya ends up with after taking one small workflow through all seven steps of the AI Workflow Framework in the Claude desktop app. It is the folder described, file by file, at https://handsonai.info/ai-workflow-framework/examples/worked-example/ — read that page alongside this folder.

What is here: `registry/` (the AI Registry bundle every framework step reads and writes), `REGISTRY.md` (the dashboard the registry tools generate from it), `context/` (the tone guide and three past reports the workflow draws on), `framework/` (the record Steps 1–7 produced: the opportunity report, requirements and scenario inputs, the design spec, the two staged skills, three rounds of test results, the run log, and the improvement plan), and `outputs/` (the workflow's own output: the five saved status reports).

## Open it

- **The Claude desktop app:** open this folder as the working folder — any folder works; a project is optional.
- **Claude on the web:** upload the files to a project.
- **Claude Code or Codex:** open a terminal in this folder and start the tool here.
- **Gemini or Microsoft 365 Copilot:** upload the folder where your tool reads project files.

Install the Hands-on AI plugin first if you have not — https://handsonai.info/ai-workflow-framework/skills/ has the steps for every platform.

You do not need HubSpot. The orchestrator skill accepts a pasted update list in place of the live pull, and the three files in `framework/weekly-status-report/inputs/` are exactly what to paste.

## Three things to try

1. **Watch the skills orient.** Say: *continue my workflow*. The skill lists the two Workflow nodes in `registry/workflows/`, orients on Weekly Status Report once you pick it (the other is a backlog stub), sees every step's artifact through the improvement plan, tells you the workflow is in production and its 2026-08-14 review is due, and offers to run Improve.
2. **Regenerate the dashboard.** Say: *run the indexing-registry skill*. Lint reports no errors and one warning (the review is due). `REGISTRY.md` does not change — it is already current. Then say: *generate my dashboard* and open `registry-dashboard.html`. The Skills inventory lists the two staged skills under `framework/weekly-status-report/skills/` — the tools count every `skills/` folder, whether or not the skill is installed in your platform.
3. **Rewind one step and run it yourself.** Delete `framework/weekly-status-report/improvement-plan.md`. In `registry/workflows/weekly-status-report.md`, take out the `Improvement plan` line under `# Artifacts`, delete the Note line between `<!-- GENERATED:insights -->` and `<!-- /GENERATED -->`, and change `stale_after: 2026-08-14` to `stale_after: 2026-07-10`. Delete `registry/notes/status-report-scope-grows-a-section-at-a-time.md` and its line in `registry/notes/index.md`. (The node's `generated:` stamp still says Improve wrote it; Improve will restamp it.) Then say: *Run the improve skill on weekly status report*. Compare the plan it writes with the one you deleted. (`framework/weekly-status-report/test-results.md` already reads `readiness: not-ready` — the first Improve run set it that way for Build's fix mode; Improve compares against the Ready round, `test-results-2026-06-08.md`, so this is expected.)

## Run a test scenario

Say: *run the weekly status report skill as a test run* and paste the contents of `framework/weekly-status-report/inputs/E2-blocked-heavy-week.md`. Expect a draft with four blockers, one flagged "owner needed", the four sections in template order, and a pause for your review — and no new row in `runs.md`, because test runs save under `test-runs/`.

The skills in `framework/weekly-status-report/skills/` are staged source. To install them the way Build would, zip each skill folder (`weekly-status-report/` and `status-report-drafting/`) and add it under your platform's skills setting — see the skills setup page above. On Microsoft 365 Copilot, delete the `disable-model-invocation: true` line from the orchestrator's frontmatter first; Copilot rejects skills with non-standard fields.
