# The catalog and registering the candidates

Read before the transition list (fast path: before the report), for a workflow with no process; at the catalog confirmation; at Phase 5's registration; and at the entry check for a `backlog.md` beside a registry.

**A workflow with no process** (registry present; otherwise candidates stay grouped by area of work). Before the transition list (fast path: before the report), check every candidate has a Process. Where none fits, teach the term and ask, once per new process, exactly:

**Ask:** "[Workflow] doesn't fit any of your processes. What would you call the set of related work it belongs to, and which function (the team or role that owns that kind of work) looks after it? Your functions are [the registry's Function names]."
- *Why:* every workflow sits under one process, and the process's owner owns the workflow too.
- *Example:* a bookkeeper might say: "Client Onboarding, and Client Services looks after it."
- *Not sure?* I'll suggest a name from your own words and the function in your registry that fits it best. You can change either later.

A person, or a function not in the registry, maps to the Function that fits, said in one line ("I'll put it under [Function]."); if none fits, **Ask:** "Shall I add [function] as a new function?", and on yes write a complete Function node per `registry/SCHEMA.md` (title, description, one sentence of charter prose, an empty GENERATED `# Owns` block) and its line in `registry/functions/index.md`. Never write an `owner:` matching no Function file. Write a complete minimal Process node per `naming-workflows` (never a default or ownerless stub), with its line in the right Line of Business's `# Processes` list and `registry/processes/index.md` (ask which line and where, if not obvious); the maintenance pass refreshes `# Owns`. The catalog shows it with "(new)".

**Catalog confirmation (one message)**, the student's one look before writing. Place each candidate under the Process where it was found, unless it clearly belongs elsewhere (it happens before that Process starts, or another Process's owner does it): then move it, with the reason in brackets after its description. Every process with workflows, in the report's order and numbers (other-lens or pick-up run: only this run's, 1 to N), each as name plus a one-sentence description of about 20 words, in the `naming-workflows` shape (one sentence: when it starts, what it produces, who receives or acts on it; no targets, no tool names), with "(already runs)" after work that already runs. No size, value lever, or ranking. No registry: open with "Here's your list of workflows.", drop the owner sentence, and the *Why* is "the name and description are what Deconstruct starts from later." Say exactly this, with the student's workflows:

> Here's what goes into your registry. Each workflow sits under the process it belongs to and is owned by that process's owner.
>
> **Process:** [Process]
> 1. **[Workflow name].** [One-sentence description.]
> 2. …

**Ask:** "Anything to rename, reword, move or leave out? You can answer by number, for example 'rename 4.'" (With fewer than four workflows on screen, use the highest number shown.)
- *Why:* the name and description are what you'll see on your dashboard, and what Deconstruct starts from later.
- *Not sure?* Say "looks good." You can edit any workflow later.

Apply every change to the report. A left-out workflow keeps its card, marked "Left out of the backlog", and gets no registry entry and no backlog line.

**Register the candidates (registry present)** as backlog Workflow nodes under their confirmed Process, in the registry (`registry/` locally, `Framework/registry/` on the web, through the connection), as the indexing-registry skill's `registry-bundle.md` says. Work that already runs gets `status: in-production` instead, never the backlog, and its skill or agent under `# Skills` or `# Agents`: a link when the file is in this workspace, else its name and home as plain text ("Newsletter Repurposer, a skill in your Claude account").

1. **Write the stub** at `registry/workflows/<slug>.md` (slug = kebab-case of the Workflow name), in the `naming-workflows` stub format, with `generated.at` the current UTC time:

   ```yaml
   ---
   type: Workflow
   title: "[Workflow name]"
   description: "[One sentence, naming-workflows shape: when it starts, what it produces, who receives or acts on it.]"
   generated: { by: process:analyze, at: YYYY-MM-DDTHH:MM:SSZ }
   status: backlog
   trigger: "[Trigger field]"
   ---
   # [Workflow name]

   [Description.]

   # Artifacts

   - [Opportunity report]([the report's link])

   # Skills

   # Agents

   # Insights

   <!-- GENERATED:insights -->
   <!-- /GENERATED -->
   ```

   The report's link is relative to the registry's parent folder: `framework/ai-opportunity-report.md` on Claude Code and Codex; `ai-opportunity-report.md` on the web and Claude desktop. The body repeats `description` on purpose. `trigger` is provisional. No `execution_mode` or `autonomy` (Design sets those); pain point, size, and value lever stay in the report.
2. Add each stub's line to its Process's `# Workflows` list and to `registry/workflows/index.md`, replacing any placeholder line there (`_No workflows captured yet._`, `_No entries yet…_`) (bundle-root-relative link: `[Weekly Status Report](/workflows/weekly-status-report.md)`). If a node for that slug, or for the same work under another name, already exists, merge — never overwrite fields already set, except the backlog-to-`in-production` move the history pass confirmed.

**The backlog with no registry** (locally and on the web; not on print-to-save, where the report carries the list): write `backlog.md` in the framework folder: a `# Backlog` heading, then a `## [Area of work]` heading per area in the report's order, each candidate as `[n]. **[Workflow name].** [One-sentence description.]` in the report's numbering. It holds only the candidates the catalog kept: never a left-out workflow, and never work that already runs, which stays in the report. A later run (picking up the rest, the other lens) adds its candidates under their areas, continuing the numbering. Never tell the student the file's name; speak of the report and the backlog.

**A `backlog.md` beside a registry** (Analyze's entry check 3: the registry exists, and `backlog.md` is still in the framework folder from before it was set up). Once a registry exists, its `backlog` nodes are the backlog, and nothing else reads `backlog.md`, so its candidates would drop out. Offer, in one line in your own words, to add the workflows it lists to the registry's backlog, naming how many. On yes:
1. Read the registry (Phase 1's reading, with no summary unless the student asks) and the report the candidates came from.
2. Place each candidate under the Process that fits it, asking *A workflow with no process* where none does.
3. Show the catalog confirmation with these workflows, in `backlog.md`'s order, and apply the changes.
4. Write each one's stub and index lines as above (a candidate already in the registry by what it is: merge, as above), with the report linked under `# Artifacts`, then the maintenance pass.
5. Move `backlog.md` into the framework folder's `history/` as `backlog-YYYY-MM-DD-HHMM.md` (locally and on a drive; never delete it), so it isn't offered again.
6. Say in one line how many were added, then carry on with the opening.

On no, leave `backlog.md` where it is, say in one line that those workflows stay out of the registry's backlog until they're added, and carry on with the opening. On print-to-save this check never runs.
