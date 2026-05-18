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

**Plan Mode Prompt:** At the start of Design, prompt the user:

> "The Design phase is collaborative — we plan the architecture together before anything gets built. **Enter plan mode now** if your platform supports it (in Claude Code: `shift+tab` or `/plan`). This ensures we focus on design without accidentally generating artifacts. If plan mode isn't available, I'll collaborate through conversation — proposing, you reacting, iterating until you approve."

This is directive, not optional — plan mode is the preferred path for design collaboration.

#### Step 1 — Load Workflow Requirements

Read the Workflow Requirements from `outputs/[workflow-name]-requirements.md`. If the user specifies a file path, use that. Otherwise, look for the most recent Workflow Requirements in `outputs/`.

Read the `Definition Type` field from the Metadata table. If `Outcome-Driven`, use the outcome-driven processing path for all subsequent steps (see **Outcome-Driven Processing Path** below). If `Step-Decomposed` (or no Definition Type field is present), use the standard step-decomposed path.

#### Step 2 — Confirm Understanding

For step-decomposed requirements: Summarize the workflow name, step count, and outcome (from the Outcome section of the Workflow Requirements). Ask the user to confirm before proceeding.

For outcome-driven requirements: Summarize the workflow name, outcome, and the headline rules and constraints (from the Outcome and Rules & Constraints sections). Ask the user to confirm before proceeding.

#### Step 3 — Architecture Decisions

Before assessing autonomy and orchestration, gather the information needed to make platform-aware recommendations. The approach: **one question, then extract everything else from the Workflow Requirements.**

**a. One question: Platform**

Platform is the only thing not already in the Workflow Requirements. Determine the user's AI platform:
- If stated in conversation or definition, confirm: "You mentioned [platform] — is that still correct?"
- If not stated, ask. Let the user name their tool — do not present a fixed list.

Accept whatever level of specificity the user provides — "Claude Code", "Google Gemini", "ChatGPT", "Claude" are all fine. Do NOT try to disambiguate to a specific offering upfront. Instead:
- **For Design:** The ecosystem (Claude, Google, OpenAI, M365) is enough for pattern selection. Code-vs-nocode is inferred if the tool is specific (Claude Code = code, ChatGPT = no-code) or left open if vague.
- **For Orchestration Mechanism:** The recommendation is driven by workflow characteristics first (tool use? autonomous decisions? multiple domains?). If the recommended mechanism requires capabilities the named platform might or might not support (e.g., recommending an agent when "Google Gemini" could mean the web app or ADK), ask a **motivated follow-up** in context.
- **For Build:** The specific offering (Claude Code vs. Claude.ai, ADK vs. Gemini web) is resolved when generating artifacts in the Build phase — not during Design.

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

**Present as a confident assessment:** "This workflow is **[level]** because [1-2 sentence reasoning]." If the user disagrees, discuss and adjust.

#### Step 5 — Orchestration Mechanism

Based on the autonomy assessment and architecture decisions, recommend who drives the workflow and how humans are involved. Analyze internally and present a confident recommendation — do NOT walk through decision questions.

**Orchestration mechanism (who drives the workflow):**

| Mechanism | Description | Signals |
|-----------|-------------|---------|
| **Prompt** | Human follows structured instructions step by step, all logic inline | Sequential steps, human provides inputs and makes decisions |
| **Skill-Powered Prompt** | Human invokes reusable skills in a defined sequence | Repeatable sub-routines, moderate complexity, steps that recur across workflows |
| **Agent** | Agent orchestrates the flow, invoking skills and making sequencing decisions | Tool use required, autonomous decisions, multi-step reasoning |

Single-agent vs. multi-agent is an architecture detail decided during Agent Configuration (Step 8) if "Agent" is selected — not a top-level choice here.

**Human Involvement** — Determine the involvement mode from architecture decisions and include it in the recommendation:

| Mode | Description | Determined by |
|------|-------------|---------------|
| **Augmented** | Human is in the loop — reviews, steers, or decides at key points during the run. | Web/desktop deployment, no scheduled execution |
| **Automated** | AI runs solo — executes end-to-end without human involvement during the run. | Scheduled/unattended execution, CLI |

**Platform sub-choice for agent mechanism:** When the orchestration mechanism is Agent, the platform choice determines the implementation path. Some platforms have multiple agent offerings (e.g., Claude Code has sub-agents via markdown files vs. Claude Agent SDK in TypeScript/Python). If the platform has multiple agent offerings, ask the user which offering they want to use — this determines whether the Build phase generates markdown files, Python code, TypeScript code, or GUI configuration steps. For non-agent mechanisms (Prompt, Skill-Powered Prompt), no sub-choice is needed — artifacts are always markdown files.

**Present as a confident recommendation:** "Based on your workflow's **[autonomy level]** autonomy and [key architecture signals], I recommend **[mechanism]** with **[involvement mode]** because [2-3 sentence reasoning]." If the user pushes back, explain alternatives and discuss.

Ask the user to confirm the mechanism, involvement mode, and platform sub-choice (if applicable).

**Fast-track for complete Workflow Requirements:** If the Workflow Requirements + conversation context provide enough information to resolve ALL architecture dimensions, the autonomy level, AND the orchestration mechanism, present the entire Design analysis as a single confirmation block instead of stepping through questions one at a time.

**Packaging decision:** Before the Layer 1 confirmation, propose a Packaging value based on the platform and the workflow's shape (single skill → Standalone Skill; multiple related artifacts → Plugin; ChatGPT with agent + skills → Workspace Agent; ad-hoc files → Loose Files). The user confirms or overrides.

For step-decomposed workflows:

> "Based on your workflow definition, here's my design analysis:
> - **Platform:** [platform] ([surface])
> - **Packaging:** [packaging value] — [reason]
> - **Autonomy level:** [level] — [brief rationale]
> - **Orchestration mechanism:** [mechanism] ([involvement mode])
> - **Tools needed:** [list — availability to be researched during Build]
> - **Steps classified:** [summary table]
> - **Skill candidates:** [list]
> - **Agent blueprints:** [summary]
>
> Does this look right, or would you like to adjust anything?"

For outcome-driven workflows:

> "Based on your outcome-driven workflow definition, here's my design analysis:
> - **Platform:** [platform] ([surface])
> - **Packaging:** [packaging value] — [reason]
> - **Autonomy level:** Autonomous (by definition — agent determines its own execution path)
> - **Orchestration mechanism:** Agent ([involvement mode])
> - **Tools needed:** [list — availability to be researched during Build]
> - **Capability domains mapped:** [summary table]
> - **Skill candidates:** [list]
> - **Agent blueprint:** [summary]
>
> Does this look right, or would you like to adjust anything?"

Only drop into the question-by-question flow when genuinely missing information.

**Layer 1 confirmation moment** (after Step 5, before moving to Step 6):

The architecture work is complete. Before classifying each step, confirm the L1 decisions are right — catching strategic errors before investing in L2/L3 work:

> "Architecture confirmed:
> - **Platform:** [platform] ([surface])
> - **Mechanism:** [mechanism] ([involvement mode])
> - **Autonomy:** [level]
> - **Packaging:** [packaging value]
>
> Moving to Layer 2 — Decomposition. I'll classify each step and identify which building blocks deliver each one. Confirm to proceed, or push back on any of the above."

If the user pushes back, revise the relevant L1 decisions and re-confirm before proceeding. This is a lightweight confirmation, not a hard gate — but it's the cheapest moment to catch architecture mistakes.

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

#### Step 9 — Generate Design Spec

Write to `outputs/[workflow-name]-design-spec.md` using the template below. Every section is mandatory unless marked (optional). Do not add, remove, rename, or reorder sections.

**Generation order:**

1. Generate all spec sections (frontmatter through Stakeholders) following the template.
2. **Run the Build Skill Needs Checklist** (at the end of this step) to verify every required field is present and well-formed.
3. **Write the Self-Test Summary section** as the final section of the spec. For each checklist item, mark ✓ (passed) or ⚠️ (issue — describe inline). This makes the verification visible to the user and to downstream consumers.
4. If any checklist item failed (⚠️), fix the underlying section before writing the spec. The Self-Test Summary should ideally show all ✓ — but if a ⚠️ remains (e.g., a deliberate gap that the user accepted), it's surfaced honestly.

**Conditional sections to generate:**
- `Orchestrator Prompt Outline` — only when mechanism is `Prompt` or `Skill-Powered Prompt`. Omit for `Agent`.
- `Agent Configuration` — only when mechanism is `Agent`. (Mandatory for outcome-driven.)
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
- **Build Output**: One of: `New skill: S1` (build a new skill, defined below) / `Use existing: [name]` (reference an existing skill) / `New agent: A1` (build a new agent, defined below) / `Inline prompt → Workflow Requirements Step N` (this step becomes a prompt block in the orchestrator, sourced from the named step's requirements) / `MCP server: [name]` (configure a connector) / `Human (no artifact)` (no AI artifact — human-performed)
- **Human Gate?**: Yes / No (sourced from Workflow Requirements Human Gates table)

## Orchestrator Prompt Outline

*Include this section only when mechanism is `Prompt` or `Skill-Powered Prompt`. Omit for `Agent` (the agent IS the orchestrator — see Agent Configuration below).*

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

## Agent Configuration (mandatory when orchestration = Agent; otherwise omit)

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

**Orchestration Pattern:** Supervisor (one agent delegates to others) / Pipeline (agents in sequence) / Parallel (agents run concurrently) / Network (agents call each other peer-to-peer)

**Coordinator:** [Agent ID that coordinates, or "Pattern-based" if no single coordinator]

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
- ✓ / ⚠️ All Build Output values use canonical forms (`New skill: SN` / `Use existing: [name]` / `New agent: AN` / `Inline prompt → Workflow Requirements Step N` / `MCP server: [name]` / `Human (no artifact)`)
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
- [ ] Every Build Output value is one of the canonical forms (`New skill: SN`, `Use existing: [name]`, `New agent: AN`, `Inline prompt → Workflow Requirements Step N`, `MCP server: [name]`, `Human (no artifact)`)
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

#### Step 10 — Spec Approval Gate

**This is a hard gate. Do not proceed without explicit approval.**

Present a summary of the Design Spec:

> "Here's the Design Spec summary:
>
> - **Autonomy:** [level] (for outcome-driven: Autonomous)
> - **Mechanism:** [orchestration mechanism] ([involvement mode])
> - **Structure:** [count] steps, [count] skill candidates, [count] agents (for outcome-driven: [count] capability domains, [count] skill candidates, [count] agents)
> - **Integration options:** [count] tools with recommended integration approaches
> - **Implementation order:** [brief summary]
>
> The full spec is saved to `outputs/[workflow-name]-design-spec.md`.
>
> **Do you approve this spec?** I won't generate any artifacts until you confirm. If you want changes, tell me what to adjust and I'll revise."

Loop if the user requests changes — revise the spec and re-present for approval.

After the user approves, instruct them to **exit plan mode** if they entered it at the start of Design:

> "Spec approved. **Exit plan mode now** (in Claude Code: `shift+tab` or `/plan`) so artifacts can be generated in the Build phase."
>
> "To build the workflow, run the `build` skill (Step 4) (or say *'Build the workflow from my Design Spec'*)."

### Outcome-Driven Processing Path

When the Workflow Requirements has `Definition Type: Outcome-Driven`, the following modifications apply to the standard workflow:

**Step 3 (Architecture Decisions):** Same as standard, but the source sections differ. For outcome-driven Workflow Requirements, extract tools from the **Inputs**, **Rules & Constraints**, and **Context Inventory** sections (there are no per-step data flows to read from). Capability Domains do not exist in the Workflow Requirements — they are derived in Step 6.

**Step 4 (Autonomy Assessment):** State as fact: "This is an outcome-driven workflow — autonomy is **Autonomous** by definition. The agent system determines its own execution path."

**Step 5 (Orchestration Mechanism):** State as fact: "Orchestration is **Agent**." Still determine the involvement mode (Augmented/Automated) from the definition's Human Gates section and trigger type. Still ask the platform sub-choice if the platform has multiple agent offerings.

**Step 6 (Classify Each Step) → Capability Domain Mapping:** Replace per-step classification with capability domain mapping.

**Important:** Capability Domains are derived by Design — they are **not** captured in the Workflow Requirements (the Workflow Requirements stays in "what" territory; capability decomposition is "how"). Infer capability domains from the Workflow Requirements' Outcome, Inputs, Rules & Constraints, and Acceptance Criteria. Propose them to the user and confirm before mapping.

For each derived capability domain:

| Domain | Integration Needs | Intelligence Requirements | Reusable Skill? |
|--------|-------------------|--------------------------|-----------------|
| [domain] | Tools/connectors needed | Model class, context sources | Yes/No + rationale |

Same Integration Discovery and Skill Discovery processes apply, operating on capability domains instead of steps.

**Step 7 (Skill Candidates):** Same field structure — identify which capability domains should become skills. Each skill candidate uses the full 12-field Skill Candidate block (with Covers Domains in place of Covers Steps).

**Step 8 (Agent Configuration):** This becomes the primary section. Agent Configuration is **mandatory** (not optional) for outcome-driven workflows. Document the agent(s) with all 13 standard fields, drawing Description, Mission, Responsibilities, Output Format, and Constraints from the Workflow Requirements' Outcome, Rules & Constraints, and Acceptance Criteria.

**Step 8b (Verify Evaluation Inputs):** Same as step-decomposed — confirm Acceptance Criteria and Example Scenarios in the Workflow Requirements are complete; do not duplicate.

**Step 9 (Generate Spec):** Use the modified template sections below. The spec uses the same filename pattern and same frontmatter shape (with `definition_type: Outcome-Driven`). The Step-by-Step Decomposition section is replaced with Capability Domain Mapping; the Autonomy Spectrum Summary becomes a brief Autonomous statement; Build Output is captured per domain rather than per step.

**Outcome-driven spec template modifications:**

Replace the `## Step-by-Step Decomposition` section with:

```markdown
## Capability Domain Mapping

(Capability domains are derived by Design from the Workflow Requirements' Outcome, Inputs, Rules, and Acceptance Criteria. They are not present in the Workflow Requirements.)

| Domain | Description | Integration (use/build) | Intelligence | Build Output |
|--------|-------------|------------------------|--------------|--------------|

**Build Output values:** Same canonical forms as the step-decomposed table (`New skill: SN`, `Use existing: [name]`, `New agent: AN`, etc.). For outcome-driven workflows, expect most domains to map to either `New skill: SN` (if the agent should delegate to a reusable skill) or `Handled by agent` (if the agent handles the domain inline with its own instructions).

### Autonomy Statement

This is an outcome-driven workflow. Autonomy is Autonomous — the agent system determines its own execution path based on the Outcome, Inputs, Rules & Constraints, and Acceptance Criteria defined in the Workflow Requirements.
```

Skill Candidates use the same 12-field block (with `Covers Domains` instead of `Covers Steps`). Agent Configuration is **mandatory** for outcome-driven specs.

**Build Skill Needs Checklist modifications for outcome-driven:**

Use the full step-decomposed checklist with these substitutions:
- Replace "Step-by-Step Decomposition" with "Capability Domain Mapping"
- Replace "Step IDs match Workflow Requirements Step IDs" with "Capability Domains are derived from Workflow Requirements (not restated from a section that doesn't exist there)"
- Replace "Inline prompt → Workflow Requirements Step N" Build Output value with "Handled by agent"
- Agent Configuration is mandatory (not optional)

All other checklist items apply unchanged.

## Outputs

### `outputs/[workflow-name]-design-spec.md` — Design Spec

Uses the mandatory template defined in Step 9. The Design Spec **references** the Workflow Requirements as canonical source — it does not restate Outcome, Metadata, Context Inventory, Acceptance Criteria, Example Scenarios, Human Gates, Steps Overview, or per-step requirements.

The spec opens with YAML frontmatter (workflow, requirements_file, spec_version, definition_type, mechanism, involvement, platform, platform_mode, packaging, counts) so Build and downstream skills can summarize the spec without parsing prose.

The spec is organized into three layered groups:

- **Layer 1 — Architecture:** Execution Pattern, Architecture Decisions (with Packaging), Autonomy Spectrum Summary, Integration Options (with Source URLs), Model Recommendation (with per-platform mapping)
- **Layer 2 — Decomposition:** Step-by-Step Decomposition (with Build Output column) — or Capability Domain Mapping for outcome-driven — Orchestrator Prompt Outline (when mechanism is Prompt or Skill-Powered Prompt), Data Readiness Summary, Recommended Implementation Order
- **Layer 3 — Component Blueprints:** Skill Candidates (12 fields each), Agent Configuration (optional, mandatory for outcome-driven; 13 fields each), Multi-Agent Configuration (when applicable), Prerequisites, Deployment Plan

**Cross-layer sections:** Evaluation Inputs (pointer to Workflow Requirements), Deferred to Build, Stakeholders (optional), Self-Test Summary (results of the Build Skill Needs Checklist).

For outcome-driven workflows: Step-by-Step Decomposition is replaced by Capability Domain Mapping; Autonomy Spectrum Summary is replaced by an Autonomy Statement; Orchestrator Prompt Outline is omitted (the agent IS the orchestrator); Agent Configuration is mandatory.

## Guidelines

- Use plain language; avoid jargon unless the user introduced it
- After writing the spec, tell the user: "Design Spec saved to `outputs/[name]-design-spec.md`. Read it alongside the Workflow Requirements at `outputs/[name]-requirements.md`."
- Do not proceed past the Spec Approval Gate (Step 10) without explicit user approval
- Do not research integration availability — that happens in the Build phase
- Do not generate platform artifacts — that happens in the Build phase
- Do not restate Workflow Requirements content in the Design Spec — reference the file
