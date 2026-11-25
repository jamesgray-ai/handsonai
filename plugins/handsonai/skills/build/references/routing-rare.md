
# Routing: the rare cases

Part of the routing rule (`routing.md`), kept apart so a normal run doesn't load it. Read the section that applies.

## A round left behind

When Test meets a round `in-progress` whose `plan_revision` isn't the current plan revision, or whose number is at or below the build record's `last_close_after_round` (Build closed while it was open), it moves the file to `history/test-results-round-[n].md` with `round_status: abandoned` and opens a fresh round, numbered n+1. So a Build close only ever counts as after a round that had finished.

## A retired workflow brought back

"Change my workflow" on a retired workflow goes to Design. Design sets the node's `status` to `under-development` and says so in one line. When there's a build record, Design logs one entry in the plan's `changes:` that puts back the built version of every task (source `change my workflow`, `what: put back the built version`), raising each task's `rev` without changing its content, together with any change the leader asked for. The direct-edit check runs first, and a task a kept edit touches is left out of the put-back; a big change or a change of platform sets the files aside instead, with no put-back. That sends the workflow to Build (state 6), which reinstalls the version it built, and then to Test (state 8), which re-checks it before it goes live again. With no build record, Design works out the state from the files and carries on, or gives the owner's start phrase with the location (Deconstruct's when the folder has no requirements yet). Its next go-live sets `status: in-production` again.

## Running work brought in

"Run the deconstruct skill on [workflow]" on running work Analyze recorded goes to Deconstruct, which takes it as a new workflow: its normal interview, starting from the leader's account of what the work does today, with where it runs today (by hand, set up somewhere, on a schedule) recorded in the requirements' `Runs today` row. That phrase is the only route in: the running-work message and the bring-in line both give it, and neither offers "change my workflow", which is Design's change phrase, so no line sends the leader from one phrase to the other. A leader who says "change my workflow" about running work anyway is sent once, to Deconstruct's phrase: any other step that receives it says the bring-in line (`routing.md`, *When this step isn't the owner*), which gives Deconstruct's start phrase naming the workflow in N-F2's new-chat form, and stops; Deconstruct, receiving it, takes it as the same request. The location is the working folder (on Claude Code and Codex, the framework folder), since the workflow has no folder yet. Once Deconstruct first saves its progress, the workflow has a folder, so it is no longer state 0, and the states above apply as for any workflow. The node stays `in-production`, so the workflow counts as live throughout: the version that runs today keeps running until Build installs the new one; before every Build run changes it, the leader pauses any schedule and a copy is kept of whatever is installed, as for any change to a live workflow, and Build waits for the leader's word; and Test, at the Ready round that takes the new version live, asks the leader to switch off for good the version that ran before, when it was set up somewhere or ran on a schedule. Running work is state 0 only where there's a registry: with none, Analyze keeps it in its report, and work named at cold entry is a new workflow.

## A cloud session

**A cloud session** (the session says it runs in the cloud, or the workspace is a fresh clone of a GitHub repository with nothing of the leader's own computer in reach): name the repository, never a path on the machine. N-F3's [location] is "your [repository] repository on GitHub", and the opening adds once: "Changes are saved to GitHub, on a branch." At the close, commit the step's own files and push them to the session's branch yourself, asking nothing (it is how the work is kept there; never rely on the platform to prompt it), and, whenever that branch isn't the repository's default, say N-F18: "Your work is saved on GitHub, on the branch [branch]. Before your next step, merge it into main, or choose this branch when you start the next session." There, the Git save-point offer isn't made. If you can't tell whether this is a cloud session, say N-F18 whenever the work was pushed to a branch other than the default.

## Earlier versions

A file is from an earlier version of the framework when:
- `requirements.md` has no `revision:` in its frontmatter, or has a `Definition Type` row, a `## Steps Overview` heading, or `## Inputs` with no `## Path`: the owner is Deconstruct;
- the plan is a `design-spec.md`, or a `design-plan.md` with no `requirements_revision:`: Design;
- there is a `test-results.md` but no `build-record.md`, and no `history/set-aside-*/` (a set-aside moves the results before the record): Build;
- `test-results.md` has no `round:`: Test.

Which skills or agents a node links is never a sign of an earlier version: a big change or a platform change sets the build record aside and leaves `# Skills` and `# Agents` linked.

The earliest in that order decides the owner. `run-guide.md` and `improvement-plan.md` are no sign on their own: the rule only checks whether a run guide exists (for N-B44, `routing.md`), and nothing reads either.

**The owner starts fresh.** It moves that file, and every later file in the chain (plan, build record, results), into `history/earlier-version-[date]/`, where nothing reads them; says so in one line (where N-B44 was asked, its first sentence already said so, and isn't repeated); and begins as for a new workflow. The leader may still offer an earlier requirements file as something they have written down.

