# Re-runs, big changes, and calling one off

Read for a re-run before anything is built, a big-change redo, or calling either off. Every quoted line is said exactly; each question is its own message. There's no opening on either: its first line replaces it.

## Contents

- A re-run before anything is built
- What every re-run and redo adds
- A big change
- Calling it off
- What's saved

## A re-run before anything is built

Entered when the leader asks Deconstruct by name for a workflow in routing states 4 to 6 with no `build-record.md`.

1. **The first line** (model wording) names the workflow, confirms the location with N-F3's promise clause ("I'll read and save your files in [location]."), and says that the plan Design made, if there is one, stays and will be brought up to date. Then:

   **Ask:** "What should change in [Workflow]'s requirements? Or say 'go through it all', and I'll play back each part."
2. **One playback per item,** in the interview's order (`interview.md`: the safety answers, what it's for, what it must get right, what it works from, its rules, its safety limits, the practice runs), in plain words, ending "What would you change or clarify?". Ask an item's questions only where the leader's answer to that question, or a correction in a playback, reaches; ask them as written in `interview.md`. Play back every item once, so the leader can catch anything else. A file the earlier interview wrote may hold steps, decisions and value figures this interview doesn't ask about: play them back as recorded, in plain words, and change a line only from what the leader says, in the requirements template's formats (never a rule or checkpoint that names a law as its reason ("…, as [the law] requires."): it isn't the leader's to change or drop; say in one line that the law requires it, so it stays); no question is asked about them, except the one fact a changed step line can't be written without (whether it's fixed or flexible), asked in your own words. A change that adds a write, a source or a run without the leader brings its safety limits (`interview.md`, *The safety limits*). Lines the requirements already hold are *(you said)*, including lines Design or Test changed, played back as recorded. Labels stay as they are; a new line takes the next number. No count line is said on a re-run. Then, in the same pass (*What every re-run and redo adds*, below): the new floor questions, a removal step as a `When` rule, and the one `expect:` message.
3. **"Nothing", or "keep it as it was",** before the new file is saved, calls it off (below).
4. **The preview, then "go ahead":** the current requirements go into `history/requirements-YYYY-MM-DD-HHMM.md`; the new file is written with `revision` raised by one and a `revisions:` entry (`by: deconstruct`, the `lines` added, changed or removed), keeping every earlier entry. New practice inputs take the next E numbers, and dropped ones move into `history/`. When a line is removed, take its ID out of every `tests:` header in `inputs/`, whichever step wrote the input; an input left testing nothing moves into `history/E[n]-[short-name]-YYYY-MM-DD-HHMM.md`, and its Example Scenarios row goes with it. A re-run that changes only practice inputs doesn't raise `revision`. The new file's `track:` is worked out again from the risk signs, as the interview writes it (`interview.md`, *What the file records about risk*), and the progress file's `Track:` line with it; nothing about it is said. The plan stays where it is: the raised revision sends Design to update it. The node's status stays. Then the close.

The progress file works as usual, with a `Re-run: [what should change]` line after the `Said:` line, so a re-run stopped partway resumes, and Design waits until it's finished or called off.

## What every re-run and redo adds

Requirements written before this release may lack what later steps now read. On a re-run or a redo, whatever the leader asked to change:

- **The new floor questions,** each asked as written, in its item's place in the playbacks, only where the file can't answer it:
  - how runs start (`Starts`), with how soon where it applies (`interview.md`, *How runs start*); `Per run` is inferred, never asked;
  - carry-over (`Remembers`), only when `Starts` is a schedule or an event checked on a schedule, or `Per run` is a batch (`interview.md`, *What it works from*);
  - the policy question (`Policy check:`), with the same trigger as in the interview (`interview.md`, *The policy question*): a source the leader described as confidential or regulated, or as holding client, staff or personal details, or a source plainly about clients, staff or individuals by its own name or by the Analyze report, the line filled with the source itself, never with a guess at what it holds; never for a row saved `Confidential` only as the safe fallback.
- **The safety limits,** when the file's Security section holds no constraint the leader kept (the one-line form, or no P line): show the safety limits message in its place in the playbacks (`interview.md`, *The safety limits*), since an older file can't say whether the leader ever saw it.
- **A removal step chosen here** (a "no" to the policy question, then "a step where someone removes…") is a `When` rule with its role tag, played back with the rules, never a new step, so no step is renumbered.
- **Old inputs with no `expect:` line.** Every input whose `source:` is `deconstruct` must carry one before the save. Fill them with **one drafted message** (model wording), never a question per input: for each such input, an expected result in plain words, taken from its Example Scenarios "What to look for" cell (for an input aimed at a D line, an out-of-bounds line or carry-over, from that line's own wording), each tagged *(my suggestion)*, ending "What would you change or add?". The rubber-stamp guard applies. The kept wording becomes the input's `expect:` line and the cell, word for word. It's its own message: right after the practice-runs playback when the re-run plays that part back, otherwise right before the preview, so it's said whatever the re-run touches.

## A big change

Entered by routing state 2: `big_change` is set (the node's field, or the requirements' frontmatter with no registry), written by Design when it judged a "change my workflow" big. Design has already moved the plan, build record and results into `history/set-aside-YYYY-MM-DD-HHMM/`; don't move them again.

**A set-aside that stopped partway.** If a results file (`test-results.md`, or a `history/test-results-*.md` at the top of `history/`, a finished round included), the build record or the plan is still in the workflow folder, first move what's left into the newest set-aside folder, in Design's order (results, then build record, then plan); with no set-aside folder yet (Design stopped after writing `big_change`, before its first move), create `history/set-aside-YYYY-MM-DD-HHMM/` and move them there. Say so in one line, so the redone requirements never meet the old plan. With a registry, then remove the node's "Design plan" and "Test results" links under `# Artifacts` if they're still there, since their files are now set aside, and restamp `generated`.

1. **The first line** (model wording) names the workflow and the recorded reason in plain words, confirms the location with N-F3's promise clause, and says that "keep it as it was" calls the change off. **A redo stopped partway** (a progress file with a `Big change:` line): give the resume line (SKILL.md, *Pause and resume*) in place of this first line, and carry on from its `Next:` item, never playing back again the items already done.
2. **One playback per item** of what's recorded, in the interview's order, in plain words, ending "What would you change or clarify?". Ask questions only where the recorded reason reaches, or a correction in a playback, as written in `interview.md`. An item the reason doesn't touch gets its playback only. Steps, decisions and value figures an earlier file holds are played back as recorded and changed only from what the leader says. A rule or checkpoint that names a law as its reason is never changed or dropped, whatever the recorded reason or the leader says: say in one line that the law requires it, so it stays (as on a re-run, step 2). The new floor questions, a removal step as a `When` rule and the one `expect:` message apply here too (*What every re-run and redo adds*).
3. **The file's `track:`** is worked out again at the file write (`interview.md`, *What the file records about risk*); nothing about it is said.
4. **The preview, then "go ahead":** the old requirements go into `history/requirements-YYYY-MM-DD-HHMM.md` (with no registry, that copy keeps `big_change`, and so the reason for the redesign; with a registry, the registry log keeps it, and its line is never removed); the new file is written with `revision` raised and a `revisions:` entry; a removed line comes out of every `tests:` header in `inputs/`, as on a re-run (*A re-run before anything is built*, step 4); `big_change` is removed (from the node, or left out of the new frontmatter). The node's status stays, so a live workflow stays `in-production` and keeps running until its new version is built and tested. Then the close: Design plans afresh.

The progress file has a `Big change: [the recorded reason]` line after the `Said:` line. The wrong-place check (routing) matters most here: a redo started inside the live workflow's Project gets N-F7 and writes nothing.

## Calling it off

"Keep it as it was" (on a re-run before anything is built, "nothing" too), at any time before the new requirements are saved.

**A big change:**
- Move each file in the newest `history/set-aside-*/` folder back where it came from: `design-plan.md`, `build-record.md` and `test-results.md` into the workflow folder, and every `test-results-round-*.md` (and any other `test-results-*.md`) back to the top of `history/`, where Test reads its finished rounds.
- With a registry, put the node's "Design plan" and "Test results" links back under `# Artifacts`, for whichever of those files moved back, each only if it isn't there already, in the registry's one link form on every platform (`- [Design plan](framework/[slug]/design-plan.md)`; the same for `test-results.md`), and restamp `generated`.
- Remove `big_change`, and move the progress file, if any, into `history/`.
- Then say, naming only what was set aside:

  > OK, [Workflow] stays as it was: its [plan, build record and test results] are back in place, and nothing has changed.

  followed by the next step's start phrase with the location, by the routing rule. On a live workflow (routing state 11), no start phrase follows: end that line with "It keeps running as it is.", then say N-T19 (routing).

**A re-run before anything is built:** move the progress file, if any, into `history/`, then say:

> OK, [Workflow]'s requirements stay as they were, and nothing has changed.

followed by the next step's start phrase with the location, by the routing rule.

These are the only times Deconstruct moves another step's files (apart from an earlier version's files): here, and only back to where Design set them aside from; and when it finishes a set-aside that stopped partway, and only into the set-aside folder Design made. The same two are the only times it writes links another step owns.

## What's saved

The registry write keeps the node's status on a re-run and a redo; after a redo, it removes `big_change`. Everything else follows SKILL.md's Phase 3 and the requirements template.
