---
title: Design Your AI Workflow
description: Gather architecture decisions, choose an execution pattern and interaction mode, classify steps on the autonomy spectrum, map AI building blocks, identify skill candidates, and document agent blueprints — producing a platform-agnostic AI Building Block Spec.
---

# 3.1: Design Your AI Workflow

> **Part of:** [Build Workflows](index.md)

!!! tip "New to the building blocks?"
    See the [Agentic Building Blocks](../../agentic-building-blocks/index.md) reference for definitions, examples, and cross-platform comparisons of all ten blocks.

## What This Is

The Design phase is where you decide *how* your workflow should be built — before you build it. You take the Workflow Definition from the [Deconstruct step](../deconstruct/index.md) and make five design decisions:

1. **Architecture approach** — Will you build no-code (in a platform UI) or code-first (with APIs and SDKs)?
2. **Architecture decisions** — What platform are you using, and what integrations and constraints does the Workflow Definition reveal?
3. **Execution pattern** — How complex does the AI implementation need to be?
4. **Autonomy classification** — How much AI assistance does each step need?
5. **Building block mapping** — What specific AI components does each step require?

!!! abstract "Framework vs. platform — by design"
    This framework guides you through *which decisions to make* and *what building blocks to design* — it is platform-agnostic. The AI model provides the platform-specific expertise: it researches your chosen platform's current tools, SDKs, and best practices at runtime via web search. This separation ensures the framework stays current as platforms evolve, without requiring documentation updates every time a platform changes its offerings.

| | |
|---|---|
| **What you'll do** | Upload your Workflow Definition, choose your architecture approach, confirm your platform, review the AI's extracted architecture analysis and execution pattern recommendation, review step classifications, and adjust anything that doesn't look right |
| **What you'll get** | An **AI Building Block Spec** — architecture approach with rationale, architecture decisions, execution pattern with interaction mode, autonomy classifications, building block mapping, skill candidates, agent blueprints (when applicable), and a prioritized build sequence |
| **Time** | ~15–25 minutes (architecture questions + reviewing the AI's analysis) |

## Why This Matters

Not every workflow needs the same level of AI infrastructure. A weekly status report might need a single well-crafted prompt. A multi-department content pipeline might need specialized agents coordinating across stages. Choosing the wrong execution pattern means either over-engineering (building agents when a prompt would do) or under-building (forcing a prompt to do agent-level work).

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

Most workflows start no-code. Code-first becomes the right choice when you need programmatic control, integration into existing systems, or production-grade deployment. The same four execution patterns (Prompt, Skill-Powered Prompt, Single Agent, Multi-Agent) apply to both approaches — the architecture approach determines *how* you implement them, not *what* you implement.

!!! tip "You can switch later"
    Many teams prototype no-code, validate the workflow works, then rebuild code-first for production. The AI Building Block Spec captures the design either way — only the Construct phase changes.

## Architecture Decisions

Before choosing an execution pattern, the model gathers the information that shapes platform-aware recommendations. Rather than walking through a checklist, it uses an **extract-then-confirm** approach: ask one question, extract everything else from your Workflow Definition, and present the analysis for confirmation.

**One question: Platform.** The only thing not already in your Workflow Definition is which AI platform you'll use. If you've already mentioned it in conversation, the model confirms. If not, it asks — and accepts whatever level of specificity you provide ("Claude Code", "ChatGPT", "Google Gemini", "Claude" are all fine). The model doesn't try to disambiguate to a specific offering upfront — the ecosystem is enough for Design decisions, and the specific tool is resolved during Construct when generating artifacts.

**Everything else is extracted from the Workflow Definition:**

- **Tool integrations** — pulled from data flows, context needs, and step details across all steps. The model researches availability on your platform via web search and categorizes each: Built-in, Available with setup, Possible with code, or Manual.
- **Trigger/schedule** — pulled from your Scenario Metadata. Time-based triggers are noted as scheduled execution requirements with implications for interaction mode and infrastructure.
- **Browser access** — if any step involves logging into a website, it's flagged during step classification rather than asked about separately. The connection details are handled during Construct.
- **Shareability** — deferred to Construct, where it determines artifact format (file-based vs. code-based). Not asked during Design.

Code comfort and deployment surface are inferred from the platform choice when specific (Claude Code = CLI + code-comfortable, ChatGPT = web + no-code) or resolved during Construct when vague.

After extracting, the model presents a single confirmation block showing the platform, extracted tool integrations with availability mapping, trigger implications, and any flags — then asks if anything was missed or needs adjustment. The confirmed decisions gate all subsequent recommendations.

## Execution Pattern Spectrum

Every AI workflow falls somewhere on this spectrum. The right pattern depends on what your workflow actually needs — not on how sophisticated you want it to be.

| Pattern | Description | Signals |
|---------|-------------|---------|
| **Prompt** | Single structured prompt with step-by-step instructions, all logic inline | Sequential steps, human provides inputs and makes decisions |
| **Skill-Powered Prompt** | Prompt that invokes reusable skills for complex sub-routines | Repeatable sub-routines, moderate complexity, steps that recur across workflows |
| **Single Agent** | One agent with tool access, capable of autonomous decisions | Tool use required, autonomous decisions, multi-step reasoning |
| **Multi-Agent** | Specialized agents coordinating in a pipeline | Multiple expertise domains, parallel execution, review gates between stages |

### Choosing a Pattern

The model analyzes your workflow steps and architecture decisions, then presents a confident recommendation — for example: *"Based on your workflow, I recommend **Skill-Powered Prompt** with **Interactive** mode because your steps are sequential with two reusable sub-routines, and you're running this from the web UI."*

The signals it reasons through internally:

- **Tool use** (web search, file access, APIs) → pushes toward agent patterns
- **Autonomous decision-making** (AI decides what to do next) → requires at least Single Agent
- **Reusable logic** (sub-routines across workflows) → flags skill candidates
- **Multiple expertise domains** (research vs. writing vs. editing) → suggests Multi-Agent
- **Parallel execution or review gates** → suggests Multi-Agent

If you disagree with the recommendation, the model explains the alternatives and you discuss. Most workflows start as Prompt or Skill-Powered Prompt and evolve toward agents as you add automation.

When the execution pattern is agent-based and the platform has multiple agent offerings (e.g., Claude Code sub-agents vs. Claude Agent SDK), the model asks which offering you want to use — this determines the artifact format in the Construct phase.

### Interaction Mode

After choosing an execution pattern, determine how the human and AI interact during the workflow run:

| Mode | Description | Determined by |
|------|-------------|---------------|
| **Interactive** | Human and AI collaborate in real-time. AI pauses for input, review, and decisions at marked steps. | Web/desktop deployment, no scheduled execution |
| **Autonomous** | AI executes end-to-end without human involvement during the run. | Scheduled/unattended execution, CLI |
| **Hybrid** | Some steps run autonomously, others pause for human interaction. | Mix of automated and review steps |

The interaction mode is determined by your architecture decisions — platform, scheduled execution needs, and which steps require human review.

!!! info "Deeper architectural patterns"
    For detailed implementation blueprints (prompt chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer, and autonomous agents), see [Workflow Architecture Patterns](../../patterns/workflow-architecture/index.md).

---

!!! warning "Activate plan mode now"
    You've made the key decisions — architecture, execution pattern, and interaction mode. This is the transition point. **Activate plan mode** on your AI tool before continuing. The model will now plan the rest of the spec (autonomy classification, building block mapping, skill candidates, agent blueprints) based on the decisions you've locked in. See [How to activate plan mode](#two-phases-two-modes) for platform-specific instructions.

## Autonomy Classification

For each step in your Workflow Definition, classify it on the autonomy spectrum:

| Level | Description | Example |
|-------|-------------|---------|
| **Human** | Requires human judgment, creativity, or physical action; AI cannot perform this | Final approval of a contract, in-person meeting |
| **Deterministic** | Follows fixed rules; AI executes reliably with minimal supervision | Formatting a report, extracting data from a template |
| **Semi-Autonomous** | AI does most of the work; human reviews at key checkpoints | Drafting an email for human review before sending |
| **Autonomous** | AI executes end-to-end, including decisions and tool use | Research agent that finds, evaluates, and summarizes sources |

## Building Block Mapping

Map each AI-assisted step to one or more of the ten building blocks:

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

This detail enables generation of skills on any platform during the Construct phase.

## Agent Blueprints

When the execution pattern is Single Agent or Multi-Agent, document each agent your workflow needs. These are platform-agnostic specifications — the model builds them into working agents during [Construct](index.md#32-construct).

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

This agent configuration is **platform-agnostic** — it serves as a blueprint. During the Construct phase, the model researches your chosen platform's current tools and generates platform-appropriate agent implementations.

## How to Use This

This step is facilitated by the **`building-workflows`** Business-First AI Framework Skill. How you get it depends on your platform — see [How to Add Skills to Your Platform](../../agentic-building-blocks/skills/index.md#how-to-add-skills-to-your-platform) for installation instructions for Claude Code, Cursor, Codex CLI, Gemini CLI, and VS Code Copilot.

**Start with this prompt:**

```
Design the AI workflow from my Workflow Definition.
Recommend an execution pattern and map building blocks.
```

Upload or paste your Workflow Definition file (`[workflow-name]-definition.md`) from the Deconstruct step when prompted. The skill runs the Design analysis and produces an AI Building Block Spec.

!!! tip "If your AI tool doesn't support skills"
    Use this page as a conversation guide — walk through each section in order with your AI tool. The methodology works the same way whether or not a skill is driving the process.

### Two phases, two modes

Design has two distinct phases that use different modes of interaction with the model:

**Phase 1: Collaborative decisions (normal conversation)**

The first part of Design is a back-and-forth conversation. The model scans your Workflow Definition for known answers, confirms what it can infer, asks about anything genuinely unknown, recommends an execution pattern and interaction mode, and you discuss and confirm. This is normal conversational mode — you're making decisions together.

**Phase 2: Plan the spec (plan mode)**

Once the architecture decisions and execution pattern are locked in, the model has everything it needs to plan the full AI Building Block Spec. This is when you **activate plan mode** — the model shifts from asking you questions to planning: classifying each step on the autonomy spectrum, mapping building blocks, identifying skill candidates, and documenting agent blueprints.

**How to activate plan mode on your platform:**

| Platform | How to activate plan mode |
|---|---|
| **Claude Code** | Press `Shift+Tab` twice, or type `/plan` |
| **Cursor** | Select "Plan" in the composer mode |
| **Codex CLI** | Run with the `--plan` flag |
| **Other AI tools** | Ask the model: *"Switch to plan mode. Based on the architecture decisions and execution pattern we've agreed on, plan the full AI Building Block Spec — classify each step, map building blocks, identify skill candidates, and document agent blueprints."* |

After the model produces the plan, **review and approve the AI Building Block Spec** before moving on. If anything needs adjustment — a step classification, a skill candidate, an agent blueprint — now is the time. Once you approve, the model transitions to [Construct (3.2)](construct.md) and begins building.

## What This Produces

The **AI Building Block Spec** contains:

- **Architecture approach** — No-code or Code-first, with rationale and recommendation signals
- **Execution pattern** — Prompt, Skill-Powered Prompt, Single Agent, or Multi-Agent, with interaction mode and reasoning
- **Architecture decisions** — platform, tool integrations (with connector mapping), trigger/schedule implications, and any flags (browser access, infrastructure needs) — each with rationale and a constraints summary showing how they shaped the recommendations. Deployment surface, code comfort, and shareability are resolved during Construct.
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

This AI Building Block Spec is the input for the [Construct phase](index.md), where the model generates platform-appropriate artifacts (prompts, skills, agents, connectors) based on your execution pattern and architecture decisions.
