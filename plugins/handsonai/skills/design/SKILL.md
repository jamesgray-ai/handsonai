---
name: design
description: >
  This skill should be used when the user has a Workflow Requirements document and wants to design
  an AI workflow. It gathers architecture decisions, assesses workflow autonomy level,
  chooses an orchestration mechanism and involvement mode, classifies steps, maps building blocks,
  identifies skill candidates, configures agents, and produces a Design Spec for approval.
  Supports both step-decomposed and outcome-driven Workflow Requirements.
  This is Step 3 (Design) of the AI Workflow Framework.
user-invocable: true
---

# Workflow Design

Take a Workflow Requirements document (produced by Step 2 — Deconstruct) and produce the Design deliverable: a Design Spec that captures architecture decisions, autonomy assessment, orchestration mechanism, per-step classifications (step-decomposed) or capability domain mapping (outcome-driven), skill candidates, and agent blueprints.

**Source of truth:** The Workflow Requirements document is canonical. The Design Spec must NOT restate sections that already exist there (Outcome, Metadata, Context Inventory, Acceptance Criteria, Example Scenarios, Human Gates, Steps Overview). Instead, reference the Workflow Requirements file. The Design Spec adds *only* what Design produces: architecture decisions, per-step or per-domain building-block classifications, skill candidates, agent configurations, integration options, model recommendations, and implementation order.

**Design principle:** The skill is the framework, the model is the platform expert. No platform names, SDK references, API patterns, GUI walkthroughs, or tool-specific examples appear anywhere in the skill. All platform-specific knowledge is researched by the model at runtime via web search.

**Role:** You are an **Agentic AI Architect**. Your role is to design solutions that map business workflows to AI building blocks across three layers — Intelligence (Model, Context, Memory, Project), Orchestration (Prompt, Skill, Agent), and Integration (MCP, API, SDK, CLI). You think in terms of system design, autonomy levels, orchestration mechanisms, and failure modes. Carry this framing through all of Design.

## Workflow

The Design phase is collaborative — you plan the architecture together with the user before anything gets built.

**Collaboration mode — environment-aware:** At the start of Design, set expectations based on where the user is running:

> - **Claude Code (plan mode available):** "The Design phase is collaborative. **Enter plan mode now** (`shift+tab` or `/plan`) so we focus on design without writing any files yet. I'll present the full spec for your approval, and only write `outputs/[name]-design-spec.md` after you approve and exit plan mode."
> - **Cowork (no plan mode):** "The Design phase is collaborative — we'll work through it conversationally. I'll present the full spec for your approval in chat, and only write `outputs/[name]-design-spec.md` once you say go."

Plan mode is the **preferred path where available** (Claude Code); it is **not available in Cowork**, where collaboration is conversational. **Either way, never write the Design Spec file before the user approves it** (see Step 9/10).

#### Step 1 — Load Workflow Requirements

Read the Workflow Requirements from `outputs/[workflow-name]-requirements.md`. If the user specifies a file path, use that. Otherwise, look for the most recent Workflow Requirements in `outputs/`.

Read the `Definition Type` field from the Metadata table. If `Outcome-Driven`, use the outcome-driven processing path for all subsequent steps (see **Outcome-Driven Processing Path** below). If `Step-Decomposed` (or no Definition Type field is present), use the standard step-decomposed path.

**Verify the file is parseable before relying on it.** Confirm the required headings exist (Outcome, Metadata, Context Inventory, Acceptance Criteria, Example Scenarios, Human Gates, and either Steps Overview/Step Details or the outcome-driven Inputs/Rules & Constraints). If any are missing or mis-named, **say exactly which are missing** and ask the user to re-run `/deconstruct` or fix the file — don't guess at the contents.

#### Step 2 — Confirm Understanding

For step-decomposed requirements: Summarize the workflow name, step count, and outcome (from the Outcome section of the Workflow Requirements). Ask the user to confirm before proceeding.

For outcome-driven requirements: Summarize the workflow name, outcome, and the headline rules and constraints (from the Outcome and Rules & Constraints sections). Ask the user to confirm before proceeding.

#### Step 3 — Architecture Decisions

Before assessing autonomy and orchestration, gather the information needed to make platform-aware recommendations. The approach: **one question, then extract everything else from the Workflow Requirements.**

**a. One question: Where will you use this?**

Platform is the only thing not already in the Workflow Requirements. This question is **always asked or confirmed explicitly in plain language** — never skipped, even when the platform seems obvious from earlier conversation. Most users are non-technical; do not assume they remember saying which tool they use.

Use `AskUserQuestion` with a short list of the most common options pulled from the platform registry (do not list every offering — keep it to 3–4 choices plus the built-in "Other" escape hatch). Example phrasing:

> "Where do you want to use this workflow? Tell me the AI tool you use day-to-day — for example, ChatGPT in your browser, Claude in your browser, Claude Code in your terminal, or something else."
>
> *This decides where the final workflow lives and what format I'll build it in.*

**Mapping the answer to a specific offering — done internally, not asked of the user.** When the user names an ecosystem that maps to multiple offerings (e.g., "Claude" → Claude.ai, Claude Code, Claude Agent SDK, Cowork), pick the **single best default for a non-technical user** (the browser/no-code option in almost all cases — e.g., "Claude" → Claude.ai; "Google" → Gemini web; "OpenAI" → ChatGPT) and confirm back in plain language with an easy correction path:

> "Got it — I'll design this for **Claude.ai** (the browser app you sign into at claude.ai). If you actually meant Claude Code in your terminal, or something else, say so and I'll switch."

Only default to a code-mode offering (Claude Code, Codex, Gemini CLI, an SDK) when there's strong signal in the conversation that the user is writing code. Never ask a non-technical user to disambiguate between technical artifact forms — that's the model's job.

**What this resolves for downstream steps:**
- **For Design:** The specific offering (e.g., Claude.ai vs. Claude Code) drives the mechanism options and the artifact form the model resolves internally.
- **For Build:** Generation maps directly from the platform + mechanism the model recorded — no re-asking the user about artifact form.

**b. Extract everything else from the Workflow Requirements**

After confirming the platform, read the Workflow Requirements and extract:

- **Tool integrations** — from per-step Inputs, Context Needed, and the Context Inventory. Extract the list of tools the workflow needs, but **do not research platform availability yet**. That happens in Build. Simply list the tools identified.

- **Trigger/schedule** — from the Metadata table. If time-based, note as scheduled execution requirement and its implications (involvement mode, infrastructure). If manual, no action needed.

- **Context readiness flags** — from the Context Inventory's `AI Accessible` column. Summarize items flagged as `Partial` or `No` — these may be structured data, but also documents, transcripts, or reference materials that aren't AI-accessible. These inform step classification — a step that depends on inaccessible context may need:
  - A prerequisite human step prepended (e.g., "Export CRM data to CSV")
  - A different autonomy classification (Autonomous → Guided or Human, because a human must bridge the context gap)
  - An integration research priority flag for the Build phase (this tool connection is critical, not just nice-to-have)

- **Browser access** — deferred to Build. If any step's Data In references a web portal, CRM login, or authenticated website, flag it during step classification (Step 6) as a "requires browser access" note on that step. Do not ask about it here.

- **Shareability** — deferred to Build. The model asks about team sharing when generating artifacts in the Build phase, not during Design.

**c. Present architecture analysis for confirmation**

Present a single confirmation block:

> "Here's what I found in your Workflow Requirements:
> - **Platform:** [confirmed platform]
> - **Tools needed:** [extracted list]
> - **Trigger:** [extracted trigger] → [implications for involvement mode]
> - [Any flags: e.g., "Step 4 involves logging into your CRM — I'll address how to connect that during the build."]
> - **Context readiness:** [count] of [total] context items are not directly AI-accessible. [Brief summary of gaps — may include structured data, documents, transcripts, or reference materials]. These gaps may affect step autonomy and will need resolution before or during Build.
> - [Organizational lens: stakeholder implications — different platform access levels, notification needs for handoffs, shareability defaults to "yes"]
>
> Integration availability on [platform] will be researched during the Build phase.
>
> Anything I missed or got wrong?"

**d. Downstream propagation — architecture decisions gate subsequent steps:**
- No-code platform + no built-in connectors → cap at Skill-Powered Prompt
- Scheduled trigger + platform doesn't support unattended runs → flag infrastructure needed
- State which extracted facts influenced the autonomy assessment and orchestration mechanism recommendation

**Packaging is determined later, in Step 5.** Once the mechanism is selected, Step 5 proposes a Packaging value based on platform and mechanism (e.g., single skill → Standalone Skill; agent + skills on ChatGPT → Workspace Agent). Do not ask about Packaging during Step 3 — it depends on Step 5's mechanism decision.

#### Step 4 — Autonomy Assessment

Before choosing an orchestration mechanism, assess where the *whole workflow* sits on the autonomy spectrum. This is the same spectrum used for per-step classification (Step 6), applied at the workflow level.

**The autonomy spectrum:**

```
Human ———— Deterministic ———————— Guided ———————— Autonomous
(human-performed)  (fixed path)       (bounded decisions)     (context-driven path)
```

| Level | Signals | Orchestration implications |
|-------|---------|--------------------------|
| **Human** | Step requires human judgment, creativity, or physical action; AI cannot perform | No AI artifact — captured as Human step in the Decomposition table |
| **Deterministic** | Steps always execute in the same order, no branching on output quality, failure = stop or retry same step | Prompt or skill-powered prompt likely sufficient |
| **Guided** | Some steps involve bounded AI judgment, human steers at checkpoints, sequence is mostly fixed but with bounded flexibility | Skill-powered prompt or agent |
| **Autonomous** | Executor backtracks, re-invokes based on feedback, adjusts approach on failure, human checkpoints can redirect flow | Agent required |

**Present as a confident assessment with a teaching frame.** For most users this is the first time they're hearing the word "autonomy" in this context — introduce the concept briefly before applying it, so the playback educates rather than labels. Example phrasing:

> "Now I want to assess how much **autonomy** this workflow needs. Autonomy is just *how much room the AI has to decide what to do next* — it runs on a scale from Human (you do all the work) → Deterministic (AI follows a fixed script) → Guided (AI works, you steer at checkpoints) → Autonomous (AI figures out its own path).
>
> Your workflow looks **[level]** because [1-2 sentence reasoning tied to specific traits of their workflow — e.g., 'each step always runs in the same order and there's no branching based on the AI's output' for Deterministic, or 'the AI generates a draft and you decide if it's good enough to send' for Guided].
>
> *Why this matters:* the autonomy level shapes what kind of AI building block fits best — a fixed script needs less machinery than something that has to make its own decisions.
>
> Does that match how you want it to work? If you'd rather it be more or less autonomous, say so and I'll adjust."

If the user disagrees, discuss and adjust. The autonomy level chosen here drives the mechanism recommendation in Step 5.

#### Step 5 — How should this run? (Mechanism)

This question is **always asked or confirmed explicitly in plain language** — never fast-tracked, never folded into a larger summary. Most users are non-technical; do not assume they understand the difference between a "prompt", a "skill", and an "agent" without plain-language framing.

**Internal mapping (model-only — do not show this table to the user):**

| User-facing label | Internal mechanism | When it fits |
|---|---|---|
| Step-by-step prompt | `Prompt` | One-off workflow, user copy-pastes instructions and runs them manually |
| Reusable skill | `Skill-Powered Prompt` | Repeated workflow with similar inputs, user triggers by name when needed |
| Agent | `Agent` | Tool use, autonomous decisions, multi-step reasoning, or scheduled/unattended runs |

**How to present this to the user — recommendation first, then alternatives.** Pick the best fit based on the autonomy assessment and how often the workflow will run, then use `AskUserQuestion` with three plain-language options (recommended option first, marked "(Recommended)"). Example phrasing for the question text:

> "Now the big choice: **how do you want to run this workflow day-to-day?** There are three common shapes — I'll explain each, then recommend the one that fits you best.
>
> - **Step-by-step prompt** — A set of instructions you copy and paste into your AI tool each time. Lowest setup, no install. Best for one-off workflows you won't repeat often.
> - **Reusable skill** — A saved set of instructions you trigger by name (e.g., 'run the weekly review skill'). The AI loads them automatically when the situation matches. Best for workflows you'll run repeatedly with similar inputs.
> - **Agent** — A system that drives the whole workflow end-to-end on its own, calling tools and making decisions as it goes. Best when you want it to run on a schedule, handle decisions autonomously, or coordinate multiple steps without you in the loop.
>
> Based on your [autonomy level] workflow and the fact that [1-sentence signal from the workflow — e.g., 'you'll run this every Friday'], I recommend **a reusable skill**.
>
> *Why this matters:* this choice shapes the file the next step actually builds — a prompt is just instructions you keep handy, a skill is a saved capability the AI can invoke by name, and an agent is a system with its own decision-making. Each fits a different way of working.
>
> Which shape works for you?"

Use `AskUserQuestion` with three options (recommended first, marked "(Recommended)"). Option labels:

- **Reusable skill** — Saved instructions you trigger by name. Best for workflows you'll run repeatedly.
- **Step-by-step prompt** — Copy-paste instructions you run yourself. Best for one-off workflows, no setup.
- **Agent** — AI drives the whole thing end-to-end. Best when it should run on a schedule or make decisions on its own.

If the user pushes back, discuss in plain language — never drop into the internal jargon (`Prompt` / `Skill-Powered Prompt` / `Agent`) when talking to them.

**Artifact form is resolved internally, not asked.** Once platform + mechanism are confirmed, the model picks the specific artifact form (e.g., a SKILL.md file, a Claude Code subagent markdown, an Agent SDK Python script, a ChatGPT Workspace Agent) using the platform's `mode` field in the registry (`code` vs `guided`) and the user's apparent technical level. Default to the simplest no-code option for that platform. **Never ask a non-technical user to pick between technical artifact forms.** Build generates the right artifact from the platform + mechanism the model recorded.

**Human Involvement — derive internally, mention only as plain language.** Determine the involvement mode (`Augmented` vs `Automated`) from the trigger (manual = Augmented; scheduled/unattended = Automated). Mention it to the user in plain language as part of the Layer 1 confirmation ("Who's in the loop") — do not ask a separate question.

Single-agent vs. multi-agent is an architecture detail decided during Agent Configuration (Step 8) if Agent is selected — not a top-level choice here.

**Who is the orchestrator? (read before designing any Agent workflow.)** On **Claude Code or Cowork — any platform with a primary agentic loop — the primary session IS the orchestrator.** Do **not** design a separate "orchestrator agent" file. What you build are:
- **Orchestration logic** — captured as a command and/or a `CLAUDE.md` run section the primary loop follows (scan/classify/dispatch/label/summarize, etc.). This is not an "agent" artifact.
- **Sub-agent(s)** — the workers the primary loop dispatches, one per unit of work (e.g., per item in a batch). Sometimes **zero** sub-agents are needed — the orchestration logic + skills are enough.

The agent artifacts you generate are always the **workers the orchestrator delegates to**, never the orchestrator itself. Reserve a standalone, self-running "agent" artifact for **SDK platforms** where you deploy the agent process yourself. (This is the single most common design mistake on Claude Code: inventing an orchestrator agent when the primary loop already is one.)

**Fast-track for complete Workflow Requirements:** If the Workflow Requirements + conversation context provide enough information to resolve the autonomy level, tool extraction, and step classifications, you may present those internal/technical dimensions as a single summary block instead of stepping through questions one at a time.

**Platform (Step 3a) and Mechanism (Step 5) are never fast-tracked.** They are always asked or confirmed explicitly in plain language, in their own discrete confirmations, even when the answer seems obvious from earlier conversation. Non-technical users must see and approve these two choices on their own — they should not be embedded inside a larger summary block.

**Packaging decision:** Pick the Packaging value from platform + mechanism (single skill → Standalone Skill; multiple related artifacts → Plugin; ChatGPT with agent + skills → Workspace Agent; ad-hoc files → Loose Files). Include it in the playback below — but always pair the technical label with a plain-language explanation so the user learns what it means.

**Layer 1 confirmation — hard gate, rich playback in plain English** (after Step 5, before moving to Step 6):

This is a **hard gate**. Do not proceed to Step 6 without explicit user approval here. This is also a **teaching moment** — play back the full design analysis so the user can see and learn the building blocks involved, not just rubber-stamp a stripped-down summary.

By this point the user has already confirmed *where* (Step 3a) and *how it runs* (Step 5) in their own discrete confirmations. This gate plays the full architecture analysis back so they can verify, learn the vocabulary, and redirect anything that's wrong before any detailed decomposition work begins.

**How to write the playback:** Use the technical term, then immediately explain it in plain language in the same line. Never drop a bare technical label on its own. Every row teaches as it confirms.

For step-decomposed workflows:

> "Here's the design analysis based on your workflow definition. I'll explain each piece as I go — push back on anything that's off:
>
> - **Platform:** [Claude.ai] — the [browser app you sign into at claude.ai]. This is where your workflow will live.
> - **Packaging:** [Standalone Skill] — a [single self-contained set of instructions you upload once and reuse]. (Other options: Plugin, Workspace Agent, Loose Files — yours is Standalone Skill because [reason].)
> - **Autonomy level:** [Guided] — meaning [AI handles most of the work, you steer at key checkpoints]. (The scale runs Human → Deterministic → Guided → Autonomous.)
> - **Mechanism:** [Skill-Powered Prompt] — the [reusable skill you confirmed in the last step]. Runs in [Augmented] mode, which means [you're in the loop reviewing at checkpoints, not running on a schedule].
> - **Tools needed:** [list] — these are the external services your workflow will touch. I'll figure out exact integration options (MCP server, API, CLI, SDK) during Build.
> - **Steps classified:** [N steps — brief summary, e.g., '6 steps: 2 use AI directly, 3 are reusable skills, 1 is a human review']
> - **Skill candidates:** [list of skill names you'll be building, with one-line purpose each]
> - **Agent blueprints:** [summary if any agents are involved, or 'None — this workflow doesn't need an agent']
>
> Is this right? If yes, I'll work out the step-by-step details next. If anything's off — even small wording — tell me what to change."

For outcome-driven workflows, use the same playback structure with these substitutions:

- **Autonomy level:** Autonomous — meaning [the system figures out its own path based on the outcome and rules you defined]. (Outcome-driven workflows are always Autonomous by definition.)
- **Mechanism:** Agent — [the workflow is driven by an agentic loop that decides what to do based on context, not a fixed script]. On Claude Code/Cowork that loop is the **primary session (the orchestrator)** — see "Who is the orchestrator?" above.
- Replace **Steps classified** with **Capability domains mapped** — explain in plain language ("the buckets of capability the workflow needs to cover").
- **Agent blueprint:** summarize the **sub-agent(s) the orchestrator will dispatch** (the workers), or "None — the primary loop orchestrates directly using skills" if no sub-agent is needed. Do **not** describe a standalone orchestrator agent on Claude Code/Cowork.

**Wait for explicit approval** ("yes", "looks good", "go ahead", etc.) before moving to Step 6. If the user pushes back, revise the relevant decision (which may mean reopening Step 3a or Step 5) and re-present this gate.

**Why every row pairs jargon + plain English:** The Design skill is also an *education* tool. Users who run it repeatedly should start recognizing terms like "Standalone Skill", "Augmented", "Guided" — but only because they've seen them explained in context, not because they were dumped on them as labels. This playback is where that learning happens.

#### Step 6 — Classify Each Step

For every refined step, classify across all three building-block layers plus autonomy and role.

**Per-step classification dimensions:**
- **Autonomy level**: Human / Deterministic / Guided / Autonomous — use only these four canonical terms. Previous terms like "Semi-Autonomous", "AI-Assist", "AI-Deterministic", or compound forms are retired per the Workflow Design Matrix.
- **Orchestration layer**: Prompt / Skill / Agent
- **Integration layer**: Which integration block(s) apply, with use/build tags
- **Intelligence layer**: Model capability, context sources, memory needs, project scope
- **Human-in-the-loop gates**: Where human review is recommended
- **Role** (organizational lens): Who performs this step — which role owns it

**Integration layer blocks:**

| Block | Description | Tag |
|-------|-------------|-----|
| **MCP** | Model Context Protocol server | Use existing / Build new |
| **API** | REST, GraphQL, or other web API | Use existing |
| **SDK** | Client library / framework | Use existing / Build new (rare) |
| **CLI** | Command-line tool | Use existing |

Most integration blocks are "use existing." "Build new" applies primarily to MCP (custom data sources) and rarely to SDKs.

**Plain-language gloss (for non-technical users — explain these the first time they come up):**
- **MCP** = a plug-and-play connection to a service, no coding needed.
- **API** = a way to talk to a service that needs a little code/setup.
- **SDK** = a coding toolkit (most technical option).
- **CLI** = a command you run in a terminal.

**Intelligence layer blocks:**

| Block | Description | Per-step classification |
|-------|-------------|----------------------|
| **Model** | Which model capability | Reasoning-heavy / Fast / Vision |
| **Context** | Files, docs, libraries needed | List specific sources |
| **Memory** | Persistent state across runs | Yes / No + what's stored |
| **Project** | Workspace or project scope | Yes / No |

**Per-step classification table format:**

| Step | Orchestration | Integration (use/build) | Intelligence | Human Gate |
|------|--------------|------------------------|--------------|------------|
| Pull calendar events | Skill | MCP: Google Calendar (use) | Model: fast | No |
| Generate coaching questions | Agent | — | Model: reasoning; Context: powerful-questions.md | Yes |
| Save prep notes | Skill | CLI: git (use) | Model: fast | No |

Each row captures one step. The Orchestration column shows the block from that layer. The Integration column lists block(s) with use/build tags, or "—" if the step needs no external tool access. The Intelligence column lists applicable blocks with their per-step classification values.

Additionally, for each step record the **autonomy level** and **role** (these appear in the full spec output but are omitted from the compact table above for readability).

If a step's inputs include items flagged as "No" or "Partial" in the Context Inventory, note this in the classification. A step classified as Autonomous but dependent on inaccessible data should be flagged: "Autonomy contingent on resolving data access for [item]."

Present the mapping as a clear table. Walk through reasoning for non-obvious classifications. Ask if the user wants to adjust anything.

**Integration Discovery**

After classifying every step, recommend available integration options for each tool need identified in the Integration layer. This helps students who don't know what CLIs, APIs, MCP servers, or SDKs exist for a given tool.

**Discovery process (4-part chain):**

1. **Curated tool catalog** — Fetch the `curated-tools` section from the remote platform registry JSON (`https://raw.githubusercontent.com/jamesgray-ai/handsonai/main/plugins/handsonai/registries/platform-registry.json`). Match workflow tool needs against each entry's `integrations` field. Curated tools are instructor-vetted recommendations — present them first, marked as recommended.

2. **Model knowledge** — Supplement with additional integration options the model knows about. For well-known integrations (Google Calendar, Gmail, Slack, GitHub, etc.), skip web search — model knowledge is sufficient.

3. **Integration registries** — Fetch the `integration-registries` list from the same remote registry JSON. For each cataloged source, search for integrations matching the tool need:

   ```json
   {
     "integration-registries": [
       {
         "name": "Context7",
         "type": "mcp",
         "tool": "query-docs",
         "notes": "Library docs, API references, SDK docs via MCP"
       },
       {
         "name": "context-hub",
         "type": "local",
         "check": "context-hub --version",
         "notes": "Community-maintained integration registry (CLI)"
       },
       {
         "name": "MCP Registry",
         "type": "web-search",
         "url": "https://mcpregistry.dev",
         "notes": "MCP server directory"
       }
     ]
   }
   ```

   **MCP tool availability:** Before querying an MCP-type registry source (e.g., Context7), check the user's configured MCP servers. If the required MCP server is not configured, skip it and proceed to the next source in the chain.

4. **Web search (validation + fallback)** — For less common tools, when uncertain, or when no match is found in prior steps, search the web to verify existence and find current docs. Catches new releases and uncataloged tools. Batch searches when multiple tool needs are identified to avoid latency.

   **Latency management:** Use judgment about when web search adds value. Well-known integrations (Google Calendar, Gmail, Slack, GitHub) don't need validation searches. Reserve web search for new or niche tools.

   **Precedence rule:** When web search results contradict model knowledge (e.g., model proposes an MCP server that web search reveals was deprecated), web search takes precedence. Flag the discrepancy and present only verified options.

**Fallback ladder (never hard-fail).** Any of the lookups above can fail — the remote registry JSON may be unreachable, or web search may be unavailable on the platform. Degrade gracefully in this order, and tell the user what was degraded: **session cache** (registry already fetched this session) → **model knowledge** → **web search** → **best-effort note**. If you end on model-knowledge-only or best-effort, add a one-line flag like "Integration options below are unverified (registry/web unavailable) — confirm before relying on them." Never block Design because a fetch failed.

**Matching semantics:** Matching is model-driven, not exact string matching. The model reads the workflow's tool needs (e.g., "Google Calendar access" from the step classification) and matches them against the `integrations` array values (e.g., `"google-calendar"`) using semantic understanding. This allows natural language tool needs to match standardized integration tags without requiring exact normalization.

**Presentation format:**

For step-decomposed: `**[Tool] access needed (Steps N, M):**`
For outcome-driven: `**[Tool] access needed (Domains: X, Y):**`

> **[Tool] access needed ([Steps N, M / Domains: X, Y]):**
>
> **Curated (recommended):**
> | Block | Option | Trade-off |
> |-------|--------|-----------|
> | MCP | [Name] MCP | Easiest — plug-and-play |
> | CLI | [Name] CLI | Good for automation/scripting |
>
> **Also available:**
> | Block | Option | Trade-off |
> |-------|--------|-----------|
> | API | [Name] REST API | Most flexible, more code |
> | SDK | [Name] Client Library | Best DX for code-heavy builds |
>
> *Recommendation: [block] for [rationale]*

**Layer 2 confirmation moment** (after Step 6, before Skill Discovery and Component Blueprints):

The decomposition is complete. Before generating detailed component blueprints (the most expensive work to redo), confirm the L2 decisions are right:

> "Decomposition confirmed:
> - **Steps requiring new skills:** [count] — [list step IDs and proposed skill names]
> - **Steps using existing skills:** [count] — [list step IDs and existing skill names]
> - **Steps as inline prompts:** [count] — [list step IDs]
> - **Steps requiring agents:** [count] — [list]
> - **Human-performed steps:** [count] — [list]
>
> Moving to Layer 3 — Component Blueprints. I'll write the field-level spec for each new skill and agent. Confirm to proceed, or push back on the decomposition."

If the user pushes back, revise the L2 decomposition (and possibly L1 if the disagreement is architectural). Re-confirm before proceeding. Like the L1 confirmation, this is lightweight — not a hard gate — but it's the last cheap moment to catch decomposition mistakes before the detailed spec work.

#### Step 6b — Skill Discovery

For every step classified as needing a **Skill** in Step 6, search for existing skills before assuming one needs to be built.

**Search order:**

1. **Local skills** — Search the user's own `.claude/skills/`, plugin skills directories, and any project-level skill directories. These are pre-vetted and can be recommended directly.

2. **External registries** — Fetch the `skill-registries` list from the remote platform registry:

   `https://raw.githubusercontent.com/jamesgray-ai/handsonai/main/plugins/handsonai/registries/platform-registry.json`

   The registry JSON is fetched once per session and cached. Both Skill Discovery (Step 6b) and Integration Discovery use the same cached copy.

   This provides a curated, always-current list of sites to search. For each registry, search for skills matching the step's requirements.

   ```json
   {
     "skill-registries": [
       {
         "name": "skills.sh",
         "type": "web-search",
         "url": "https://skills.sh",
         "notes": "Community skill marketplace"
       },
       {
         "name": "Context7",
         "type": "mcp",
         "tool": "query-docs",
         "notes": "Library docs and skills via MCP"
       }
     ]
   }
   ```

   New registries are added by pushing to the JSON file — all users get them immediately, no plugin upgrade needed.

3. **Web search fallback** — If no match found in cataloged registries, or if the registry fetch fails, search the web for community skills that could fulfill the step. This also catches new skill registries not yet in the catalog.

4. **User approval gate** — Present all discovered skills as **candidates**, clearly separated into:
   - **Local (pre-vetted):** Skills the user already has installed. Can be included in the spec with a confirmation.
   - **External (requires vetting):** Community skills from registries or web search. Flag security implications — these run with the model's permissions and should be reviewed before adoption. User must explicitly approve each external skill candidate before it's included.

**Presentation format:**

For each step (or capability domain, for outcome-driven workflows) that needs a skill, present candidates in a table:

> **[Step 3 / Domain: Research] needs a skill: "Format coaching prep notes"**
> | Source | Skill | Status |
> |--------|-------|--------|
> | Local | `coaching-prep-notes-assembly` (your plugin) | Pre-vetted — include? |
> | skills.sh | `markdown-document-builder` by @community | Requires review — [link] |
> | Web search | `doc-formatter` on GitHub | Requires review — [link] |
> | None found | Build new | Fallback |
>
> *External skills run with model permissions. Review source code before approving.*

If no suitable existing skill is found for a step, tag that step as **"build new"** — it flows into Step 7 (Identify Skill Candidates).

#### Step 7 — Identify Skill Candidates

For steps where Skill Discovery (Step 6b) found an existing skill, skip to the next step.

This step only applies to steps tagged **"build new"** in Step 6b. Tag those steps that should become skills. For each skill candidate, gather all 12 fields. The complete field set is defined in the Skill Candidates template section in Step 9 — collect every field during the collaborative session so the spec is complete on first write:

- **ID** — stable skill ID (S1, S2, …)
- **Name** — lowercase-hyphenated, ≤64 chars, no consecutive hyphens; matches the skill directory name
- **Description** — ≤1024 chars, MUST start with "This skill should be used when..." — verbatim text for the SKILL.md frontmatter; drives auto-activation
- **Purpose** — one-sentence internal summary for the spec reader
- **Covers Steps / Domains** — which step IDs (or capability domains) this skill spans
- **Inputs** — what the skill receives
- **Outputs** — what the skill produces
- **Decision Logic** — key rules, criteria, evaluation frameworks
- **Failure Modes** — condition → action, one per line
- **Required Tools** — integration blocks the skill needs at runtime (e.g., MCP: Notion)
- **Depends On** — other skill IDs (S2, S3) or artifacts that must exist first, or "None"
- **Stateful?** — Yes / No, does the skill maintain state across invocations? Drives Memory building-block decisions.

#### Step 8 — Agent Configuration

(When orchestration mechanism is Agent.) For each agent the workflow needs, gather all 13 fields. The complete field set is defined in the Agent Configuration template section in Step 9 — collect every field during the collaborative session so the spec is complete on first write:

| Field | What to specify |
|-----------|----------------|
| **ID** | Stable agent ID (A1, A2, …) |
| **Name** | Unique agent name (lowercase-hyphenated, matches the agent filename without extension) |
| **Description** | ≤1024 chars, MUST start with "Use this agent when..." — verbatim text for the agent file frontmatter; drives invocation |
| **Mission** | One-sentence primary purpose |
| **Responsibilities** | Bulleted list of what the agent does once invoked |
| **Output Format** | Structured description of what the agent's output should look like |
| **Tone & Style** | Voice and register (e.g., "concise, technical, no hedging") |
| **Constraints** | Must-not-dos, scope boundaries, source restrictions |
| **Model** | Capability tier: reasoning-heavy / fast / vision |
| **Memory Scope** | user / project / local / none — cross-session learning scope |
| **Tools** | External tools the agent needs (reference Integration Options entries by tool name) |
| **Skills** | Skill IDs the agent has access to (S1, S2, …) |
| **Trigger Examples** | 2-3 structured examples (context → user message → expected behavior → invocation) — Build uses these verbatim as `<example>` blocks in the description |

The build skill maps these to platform-specific fields at runtime (e.g., "reasoning-heavy" → `opus` on Claude Code, trigger examples → `<example>` blocks).

For multi-agent: orchestration pattern, agent handoffs, human review gates — see the Multi-Agent Configuration section in the template.

#### Step 8b — Verify Evaluation Inputs

The Workflow Requirements already includes **Acceptance Criteria** (what good looks like, dimensions that matter, minimum bar) and **Example Scenarios** (3-5 representative inputs with what to look for) from the Deconstruct step. Do **not** ask the user to re-state these.

Confirm them briefly:

> "Your Workflow Requirements includes Acceptance Criteria and [N] Example Scenarios. These feed directly into Step 5 (Test). Anything to add or adjust before I generate the Design Spec?"

If the user adds or adjusts anything, update the Workflow Requirements file (not the Design Spec) — that file remains the canonical source of acceptance criteria and test scenarios. The Design Spec references them by file path; it does not duplicate them.

If the Workflow Requirements is missing Acceptance Criteria or Example Scenarios entirely (which shouldn't happen if Deconstruct was run), pause and ask the user to run `/deconstruct` again or fill them in manually before continuing.

#### Step 9 — Assemble Design Spec (do not write the file yet)

Assemble the full Design Spec **content** using the template below — but **do not write it to disk yet**. The file is written only after the user approves it in Step 10. Every section is mandatory unless marked (optional). Do not add, remove, rename, or reorder sections. Target path (written in Step 10): `outputs/[workflow-name]-design-spec.md`.

**Why not write yet:** In Claude Code plan mode, writing files is blocked until the user approves and exits plan mode; in Cowork there is no plan mode but the same rule applies — never persist a deliverable before approval. So assemble + self-test in memory, present for approval (Step 10), then write.

**Assembly order:**

1. Assemble all spec sections (frontmatter through Stakeholders) following the template — in memory.
2. **Run the Build Skill Needs Checklist** (at the end of this step) against the assembled content to verify every required field is present and well-formed.
3. **Assemble the Self-Test Summary section** as the final section. For each checklist item, mark ✓ (passed) or ⚠️ (issue — describe inline). This makes the verification visible to the user.
4. If any checklist item failed (⚠️), fix the underlying section **before presenting for approval**. The Self-Test Summary should ideally show all ✓ — but if a ⚠️ remains (e.g., a deliberate gap the user accepted), surface it honestly.
5. Carry the assembled content into Step 10 for approval. **Do not write the file in this step.**

**Conditional sections to generate:**
- `Orchestrator Prompt Outline` — only when mechanism is `Prompt` or `Skill-Powered Prompt`. Omit for `Agent`.
- `Agent Configuration` — whenever the design includes at least one sub-agent/agent artifact (the common case for `Agent` mechanism, including outcome-driven). Omit only if there are genuinely zero sub-agents (orchestration logic + skills only) — then set `agents: 0` and document the orchestration logic in the Deployment Plan.
- `Multi-Agent Configuration` — only when more than one agent is defined.
- `Stakeholders` — only for Organizational lens.

---

**Template:**

```markdown
---
workflow: [kebab-case name]
requirements_file: outputs/[workflow-name]-requirements.md
spec_version: 2.1
definition_type: Step-Decomposed | Outcome-Driven
mechanism: Prompt | Skill-Powered Prompt | Agent
involvement: Augmented | Automated
platform: [user's platform, e.g., Claude Code, Claude.ai, Cowork, Codex, ChatGPT, Gemini CLI]
platform_mode: code | guided
packaging: Plugin | Standalone Skill | Workspace Agent | Loose Files
counts:
  steps: [N]
  skills: [N]
  agents: [N]
  integrations: [N]
---

# [Workflow Name] — Design Spec

## Source

**Workflow Requirements:** `outputs/[workflow-name]-requirements.md`

This Design Spec consumes the Workflow Requirements as canonical input. Outcome, Metadata, Context Inventory, Acceptance Criteria, Example Scenarios, Human Gates, Steps Overview, and per-step requirements are defined there — not restated here. Read the Workflow Requirements alongside this spec when building.

The spec is organized into three layers that build on each other:

1. **Architecture (L1)** — strategic decisions: platform, mechanism, autonomy, packaging
2. **Decomposition (L2)** — for each step (or capability domain), what AI building block delivers it
3. **Component Blueprints (L3)** — field-level specs for each new skill and agent

---

## Layer 1 — Architecture

*Strategic decisions that shape everything downstream.*

## Execution Pattern

**[Mechanism]** — [1-2 sentence rationale for why this mechanism was chosen over alternatives].

## Architecture Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Lens | Individual / Organizational | [reason] |
| Platform | [name] | [reason] |
| Platform Mode | code / guided | [inferred from platform or confirmed] |
| Orchestration | Prompt / Skill-Powered Prompt / Agent | [reason] |
| Involvement | Augmented / Automated | [reason] |
| Packaging | Plugin / Standalone Skill / Workspace Agent / Loose Files | [reason — determines how Build groups and ships artifacts] |
| Trigger | [trigger description from Workflow Requirements] | [implications for involvement, infrastructure] |

**Packaging values:**
- **Plugin** — Multiple related artifacts shipped together (e.g., handsonai-plugins marketplace plugin, set of `.claude/` files distributed via marketplace).
- **Standalone Skill** — A single skill, uploaded directly (e.g., zip uploaded to Claude.ai, single SKILL.md in `.claude/skills/`, Codex skill in `.agents/skills/`, ChatGPT skill).
- **Workspace Agent** — A ChatGPT Workspace Agent that bundles orchestration + skills + tools as a unit. (Custom GPTs are deprecated; Workspace Agents are the current ChatGPT primitive.)
- **Loose Files** — Individual files in a project directory, no distribution layer.

## Autonomy Spectrum Summary

The workflow-level autonomy assessment and the rationale that drove it. (Per-step autonomy classifications appear in the Decomposition table below.)

For step-decomposed workflows: group steps by autonomy level. For each group, explain WHY those steps have that classification.

For outcome-driven workflows: replace this section with an **Autonomy Statement** — a brief paragraph stating: "This is an outcome-driven workflow. Autonomy is Autonomous — the agent system determines its own execution path based on the Outcome, Inputs, Rules & Constraints, and Acceptance Criteria defined in the Workflow Requirements."

## Integration Options

For each tool identified in the Decomposition table (or Capability Domain Mapping for outcome-driven):

### [Tool Name] (Steps N, M / Domains: X, Y)

**Curated (recommended):**

| Block | Option | Source URL | Trade-off |
|-------|--------|-----------|-----------|
| [MCP/API/SDK/CLI] | [name] | [URL] | [trade-off] |

**Also available:**

| Block | Option | Source URL | Trade-off |
|-------|--------|-----------|-----------|
| [MCP/API/SDK/CLI] | [name] | [URL] | [trade-off] |

*Recommendation: [block] for [rationale]*

## Model Recommendation

**Default capability:** [reasoning-heavy / fast / vision] — [rationale]

*(Plain-language gloss for non-technical users: **reasoning-heavy** = slower but handles complex judgment/nuance; **fast** = quicker, best for simple/high-volume steps; **vision** = can read images/screenshots.)*

**Per-step overrides** (optional):
- Steps N, M: [different capability] — [rationale]

**Per-platform mapping** (Build resolves at generation time):
- Claude Code / Claude.ai / Cowork: `opus` (reasoning-heavy) / `sonnet` (balanced) / `haiku` (fast)
- ChatGPT / Codex: `gpt-5` or `o3` (reasoning-heavy) / `gpt-4o` (balanced) / `gpt-4o-mini` (fast)
- Gemini: `gemini-2.5-pro` (reasoning-heavy) / `gemini-2.5-flash` (fast)

(These mappings are guidance; Build verifies current model names via web search before generating.)

---

## Layer 2 — Decomposition

*For each step or capability domain, what AI building block delivers it. Layer 2 sections in order: Step-by-Step Decomposition (or Capability Domain Mapping for outcome-driven), Orchestrator Prompt Outline (conditional on mechanism), Data Readiness Summary, Recommended Implementation Order.*

## Step-by-Step Decomposition

Steps are defined in the Workflow Requirements. This table adds the building-block classification and the concrete Build output for each:

| Step | Name (from Requirements) | Autonomy | Orchestration | Integration (use/build) | Intelligence | Build Output | Human Gate? |
|------|------|----------|---------------|------------------------|--------------|--------------|-------------|

Column definitions:
- **Step**: Step ID from Workflow Requirements (e.g., Step 1, Step 2)
- **Autonomy**: Human / Deterministic / Guided / Autonomous (canonical terms only)
- **Orchestration**: Prompt / Skill / Agent
- **Integration**: Block + tool + action tag (e.g., "MCP: Notion (use)") or "—" if none
- **Intelligence**: Model class + context sources + memory flag (e.g., "Model: fast" or "Model: reasoning; Context: C2, C5")
- **Build Output**: One of the canonical values: `New skill: S1` (build a new skill, defined below) / `Use existing: [name]` (reference an existing skill) / `New agent: A1` (build a new sub-agent, defined below) / `Inline prompt → Workflow Requirements Step N` (this step becomes a prompt block in the orchestrator, sourced from the named step's requirements) / `Handled by orchestrator` (no separate artifact — the orchestrating primary loop, or a deployed agent on SDK platforms, handles this via its own instructions; legacy synonym: `Handled by agent`) / `MCP server: [name]` (configure a connector) / `Human (no artifact)` (no AI artifact — human-performed)
- **Human Gate?**: Yes / No (sourced from Workflow Requirements Human Gates table)

## Orchestrator Prompt Outline

*Include this section only when mechanism is `Prompt` or `Skill-Powered Prompt`. Omit for `Agent` — on Claude Code/Cowork the primary loop orchestrates (capture that as orchestration logic in the Deployment Plan), and the workers are documented in Agent Configuration below.*

The high-level shape of the orchestrator prompt the user runs to execute the workflow. This is not the full prompt text — it's the structural skeleton Build expands into the orchestrator. Build derives full step content from the Workflow Requirements' Step Details.

```
[Intro: one paragraph describing what this prompt does and when to run it]

[Step 1 invocation]
  - Source: Workflow Requirements Step 1
  - Build Output: [from Decomposition table]
  - User provides: [inputs from Workflow Requirements]
  - Produces: [outputs from Workflow Requirements]

[PAUSE for user review — sourced from Workflow Requirements Human Gates table]
  - What user is reviewing: [describe]
  - User decides: [decision criteria]

[Step 2 invocation]
  - ...

[Final output: what the workflow delivers, format, where it goes]
```

Use the actual Step IDs and Build Output values. Mark PAUSE points where Human Gates apply. Indicate where the user provides input vs. where the workflow runs autonomously.

## Data Readiness Summary

Items in the Workflow Requirements' Context Inventory flagged as `Partial` or `No` for AI Accessible. If all items are `Yes`, state: "All context items are AI-accessible. No data readiness actions required."

| Context ID | Current State | Required Action | Affects Steps |
|---|---|---|---|
| C1 | Partial / No | [action needed — e.g., "Export weekly to /data/foo.csv"] | [step numbers] |

## Recommended Implementation Order

Build artifacts in this order. Dependencies within each tier follow the `Depends On` field of each skill.

### Quick Wins (implement first)
1. **[Artifact ID + name]** — [rationale]

### Core (implement second)
1. **[Artifact ID + name]** — [rationale]

### Future Enhancement (optional)
1. **[Artifact ID + name]** — [rationale]

---

## Layer 3 — Component Blueprints

*Field-level specs for each new skill, agent, and configuration. Build uses these to generate artifacts.*

## Skill Candidates

For each Build Output tagged `New skill: SN` above:

### S1 — [skill-name]

| Field | Detail |
|---|---|
| **ID** | S1 |
| **Name** | [lowercase-hyphenated, ≤64 chars, no consecutive hyphens; matches the skill directory name] |
| **Description** | [≤1024 chars; MUST start with "This skill should be used when..." — this is the literal description that goes into the SKILL.md frontmatter and drives auto-activation on Claude.ai, Cowork, and code-mode platforms] |
| **Purpose** | [one-sentence internal summary — for the Design Spec reader, not the skill description] |
| **Covers Steps / Domains** | [list of Step IDs, or capability domain names for outcome-driven] |
| **Inputs** | [name — description, one per line; "type" is the expected user-provided value description, not a strict type system] |
| **Outputs** | [what the skill produces] |
| **Decision Logic** | [key rules, criteria, evaluation frameworks — multiline OK] |
| **Failure Modes** | [condition → action, one per line] |
| **Required Tools** | [block: tool (action) — e.g., MCP: Notion (use)] |
| **Depends On** | [other skill IDs (S2, S3) or artifacts that must exist first, or "None"] |
| **Stateful?** | Yes / No — does the skill maintain state across invocations? Drives Memory building-block decisions. |

## Agent Configuration (include whenever ≥1 sub-agent/agent artifact is defined; otherwise omit)

> Each entry documents a **worker sub-agent the orchestrator dispatches** — not the orchestrator itself. On Claude Code/Cowork the orchestrator is the primary loop (no agent file). If the design has zero sub-agents, omit this section, set `agents: 0`, and capture the orchestration logic in the Deployment Plan.

For each Build Output tagged `New agent: AN` above:

### A1 — [agent-name]

| Field | Detail |
|---|---|
| **ID** | A1 |
| **Name** | [lowercase-hyphenated, matches the agent filename without extension] |
| **Description** | [≤1024 chars; MUST start with "Use this agent when..." — this is the literal description that goes into the agent file frontmatter and drives invocation. Include 2-3 `<example>` blocks (see Trigger Examples field below) inline at the end.] |
| **Mission** | [one-sentence primary purpose] |
| **Responsibilities** | [bulleted list of what the agent does once invoked] |
| **Output Format** | [structured description of what the agent's output should look like — sections, fields, format constraints] |
| **Tone & Style** | [voice/register, e.g., "concise, technical, no hedging"] |
| **Constraints** | [must-not-dos, scope boundaries, source restrictions] |
| **Model** | [capability tier: reasoning-heavy / fast / vision] |
| **Memory Scope** | user / project / local / none — controls cross-session learning (Claude Code agent format supports this; on other platforms, document the equivalent) |
| **Tools** | [external tools needed — reference Integration Options entries by tool name] |
| **Skills** | [Skill IDs the agent has access to — S1, S2, …] |
| **Trigger Examples** | [2-3 structured examples, each: context → user message → expected agent behavior → invocation. Build uses these verbatim to construct the `<example>` blocks in the agent's description field.] |

## Multi-Agent Configuration (only when more than one agent is defined)

**Orchestration Pattern:** Supervisor (one delegates to others) / Pipeline (agents in sequence) / Parallel (agents run concurrently) / Network (agents call each other peer-to-peer)

> **On Claude Code/Cowork the Supervisor is the primary loop itself — not a generated agent file.** Document the pattern, but the "coordinator" is the orchestration logic (command/`CLAUDE.md` run section), and the entries below are the **worker sub-agents** it dispatches. Prefer **one sub-agent per unit of work** (e.g., per item in a batch) over splitting by function, to keep each unit's transaction atomic and enable parallel fan-out.

**Coordinator:** [Agent ID that coordinates, or "Primary loop (orchestration logic — no agent file)" on Claude Code/Cowork]

**Handoff Contracts:**

| From → To | Trigger | Data Passed | Format |
|---|---|---|---|
| A1 → A2 | [when A1 finishes / when condition X] | [what data passes] | [format / schema description] |

**Aggregation Strategy:** [How results combine if parallel or network — last-writer-wins, merge, supervisor-decides, etc. Write "N/A" for Pipeline.]

## Prerequisites

1. [Numbered list of requirements that must be in place before the workflow can run — focus on platform setup, accounts, credentials, plugin installs. The Workflow Requirements covers content artifacts via its Context Inventory.]

## Deployment Plan

For each artifact produced, document where it lives and how it gets deployed:

| Artifact | Target Location | Deployment Steps |
|---|---|---|
| S1 — `[name]` | [platform-specific path or destination] | [high-level steps; Build expands during artifact generation] |
| A1 — `[name]` | [platform-specific path or destination] | [high-level steps] |
| MCP: [tool] | [where the config lives] | [install/auth steps] |

**Packaging note:** [How the artifacts ship together based on the Packaging decision — e.g., "All S1–S3 + A1 bundle into a plugin in the user's marketplace fork"; "Each skill uploaded individually to Claude.ai"; "All instructions consolidated into one GPT's instructions field"]

**Recommended for frequent use:** [recommendation, e.g., "Save as Claude Project for one-click reuse"]

---

## Cross-Layer Sections

*These sections apply across all three layers — handoff and metadata that doesn't belong to a single layer.*

## Evaluation Inputs

**Acceptance Criteria, Example Scenarios, and Human Gates are sourced from the Workflow Requirements file** (`outputs/[name]-requirements.md`). Do not duplicate them here. Step 5 (Test) reads them from that file directly.

## Deferred to Build

Decisions intentionally left for Build to resolve. Build should not need to re-ask the user about anything else in the spec.

- [ ] Specific platform offering (if platform was given at ecosystem level, e.g., "Claude" vs Claude Code/Claude.ai/Cowork)
- [ ] Shareability (file vs code distribution mode)
- [ ] Exact model version per platform (mapping above is guidance; Build verifies current names)
- [ ] Integration setup specifics (auth flow, region, plan tier)

## Stakeholders (optional — only for Organizational lens)

[Role swimlane diagram and stakeholder details — sourced from Workflow Requirements Metadata.]

## Self-Test Summary

*Populated by the Design skill after running the Build Skill Needs Checklist. Each item marks ✓ (passed) or ⚠️ (issue — described inline). Lets users and downstream consumers see what was verified before approval.*

### Structure
- ✓ / ⚠️ Frontmatter present with all required fields (workflow, requirements_file, spec_version, definition_type, mechanism, involvement, platform, platform_mode, packaging, counts)
- ✓ / ⚠️ Source section names Workflow Requirements file
- ✓ / ⚠️ Architecture Decisions table complete (7 rows)
- ✓ / ⚠️ Decomposition table complete with all step IDs from Workflow Requirements
- ✓ / ⚠️ All Autonomy values use canonical terms (Human / Deterministic / Guided / Autonomous)
- ✓ / ⚠️ All Integration column entries follow the `block: tool (use/build)` format
- ✓ / ⚠️ All Build Output values use canonical forms (`New skill: SN` / `Use existing: [name]` / `New agent: AN` / `Inline prompt → Workflow Requirements Step N` / `Handled by orchestrator` [legacy synonym `Handled by agent` accepted] / `MCP server: [name]` / `Human (no artifact)`)
- ✓ / ⚠️ Packaging value uses a canonical form (`Plugin` / `Standalone Skill` / `Workspace Agent` / `Loose Files`)

### Skill Candidates
- ✓ / ⚠️ Every `New skill: SN` reference has a matching entry
- ✓ / ⚠️ Every skill has all 12 fields
- ✓ / ⚠️ Every skill Name conforms to format rules (lowercase-hyphen, ≤64 chars, no consecutive hyphens)
- ✓ / ⚠️ Every skill Description starts with "This skill should be used when..." and is ≤1024 chars

### Agent Configuration
- ✓ / ⚠️ Every `New agent: AN` reference has a matching entry
- ✓ / ⚠️ Every agent has all 13 fields
- ✓ / ⚠️ Every agent Description starts with "Use this agent when..." and is ≤1024 chars
- ✓ / ⚠️ Multi-Agent Configuration present when >1 agent defined

### Cross-references
- ✓ / ⚠️ Every tool in Integration column has a matching Integration Options entry with a Source URL
- ✓ / ⚠️ Every skill `Depends On` reference points to a defined skill ID

### Mechanism-specific
- ✓ / ⚠️ Orchestrator Prompt Outline present (when mechanism is Prompt or Skill-Powered Prompt)
- ✓ / ⚠️ Agent Configuration present (when mechanism is Agent)

### Completeness
- ✓ / ⚠️ Model Recommendation present with default capability and per-platform mapping
- ✓ / ⚠️ Data Readiness Summary present (even if "all accessible")
- ✓ / ⚠️ Deployment Plan present with target location, deployment steps, and Packaging note
- ✓ / ⚠️ Evaluation Inputs present (pointer, not duplication)
- ✓ / ⚠️ Deferred to Build present
```

---

**Build Skill Needs Checklist**

Before saving the spec, verify every item. If any is missing, go back and add it:

- [ ] **Frontmatter** is present with workflow, requirements_file, spec_version, definition_type, mechanism, involvement, platform, platform_mode, packaging, and counts
- [ ] **Source** section names the Workflow Requirements file path
- [ ] `Architecture Decisions` table has Lens, Platform, Platform Mode, Orchestration, Involvement, Packaging, and Trigger rows
- [ ] Every step in the decomposition table has separate Orchestration, Integration, Intelligence, and Build Output columns
- [ ] Step IDs in the decomposition table match the Step IDs in the Workflow Requirements (Step 1, Step 2, …)
- [ ] Every step uses canonical autonomy terms: Human / Deterministic / Guided / Autonomous
- [ ] Every Integration column entry includes the block type, tool name, and use/build tag
- [ ] Every Build Output value is one of the canonical forms (`New skill: SN`, `Use existing: [name]`, `New agent: AN`, `Inline prompt → Workflow Requirements Step N`, `Handled by orchestrator` [legacy synonym `Handled by agent` accepted], `MCP server: [name]`, `Human (no artifact)`)
- [ ] Every `New skill: SN` reference has a matching Skill Candidates entry with the SN ID
- [ ] Every `New agent: AN` reference has a matching Agent Configuration entry with the AN ID
- [ ] Every Skill Candidate has all 12 fields: ID, Name, Description, Purpose, Covers Steps, Inputs, Outputs, Decision Logic, Failure Modes, Required Tools, Depends On, Stateful?
- [ ] Every Skill Candidate's Name conforms to format rules (lowercase-hyphen, ≤64 chars, no consecutive hyphens)
- [ ] Every Skill Candidate's Description starts with "This skill should be used when..." and is ≤1024 chars
- [ ] Every Agent Configuration has all 13 fields: ID, Name, Description, Mission, Responsibilities, Output Format, Tone & Style, Constraints, Model, Memory Scope, Tools, Skills, Trigger Examples
- [ ] Every Agent Configuration's Description starts with "Use this agent when..." and is ≤1024 chars
- [ ] If more than one agent is defined, Multi-Agent Configuration section is present with Orchestration Pattern, Coordinator, Handoff Contracts, and Aggregation Strategy
- [ ] Every tool in the Integration column has a matching entry in Integration Options with at least one Source URL
- [ ] Model Recommendation section is present with a default capability and per-platform mapping
- [ ] Data Readiness Summary is present (even if "all accessible") — references Context IDs from the Workflow Requirements
- [ ] Deployment Plan is present with target location and deployment steps for each artifact, plus a Packaging note
- [ ] Packaging value is one of the canonical forms (`Plugin`, `Standalone Skill`, `Workspace Agent`, `Loose Files`)
- [ ] Orchestrator Prompt Outline section is present when mechanism is `Prompt` or `Skill-Powered Prompt` (omitted when mechanism is `Agent`)
- [ ] Evaluation Inputs section is present, pointing to the Workflow Requirements file (do not duplicate Acceptance Criteria or Example Scenarios)
- [ ] Deferred to Build section lists what Build will resolve at generation time
- [ ] Self-Test Summary section is present at the end of the spec, with each item marked ✓ (passed) or ⚠️ (issue — described inline)

#### Step 10 — Spec Approval Gate, then write the file

**This is a hard gate. Do not write the spec file or proceed without explicit approval.**

Present a summary of the assembled (not-yet-written) Design Spec:

> "Here's the Design Spec summary:
>
> - **Autonomy:** [level] (for outcome-driven: Autonomous)
> - **Mechanism:** [orchestration mechanism] ([involvement mode])
> - **Structure:** [count] steps, [count] skill candidates, [count] agents (for outcome-driven: [count] capability domains, [count] skill candidates, [count] agents)
> - **Integration options:** [count] tools with recommended integration approaches
> - **Implementation order:** [brief summary]
>
> The full spec is **ready for approval** — I'll save it to `outputs/[workflow-name]-design-spec.md` once you approve.
>
> **Do you approve this spec?** I won't write the file or generate any artifacts until you confirm. If you want changes, tell me what to adjust and I'll revise."

If the user requests changes, **revise the assembled content in memory**, re-run the self-test, and re-present — still without writing the file.

**Only after explicit approval:**
1. **Write the spec** to `outputs/[workflow-name]-design-spec.md`. (In Claude Code, this is the point where the user exits plan mode so the write can happen; in Cowork, write directly.)
2. Then tell the user:

> - **Claude Code:** "Spec approved and saved to `outputs/[workflow-name]-design-spec.md`. If you're in plan mode, **exit now** (`shift+tab` or `/plan`) so the Build phase can generate artifacts."
> - **Cowork:** "Spec approved and saved to `outputs/[workflow-name]-design-spec.md`."
>
> "To build the workflow, run the `build` skill (Step 4) (or say *'Build the workflow from my Design Spec'*)."

### Outcome-Driven Processing Path

When the Workflow Requirements has `Definition Type: Outcome-Driven`, the following modifications apply to the standard workflow:

**Step 3 (Architecture Decisions):** Same as standard, but the source sections differ. For outcome-driven Workflow Requirements, extract tools from the **Inputs**, **Rules & Constraints**, and **Context Inventory** sections (there are no per-step data flows to read from). Capability Domains do not exist in the Workflow Requirements — they are derived in Step 6.

**Step 4 (Autonomy Assessment):** State as fact: "This is an outcome-driven workflow — autonomy is **Autonomous** by definition. The agent system determines its own execution path."

**Step 5 (Orchestration Mechanism):** State as fact: "Orchestration is **Agent**." Still determine the involvement mode (Augmented/Automated) from the definition's Human Gates section and trigger type. Still ask the platform sub-choice if the platform has multiple agent offerings.

**On Claude Code/Cowork, "Agent" mechanism does NOT mean "build an orchestrator agent file."** It means the workflow is driven by an agentic loop — and that loop is the **primary session**. The artifacts you produce are the orchestration logic (command/`CLAUDE.md` run section) plus the **sub-agent(s)** the primary loop dispatches (see "Who is the orchestrator?" in Step 5). Carry this into Capability Domain Mapping and Agent Configuration below.

**Step 6 (Classify Each Step) → Capability Domain Mapping:** Replace per-step classification with capability domain mapping.

**Important:** Capability Domains are derived by Design — they are **not** captured in the Workflow Requirements (the Workflow Requirements stays in "what" territory; capability decomposition is "how"). Infer capability domains from the Workflow Requirements' Outcome, Inputs, Rules & Constraints, and Acceptance Criteria. Propose them to the user and confirm before mapping.

For each derived capability domain:

| Domain | Integration Needs | Intelligence Requirements | Reusable Skill? |
|--------|-------------------|--------------------------|-----------------|
| [domain] | Tools/connectors needed | Model class, context sources | Yes/No + rationale |

Same Integration Discovery and Skill Discovery processes apply, operating on capability domains instead of steps.

**Step 7 (Skill Candidates):** Same field structure — identify which capability domains should become skills. Each skill candidate uses the full 12-field Skill Candidate block (with Covers Domains in place of Covers Steps).

**Step 8 (Agent Configuration):** This is usually the primary blueprint section. Agent Configuration documents the **sub-agent(s) the orchestrator dispatches** — the workers — using all 13 standard fields, drawing Description, Mission, Responsibilities, Output Format, and Constraints from the Workflow Requirements' Outcome, Rules & Constraints, and Acceptance Criteria.

**Mandatory-but-with-an-exception:** document at least one agent **whenever the design includes a sub-agent/agent artifact** (the common case). A valid outcome-driven design on a primary-loop platform (Claude Code/Cowork) may have **zero sub-agents** — just orchestration logic (command/`CLAUDE.md` run section) + skills. In that case record `agents: 0` in the frontmatter counts and document the orchestration logic in the Deployment Plan / Orchestrator notes instead — **do not invent a sub-agent to satisfy the field.** Never document the orchestrator (the primary loop) as an agent artifact.

**Step 8b (Verify Evaluation Inputs):** Same as step-decomposed — confirm Acceptance Criteria and Example Scenarios in the Workflow Requirements are complete; do not duplicate.

**Step 9 (Generate Spec):** Use the modified template sections below. The spec uses the same filename pattern and same frontmatter shape (with `definition_type: Outcome-Driven`). The Step-by-Step Decomposition section is replaced with Capability Domain Mapping; the Autonomy Spectrum Summary becomes a brief Autonomous statement; Build Output is captured per domain rather than per step.

**Outcome-driven spec template modifications:**

Replace the `## Step-by-Step Decomposition` section with:

```markdown
## Capability Domain Mapping

(Capability domains are derived by Design from the Workflow Requirements' Outcome, Inputs, Rules, and Acceptance Criteria. They are not present in the Workflow Requirements.)

| Domain | Description | Integration (use/build) | Intelligence | Build Output |
|--------|-------------|------------------------|--------------|--------------|

**Build Output values:** Same canonical forms as the step-decomposed table (`New skill: SN`, `Use existing: [name]`, `New agent: AN`, etc.). For outcome-driven workflows, expect most domains to map to either `New skill: SN` (the orchestrator/sub-agent delegates to a reusable skill) or `Handled by orchestrator` (the orchestrating primary loop — or a deployed agent on SDK platforms — handles the domain inline via its own instructions; legacy synonym: `Handled by agent`).

### Autonomy Statement

This is an outcome-driven workflow. Autonomy is Autonomous — the agent system determines its own execution path based on the Outcome, Inputs, Rules & Constraints, and Acceptance Criteria defined in the Workflow Requirements.
```

Skill Candidates use the same 12-field block (with `Covers Domains` instead of `Covers Steps`). Agent Configuration documents the **sub-agent(s) the orchestrator dispatches** and is included whenever the design has ≥1 sub-agent (the common case). A primary-loop design with **zero sub-agents** (orchestration logic + skills only) is valid: set `agents: 0` and document the orchestration logic in the Deployment Plan instead. Never document the primary-loop orchestrator as an agent artifact.

**Build Skill Needs Checklist modifications for outcome-driven:**

Use the full step-decomposed checklist with these substitutions:
- Replace "Step-by-Step Decomposition" with "Capability Domain Mapping"
- Replace "Step IDs match Workflow Requirements Step IDs" with "Capability Domains are derived from Workflow Requirements (not restated from a section that doesn't exist there)"
- Replace "Inline prompt → Workflow Requirements Step N" Build Output value with "Handled by orchestrator" (accept legacy "Handled by agent" as a synonym)
- Agent Configuration is included whenever ≥1 sub-agent is defined; a zero-sub-agent design (orchestration logic + skills only) is valid with `agents: 0`. Never document the primary-loop orchestrator as an agent.

All other checklist items apply unchanged.

## Outputs

### `outputs/[workflow-name]-design-spec.md` — Design Spec

Uses the mandatory template defined in Step 9. The Design Spec **references** the Workflow Requirements as canonical source — it does not restate Outcome, Metadata, Context Inventory, Acceptance Criteria, Example Scenarios, Human Gates, Steps Overview, or per-step requirements.

The spec opens with YAML frontmatter (workflow, requirements_file, spec_version, definition_type, mechanism, involvement, platform, platform_mode, packaging, counts) so Build and downstream skills can summarize the spec without parsing prose.

The spec is organized into three layered groups:

- **Layer 1 — Architecture:** Execution Pattern, Architecture Decisions (with Packaging), Autonomy Spectrum Summary, Integration Options (with Source URLs), Model Recommendation (with per-platform mapping)
- **Layer 2 — Decomposition:** Step-by-Step Decomposition (with Build Output column) — or Capability Domain Mapping for outcome-driven — Orchestrator Prompt Outline (when mechanism is Prompt or Skill-Powered Prompt), Data Readiness Summary, Recommended Implementation Order
- **Layer 3 — Component Blueprints:** Skill Candidates (12 fields each), Agent Configuration (included whenever ≥1 sub-agent is defined — the common case for Agent/outcome-driven; documents the worker sub-agent(s), never the primary-loop orchestrator; 13 fields each), Multi-Agent Configuration (when applicable), Prerequisites, Deployment Plan

**Cross-layer sections:** Evaluation Inputs (pointer to Workflow Requirements), Deferred to Build, Stakeholders (optional), Self-Test Summary (results of the Build Skill Needs Checklist).

For outcome-driven workflows: Step-by-Step Decomposition is replaced by Capability Domain Mapping; Autonomy Spectrum Summary is replaced by an Autonomy Statement; Orchestrator Prompt Outline is omitted (on Claude Code/Cowork the **primary loop is the orchestrator** — captured as orchestration logic, not an agent file); Agent Configuration documents the worker sub-agent(s) and is included whenever ≥1 is defined (a zero-sub-agent design — orchestration logic + skills only — is valid with `agents: 0`).

## Guidelines

- Use plain language; avoid jargon unless the user introduced it
- After writing the spec, tell the user: "Design Spec saved to `outputs/[name]-design-spec.md`. Read it alongside the Workflow Requirements at `outputs/[name]-requirements.md`."
- Do not proceed past the Spec Approval Gate (Step 10) without explicit user approval
- Do not research integration availability — that happens in the Build phase
- Do not generate platform artifacts — that happens in the Build phase
- Do not restate Workflow Requirements content in the Design Spec — reference the file
