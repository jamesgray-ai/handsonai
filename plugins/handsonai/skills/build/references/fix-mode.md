# Fix mode

Read in fix mode (the last round is Not ready with Issues rows at Level `build` and no Build close since, reached by name or by "continue my workflow"), for a put-back of the built version, and for adopted direct edits. Fix mode runs in one pass with any other work this entry has: tasks whose `rev` rose after Design handled a change request, adopted direct edits, and an undo.

**Contents:** 1. The opener · 2. The fixes · 3. Adopted direct edits · 4. Putting back the built version · 5. The close

## 1. The opener

Say exactly, naming what Test found and what will be redone in plain words ("the main skill that writes the summary", never an ID):

"Test found [what, in plain words] in [the part, in plain words]. I'll redo just that[, and re-check what uses it], and leave everything else as it is."

Before anything changes:
- **Three rounds in a row not ready** (counted from `test-results.md` and `history/test-results-round-*.md`, skipping `history/set-aside-*/`, `history/earlier-version-*/` and any round marked `round_status: abandoned`), unless the plan's `changes:` already logs a Build request whose `after_round` is the last round's number: record a plan-only change request pointing to the results, and say exactly: "Three test rounds in a row haven't reached Ready, so the problem is probably in the plan, not the build. I recommend going back to Design with what Test found. I've noted it for Design: say 'run the design skill. My files are in [location].'" If the leader insists on fixing anyway, withdraw your request and carry on.
- **A live workflow:** `live-change.md`.
- **A direct edit** to a part fix mode will redo: `SKILL.md`'s entry check 7.
- **The block** (Claude Code) is re-applied before any check, from a fresh list of each connection's tools, using the OK the record holds.

Signposts count only the parts fix mode runs ("Part 1 of 2 in this fix").

## 2. The fixes

For each Issues row at Level `build`:
1. **Map it to its task:** the row's Task column; otherwise through the record's Artifact and Context ID columns.
2. **A Cause in a connection or permission** goes back to Part 1, for that connection only.
3. **A change the leader asked for at their real example** (the row's Cause is `leader's change`, the change itself in "What to change"): a ruling when it keeps every requirement line met; N-B29 and a change request when it would change what the workflow does; N-B34 when it would break a requirement line.
4. **A miss whose fix needs a requirement line changed:** N-B34, with no request; the task's row is `Built, misses [line]`, saved, so Test's next round finds it. N-B34 comes at the close, after the other fixes are saved, with its last sentence (Test's phrase). A fixed step gets N-B34's fixed-step form.
5. **A miss whose fix needs the plan changed:** a plan-only change request pointing to the results. Fix and check the other tasks first; then N-B9.
6. **Otherwise** fix the task, and check it and every task that uses it again, up to three tries.

Also:
- The bare run is skipped (the installed skill would load).
- A change to a shared skill still gets N-B25.
- Rebuilt skills replace the existing ones; a plugin's version rises. Every changed part is staged and installed together in Part 3 when the workflow is live.
- **An agent on Microsoft 365** is fixed the way it was made: `microsoft-365-agent.md` section 5.
- A quick real check made in this entry (for a new kind of change) is offered for undo (N-B33).
- **Rulings live in one place.** A ruling recorded in fix mode stays in its row until Design next changes the plan, when Design writes it into the blueprint. A task rebuilt from a changed plan follows its blueprint, and its row starts its rulings afresh.

## 3. Adopted direct edits

When Design has handled a kept direct edit, the tasks it touches are marked `adopted: true`. For each, take the task's text from what's installed: from the installed part where you can read it, otherwise from the edited text saved in the file the change request's `what` names. Refresh `context/` from a kept edit to a runtime context copy. Record the task's `rev` and the new fingerprint, check it again, and regenerate only the parts another change touched.

## 4. Putting back the built version

Two triggers mean the same thing: `direct_edit: undo` in the results, and a `changes:` entry in the plan whose *what* is "put back the built version" (Design raised the touched tasks' `rev` without changing their content), whether for a direct edit, a retired workflow brought back, or any request to reinstall the workflow (every task).

For each part any of these touches, reinstall the version you built, from the staged package, the kept copy or Git, **never regenerated from the blueprint**, so the leader gets back exactly what was built; record the new `rev` as built; reset the fingerprint; and check it again. A part that's no longer installed is simply put back. Where you find no staged package, kept copy or Git version to put back, say so in one line (model wording) and rebuild those tasks from the plan. An agent on Microsoft 365 is put back by building it again from its kept prompts (`microsoft-365-agent.md` section 6). A task another change in the same update also touches is rebuilt from the plan instead, which leaves the edit out too. Tasks with no part to reinstall:
- **a setup task:** its read-back again; anything missing goes back to Part 1 for that item only;
- **`KW`:** its lines come back with the parts that carry them; find each one in the reinstalled text;
- **`SCH`:** its five points and N-B49 re-checked against the reinstalled build, its switch-on steps kept, and the schedule left paused until Test gives the switch-back steps.

It's a change to a live workflow when the workflow is live (`live-change.md`); a retired workflow brought back gets N-B41 first too. The Build close after that round settles it; nothing is cleared, since Build never writes the results, and Test decides the next round.

## 5. The close

- **"What was built"** is rewritten, and the close shows what changed in one line. **"What it can access"** is rewritten when a connection or permission changed.
- **N-B37** is repeated for the new version (keep the old copy too).
- **The Test sentence** gives Test's start phrase with the location; Test decides what runs again. No rounds sentence. On a live workflow, N-B38.
