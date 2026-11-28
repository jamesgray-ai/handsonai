# Fix mode

Read in fix mode (the last round is Not ready with Issues rows at Level `build` and no Build close since, reached by name or by "continue my workflow"), for a put-back of the built version, and for adopted direct edits. Fix mode runs in one pass with any other work this entry has: tasks whose `rev` rose after Design handled a change request, adopted direct edits, and an undo.

Reading this file, the record and the round is tool calls with no text: never a line naming fix mode, the files you read or what you'll do next. Your first text is a line for the leader (`SKILL.md`, its first rule), usually the opener (N-B14).

**Contents:** 1. The opener · 2. The fixes · 3. Adopted direct edits · 4. Putting back the built version · 5. The close

## 1. The opener

**First, three rounds in a row not ready** (counted from `test-results.md` and `history/test-results-round-*.md`, skipping `history/set-aside-*/`, `history/earlier-version-*/` and any round marked `round_status: abandoned`), unless the plan's `changes:` already logs a Build request whose `after_round` is the last round's number: before the opener, record a plan-only change request pointing to the results, and say exactly (N-B10): "Three test rounds in a row haven't reached Ready, so the problem is probably in the plan, not the build. I recommend going back to Design with what Test found. I've noted it for Design: say 'run the design skill. My files are in [location].'" (N-B10) Only if the leader insists on fixing anyway, withdraw your request and give the opener; otherwise nothing else is said.

**The opener** (N-B14, *your words*), naming what Test found and what will be redone in plain words ("the main skill that writes the summary", never an ID), and that everything else stays as it is. A model:

"Test found [what, in plain words] in [the part, in plain words]. I'll redo just that[, and re-check what uses it], and leave everything else as it is."

Nothing comes before it but the three-rounds line above.

Then, before anything changes:
- **A live workflow:** `live-change.md` (N-B41 straight after the opener).
- **A direct edit** to a part fix mode will redo: `SKILL.md`'s entry check 7.
- **The block** (Claude Code) is re-applied before any check, from a fresh list of each connection's tools, using the OK the record holds (the record's `## Claude Code profile` and `fingerprints.wrapper`, written only after the leader's OK to N-B20; with neither, ask N-B20 as Part 1 does). Re-applying it is `claude-code-block.md` section 4's steps 4 to 8 in full, never step 4 alone: the rules asked for, written to the settings, recorded, the check agent files written, and the settings read back with `settings-check`, all before the first check. It is no part of its own and asks nothing.

Fix mode announces no parts either (`SKILL.md`, before *Phase 1*): no part name or count, in any words.

## 2. The fixes

For each Issues row at Level `build`:
1. **Map it to its task:** the row's Task column; otherwise through the record's Artifact and Context ID columns.
2. **A Cause in a connection or permission** goes back to Part 1, for that connection only.
3. **A change the leader asked for at their real example** (the row's Cause is `leader's change`, the change itself in "What to change"): a ruling when it keeps every requirement line met; N-B29 and a change request when it would change what the workflow does; N-B34 when it would break a requirement line, in its fixed-step form when that line is a fixed step or a rule or checkpoint that names a law as its reason, which is never changed or dropped.
4. **A miss whose fix needs a requirement line changed:** N-B34, with no request; the task's row is `Built, misses [line]`, saved, so Test's next round finds it. N-B34 comes at the close, after the other fixes are saved, with its last sentence (Test's phrase). A fixed step, or a rule or checkpoint that names a law as its reason, gets N-B34's fixed-step form: a line a law requires is never offered to be changed or dropped.
5. **A miss whose fix needs the plan changed:** a plan-only change request pointing to the results. Fix and check the other tasks first; then N-B9.
6. **Otherwise** fix the task the way it was built: a brief of the change, from the kept copy in `built/`, to the platform's creator, then the check before saving (`creator.md` sections 2 to 5); then check it and every task that uses it again, up to three tries. **Every input tied to it:** re-check the fixed part on every input the round's Issues rows tie to this task (each row's Input column), one run each, not only the first; these inputs were already run in Test, so read each from `inputs/`, its header lines left out, and no other input there (Test saves every input it wrote that an Issues row names; the leader's real example is there only when they said yes to keeping it). Say which inputs you re-ran, by their plain labels, as the runs show them: never a count you promised before running them. An input a row names that isn't in `inputs/` (the leader's real example they didn't keep, or a round from before this release): say in one line *(your words)* that it couldn't be re-checked here, so Test's next round runs it.

Also:
- No fresh-chat run: Test's next round runs the fixed workflow whole (`fresh-chat-run.md` section 2).
- A change to a shared skill still gets N-B25 before anything of it is written, kept in `built/` until Part 3, with `SKILL.md` step 2's care for other live workflows that use it.
- Rebuilt skills replace the existing ones; a plugin's version rises. Every changed part is kept in `built/` and saved together in Part 3.
- **An agent on Microsoft 365** is fixed the way it was made: `microsoft-365-agent.md` section 5.
- A quick real check made in this entry (for a new kind of change) is offered for undo (N-B33).
- **Rulings live in one place.** A ruling recorded in fix mode stays in its row until Design next changes the plan, when Design writes it into the blueprint. A task rebuilt from a changed plan follows its blueprint, and its row starts its rulings afresh.

## 3. Adopted direct edits

When Design has handled a kept direct edit, the tasks it touches are marked `adopted: true`. For each, take the task's text from what's installed: from the installed part where you can read it, otherwise from the edited text saved in the file the change request's `what` names. Refresh `context/` from a kept edit to a runtime context copy. Record the task's `rev` and the new fingerprint, check it again, and regenerate only the parts another change touched.

## 4. Putting back the built version

Two triggers mean the same thing: `direct_edit: undo` in the results, and a `changes:` entry in the plan whose *what* is "put back the built version" (Design raised the touched tasks' `rev` without changing their content), whether for a direct edit, a retired workflow brought back, or any request to reinstall the workflow (every task).

For each part any of these touches, reinstall the version you built, from the kept copy in `built/` (in a folder built before this release, `package/` or `history/built-…/`), a kept copy in `history/kept-copy-…/` or Git, **never regenerated from the blueprint**, so the leader gets back exactly what was built; record the new `rev` as built; reset the fingerprint; and check it again. A part that's no longer installed is simply put back. Where you find no kept copy or Git version to put back, say so in one line (model wording) and rebuild those tasks from the plan. An agent on Microsoft 365 is put back by building it again from its kept prompts (`microsoft-365-agent.md` section 6). A task another change in the same update also touches is rebuilt from the plan instead, which leaves the edit out too. Tasks with no part to reinstall:
- **a setup task:** its read-back again; anything missing goes back to Part 1 for that item only;
- **`KW`:** its lines come back with the parts that carry them; find each one in the reinstalled text;
- **`SCH`:** its five points and N-B49 (`standard-tasks.md`) re-checked against the reinstalled build, its switch-on steps kept, and the schedule left paused until Test gives the switch-back steps.

It's a change to a live workflow when the workflow is live (`live-change.md`); a retired workflow brought back gets N-B41 first too. The Build close after that round settles it; nothing is cleared, since Build never writes the results, and Test decides the next round.

## 5. The close

- **The close's shape** (`package-and-install.md`, *The close*): its bold headline is the change itself ("**The booking link is out of the email.**"), never "Your workflow is built and checked".
- **"What was built"** is rewritten, and the close shows what changed in one line. **"What it can access"** is rewritten when a connection or permission changed.
- **N-B37** (`package-and-install.md`, section 4) is repeated for the new version (keep the old copy too).
- **The Test sentence** gives Test's start phrase with the location; Test decides what runs again. No rounds sentence. On a live workflow, N-B38. **Where N-B34 is said at this close,** its last sentence (Test's phrase) is the Test sentence: the close doesn't say Test's phrase a second time.
