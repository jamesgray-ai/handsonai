# Planning a schedule

Read when the requirements' `Starts` is `schedule: …` or `event: … · checked …` (with no `Starts` row, when the Trigger is a schedule). Part of `plan-template.md`: section 2's schedule rules, and section 7's `SCH` task.

## What to settle

**A schedule:** whether a scheduled run can reach the workflow's context from where it runs (a ChatGPT Project task can't read the Project's files; plan as if a Claude scheduled task can't read Project knowledge); what an unattended run does at each checkpoint (it ends the run and leaves a draft or a notification, never an assumed yes); and that stopping there rests on the workflow's instruction alone: no platform holds a run at a checkpoint in this release. A checkpoint before a change that can't be undone that rests on the instruction alone, where the change isn't a draft only, is a consequential point in the review. On Claude Code, where the workflow keeps a run log, recommend a desktop task: a cloud routine runs from a fresh clone of the remote, so its switch-on steps include the leader's push, and a re-check starts with a pull.

## The `SCH` task

**`SCH` — The schedule,** when `Starts` is `schedule: …` or `event: … · checked …` (with no `Starts` row, when the Trigger is a schedule):

```markdown
### SCH — The schedule
- **Builds:** the cadence (the leader's own; for an event, its checking interval; for `checked as often as it can`, the platform's shortest schedule, its figure written here only); where it runs; whether its context can be reached from there; for each checkpoint, what an unattended run does there and whether the platform holds the run or stopping rests on the instruction alone; the actions-per-run cap, sized from `Per run` where it's recorded
- **Uses / hands on:** the orchestrator's task (its actions-per-run cap and its checkpoints)
- **Meets:** Trigger[, Starts], [the G lines that must hold when it runs unattended]
- **Done when:** the connections are set up in the account that runs the schedule, the five safety points are checked and recorded, and the switch-on steps are written; it is never switched on
- **Depends on:** [the orchestrator's task], KW
- **rev:** 1
```

- **Where it runs:** on Claude Code with a run log, a desktop task by default; for a cloud routine, the leader's push before switching on and a pull before a re-check.
- **Context:** where it can't be reached from the schedule, the task places it where the run can read it, or the plan says the workflow runs by hand.
- **Checkpoints:** in a scheduled run, stopping at a checkpoint rests on the instruction alone on every platform in this release (above); each one before a change that can't be undone that rests on the instruction (not a draft) is a consequential point.
