---
name: analyze
description: >
  This skill should be used when the user wants to analyze AI workflow opportunities,
  run a workflow audit, find automation candidates, or says "where can AI help".
  With the user's permission, looks through their saved memory and past chats
  for opportunities, walks their processes, then registers every candidate as a
  backlog Workflow node in the AI Registry (work that already runs as in
  production) with an opportunity report, ready for the Deconstruct step. Also use when the user says "continue my workflow"
  and framework/analyze-in-progress.md exists (an interrupted Analyze).
  It stays strategic: it names the work, the pain, and the value, never the tools or integrations.
  This is Step 1 (Analyze) of the AI Workflow Framework.
---

# Analyze Workflows

Analyze catalogs: it names each workflow and describes it well. It never ranks the workflows or picks one to build first; Deconstruct opens with that choice.

## Workflow

**Opening** (skipped when resuming or picking up the rest). Say exactly this, as two short paragraphs:

> "This step finds opportunities to create more value with AI in your business: friction to remove, and work you'd do more of, or do better, if you had the time. Each one becomes a **candidate workflow**: a specific, repeatable piece of work worth building with AI. I'll look through what your AI already knows about your work, if you allow it, then walk the processes in your registry with you. By the end you'll have every candidate saved to your registry's **backlog** (your list of workflows to build), with an opportunity report alongside (work that already runs is recorded as running). It runs in three parts: (1) how we'll look at your work, (2) where the opportunities are, and (3) your backlog and your report. Each process takes about 3 to 5 minutes, and you can do one or all of them. Step 2, Deconstruct, takes one workflow you choose from the backlog and maps it in detail. Stopping early is safe. Progress is saved."
>
> "I'll explain each question as I ask it, and 'not sure' is always a fine answer. If you've done this before, say 'skip the explanations'."

After "skip the explanations", drop the *Example* and *Not sure?* lines; the *Why* lines stay.

**Never show the Ask: label**; the student sees only the question. *Why*, *Example*, and *Not sure?* keep their labels. If the student works in the field an *Example* comes from, skip it and go straight to *Not sure?*.

**Signposts** (never phase numbers or names), at the top of each part's first message: "**Part 1 of 3 — How we'll look at your work.**" (on the Phase 1 summary when there is one, otherwise on the first Phase 2 question — the relationship question when it's asked, else the lens question; personal-life registry with no summary (same session): the lens confirmation), "**Part 2 of 3 — Where the opportunities are.**" (on the Part 2 intro), "**Part 3 of 3 — Your backlog and your report.**" (on the message telling the student about the report; a no-process question asked before the transition list stays in Part 2).

> **Registry entry:** a workflow's entry is its Workflow node in the `registry/` bundle (resolution, write rules, and your fields: `indexing-registry/references/registry-bundle.md`). With no `registry/SCHEMA.md`, right after the opening say once: "You don't have a registry yet, so your workflows will live in the report for now. When you want them saved and shown on a dashboard, say 'run the scaffolding-registry skill'." (a legacy `workflow.yaml` workspace: offer `scaffolding-registry`, which migrates it). Write no registry entries until it exists.

### Variants

Swaps apply to every quoted line, including approved wording, and every report heading, label, and column.

| Variant | Swaps |
|---|---|
| **No registry** | "ask about your work" for "walk the processes in your registry with you"; "every candidate listed in an opportunity report" for "every candidate saved to your registry's backlog (your list of workflows to build), with an opportunity report alongside (work that already runs is recorded as running)"; "It takes about 15 minutes" for "Each process takes about 3 to 5 minutes, and you can do one or all of them"; "your list of workflows" for "your backlog" and "the backlog" everywhere else (the opening's part 3, the Part 3 signpost, the transition line; the close has its own swaps); "your report" for "your registry"; "area of work" for "process" everywhere (the "**Area of work:**" label, the Summary Table column, the Candidate Summary field, the report summary line), in the student's words; if they named none, ask once which area each workflow belongs to before the transition list. Drop every mention of owners and the dashboard. Catalog: "Here's your list of workflows." for "Here's what goes into your registry."; a left-out workflow's card is marked "Left out of your list of workflows". |
| **No history to read** (no saved memory, no way to search past chats, and not Claude Code) | Start the opening's third sentence at "I'll walk…" (no registry: "I'll ask…"); skip the history pass. |
| **Personal-life registry** (the founding `registry/log.md` entry says so) | "routine" for "process", "area" for "line of business", "household" (or "your life" for one person) for "business", "role" for "function", "your [household / life]" for "your work"; the no-process question's parenthetical becomes "(the person in your household who handles that kind of work)", and its *Example* is dropped. The lens is always Individual: skip the lens question and confirm it in one line ("This registry is about your own life, so we'll look at the routines you run each day."). Drop the close's lens sentences, and add no other-lens note to the report. |
| **Fast path** | No signposts. Say only: "I'll register the workflows you name as **candidate workflows** in your registry's **backlog** (your list of workflows to build), with a report, in about 5 minutes. Step 2, Deconstruct, takes one you choose and maps it in detail." (no registry: "I'll list the workflows you name as **candidate workflows** in a report, in about 5 minutes. Step 2, Deconstruct, takes one you choose and maps it in detail.", then the no-registry line). The report has no **Not looked at yet** or **History** row and the close no "you looked at" sentences. |

### Fast Path

Only when the user says they don't want discovery ("I already know the three workflows, just register them"); a workflow merely mentioned, or already in the registry, is a **seed** for discovery. Infer the lens and confirm it, exactly:

**Ask:** "These sound like [your own work / work across the business], so I'll use the **[individual / organizational] lens**: [the work you personally do each day / the processes across the business, end to end]. Right?"

Then go to Phases 4–5. With a registry, read `## Objectives` and the Processes, and place each workflow under the Process that fits (ask when none does); with none, group by area of work. Facts (trigger, deliverable, pain point, size, systems, objective, stakeholders, metrics, the **Role** row) come only from the student or the registry (an objective the work plainly serves counts): omit **Role** with neither, mark other gaps "Not clear yet — Deconstruct settles it", and the size "Not sized yet". The value lever, why it's a good candidate, and how AI helps are your classification.

### Standard Path

#### Phase 1 — Read what's known

Read the registry bundle (the Business node and its `## Objectives`, which every later question ties back to; Lines of Business; Functions; Processes and owners; Workflow nodes), and this conversation and any files shared in it. Never make the user repeat what's there. Saved memory and past chats wait for the history pass. Ignore the session's tools, connectors, and MCP servers (they bias discovery), except to tell whether saved memory or past-chat search exists, and which skills the student set up.

**Same-session skip.** If `scaffolding-registry` ran earlier in this conversation, say "I'll use the registry we just built" and go to Phase 2. Otherwise summarize: "Your registry says you run [business] with [LOBs], working toward [objectives, if present]; the processes you named are [grouped by line of business — X, Y under A; Z under B], and you have [N] workflows — [N] in the backlog, [N] under development, [N] in production, [N] retired (omit zero counts; drop the workflows clause when there are none). Here's what else I know about your work: …" Drop the "what else I know" clause when there is nothing beyond the registry. Then, exactly:

**Ask:** "Is anything here wrong or missing?"
- *Why:* Analyze only looks inside the processes listed here, so a missing one means missed workflows.

A missing process the student names joins the walk's list marked "(new)" (picking up the rest too); write it only if it ends up holding a workflow, by *A workflow with no process* (ask its function then). A wrong entry: note it and say the registry can be reshaped later ("ask me to rename or move it"). Skip later questions the summary answers. With no registry and no context, say so and go to Phase 2.

#### Phase 2 — Lens selection

A named lens ("run the analyze skill with the individual lens") is confirmed in one line. Otherwise infer and recommend; never ask cold. Infer from `registry/log.md`'s founding entry and the Business node (or Phase 1's context): a company or unit the user owns or leads → Organizational; a team they work inside → Individual (their part of its processes); a household or their own life → Individual. If nothing says how the user relates to the business, ask first:

**Ask:** "Your registry describes [business name]. Is it your company, or do you work inside it?" (No registry: "Is the work we're looking at your own business's, or do you work inside an organization?")

Say exactly this (Organizational recommended):

**Ask:** "I'd look at this from the business's point of view: the processes that drive your goals, end to end. That's the **organizational lens**. Does that fit, or would you rather start with the work you personally do each day, the **individual lens**?"
- *Why:* the lens decides which work we look at — processes across the business, or your own tasks — so the candidates match what you want to improve.
- *Example:* a clinic owner might pick organizational to fix patient booking across the front desk; a sales manager might pick individual to cut their own weekly reporting.
- *Not sure?* Keep my suggestion. You can run the other lens afterwards.

Recommending Individual, say instead: "I'd look at this from your point of view: the work you personally do each day. That's the **individual lens**. Does that fit, or would you rather look at the processes across the business, end to end, the **organizational lens**?" (same *Why*, *Example*, and *Not sure?*). The other lens comes up again only in the close.

#### Phase 3 — Where the opportunities are

**The Part 2 intro (one message, after the lens).** Say exactly this, then the history question (or, with no history to read, the walk):

> "We're looking for opportunities to create more value: friction to remove, like work that's slow, repetitive, or inconsistent, and things you'd do more of, or do better, if you had the time. Each one becomes a candidate workflow. First I'll check what your AI already knows about your work; then we'll walk your processes for anything it missed."

Drop the last sentence when the history question won't be asked. With no Process nodes, say "then I'll ask about your work" for "then we'll walk your processes", and ask the individual bank's Q1 (role) next on either lens (before the history question, or as the first question when there's no history); its answer is the history filter.

##### History pass (before the walk)

Skip it with no history to read, or when an existing report's **History** row says Checked or Declined. Use no saved memory, even for the Phase 1 summary or when it's already in the conversation, until the student says yes. Ask exactly this, fitted to the platform: drop "and your past chats" when the platform can't search them, and "your saved memory and" when there is none; in Claude Code, say "your memory files and the requests you've typed into Claude Code on this computer, across all your projects" for "your saved memory and your past chats", dropping "your memory files and" when none exist.

**Ask:** "I can look through what your AI already knows about your work: your saved memory and your past chats. I'll summarize patterns, not quote anything. Want me to?"
- *Why:* if you've asked your AI for help with the same work before, your history shows candidates you'd otherwise have to remember.
- *Not sure?* Say no, and we'll go straight to your processes (no registry: "and I'll go straight to asking about your work").

On no, go to the walk. On yes, read only these, in plain words, never by a tool's name:
- **Saved memory**, and **past chats** where the platform searches them on request: work asked about more than once, things drafted regularly, skills or agents set up, each process name.
- **Claude Code:** the memory files (the workspace's and user's `CLAUDE.md`, and `~/.claude/projects/<project>/memory/MEMORY.md`) and the typed prompts in `~/.claude/history.jsonl`, which covers every project, so keep only this registry's work. First tell the student in one plain line that the app will ask them to approve reading it. Never open that file directly (it holds pasted content): extract `display`, `project`, and `timestamp`, each prompt cut to about 200 characters, newest first, about 1,000 entries or 90 days, into a scratch file outside the workspace (the session's scratchpad, else the system temp folder) — `jq -r '[.timestamp,.project,(.display|.[0:200])]|@tsv' ~/.claude/history.jsonl | sort -rn | head -1000 > [scratch file]`, or a one-line `python3 -c` without `jq`. Read it in pages, newest first; delete it once you've shown what you found. Never read session transcripts (the `.jsonl` files under `~/.claude/projects/`): they hold file contents and command output.

**Filters.** Keep work that fits the registry's business (no registry: the work described; personal-life: its areas). Leave out one-off questions and personal topics (personal-life: anything outside its areas) unlisted. Repetition is evidence, not a requirement; include work that already runs. No cap. Work already in the registry (matched by what it is, not only its name) is named on one line ("[Workflow] is already in your registry"), except a backlog node the history shows a skill or agent runs: list it as a numbered item ("[Workflow]: already in your backlog; your history shows [skill] runs it"). If the already-runs questions confirm it, it is recorded as running at registration, with its `# Skills` / `# Agents` entry and a card (Phase 4), any improvement written in; its transition and catalog line reads "[Workflow] is already in your registry, now recorded as running", and it counts in the close's [M].

If nothing fits, say "I didn't find anything in your history that fits [business]." (no registry: "that fits the work you described") and go to the walk; if everything found is already registered, name those lines and go to the walk.

**Show what you found** in one message under "**Process:** [name]" labels (no registry: none until areas are named), numbered straight through, each a short name plus its evidence in one clause ("you've asked for help with this about 6 times since August", "you have a skill that drafts these"). End with "I left out one-off questions and anything outside [business]." (no registry: "anything outside the work you described"; personal-life registry: "anything outside the areas in your registry"). Then:

**Ask:** "Which of these are worth keeping? For each, say keep, drop, or 'already handled'. You can answer by number, for example 'keep 1 and 3, drop 2'."
- *Why:* only what you keep goes into your backlog, so you decide what counts.
- *Not sure?* Keep anything you'd be glad to stop doing by hand. You can drop it later.

**Kept items.** Draft each one's problem and size from the evidence, one item per message (the one place you propose a problem first, since it rests on their own history); record only what the student confirms or says instead.

**Ask:** "[Name]: [the evidence, in one clause, such as 'you've asked for help with this about 6 times since August' or 'your memory says you write these every week']. My guess: [size], and [problem]. Is that right?"
- *Why:* that tells us roughly what it's worth to fix, and it goes in your report.
- *Not sure?* Say what's right, and I'll mark the rest "not clear yet".

**Work that already runs** ("already handled", or kept when the evidence shows a skill or agent runs it) gets no size guess. If the evidence shows no skill or agent, first **Ask:** "Does a skill or agent you set up do that?" (no: drop it). Then, in its own message:

**Ask:** "Do you use it regularly?"
- *Why:* only work you use regularly is recorded as running.

If not, treat it as a kept item. If yes, in its own message:

**Ask:** "Does it work well, or could it be better?"
- *Why:* if it could be better, your report says what to improve.

If the evidence doesn't name it, then **Ask:** "What's it called, and where does it live?" (*Not sure?* I'll write "a skill in your [platform] account".) It is registered as already running (Phase 5).

##### The walk

Whenever `registry/processes/` has nodes, on either lens, the Processes are the agenda (the banks below supply probes) and the walk covers what the history missed, never re-asking a kept piece. Registry order (the Business node's `# Lines of Business` list, then each line's `# Processes` list) is value-chain order, not a ranking. Organizational lens: the process end to end; Individual: "your part of this process." Tie each answer to the objective it threatens; the card's Business Objective (Organizational only; on Individual the objective only shapes the goal clause) reads "None of the stated objectives — protects [what it protects]" when none fits, or "No stated objectives — protects [what it protects]" with no `## Objectives` block (then don't ask the organizational bank's Q1). Skip any Process the user says is fine.

**Which process first.** Say exactly this (opening with "Now let's walk your processes for anything your history missed." when the history pass showed anything), then the processes numbered straight through, one per line, under a "**Line of business:** [name]" label per line:

> "You don't need to do all [N] today. Pick one process to start; each takes about 3 to 5 minutes. After each one you can keep going or stop, and your progress is saved. If a process runs fine, say so and we'll skip it."

**Ask:** "Which process do you want to start with? Give me the number."
- *Why:* starting where it matters most means your most useful candidates come first, even if you stop early.
- *Not sure?* I'd start with [one process], because it drives [the objective]. (With no objectives: the one where the work feels slowest or most repetitive.)

Name each process as you start it, with its goal ("[Process] (goal: [the objective it serves])"; no goal clause when it serves none). After its close line, **Ask:** "Want to look at another process? Give me its number, or say 'stop here for now'." (relisting those not looked at, with their original numbers). No time limit; walk only what the student picks. Processes not walked go in the report's **Not looked at yet** row (never one created this run).

**The walk question, once per process,** anchored in its most recent real run, in the student's words with its real start and end. Ask it open: never list likely pain points first (students echo the list). Guesses come only from the history pass or *Thin answers* step 3. Say exactly this on the first process; later, the **Ask:** and *Why* lines:

**Ask:** "Take the last time [process] ran, from [its start] to [its end]. Where did the time go, or where did it get stuck?" (Individual lens, except a personal-life registry: "Take the last time you did your part of [process], from [its start] to [its end]. Where did the time go, or where did it get stuck?")
- *Why:* the places where time or results are lost, or where doing more would pay off, are where a workflow is worth building.
- *Example:* a property manager might say: "Turning over a unit. I chase three contractors by phone, then re-enter the dates in two calendars."
- *Not sure?* Tell me the one part you'd hand to someone else tomorrow if you could.

When the answer is all about lost time, ask once per process:

**Ask:** "If that took no time at all, what would you do with it, or do more of?"
- *Why:* some of the best opportunities are work you'd do more of, not just work you'd do faster.

A new piece it names is an opportunity like any other.

**Pieces of work.** Play several back as separate pieces ("That's three pieces of work: launch emails, waitlist follow-up, and promotion across channels."), taking first those with a named problem or wanted more of. If the rest were only steps, ask once:

**Ask:** "Of the other [N], which ones slow you down or could be better, or would you do more of with the time? We'll skip any that run fine."
- *Why:* a step that runs fine isn't worth building, so we only keep the ones with a problem or a payoff.

A piece becomes an opportunity only when the student names a problem with it, or value in doing more of it.

**Depth rule — stay strategic.** An opportunity is complete with the work, the problem, its size (how often or how much), and the goal; stop then. At most one follow-up, only for a missing element (usually size); one thing per message; when a piece is unclear, ask about the last real time ("Think of the last proposal you sent. What did you do after it went out?"). Never ask about inputs, rules, steps, or edge cases (Deconstruct's job). When the size is missing, say exactly this on the first piece; later, the **Ask:** and *Why* lines:

**Ask:** "Roughly how much time does [the piece of work] take you in a typical week or month?"
- *Why:* that tells us roughly what it's worth to fix, and it goes in your report.
- *Example:* an accounts clerk might say: "About four hours at every month end."
- *Not sure?* A rough guess is fine. If you'd rather not guess, I'll mark it "not sized yet", and Deconstruct asks for today's number when you map it.

When the problem is quality, or work not done at all, ask how often instead ("Roughly how many [scoping calls] do you have in a typical month?", same *Why*), and record the size as the count plus what it affects ("4 calls a month; better calls mean more proposals accepted").

Name a clear starting point and result in one clause ("Repurposing has a clean starting point, a finished issue, and a clear result, LinkedIn and Substack posts, so it's a strong candidate").

**Close each process in one line**, naming everything noted from it: "Noted for [process]: [piece 1], [piece 2], [piece 3]. That's enough for the report. Deconstruct goes into the detail later."

**Fallback — no Process nodes.** Use the question bank for the chosen lens, exactly as below.

> **Ask one question at a time — these banks are a scaffold for you, not a list to paste at the user.** Adapt to their answers, skip anything the history pass already covered, and follow up for concrete examples.

**Individual Lens — Discovery Questions**

1. **Role & responsibilities** — What is your role? What are you accountable for?
2. **Repetitive tasks** — What tasks do you perform daily or weekly that feel repetitive, tedious, or low-value?
3. **Information synthesis** — Where do you spend time gathering, combining, or making sense of information from multiple sources?
4. **Multi-step processes** — What workflows involve multiple handoffs, approvals, or sequential steps?
5. **Quality & consistency** — Where do errors, inconsistencies, or quality issues tend to creep in?
6. **Communication overhead** — What recurring communications (status updates, reports, summaries) take more time than they should?
7. **Decision-making** — What decisions require you to weigh multiple factors or reference past precedents?

**Organizational Lens — Discovery Questions**

1. **Business objectives & outcomes** — What are your top 2-3 business objectives or OKRs? What outcomes drive success?
2. **Value chain & core processes** — What are the key end-to-end processes that deliver on those outcomes? (lead-to-close, hire-to-onboard, order-to-fulfill, etc.)
3. **Cross-functional handoffs** — Where do processes cross team boundaries? Where do things fall through cracks?
4. **Bottlenecks & cycle time** — Which processes take too long? Where do things stall waiting on people, approvals, or information?
5. **Consistency & quality risk** — Where do different people handle the same process differently? Where does inconsistency create risk?
6. **Visibility & measurement gaps** — Which processes lack metrics on performance, cycle time, or quality?
7. **Scale constraints** — Which processes break when volume increases? What works for 10 customers but not 100?

**Adaptive ordering:** start with the areas Phase 1 revealed least; skip what the history covered; with a registry, confirm Q1 and Q2 rather than re-ask. Probe for concrete examples: "I spend 30 minutes every Monday formatting a status report from three Jira boards" is far more useful than "I do reporting."

**Thin answers.** When an answer is too vague to name the work or the problem:
1. Play back what you have: "So far I have: [their words]."
2. Ask one narrower follow-up anchored in a real instance: "Think of the last time you did this. What happened first?"
3. If it's still thin after two tries, propose a guess to react to. Say: "Here's my guess: [X], [Y], or [Z], from what you've told me about [your role / this process]. What's right and what's wrong?"
4. If they still don't know, move on: leave the process under **Not looked at yet**, or record the size as "Not sized yet". Never invent an opportunity and record it as theirs.

##### Transition

When the student stops or every process is done (no Process nodes: the role answered and 3+ concrete opportunities; if the history alone produced them, first **Ask:** "Want me to ask about your work for anything your history missed, or stop here?"), and every piece has a process (*A workflow with no process*; a new one is marked "(new)"): number the opportunities straight through under "**Process:** [name]" labels in registry order (no registry: the order named; on an other-lens run, only this run's pieces 1 to N), the order and numbers the report and catalog reuse, with "(already runs)" after work that already runs. Pieces matching an existing workflow (by what the work is) go on one line instead ("[Workflow] is already in your registry", adding ", now recorded as running" for one the history pass moved). Then, exactly:

**Ask:** "Anything to add? If not, I'll add these to your registry's backlog, and write up a short opportunity report alongside. You'll see exactly how they'll look in your registry before anything goes into it."
- *Why:* anything you add now goes into the same catalog you'll check next.

With work that already runs, say "add these to your registry" for "add these to your registry's backlog". With no registry, say: "Anything to add? If not, I'll write up your opportunity report with all of these. You'll check the list before it's final."

#### Phase 4 — Opportunity report

**Self-check each opportunity** for a **concrete trigger** and a **tangible deliverable**. If one is fuzzy and its one follow-up is unused, ask it (never on the fast path); otherwise mark it "Not clear yet — Deconstruct settles it". Never drop an opportunity the student named. On the fast path, first settle any workflow with no process.

**Work that already runs.** On its card and in the Candidate Summary, *Pain point* reads "None stated — runs well" or the improvement the student named, and *How AI helps* describes what the skill or agent does today. Never invent either. **A registry workflow the history pass moved to running** gets an unnumbered card under its process, headed "[Workflow] (already in your registry, now recorded as running)", with no Summary Table or Candidate Summary row, not counted in **Opportunities identified**.

**Telling the student about the report**, in a few lines: how many opportunities, under how many processes, where it's saved (print-and-save: where to save it), and what each card holds (the problem, what AI would do, its size). Define the value lever the first time it appears, exactly: "Each card names its **value lever**: the kind of value AI creates here — Streamline, Automate, Accelerate, or Create value." Never present a ranking, a top pick, or an impact rating.

#### Phase 5 — Candidates registered

Every candidate goes into the backlog (work that already runs is registered as running). No cap, and no "which do you want to build?" question.

**A workflow with no process** (registry present; otherwise candidates stay grouped by area of work). Before the transition list (fast path: before the report), check every candidate has a Process. Where none fits, teach the term and ask, once per new process, exactly:

**Ask:** "[Workflow] doesn't fit any of your processes. What would you call the set of related work it belongs to, and which function (the team or role that owns that kind of work) looks after it? Your functions are [the registry's Function names]."
- *Why:* every workflow sits under one process, and the process's owner owns the workflow too.
- *Example:* a bookkeeper might say: "Client Onboarding, and Client Services looks after it."
- *Not sure?* I'll suggest a name from your own words and the function in your registry that fits it best. You can change either later.

A person, or a function not in the registry, maps to the Function that fits, said in one line ("I'll put it under [Function]."); if none fits, **Ask:** "Shall I add [function] as a new function?", and on yes write a complete Function node per `registry/SCHEMA.md` (title, description, one sentence of charter prose, an empty GENERATED `# Owns` block) and its line in `registry/functions/index.md`. Never write an `owner:` matching no Function file. Write a complete minimal Process node per `naming-workflows` (never a default or ownerless stub), with its line in the right Line of Business's `# Processes` list and `registry/processes/index.md` (ask which line and where, if not obvious); the maintenance pass refreshes `# Owns`. The catalog shows it with "(new)".

**Catalog confirmation (one message)**, the student's one look before writing. Place each candidate under the Process where it was found, unless it clearly belongs elsewhere (it happens before that Process starts, or another Process's owner does it): then move it, with the reason in brackets after its description. Every process with workflows, in the report's order and numbers (other-lens run: only this run's, 1 to N), each as name plus a one-sentence description of about 20 words, "When/From [trigger], [what it produces]", with "(already runs)" after work that already runs. No size, value lever, or ranking. No registry: open with "Here's your list of workflows.", drop the owner sentence, and the *Why* is "the name and description are what Deconstruct starts from later." Say exactly this, with the student's workflows:

> Here's what goes into your registry. Each workflow sits under the process it belongs to and is owned by that process's owner.
>
> **Process:** [Process]
> 1. **[Workflow name].** [One-sentence description.]
> 2. …

**Ask:** "Anything to rename, reword, move or leave out? You can answer by number, for example 'rename 4.'" (With fewer than four workflows on screen, use the highest number shown.)
- *Why:* the name and description are what you'll see on your dashboard, and what Deconstruct starts from later.
- *Not sure?* Say "looks good." You can edit any workflow later.

Apply every change to the report. A left-out workflow keeps its card, marked "Left out of the backlog", and gets no registry entry.

**Register the candidates (registry present)** as backlog Workflow nodes under their confirmed Process. Work that already runs gets `status: in-production` instead, never the backlog, and its skill or agent under `# Skills` or `# Agents`: a link when the file is in this workspace, else its name and home as plain text ("Newsletter Repurposer, a skill in your Claude account").

1. **Write the stub** at `registry/workflows/<slug>.md` (slug = kebab-case of the Workflow name), in the `naming-workflows` stub format:

   ```yaml
   ---
   type: Workflow
   title: "[Workflow name]"
   description: "[Description sentence]. [Deliverable folded in as the outcome sentence.]"
   generated: { by: process:analyze, at: YYYY-MM-DD }
   status: backlog
   trigger: "[Trigger field]"
   ---
   # [Workflow name]

   [Description.] [Deliverable sentence.]

   # Artifacts

   - [Opportunity report](framework/ai-opportunity-report.md)

   # Skills

   # Agents

   # Insights

   <!-- GENERATED:insights -->
   <!-- /GENERATED -->
   ```

   The body repeats `description` on purpose. `trigger` is provisional. No `execution_mode` or `autonomy` (Design sets those); pain point, size, and value lever stay in the report.
2. Add each stub's line to its Process's `# Workflows` list and to `registry/workflows/index.md`, replacing any placeholder line there (`_No workflows captured yet._`, `_No entries yet…_`) (bundle-root-relative link: `[Weekly Status Report](/workflows/weekly-status-report.md)`). If a node for that slug, or for the same work under another name, already exists, merge — never overwrite fields already set, except the backlog-to-`in-production` move the history pass confirmed.

**After the catalog confirmation:** append the Workflow Candidate Summary (*Output*), write the nodes, add the other-lens note (unless both lenses are done, or personal-life), run the `indexing-registry` maintenance pass if `registry/SCHEMA.md` exists (best-effort; a failed refresh never fails this step), then the close.

### Resuming and picking up

**Progress file** (`framework/analyze-in-progress.md`, which makes "Progress is saved" true): save it after the lens, the history pass, the process pick, each completed opportunity, and each process (no Process nodes: also the role answer), in plain words, since the student sees it written:
- the lens; the run ("Run: new", "Run: picking up the rest", or "Run: other lens ([lens])");
- the history pass: "History: not checked yet"; "History: checked; still to confirm: […]" after the keep-or-drop answer, each item with its name, process and evidence clause (its drafted guess only once you've asked it), and each "already handled" answer awaiting the already-runs questions; "History: checked; kept …"; "History: declined"; "History: nothing to read";
- work that already runs as "already runs with [name], [where it lives]; works well" or "could be better: [what]"; and "registry workflows to record as running: [name], [skill or agent], [where it lives], [works well / could be better]";
- the processes in the order picked, each "looked at", "in progress", "runs fine", or "not looked at yet", with each process's or area's noted pieces (work, problem, size, goal, as far as known); no Process nodes: also role, domain, and questions covered;
- after writing the report, "Report written; list not confirmed yet".

Say nothing about it. Delete it once the Workflow nodes are written (no registry: once the catalog is confirmed). Print-and-save mode: no file.

**Resume** (the file exists; this beats the pick-up offer, and both replace the opening). Say what was noted ("Last time we covered [processes]; I noted [pieces]"; with no Process nodes: "Last time we talked about [the topics covered, in plain words]; I noted [pieces]"; with nothing noted yet, just "Let's pick up where we left off."), then continue, with no lens question, from the first step not covered:
- "Report written; list not confirmed yet" → the catalog confirmation;
- "History: not checked yet" → the history pass; "still to confirm" → the next item on that list;
- no process picked → the process pick;
- a process marked "in progress" → "Want to pick up [process] where we left off?";
- otherwise → the "Want to look at another process?" question with the processes not looked at;
- with no Process nodes → the first discovery question not covered.

On "Run: picking up the rest", the pick and every relist offer only this lens's **Not looked at yet** processes. A resumed "Run: other lens" or "Run: picking up the rest" merges into the existing report.

**Picking up the rest.** With no progress file, a **Not looked at yet** row in the report (or an older **Noted, not walked** row), and no other lens named, run Phase 1, then, in place of the opening and lens question, **Ask:** "Last time you looked at [processes]. Want to pick up with the rest?" On yes: the lens whose row lists processes (ask only when two do); the history pass unless **History** says Checked or Declined; the process pick with only those processes; merge as for the other lens, leaving **Lens** and the other-lens note unchanged. On no, run a fresh analysis.

**The other lens** is offered only in the close. Under the report header, note that it hasn't been run (never for personal-life; **Lens** keeps the lens used). When the student runs it, run Phases 2–5 on that lens (in a later session, Phase 1 first, with the existing report), and merge; the catalog numbers only this run's workflows. A piece matching a registered workflow: say "[Workflow] is already in your registry; I'll add what we learned to its card", update its card, and leave it out of the catalog numbering and the close's [N]. Set **Lens** to "Individual + Organizational" and remove the note.

**Merging into the report:** add the cards under their processes; extend the Summary Table and Candidate Summary; combine **Opportunities identified**; keep one **Not looked at yet** row per lens ("Not looked at yet ([lens] lens)"), renaming an older **Noted, not walked** row; set **History** to this run's result when the pass ran. A fresh same-lens analysis instead renames the old file to `ai-opportunity-report-YYYY-MM-DD.md` (today) first.

**"Continue my workflow"** with no progress file: check `registry/workflows/` and `framework/`. If `outputs/` holds a framework record from before 9.0, follow *Moving a pre-9.0 record out of outputs/* in the indexing-registry skill's registry-bundle reference first. If the student kept the pre-9.0 layout (`registry/log.md` has a "Kept the pre-9.0 `outputs/` layout" entry), an existing workflow's artifacts are in `outputs/[workflow-name]/`, not `framework/[workflow-name]/`, and while `outputs/ai-opportunity-report.md` exists, `framework/ai-opportunity-report.md` in this skill means that file. If a workflow exists, orient them ("You finished Step [N] ([name]) — next is Step [N+1]"; infer no step from an `in-production` node with no Requirements, which Analyze recorded as already running) and route to that skill. Run Analyze only for *new* opportunities.

## Output

Write `framework/ai-opportunity-report.md` (merges and renames: *Resuming and picking up*). If the environment can't keep files between conversations, tell the user to save the report and re-supply it for Deconstruct, or continue in this conversation. In order:

### Report Header

| | |
|---|---|
| **Name** | [User's name if known, otherwise omit row] |
| **Role** | [Role and domain] |
| **Date** | [YYYY-MM-DD] |
| **Lens** | Individual / Organizational / Individual + Organizational |
| **Opportunities identified** | [count] |
| **History** | Checked / Declined / Nothing to read |
| **Not looked at yet** | [Processes not walked, if any, each that still holds a workflow from this run marked "(holds [N] workflow(s))"; omit the row otherwise] |

### Summary Table

| # | Opportunity | Process | Value lever | Size |
|---|------------|---------|-------------|------|
| 1 | [Name] | [Process] | Streamline / Automate / Accelerate / Create value | [In the student's own numbers, "Not sized yet", or "Already runs"] |

Never rank: no top recommendation, priority order, or impact rating. Size is a fact about the work, kept for Deconstruct's build choice.

### Detailed Opportunity Cards

Group cards under a `#### [Process]` heading per Process, in registry order (others last), numbered straight through as in the Summary Table.

For each opportunity:

---

**[#] [Opportunity Name]**

**Why it's a good candidate:**
[What characteristics make this well-suited for AI — repetitive, pattern-based, language-heavy, clear inputs/outputs, etc.]

**Current pain point:**
[What's slow, error-prone, inconsistent, or draining about how this is done today]

**How AI helps:**
[What AI takes as input and what it produces — the work, never the mechanism]

**Value lever:** Streamline | Automate | Accelerate | Create value — [one sentence on why this lever]

**Size:** [In the student's own numbers — "about 3 hours per proposal", "1,700+ on two waitlists", "4 calls a month; better calls mean more proposals accepted". If they gave none: "Not sized yet — Deconstruct asks for today's number." Work that already runs: "Already runs with [skill or agent]", then what could be better, if anything.]

**What changes for the business:**
[The outcome in plain language — who gets what, sooner, cheaper, or for the first time. No tool, connector, or product name.]

**Systems involved today:** [Only if the user named one — the systems the work touches now. Omit the row otherwise.]

**Business Objective:** [Organizational lens only — which strategic objective this workflow supports]
**Stakeholders:** [Organizational lens only — roles/teams involved (process owner + participants)]
**Success Metrics:** [Organizational lens only — KPIs for measuring improvement]

---

### Workflow Candidate Summary

Appended after the catalog confirmation under `## Workflow Candidate Summary`, in the report's order and numbering, per candidate kept:

| Field | Content |
|-------|---------|
| **Workflow** | 2-4 word noun phrase, Title Case |
| **Process** | The Process it is filed under |
| **Description** | One sentence describing what this workflow does |
| **Trigger** | What kicks off this workflow — an event, schedule, or request |
| **Deliverable** | The tangible output — what gets produced, sent, or decided |
| **Value lever** | Streamline / Automate / Accelerate / Create value |
| **Pain point** | What's slow, error-prone, or manual today |
| **AI opportunity** | Specific description of what AI would do |
| **Frequency** | Daily / Weekly / Monthly / Ad-hoc |
| **Size** | In the student's own numbers ("about 3 hours per proposal"), "Not sized yet", or "Already runs with [skill or agent]" |
| **Lens** | Individual / Organizational |
| **Business Objective** | (Organizational only) Which strategic objective this workflow supports |
| **Stakeholders** | (Organizational only) Roles/teams involved |
| **Success Metrics** | (Organizational only) KPIs for measuring improvement |

### Appendix: Value Lever Definitions

**Value lever — what kind of value does AI create here?** One per opportunity, the dominant one.

- **Streamline** — the work still happens the same way, with fewer steps, handoffs, or reformatting. Test: would the person still do it, just faster and cleaner?
- **Automate** — work a person does today runs without them. Test: does a person stop doing something they do now?
- **Accelerate** — the outcome arrives sooner, or more of it arrives in the same time. Test: is the gain measured in cycle time or throughput rather than effort?
- **Create value** — something becomes possible that was not done at all before. Test: is there no "today" version of this work to compare against?

When two levers apply, pick the one the user would use to justify the work to their manager or to themselves.

## Guidelines

- **Stay strategic.** Name the work, the pain, the value lever, and the deliverable; never a tool, connector, integration, agent count, model, or platform, nor a script, API, or mechanism. Systems the user uses today ("three Jira boards") may appear only in *Current pain point* and *Systems involved today* (never in the other card fields, the Candidate Summary's *Description*, *AI opportunity*, and *Pain point*, or the stub's `description`); never introduce one the user didn't name. Asked "could this run through Slack?", or whether it should run on its own, or how much the AI should decide: say once that Design (Step 3) settles that, then return to the work. A product name in a recommendation: restate it as the outcome.
- Ask one question at a time — never present a wall of questions.
- Be specific: "AI could draft the weekly status email from the three boards you already update" beats "AI could help with reporting"
- **Scope:** one trigger-to-deliverable flow per candidate; Individual lens: one owner's (note cross-team dependencies on the card); Organizational: across roles, naming the process owner and participating roles.
- **Never pick a workflow to build first.** No "start with", "build first", "natural second build", or step count; Deconstruct teaches how to choose.

**The close.** Say exactly this, in this order — what was completed, what's next, the rest as optional:

> You now have [N] workflows in your registry's backlog, grouped under the processes they belong to. Your opportunity report has the full detail for each one: `framework/ai-opportunity-report.md`. You can see the workflows on your dashboard too.
>
> **Next: Step 2, Deconstruct.** You'll choose one workflow from your backlog, and we'll map it step by step. That takes about 45 to 60 minutes. To start, say "run the deconstruct skill" (in Claude Code, you can also type `/deconstruct` and pick it from the list).
>
> **Later, if you want:** you looked at [k] of your [P] processes. Say "run the analyze skill" any time to pick up the rest. The **individual lens** looks at the work you personally do each day, such as your inbox, prep and admin, and can find different workflows. Say "run the analyze skill with the individual lens."

Fit it to the run:
- [N] is this run's backlog workflows; with others already there, "[N] new workflows in your registry's backlog ([total] in all)" ([total]: every `status: backlog` node). Running work adds " and [M] that already run, recorded as running" after "[N] workflows in your registry's backlog". [k] counts the processes looked at on this lens, across runs.
- Drop the "you looked at" sentences when every process was looked at, or there are no Process nodes; the lens sentences when both lenses are done, or personal-life; the paragraph when both go. After the Individual lens, the lens sentences name the **organizational lens**: "looks at the processes across the business, end to end, and can find different workflows. Say 'run the analyze skill with the organizational lens.'"
- No registry: "in your report" for "in your registry's backlog", "from your report" for "from your backlog", "grouped under the areas of work they belong to" for "grouped under the processes they belong to"; no dashboard sentence.
- No dashboard file: drop the dashboard sentence, unless the maintenance pass updated a dashboard Claude Artifact ("Your dashboard's Claude page now shows them too."); a dashboard file plus an updated **Claude Artifact**: "Your dashboard, and its Claude page, now show them too."
- Print-and-save mode: first list every printed file with its location (the report, each workflow entry, each edited process, `registry/workflows/index.md`, `REGISTRY.md`), then open with "Once you've saved those files, you'll have [N] workflows in your registry's backlog" in place of the first clause.
- Never name `REGISTRY.md` or any file but the report.

**Saving a version** — only when `git rev-parse --show-toplevel` returns the workspace folder (never on the web or a connected drive). After the close, once, say exactly: "Your folder keeps a history of its changes (it's a Git repository). Want me to save this point in that history, so you can come back to it later? It stays on your computer — nothing is shared." On yes, commit locally; never push as part of this offer.
