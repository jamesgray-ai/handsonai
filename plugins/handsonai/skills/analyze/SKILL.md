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

Analyze concrete opportunities where AI can improve your workflows. Produces an opportunity report with a summary table, detailed opportunity cards grouped by process, and a structured workflow candidate list, and registers every candidate as a backlog Workflow node in the AI Registry (work the student already runs with a skill or agent goes in as in production). Analyze catalogs: it names each workflow and describes it well. It never ranks the workflows or picks one to build first; that choice is made at the start of Deconstruct.

## Workflow

**Set expectations up front (first message).** Skip this when resuming (an existing `framework/analyze-in-progress.md`, which comes first) or picking up the rest. Otherwise say exactly this, as two short paragraphs:

> "This step finds opportunities to create more value with AI in your business: friction to remove, and work you'd do more of, or do better, if you had the time. Each one becomes a **candidate workflow**: a specific, repeatable piece of work worth building with AI. I'll look through what your AI already knows about your work, if you allow it, then walk the processes in your registry with you. By the end you'll have every candidate saved to your registry's **backlog** (your list of workflows to build), with an opportunity report alongside (work that already runs is recorded as running). It runs in three parts: (1) how we'll look at your work, (2) where the opportunities are, and (3) your backlog and your report. Each process takes about 3 to 5 minutes, and you can do one or all of them. Step 2, Deconstruct, takes one workflow you choose from the backlog and maps it in detail. Stopping early is safe. Progress is saved."
>
> "I'll explain each question as I ask it, and 'not sure' is always a fine answer. If you've done this before, say 'skip the explanations'."

**Words that fit the workspace.** These swaps apply to every quoted line in this skill, including approved wording, and to every heading, label, and column name in the report:
- **No registry:** "ask about your work" for "walk the processes in your registry with you"; "every candidate listed in an opportunity report" for "every candidate saved to your registry's backlog (your list of workflows to build), with an opportunity report alongside (work that already runs is recorded as running)"; "It takes about 15 minutes" for "Each process takes about 3 to 5 minutes, and you can do one or all of them"; "your list of workflows" for "your backlog" and "the backlog" everywhere else (the opening's part 3, the Part 3 signpost, the transition line; the close has its own swaps below); "your report" for "your registry". "area of work" for "process" everywhere (the "**Area of work:**" label, the Summary Table column, the Candidate Summary field, the report summary line), using the areas the student named, in their words; if they named none, ask once which area each workflow belongs to before the transition list. Drop every mention of owners and the dashboard. In the catalog, say "Here's your list of workflows." in place of "Here's what goes into your registry.", and a left-out workflow's card is marked "Left out of your list of workflows".
- **No history to read** (no saved memory, no way to search past chats, and not Claude Code): start the opening's third sentence at "I'll walk…" (no registry: "I'll ask…"), and skip the history pass.
- **Personal-life registry** (the founding `registry/log.md` entry says so): "routine" for "process", "area" for "line of business", "household" (or "your life" for one person) for "business", "role" for "function"; the no-process question's parenthetical becomes "(the person in your household who handles that kind of work)", and its *Example* is dropped. The lens is always Individual: skip the lens question and confirm it in one line ("This registry is about your own life, so we'll look at the routines you run each day."). Drop the close's lens sentences, and add no other-lens note to the report.

On the fast path, use no signposts, and say only (no registry: "I'll list the workflows you name as **candidate workflows** in a report, in about 5 minutes. Step 2, Deconstruct, takes one you choose and maps it in detail.", then the no-registry line below): "I'll register the workflows you name as **candidate workflows** in your registry's **backlog** (your list of workflows to build), with a report, in about 5 minutes. Step 2, Deconstruct, takes one you choose and maps it in detail." After "skip the explanations", drop the *Example* and *Not sure?* lines; the *Why* lines stay.

**Never show the Ask: label.** It marks the exact wording for you. The student sees only the question itself; the *Why*, *Example*, and *Not sure?* lines keep their labels.

**Signposts.** The student hears three parts, never phase numbers (no signposts on the fast path). Say one line at each, at the top of that part's first message: "**Part 1 of 3 — How we'll look at your work.**" (Phases 1–2: on the Phase 1 summary when there is one, otherwise on the first Phase 2 question — the relationship question when it's asked, else the lens question; personal-life registry with no summary (same session): the lens confirmation), "**Part 2 of 3 — Where the opportunities are.**" (Phase 3: on its intro, the first message after the lens), "**Part 3 of 3 — Your backlog and your report.**" (Phases 4–5: on the message telling the student about the report; a no-process question asked before the transition list stays in Part 2). Phase names are internal; never show them.

> **Registry entry:** the workflow's registry entry is its Workflow concept node in the workspace's `registry/` bundle — see `indexing-registry/references/registry-bundle.md` (in this plugin) for resolution, write rules, and your fields. If the workspace has no `registry/SCHEMA.md`, make the offer below once, right after the opening (a legacy `workflow.yaml` workspace: offer `scaffolding-registry`, which also migrates it); do not write registry entries until the bundle exists.

**Resume orientation:** if `framework/analyze-in-progress.md` exists, an Analyze walk was interrupted: say what was noted so far ("Last time we covered [processes]; I noted [pieces]"; with no Process nodes: "Last time we talked about [the topics covered, in plain words]; I noted [pieces]"; with nothing noted yet, just "Let's pick up where we left off."), then continue from the first step not covered — the catalog confirmation if the file says "Report written; list not confirmed yet", the history pass if the file says "History: not checked yet"; if it says "still to confirm", the next item on that list; the process pick if none is picked, otherwise, for a process marked "in progress", "Want to pick up [process] where we left off?", else the "Want to look at another process?" question with the processes still not looked at (with no Process nodes: continue from the first discovery question not covered), with no opening and no lens question. Otherwise, if the user says "continue my workflow" (or similar), they're returning mid-journey — check `registry/workflows/` for existing Workflow nodes, and `framework/` for their artifacts. If `outputs/` holds a framework record from before 9.0, follow *Moving a pre-9.0 record out of outputs/* in the indexing-registry skill's registry-bundle reference first. If the student kept the pre-9.0 layout (`registry/log.md` has a "Kept the pre-9.0 `outputs/` layout" entry), an existing workflow's artifacts are in `outputs/[workflow-name]/`, not `framework/[workflow-name]/`, and while `outputs/ai-opportunity-report.md` exists, `framework/ai-opportunity-report.md` in this skill means that file. If one exists, orient them ("You finished Step [N] ([name]) — next is Step [N+1]"; an `in-production` node with no Requirements was recorded by Analyze as already running, so infer no step from it) and route to that skill instead of starting a new analysis. Run Analyze only for finding *new* opportunities.

### Fast Path

Only when the user explicitly says they don't want discovery ("I already know the three workflows, just register them"). A workflow the user merely mentions, or one already in the registry, is a **seed** for discovery, not a reason to skip it. On the fast path, infer the lens from what they describe and confirm it in one line, exactly:

**Ask:** "These sound like [your own work / work across the business], so I'll use the **[individual / organizational] lens**: [the work you personally do each day / the processes across the business, end to end]. Right?"

Then go straight to Phase 4 and Phase 5. With a registry, read the Business node's `## Objectives` and the Process nodes first, and place each workflow under the Process whose description fits it (ask when none does). With no registry, group them by area of work, asking once which area each belongs to if the student named none. Facts about the work (trigger, deliverable, pain point, size, systems, objective, stakeholders, metrics) come only from what the student said or the registry (a registry objective the work plainly serves counts); the header's **Role** row comes from the same, and is omitted with neither; mark a missing one "Not clear yet — Deconstruct settles it", and the size "Not sized yet" unless given. The value lever, why it's a good candidate, and how AI helps are your classification, written as usual. On the fast path, the report has no **Not looked at yet** row and the close no "you looked at" sentences.

### Standard Path

Work through these steps in order:

#### Phase 1 — Read what's known

Before asking any questions, read what you already have — in this order:

1. **The registry bundle**, if `registry/SCHEMA.md` exists: the Business node, Lines of Business, Functions, Processes (with their owners), and any existing Workflow nodes (backlog or otherwise). This is the richest description of the user's work available and was written minutes or days ago — never make the user repeat it. The organizational lens maps directly onto the Process nodes.
2. This conversation and any files the student has shared in it: role, recurring tasks, pain points, goals. Saved memory and past chats are read only in the history pass (Phase 3), after the student says yes.

Disregard the roster of tools, connectors, and MCP servers available in this session, except to tell whether saved memory or past-chat search exists, and which skills the student set up. Which tools exist is a Design and Build concern; reading them here biases discovery toward whatever happens to be connected.

If the Business node has a `## Objectives` block, read it: those are the outcomes every later question ties back to.

**Same-session skip (distinct from the Fast Path above, which is the user declining discovery).** If the `scaffolding-registry` skill ran earlier in this same conversation, do not re-summarize or re-confirm — say one line ("I'll use the registry we just built") and go to Phase 2. The test is "ran in this conversation" only: a registry written yesterday, or by someone else, still gets the short summary and confirmation below, because the user may not have seen it.

Present a short summary so the user can confirm or correct it: "Your registry says you run [business] with [LOBs], working toward [objectives, if present]; the processes you named are [grouped by line of business — X, Y under A; Z under B], and you have [N] workflows — [N] in the backlog, [N] under development, [N] in production, [N] retired (omit zero counts; drop the workflows clause when there are none). Here's what else I know about your work: …" Drop the "what else I know" clause when there is nothing beyond the registry. Then, exactly:

**Ask:** "Is anything here wrong or missing?"
- *Why:* Analyze only looks inside the processes listed here, so a missing one means missed workflows.

Skip every discovery question in Phase 3 that this summary already answers. If there is no registry and no prior context, say so and go to Phase 2.

#### Phase 2 — Lens selection

If the student named a lens ("run the analyze skill with the individual lens"), use it and confirm in one line; skip the question block. Otherwise infer the lens, then recommend it with the question block below. Never ask the student to choose cold.

**Inference rule.** The registry usually makes it obvious — read the founding entry in `registry/log.md` (the scaffold records who the registry is for: a business they own, a company or unit they lead, their role inside an organization, or their personal life) and the Business node's identity sentence and Lines of Business: a company or business unit the user owns or leads → Organizational; a team or department the user works inside → Individual (their part of the team's processes); a household or a person's own life areas → Individual. Without a registry, infer from Phase 1's context. If nothing says how the user relates to the business, ask this first, then recommend:

**Ask:** "Your registry describes [business name]. Is it your company, or do you work inside it?" (No registry: "Is the work we're looking at your own business's, or do you work inside an organization?")

Say exactly this (Organizational recommended):

**Ask:** "I'd look at this from the business's point of view: the processes that drive your goals, end to end. That's the **organizational lens**. Does that fit, or would you rather start with the work you personally do each day, the **individual lens**?"
- *Why:* the lens decides which work we look at — processes across the business, or your own tasks — so the candidates match what you want to improve.
- *Example:* a clinic owner might pick organizational to fix patient booking across the front desk; a sales manager might pick individual to cut their own weekly reporting.
- *Not sure?* Keep my suggestion. You can run the other lens afterwards.

When Individual is recommended, swap the two: "I'd look at this from your point of view: the work you personally do each day. That's the **individual lens**. Does that fit, or would you rather look at the processes across the business, end to end, the **organizational lens**?" The *Why*, *Example*, and *Not sure?* lines are the same. If the student works in the field an *Example* comes from, skip that *Example* and go straight to *Not sure?*. The other lens comes up again in the close, not here.

#### Phase 3 — Where the opportunities are

**The Part 2 intro (one message, after the lens).** Say exactly this, then the history question (or, with no history to read, the walk):

> "We're looking for opportunities to create more value: friction to remove, like work that's slow, repetitive, or inconsistent, and things you'd do more of, or do better, if you had the time. Each one becomes a candidate workflow. First I'll check what your AI already knows about your work; then we'll walk your processes for anything it missed."

Drop the last sentence when the history question won't be asked (no history to read, or picking up the rest). With no Process nodes, say "then I'll ask about your work" in place of "then we'll walk your processes".

**History pass (before the walk).** Skip it when there is no history to read. Don't use saved memory for anything, including the Phase 1 summary, until the student says yes, even when it is already in this conversation. With no Process nodes, ask the individual bank's Q1 (role) first, whichever lens, and use the answer as the filter below. Then ask, exactly (drop "and your past chats" when the platform can't search them, and "your saved memory and" when there is none; in Claude Code, say "your memory files and the requests you've typed into Claude Code on this computer, across all your projects" in place of "your saved memory and your past chats", dropping "your memory files and" when none exist):

**Ask:** "I can look through what your AI already knows about your work: your saved memory and your past chats. I'll summarize patterns, not quote anything. Want me to?"
- *Why:* if you've asked your AI for help with the same work before, your history shows candidates you'd otherwise have to remember.
- *Not sure?* Say no, and we'll go straight to your processes.

On no, go to the walk. On yes, read only these, asking in plain words, never by a tool's name:
- **Saved memory** the platform gives you, and **past chats** where the platform can search them on request: search for work asked about more than once, things drafted regularly, skills or agents the student set up, and each process name.
- **In Claude Code:** the memory files (the workspace's and the user's `CLAUDE.md`, and this project's `~/.claude/projects/<project>/memory/MEMORY.md`) and the prompts the student typed, in `~/.claude/history.jsonl`. Never open that file directly: it can hold pasted content. Extract only `display`, `project`, and `timestamp`, newest first, with a filter command (`jq -r '[.timestamp,.project,.display]|@tsv' ~/.claude/history.jsonl | sort -rn | head -1000` if `jq` is installed, else the same in a one-line `python3 -c`), keeping the last 90 days or about 1,000 entries. First tell the student in one plain line that the app will ask them to approve reading it. That file covers every project on this computer, so keep only work that fits this registry. Never read session transcripts (the `.jsonl` files under `~/.claude/projects/`): they hold file contents and command output.

Keep work that fits the business the registry describes (no registry: the work the student described; a personal-life registry: the areas in the registry). Leave out one-off questions, and personal topics (a personal-life registry: anything outside its areas), without listing them; also leave out work already in the registry, matched by what the work is, not only its name, and name it on one line ("[Workflow] is already in your registry"); when that node is in the backlog but the history shows a skill or agent runs it, ask the already-runs questions below and move it to `in-production` (on that line, and the catalog's, "[Workflow] is already in your registry, now recorded as running"; it counts in the close's [M]) with its `# Skills` / `# Agents` entry. Repetition is evidence, not a requirement: show anything that looks like an opportunity, including work that already runs with a skill or agent. No cap. If nothing fits, say "I didn't find anything in your history that fits [business]." (no registry: "that fits the work you described") and go to the walk.

Show what you found in one message, under a "**Process:** [name]" label per process that fits (no registry: no labels until the student names areas), numbered straight through, each as a short name plus its evidence in one clause ("you've asked for help with this about 6 times since August", "you have a skill that drafts these"). End with "I left out one-off questions and anything outside [business]." (no registry: "anything outside the work you described"; personal-life registry: "anything outside the areas in your registry"). Then:

**Ask:** "Which of these are worth keeping? For each, say keep, drop, or 'already handled'. You can answer by number, for example 'keep 1 and 3, drop 2'."
- *Why:* only what you keep goes into your backlog, so you decide what counts.
- *Not sure?* Keep anything you'd be glad to stop doing by hand. You can drop it later.

For each kept item, draft its problem and size from the evidence and ask the student to confirm or correct it, one item per message:

**Ask:** "[Name]: [the evidence, in one clause, such as 'you've asked for help with this about 6 times since August' or 'your memory says you write these every week']. My guess: [size], and [problem]. Is that right?"
- *Why:* that tells us roughly what it's worth to fix, and it goes in your report.
- *Not sure?* Say what's right, and I'll mark the rest "not clear yet".

This is the one place you propose a problem before the student names it, because the guess rests on their own history. Record only what the student confirms or says instead.

Work that already runs ("already handled", or kept when the evidence shows a skill or agent runs it) gets no size guess. When the evidence shows no skill or agent, ask first, **Ask:** "Does a skill or agent you set up do that?" (on no, drop it). Then, in its own message:

**Ask:** "Does it work well, or could it be better?"
- *Why:* if it could be better, your report says what to improve.

When the evidence doesn't name it, follow with **Ask:** "What's it called, and where does it live?" (*Not sure?* I'll write "a skill in your [platform] account".) before writing its `# Skills` / `# Agents` entry or its card. It is registered as already running (Phase 5).

**The walk — whenever `registry/processes/` has nodes, on either lens.** The Processes are the agenda; the question banks below supply the probes. The walk covers what the history pass missed: don't re-ask a piece already kept. The registry lists the processes in value-chain order — the Business node's `# Lines of Business` list, then each line's `# Processes` list — set when the registry was drafted; it is not a ranking, and there is no rank field. The Business Objective row is written on the Organizational lens only; on the Individual lens the objective shapes the walk's goal clause and nothing more. Tie each answer back to the objective it threatens (the Business node's `## Objectives`, if present); when none of the stated objectives fits, the card's Business Objective reads "None of the stated objectives — protects [what it protects]". If the Business node has no `## Objectives` block at all, write "No stated objectives — protects [what it protects]" and do not ask the organizational bank's Q1 to fill the gap: the walk is the agenda, and objectives belong to the registry interview. The lens sets the framing, not whether the walk happens: on the Organizational lens the question is about the process end to end; on the Individual lens it is "your part of this process." Use the registry's own words: for a personal registry, 'routine' and 'area'; otherwise 'process' and 'line of business'. Skip any Process the user says is fine.

**Which process first.** Show the processes numbered straight through, one per line, under a "**Line of business:** [name]" label for each line, after exactly this (when the history pass showed the student anything, open it with "Now let's walk your processes for anything your history missed."):

> "You don't need to do all [N] today. Pick one process to start; each takes about 3 to 5 minutes. After each one you can keep going or stop, and your progress is saved. If a process runs fine, say so and we'll skip it."

**Ask:** "Which process do you want to start with? Give me the number."
- *Why:* starting where it matters most means your most useful candidates come first, even if you stop early.
- *Not sure?* I'd start with [the processes that serve the student's objectives], because they drive [the objective]. (With no objectives: the one where the work feels slowest or most repetitive.)

Name each process as you start it, with its goal ("[Process] (goal: [the objective it serves])"; drop the goal clause when the process serves none of the stated objectives, or there are none). After each process's close line, ask, **Ask:** "Want to look at another process? Give me its number, or say 'stop here for now'." (relist the processes not looked at yet, with their original numbers) Walk only what the student picks; there is no time limit. Processes not walked are listed in a **Not looked at yet** row of the report header (a process created during this run is never listed there). The transition signal fires when the student stops or every process is done.

**The walk question, once per process.** Anchor it in the most recent real run of that process, named in the student's words with its real start and end. Ask it open: never list likely pain points from the student's own business before they answer (a student echoes the list, and the report then holds your guesses, not their friction). Guesses come only as step 3 of the thin-answer recipe below, or from the history pass. Say exactly this on the first process; on later processes the **Ask:** and *Why* lines, with its anchor:

**Ask:** "Take the last time [process] ran, from [its start] to [its end]. Where did the time go, or where did it get stuck?" (Individual lens, except a personal-life registry: "Take the last time you did your part of [process], from [its start] to [its end]. Where did the time go, or where did it get stuck?")
- *Why:* the places where time or results are lost, or where doing more would pay off, are where a workflow is worth building.
- *Example:* a property manager might say: "Turning over a unit. I chase three contractors by phone, then re-enter the dates in two calendars."
- *Not sure?* Tell me the one part you'd hand to someone else tomorrow if you could.

When the answer is all about lost time, ask once per process:

**Ask:** "If that took no time at all, what would you do with it, or do more of?"
- *Why:* some of the best opportunities are work you'd do more of, not just work you'd do faster.

A new piece it names is an opportunity like any other.

**Pieces of work.** When the answer names more than one piece of work, play them back as separate pieces ("That's three pieces of work: launch emails, waitlist follow-up, and promotion across channels."). Take first the pieces the student named a problem with, or wanted more of. If the rest were named only as steps, ask once:

**Ask:** "Of the other [N], which ones slow you down or could be better, or would you do more of with the time? We'll skip any that run fine."
- *Why:* a step that runs fine isn't worth building, so we only keep the ones with a problem or a payoff.

A piece becomes an opportunity only when the student names a problem with it, or value in doing more of it.

**Depth rule — stay strategic.** An opportunity is complete when you can name the work, the problem, roughly how often or how much (its size), and the goal it serves. Stop on it as soon as it is complete. Ask at most one follow-up per opportunity, and only to fill a missing element, usually the size. Ask one thing per message; when it isn't clear what a piece is, ask about the last real time it happened ("Think of the last proposal you sent. What did you do after it went out?"). Inputs, rules, steps, and edge cases are Deconstruct's job; never ask about them here. When the size is missing, say exactly this on the first piece; afterwards the **Ask:** and *Why* lines:

**Ask:** "Roughly how much time does [the piece of work] take you in a typical week or month?"
- *Why:* that tells us roughly what it's worth to fix, and it goes in your report.
- *Example:* an accounts clerk might say: "About four hours at every month end."
- *Not sure?* A rough guess is fine. If you'd rather not guess, I'll mark it "not sized yet", and Deconstruct asks for today's number when you map it.

When the problem is quality, or work not being done at all, time undersells it: ask how often instead ("Roughly how many [scoping calls] do you have in a typical month?", same *Why*), and record the size as the count plus what it affects ("4 calls a month; better calls mean more proposals accepted").

When an opportunity has a clear starting point and a clear result, say so in one clause in the student's own case ("Repurposing has a clean starting point, a finished issue, and a clear result, LinkedIn and Substack posts, so it's a strong candidate").

**Close each process in one line** before moving on, naming everything noted from it: "Noted for [process]: [piece 1], [piece 2], [piece 3]. That's enough for the report. Deconstruct goes into the detail later."

**Save progress** (this is what makes the opening's "Progress is saved" true) to `framework/analyze-in-progress.md`: once the lens is settled, after the history pass, after the process pick, each time an opportunity is complete, and after each process (with no Process nodes: also after the role answer). The student sees this file being written, so write it in plain words they could read: the lens; the run ("Run: new", "Run: picking up the rest", or "Run: other lens ([lens])"); the history pass ("History: not checked yet", "History: checked; still to confirm: […]" after the keep-or-drop answer, each item with its name, process, evidence clause and drafted guess, and each "already handled" answer awaiting the already-runs questions, "History: checked; kept …", "History: skipped"); work that already runs as "already runs with [name], [where it lives]; works well" or "could be better: [what]"; the processes in the order picked, each marked "looked at", "in progress", "runs fine", or "not looked at yet"; and for each process or area of work its noted pieces with whatever you have of work, problem, size, and goal. With no Process nodes, also save the student's role and domain and the discovery questions already covered. After writing the report, save "Report written; list not confirmed yet". Say nothing about it to the student. Delete it once the Workflow nodes are written (no registry: once the catalog is confirmed). In print-and-save mode, skip this file.

**Fallback — no Process nodes.** Use the question bank for the chosen lens, exactly as below.

> **Ask one question at a time — these banks are a scaffold for you, not a list to paste at the user.** Adapt to their answers, skip anything the history pass already covered, and follow up for concrete examples. (Restated after the banks too — but apply it from the first question.)

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

**Adaptive ordering:** With a registry, the Processes set the order and the banks supply the probes. Without one, start with the areas where Phase 1 revealed the least. Skip areas the history pass already covered — no need to re-ask what you already know. A registry's Business and Process nodes usually answer Q1 and Q2 already — confirm rather than re-ask.

Probe for concrete examples: "I spend 30 minutes every Monday formatting a status report from three Jira boards" is far more useful than "I do reporting."

**Thin answers.** When an answer is too vague to name the work or the problem:
1. Play back what you have: "So far I have: [their words]."
2. Ask one narrower follow-up anchored in a real instance: "Think of the last time you did this. What happened first?"
3. If it's still thin after two tries, propose a guess to react to. Say: "Here's my guess: [X], [Y], or [Z], from what you've told me about [your role / this process]. What's right and what's wrong?"
4. If they still don't know, move on: leave the process under **Not looked at yet**, or record the size as "Not sized yet". Never invent an opportunity and record it as theirs.

**Transition signal:** When the student stops or every process is done (with no Process nodes: once the role is answered and there are 3+ concrete opportunities), and after settling any piece that belongs to none of the registry's processes (*A workflow with no process*, Phase 5; it then appears under its new process marked "(new)"), list the opportunities numbered straight through under a "**Process:** [name]" label for each process, in registry order (no registry: the order the student named them; the report and catalog use the same order and numbers; on an other-lens run, number only this run's pieces 1 to N, as the catalog does), marking work that already runs "(already runs)" after its name. On every run, leave pieces that match an existing workflow (by what the work is, not only its name) out of the numbered list and name them on one line ("[Workflow] is already in your registry", adding ", now recorded as running" for one the history pass moved). Then, exactly:

**Ask:** "Anything to add? If not, I'll add these to your registry's backlog, and write up a short opportunity report alongside. You'll see exactly how they'll look in your registry before anything goes into it."
- *Why:* anything you add now goes into the same catalog you'll check next.

With work that already runs in the list, say "add these to your registry" in place of "add these to your registry's backlog". With no registry, say: "Anything to add? If not, I'll write up your opportunity report with all of these. You'll check the list before it's final."

#### Phase 4 — Opportunity report

**Self-check before writing each opportunity:** confirm it has a **concrete trigger** (what kicks it off) and a **tangible deliverable** (what gets produced). If either is fuzzy and the opportunity's one follow-up is unused, ask it (never on the fast path); otherwise write what you have and mark the fuzzy field "Not clear yet — Deconstruct settles it". Never drop an opportunity the student named.

**Before writing the report** (fast path), settle any workflow that fits no process, using *A workflow with no process* in Phase 5, so every card has its group. On a walk this is settled earlier, before the transition list.

**Work that already runs.** On its card and in the Candidate Summary, *Pain point* reads "None stated — runs well" or the improvement the student named, and *How AI helps* describes what the skill or agent does today. Never invent either.

**Telling the student about the report.** After writing it, say in a few lines: how many opportunities, grouped under how many processes, where the file is saved (print-and-save mode: where to save it), and what each card holds (the problem, what AI would do, its size). Define the value lever the first time it appears, exactly: "Each card names its **value lever**: the kind of value AI creates here — Streamline, Automate, Accelerate, or Create value." Never present a ranking, a top pick, or an impact rating.

#### Phase 5 — Candidates registered

Every candidate goes into the backlog, except work that already runs, which is registered as running. There is no cap and no "which do you want to build?" question: Analyze catalogs the work, and which workflow to build first is chosen at the start of Deconstruct.

**A workflow with no process (registry present).** With no registry, skip this: candidates stay grouped by area of work. Before the transition list on a walk, or before the report is written on the fast path, check every candidate has a Process. Where none fits (common on the Individual lens), teach the term and ask, once per new process, exactly:

**Ask:** "[Workflow] doesn't fit any of your processes. What would you call the set of related work it belongs to, and which function (the team or role that owns that kind of work) looks after it? Your functions are [the registry's Function names]."
- *Why:* every workflow sits under one process, and the process's owner owns the workflow too.
- *Example:* a bookkeeper might say: "Client Onboarding, and Client Services looks after it."
- *Not sure?* I'll suggest a name from your own words and the function in your registry that fits it best. You can change either later.

When the answer is a person, or a function not in the registry, match it to the registry Function that fits and say which in one line ("I'll put it under [Function]."); if none fits, ask once, **Ask:** "Shall I add [function] as a new function?", and on yes write a complete Function node per `registry/SCHEMA.md` (title, description, one sentence of charter prose, an empty GENERATED `# Owns` block), with its line in `registry/functions/index.md`. Never write an `owner:` that matches no Function file. Write a complete minimal Process node per `naming-workflows`' rule — never a default, never an ownerless stub — and add its line to the right Line of Business's `# Processes` list and to `registry/processes/index.md` (ask which line, and where in the order, if it is not obvious). The owning Function's `# Owns` block is GENERATED; the maintenance pass refreshes it. In the catalog, show the new process with "(new)" after its name.

**Catalog confirmation (one message).** This is the student's one look at the catalog before it is written. Place each candidate under the Process where it was found, unless the work clearly belongs elsewhere (it happens before that Process starts, or another Process's owner does it); then place it under the right one and give the reason in brackets after its description. Show every process that has workflows, with its workflows, in the report's process order and numbers, numbered straight through across processes (on an other-lens run, number only this run's workflows 1 to N; the merged report keeps its own numbering), each as name plus a one-sentence description of about 20 words in the form "When/From [trigger], [what it produces]", with "(already runs)" after the name of work that already runs. No size, value lever, or ranking on this screen. With no registry, the workspace swaps above apply: open with "Here's your list of workflows.", drop the owner sentence, and the *Why* is "the name and description are what Deconstruct starts from later." Say exactly this, with the student's own workflows:

> Here's what goes into your registry. Each workflow sits under the process it belongs to and is owned by that process's owner.
>
> **Process:** [Process]
> 1. **[Workflow name].** [One-sentence description.]
> 2. …

**Ask:** "Anything to rename, reword, move or leave out? You can answer by number, for example 'rename 4.'" (With fewer than four workflows on screen, use the highest number shown.)
- *Why:* the name and description are what you'll see on your dashboard, and what Deconstruct starts from later.
- *Not sure?* Say "looks good." You can edit any workflow later.

Apply every change to the report (cards, Summary Table). A workflow the student leaves out keeps its card in the report, marked "Left out of the backlog", and gets no registry entry.

Then append a **Workflow Candidate Summary** to the report with structured metadata for each candidate kept (not left out):

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
| **Size** | In the student's own numbers ("about 3 hours per proposal"), or "Not sized yet" |
| **Lens** | Individual / Organizational |
| **Business Objective** | (Organizational only) Which strategic objective this workflow supports |
| **Stakeholders** | (Organizational only) Roles/teams involved |
| **Success Metrics** | (Organizational only) KPIs for measuring improvement |

Append it under a `## Workflow Candidate Summary` heading, in the same process order and numbering as the report.

**Register the candidates (registry present).** If `registry/SCHEMA.md` exists, write each candidate as a backlog Workflow node so the registry becomes the student's candidate list. Work that already runs gets the same node with `status: in-production` in place of `backlog`, and its skill or agent under `# Skills` or `# Agents`: a link to the file when it is in this workspace, otherwise its name and where it lives as plain text ("Newsletter Repurposer, a skill in your Claude account"). It is never put in the backlog.

1. **Process placement** is the one confirmed above.
2. **Write the stub** at `registry/workflows/<slug>.md` (slug = kebab-case of the Workflow name), in the `naming-workflows` stub format:

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

   The body's opening paragraph deliberately repeats the frontmatter `description`: the frontmatter is what tools read, the body is what people read. `trigger` is provisional — Deconstruct refines it. The stub carries no `execution_mode` or `autonomy`: those are Design's to set once the steps are known. Pain point, size, and value lever stay in the report; the registry holds the inventory.
3. Add each stub's line to its Process's `# Workflows` list and to `registry/workflows/index.md`, replacing any placeholder line there (`_No workflows captured yet._`, `_No entries yet…_`) (bundle-root-relative link: `[Weekly Status Report](/workflows/weekly-status-report.md)`). If a node for that slug, or for the same work under another name, already exists, merge — never overwrite fields already set, except the backlog-to-`in-production` move the history pass confirmed.

**No registry.** Right after the opening, say once: "You don't have a registry yet, so your workflows will live in the report for now. When you want them saved and shown on a dashboard, say 'run the scaffolding-registry skill'." Then continue; don't repeat it here.

**The other lens.** The other lens is offered in the close as a later session; never ask about it as a question. Add a one-line note under the report header that the other lens hasn't been run yet (never for a personal-life registry) (keep the header's **Lens** row naming the lens used). When the student runs the other lens, now or in a later session, run Phases 2–5 on that lens (in a later session, run Phase 1 first: read the registry and the existing report and give the short summary) and merge the new candidates into the report and the registry; the catalog confirmation shows only this run's workflows, numbered straight through. When a piece of work matches a workflow already in the registry, say so ("[Workflow] is already in your registry; I'll add what we learned to its card"), update its existing card, and leave it out of the catalog numbering and the close's [N]. Update the header's **Opportunities identified** to the combined count and **Not looked at yet** to the processes neither run walked. Then run the maintenance pass and the close; when both lenses are now done, the close's lens sentences are dropped and no other-lens note is added.

**Picking up the rest.** When there is no `framework/analyze-in-progress.md`, the student runs Analyze again, the report's header has a **Not looked at yet** row (an older report's **Noted, not walked** row counts; rename it on merge), and the student hasn't named a lens other than the report's, run Phase 1, then offer to continue in place of the opening and the lens question, **Ask:** "Last time you looked at [processes]. Want to pick up with the rest?" On yes, use the report's lens (when it names both, ask which), skip the history pass, go to the process pick with only the processes not looked at yet, and merge the new candidates into the report and the registry as for the other lens (same catalog numbering, header updates, and matching rule). On no, run a fresh analysis.

## Output

Write the report to `framework/ai-opportunity-report.md`. Create the `framework/` directory if it doesn't exist. If the file already exists and this run is the other lens (now, in a later session, or resumed with "Run: other lens"), merge into it: add the new cards under their processes, extend the Summary Table and the Workflow Candidate Summary, set the header's **Lens** to "Individual + Organizational", and remove the other-lens note. On any merge, an older report's **Noted, not walked** row becomes **Not looked at yet**. When picking up the rest (including a resumed "Run: picking up the rest"), merge the same way, leaving the **Lens** row and the other-lens note unchanged. Otherwise (a fresh analysis on the same lens), rename the existing file to `ai-opportunity-report-YYYY-MM-DD.md` (using today's date) before writing the new one.

If this environment can't keep files between conversations (no persistent workspace — output is produced as a download), tell the user to save the report and re-supply it when they run the Deconstruct step, or continue in this same conversation.

The report must include (in this order):

### Report Header

| | |
|---|---|
| **Name** | [User's name if known, otherwise omit row] |
| **Role** | [Role and domain] |
| **Date** | [YYYY-MM-DD] |
| **Lens** | Individual / Organizational / Individual + Organizational |
| **Opportunities identified** | [count] |
| **Not looked at yet** | [Processes not walked, if any, each that still holds a workflow from this run marked "(holds [N] workflow(s))"; omit the row otherwise] |

### Summary Table

| # | Opportunity | Process | Value lever | Size |
|---|------------|---------|-------------|------|
| 1 | [Name] | [Process] | Streamline / Automate / Accelerate / Create value | [In the student's own numbers, "Not sized yet", or "Already runs"] |

The report never ranks: no top recommendation, no priority order, no impact rating. Size is a fact about the work in the student's own numbers, kept for the build choice in Deconstruct.

### Detailed Opportunity Cards

Group cards by Process, in registry order (the Business node's `# Lines of Business` list, then each line's `# Processes` list; processes outside the registry last), under a `#### [Process]` heading per group. Number the cards straight through in the order they appear, and use the same order and numbers in the Summary Table.

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

(Appended after the catalog confirmation — see Phase 5 format above)

### Appendix: Value Lever Definitions

Use these definitions when choosing each opportunity's value lever:

**Value lever — what kind of value does AI create here?** One per opportunity, the dominant one.

- **Streamline** — the work still happens the same way, with fewer steps, handoffs, or reformatting. Test: would the person still do it, just faster and cleaner?
- **Automate** — work a person does today runs without them. Test: does a person stop doing something they do now?
- **Accelerate** — the outcome arrives sooner, or more of it arrives in the same time. Test: is the gain measured in cycle time or throughput rather than effort?
- **Create value** — something becomes possible that was not done at all before. Test: is there no "today" version of this work to compare against?

When two levers apply, pick the one the user would use to justify the work to their manager or to themselves.

## Guidelines

- **Stay at the strategic level.** Analyze names the work, the pain, the value lever, and the deliverable. It never names a tool, connector, integration, agent count, model, or platform, and never proposes a script, API, or automation mechanism. The systems the user uses today are facts about the work and may appear in *Current pain point* and *Systems involved today* ("three Jira boards"); they never appear in *Why it's a good candidate*, *How AI helps*, *Value lever*, or *What changes for the business*, and Analyze never introduces a system the user did not name. The same rule covers the Workflow Candidate Summary's *Description*, *AI opportunity*, and *Pain point* fields and the stub's `description` — that text is what Deconstruct reads first. If the user asks "could this run through Slack?", say once that Design (Step 3) chooses the mechanism and return to the work. Likewise if the user asks whether it should run on its own or with them in the loop, or how much the AI should decide: say once that Design (Step 3) settles how much the AI decides and who takes part, once the steps are known, and return to the work. If you notice yourself writing a product name in a recommendation, stop and restate it as the outcome.
- Ask one question at a time — never present a wall of questions.
- Be specific in recommendations: "AI could draft the weekly status email from the three boards you already update" beats "AI could help with reporting"
- **Individual lens:** Scope each workflow candidate to one person's trigger-to-deliverable flow. If a workflow spans multiple people, note the cross-team dependencies in the opportunity card but keep the candidate focused on a single owner's scope.
- **Organizational lens:** Scope each workflow candidate to one trigger-to-deliverable flow, even if it spans multiple roles. Identify the process owner (accountable for the end-to-end outcome) and list participating roles.
- **Never pick a workflow to build first.** No "start with", "build first", "natural second build", or step count in Analyze; the student chooses at the start of Deconstruct, which teaches how to choose.
- After the catalog confirmation, append the Workflow Candidate Summary, write the backlog nodes (see Phase 5), and add the other-lens note to the report (unless both lenses are now done, or the registry is personal-life). Then, if `registry/SCHEMA.md` exists, invoke the `indexing-registry` skill for a maintenance pass (best-effort — a failed refresh never fails this step), then deliver the close below.

**The close.** Say exactly this, in this order — what was completed, what's next, the other lens as optional:

> You now have [N] workflows in your registry's backlog, grouped under the processes they belong to. Your opportunity report has the full detail for each one: `framework/ai-opportunity-report.md`. You can see the workflows on your dashboard too.
>
> **Next: Step 2, Deconstruct.** You'll choose one workflow from your backlog, and we'll map it step by step. That takes about 45 to 60 minutes. To start, say "run the deconstruct skill" (in Claude Code, you can also type `/deconstruct` and pick it from the list).
>
> **Later, if you want:** you looked at [k] of your [P] processes. Say "run the analyze skill" any time to pick up the rest. The **individual lens** looks at the work you personally do each day, such as your inbox, prep and admin, and can find different workflows. Say "run the analyze skill with the individual lens."

Fit it to the run: [k] counts every process looked at, in any run; drop the "you looked at" sentences when every process was looked at, or there are no Process nodes; drop the lens sentences when both lenses are now done, or the registry is personal-life; drop the paragraph when both go. With work that already runs, add " and [M] that already run, recorded as running" after "[N] workflows in your registry's backlog". In print-and-save mode, first list every file printed in this step with its location (the report, each new workflow entry, each edited process, `registry/workflows/index.md`, and `REGISTRY.md`), then open the close with "Once you've saved those files, you'll have [N] workflows in your registry's backlog" in place of its first clause. [N] is the backlog workflows registered in this run; if the backlog already held others, say "[N] new workflows in your registry's backlog ([total] in all)", where [total] is every `status: backlog` Workflow node after this run. With no registry, say "in your report" in place of "in your registry's backlog", "from your report" in place of "from your backlog", and "grouped under the areas of work they belong to" in place of "grouped under the processes they belong to", and drop the dashboard sentence; with no dashboard file, drop the dashboard sentence, unless the maintenance pass updated a dashboard Claude Artifact, then say "Your dashboard's Claude page now shows them too."; when there is a dashboard file and the maintenance pass also updated a dashboard **Claude Artifact**, say "Your dashboard, and its Claude page, now show them too." in place of the dashboard sentence. After the Individual lens, the lens sentences name the **organizational lens** instead: "looks at the processes across the business, end to end, and can find different workflows. Say 'run the analyze skill with the organizational lens.'" Never name `REGISTRY.md` or any file but the report.

**Saving a version — only when the folder is a git repository** (in write mode with a shell, `git rev-parse --show-toplevel` returns the workspace folder; never on the web or in a connected drive). After the close, once, say exactly: "Your folder keeps a history of its changes (it's a Git repository). Want me to save this point in that history, so you can come back to it later? It stays on your computer — nothing is shared." On yes, commit locally; never push as part of this offer.
