---
title: Framework Glossary
description: Every term you meet in the seven-step AI Workflow Framework, in plain language — lens, autonomy, involvement, skill, agent, report card, registry, and more.
---

Every term you'll meet across the seven steps, in plain language, each linked to the page that introduces it.

**Acceptance criterion (AC)** — A numbered, yes/no statement of what a successful run must do, derived from a real example you were happy with. Captured in [Deconstruct](../deconstruct/) as `AC1, AC2, …` and graded line by line in [Test](../test/).

**Agent (mechanism)** — An orchestration mechanism that decides its own path at runtime, using tools on its own judgment and able to run unattended. Chosen in [Design](../design/) when a workflow's steps depend on what it finds along the way.

**Agent (building block)** — One of the Orchestration-layer AI building blocks: a configured worker with a mission, tools, and constraints that an orchestrator or a person dispatches. See [Agentic Building Blocks](../../agentic-building-blocks/). *Agent* the mechanism means the whole workflow is driven by one agent that decides its own path; *agent* the building block is any configured agent, including the workers a mechanism-level agent dispatches.

**Augmented / Automated (involvement)** — The two values of human involvement. **Augmented** means a human is in the loop during the run — reviewing, steering, or approving at key points. **Automated** means the AI runs solo and a human only reviews the finished output. Set during [Design](../design/) and classified in the [AI Workflow Design Matrix](../workflow-design-matrix/).

**Autonomy** — How much decision-making the AI has. **Deterministic** follows fixed rules with no judgment calls. **Guided** makes bounded decisions within guardrails you set. **Autonomous** plans, decides, and adapts independently. A fourth value, **Human**, exists only when classifying an individual step in [Design](../design/) — a step a person performs, with no AI involved — and never appears at the whole-workflow level. See the [AI Workflow Design Matrix](../workflow-design-matrix/).

**Backlog** — The `status: backlog` value on a Workflow node: a candidate workflow [Analyze](../analyze/) has registered in your registry but nobody has started building yet.

**Baseline** — The report card from the round of [Test](../test/) that first reaches Ready. [Improve](../improve/) re-runs the same inputs later and compares every line against this baseline to see what changed.

**Building blocks (three layers)** — The AI building blocks a workflow step can be mapped to, grouped in three layers: **Intelligence** (Model, Context, Memory, Project), **Orchestration** (Prompt, Skill, Agent), and **Integration** (MCP, API, SDK, CLI). Mapped during [Design](../design/); see [Agentic Building Blocks](../../agentic-building-blocks/) for full definitions.

**Capability domain** — In a goal-driven workflow, a durable competency the agent draws on at runtime (for example "research" or "synthesis") — not a step or a pipeline stage. Capability domains replace step-by-step decomposition in [Design](../design/) for goal-driven workflows.

**Connector** — The mechanism a workflow uses to reach a live system such as a CRM, calendar, or drive. [Design](../design/) works out how the workflow will reach each system — a platform-native connector first, otherwise an MCP server, API, SDK, or CLI; [Build](../build/) has you authorize each one in the account that will actually run the workflow.

**Context** — One of the Intelligence-layer building blocks: the documents, examples, and reference material a step needs to produce good output. Resolved item by item during [Build](../build/)'s Prepare Context phase.

**Context Inventory (C1…)** — The table in the Workflow Requirements listing every artifact a workflow needs, each with a stable ID (`C1, C2, …`), its status, sensitivity, source, and whether the AI can currently access it. Captured in [Deconstruct](../deconstruct/).

**Definition type (step-driven / goal-driven)** — Which of the two Deconstruct paths a workflow took. **Step-driven** means you can describe how the work gets done. **Goal-driven** means you know what "done" looks like and an agent figures out the steps at runtime. Chosen at the start of [Deconstruct](../deconstruct/).

**Design Spec** — The architectural blueprint [Design](../design/) produces from your Workflow Requirements: platform, mechanism, autonomy, step classifications, skill and agent blueprints. It is a draft — its frontmatter carries `approved: false` until you say "approve," and [Build](../build/) refuses to run on an unapproved spec.

**Execution mode** — A Workflow node field recording how the workflow currently runs: `manual` (a person still does it, AI hasn't run it yet), `augmented` (AI runs it with a human in the loop), or `automated` (AI runs it unattended). One of the four fixed-value fields on a Workflow node — see the [AI Registry Setup guide](../../builder-setup/ai-registry-setup/) — kept current by each framework step that touches the node, and checked by [Run](../run/) before a workflow can be put on a schedule.

**Fix mode** — The path [Build](../build/) takes when you return from a Not Ready verdict in [Test](../test/): it rebuilds only the building blocks your test results named, leaving everything else installed as-is.

**Golden example** — A real past output you'd consider exactly right, supplied in [Deconstruct](../deconstruct/). [Test](../test/) compares new output against it to see what's missing, extra, or different in substance.

**Human gate (G1…)** — A point in the workflow where a person must review or approve before it continues, captured with a stable ID (`G1, G2, …`) in [Deconstruct](../deconstruct/) and checked off in [Test](../test/)'s report card.

**Lens** — The scope of an [Analyze](../analyze/) audit: **Individual** (your own workflows) or **Organizational** (a value chain process spanning multiple roles). The lens changes what you're analyzing, not the matrix you classify it on — see the [AI Workflow Design Matrix](../workflow-design-matrix/).

**Orchestrator skill** — The top-level skill that drives a Skill-mechanism workflow: it invokes the component skills in order and pauses at human gates. Named after the workflow itself and specified in [Design](../design/)'s Orchestrator Prompt Outline.

**Packaging** — How [Design](../design/) decides the built artifacts will ship: as a **Plugin**, a **Standalone Skill**, a **Workspace Agent**, or **Loose Files**.

**Platform mode** — Whether your platform generates source files directly (**code mode**, e.g. Claude Code, Cursor) or step-by-step GUI instructions (**guided mode**, e.g. Copilot Studio). [Build](../build/) reads this from the platform registry — it is never something you select.

**Process (registry)** — A registry node representing an end-to-end business process; every Workflow node belongs to exactly one Process, listed in that Process's `# Workflows` section. Set up during your [AI Registry](../../builder-setup/ai-registry-setup/) interview.

**Registry** — Your AI Registry: a folder of Markdown "nodes" describing your business, its processes, and its workflows, which every framework step reads from and writes to so you never re-describe your work. See the [AI Registry Setup guide](../../builder-setup/ai-registry-setup/).

**Report card** — The table [Test](../test/) produces per scenario: every acceptance criterion, rule, and human gate listed as **Expected | From | Result | Evidence**, with Result always exactly Met or Not met.

**Requirements (Workflow Requirements)** — The Product Requirements Document for a workflow: goal, value and measurement, context inventory, acceptance criteria, example scenarios, rules, and human gates. Produced by [Deconstruct](../deconstruct/) and consumed by every later step.

**Rule (R1…)** — A must-do, must-never-do, or fallback statement about how the work should be done, captured with a stable ID (`R1, R2, …`) in [Deconstruct](../deconstruct/) and checked in [Test](../test/)'s report card.

**Run Card** — The one-page guide [Run](../run/) writes after your first real run, covering how to start the workflow, what to have ready, and what to check before you act on the output. Saved as `run-guide.md`.

**Run log** — The one-line-per-run record (`runs.md`) that [Run](../run/) starts: date, input, result, and edits needed. [Improve](../improve/) reads it as evidence of drift.

**Scenario (E1…)** — A representative input, with what to look for in the output, captured in [Deconstruct](../deconstruct/)'s Example Scenarios and given a stable ID (`E1, E2, …`). [Test](../test/) runs each one and grades it against the acceptance criteria.

**Skill (mechanism)** — An orchestration mechanism you start by name; it follows the mapped steps every time, pausing where you said. Chosen in [Design](../design/) when you trigger the work yourself and the same steps repeat each run.

**Skill (building block)** — Any reusable instruction set the model follows, including the smaller component skills an orchestrator skill invokes. *Skill* the mechanism means the whole workflow runs as one skill you start by name; *skill* the building block is any reusable instruction set, including the component skills inside it. See [Agentic Building Blocks](../../agentic-building-blocks/).

**Stable ID** — A short label (`S1`, `A1`, `C1`, `E1`, `AC1`, `R1`, `G1`) that stays the same across every document referencing it, so every framework step can point at exactly the same component. Introduced in [Deconstruct](../deconstruct/) and [Design](../design/).

**`stale_after`** — The review-date field on a Workflow node. A workflow is stale once today's date reaches it; [Run](../run/) sets it on go-live, and [Improve](../improve/) resets it at the close of each review.

**Workflow node** — The registry file (`registry/workflows/<slug>.md`) that tracks one workflow's status, mode, and artifacts across every framework step, so any session can pick up where you left off. First written by [Analyze](../analyze/); see the [AI Registry Setup guide](../../builder-setup/ai-registry-setup/).
