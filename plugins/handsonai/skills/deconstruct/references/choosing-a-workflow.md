# Choosing the workflow

Read for the backlog choice or cold entry: a new interview (routing state 3), after Deconstruct's own entry checks and the opening. Every quoted line is said exactly; each question is its own message.

## The backlog choice

Run it whenever there are backlog candidates, whether or not the leader mentions them. The candidates are:
- with a registry, the `status: backlog` Workflow nodes (`registry/` in the working folder), and only those: a `backlog.md` left beside a registry isn't read (Analyze offers to register what it lists, at its own entry);
- with no registry, the lines of `backlog.md` in the framework folder; with no `backlog.md`, the candidate list in the framework folder's `ai-opportunity-report.md`.

With a registry, no backlog node and a `backlog.md` still in the framework folder, say in one line (model wording) that the workflows listed there aren't in the registry yet, and give Analyze's start phrase with the working folder as the location, to say in a new chat ("run the analyze skill. My files are in [location]."); then cold entry's question, in the same message, for a leader who wants to carry on here.

Leave out `in-production` nodes, candidates recorded as already running, and any candidate whose slug already has a workflow folder, with or without a registry: it's under way (an unfinished interview was offered by the entry checks; anything further along gets the not-owner reply below).

If the leader named a backlog workflow, use it. **A workflow named here or at cold entry** (rather than at entry) hasn't been routed yet: first check for a node or a workflow folder with its slug, or a node with its name. If there is one, apply `routing.md`'s states to it exactly as at entry, and say that state's line or take the route SKILL.md's state table gives (running work Analyze recorded is brought in: SKILL.md, *Running work brought in*; a retired one gets the retired line). Only a name with neither goes to cold entry. Otherwise show every candidate, numbered straight through under a "**Process:** [name]" label per process, the labels listed in registry order (the Business node's `# Lines of Business` list, then each line's `# Processes` list; with no registry, the report's order), each with its goal where it has one (below), then:

**Ask:** "Which workflow from your backlog do you want to work on? Or name any other workflow."

A workflow named that isn't in the backlog is taken as a new one (cold entry, below), with no detour to Analyze.
- *Why:* Start small to learn the whole loop. Pick one that has a handful of steps, starts when you decide, uses material you have, and helps you.
- *Not sure?* I'll suggest one, with the reason.

**After a first workflow** (below), the *Why* is this one instead, word for word:
- *Why:* A good next one has a handful of steps, starts when you decide, uses material you already have, and would help you.

**The goal** comes from the Candidate Summary of the matching card in the Analyze report, read at its known place, `framework/ai-opportunity-report.md`, whatever form the node's or `backlog.md`'s link to it takes. The line reads "[name] (goal: [goal])", the goal's final full stop dropped. With no Goal row for a card, the report's **Goals and processes** row gives the goal of the candidate's process, when it has one. A candidate gets no goal clause when the report has no Goal row (an earlier version's report), when no card matches it (a workflow renamed since), or when its goal is "None named". Sizes are never shown, even from a report that still has them.

Its variants:
- **Only the report holds candidates** (no `backlog` Workflow node in a registry and no `backlog.md`; a report beside a registry with backlog nodes doesn't count, so there it stays "from your backlog"): say "from your report" in place of "from your backlog" in the question, and label the groups "**Area of work:**". (With `backlog.md`, keep "from your backlog".)
- **Personal life:** label the groups "**Routine:**".
- **After a first workflow** (a workflow folder holding more than a progress file, or a node past `backlog`, not counting running work Analyze recorded): the later-workflow *Why* above, word for word, in place of the first.
- **On *Not sure?*:** apply the *Why*'s tests (a handful of steps, started when the leader decides, material they have, and help to them) to what the candidates say and suggest one in a sentence that names the tests it passes; never claim a step count. A large pick goes ahead.

**Prefilled from the chosen candidate** (for a backlog pick, and for running work Analyze recorded):
- **From the Workflow node** (with no registry, the card's Candidate Summary row): the name, description and trigger.
- **From the matching card's Candidate Summary row** in `framework/ai-opportunity-report.md`: the deliverable and the frequency (for N-D23), and any `Lens`, `Value lever`, `Business Objective`, `Stakeholders` and `Success Metrics`. A trigger, deliverable or frequency the row marks "Not clear yet" stays "not clear yet" (the interview's first message settles the trigger and deliverable).
- **From the matching detailed card,** for the file's Value table, never asked about: the **Goal** (the registry goal it serves, or "None named"), the **Business Objective** on the Organizational lens, and **What changes for the business**; and its **Status** line, when the work already runs (SKILL.md, *Running work brought in*).
- **The Value table's Business Objective row:** the card's Business Objective on the Organizational lens when it names an objective, otherwise its Goal. Analyze's two fallbacks, "None of the stated objectives — protects …" and "No stated objectives — protects [what]", are Business Objective values only, and neither is a named objective. With Goal "None named" and no named Business Objective (either "protects …" fallback included), the row takes the card's value or "—", and is never asked about.

Ignore any autonomy or involvement field on the candidate, without comment. Ask for Lens (Individual for one person's repeated work, Organizational for work across roles), Owner and Stakeholders only when they aren't obvious. If the registry has a Business node with `## Objectives`, hold them for the file's Value table. With no report, no matching card, or an earlier report without these rows, the interview takes the fallbacks `interview.md` gives.

**Run by name with candidates.** When the leader runs Deconstruct by name and backlog candidates exist, the backlog choice runs; any workflow further along gets the routing rule's not-owner reply (`routing.md`, *Any other state*; SKILL.md's state table): where it is, then N-F2 in its platform form, word for word, with the next step's name and start phrase (never model wording for that sentence), unless the leader asked to change its requirements: then, in states 4 to 6 with no `build-record.md`, it's the re-run (`re-runs.md`), and otherwise SKILL.md's state table says what follows. Listen for that intent; when it's unclear, ask whether they want to change what it must do.

## Cold entry

No backlog, or a workflow not in it.

**Ask:** "Tell me about the workflow — what kicks it off, what you do, and what comes out the other end. Rough is fine."

When the leader already named the workflow, N-D1 comes first, and a document they offer stands in for this question (its trigger, work and deliverable are played back from it instead). With nothing named, N-D1 comes right after this answer.

Its answer prefills the trigger and deliverable in the interview's first message, confirmed rather than asked again. Ask for Lens, Owner and Stakeholders only when they aren't obvious.

**Work that already runs.** Never ask where the work runs today. A workflow named at cold entry is a new workflow, whatever the leader says about it. When the leader says it already runs somewhere (set up as an agent, on a schedule), acknowledge it in one line (model wording) so they know it was heard: Build will ask about the one they have before it installs anything. Ask nothing about it, and record what they said, in their words, as the Metadata's `Runs today` row ending `· where: not asked` ("set up as an agent; on a schedule, every Friday at 4 · where: not asked"), so Build asks its older-version question. Nothing else about it is recorded. Later questions are about the new workflow, never about how today's setup works or gets its input ("did you paste your notes in…?", "was the draft already waiting…?"). What they said about when it runs is already said: the how-runs-start question (`interview.md`) states it as theirs ("You said it runs every Friday at 4.") and asks only what it leaves open.

**"Not sure" to this question** is a thin answer (SKILL.md rule 9): one narrower follow-up, anchored in the last time they did repeated work. If they still have nothing in mind, it's *No workflow in mind*.

**No workflow in mind.** Give Analyze's start phrase with the working folder as the location, to say in a new chat ("run the analyze skill. My files are in [location]."; on Microsoft 365, "…My files are in OneDrive, in ai-workspace."), in one line of model wording, and stop.
