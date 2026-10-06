---
name: analyze
description: >
  This skill should be used when the user wants to analyze AI workflow opportunities,
  run a workflow audit, find automation candidates, or says "where can AI help".
  Scans memory and conversation history, interviews the user about their work,
  then produces a prioritized opportunity report with structured workflow
  candidates and registers the chosen candidates as backlog Workflow nodes in the AI Registry,
  ready for the Deconstruct step. This is Step 1 of the AI Workflow Framework.
  It stays strategic: it names the work, the pain, and the value, never the tools or integrations.
---

# Analyze Workflows

Analyze concrete opportunities where AI can improve your workflows. Produces a categorized opportunity report with a summary table, detailed opportunity cards, and a structured workflow candidate list, and registers the chosen candidates as backlog Workflow nodes in the AI Registry.

## Workflow

**Set expectations up front (first message).** Say: "This is a guided interview of about 15–20 minutes. By the end you'll have up to five candidate workflows registered in your backlog, and one I'll recommend building first. Stopping early is safe — everything is saved and you can pick up later."

> **Registry entry:** the workflow's registry entry is its Workflow concept node in the workspace's `registry/` bundle — see `indexing-registry/references/registry-bundle.md` (in this plugin) for resolution, write rules, and your fields. If the workspace has no `registry/SCHEMA.md`, offer the `scaffolding-registry` skill first (it also migrates legacy `workflow.yaml` workspaces); do not write registry entries until the bundle exists.

**Resume orientation:** if the user says "continue my workflow" (or similar), they're returning mid-journey — check `registry/workflows/` for existing Workflow nodes, and `outputs/` for their artifacts. If one exists, orient them ("You finished Step [N] ([name]) — next is Step [N+1]") and route to that skill instead of starting a new analysis. Run Analyze only for finding *new* opportunities.

### Fast Path

Only when the user explicitly says they don't want discovery ("I already know the three workflows, just register them"). A workflow the user merely mentions, or one already in the registry, is a **seed** for discovery, not a reason to skip it. On the fast path, infer the lens from what they describe, confirm it, and go straight to Phase 4 and Phase 5; even on the fast path, read the bundle's Process nodes before registering anything.

### Standard Path

Work through these steps in order:

#### Phase 1 — Read what's known

Before asking any questions, read what you already have — in this order:

1. **The registry bundle**, if `registry/SCHEMA.md` exists: the Business node, Lines of Business, Functions, Processes (with their owners), and any existing Workflow nodes (backlog or otherwise). This is the richest description of the user's work available and was written minutes or days ago — never make the user repeat it. The organizational lens maps directly onto the Process nodes.
2. Conversation history, memory, project files, and any other available context: role, recurring tasks, pain points, tools, goals.

Disregard the roster of tools, connectors, and MCP servers available in this session. Which tools exist is a Design and Build concern; reading them here biases discovery toward whatever happens to be connected.

If the Business node has a `## Objectives` block, read it: those are the outcomes every later question ties back to.

**Same-session skip (distinct from the Fast Path above, which is the user declining discovery).** If the `scaffolding-registry` skill ran earlier in this same conversation, do not re-summarize or re-confirm — say one line ("I'll use the registry we just built") and go to Phase 2. The test is "ran in this conversation" only: a registry written yesterday, or by someone else, still gets the short summary and confirmation below, because the user may not have seen it.

Present a short summary so the user can confirm or correct it: "Your registry says you run [business] with [LOBs], working toward [objectives, if present]; the processes you named are [grouped by line of business — X, Y under A; Z under B], and [N] workflows are already in the backlog. Here's what else I know about your work: … Anything wrong or missing?" Drop the "what else I know" clause when there is nothing beyond the registry. Skip every discovery question in Phase 3 that this summary already answers. If there is no registry and no prior context, say so and move directly to Phase 3.

#### Phase 2 — Lens selection

After presenting the memory scan summary (or noting no prior context), ask the user which lens to use:

> **Individual lens** — Workflows you personally perform in your role (reporting, email triage, content creation, etc.)
>
> **Organizational lens** — Workflows critical to delivering on your business outcomes — your value chain, cross-functional processes, and strategic operations (customer onboarding, sales pipeline, product delivery, etc.)
>
> Which lens should we start with?

**Inference rule:** If user context makes the answer obvious, infer and confirm rather than asking. The registry usually makes it obvious — read the founding entry in `registry/log.md` (the scaffold records who the registry is for: a business they own, a company or unit they lead, their role inside an organization, or their personal life) and the Business node's identity sentence and Lines of Business: a company or business unit the user owns or leads → Organizational; a team or department the user works inside → Individual (their part of the team's processes); a household or a person's own life areas → Individual. Say it in one sentence: "Your registry describes [a household / a consultancy you own / the data platform team], so the [lens] lens fits best — sound right?" If neither the log nor the identity sentence says how the user relates to the business, fold the question into that sentence ("Is this your company, or do you work inside it?"). The other lens is offered in Phase 6, not here.

#### Phase 3 — Discovery interview

Based on gaps in your understanding (or starting from scratch), ask focused questions to build a complete picture. Use the question set for the user's chosen lens.

**Process walk — the primary mode whenever `registry/processes/` has nodes, on either lens.** The Processes are the agenda; the question banks below supply the probes. Walk the Processes in Line of Business order, highest-ranked first. For each one, ask about friction and business challenge, one question at a time: what is slow, what is inconsistent between people, where do handoffs stall, what breaks at higher volume, what gets measured and what does not. Tie each answer back to the objective it threatens (the Business node's `## Objectives`, if present). The lens sets the framing, not whether the walk happens: on the Organizational lens the question is about the process end to end; on the Individual lens it is "your part of this process." Skip any Process the user says is fine.

**Time bound.** The walk must fit the 15–20 minutes promised. If the registry holds more than six Processes, open by asking the user to pick the four or five that matter most right now, and list the rest in the report header as "noted, not walked." Stop once three or more concrete opportunities exist and the transition signal below fires; the user can always ask to continue.

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

Ask these questions **one at a time** — not as a list. Use the user's answers to ask smart follow-up questions. Probe for concrete examples: "I spend 30 minutes every Monday formatting a status report from three Jira boards" is far more useful than "I do reporting."

**Handling vague answers:** If the user gives vague responses after 2-3 probes on a topic, move on. If answers are vague across all areas, shift to hypothesis mode. For the individual lens: "Based on your role, I'd guess you spend time on X — is that right?" For the organizational lens: "For a [size] [industry] company, the value chain processes that typically benefit most from AI are X, Y, Z — do any of those resonate?"

**Transition signal:** When you've identified 3+ concrete opportunities, tell the user: "I've identified [N] opportunities so far. I have enough to put together the report — do you want to add anything else, or should I go ahead?" Let them add more or confirm before proceeding.

Continue until you can identify at least 3 concrete opportunities — typically 5-10 questions, fewer if the memory scan provided strong context.

#### Phase 4 — Opportunity report

Once you can identify at least 3 concrete, specific opportunities with enough detail to fill the card format below, produce the structured report.

**Two scales you'll classify each opportunity on (plain-language — full definitions in the Appendix):**
- **Autonomy** = how much the AI decides on its own — look at **what decides the next step**: **Deterministic** (you give instructions; the AI carries out every step, and its output never changes what happens next, even when it writes or analyzes inside a step) → **Guided** (you give bounded decisions with your method — the AI uses your rubric, criteria, or process to route an item, choose a tool, or judge quality and send work back) → **Autonomous** (you give a goal; the AI plans its own steps and keeps going until the goal is met). An opportunity where the AI drafts inside set steps and the workflow pauses for a person's review before it goes out is Deterministic + Augmented; if the draft is delivered and reviewed only after the run, it's Deterministic + Automated. Use the tests in the Appendix for every opportunity.
- **Involvement** = does a person take part while it runs: **Augmented** (a person is in the workflow along the way, guiding, engaging, or collaborating with the AI) vs. **Automated** (no one takes part until it's done — starting it by hand doesn't change that).

**Self-check before writing each opportunity:** confirm it has a **concrete trigger** (what kicks it off) and a **tangible deliverable** (what gets produced). If either is fuzzy, ask one more question or drop the opportunity — a candidate without a clear trigger + deliverable will stall in Deconstruct (Step 2).

#### Phase 5 — Candidates registered

After presenting the full report, ask the user to pick their top workflow candidates — the ones they want to build. Once they've chosen, produce a **Workflow Candidate Summary** with structured metadata for each candidate:

For each candidate:

| Field | Content |
|-------|---------|
| **Workflow** | 2-4 word noun phrase, Title Case |
| **Description** | One sentence describing what this workflow does |
| **Trigger** | What kicks off this workflow — an event, schedule, or request |
| **Deliverable** | The tangible output — what gets produced, sent, or decided |
| **Autonomy** | Deterministic / Guided / Autonomous |
| **Involvement** | Augmented / Automated |
| **Value lever** | Streamline / Automate / Accelerate / Create value |
| **Pain point** | What's slow, error-prone, or manual today |
| **AI opportunity** | Specific description of what AI would do |
| **Frequency** | Daily / Weekly / Monthly / Ad-hoc |
| **Priority** | High / Medium / Low |
| **Reasoning** | Why this priority level — based on impact, frequency, and feasibility |
| **Lens** | Individual / Organizational |
| **Business Objective** | (Organizational only) Which strategic objective this workflow supports |
| **Stakeholders** | (Organizational only) Roles/teams involved |
| **Success Metrics** | (Organizational only) KPIs for measuring improvement |

Append this summary to the output file under a `## Workflow Candidate Summary` heading. Recommend which candidate to deconstruct first, with reasoning.

**First-workflow scope guardrail.** If this is the user's first workflow with the framework (no prior workflow folders in `outputs/` and no registry Workflow nodes beyond `status: backlog` ones, or they say so), recommend a **starter-sized** candidate for round one: roughly 3–5 steps, touches at most one external system, triggered manually. Say why: "Your highest-impact opportunity is usually also your most complex — build a small one first to learn the full loop, then take on [big candidate] second. It stays on your list." Impact ranking still stands; this only affects which one to *build first*. If the user insists on starting big, proceed — their call.

**Register the candidates (registry present).** If `registry/SCHEMA.md` exists, write each chosen candidate as a backlog Workflow node so the registry becomes the student's candidate list:

1. **Process placement, one confirmation for all candidates.** A candidate found while walking a Process is already placed under it — confirm placement only for candidates that surfaced outside the walk. For those, propose which existing Process each belongs to: "I'd file *Weekly Status Report* under *Client Delivery* and *Inbox Triage* under *Operations* — right?" Where no existing Process fits (common on the Individual lens), ask the user to name one and which function owns it, then write a complete minimal Process node per `naming-workflows`' rule — never a default, never an ownerless stub.
2. **Write the stub** at `registry/workflows/<slug>.md` (slug = kebab-case of the Workflow name), in the `naming-workflows` stub format:

   ```yaml
   ---
   type: Workflow
   title: "[Workflow name]"
   description: "[Description sentence]. [Deliverable folded in as the outcome sentence.]"
   generated: { by: process:analyze, at: YYYY-MM-DD }
   status: backlog
   trigger: "[Trigger field]"
   execution_mode: augmented
   ---
   # [Workflow name]

   [Description.] [Deliverable sentence.]

   # Artifacts

   - [Opportunity report](outputs/ai-opportunity-report.md)

   # Skills

   # Agents

   # Insights

   <!-- GENERATED:insights -->
   <!-- /GENERATED -->
   ```

   `execution_mode` is `augmented` for an Augmented workflow and `automated` for an Automated one (`manual` means not yet run by AI); write the value only — no comment in the file.

   `trigger` and `execution_mode` are provisional — Deconstruct and Design refine them. Priority, pain point, and the "build first" recommendation stay in the report; the registry holds the inventory.
3. Add each stub's line to its Process's `# Workflows` list and to `registry/workflows/index.md` (bundle-root-relative link: `[Weekly Status Report](/workflows/weekly-status-report.md)`). If a node for that slug already exists, merge — never overwrite fields already set.

No registry? Say so once ("No registry here, so the candidates live in the report only — set one up with the `scaffolding-registry` skill when you want an inventory" — unless you already said this at the start) and continue.

#### Phase 6 — The other lens

After completing the report and candidate selection for the first lens, offer it as a later session, not a continuation: "We've registered [N] candidates from the [lens] perspective. The [other] lens — [one-line description] — usually surfaces different ones; it's worth a separate 15-minute session when you're ready. Want me to note that in the report?" If the user wants it now, run it.

If the user asks to run the second lens now, run its discovery questions and merge the new candidates into the report and the registry.
If they only want it noted, add it to the report (a Lens row plus a one-line note that the other lens is pending) and move on.
If they decline both, proceed to the next framework step.

## Output

Write the report to `outputs/ai-opportunity-report.md`. Create the `outputs/` directory if it doesn't exist. If the file already exists, rename the existing file to `ai-opportunity-report-YYYY-MM-DD.md` (using today's date) before writing the new one.

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
| **Top recommendation** | [#1 priority opportunity + one-sentence reason] |

### Summary Table

| # | Opportunity | Autonomy | Involvement | Value lever | Impact |
|---|------------|----------|-------------|-------------|--------|
| 1 | [Name] | Deterministic / Guided / Autonomous | Augmented / Automated | Streamline / Automate / Accelerate / Create value | High / Medium / Low |

### Top Recommendations

List the top 3 opportunities in priority order with a one-sentence rationale for each.

### Detailed Opportunity Cards

Group cards by autonomy level (Deterministic → Guided → Autonomous). Within each group, order from highest to lowest impact.

For each opportunity:

---

**[#] [Opportunity Name]**

**Autonomy:** Deterministic | Guided | Autonomous
**Involvement:** Augmented | Automated

**Why it's a good candidate:**
[What characteristics make this well-suited for AI — repetitive, pattern-based, language-heavy, clear inputs/outputs, etc.]

**Current pain point:**
[What's slow, error-prone, inconsistent, or draining about how this is done today]

**How AI helps:**
[What AI takes as input and what it produces — the work, never the mechanism]

**Value lever:** Streamline | Automate | Accelerate | Create value — [one sentence on why this lever]

**What changes for the business:**
[The outcome in plain language — who gets what, sooner, cheaper, or for the first time. No tool, connector, or product name.]

**Systems involved today:** [Only if the user named one — the systems the work touches now. Omit the row otherwise.]

**Business Objective:** [Organizational lens only — which strategic objective this workflow supports]
**Stakeholders:** [Organizational lens only — roles/teams involved (process owner + participants)]
**Success Metrics:** [Organizational lens only — KPIs for measuring improvement]

---

### Workflow Candidate Summary

(Appended after user selects candidates — see Phase 5 format above)

### Appendix: Classification Definitions

Use these definitions when classifying opportunities:

**Autonomy — How much does the AI decide on its own? Look at what decides the next step.**

- **Deterministic** — you give instructions. You set every step, and the AI carries each one out. It may write or summarize inside a step, but its output never changes what happens next. Test: does the work follow the same path whatever the AI produces? Examples: formatting reports, drafting a weekly status report from fixed sources, drafting feedback against a rubric for a person to review (the rubric shapes what it writes; it doesn't decide what happens next).
- **Guided** — you give bounded decisions, with your method. You set the structure and the methodology (a rubric, criteria, a process); the AI uses it to make decisions on your behalf: route an item, choose a tool, judge quality and send work back. Its decisions are bounded (within your structure, by your rules), not open-ended. Test: does the AI's judgment, made by your rules, decide what happens next? Examples: sorting support emails by category and routing each to the right queue (escalating unclear ones), scoring insights 1–10 against a rubric and drafting only those that score 7 or higher, an agent that grades drafts against your criteria and sends failures back to be fixed, a browser assistant that judges prospects against a persona and works out how to navigate the site.
- **Autonomous** — you give a goal. The AI plans its own steps, decides what to do next at each turn, and keeps going until the goal is met. Its decision-making is open-ended. Test: could you only describe the goal, not the steps? Examples: research agents that decide what to investigate and write an article, a monitoring agent that decides where to dig when something changes.

Two notes: **writing or summarizing inside a step never makes a workflow Guided**, and **the number of agents doesn't set the level**. The level is the highest any AI step reaches. Whether a person should check the output is the involvement question, never a reason to raise autonomy. A branch on a value the AI didn't judge — an API's score, a timer, a field value — is still an instruction: Deterministic. A person approving the AI's decisions doesn't lower the level: if the AI proposes selections by your method and you approve them, it's Guided + Augmented.

**Human Involvement — Does a person take part while it runs?**

- **Augmented**: A person is in the workflow along the way, guiding, engaging, or collaborating with the AI while it runs.
- **Automated**: No one takes part until it's done. Starting a run by hand doesn't make it Augmented.

**Value lever — what kind of value does AI create here?** One per opportunity, the dominant one.

- **Streamline** — the work still happens the same way, with fewer steps, handoffs, or reformatting. Test: would the person still do it, just faster and cleaner?
- **Automate** — work a person does today runs without them. Test: does a person stop doing something they do now?
- **Accelerate** — the outcome arrives sooner, or more of it arrives in the same time. Test: is the gain measured in cycle time or throughput rather than effort?
- **Create value** — something becomes possible that was not done at all before. Test: is there no "today" version of this work to compare against?

When two levers apply, pick the one the user would use to justify the work to their manager or to themselves.

## Guidelines

- **Stay at the strategic level.** Analyze names the work, the pain, the value lever, and the deliverable. It never names a tool, connector, integration, agent count, model, or platform, and never proposes a script, API, or automation mechanism. The systems the user uses today are facts about the work and may appear in *Current pain point* and *Systems involved today* ("three Jira boards"); they never appear in *Why it's a good candidate*, *How AI helps*, *Value lever*, or *What changes for the business*, and Analyze never introduces a system the user did not name. If the user asks "could this run through Slack?", say once that Design (Step 3) chooses the mechanism and return to the work. If you notice yourself writing a product name in a recommendation, stop and restate it as the outcome.
- Ask one question at a time — never present a wall of questions
- Use a conversational flow — let answers guide follow-up questions naturally
- Push for concrete examples over vague descriptions
- Be specific in recommendations: "AI could draft the weekly status email from your Jira board data" beats "AI could help with reporting"
- **Individual lens:** Scope each workflow candidate to one person's trigger-to-deliverable flow. If a workflow spans multiple people, note the cross-team dependencies in the opportunity card but keep the candidate focused on a single owner's scope.
- **Organizational lens:** Scope each workflow candidate to one trigger-to-deliverable flow, even if it spans multiple roles. Identify the process owner (accountable for the end-to-end outcome) and list participating roles.
- After writing the report, ask the user to pick their candidates for Phase 5. Once they've chosen, append the Workflow Candidate Summary, write the backlog nodes (see Phase 5), and tell the user: "Report saved to `outputs/ai-opportunity-report.md` and [N] candidates registered in your backlog. Start with *[recommended]*: say 'run the deconstruct skill' — about 45–60 minutes, and it turns the candidate into requirements."
- After writing the report and the backlog nodes, invoke the `indexing-registry` skill for a maintenance pass (best-effort — a failed refresh never fails this step), then deliver the closing message above.
- **Signpost each phase transition.** Announce each phase in one short line as you reach it ("Phase 3 of 6 — the discovery interview") so the user always knows where they are.
