
# Where a workflow is, and what's next

Every framework skill uses this one rule: at its entry, before its opening, and when the leader says "continue my workflow". Where code can run, the `framework-state` script applies it and returns the state; this file is the rule and its written fallback. It is the same, byte for byte, in all five skills.

## What it reads

- **The workflow's folder,** current files only: `requirements.md`, `deconstruct-in-progress.md`, `design-plan.md`, `build-record.md`, `test-results.md`. To spot an earlier version (last section) it also looks for `design-spec.md`, and checks only whether `run-guide.md` or an old run log is in the folder. Never `history/`, except whether a `history/set-aside-*/` folder exists and, for the live test below, the newest set-aside build record.
- **The Workflow node,** where there's a registry: `status` and `big_change`.
- **With no registry:** `big_change` in the frontmatter of `requirements.md`, and the "Live since" line at the top of `build-record.md`.
- **The framework folder,** for "continue my workflow" only: its workflow folders (and, where there's a registry, their nodes), whether `analyze-in-progress.md` is there, and whether there are backlog candidates (the registry's `backlog` nodes, or, with no registry, `backlog.md`).

## Terms

- **Live:** with a registry, the node's `status` is `in-production`. With no registry, the build record's top section says "Live since YYYY-MM-DD"; or, while a redo is pending or being rebuilt, the newest build record in `history/set-aside-*/` says so.
- **Plan revision:** the highest task `rev` in `design-plan.md`. It is worked out, never stored.
- **The last round:** the round in `test-results.md`; its number is `round`. With no results file, the last round is 0.
- **A Build close after the last round:** the build record's `last_close_after_round` is at or above the last round's number. (A round still in progress when Build closed is set aside before this is read: "A round left behind", below.)
- **An unlogged change request:** an entry under `change_requests` in `build-record.md` or `test-results.md` whose `id` isn't in the plan's `changes:` log. A request whose only task is `SCH` (a schedule-only request) doesn't count. An entry with no `id` can't be read: routing stops and falls back to reading the files by hand.
- **Built and saved:** the record shows the task built, with `Saved: yes`. Two cases count as built: a task Build finished with a known miss (`Built, misses [line]`: after Build's first close, its check failed because a requirement line can't be met, and Test settles the line), and the `SCH` task recorded with `schedule: safety-incomplete`.
- **An earlier version:** see the last section.

## The states

Check these in order. The first that matches is the state.

| # | State | What shows it | Owner |
|---|---|---|---|
| 0 | Not a framework workflow, or retired | The node is `retired`; or the node is `in-production` and the workflow has no folder (running work Analyze recorded) | None: state 0's line, then stop. Two exceptions: "change my workflow" on a retired workflow goes to Design, and Deconstruct by name ("run the deconstruct skill on [workflow]") on running work goes to Deconstruct (both below) |
| 1 | Earlier version | A file in an earlier version's format | The step that writes the earliest such file |
| 2 | Redo pending | `big_change` is set | Deconstruct |
| 3 | Requirements needed | No `requirements.md`, or a `deconstruct-in-progress.md` | Deconstruct; Analyze when the leader has no workflow in mind yet |
| 4 | Plan needed | No `design-plan.md`; or the requirements' `revision` is above the plan's `requirements_revision`, not counting revisions marked `plan_unaffected`; or an unlogged change request | Design |
| 5 | Plan to approve | The plan isn't `approved: true` | Design |
| 6 | Build needed | No `build-record.md`; or a task not built and saved, other than one waiting on an unanswered open item; or a task whose `rev` is above its built `rev` in the record; or the record's `plan_revision` isn't set or isn't the current plan revision, unless a task waits on an unanswered open item; or `direct_edit: undo` in the results with no Build close after that round; or the last round is `not-ready`, has an Issues row at Level `build`, and has no Build close after it | Build (after a Not ready round, in fix mode) |
| 7 | Waiting on an open item | Every task that can be built is built and saved, and at least one waits on an unanswered open item | Design, to answer the item |
| 8 | Test needed | No `test-results.md`; or a round `in-progress`; or a Build close after the last round; or the last round is `not-ready` with nothing in it for Build (no Issues row at Level `build`, no `direct_edit: undo`) | Test |
| 9 | Waiting on access | The last round is `waiting-on-access` | Test (it gives the connection's steps, then checks again) |
| 10 | Ready to go live | The last round is `ready` for the current plan revision, with `go_live: pending` | Test |
| 11 | Live | Live, and nothing above matched | Test, for a re-check |

**A round left behind.** When Test meets a round `in-progress` whose `plan_revision` isn't the current plan revision, or whose number is at or below the build record's `last_close_after_round` (Build closed while it was open), it moves the file to `history/test-results-round-[n].md` with `round_status: abandoned` and opens a fresh round, numbered n+1. So a Build close only ever counts as after a round that had finished.

**A retired workflow brought back.** "Change my workflow" on a retired workflow goes to Design. Design sets the node's `status` to `under-development` and says so in one line. When there's a build record, Design logs one entry in the plan's `changes:` that puts back the built version of every task (source `change my workflow`, `what: put back the built version`), raising each task's `rev` without changing its content, together with any change the leader asked for. The direct-edit check runs first, and a task a kept edit touches is left out of the put-back; a big change or a change of platform sets the files aside instead, with no put-back. That sends the workflow to Build (state 6), which reinstalls the version it built, and then to Test (state 8), which re-checks it before it goes live again. With no build record, Design works out the state from the files and carries on, or gives the owner's start phrase with the location (Deconstruct's when the folder has no requirements yet). Its next go-live sets `status: in-production` again.

**Running work brought in.** "Run the deconstruct skill on [workflow]" on running work Analyze recorded goes to Deconstruct, which takes it as a new workflow: its normal interview, on the light or full track, starting from the leader's account of what the work does today, with where it runs today (by hand, set up somewhere, on a schedule) recorded in the requirements' `Runs today` row. That phrase is the only route in: the running-work message and the bring-in line both give it, and neither offers "change my workflow", which is Design's change phrase, so no line sends the leader from one phrase to the other. A leader who says "change my workflow" about running work anyway is sent once, to Deconstruct's phrase: any other step that receives it says the bring-in line (below), which gives Deconstruct's start phrase naming the workflow in N-F2's new-chat form, and stops; Deconstruct, receiving it, takes it as the same request. The location is the framework folder, since the workflow has no folder yet. Once Deconstruct first saves its progress, the workflow has a folder, so it is no longer state 0, and the states above apply as for any workflow. The node stays `in-production`, so the workflow counts as live throughout: the version that runs today keeps running until Build installs the new one; before every Build run changes it, the leader pauses any schedule and a copy is kept of whatever is installed, as for any change to a live workflow, and Build waits for the leader's word; and Test, at the Ready round that takes the new version live, asks the leader to switch off for good the version that ran before, when it was set up somewhere or ran on a schedule. Running work is state 0 only where there's a registry: with none, Analyze keeps it in its report, and work named at cold entry is a new workflow.

## What each step accepts

- **Analyze:** state 3 when the leader has no workflow in mind yet; its own progress file; and, by name, at any time, to find more workflows.
- **Deconstruct:** states 2 and 3; and state 0's running work, by name (or by "change my workflow", when the leader says that here), which it takes as a new workflow (above). By name, a re-run of the requirements while there is no `build-record.md` (states 4 to 6): the plan is kept, and the raised `revision` sends Design to update it.
- **Design:** states 4, 5 and 7. By name, re-planning while there is no `build-record.md` (it updates the plan in place). "Change my workflow" in any state from 4 on (in state 4 with no plan yet, Design runs its normal flow), and on a retired workflow in state 0, which it brings back (above). A change to the schedule alone, by name, in any state from 4 on.
- **Build:** state 6; after a Not ready round with Issues rows at Level `build`, in fix mode.
- **Test:** states 8 to 11. In state 10, when the workflow is already live (a go-live that was interrupted), Test finishes the remaining go-live steps without asking again. In state 11, "test the workflow I built" opens a re-check round.
- **State 1:** the owner asks N-B44 first when the workflow is live or was built, then starts fresh (last section); any other step says N-T22 with the owner's start phrase, and nothing else.

## When this step isn't the owner

Say in one line where the workflow is and which step is next, with that step's start phrase and the location, then stop. That line is the whole message: nothing before it and nothing after it. Use these lines where they apply:

- **State 0, running work** (the running-work message): "This workflow already runs outside the framework. To bring it in, say 'run the deconstruct skill on [workflow]. My files are in [location].' Deconstruct pins down what it must produce and how it should go; until the new version is built and installed, keep running it as it is." The location is the framework folder. A step other than Deconstruct that receives "change my workflow" on running work says the bring-in line instead, which gives the same phrase in N-F2's new-chat form: "To bring [workflow] into the framework, start Deconstruct in a new chat with: 'run the deconstruct skill on [workflow]. My files are in [location].'"
- **State 0, retired** (the retired line): "This workflow is retired. To bring it back, say 'change my workflow. My files are in [location].'"
- **State 1** (N-T22): "This was made with an earlier version of the framework. Start it again with '[start phrase]. My files are in [location].'"
- **State 7** (the open-item line): "[The waiting tasks, in plain words] wait for [the open item]. To answer it, say 'run the design skill. My files are in [location].'" With one waiting task: "[The waiting task, in plain words] waits for [the open item]. To answer it, say 'run the design skill. My files are in [location].'"
- **State 11, on "continue my workflow", or when Design is started by name** (N-T19): "This workflow is live. To change it, say 'change my workflow. My files are in [location].' To re-check it, say 'test the workflow I built. My files are in [location].'"
- **Any other state:** the step's own not-owner line where its SKILL.md gives one (Test, states 2 to 6: N-T25); otherwise model wording that names the workflow, where it is in plain words, the owner step by name, and its start phrase with the location.

| Step | Start phrase |
|---|---|
| Analyze | "run the analyze skill" |
| Deconstruct | "run the deconstruct skill" ("…on [workflow]" when naming one) |
| Design | "run the design skill", or "change my workflow: [what changed]" |
| Build | "run the build skill" |
| Test | "test the workflow I built" |

Each is followed by "My files are in [location]." On the web, the location is the drive and folder ("Google Drive, in Framework/[workflow-slug]"; on Microsoft 365, "OneDrive, in Framework/[workflow-slug]"); on Claude desktop, the framework folder by its own name ("Framework/[workflow-slug]"); on Claude Code and Codex, the folder in the workspace ("framework/[workflow-slug]"). A start phrase for a workflow built on another platform, to be said there (N-T15), takes that platform's location, in that platform's form above: for a workflow built for ChatGPT, "Google Drive, in Framework/[workflow-slug]", even when this chat reads a local folder. Each step runs in a new chat (a new session on Claude Code and Codex). On Microsoft 365 the line says to open a new Cowork chat, and only names the folder, as on the web; on Claude desktop, with the files in a local folder, it says to add the framework folder to the new chat.

## "Continue my workflow"

Any framework skill may receive it.
1. **Find the workflow.** If the leader named one, that one. Otherwise, if `analyze-in-progress.md` is in the framework folder: Analyze owns it when no workflow that isn't retired has a folder; when some do, ask N-F9 with the unfinished Analyze session listed beside them, whether there is one of them or several. Otherwise, among the workflows that have a folder and aren't retired: the only one in progress, by the states above (any state but 11: not yet live, or live and partway through a change, a fix or a redo); or, when none is in progress and there's only one, that one (state 11 then says N-T19); otherwise ask (N-F9): "Which workflow should we pick up: [Name] ([where it is, in plain words]), [Name] ([where it is])?" With exactly two, and no unfinished Analyze session: "Which workflow should we pick up: [Name] ([where it is, in plain words]) or [Name] ([where it is])?" With an unfinished Analyze session, the question ends "…, or your unfinished Analyze session?", and picking it gives it to Analyze. Backlog candidates with no folder don't count, and neither do retired workflows: with no folder for a workflow that isn't retired, but a backlog, give Deconstruct's start phrase with the location, since its backlog choice does the picking; with neither, say in one line that there's nothing to continue yet, and give Analyze's start phrase. On the web with no location given, look for the framework folder by name; if the files aren't there, ask (N-F3a): "I can't find the files for [workflow] in [where I looked]. Where are they?" On Claude desktop, or on Microsoft 365 when Cowork can't read the drive, a chat that can't read any framework files asks N-F13 instead (below), since it couldn't open a path the leader gave.
2. **Work out the state.**
3. **If this skill owns it, carry on,** with a resume line in place of the opening. Otherwise give the owner's start phrase with the location, to say in a new chat, and stop. In state 11, say N-T19 rather than starting a re-check.

## The order at every entry, before the opening

1. **The wrong place** (every step but Analyze): this chat is inside the workflow's own place (its context files present, no framework files). Say N-F7 and stop: "This chat is inside your workflow's [Project / folder], where it runs, so I'll keep the framework out of it. Open a new chat outside it and say '[start phrase]. My files are in [location].'" Claude desktop: "This chat has your workflow's folder added, where it runs, so I'll keep the framework out of it. Open a new chat with your framework folder added and say '[start phrase]. My files are in [location].'" On Claude Code and Codex, the workflow's place is the workspace it's installed in: when the workflow's skill or agent is installed in this workspace (`.claude/skills/[workflow]/` or `.claude/agents/` on Claude Code, Codex's skills folder) and the workspace has no `framework/` folder, this is the wrong place, not a missing location, so it comes before the location: say N-F7's Claude Code and Codex form, "This session is inside the workspace where your workflow runs, so I'll keep the framework out of it. Start a new session in the workspace that holds your framework folder and say '[start phrase]. My files are in [location].'", and stop. Never ask where the files are.
2. **The location:** take it from the start phrase, or find it (above). The opening confirms it in one line (N-F3). When this chat can't read the files the step needs, ask for them before anything else (N-F13). On Microsoft 365, only when Cowork can't find or read the framework files at the location (an admin may limit its OneDrive access): "I can't see your framework files yet. Attach your Framework folder in OneDrive to this chat, then say 'done'." Nothing is read, saved or asked until the files can be read; if they still can't be once the leader says "done", say so in one line, say that their Microsoft 365 admin can let Cowork read their OneDrive, give this step's start phrase with the location to say once that's done, and stop. On Claude desktop, when no folder is added to this chat: "I can't see your framework files yet. Add your framework folder to this chat, then say 'done'."
3. **The state,** by the table. In state 1, when this step is the owner and the workflow is live or was built (the node is `in-production`, or skills or agents are linked, or the folder has results, a run guide or an old run log), ask first (N-B44): "[Workflow] was made with an earlier version of the framework, so I'll set its old files aside and start fresh. If it runs on a schedule, pause it first: [steps]. Say 'done' when it's paused, or 'no schedule'." It isn't asked again in the same chat once answered.
4. **Is it this step's?** If not, the line above, and stop.
5. **This step's own entry checks,** then its opening, or a resume line. When an entry check asks the leader something before the opening, its message starts with one line that names this step and the workflow and confirms the location (N-F3's promise clause), so a new chat never opens on a bare question; the opening then doesn't repeat that line.

## Earlier versions

A file is from an earlier version of the framework when:
- `requirements.md` has no `revision:` in its frontmatter, or has a `Definition Type` row, a `## Steps Overview` heading, or `## Inputs` with no `## Path`: the owner is Deconstruct;
- the plan is a `design-spec.md`, or a `design-plan.md` with no `requirements_revision:`: Design;
- there is a `test-results.md` but no `build-record.md`, and no `history/set-aside-*/` (a set-aside moves the results before the record): Build;
- `test-results.md` has no `round:`: Test.

Which skills or agents a node links is never a sign of an earlier version: a big change or a platform change sets the build record aside and leaves `# Skills` and `# Agents` linked.

The earliest in that order decides the owner. `run-guide.md` and `improvement-plan.md` are no sign on their own: the rule only checks whether a run guide exists (for N-B44, above), and nothing reads either.

**The owner starts fresh.** It moves that file, and every later file in the chain (plan, build record, results), into `history/earlier-version-[date]/`, where nothing reads them; says so in one line (where N-B44 was asked, its first sentence already said so, and isn't repeated); and begins as for a new workflow. The leader may still offer an earlier requirements file as something they have written down.

