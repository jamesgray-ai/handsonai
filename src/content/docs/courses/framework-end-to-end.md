---
title: Run the Framework End-to-End
description: Run the AI Workflow Framework end-to-end on a real workflow — Competitive Intelligence — and ship a working skill and agent in your workspace.
---

In this exercise you run the AI Workflow Framework end-to-end yourself, live in class. Starting from a pre-built Workflow Requirements, you invoke `/handsonai:design`, `/handsonai:build`, `/handsonai:test`, and `/handsonai:run` on a **Competitive Intelligence** workflow — shipping a `competitor-research` skill and `competitor-brief` agent that produce a structured brief on a real competitor. In a follow-up session, you'll evolve that workflow into a self-improving system.

## Lesson: Ship a Workflow Using the AI Workflow Framework

Run the framework end-to-end yourself with the Hands-on AI plugin installed — in Claude Code (slash commands), Cowork (type `/` to pick each skill), or Claude Chat (just ask for the step). Starting from a pre-built Workflow Requirements, you invoke `/handsonai:design`, `/handsonai:build`, `/handsonai:test`, and `/handsonai:run` — generating a `competitor-research` skill and `competitor-brief` agent from your approved spec, then running the workflow on a real competitor. Watch a structured context file get produced on the first run.

### Hands-on assignment

**Starting point:** a pre-built Workflow Requirements (download below).
**Ending point:** a shipped skill + agent producing a brief on a real competitor.

1. **`/handsonai:design`** — Turn the requirements into an approved Design Spec (plan mode, collaborative). See the [Design step docs](../../ai-workflow-framework/design/).
2. **`/handsonai:build`** — Generate the `competitor-research` skill and `competitor-brief` agent from your spec. See the [Build step docs](../../ai-workflow-framework/build/).
3. **`/handsonai:test`** — Validate the building blocks before trusting them with real input. See the [Test step docs](../../ai-workflow-framework/test/).
4. **`/handsonai:run`** — Invoke the workflow on a real competitor; watch `knowledge/competitors/{name}.md` emerge. See the [Run step docs](../../ai-workflow-framework/run/).

### Download the Workflow Requirements

The Step 2 (Deconstruct) artifact is pre-built so we can spend class time running the rest of the framework on it.

<a href="/assets/courses/competitive-intelligence-workflow-requirements.md" download="competitive-intelligence-workflow-requirements.md"><strong>Download the Competitive Intelligence — Workflow Requirements (.md)</strong></a>

### Set up your workspace before class

Do these steps in the folder you have open in Cowork or Claude Code.

**Step 1 — get a `registry/` folder.** Open the folder you'll work in (any folder — it doesn't need to be a GitHub repository) in your AI assistant and say *"Set up my AI registry."* It creates the `registry/` folder for you. If you'd like GitHub to build a dashboard automatically, start from the [AI Registry template repository](https://github.com/jamesgray-ai/ai-registry-template) instead — the [AI Registry setup guide](/builder-setup/ai-registry-setup/) walks through both.

**Step 2 — create the workflow folder and save the download.** Inside your workspace, create a folder named `outputs`, and inside it a folder named `competitive-intelligence-brief`. Save the download as `requirements.md` inside that folder, so the full path is `outputs/competitive-intelligence-brief/requirements.md`. (Rename the downloaded file — the framework skills look for `requirements.md`.)

**Step 3 — hand-type the first Workflow node.** In `registry/workflows/`, create a file named `competitive-intelligence-brief.md` and paste in exactly this. Easiest path: ask your AI assistant to create the file for you with this exact content. (Or, if your registry lives on GitHub and you save files yourself, open your repository on github.com, click **Add file → Create new file**, paste `registry/workflows/competitive-intelligence-brief.md` as the filename, paste the block below as the content, then **Commit** — same result either way.)

```markdown
---
type: Workflow
title: "Competitive Intelligence Brief"
description: "Research a competitor's recent moves and produce a structured brief plus an updated knowledge file."
generated: { by: process:deconstruct, at: 2026-07-06 }
status: under-development
definition_type: step-driven
execution_mode: manual
autonomy: guided
trigger: "manual"
stale_after: 2026-10-06
---
# Competitive Intelligence Brief

Research a competitor's recent moves and produce a structured brief plus an
updated knowledge file. Triggered manually on demand, or scheduled per competitor.

# Artifacts

- [Requirements](outputs/competitive-intelligence-brief/requirements.md)
```

The node is the small file every framework step reads first; your `registry/` is the inventory. When class starts, you'll run `/design` and it will pick up right where the pre-built requirements leave off.

### What you'll walk away with

- A `competitor-research` skill and a `competitor-brief` agent installed in your workspace, ready to invoke any time
- A populated `knowledge/competitors/{name}.md` file on a real competitor — the seed for the self-improvement work later in the course
- First-hand reps on every framework step as a chainable slash command (`/handsonai:analyze`, `/handsonai:deconstruct`, `/handsonai:design`, `/handsonai:build`, `/handsonai:test`, `/handsonai:run`, `/handsonai:improve`)

## Lesson: Recognize When a Workflow Needs to Improve

A brief, conceptual preview of Step 7 of the framework — [Improve](../../ai-workflow-framework/improve/) — anchored to the workflow you just ran. Identify the three signals that tell you a running workflow needs to evolve: hypotheses that never confirm, edge cases where the schema breaks, and drift as your priorities evolve. Improve is the step that never ends — and in the follow-up session, you'll actually do the iteration.

## Lesson: Evolve Your Workflow Into a Self-Improving System

Take the workflow you just shipped and evolve it into a system that gets sharper every time it runs. Apply Karpathy's "LLM Wiki" pattern to its structured context file — structure it with Rules / Facts / Hypotheses sections, implement an ingest / query / lint learning loop, and schedule the workflow to run daily without you. By session end, your workflow's outputs feed a self-improving knowledge base of competitor intelligence — Step 7 (Improve) in action.
