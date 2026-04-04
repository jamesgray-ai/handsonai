---
title: "Example: Content Calendar Planning"
description: A complete worked example showing the framework deliverables — Workflow Definition, AI Building Block Spec, and workflow prompt — for a real content calendar planning workflow.
---This page walks through the complete output of running a real workflow through the [Business-First AI Framework](../index.md). The workflow is **Content Calendar Planning** — a weekly process for planning and sequencing content across LinkedIn, Substack, X, and YouTube.

The first four steps of the framework — Analyze, Deconstruct, Design, and Build — produced three key deliverables for this workflow. Each one is a detailed markdown document. This page summarizes what's in each and why it matters — then links to the full file on GitHub where you can read every table, every decision point, and every failure mode at full width.

---

## The Deliverables

### 1. Workflow Definition (Step 2 — Deconstruct)

[GitHub View full Workflow Definition on GitHub](https://github.com/jamesgray-ai/handsonai/blob/main/examples/content-calendar-planning/workflow-definition.md)

The Workflow Definition is what [Deconstruct](../deconstruct/index.md) produces. What started as "I plan content on Sundays" became **10 refined steps across four phases** after the six-question deep dive.

**What's inside:**

- **Scenario metadata** — workflow name, trigger, outcome, business objective
- **10 refined steps** organized into four phases: Input Gathering (4 steps), Planning (4 steps), Approval (1 step), Execution (1 step)
- **Each step decomposed** with: Action, Sub-steps, Decision Points, Data In, Data Out, Context Needed, and Failure Modes
- **Dependency map** showing which steps can run in parallel and which must be sequential
- **Context shopping list** — 9 artifacts the workflow needs, with status (Exists / Needs Creation)
- **Related workflows** — upstream and downstream dependencies

**Key insight:** Notice how each step captures not just *what* to do, but *what to do when things go wrong*. Step 1 has a fallback for when no metrics data exists. Step 2 detects an empty backlog and escalates the importance of Step 3. Step 9 limits refinement to 3 rounds to prevent endless iteration. This failure-mode thinking is what makes the workflow robust enough for AI to execute.

---

### 2. AI Building Block Spec (Step 3 — Design)

[GitHub View full Building Block Spec on GitHub](https://github.com/jamesgray-ai/handsonai/blob/main/examples/content-calendar-planning/building-block-spec.md)

The AI Building Block Spec is what [Design](../design.md) produces from the Workflow Definition. It classifies each step on the autonomy spectrum, identifies which steps should become reusable skills, and recommends an implementation order.

**What's inside:**

- **Orchestration mechanism selection** — why "Skill-Powered Prompt" was chosen over a full agent (the creative middle steps benefit from human judgment)
- **Step-by-step decomposition table** — each step classified by Phase, Autonomy level, Building Blocks needed, Skill candidacy, and whether it's a Human Gate
- **Autonomy spectrum summary** — Deterministic (4 steps), Guided (4 steps), Human (2 steps)
- **4 skill candidates** with full specifications: purpose, inputs, outputs, decision logic, and failure modes
- **Dependency map** and critical path analysis
- **Context inventory** — what data sources and reference materials each step needs
- **Recommended implementation order** — Quick Wins first (prompt + 2 simple skills), then Guided (2 complex skills), then Future Enhancements

**Key insight:** The spec doesn't say "build everything at once." It recommends starting with a prompt — pure conversation, no infrastructure — so you get value immediately. Database skills layer in incrementally. This build order means you're running the workflow on day one.

---

### 3. Workflow Prompt (Step 4 — Build)

[GitHub View full Workflow Prompt on GitHub](https://github.com/jamesgray-ai/handsonai/blob/main/examples/content-calendar-planning/baseline-prompt.md)

The workflow prompt is one of the platform artifacts that [Build (Step 4)](../build/index.mdx) produces. This is the ready-to-run prompt you paste into any AI tool to execute the workflow.

**What's inside:**

- **Full 10-step orchestration** — the AI knows exactly what to do at each step, what to present, and when to pause for human input
- **Phase-by-phase instructions** — Input Gathering runs skills automatically, Planning proposes and waits for approval, Approval iterates collaboratively, Execution commits to the database
- **Embedded context** — channel cadence targets, channel-format fit rules, and content pillar definitions are baked into the prompt so no external documents are needed
- **Input and output specifications** — what the user provides (fresh ideas, calendar context, theme selection, approvals) and what the workflow produces (input summary, draft plan, final plan, database confirmation)

**Key insight:** The prompt reads like a conversation script. At each step, the AI knows whether to act autonomously, propose and wait, or ask for input. The human-in-the-loop gates (Steps 3, 5, 6, 9) are explicit — the AI won't proceed without approval at those points.

---

## What to Notice

A few things to take away from this example:

- **The expansion.** "I plan content on Sundays" became 10 steps across 4 phases, with decision logic, failure modes, and a dependency map. That expansion is what makes the workflow executable by AI.
- **The autonomy spectrum.** Not every step needs AI autonomy. Steps 1, 2, 4, and 10 are deterministic (fixed data operations). Steps 5-8 are guided (AI proposes, human decides). Steps 3 and 9 are human-led. The framework helps you see this clearly.
- **The build order.** The Building Block Spec doesn't just say "build everything." It recommends starting with a prompt (pure conversation, no infrastructure needed), then layering in skills incrementally. You get value from the first run.
- **Platform-agnostic.** The Workflow Definition and Building Block Spec work with any AI tool. The skills and MCP connections are implementation details that vary by platform — but the underlying logic is the same everywhere.

---

## Try It on Your Own Workflow

Ready to run your own workflow through the framework?

- **[Step 1 — Analyze](../analyze.md)**: Find which of your workflows are candidates for AI
- **[Step 2 — Deconstruct](../deconstruct/index.md)**: Break your chosen workflow into atomic steps
- **[Step 3 — Design](../design.md)**: Design the AI implementation architecture
- **[Step 4 — Build](../build/index.mdx)**: Generate platform artifacts
- **[Step 5 — Test](../test.md)**: Evaluate output quality and establish a baseline
- **[Step 6 — Run](../run.md)**: Deploy and operate the workflow
- **[Step 7 — Improve](../improve.md)**: Evaluate and evolve running workflows

Or start from the [Business-First AI Framework overview](../index.md) for the full methodology.
