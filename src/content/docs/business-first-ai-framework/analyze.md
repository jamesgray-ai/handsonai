---
title: "Step 1: Analyze Workflows for AI Opportunity"
description: Run a structured audit of your workflows to identify where AI creates the most value — produces a prioritized opportunity report with actionable first steps.
---> **Platforms:** `claude` `openai` `gemini` `m365-copilot`

## What This Is

A structured audit that helps you find where AI fits in your work. The analysis supports two lenses: **Individual** (workflows you personally perform) and **Organizational** (value chain processes that deliver on business objectives). The AI scans what it already knows about you, asks which lens to use, interviews you with lens-specific questions, then analyzes the results to surface opportunities you'd miss on your own.

| | |
|---|---|
| **What you'll do** | Walk through a guided conversation covering your role, tasks, and pain points |
| **What you'll get** | A prioritized report of AI opportunities classified by autonomy (Deterministic, Guided, Autonomous) and involvement (Augmented, Automated) — with concrete next steps for each |
| **Time** | ~20–30 minutes for the full conversation |

## Why This Matters

Most people adopt AI by reacting to problems — they reach for ChatGPT when they're stuck on an email or ask Claude to summarize a document. That's useful, but it misses the bigger picture.

A proactive audit of your workflows can reveal opportunities you'd never notice in the moment: repetitive tasks that could run on autopilot, decisions that would benefit from an AI collaborator, and multi-step processes that could be orchestrated end-to-end.

This step guides an AI through a structured analysis of your work — from either an **individual** perspective (your personal tasks and pain points) or an **organizational** perspective (your business's value chain and strategic processes) — and produces a classified report of opportunities along two dimensions:

- **Autonomy** — How much decision-making does the AI have? **Deterministic** (follows fixed rules), **Guided** (makes bounded decisions), or **Autonomous** (plans and adapts independently)
- **Human Involvement** — Is a human in the loop during execution? **Augmented** (human reviews and steers) or **Automated** (AI runs solo)

## How to Use This

This step is facilitated by the **`analyze`** Business-First AI Framework Skill. How you get it depends on your platform — see [Get the Skills](skills.mdx) for installation instructions.

**Start with this prompt:**

```
I'd like to analyze my workflows for AI opportunities. Help me audit
what I do and identify where AI could help.
```

The skill runs a structured audit and produces a categorized opportunity report.

:::tip[If your AI tool doesn't support skills]
Download the skill file from [GitHub](https://github.com/jamesgray-ai/handsonai-plugins/tree/main/plugins/business-first-ai/skills/analyze) and paste it into your system prompt or project instructions. Same methodology, same output format.
:::
:::tip[Classify opportunities with the six primitives]
Once you've identified opportunities, use the [six use case primitives](../use-cases/index.md) — Content Creation, Research, Coding, Data Analysis, Ideation & Strategy, and Automation — to classify what type of AI work each one involves. This makes it easier to find examples and choose the right building blocks.
:::
:::tip[Best results come from rich context]
The more the AI knows about your actual work, the better the recommendations. If possible, use a tool where you've had many prior conversations or uploaded relevant documents.
:::
## What to Expect

Here's what typically happens:

1. The AI reviews what it knows about you and presents a summary. Correct anything that's wrong and fill in gaps.
2. The AI asks which **lens** to use — **Individual** (your personal workflows) or **Organizational** (your business's value chain processes). If your context makes one obvious, it infers and confirms.
3. The AI asks you a series of lens-specific questions. Answer as specifically as you can — concrete examples produce better recommendations than general descriptions.
4. You receive a structured report with a summary table and detailed cards for each opportunity, grouped by category.
5. You pick your top workflow candidates, and the AI formats a **Workflow Candidate Summary** with structured metadata — including trigger, deliverable, and lens — ready for the Deconstruct step.
6. The AI offers to explore the other lens for a more complete picture. You can accept or move on.

Most people discover 5–15 opportunities across different autonomy levels. Pick three to start with.

### How to Prioritize

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

The Workflow Candidate Summary is the input for [Deconstruct Workflows](deconstruct/index.md) (Step 2) — the trigger and deliverable fields map directly to the scope check that starts the deconstruction.

See three complete [example reports](analyze-examples.md) to get a feel for the format and level of detail.

## Tips for Better Results

- **Use a tool with memory or projects enabled.** The richer the AI's context about your actual work, the more specific and useful the recommendations will be.
- **Be concrete when answering questions.** "I spend 30 minutes every Monday formatting a status report from three Jira boards" is far more useful than "I do reporting."
- **Run it again in a few weeks.** As you have more conversations and the AI learns more about your work, re-running this prompt will surface new opportunities.
- **Share the output with your team.** Some of the best opportunities come from workflows that span multiple people — your colleagues may see possibilities you don't. The organizational lens is especially useful for this.
- **Try both lenses.** The individual lens surfaces your personal pain points; the organizational lens surfaces value chain opportunities that may have higher strategic impact. The skill offers to run both.

## Related

- [Example Reports](analyze-examples.md) — three complete AI Opportunity Reports (Marketing Ops Manager, AI Instructor, and VP of Operations using the organizational lens) showing what the finished deliverable looks like
- **Next step:** Ready to act on an opportunity? Use the [Deconstruct Workflows guide](deconstruct/index.md) (Step 2) to break it into discrete steps.
- [Business-First AI Framework](index.md) — the full seven-step methodology
- [Prompts](../agentic-building-blocks/prompts/index.md)
- [Agents](../agentic-building-blocks/agents/index.md)
