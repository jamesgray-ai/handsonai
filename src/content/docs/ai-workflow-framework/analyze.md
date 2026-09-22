---
title: "Step 1: Analyze Workflows for AI Opportunity"
description: Run a structured audit of your workflows to identify where AI creates value, and register your top candidates in your registry backlog.
---

> **Part of:** [AI Workflow Framework](../)

## What This Is

A structured audit that helps you find where AI fits in your work. The analysis supports two **lenses** — perspectives you can analyze from: **Individual** (workflows you personally perform) and **Organizational** (value chain processes that deliver on business objectives). The AI scans what it already knows about you, asks which lens to use, interviews you with lens-specific questions, then analyzes the results to identify opportunities you'd miss on your own.

| | |
|---|---|
| **What you'll do** | Walk through a guided conversation covering your role, tasks, and pain points |
| **What you'll get** | Three to five candidate workflows registered in your registry backlog, a prioritized report, and one recommendation to build first |
| **Time** | ~15–20 minutes |

## Why This Matters

Most people adopt AI by reacting to problems — they reach for ChatGPT when they're stuck on an email or ask Claude to summarize a document. That's useful, but it misses the bigger picture.

A proactive audit of your workflows can reveal opportunities you'd never notice in the moment: repetitive tasks that could run on autopilot, decisions that would benefit from an AI collaborator, and multi-step processes that could be orchestrated end-to-end.

This step guides an AI through a structured analysis of your work — from either an **individual** perspective (your personal tasks and pain points) or an **organizational** perspective (your business's value chain and strategic processes) — and produces a classified report of opportunities along two dimensions:

- **Autonomy** — How much decision-making does the AI have? **Deterministic** (follows fixed rules), **Guided** (makes bounded decisions), or **Autonomous** (plans and adapts independently)
- **Human Involvement** — Is a human in the loop during execution? **Augmented** (human reviews and steers) or **Automated** (AI runs solo)

## How the Skill Works

The skill runs six phases in order:

1. **Read what's known** — The registry (your business, processes, existing workflows) plus memory and project files. Presented for you to confirm; nothing you've already said is asked again.
2. **Lens selection** — Individual (your own workflows) or Organizational (your business's processes). Inferred and confirmed when obvious.
3. **Discovery interview** — Focused questions, one at a time, only on what step 1 didn't cover.
4. **Opportunity report** — A summary table and detailed cards, grouped by autonomy level, ordered by impact.
5. **Candidates registered** — You pick 3–5; each becomes a backlog Workflow node in your registry, filed under one of your processes, and the skill recommends which to build first (a starter-sized one).
6. **The other lens** — Offered as a later session.

Most people discover 5–15 opportunities across different autonomy levels. Pick three to five to start with.

## How to Use This

This step is facilitated by the **`analyze`** AI Workflow Framework skill. How you get it depends on your platform — see [Set Up the Skills](../skills/) for installation instructions.

**How to start:** Say *"run the analyze skill"* (or *"analyze the workflow"*) — works on every platform. With the plugin installed, Claude Code also accepts `/handsonai:analyze`, and Cowork lists it when you type `/`.

**Platform compatibility:** Claude (Chat, Cowork, Code) ✓ &nbsp;|&nbsp; ChatGPT & Codex ✓ &nbsp;|&nbsp; Gemini (Spark, Enterprise, CLI) ✓ &nbsp;|&nbsp; M365 Copilot ✓ &nbsp;|&nbsp; Cursor / Antigravity ✓

**Start with this prompt:**

```
I'd like to analyze my workflows for AI opportunities. Help me audit
what I do and identify where AI could help.
```

The skill runs the six phases above and produces a categorized opportunity report, and registers your chosen candidates in the registry backlog.

### Example prompts

```
"Help me analyze AI workflow opportunities"
→ Runs the full audit and produces a categorized opportunity
  report with structured workflow candidates

"I want to figure out which parts of my job could benefit from AI"
→ Interactive discovery session followed by a structured report
  with specific, actionable recommendations
```

:::tip[Don't have the skill installed yet?]
Every platform in the course can load it — [Set Up the Skills](../skills/) has the steps, and [analyze.zip](https://github.com/jamesgray-ai/handsonai-plugins/releases/latest/download/analyze.zip) is the direct download. Same methodology, same output format.
:::
:::tip[Classify opportunities with the six primitives]
Once you've identified opportunities, use the [six use case primitives](../../use-cases/) — Content Creation, Research, Coding, Data Analysis, Ideation & Strategy, and Automation — to classify what type of AI work each one involves. This makes it easier to find examples and choose the right building blocks.
:::
:::tip[Best results come from rich context]
The more the AI knows about your actual work, the better the recommendations. If possible, use a tool where you've had many prior conversations or uploaded relevant documents.
:::

## How to Prioritize

- **Start with Deterministic + Augmented** if you're new to AI — lowest risk, easiest to try
- **Move to Deterministic + Automated** once you trust the process — the time savings compound quickly
- **Explore Guided and Autonomous** when you're ready for more AI decision-making

## What Analyze Produces

The **AI Opportunity Report** (`ai-opportunity-report.md`) captures:

- **Report header** — your name, role, date, opportunity count, and top recommendation
- **Summary table** — every opportunity listed with its autonomy level, involvement mode, and impact level
- **Top recommendations** — the 3 highest-priority opportunities with one-sentence rationales
- **Detailed opportunity cards** — grouped by autonomy level (Deterministic → Guided → Autonomous), each with: why it's a good candidate, current pain point, how AI helps, and a practical first step
- **Workflow Candidate Summary** — structured metadata for the workflows you choose to pursue: name, description, trigger, deliverable, autonomy, involvement, pain point, AI opportunity, frequency, priority, reasoning, and lens. Organizational-lens candidates also include business objective, stakeholders, and success metrics.
- **Backlog Workflow nodes** — one per chosen candidate in `registry/workflows/`, linked to the report. Deconstruct picks one up from here.

The Workflow Candidate Summary is the input for [Deconstruct Workflows](../deconstruct/) (Step 2) — the trigger and deliverable fields map directly to the scope check that starts the deconstruction. Its business objective and success metrics also seed Deconstruct's `Value & Measurement` section, so an organizational-lens candidate arrives with two of those answers already drafted.

Analyze does not settle the question of value, and shouldn't. It surveys many workflows to find the few worth pursuing; the outcome that changes, and the number that measures it today, are established once a specific workflow is on the table. Deconstruct asks for both.

See three complete [example reports](../analyze-examples/) to get a feel for the format and level of detail.

## Tips for Better Results

- **Use a tool with memory or projects enabled.** The richer the AI's context about your actual work, the more specific and useful the recommendations will be.
- **Be concrete when answering questions.** "I spend 30 minutes every Monday formatting a status report from three Jira boards" is far more useful than "I do reporting."
- **Run it again in a few weeks.** As you have more conversations and the AI learns more about your work, re-running this prompt will surface new opportunities.
- **Share the output with your team.** Some of the best opportunities come from workflows that span multiple people — your colleagues may see possibilities you don't. The organizational lens is especially useful for this.
- **Try both lenses.** The individual lens surfaces your personal pain points; the organizational lens surfaces value chain opportunities that may have higher strategic impact — worth a separate short session.

## Related

- [Example Reports](../analyze-examples/) — three complete AI Opportunity Reports (Marketing Ops Manager, AI Instructor, and VP of Operations using the organizational lens) showing what the finished deliverable looks like
- **Next step:** Ready to act on an opportunity? Use the [Deconstruct Workflows guide](../deconstruct/) (Step 2) to break it into discrete steps.
- [AI Workflow Framework](../) — the full seven-step methodology
- [Prompts](../../agentic-building-blocks/prompts/)
- [Agents](../../agentic-building-blocks/agents/)
