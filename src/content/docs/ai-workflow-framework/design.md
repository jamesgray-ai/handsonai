---
title: Design Your AI Workflow
description: Take your Workflow Requirements and design the AI architecture — three layers of decisions (Architecture, Decomposition, Component Blueprints) produced as a platform-agnostic Design Spec that any model on any platform can build from.
---

> **Part of:** [AI Workflow Framework](../)

:::tip[New to the building blocks?]
See the [Agentic Building Blocks](../../agentic-building-blocks/) reference for definitions, examples, and cross-platform comparisons of all blocks.
:::

## What This Is

The Design phase is where you decide *how* your workflow should be built — before you build it. You take the **Workflow Requirements** from the [Deconstruct step](../deconstruct/) (the *what*) and produce a **Design Spec** (the *how*) — the architectural blueprint Build consumes to generate skills, agents, and prompts.

The Workflow Requirements is the canonical source of truth. The Design Spec references it, never restates it. Build reads both together.

### Design has three layers

Design walks through three layers of decisions that build on each other. Each layer is approved before the next begins, so strategic errors get caught before you've invested time in detailed specs:

| Layer | What it decides | Why it's separate |
|---|---|---|
| **Layer 1 — Architecture** | Platform, mechanism (Prompt/Skill-Powered Workflow/Agent), autonomy level, packaging, model class, integration options | Strategic. Cheap to revisit. Wrong call here cascades everywhere. |
| **Layer 2 — Decomposition** | For each step (or capability domain), what AI building block delivers it: a new skill, an existing skill, an inline prompt block, an agent, or a human action | Structural. Decides what gets built and what gets reused. |
| **Layer 3 — Component Blueprints** | Field-level specs for each new skill and agent — name, description, inputs/outputs, decision logic, failure modes, tools, deployment | Detailed. Most expensive to redo. Build uses these to generate artifacts. |

The Design skill walks you through these layers in order, with a lightweight confirmation moment between each. The final Spec Approval Gate at the end is the only hard gate.

| | |
|---|---|
| **What you'll do** | Confirm your platform, work through three layers of design decisions with lightweight confirmation at each handoff, and approve the final spec |
| **What you'll get** | A **Design Spec** — three-layer architecture and component blueprints, with frontmatter, stable IDs, and a Self-Test Summary |
| **Time** | ~15–25 minutes |

:::note[Three terms you'll see, in plain language]
- **Frontmatter** — a small block of labeled facts at the top of the file (workflow name, mechanism, counts). It lets the next step read the headline decisions without re-reading the whole document.
- **Stable IDs** — short labels like S1 (skill), A1 (agent), C1 (context item), E1 (test scenario) that stay the same across documents, so every step can point at exactly the same component.
- **agentskills.io** — the open standard format for skills that every major AI platform now reads, which is what makes your design portable between platforms.
:::

## Why This Matters

Not every workflow needs the same level of AI infrastructure. A weekly status report might need a single well-crafted prompt. A multi-department content pipeline might need specialized agents coordinating across stages. Choosing the wrong mechanism means either over-engineering (building agents when a prompt would do) or under-building (forcing a prompt to do agent-level work).

Design also makes the workflow **portable**. Because the Design Spec follows the agentskills.io standard and uses stable IDs for every component, the same spec can be built on Claude Code, Claude.ai, Cowork, Codex, ChatGPT, or Gemini CLI — with only the platform-specific bits (Packaging, Deployment Plan) adjusted at the handoff.

:::note[Framework vs. platform — by design]
This framework guides you through *which decisions to make* and *what building blocks to design* — it is platform-agnostic. The AI model provides the platform-specific expertise: it researches your chosen platform's current tools, SDKs, and best practices at runtime via web search. This separation ensures the framework stays current as platforms evolve.
:::

---

## Layer 1 — Architecture

Strategic decisions that shape everything downstream. You start here.

### Architecture Approach

| Approach | What it means | Build in |
|----------|---------------|----------|
| **No-code** | Build entirely in a platform's UI — projects, workspace agents, gems, notebooks | Claude Projects, ChatGPT Workspace Agents, Gemini Gems, M365 Copilot |
| **Code-first** | Build with APIs and SDKs — programmatic model access, code-based agents, version-controlled workflows | Claude Agent SDK, OpenAI Agents SDK, Google ADK, LangChain, etc. |

The model analyzes your workflow and recommends an approach based on signals like integration needs, deployment scale, and developer experience. Most workflows start no-code and graduate to code-first when scale or integration demands it.

### Platform decision

You name your AI platform — at whatever level of specificity you have. "Claude Code," "ChatGPT," "Google Gemini," "Claude" are all fine. The ecosystem is enough for Design decisions; the specific offering (Claude Code vs. Claude.ai vs. Cowork) is resolved when Build generates artifacts.

### Other Architecture Decisions extracted from the Workflow Requirements

Rather than walking through a checklist, the Design skill uses an **extract-then-confirm** approach: ask one question (platform), extract everything else from the Workflow Requirements, present the analysis for confirmation.

- **Tool integrations** — pulled from per-step Inputs, Context Needed, and the Context Inventory
- **Trigger/schedule** — pulled from the Metadata table; time-based triggers imply scheduled execution
- **Context readiness flags** — pulled from the Context Inventory's AI Accessible column; flags items needing resolution before Build

### Autonomy Assessment

Where the *whole workflow* sits on the autonomy spectrum:

```
Human ———— Deterministic ———————— Guided ———————— Autonomous
(human-performed)  (fixed path)       (bounded decisions)     (context-driven path)
```

| Level | Signals | Orchestration implications |
|-------|---------|--------------------------|
| **Human** | Step requires human judgment, creativity, or physical action; AI cannot perform | No AI artifact — captured as Human step in the Decomposition table |
| **Deterministic** | Steps execute in fixed order, no branching on quality, failure = stop or retry | Prompt or Skill-Powered Workflow likely sufficient |
| **Guided** | Bounded AI judgment at steps, human steers at checkpoints, mostly fixed sequence | Skill-Powered Workflow or Agent |
| **Autonomous** | Executor backtracks, re-invokes, adjusts on failure, checkpoints can redirect | Agent required |

### Orchestration Mechanism

Based on the autonomy assessment and architecture decisions, the model recommends who drives the workflow:

| Mechanism | Description | Signals |
|-----------|-------------|---------|
| **Prompt** | Human follows structured instructions step by step, all logic inline | Sequential steps, human provides inputs and makes decisions |
| **Skill-Powered Workflow** | Human invokes reusable skills in a defined sequence | Repeatable sub-routines, moderate complexity |
| **Agent** | Agent orchestrates the flow, invoking skills and making sequencing decisions | Tool use required, autonomous decisions, multi-step reasoning |

Plus an involvement mode:

| Mode | Description | Determined by |
|------|-------------|---------------|
| **Augmented** | Human in the loop — reviews, steers, or decides at key points during the run | Web/desktop deployment, no scheduled execution |
| **Automated** | AI runs solo — executes end-to-end without human involvement | Scheduled/unattended execution, CLI |

### Packaging

How the artifacts ship together:

| Value | When to use |
|---|---|
| **Plugin** | Multiple related artifacts shipped together as a marketplace plugin (e.g., handsonai-plugins layout) |
| **Standalone Skill** | A single skill, uploaded directly (zip for Claude.ai, single SKILL.md for code-mode platforms, single skill for ChatGPT) |
| **Workspace Agent** | A ChatGPT Workspace Agent bundling orchestration + skills + tools (the current ChatGPT primitive; Custom GPTs are deprecated) |
| **Loose Files** | Individual files in a project directory, no distribution wrapper |

### Model Recommendation

A capability tier (reasoning-heavy / balanced / fast / vision) with per-step overrides if needed. The spec records only the tier — Build resolves the concrete model name for the target platform via web search at generation time, so specs never carry model IDs that go stale.

### Integration Options

For each tool the workflow needs, the model researches available integration options — curated MCP servers, APIs, SDKs, and CLIs — with source URLs and trade-offs. The output is platform-agnostic; Build does the per-platform setup research.

### Safety & Permissions

Before Layer 1 closes, the design answers four questions in plain language — they matter most for workflows that write to live systems, run unattended, or process content you didn't author:

1. **Write access** — Which connected tools can this workflow create, modify, or send through? Apply least privilege: only the scopes it needs, and prefer draft-don't-send until trust is established.
2. **Untrusted input** — Does any step process content you didn't author (inbound email, web pages, form submissions)? That content must be treated as data, never as instructions — this is how prompt-injection incidents happen.
3. **Unattended runs** — Scheduled or headless? Then human gates on outward-facing actions, a cap on actions per run, and a log of every write.
4. **Blast radius** — What's the worst realistic outcome of a bad run? Put a human gate in front of that action.

The answers and mitigations are recorded in the spec's Safety & Permissions section; Build enforces them during connector setup, and Run re-verifies them before the first scheduled run. For a read-only, human-triggered workflow this is one sentence, not a hurdle.

**End of Layer 1.** Lightweight confirmation: "Architecture confirmed: [summary]. Moving to Decomposition. Confirm to proceed."

---

## Layer 2 — Decomposition

For each step (or capability domain), decide which AI building block delivers it.

### Step-by-Step Decomposition

Steps are defined in the Workflow Requirements. This table adds the building-block classification and the concrete Build output for each:

| Column | Values |
|---|---|
| **Step** | Step ID from Workflow Requirements |
| **Autonomy** | Human / Deterministic / Guided / Autonomous |
| **Orchestration** | Prompt / Skill / Agent |
| **Integration** | Block + tool + use/build tag (e.g., "MCP: HubSpot (use)") |
| **Intelligence** | Model class + context source IDs + memory flag |
| **Build Output** | One of: `New skill: S1` / `Use existing: [name]` / `New agent: A1` / `Inline prompt → Workflow Requirements Step N` / `MCP server: [name]` / `Human (no artifact)` |
| **Human Gate?** | Yes / No (from Workflow Requirements Human Gates) |

For goal-driven workflows, this is replaced by a **Capability Domain Mapping** — capability domains are derived during Design (not present in the Workflow Requirements). A capability domain is a *durable competency the agent draws on* (e.g., "research," "synthesis") — **not** a step or pipeline stage. Collapse parallel applications of one competency into a single domain (expressed as a fan-out rather than duplicate rows), and treat domains as *capabilities available to the orchestrator at runtime*, not a fixed path. Each maps to integration needs, intelligence requirements, and a Build Output.

### Orchestrator Prompt Outline

When mechanism is `Prompt` or `Skill-Powered Workflow`, the spec includes an **Orchestrator Prompt Outline** — the structural skeleton of the workflow's main prompt. It names which step invokes which skill, where PAUSE points sit (from Human Gates), and what the user provides at each gate. Build expands the outline into the full orchestrator using Step Details from the Workflow Requirements.

Omitted for `Agent` mechanism — the agent itself is the orchestrator (see Agent Configuration in Layer 3).

### Data Readiness Summary

Context items from the Workflow Requirements' Context Inventory flagged as `Partial` or `No` for AI Accessible — with the action needed to make each one accessible before Build runs.

### Recommended Implementation Order

Quick Wins → Core → Future Enhancement. Within each tier, dependencies follow the `Depends On` field of each skill.

**End of Layer 2.** Lightweight confirmation: "Decomposition confirmed: [counts]. Moving to Component Blueprints. Confirm to proceed."

---

## Layer 3 — Component Blueprints

Field-level specs Build uses to generate each new skill and agent.

### Skill Candidates (12 fields)

For each step tagged `New skill: SN`:

| Field | Purpose |
|---|---|
| ID, Name, Description | Identity. Name must be lowercase-hyphenated, ≤64 chars, and capability-named (gerund/verb-object like `summarizing-transcripts`, never workflow-coupled — only the orchestrator skill takes the workflow name). Description must start with "This skill should be used when...", be ≤1024 chars, be written in third person, and name concrete trigger keywords — this is the verbatim text that goes into the SKILL.md frontmatter and drives auto-activation. |
| Purpose, Covers Steps/Domains | Internal context for spec readers |
| Inputs, Outputs | The skill's contract |
| Decision Logic, Failure Modes | What the skill does and how it handles edge cases |
| Required Tools, Depends On | Runtime dependencies on tools and other skills |
| Stateful? | Memory building-block flag |

### Agent Configuration (14 fields, mandatory when mechanism = Agent)

For each step tagged `New agent: AN`:

| Field | Purpose |
|---|---|
| ID, Name, Description | Identity. Description must start with "Use this agent when..." and is the verbatim text for the agent file frontmatter. |
| Mission, Responsibilities, Output Format, Tone & Style, Constraints | The agent's behavior — decomposed into structured sub-fields, not jammed into a single "Instructions" cell. For orchestrator-dispatched workers, Output Format is the handoff contract; for Autonomous agents, Constraints includes an iterations-per-run bound. |
| Failure Modes | Condition → action, one per line — including what the agent returns to its orchestrator when it cannot complete (mirrors the skill blueprint field) |
| Model, Memory Scope | Capability and persistence. Memory defaults to `none`; use it only for genuine cross-run state (tracking an entity, learned preferences), and avoid it for research/freshness workflows where stale recall misleads — prefer a curated context file when the learning should stay human-visible. |
| Tools, Skills | Cross-references to Integration Options entries and Skill IDs. Tools follow least privilege — only what the Responsibilities require. |
| Trigger Examples | 2-3 structured examples (context → user message → expected behavior → invocation) Build uses verbatim to construct `<example>` blocks in the agent's description |

### Multi-Agent Configuration

When more than one agent is defined, this section captures the orchestration pattern (Supervisor / Pipeline / Parallel / Network), the coordinator, the Handoff Contracts table (data passed between agents), and the Aggregation Strategy.

### Prerequisites and Deployment Plan

Prerequisites lists platform setup, accounts, credentials, and plugin installs needed before the workflow can run. The Deployment Plan documents where each artifact lives and how it gets deployed — with a Packaging note explaining how artifacts ship together.

**End of Layer 3.** Final Spec Approval Gate — the only hard gate. Review the full spec; approve to move to [Build](../build/).

---

## Cross-Layer Sections

These sections sit outside the three layers:

- **Evaluation Inputs** — pointer to the Workflow Requirements' Acceptance Criteria and Example Scenarios (not duplicated). Step 5 (Test) reads them from the Workflow Requirements directly.
- **Deferred to Build** — explicit list of decisions intentionally left for Build (specific platform offering, exact model version, integration setup specifics)
- **Stakeholders** (optional, organizational lens) — role swimlane and stakeholder details
- **Self-Test Summary** — populated by the Design skill after running the Build Skill Needs Checklist; each item ✓ (passed) or ⚠️ (issue described inline). Lets you see what was verified before approving.

---

## How the Skill Works

The three layers above are the conceptual structure of the Design Spec. In practice, the skill walks them in this chronological order:

1. **Load Workflow Requirements** — Read the Workflow Requirements file from `outputs/`.
2. **Confirm understanding** — Summarize the workflow and ask you to confirm.
3. **Architecture decisions (Layer 1)** — Confirm platform (the one question), then extract tool integrations, trigger/schedule, and constraints from the Workflow Requirements and present a confirmation block.
4. **Autonomy assessment** — Assess where the whole workflow sits on the autonomy spectrum (Deterministic, Guided, Autonomous).
5. **Orchestration mechanism** — Recommend a mechanism (Prompt, Skill-Powered Workflow, or Agent) with an involvement mode (Augmented or Automated).
6. **Classify each step (Layer 2)** — Per-step autonomy level, AI building blocks, tools, human review gates.
7. **Identify skill candidates** — Steps tagged for skill creation with generation-ready detail.
8. **Agent configuration (Layer 3)** — When applicable, generate a platform-agnostic agent blueprint.
9. **Generate Design Spec** — Write the complete design document.
10. **Spec Approval Gate** — Present the spec for approval. No artifacts are generated until you confirm.

## How to Use This

This step is facilitated by the **`design`** AI Workflow Framework skill. How you get it depends on your platform — see [Set Up the Skills](../skills/) for installation.

**How to start:** Say *"run the design skill"* (or *"design the workflow"*) — works on every platform. On Claude Code or Cowork with the plugin installed, you can also type `/handsonai:design`.

**Platform compatibility:** Claude Code ✓ &nbsp;|&nbsp; Claude.ai ✓ &nbsp;|&nbsp; Claude Cowork ✓ &nbsp;|&nbsp; ChatGPT ✓ &nbsp;|&nbsp; Gemini ✓ &nbsp;|&nbsp; M365 Copilot ✓ &nbsp;|&nbsp; Cursor / Codex / Antigravity ✓

**Start with this prompt:**

```
Design the AI workflow from my Workflow Requirements.
Assess the autonomy level, recommend an orchestration mechanism, and map building blocks.
```

Upload or paste your Workflow Requirements file (`[workflow-name]/requirements.md`) from the Deconstruct step. The skill runs the three layers in order, with lightweight confirmation between each, and produces a Design Spec.

### Example prompts

```
"Design the AI workflow from my Workflow Requirements"
→ Reads the most recent Workflow Requirements, runs Design,
  produces the Design Spec for approval

"Design the expense-reporting workflow"
→ Reads outputs/expense-reporting-requirements.md, recommends
  an orchestration mechanism, and generates the spec
```

:::tip[If your AI tool doesn't support skills]
Download the skill file from [GitHub](https://github.com/jamesgray-ai/handsonai-plugins/tree/main/plugins/handsonai/skills/design) and paste it into your system prompt or project instructions. Or use this page as a conversation guide.
:::

### Plan mode and the three layers

The Design skill works best in plan mode. The layered flow maps naturally onto how you'll work with the model:

| Layer | Mode |
|---|---|
| **L1 Architecture** | Conversational — discuss platform, mechanism, packaging. Quick back-and-forth. |
| **L2 Decomposition** | The natural plan-mode entry point — start planning here. The model classifies each step and proposes Build Outputs. |
| **L3 Component Blueprints** | Stays in plan mode — detailed field-level spec generation. |

**How to activate plan mode on your platform:**

| Platform | How to activate plan mode |
|---|---|
| **Claude Code** | Press `Shift+Tab` twice, or type `/plan` |
| **Cursor** | Select "Plan" in the composer mode |
| **Codex CLI** | Run with the `--plan` flag |
| **Other AI tools** | Ask the model: *"Switch to plan mode. Walk me through Layers 2 and 3 of the Design — classify each step, identify skill candidates, write the component blueprints."* |

After the model produces the spec, **review and approve at the Spec Approval Gate** before moving to Build. In plan mode the spec is carried in the harness plan file and approved through the plan-approval dialog — the model also shows the full spec in the conversation so you can read it. If you don't see it, just ask the model to paste the spec inline.

---

## What This Produces

The **Design Spec** is organized into the three layers above, plus cross-layer sections. The spec opens with YAML frontmatter so Build can summarize it in one read.

**Before Layer 1:** Source, then **Value & Measurement** — carried forward from the Workflow Requirements so the spec says what the workflow is for without a second file.

**Layer 1 — Architecture sections:** Execution Pattern, Architecture Decisions (with Packaging), Autonomy Spectrum Summary, Safety & Permissions (including **Constraint Conformance**), Integration Options (with Source URLs), Model Recommendation (with per-platform mapping).

**Layer 2 — Decomposition sections:** Step-by-Step Decomposition (or Capability Domain Mapping for goal-driven), Orchestrator Prompt Outline (when mechanism is Prompt or Skill-Powered Workflow), Data Readiness Summary, Recommended Implementation Order.

**Layer 3 — Component Blueprint sections:** Skill Candidates (12 fields each), Agent Configuration (14 fields each; mandatory for goal-driven), Multi-Agent Configuration (when applicable), Prerequisites, Deployment Plan.

**Cross-layer sections:** Evaluation Inputs (pointer), Deferred to Build, Stakeholders (optional), Self-Test Summary (verification results).

### Two sections worth reading closely

**Value & Measurement** is copied forward from the Workflow Requirements unchanged — the objective, the outcome, the metric, today's number, and the target. Design does not re-open those questions; it carries them so that whoever reads the spec on its own can still see what the build is for and how it will be judged. If today's number was never established, the spec says so in those words rather than quietly dropping the row.

**Constraint Conformance** is the section that makes the protections from Deconstruct real. Design walks each one and records where the architecture satisfies it, in a small table with one of three states:

- **Satisfied** — the design meets the constraint, and the row names how: which gate, which permission, which boundary.
- **Accepted** — the constraint cannot be met as stated, and someone with the authority to say so has accepted the difference. The row names who accepted it.
- **Open** — nothing in the design meets it yet.

An `Open` row is not a failure of the spec; it is the spec being honest. But it does not survive into a build: the design is not finished while one is outstanding, and Build reads them. A constraint that everyone assumed was handled, and that no document ever claimed was handled, is the one that fails in production.

Requirements written before this section existed simply have nothing to reconcile. Design notices that, fills in what it can infer from the architecture, and asks about the rest rather than declaring the workflow constraint-free by default.

Build reads both the Design Spec and the Workflow Requirements together — the Design Spec is the architectural blueprint; the Workflow Requirements remains the canonical source for per-step content, acceptance criteria, and human gates.

---

## Consuming the Design Spec

The Design Spec is structured for machine consumption — by the Build skill, by other AI agents, or by engineers building tooling around the spec.

### Schema

| Element | Format |
|---|---|
| **Frontmatter** | YAML. Required fields: `workflow`, `requirements_file`, `spec_version`, `definition_type`, `mechanism`, `involvement`, `platform`, `platform_mode`, `packaging`, `counts` |
| **Stable IDs** | `S1`, `S2`, … for skills; `A1`, `A2`, … for agents; `C1`, `C2`, … for context items (in the Workflow Requirements); `E1`, `E2`, … for example scenarios (in the Workflow Requirements) |
| **Canonical vocabulary** | Autonomy: `Human / Deterministic / Guided / Autonomous`. Mechanism: `Prompt / Skill-Powered Workflow / Agent`. Packaging: `Plugin / Standalone Skill / Workspace Agent / Loose Files`. Build Output: `New skill: SN / Use existing: [name] / New agent: AN / Inline prompt → Workflow Requirements Step N / MCP server: [name] / Human (no artifact)` |
| **Section ordering** | Layer 1 → Layer 2 → Layer 3 → Cross-layer. Section names within each layer are fixed (consumers can locate any section by name). |
| **Self-Test Summary** | Each Build Skill Needs Checklist item marked ✓ or ⚠️ with inline description. Lets consumers see what was verified. |

### Consuming the spec standalone (without the Build skill)

A capable agent (Claude Code, Codex, ChatGPT with skill support, Gemini CLI) can build the artifacts from the Design Spec alone, given access to:

1. **The Workflow Requirements file** — referenced from frontmatter `requirements_file:`
2. **The agentskills.io specification** — the open standard skill format ([agentskills.io/specification](https://agentskills.io/specification))
3. **The target platform's agent format docs** — Claude Code's [sub-agents docs](https://code.claude.com/docs/en/sub-agents), Codex's [subagents docs](https://developers.openai.com/codex/subagents), or equivalent

For best results, run Build via the framework's Build skill — it auto-resolves these via the platform registry and handles deployment.

### Cross-platform portability

The Design Spec is portable across platforms because every major platform (Claude Code, Claude.ai, Cowork, Codex, ChatGPT, Gemini CLI) now follows the agentskills.io standard for skills. Three practical workflows:

1. **Same platform throughout** (most common) — Design on Claude Code → Build on Claude Code. Platform in the spec matches Build's runtime platform.
2. **Design once, Build elsewhere** — Skill Candidates and Agent Configuration carry over unchanged because they're agentskills.io-compatible. Update Architecture Decisions (Platform, Packaging) and Deployment Plan when moving. Example: design on Claude Code at home, build on Codex at work.
3. **Plan for a different target platform** — Design on Claude Code targeting ChatGPT Workspace Agents (or any other platform). Build resolves the platform-specific translation at generation time.

**agentskills.io is the portability layer.** Every major platform converges on the standard, so Skill Candidates from one platform's Design Spec build cleanly on another with minimal rewriting.

---

## Related

- **Previous step:** [Deconstruct Workflows](../deconstruct/) (Step 2) — produces the Workflow Requirements that Design consumes
- **Next step:** [Build the Workflow](../build/) (Step 4) — generates platform artifacts from the Design Spec
- [AI Workflow Framework](../) — the full seven-step methodology
- [Workflow Design Matrix](../workflow-design-matrix/) — how autonomy and involvement combine into six workflow archetypes
- [Workflow Architecture Patterns](../../patterns/workflow-architecture/) — implementation blueprints (prompt chaining, routing, orchestrator-workers, evaluator-optimizer, autonomous agents)
- [Agents](../../agentic-building-blocks/agents/), [Skills](../../agentic-building-blocks/skills/), [Prompts](../../agentic-building-blocks/prompts/)
