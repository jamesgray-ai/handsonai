# A change to a live workflow, and an older version's copy

Read, before anything changes, on every Build run that changes a live workflow (a small change, fix mode, a rebuild after a big or platform change, a requirement change from Test, a kept or undone direct edit, a put-back), on an install that replaces an earlier-version workflow that is live or was built, on a retired workflow's put-back, on running work brought in (the requirements carry a `Runs today` row), whenever `schedule:` isn't `none` before go-live, when a schedule safety point fails on a live schedule, and for the copy of an older version after a yes to N-B51. Only the leader pauses, switches off or switches on a version that runs: give the steps, wait for their word, and never say you did it.

**Contents:** 1. The leader's pause, first · 2. The kept copy, next · 3. Running work brought in · 4. The change · 5. The close · 6. An older version's copy

## 1. The leader's pause, first

Ask on every Build run that changes a live workflow, replaces a live or built earlier version, or puts back a retired workflow, **whatever `schedule:` says** (a leader can schedule a workflow whose plan has no `SCH` task, and no step can see it). Before go-live, ask whenever `schedule:` isn't `none`. Said exactly, in the form that fits the record:

- **Switch-on steps in the record:** "Pause [workflow]'s schedule while I change it: [steps]. Say 'done' when it's paused, or 'no schedule' if it isn't running on one."
- **Before go-live, with `schedule: not-on`:** "If you've switched on [workflow]'s schedule, pause it while I change it: [steps]. Say 'done' when it's paused, or 'no schedule'."
- **No switch-on steps in the record** (a schedule the leader made by hand, or a plan with no `SCH` task): "If you've set up a schedule for [workflow] yourself, pause it while I change it. Say 'done' when it's paused, or 'no schedule'."
- **`schedule: paused` set since the last go-live** (a fix to the same change): **Ask:** "Is [workflow]'s schedule still paused from the last change? Say 'yes', or pause it now[ ([steps])] and say 'done'." (the steps only when the record has your switch-on steps).

Wait for "done" (or "yes" to the still-paused form), then write `schedule: paused`. "No schedule" leaves the value as it is. If the leader won't pause it, say exactly: "I can't change [workflow] while its schedule is on: a scheduled run could use the changed version before it's been tested. Pause it with [steps], then say 'done'; or say 'stop' and I'll leave it as it is." Wait; on "stop", end without changing anything (a stop, not a close). Before go-live with `schedule: none`, ask nothing.

## 2. The kept copy, next

Where files can be kept, save a copy of the current version in `history/kept-copy-YYYY-MM-DD-HHMM/`, or a Git commit where the folder is a repository. On a drive that can write, move the copy you already keep in `package/` into `history/kept-copy-YYYY-MM-DD-HHMM/` yourself, and ask only for what isn't there (a .zip the leader saved from the chat, say): **Ask:** "Do you have the copy you kept? If not, download it now: [steps]. Say 'done' when you have it." Write the steps to put the kept copy back in the record's "Put back the kept copy" section.

**With no copy,** don't change the workflow; say exactly: "I won't change [workflow] until you have a copy of the current version, so you can go back if the change goes wrong. [Steps to keep one on this platform.] Say 'done' when you have it, or 'stop' to leave it as it is."

**An agent on Microsoft 365:** the record's last pasted instructions are the copy when N-E1's agent form said nothing changed (`microsoft-365-agent.md` section 6); otherwise the line above, with Agent Builder's steps to copy its instructions out.

## 3. Running work brought in

You never built the version that runs today, so `package/` holds nothing of it. Before the first change, ask N-B41's no-steps form (the record has no steps). Then its kept copy is of what the `Runs today` row says is set up: copy each installed part you can read into `history/kept-copy-YYYY-MM-DD-HHMM/` (or a Git commit); for what you can't read, the no-copy line above with that platform's steps, holding the change until the leader has one (never the download question: there's no earlier copy to ask about). For work done by hand there is nothing installed to copy: say so in one line (model wording) in place of the kept copy. Where a new part goes in the old one's place, it's installed over it; anything of the old version you don't replace stays where it is until Test's go-live asks for it to be switched off for good, and "What was built" names it.

## 4. The change

Re-apply the protection before any check (on Claude Code, the block). On every platform, every changed part is staged in `package/` and installed together in Part 3, so the live version is never a mix of old and new parts, even across a pause or a stop. A stop in Part 2 leaves the live version as it was.

## 5. The close

N-B13 with this in place of its Test sentence and rounds sentence, said exactly:

"Your changed version is installed but not tested yet. Before its next real run, [N-B13's Test sentence for this platform, beginning 'start Test…']. If you need to run it before then, put back [the copy you kept / the earlier version, kept in [place]]: [steps]."

For a scheduled workflow, add before "If you need": "Keep its schedule paused until the test passes." Use "the earlier version, kept in [place]" where you kept the copy yourself.

## 6. An older version's copy

After a yes to N-B51 (or something you found at an install name or place, or an "already there" at the install line), once the leader has paused it: a copy only where the new version will be saved over the older one (a part of the same name or in the same place). Anywhere else nothing of the older version is touched, so the paused version is its own copy, and none is asked for. Where a copy is needed, in this order:

1. **On Claude Code and Codex, already in Git.** Check yourself whether the older version's files are committed and unchanged since (`git status` and `git log` on those files). If they are, that commit is the copy; say so in one line (model wording).
2. **You make it,** where you can reach the files (a skill folder in the workspace, Cowork's skills folder, files in a drive you can write): into `history/kept-copy-YYYY-MM-DD-HHMM/`, saying where in one line (model wording). Nothing is asked.
3. **Only where you can't reach the files** (a skill kept in a Claude or ChatGPT account), ask once: **Ask:** "Before I save the new version over your older one: are its files saved in GitHub or another version history?" A yes counts as the copy.
4. **The leader keeps one:** after a no, say exactly, and wait: "I won't save the new version over your older one until you have a copy of it, so you can go back to it. [Steps to keep one on that platform.] Say 'done' when you have it, 'no copy' and I'll install the new one under a different name so nothing is overwritten, or 'stop' to leave everything as it is." "Done" is the copy. "No copy" is never a dead end: install the new part under a different name, record that as a ruling, and say the new name in one line (model wording). The new name goes everywhere the old one would have: decided in Part 1, the parts are built with it; decided at Part 3's install, change the orchestrator's references to that part, and the start phrase in "What was built", to the new name, and run the built-text check again on what changed before that part is saved. The older version stays as it is, paused, and its line names it as still set up.

"Stop" at the pause form or here ends Build with nothing installed (a stop); the next entry asks again. Then write the older-version line (`build-record-template.md`), and, where a copy was kept, the steps to put the older version back in "Put back the kept copy". `schedule:` isn't touched: it belongs to the new workflow.

Where a new part takes the older version's place, it's installed over it when it's installed (on a first build on Claude Code and Codex, in Part 2; elsewhere in Part 3, with the install line's replace steps, ending by switching the skill on again where the leader switched it off). Then rewrite the older-version line in its replaced form, naming whatever of the older version is still set up, never the new part's place.
