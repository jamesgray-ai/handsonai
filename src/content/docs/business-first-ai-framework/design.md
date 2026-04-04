---
title: Design Your AI Workflow
description: Gather architecture decisions, assess workflow autonomy level, choose an orchestration mechanism and involvement mode, classify steps on the autonomy spectrum, map AI building blocks, identify skill candidates, and document agent blueprints — producing a platform-agnostic AI Building Block Spec.
---> **Part of:** [Business-First AI Framework](index.md)

:::tip[New to the building blocks?]
See the [Agentic Building Blocks](../agentic-building-blocks/index.md) reference for definitions, examples, and cross-platform comparisons of all blocks.
:::
## What This Is

The Design phase is where you decide *how* your workflow should be built — before you build it. You take the Workflow Definition from the [Deconstruct step](deconstruct/index.md) and make design decisions. The Design skill supports both **step-decomposed** and **outcome-driven** Workflow Definitions:

**For step-decomposed definitions**, you make five design decisions:

1. **Architecture decisions** — What platform are you using, and what integrations and constraints does the Workflow Definition reveal?
2. **Autonomy assessment** — Where does the whole workflow sit on the autonomy spectrum (Deterministic → Guided → Autonomous)?
3. **Orchestration mechanism** — Who drives the workflow (Prompt, Skill-Powered Prompt, or Agent)?
4. **Autonomy classification** — How much AI assistance does each step need?
5. **Building block mapping** — What specific AI components does each step require?

**For outcome-driven definitions**, the flow is streamlined — autonomy (Autonomous) and orchestration (Agent) are pre-determined by definition. The Design phase focuses on:

1. **Architecture decisions** — Platform and tool integrations extracted from capability domains
2. **Involvement mode** — Augmented or Automated, determined from the definition's human gates and trigger type
3. **Capability domain mapping** — What integrations, intelligence, and reusable skills does each capability domain need?
4. **Agent configuration** — The primary design artifact: agent blueprints drawn from the definition's goal, constraints, and expected outputs
5. **Evaluation criteria** — Carried forward from the definition's quality criteria, with supplementary questions as needed

:::note[Framework vs. platform — by design]
This framework guides you through *which decisions to make* and *what building blocks to design* — it is platform-agnostic. The AI model provides the platform-specific expertise: it researches your chosen platform's current tools, SDKs, and best practices at runtime via web search. This separation ensures the framework stays current as platforms evolve, without requiring documentation updates every time a platform changes its offerings.
:::
| | |
|---|---|
| **What you'll do** | Upload your Workflow Definition, choose your architecture approach, confirm your platform, review the AI's autonomy assessment and orchestration mechanism recommendation, review step classifications, and adjust anything that doesn't look right |
| **What you'll get** | An **AI Building Block Spec** — architecture approach with rationale, architecture decisions, autonomy level assessment, orchestration mechanism with involvement mode, per-step autonomy classifications, building block mapping, skill candidates, agent blueprints (when applicable), and a prioritized build sequence |
| **Time** | ~15–25 minutes (architecture questions + reviewing the AI's analysis) |

## Why This Matters

Not every workflow needs the same level of AI infrastructure. A weekly status report might need a single well-crafted prompt. A multi-department content pipeline might need specialized agents coordinating across stages. Choosing the wrong orchestration mechanism means either over-engineering (building agents when a prompt would do) or under-building (forcing a prompt to do agent-level work).

Design also maps each step to specific **AI building blocks** — Prompt, Context, Skill, Agent, MCP, Project, API, or SDK — so you know exactly what to build. The recommended implementation order (quick wins first, complex agent steps last) gives you a practical sequence for rolling out AI incrementally.

## Architecture Approach

Before any other decisions, choose how you'll build your workflow. This is the first fork in the road — it shapes which platforms, tools, and building blocks are available to you.

| Approach | What it means | Build in |
|----------|---------------|----------|
| **No-code** | Build entirely in a platform's UI — projects, custom GPTs, gems, notebooks | Claude Projects, ChatGPT GPTs, Gemini Gems, M365 Copilot |
| **Code-first** | Build with APIs and SDKs — programmatic model access, code-based agents, version-controlled workflows | Claude Agent SDK, OpenAI Agents SDK, Google ADK, LangChain, etc. |

### Which approach fits?

The model analyzes your workflow and recommends an approach based on these signals:

| Signal | Points toward |
|--------|---------------|
| Need to integrate into an existing application | Code-first |
| Need CI/CD deployment or version control | Code-first |
| Need to process high volume or run at scale | Code-first |
| Non-developer or exploring AI for the first time | No-code |
| Prototyping before committing to production | No-code first, then code-first |
| Workflow runs inside a single AI platform | No-code |
| Workflow needs to orchestrate across multiple services | Code-first |

Most workflows start no-code. Code-first becomes the right choice when you need programmatic control, integration into existing systems, or production-grade deployment. The same three orchestration mechanisms (Prompt, Skill-Powered Prompt, Agent) apply to both approaches — the architecture approach determines *how* you implement them, not *what* you implement.

:::tip[You can switch later]
Many teams prototype no-code, validate the workflow works, then rebuild code-first for production. The AI Building Block Spec captures the design either way — only the Build step changes.
:::
## Architecture Decisions

Before assessing autonomy and choosing an orchestration mechanism, the model gathers the information that shapes platform-aware recommendations. Rather than walking through a checklist, it uses an **extract-then-confirm** approach: ask one question, extract everything else from your Workflow Definition, and present the analysis for confirmation.

**One question: Platform.** The only thing not already in your Workflow Definition is which AI platform you'll use. If you've already mentioned it in conversation, the model confirms. If not, it asks — and accepts whatever level of specificity you provide ("Claude Code", "ChatGPT", "Google Gemini", "Claude" are all fine). The model doesn't try to disambiguate to a specific offering upfront — the ecosystem is enough for Design decisions, and the specific tool is resolved during Build when generating artifacts.

**Everything else is extracted from the Workflow Definition:**

- **Tool integrations** — pulled from data flows, context needs, and step details across all steps. The model lists the tools identified but defers platform availability research to the Build step.
- **Trigger/schedule** — pulled from your Scenario Metadata. Time-based triggers are noted as scheduled execution requirements with implications for involvement mode and infrastructure.
- **Browser access** — if any step involves logging into a website, it's flagged during step classification rather than asked about separately. The connection details are handled during Build.
- **Shareability** — deferred to Build, where it determines artifact format (file-based vs. code-based). Not asked during Design.

Code comfort and deployment surface are inferred from the platform choice when specific (Claude Code = CLI + code-comfortable, ChatGPT = web + no-code) or resolved during Build when vague.

After extracting, the model presents a single confirmation block showing the platform, extracted tool integrations with availability mapping, trigger implications, and any flags — then asks if anything was missed or needs adjustment. The confirmed decisions gate all subsequent recommendations.

## Autonomy Assessment

Before choosing an orchestration mechanism, the model assesses where the *whole workflow* sits on the autonomy spectrum. This is the same spectrum used for per-step classification later — applied at the workflow level.

```
Deterministic ———————— Guided ———————— Autonomous
(fixed path)       (bounded decisions)     (context-driven path)
```

| Level | Signals | Orchestration implications |
|-------|---------|--------------------------|
| **Deterministic** | Steps always execute in the same order, no branching on output quality, failure = stop or retry same step | Prompt or skill-powered prompt likely sufficient |
| **Guided** | Some steps involve bounded AI judgment, human steers at checkpoints, sequence is mostly fixed but with bounded flexibility | Skill-powered prompt or agent |
| **Autonomous** | Executor backtracks, re-invokes based on feedback, adjusts approach on failure, human checkpoints can redirect flow | Agent required |

The model presents this as a confident assessment — for example: *"This workflow is **Guided** because most steps follow a fixed sequence, but the research step involves bounded judgment about which sources to pursue."* If you disagree, you discuss and adjust.

## Orchestration Mechanism

Based on the autonomy assessment and architecture decisions, the model recommends who drives the workflow. The orchestration mechanism answers: **who follows the steps?**

| Mechanism | Description | Signals |
|-----------|-------------|---------|
| **Prompt** | Human follows structured instructions step by step, all logic inline | Sequential steps, human provides inputs and makes decisions |
| **Skill-Powered Prompt** | Human invokes reusable skills in a defined sequence | Repeatable sub-routines, moderate complexity, steps that recur across workflows |
| **Agent** | Agent orchestrates the flow, invoking skills and making sequencing decisions | Tool use required, autonomous decisions, multi-step reasoning |

Single-agent vs. multi-agent is an architecture detail decided during agent configuration (later in Design) if "Agent" is selected — not a top-level choice here.

The model presents a confident recommendation — for example: *"Based on your workflow's **Guided** autonomy and the two reusable sub-routines I identified, I recommend **Skill-Powered Prompt** with **Augmented** involvement."*

If you disagree, the model explains the alternatives and you discuss. Most workflows start as Prompt or Skill-Powered Prompt and evolve toward agents as you add automation.

When the orchestration mechanism is Agent and the platform has multiple agent offerings (e.g., Claude Code sub-agents vs. Claude Agent SDK), the model asks which offering you want to use — this determines the artifact format in the Build step.

### Human Involvement

The orchestration mechanism recommendation includes an involvement mode — whether a human participates during the workflow run:

| Mode | Description | Determined by |
|------|-------------|---------------|
| **Augmented** | Human is in the loop — reviews, steers, or decides at key points during the run. | Web/desktop deployment, no scheduled execution |
| **Automated** | AI runs solo — executes end-to-end without human involvement during the run. | Scheduled/unattended execution, CLI |

The involvement mode is determined by your architecture decisions — platform, scheduled execution needs, and which steps require human review. See the [AI Workflow Design Matrix](workflow-design-matrix.md) for how autonomy and involvement combine into six workflow archetypes.

:::note[Deeper architectural patterns]
For detailed implementation blueprints (prompt chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer, and autonomous agents), see [Workflow Architecture Patterns](../patterns/workflow-architecture/index.md).
:::
---

:::caution[Activate plan mode now]
You've made the key decisions — architecture, autonomy level, orchestration mechanism, and involvement mode. This is the transition point. **Activate plan mode** on your AI tool before continuing. The model will now plan the rest of the spec (per-step autonomy classification, building block mapping, skill candidates, agent blueprints) based on the decisions you've locked in. See [How to activate plan mode](#two-phases-two-modes) for platform-specific instructions.
:::
## Autonomy Classification

For each step in your Workflow Definition, classify it on the autonomy spectrum:

| Level | Description | Example |
|-------|-------------|---------|
| **Human** | Requires human judgment, creativity, or physical action; AI cannot perform this | Final approval of a contract, in-person meeting |
| **Deterministic** | Follows fixed rules; AI executes reliably with no decisions | Formatting a report, extracting data from a template |
| **Guided** | AI makes bounded decisions within guardrails; human reviews at key checkpoints | Drafting an email for human review before sending |
| **Autonomous** | AI plans and executes end-to-end, including decisions and tool use | Research agent that finds, evaluates, and summarizes sources |

## Building Block Mapping

Map each AI-assisted step to one or more of the AI building blocks:

| Block | What It Is | When to Use It |
|-------|-----------|----------------|
| **Model** | The AI engine that processes inputs and generates outputs | When the task requires specific capabilities (reasoning, multimodal, speed) that influence model choice |
| **Prompt** | A well-crafted instruction that tells the model what to do for this step | Every AI step needs at least a prompt |
| **Context** | Background information, reference documents, examples, or data the model needs | When the step requires domain-specific knowledge not in the model's training |
| **Skill** | A reusable routine — give it inputs, it follows a defined process, it produces consistent outputs | When a step has complex logic that recurs across workflows |
| **Agent** | An autonomous AI that plans, uses tools, and executes multi-step work | When a step requires tool use, adaptive reasoning, or autonomous decisions |
| **MCP** | A connector giving the model access to external tools, APIs, databases, or services | When a step needs to read from or write to external systems |
| **Project** | A persistent workspace grouping prompts, context, skills, and agents | When the workflow runs frequently with the same reference materials |
| **Memory** | Accumulated knowledge the AI retains across conversations — preferences, past decisions, learned patterns | When repeating context across workflow runs is friction, or when the AI should adapt to patterns over time |
| **API** | Programmatic interfaces for accessing AI models and cloud services | When a step needs to be called from code, integrated into an application, or run at scale |
| **SDK** | Frameworks and toolkits for building AI workflows in code | When a step is implemented as a code-first agent with tool use, orchestration, or multi-agent coordination |

Also identify for each step:

- **Tools and connectors** — What external tools, APIs, or integrations does this step need?
- **Human-in-the-loop gates** — Where should a human review before the workflow continues?

## Skill Candidate Identification

Steps that should become skills share these characteristics:

- **Reusable** — The logic appears in multiple workflows or will be run repeatedly
- **Complex** — More than a simple instruction; involves multi-step reasoning, evaluation criteria, or domain expertise
- **Consistent** — Needs to produce reliable, repeatable outputs every time

For each skill candidate, document enough detail for generation:

| Detail | What to capture |
|--------|----------------|
| **Purpose** | What the skill does in one sentence |
| **Inputs** | What data or information the skill receives |
| **Outputs** | What the skill produces |
| **Decision logic** | Key rules, criteria, or evaluation frameworks |
| **Failure modes** | What happens when inputs are missing or unexpected |

This detail enables generation of skills on any platform during the Build step.

## Agent Blueprints

When the orchestration mechanism is Agent, document each agent your workflow needs. These are platform-agnostic specifications — the model builds them into working agents during [Build](build/index.mdx). Whether the workflow needs one agent or multiple agents is decided here based on the number of distinct roles, expertise domains, and orchestration needs.

| Component | What to specify |
|-----------|----------------|
| **Name** | Unique agent name |
| **Description** | Agent purpose and when it should be used |
| **Instructions** | Mission, responsibilities, behavior, goals, tone & style, output format |
| **Model** | Recommended model capability (reasoning-heavy, fast, etc.) |
| **Tools** | Tools the agent can call (MCP servers, file access, web, APIs) |

Plus:

- **Context** — What data, files, or knowledge base does the agent need access to?
- **Goal** — What triggers this agent and what does it produce?

For **multi-agent** workflows, also document:

- **Orchestration pattern** — Supervisor (one agent delegates), pipeline (agents in sequence), or parallel (agents work simultaneously)
- **Agent handoffs** — What does each agent pass to the next? What format?
- **Human review gates** — Where does a human review output before the pipeline continues?

This agent configuration is **platform-agnostic** — it serves as a blueprint. During the Build step, the model researches your chosen platform's current tools and generates platform-appropriate agent implementations.

## Outcome-Driven Design Flow

When your Workflow Definition has `Definition Type: Outcome-Driven`, the Design phase takes a streamlined path:

- **Autonomy** is Autonomous by definition — the agent system determines its own execution path
- **Involvement mode** (Augmented vs. Automated) is still determined from the definition's Human Gates section and trigger type
- **Orchestration** is Agent — the primary design artifact is the agent configuration
- **Capability domain mapping** replaces per-step classification — for each domain (research, analysis, writing, etc.), the model maps integration needs, intelligence requirements, and whether the domain should become a reusable skill
- **Evaluation criteria** are carried forward from the definition's Quality Criteria section rather than gathered from scratch
- **Agent Configuration** becomes the primary section of the spec, with instructions drawn from the definition's Goal, Constraints, and Expected Outputs

The output is the same AI Building Block Spec format, with Capability Domain Mapping replacing the Step-by-Step Decomposition table, and an Autonomy Statement replacing the Autonomy Spectrum Summary.

## How to Use This

This step is facilitated by the **`design`** Business-First AI Framework Skill. How you get it depends on your platform — see [Get the Skills](skills.mdx) for installation instructions.

**Start with this prompt:**

```
Design the AI workflow from my Workflow Definition.
Assess the autonomy level, recommend an orchestration mechanism, and map building blocks.
```

Upload or paste your Workflow Definition file (`[workflow-name]-definition.md`) from the Deconstruct step when prompted. The skill runs the Design analysis and produces an AI Building Block Spec.

:::tip[If your AI tool doesn't support skills]
Download the skill file from [GitHub](https://github.com/jamesgray-ai/handsonai-plugins/tree/main/plugins/business-first-ai/skills/design) and paste it into your system prompt or project instructions. Or use this page as a conversation guide — walk through each section in order with your AI tool.
:::
### Two phases, two modes

Design has two distinct phases that use different modes of interaction with the model:

**Phase 1: Collaborative decisions (normal conversation)**

The first part of Design is a back-and-forth conversation. The model scans your Workflow Definition for known answers, confirms what it can infer, asks about anything genuinely unknown, assesses the workflow's autonomy level, recommends an orchestration mechanism and involvement mode, and you discuss and confirm. This is normal conversational mode — you're making decisions together.

**Phase 2: Plan the spec (plan mode)**

Once the architecture decisions, autonomy level, and orchestration mechanism are locked in, the model has everything it needs to plan the full AI Building Block Spec. This is when you **activate plan mode** — the model shifts from asking you questions to planning: classifying each step on the autonomy spectrum, mapping building blocks, identifying skill candidates, and documenting agent blueprints.

**How to activate plan mode on your platform:**

| Platform | How to activate plan mode |
|---|---|
| **Claude Code** | Press `Shift+Tab` twice, or type `/plan` |
| **Cursor** | Select "Plan" in the composer mode |
| **Codex CLI** | Run with the `--plan` flag |
| **Other AI tools** | Ask the model: *"Switch to plan mode. Based on the architecture decisions, autonomy level, and orchestration mechanism we've agreed on, plan the full AI Building Block Spec — classify each step, map building blocks, identify skill candidates, and document agent blueprints."* |

After the model produces the plan, **review and approve the AI Building Block Spec** before moving on. If anything needs adjustment — a step classification, a skill candidate, an agent blueprint — now is the time. Once you approve, the model transitions to [Build (Step 4)](build/index.mdx) and begins building.

## What This Produces

The **AI Building Block Spec** contains:

- **Architecture approach** — No-code or Code-first, with rationale and recommendation signals
- **Autonomy level assessment** — Deterministic, Guided, or Autonomous, with rationale for where the whole workflow sits on the spectrum
- **Orchestration mechanism** — Prompt, Skill-Powered Prompt, or Agent, with involvement mode and reasoning
- **Architecture decisions** — platform, tool integrations (with connector mapping), trigger/schedule implications, and any flags (browser access, infrastructure needs) — each with rationale and a constraints summary showing how they shaped the recommendations. Deployment surface, code comfort, and shareability are resolved during Build.
- **Code-first selections** (when applicable) — specific API and SDK choices per step with justification (e.g., "Claude Agent SDK for the research agent because it needs tool use and multi-step orchestration")
- **Scenario summary** — workflow metadata from the Workflow Definition
- **Decomposition table** — every step with autonomy classification, decision points, failure modes, data flows, context needs, AI building block mapping, and skill candidate flags
- **Autonomy spectrum summary** — steps grouped by classification level
- **Skill candidates** — steps tagged for skill creation, with generation-ready detail (purpose, inputs, outputs, decision logic, failure modes)
- **Agent blueprints** (when applicable) — platform-agnostic specification for each agent with all five core components plus context and goal
- **Step sequence and dependencies** — sequential vs. parallel execution paths
- **Prerequisites** — what must be in place before the workflow can run
- **Context inventory** — every piece of context the workflow needs, with status and key contents
- **Tools and connectors** — external integrations required
- **Implementation order** — quick wins → semi-autonomous → complex agent steps

This AI Building Block Spec is the input for [Step 4: Build](build/index.mdx), where the model generates platform-appropriate artifacts (prompts, skills, agents, connectors) based on your orchestration mechanism and architecture decisions.
