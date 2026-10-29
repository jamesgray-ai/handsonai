# Re-runs, big changes, and calling one off

Read for a re-run before anything is built, a big-change redo, or calling either off. Every quoted line is said exactly; each question is its own message. There's no opening on either: its first line replaces it.

## Contents

- A re-run before anything is built
- A big change
- Calling it off
- What's saved

## A re-run before anything is built

Entered when the leader asks Deconstruct by name for a workflow in routing states 4 to 6 with no `build-record.md`.

1. **The first line** (model wording) names the workflow, confirms the location with N-F3's promise clause ("I'll read and save your files in [location]."), and says that the plan Design made, if there is one, stays and will be brought up to date. Then:

   **Ask:** "What should change in [Workflow]'s requirements? Or say 'go through it all', and I'll play back each part."
2. **One playback per part,** in part order (on the light track, per thing), in plain words, ending "What would you change or clarify?". Ask a part's questions only where the leader's answer to that question, or a correction in a playback, reaches; ask them as written, in their part's wording. Play back every part once, so the leader can catch anything else. Lines the requirements already hold are *(you said)*, including lines Design or Test changed, played back as recorded. Labels stay as they are; a new line takes the next number.
3. **"Nothing", or "keep it as it was",** before the new file is saved, calls it off (below).
4. **The preview, then "go ahead":** the current requirements go into `history/requirements-YYYY-MM-DD-HHMM.md`; the new file is written with `revision` raised by one and a `revisions:` entry (`by: deconstruct`, the `lines` added, changed or removed), keeping every earlier entry. New practice inputs take the next E numbers, and dropped ones move into `history/`. When a line is removed, take its ID out of every `tests:` header in `inputs/`, whichever step wrote the input; an input left testing nothing moves into `history/E[n]-[short-name]-YYYY-MM-DD-HHMM.md`, and its Example Scenarios row goes with it. A re-run that changes only practice inputs doesn't raise `revision`. The plan stays where it is: the raised revision sends Design to update it. The node's status stays. Then the close.

The progress file works as usual, with a fourth line `Re-run: [what should change]`, so a re-run stopped partway resumes, and Design waits until it's finished or called off.

## A big change

Entered by routing state 2: `big_change` is set (the node's field, or the requirements' frontmatter with no registry), written by Design when it judged a "change my workflow" big. Design has already moved the plan, build record and results into `history/set-aside-YYYY-MM-DD-HHMM/`; don't move them again.

**A set-aside that stopped partway.** If a results file (`test-results.md`, or a `history/test-results-*.md` at the top of `history/`, a finished round included), the build record or the plan is still in the workflow folder, first move what's left into the newest set-aside folder, in Design's order (results, then build record, then plan); with no set-aside folder yet (Design stopped after writing `big_change`, before its first move), create `history/set-aside-YYYY-MM-DD-HHMM/` and move them there. Say so in one line, so the redone requirements never meet the old plan. With a registry, then remove the node's "Design plan" and "Test results" links under `# Artifacts` if they're still there, since their files are now set aside, and restamp `generated`.

1. **The first line** (model wording) names the workflow and the recorded reason in plain words, confirms the location with N-F3's promise clause, and says that "keep it as it was" calls the change off. **A redo stopped partway** (a progress file with a `Big change:` line): give the resume line (SKILL.md, *Pause and resume*) in place of this first line, and carry on from its `Next:` part, never playing back again the parts already done.
2. **One playback per part** of what's recorded, in part order, in plain words, ending "What would you change or clarify?". Ask questions only where the recorded reason reaches, or a correction in a playback, as written. A part the reason doesn't touch gets its playback only.
3. **The track** stays as recorded, unless an answer shows a sign of risk on a light workflow (N-L2).
4. **The preview, then "go ahead":** the old requirements go into `history/requirements-YYYY-MM-DD-HHMM.md` (with no registry, that copy keeps `big_change`, and so the reason for the redesign; with a registry, the registry log keeps it, and its line is never removed); the new file is written with `revision` raised and a `revisions:` entry; a removed line comes out of every `tests:` header in `inputs/`, as on a re-run (*A re-run before anything is built*, step 4); `big_change` is removed (from the node, or left out of the new frontmatter). The node's status stays, so a live workflow stays `in-production` and keeps running until its new version is built and tested. Then the close: Design plans afresh.

The progress file's fourth line is `Big change: [the recorded reason]`. The wrong-place check (routing) matters most here: a redo started inside the live workflow's Project gets N-F7 and writes nothing.

## Calling it off

"Keep it as it was" (on a re-run before anything is built, "nothing" too), at any time before the new requirements are saved.

**A big change:**
- Move each file in the newest `history/set-aside-*/` folder back where it came from: `design-plan.md`, `build-record.md` and `test-results.md` into the workflow folder, and every `test-results-round-*.md` (and any other `test-results-*.md`) back to the top of `history/`, where Test reads its finished rounds.
- With a registry, put the node's "Design plan" and "Test results" links back under `# Artifacts`, for whichever of those files moved back, each only if it isn't there already, in the registry's link form (`- [Design plan](framework/[slug]/design-plan.md)` in a workspace, `- [Design plan]([slug]/design-plan.md)` in a drive and on Claude desktop; the same for `test-results.md`), and restamp `generated`.
- Remove `big_change`, and move the progress file, if any, into `history/`.
- Then say, naming only what was set aside:

  > OK, [Workflow] stays as it was: its [plan, build record and test results] are back in place, and nothing has changed.

  followed by the next step's start phrase with the location, by the routing rule. On a live workflow (routing state 11), no start phrase follows: end that line with "It keeps running as it is.", then say N-T19 (routing).

**A re-run before anything is built:** move the progress file, if any, into `history/`, then say:

> OK, [Workflow]'s requirements stay as they were, and nothing has changed.

followed by the next step's start phrase with the location, by the routing rule.

These are the only times Deconstruct moves another step's files (apart from an earlier version's files): here, and only back to where Design set them aside from; and when it finishes a set-aside that stopped partway, and only into the set-aside folder Design made. The same two are the only times it writes links another step owns.

## What's saved

The registry write keeps the node's status on a re-run and a redo; after a redo, it removes `big_change`. Everything else follows SKILL.md's Phase 7 and the requirements template.
