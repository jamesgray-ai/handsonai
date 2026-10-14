---
title: "Step 1: Analyze Workflows for AI Opportunity"
description: Run a structured audit of your workflows to identify where AI creates value, and register every candidate in your registry backlog.
---

> **Part of:** [AI Workflow Framework](../)

## What This Is

A structured audit that helps you find where AI fits in your work. The analysis supports two **lenses** — perspectives you can analyze from: **Individual** (workflows you personally perform) and **Organizational** (value chain processes that deliver on business objectives). The AI scans what it already knows about you, asks which lens to use, interviews you with lens-specific questions, then analyzes the results to identify opportunities you'd miss on your own.

| | |
|---|---|
| **What you'll do** | Walk through a guided conversation covering your role, tasks, and pain points |
| **What you'll get** | Every candidate workflow registered in your registry backlog, each with a clear name and description, and an opportunity report with the detail |
| **Time** | ~15–20 minutes |

## Why This Matters

Most people adopt AI by reacting to problems — they reach for ChatGPT when they're stuck on an email or ask Claude to summarize a document. That's useful, but it misses the bigger picture.

A proactive audit of your workflows can reveal opportunities you'd never notice in the moment: repetitive tasks that could run on autopilot, decisions that would benefit from an AI collaborator, and multi-step processes that could be orchestrated end-to-end.

This step guides an AI through a structured analysis of your work — from either an **individual** perspective (your personal tasks and pain points) or an **organizational** perspective (your business's value chain and strategic processes) — and produces a report of opportunities, grouped by process. Each one names the work, the pain, the kind of value AI adds (Streamline, Automate, Accelerate, or Create value), what gets produced, and its rough size in your own numbers. Analyze catalogs the work; it doesn't rank it or pick what to build first. You choose that at the start of [Deconstruct (Step 2)](../deconstruct/).

Analyze stays strategic. It names the work, the pain, the kind of value AI adds, and what gets produced — never the tool, connector, or integration that would do it. Those are decided in [Design (Step 3)](../design/). If a report starts naming products or connectors, say: *"Stay strategic — Design picks the tools,"* and the skill will restate the recommendation as an outcome.

## How the Skill Works

The skill runs five phases in order, in three parts you'll see signposted: how we'll look at your work, where the time goes, and your report and your backlog.

1. **Read what's known** — The registry (your business, processes, existing workflows) plus memory and project files. Presented for you to confirm; nothing you've already said is asked again.
2. **Lens selection** — Individual (your own workflows) or Organizational (your business's processes). Inferred and confirmed when obvious.
3. **Discovery interview** — With a registry, a walk through your processes asking where the friction is, tied to your objectives. Without one, focused questions, one at a time, only on what phase 1 didn't cover.
4. **Opportunity report** — A summary table and detailed cards, grouped by process, each with its value lever and rough size. No ranking.
5. **Candidates registered** — You see every workflow, grouped by process, with its name and a one-line description, and can rename, reword, move or leave out any. Each becomes a backlog Workflow node in your registry. The close offers the other lens as a later session.

There's no limit on how many candidates you register: the backlog is your catalog of workflows worth building.

## How to Use This

This step is facilitated by the **`analyze`** AI Workflow Framework skill. How you get it depends on your platform — see [Install the Hands-on AI Plugin](../skills/) for installation instructions.

**How to start:** Say *"run the analyze skill"* (or *"analyze the workflow"*) — works on every platform. With the plugin installed, Claude Code also accepts `/handsonai:analyze`, and Claude lists it when you type `/`.

**Platform compatibility:** Claude (web, desktop, Code) ✓ &nbsp;|&nbsp; ChatGPT & Codex ✓ &nbsp;|&nbsp; Gemini (Spark, Enterprise, CLI) ✓ &nbsp;|&nbsp; M365 Copilot ✓ &nbsp;|&nbsp; Cursor / Antigravity ✓

**Start with this prompt:**

```
I'd like to analyze my workflows for AI opportunities. Help me audit
what I do and identify where AI could help.
```

The skill runs the five phases above, produces an opportunity report, and registers every candidate in the registry backlog.

### Example prompts

```
"Help me analyze AI workflow opportunities"
→ Runs the full audit and produces a prioritized opportunity
  report with structured workflow candidates

"I want to figure out which parts of my job could benefit from AI"
→ Interactive discovery session followed by a structured report
  with specific, actionable recommendations
```

:::tip[Don't have the skill installed yet?]
Every platform in the course can load it — [Install the Hands-on AI Plugin](../skills/) has the steps, and [analyze.zip](https://github.com/jamesgray-ai/handsonai-plugins/releases/latest/download/analyze.zip) is the direct download. Same methodology, same output format.
:::
:::tip[Classify opportunities with the six primitives]
Once you've identified opportunities, use the [six use case primitives](../../use-cases/) — Content Creation, Research, Coding, Data Analysis, Ideation & Strategy, and Automation — to classify what type of AI work each one involves. This makes it easier to find examples and choose the right building blocks.
:::
:::tip[Best results come from rich context]
The more the AI knows about your actual work, the better the recommendations. If possible, use a tool where you've had many prior conversations or uploaded relevant documents.
:::

## Choosing What to Build First

Analyze doesn't choose for you. Deconstruct opens by asking which backlog workflow you want to map, and teaches three tests for a first one: it has a handful of steps, it starts when you decide to start it, and it works from material you already have.

- **Start small** if you're new to AI. A small first workflow teaches the full loop with the least at stake.
- **Follow the value lever you'd use to justify it** — an Automate opportunity pays back in hours you stop spending; an Accelerate one in cycle time; a Create value one in something that didn't exist before.
- **Come back for the ambitious ones** — opportunities where the AI would need to decide more of what happens next are worth building once you've shipped a small one. Design (Step 3) is where that question gets settled.

## What Analyze Produces

The **AI Opportunity Report** (`ai-opportunity-report.md`) captures:

- **Report header** — your name, role, date, lens, and opportunity count
- **Summary table** — every opportunity listed with its process, value lever, and size
- **Detailed opportunity cards** — grouped by process, each with: why it's a good candidate, current pain point, how AI helps, the value lever, its size, and what changes for the business
- **Workflow Candidate Summary** — structured metadata for every registered workflow: name, process, description, trigger, deliverable, value lever, pain point, AI opportunity, frequency, size, and lens. Organizational-lens candidates also include business objective, stakeholders, and success metrics.
- **Backlog Workflow nodes** — one per candidate in `registry/workflows/`, linked to the report. Deconstruct picks one up from here.

The Workflow Candidate Summary is the input for [Deconstruct Workflows](../deconstruct/) (Step 2) — the trigger and deliverable fields map directly to the scope check that starts the deconstruction. Its business objective and success metrics also seed Deconstruct's `Value & Measurement` section, so an organizational-lens candidate arrives with two of those answers already drafted.

Analyze does not settle the question of value, and shouldn't. It surveys many workflows to find the few worth pursuing; the outcome that changes, and the number that measures it today, are established once a specific workflow is on the table. Deconstruct asks for both.

See three complete [example reports](../analyze-examples/) to get a feel for the format and level of detail.

## Tips for Better Results

- **Bring your registry.** Analyze is sharpest when it can walk your real processes. Set it up first with [AI Registry Setup](../../builder-setup/ai-registry-setup/) — about 25 minutes, once — and run Analyze straight after; the setup interview offers to.
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
