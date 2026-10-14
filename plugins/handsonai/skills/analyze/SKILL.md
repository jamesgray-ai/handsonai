---
name: analyze
description: >
  This skill should be used when the user wants to analyze AI workflow opportunities,
  run a workflow audit, find automation candidates, or says "where can AI help".
  Scans memory and conversation history, interviews the user about their work,
  then produces an opportunity report with structured workflow candidates and
  registers every candidate as a backlog Workflow node in the AI Registry,
  ready for the Deconstruct step. This is Step 1 of the AI Workflow Framework.
  It stays strategic: it names the work, the pain, and the value, never the tools or integrations.
---

# Analyze Workflows

Analyze concrete opportunities where AI can improve your workflows. Produces an opportunity report with a summary table, detailed opportunity cards grouped by process, and a structured workflow candidate list, and registers every candidate as a backlog Workflow node in the AI Registry. Analyze catalogs: it names each workflow and describes it well. It never ranks the workflows or picks one to build first; that choice is made at the start of Deconstruct.

## Workflow

**Set expectations up front (first message).** Say exactly this, as two short paragraphs:

> "This step finds where AI can help in your business. I'll walk the processes in your registry, ask where the work is slow, repetitive, or inconsistent, and turn each spot into a **candidate workflow**: a specific, repeatable piece of work worth building with AI. By the end you'll have an opportunity report and every candidate saved to your registry's **backlog** (your list of workflows to build). It takes about 15 to 20 minutes, in three parts: (1) how we'll look at your work, (2) where the time goes, and (3) your report and your backlog. Step 2, Deconstruct, takes one workflow you choose from the backlog and maps it in detail. Stopping early is safe. Progress is saved."
>
> "I'll explain each question as I ask it, and 'not sure' is always a fine answer. If you've done this before, say 'skip the explanations'."

**Words that fit the workspace.** These swaps apply to every quoted line in this skill, including approved wording:
- **No registry:** "ask about your work" for "walk the processes in your registry"; "an opportunity report listing every candidate" for "an opportunity report and every candidate saved to your registry's backlog (your list of workflows to build)"; "your list of workflows" for "your backlog" and "the backlog" everywhere else (the opening's part 3, the Part 3 signpost, the transition line; the close has its own swaps below); "your report" for "your registry". Group workflows by the areas of work the student named, in their words, and label them "**Area of work:**" in place of "**Process:**". Drop every mention of owners and the dashboard.
- **Personal-life registry** (the founding `registry/log.md` entry says so): "routine" for "process", "area" for "line of business", "household" (or "your life" for one person) for "business", "role" for "function". The lens is always Individual: skip the lens question and confirm it in one line ("This registry is about your own life, so we'll look at the routines you run each day."). Drop the close's other-lens paragraph, and add no other-lens note to the report.

On the fast path, use no signposts, and say only (no registry: "I'll list the workflows you name as **candidate workflows** in a report, in about 5 minutes. Step 2, Deconstruct, takes one you choose and maps it in detail."): "I'll register the workflows you name as **candidate workflows** in your registry's **backlog** (your list of workflows to build), with a report, in about 5 minutes. Step 2, Deconstruct, takes one you choose and maps it in detail." After "skip the explanations", drop the *Example* and *Not sure?* lines; the *Why* lines stay.

**Signposts.** The student hears three parts, never phase numbers (no signposts on the fast path). Say one line at each: "**Part 1 of 3 — How we'll look at your work.**" (Phases 1–2), "**Part 2 of 3 — Where the time goes.**" (Phase 3), "**Part 3 of 3 — Your report and your backlog.**" (Phases 4–5). Phase names are internal; never show them.

> **Registry entry:** the workflow's registry entry is its Workflow concept node in the workspace's `registry/` bundle — see `indexing-registry/references/registry-bundle.md` (in this plugin) for resolution, write rules, and your fields. If the workspace has no `registry/SCHEMA.md`, make the offer below once, right after the opening (a legacy `workflow.yaml` workspace: offer `scaffolding-registry`, which also migrates it); do not write registry entries until the bundle exists.

**Resume orientation:** if the user says "continue my workflow" (or similar), they're returning mid-journey — check `registry/workflows/` for existing Workflow nodes, and `framework/` for their artifacts. If `outputs/` holds a framework record from before 9.0, follow *Moving a pre-9.0 record out of outputs/* in the indexing-registry skill's registry-bundle reference first. If the student kept the pre-9.0 layout (`registry/log.md` has a "Kept the pre-9.0 `outputs/` layout" entry), an existing workflow's artifacts are in `outputs/[workflow-name]/`, not `framework/[workflow-name]/`, and while `outputs/ai-opportunity-report.md` exists, `framework/ai-opportunity-report.md` in this skill means that file. If one exists, orient them ("You finished Step [N] ([name]) — next is Step [N+1]") and route to that skill instead of starting a new analysis. Run Analyze only for finding *new* opportunities.

### Fast Path

Only when the user explicitly says they don't want discovery ("I already know the three workflows, just register them"). A workflow the user merely mentions, or one already in the registry, is a **seed** for discovery, not a reason to skip it. On the fast path, infer the lens from what they describe and confirm it in one line, exactly:

**Ask:** "These sound like [your own work / work across the business], so I'll use the **[individual / organizational] lens**: [the work you personally do each day / the processes across the business, end to end]. Right?"

Then go straight to Phase 4 and Phase 5, placing each workflow under the Process whose description fits it (ask when none does); even on the fast path, read the bundle's Process nodes before registering anything.

### Standard Path

Work through these steps in order:

#### Phase 1 — Read what's known

Before asking any questions, read what you already have — in this order:

1. **The registry bundle**, if `registry/SCHEMA.md` exists: the Business node, Lines of Business, Functions, Processes (with their owners), and any existing Workflow nodes (backlog or otherwise). This is the richest description of the user's work available and was written minutes or days ago — never make the user repeat it. The organizational lens maps directly onto the Process nodes.
2. Conversation history, memory, project files, and any other available context: role, recurring tasks, pain points, tools, goals.

Disregard the roster of tools, connectors, and MCP servers available in this session. Which tools exist is a Design and Build concern; reading them here biases discovery toward whatever happens to be connected.

If the Business node has a `## Objectives` block, read it: those are the outcomes every later question ties back to.

**Same-session skip (distinct from the Fast Path above, which is the user declining discovery).** If the `scaffolding-registry` skill ran earlier in this same conversation, do not re-summarize or re-confirm — say one line ("I'll use the registry we just built") and go to Phase 2. The test is "ran in this conversation" only: a registry written yesterday, or by someone else, still gets the short summary and confirmation below, because the user may not have seen it.

Present a short summary so the user can confirm or correct it: "Your registry says you run [business] with [LOBs], working toward [objectives, if present]; the processes you named are [grouped by line of business — X, Y under A; Z under B], and you have [N] workflows — [N] in the backlog, [N] under development, [N] in production, [N] retired (omit zero counts). Here's what else I know about your work: … Anything wrong or missing?" Drop the "what else I know" clause when there is nothing beyond the registry. Skip every discovery question in Phase 3 that this summary already answers. If there is no registry and no prior context, say so and go to Phase 2.

#### Phase 2 — Lens selection

Infer the lens, then recommend it with the question block below. Never ask the student to choose cold.

**Inference rule.** The registry usually makes it obvious — read the founding entry in `registry/log.md` (the scaffold records who the registry is for: a business they own, a company or unit they lead, their role inside an organization, or their personal life) and the Business node's identity sentence and Lines of Business: a company or business unit the user owns or leads → Organizational; a team or department the user works inside → Individual (their part of the team's processes); a household or a person's own life areas → Individual. Without a registry, infer from Phase 1's context. If nothing says how the user relates to the business, ask this first, then recommend:

**Ask:** "Your registry describes [business name]. Is it your company, or do you work inside it?" (No registry: "Is the work we're looking at your own business's, or do you work inside an organization?")

Say exactly this (Organizational recommended):

**Ask:** "I'd look at this from the business's point of view: the processes that drive your goals, end to end. That's the **organizational lens**. Does that fit, or would you rather start with the work you personally do each day, the **individual lens**?"
- *Why:* the lens decides which work we look at — processes across the business, or your own tasks — so the candidates match what you want to improve.
- *Example:* a clinic owner might pick organizational to fix patient booking across the front desk; a sales manager might pick individual to cut their own weekly reporting.
- *Not sure?* Keep my suggestion. You can run the other lens afterwards.

When Individual is recommended, swap the two: "I'd look at this from your point of view: the work you personally do each day. That's the **individual lens**. Does that fit, or would you rather look at the processes across the business, end to end, the **organizational lens**?" The *Why*, *Example*, and *Not sure?* lines are the same. If the student works in the field an *Example* comes from, skip that *Example* and go straight to *Not sure?*. The other lens comes up again in the close, not here.

#### Phase 3 — Discovery interview

Based on gaps in your understanding (or starting from scratch), ask focused questions to build a complete picture. Use the question set for the user's chosen lens.

**Process walk — the primary mode whenever `registry/processes/` has nodes, on either lens.** The Processes are the agenda; the question banks below supply the probes. The registry lists them in value-chain order — the Business node's `# Lines of Business` list, then each line's `# Processes` list — set when the registry was drafted; it is not a ranking, and there is no rank field. Tie each answer back to the objective it threatens (the Business node's `## Objectives`, if present); when none of the stated objectives fits, the card's Business Objective reads "None of the stated objectives — protects [what it protects]". If the Business node has no `## Objectives` block at all, write "No stated objectives — protects [what it protects]" and do not ask the organizational bank's Q1 to fill the gap: the walk is the agenda, and objectives belong to the registry interview. The lens sets the framing, not whether the walk happens: on the Organizational lens the question is about the process end to end; on the Individual lens it is "your part of this process." Use the registry's own words: for a personal registry, 'routine' and 'area'; otherwise 'process' and 'line of business'. Skip any Process the user says is fine.

**Which processes first.** Registry setup never asks the student to rank processes, so always open the walk with this question (with five or fewer processes, use the second **Ask:** line below instead; it walks all of them). Show the processes numbered straight through, one per line, under a "**Line of business:** [name]" label for each line, so the student can answer by number ("3, 7, 9").

**Ask:** "Which of these processes matter most right now? Pick up to five, and I'll start with those."
- *Why:* it keeps this to 15–20 minutes and puts your time where it counts.
- *Example:* a landscaping company owner might pick "Quoting New Jobs" and "Crew Scheduling" over "Equipment Maintenance".
- *Not sure?* I'd start with [the processes that serve the student's objectives], because they drive [the objective]. (With no objectives: pick the ones where the work feels slowest or most repetitive.)

With five or fewer processes, say this instead:

**Ask:** "We'll go through all [N]. Which should we start with?"
- *Why:* starting where it hurts most puts the most time where it counts.
- *Example:* a landscaping company owner might start with "Quoting New Jobs".
- *Not sure?* I'd start with [the processes that serve the student's objectives], because they drive [the objective]. (With no objectives: start with the one where the work feels slowest or most repetitive.)

Walk them in the order the user named them, counting through them ("1 of 4: [Process] (goal: [the objective it serves])"), and list any not walked in a **Noted, not walked** row of the report header. **Time bound.** Walk every process the student picked; the depth rule below keeps each one short. If the walk passes about 20 minutes with processes left, say so and offer to stop there; the rest go under **Noted, not walked**. The transition signal fires after the last process.

**The walk question, once per process.** Anchor it in the most recent real run of that process, named in the student's words with its real start and end. Ask it open: never list likely pain points from the student's own business before they answer (a student echoes the list, and the report then holds your guesses, not their friction). Guesses come only as step 3 of the thin-answer recipe below. Say exactly this on the first process; on later processes the **Ask:** and *Why* lines, with its anchor:

**Ask:** "Take the last time [process] ran, from [its start] to [its end]. Where did the time go, or where did it get stuck?"
- *Why:* the places where time or results are lost are where a workflow is worth building.
- *Example:* a property manager might say: "Turning over a unit. I chase three contractors by phone, then re-enter the dates in two calendars."
- *Not sure?* Tell me the one part you'd hand to someone else tomorrow if you could.

**Pieces of work.** When the answer names more than one piece of work, play them back as separate pieces ("That's three pieces of work: launch emails, waitlist follow-up, and promotion across channels.") and take them in the order the student named them, saying so ("I'll take them in the order you named them."). Each piece is a possible opportunity.

**Depth rule — stay strategic.** An opportunity is complete when you can name the work, the problem, roughly how often or how much (its size), and the goal it serves. Stop on it as soon as it is complete. Ask at most one follow-up per opportunity, and only to fill a missing element, usually the size. Inputs, rules, steps, and edge cases are Deconstruct's job; never ask about them here. When the size is missing, say exactly this on the first piece; afterwards the **Ask:** and *Why* lines:

**Ask:** "Roughly how much time does [the piece of work] take you in a typical week or month?"
- *Why:* that tells us roughly what it's worth to fix, and it goes in your report.
- *Example:* an accounts clerk might say: "About four hours at every month end."
- *Not sure?* A rough guess is fine. If you'd rather not guess, I'll mark it "not sized yet", and Deconstruct asks for today's number when you map it.

When an opportunity has a clear starting point and a clear result, say so in one clause in the student's own case ("Repurposing has a clean starting point, a finished issue, and a clear result, LinkedIn and Substack posts, so it's a strong candidate").

**Close each process in one line** before moving on, naming everything noted from it: "Noted for [process]: [piece 1], [piece 2], [piece 3]. That's enough for the report. Deconstruct goes into the detail later." Then signpost the next process.

**Fallback — no Process nodes.** Use the question bank for the chosen lens, exactly as below.

> **Ask one question at a time — these banks are a scaffold for you, not a list to paste at the user.** Adapt to their answers, skip anything the memory scan already covered, and follow up for concrete examples. (Restated after the banks too — but apply it from the first question.)

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

**Adaptive ordering:** With a registry, the Processes set the order and the banks supply the probes. Without one, start with the areas where Phase 1 revealed the least. Skip areas already well-covered by the memory scan — no need to re-ask what you already know. A registry's Business and Process nodes usually answer Q1 and Q2 already — confirm rather than re-ask.

Probe for concrete examples: "I spend 30 minutes every Monday formatting a status report from three Jira boards" is far more useful than "I do reporting."

**Thin answers.** When an answer is too vague to name the work or the problem:
1. Play back what you have: "So far I have: [their words]."
2. Ask one narrower follow-up anchored in a real instance: "Think of the last time you did this. What happened first?"
3. If it's still thin after two tries, propose a guess to react to. Say: "Here's my guess: [X], [Y], or [Z], from what you've told me about [your role / this process]. What's right and what's wrong?"
4. If they still don't know, move on: note the process under **Noted, not walked**, or record the size as "Not sized yet". Never invent an opportunity and record it as theirs.

**Transition signal:** After the last process (with no Process nodes: once there are 3+ concrete opportunities), list the opportunities numbered straight through under a "**Process:** [name]" label for each process, in registry order (no registry: the order the student named them; the report and catalog use the same order and numbers), then say: "The report covers all of these, and they all go into your backlog."

**Ask:** "Anything to add, or shall I write the report?"

#### Phase 4 — Opportunity report

**Self-check before writing each opportunity:** confirm it has a **concrete trigger** (what kicks it off) and a **tangible deliverable** (what gets produced). If either is fuzzy and the opportunity's one follow-up is unused, ask it; otherwise write what you have and mark the fuzzy field "Not clear yet — Deconstruct settles it". Never drop an opportunity the student named.

**Telling the student about the report.** After writing it, say in a few lines: how many opportunities, grouped under how many processes, where the file is saved, and what each card holds (the problem, what AI would do, its size). Define the value lever the first time it appears, exactly: "Each card names its **value lever**: the kind of value AI creates here — Streamline, Automate, Accelerate, or Create value." Never present a ranking, a top pick, or an impact rating.

#### Phase 5 — Candidates registered

Every candidate goes into the backlog. There is no cap and no "which do you want to build?" question: Analyze catalogs the work, and which workflow to build first is chosen at the start of Deconstruct.

**A workflow with no process (registry present).** With no registry, skip this: candidates stay grouped by area of work. Before the catalog confirmation, check every candidate has a Process. Where none fits (common on the Individual lens), teach the term and ask, once per new process, exactly:

**Ask:** "[Workflow] doesn't fit any of your processes. What would you call the set of related work it belongs to, and which function (the team or role that owns that kind of work) looks after it?"
- *Why:* every workflow sits under one process, and the process's owner owns the workflow too.
- *Example:* a bookkeeper might say: "Client Onboarding, and that's me."
- *Not sure?* I'll suggest a name from your own words and make you the owner. You can change it later.

Write a complete minimal Process node per `naming-workflows`' rule — never a default, never an ownerless stub — and add its line to the right Line of Business's `# Processes` list (ask which line, and where in the order, if it is not obvious). The owning Function's `# Owns` block is GENERATED; the maintenance pass refreshes it. In the catalog, show the new process with "(new)" after its name.

**Catalog confirmation (one message).** This is the student's one look at the catalog before it is written. Place each candidate under the Process where it was found, unless the work clearly belongs elsewhere (it happens before that Process starts, or another Process's owner does it); then place it under the right one and give the reason in brackets after its description. Show every process with its workflows, in the report's process order and numbers, numbered straight through across processes, each as name plus a one-sentence description of about 20 words in the form "When/From [trigger], [what it produces]". No size, value lever, or ranking on this screen. With no registry, the workspace swaps above apply: open with "Here's what goes into your report.", drop the owner sentence, and the *Why* is "the name and description are what Deconstruct starts from later." Say exactly this, with the student's own workflows:

> Here's what goes into your registry. Each workflow sits under the process it belongs to and is owned by that process's owner.
>
> **[Process]**
> 1. **[Workflow name].** [One-sentence description.]
> 2. …

**Ask:** "Anything to rename, reword, move or leave out? You can answer by number, for example 'rename 4.'"
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

**Register the candidates (registry present).** If `registry/SCHEMA.md` exists, write each candidate as a backlog Workflow node so the registry becomes the student's candidate list:

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
3. Add each stub's line to its Process's `# Workflows` list and to `registry/workflows/index.md`, replacing any placeholder line there (`_No workflows captured yet._`, `_No entries yet…_`) (bundle-root-relative link: `[Weekly Status Report](/workflows/weekly-status-report.md)`). If a node for that slug already exists, merge — never overwrite fields already set.

**No registry.** Right after the opening, say once: "You don't have a registry yet, so your workflows will live in the report for now. When you want them saved and shown on a dashboard, say 'run the scaffolding-registry skill'." Then continue; don't repeat it here.

**The other lens.** The other lens is offered in the close as a later session; never ask about it as a question. Add a one-line note under the report header that the other lens hasn't been run yet (keep the header's **Lens** row naming the lens used). If the student asks to run it now, run Phases 2–5 on that lens, merge the new candidates into the report and the registry (a second catalog confirmation shows only the new ones), then run the maintenance pass and the close again; the close's last paragraph is then dropped.

## Output

Write the report to `framework/ai-opportunity-report.md`. Create the `framework/` directory if it doesn't exist. If the file already exists, rename the existing file to `ai-opportunity-report-YYYY-MM-DD.md` (using today's date) before writing the new one.

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
| **Noted, not walked** | [Processes left out of the walk, if any; omit row otherwise] |

### Summary Table

| # | Opportunity | Process | Value lever | Size |
|---|------------|---------|-------------|------|
| 1 | [Name] | [Process] | Streamline / Automate / Accelerate / Create value | [In the student's own numbers, or "Not sized yet"] |

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

**Size:** [In the student's own numbers — "about 3 hours per proposal", "1,700+ on two waitlists". If they gave none: "Not sized yet — Deconstruct asks for today's number."]

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
- After the catalog confirmation, append the Workflow Candidate Summary, write the backlog nodes (see Phase 5), and add the other-lens note to the report. Then invoke the `indexing-registry` skill for a maintenance pass (best-effort — a failed refresh never fails this step), then deliver the close below.

**The close.** Say exactly this, in this order — what was completed, what's next, the other lens as optional:

> You now have [N] workflows in your registry's backlog, grouped under the processes they belong to. Your opportunity report has the full detail for each one: `framework/ai-opportunity-report.md`. You can see the workflows on your dashboard too.
>
> **Next: Step 2, Deconstruct.** You'll choose one workflow from your backlog, and we'll map it step by step. That takes about 45 to 60 minutes. To start, say "run the deconstruct skill."
>
> **Later, if you want:** the **individual lens** looks at the work you personally do each day, such as your inbox, prep and admin, and can find different workflows. Say "run the analyze skill with the individual lens."

Fit it to the run: [N] is the workflows registered in this run; if the backlog already held others, say "[N] new workflows in your registry's backlog ([total] in all)". With no registry, say "in your report" in place of "in your registry's backlog", "from your report" in place of "from your backlog", and "grouped under the areas of work they belong to" in place of "grouped under the processes they belong to", and drop the dashboard sentence; with no dashboard file, drop the dashboard sentence; when the maintenance pass updated a dashboard **Claude Artifact**, say "Your dashboard, and its Claude page, now show them too." in place of the dashboard sentence. After the Individual lens, the last paragraph names the **organizational lens** instead: "looks at the processes across the business, end to end, and can find different workflows. Say 'run the analyze skill with the organizational lens.'" Never name `REGISTRY.md` or any file but the report.

**Saving a version — only when the folder is a git repository** (in write mode with a shell, `git rev-parse --show-toplevel` returns the workspace folder; never on the web or in a connected drive). After the close, once, say exactly: "Your folder keeps a history of its changes (it's a Git repository). Want me to save this point in that history, so you can come back to it later? It stays on your computer — nothing is shared." On yes, commit locally; never push as part of this offer.
