---
title: Run the Framework End-to-End
description: Run the AI Workflow Framework end-to-end on a real workflow — Competitive Intelligence — and ship a working skill and agent in your workspace.
---

In this exercise you run the AI Workflow Framework end-to-end yourself, live in class. Starting from a pre-built Workflow Requirements, you invoke `/design`, `/build`, `/test`, and `/run` on a **Competitive Intelligence** workflow — shipping a `competitor-research` skill and `competitor-brief` agent that produce a structured brief on a real competitor. In a follow-up session, you'll evolve that workflow into a self-improving system.

## Lesson: Ship a Workflow Using the AI Workflow Framework

Run the framework end-to-end yourself in Cowork (or Claude Code — same slash commands). Starting from a pre-built Workflow Requirements, you invoke `/design`, `/build`, `/test`, and `/run` — generating a `competitor-research` skill and `competitor-brief` agent from your approved spec, then running the workflow on a real competitor. Watch a structured context file get produced on the first run.

### Hands-on assignment

**Starting point:** a pre-built Workflow Requirements (download below).
**Ending point:** a shipped skill + agent producing a brief on a real competitor.

1. **`/design`** — Turn the requirements into an approved Design Spec (plan mode, collaborative). See the [Design step docs](../../ai-workflow-framework/design/).
2. **`/build`** — Generate the `competitor-research` skill and `competitor-brief` agent from your spec. See the [Build step docs](../../ai-workflow-framework/build/).
3. **`/test`** — Validate the building blocks before trusting them with real input. See the [Test step docs](../../ai-workflow-framework/test/).
4. **`/run`** — Invoke the workflow on a real competitor; watch `knowledge/competitors/{name}.md` emerge. See the [Run step docs](../../ai-workflow-framework/run/).

### Download the Workflow Requirements

The Step 2 (Deconstruct) artifact is pre-built so we can spend class time running the rest of the framework on it.

<a href="/assets/courses/competitive-intelligence-workflow-requirements.md" download="competitive-intelligence-workflow-requirements.md"><strong>Download the Competitive Intelligence — Workflow Requirements (.md)</strong></a>

### Set up your workspace before class

Do these steps in the folder where you run Cowork or Claude Code.

**Step 1 — get a `registry/` folder.** Pick whichever is true for you:

- **Starting fresh, no workspace yet:** instantiate the template repo.
  1. Open the AI Registry template repository your instructor shared (or ask your AI assistant: *"Where's the AI Registry template repo?"*).
  2. Click the green **Use this template** button near the top of the page, then **Create a new repository**.
  3. Clone the new repository to your computer (or open it directly in Cowork) — it arrives with an empty `registry/` folder already in place.
- **Already have a workspace:** open it in your AI assistant and say *"Set up my AI registry."* — it creates the `registry/` folder for you.

**Step 2 — create the workflow folder and save the download.** Inside your workspace, create a folder named `outputs`, and inside it a folder named `competitive-intelligence-brief`. Save the download as `requirements.md` inside that folder, so the full path is `outputs/competitive-intelligence-brief/requirements.md`. (Rename the downloaded file — the framework skills look for `requirements.md`.)

**Step 3 — hand-type the first Workflow node.** In `registry/workflows/`, create a file named `competitive-intelligence-brief.md` and paste in exactly this:

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
- First-hand reps on every framework step as a chainable slash command (`/analyze`, `/deconstruct`, `/design`, `/build`, `/test`, `/run`, `/improve`)

## Lesson: Recognize When a Workflow Needs to Improve

A brief, conceptual preview of Step 7 of the framework — [Improve](../../ai-workflow-framework/improve/) — anchored to the workflow you just ran. Identify the three signals that tell you a running workflow needs to evolve: hypotheses that never confirm, edge cases where the schema breaks, and drift as your priorities evolve. Improve is the step that never ends — and in the follow-up session, you'll actually do the iteration.

## Lesson: Evolve Your Workflow Into a Self-Improving System

Take the workflow you just shipped and evolve it into a system that gets sharper every time it runs. Apply Karpathy's "LLM Wiki" pattern to its structured context file — structure it with Rules / Facts / Hypotheses sections, implement an ingest / query / lint learning loop, and schedule the workflow to run daily without you. By session end, your workflow's outputs feed a self-improving knowledge base of competitor intelligence — Step 7 (Improve) in action.
