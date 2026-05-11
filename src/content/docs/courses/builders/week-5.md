---
title: Week 5 - Run the Framework End-to-End
description: Run the Business-First AI Framework end-to-end on a real workflow — Competitive Intelligence — and ship a working skill and agent in your workspace.
---

In Week 5 you run the Business-First AI Framework end-to-end yourself, live in class. Starting from a pre-built workflow definition, you invoke `/design`, `/build`, `/test`, and `/run` on a **Competitive Intelligence** workflow — shipping a `competitor-research` skill and `competitor-brief` agent that produce a structured brief on a real competitor. In Session 10, you'll evolve that workflow into a self-improving system.

## Lesson: Ship a Workflow Using the Business-First AI Framework

Run the framework end-to-end yourself in Cowork (or Claude Code — same slash commands). Starting from a pre-built workflow definition, you invoke `/design`, `/build`, `/test`, and `/run` — generating a `competitor-research` skill and `competitor-brief` agent from your approved spec, then running the workflow on a real competitor. Watch a structured context file get produced on the first run.

### Hands-on assignment

**Starting point:** a pre-built workflow definition (download below).
**Ending point:** a shipped skill + agent producing a brief on a real competitor.

1. **`/design`** — Turn the definition into an approved Building Block Spec (plan mode, collaborative). See the [Design step docs](../../../business-first-ai-framework/design/).
2. **`/build`** — Generate the `competitor-research` skill and `competitor-brief` agent from your spec. See the [Build step docs](../../../business-first-ai-framework/build/).
3. **`/test`** — Validate the building blocks before trusting them with real input. See the [Test step docs](../../../business-first-ai-framework/test/).
4. **`/run`** — Invoke the workflow on a real competitor; watch `knowledge/competitors/{name}.md` emerge. See the [Run step docs](../../../business-first-ai-framework/run/).

### Download the workflow definition

The Step 2 (Deconstruct) artifact is pre-built so we can spend Session 9 running the rest of the framework on it. Save this file into your workspace before class:

- [**Competitive Intelligence — Workflow Definition (markdown)**](/assets/courses/builders/competitive-intelligence-workflow-definition.md)

### What you'll walk away with

- A `competitor-research` skill and a `competitor-brief` agent installed in your workspace, ready to invoke any time
- A populated `knowledge/competitors/{name}.md` file on a real competitor — the seed for Session 10's self-improvement work
- First-hand reps on every framework step as a chainable slash command (`/analyze`, `/deconstruct`, `/design`, `/build`, `/test`, `/run`, `/improve`)

## Lesson: Recognize When a Workflow Needs to Improve

A brief, conceptual preview of Step 7 of the framework — [Improve](../../../business-first-ai-framework/improve/) — anchored to the workflow you just ran. Identify the three signals that tell you a running workflow needs to evolve: hypotheses that never confirm, edge cases where the schema breaks, and drift as your priorities evolve. Improve is the step that never ends — and in Session 10, you'll actually do the iteration.

## Lesson: Evolve Your Workflow Into a Self-Improving System

Take the workflow you shipped in Session 9 and evolve it into a system that gets sharper every time it runs. Apply Karpathy's "LLM Wiki" pattern to its structured context file — structure it with Rules / Facts / Hypotheses sections, implement an ingest / query / lint learning loop, and schedule the workflow to run daily without you. By session end, your workflow's outputs feed a self-improving knowledge base of competitor intelligence — Step 7 (Improve) in action.
