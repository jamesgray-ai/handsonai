# Choosing the workflow

Read for the backlog choice or cold entry: a new interview (routing state 3), after Deconstruct's own entry checks and the opening. Every quoted line is said exactly; each question is its own message.

## The backlog choice

Run it whenever there are backlog candidates, whether or not the leader mentions them. The candidates are:
- with a registry, the `status: backlog` Workflow nodes (`registry/` in a workspace; `Framework/registry/` in a drive or on Claude desktop), and only those: a `backlog.md` left beside a registry isn't read (Analyze offers to register what it lists, at its own entry);
- with no registry, the lines of `backlog.md` in the framework folder; with no `backlog.md`, the candidate list in the framework folder's `ai-opportunity-report.md`.

With a registry, no backlog node and a `backlog.md` still in the framework folder, say in one line (model wording) that the workflows listed there aren't in the registry yet, and give Analyze's start phrase with the framework folder as the location, to say in a new chat ("run the analyze skill. My files are in [location]."); then cold entry's question, in the same message, for a leader who wants to carry on here.

Leave out `in-production` nodes, candidates recorded as already running, and any candidate whose slug already has a workflow folder, with or without a registry: it's under way (an unfinished interview was offered by the entry checks; anything further along gets the one line below).

If the leader named a backlog workflow, use it. **A workflow named here or at cold entry** (rather than at entry) hasn't been routed yet: first check for a node or a workflow folder with its slug, or a node with its name. If there is one, apply `routing.md`'s states to it exactly as at entry, and say that state's line or take the route SKILL.md's state table gives (running work Analyze recorded is brought in: SKILL.md, *Running work brought in*; a retired one gets the retired line). Only a name with neither goes to cold entry. Otherwise show every candidate, numbered straight through under a "**Process:** [name]" label per process, each with its size where it has one, then:

**Ask:** "Which workflow from your backlog do you want to work on?"
- *Why:* for your first one, pick something small so you learn the whole loop before taking on something big. A good first workflow (1) has a handful of steps, (2) starts when you decide to start it, and (3) works from material you already have. Among those, pick the one that would help you most.
- *Not sure?* I'll use those three tests on your backlog and suggest one, with the reason.

Its variants:
- **Only the report holds candidates** (no `backlog` Workflow node in a registry and no `backlog.md`; a report beside a registry with backlog nodes doesn't count, so there it stays "from your backlog"): say "from your report" in place of "from your backlog" in the question, "on your report" in place of "on your backlog" in *Not sure?*, and label the groups "**Area of work:**". (With `backlog.md`, keep "from your backlog".)
- **Personal life:** label the groups "**Routine:**".
- **After a first workflow** (a workflow folder holding more than a progress file, or a node past `backlog`, not counting running work Analyze recorded): the *Why* drops its "for your first one…" sentence and says "A good next workflow" in place of "A good first workflow", keeping the three tests.
- **On *Not sure?*:** apply the three tests to what the candidates say and suggest one in a sentence that names the tests it passes; never claim a step count. A large pick goes ahead.

**Prefilled from the chosen candidate:** the name, description, trigger and deliverable, and any `Lens`, `Value lever`, `Business Objective`, `Stakeholders` and `Success Metrics`. Ignore any autonomy or involvement field on it, without comment. Ask for Lens (Individual for one person's repeated work, Organizational for work across roles), Owner and Stakeholders only when they aren't obvious. If the registry has a Business node with `## Objectives`, hold them for Part 1.

**Run by name with candidates.** When the leader runs Deconstruct by name and backlog candidates exist, the backlog choice runs; any workflow further along gets one line (model wording) naming where it is and its next step's start phrase with the location, unless the leader asked to change its requirements: then, in states 4 to 6 with no `build-record.md`, it's the re-run (`re-runs.md`), and otherwise SKILL.md's state table says what follows. Listen for that intent; when it's unclear, ask whether they want to change what it must do.

## Cold entry

No backlog, or a workflow not in it.

**Ask:** "Tell me about the workflow — what kicks it off, what you do, and what comes out the other end. Rough is fine."

When the leader already named the workflow, N-D1 comes first, and a document they offer stands in for this question (its trigger, work and deliverable are played back from it instead). With nothing named, N-D1 comes right after this answer.

Its answer prefills Part 2's trigger and deliverable, confirmed rather than asked again, and is played back at Part 4's method question (never as a path when the AI works it out each time). Ask for Lens, Owner and Stakeholders only when they aren't obvious.

**Work that already runs.** Never ask where the work runs today. A workflow named at cold entry is a new workflow, whatever the leader says about it, with no `Runs today` row. When the leader says it already runs somewhere (set up as an agent, on a schedule), acknowledge it in one line (model wording) so they know it was heard: Build will ask about the one they have before it installs anything. Ask nothing about it and record nothing.

**No workflow in mind.** Give Analyze's start phrase with the framework folder as the location, to say in a new chat ("run the analyze skill. My files are in [location]."; on Microsoft 365, "…My files are in OneDrive, in Framework."), in one line of model wording, and stop.
