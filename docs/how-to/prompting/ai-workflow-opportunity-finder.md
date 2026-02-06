---
title: How to Find AI Workflow Opportunities
description: Use this prompt template to discover where AI can help automate, augment, or orchestrate your workflows.
---

# How to Find AI Workflow Opportunities

> **Platforms:** `claude` `openai` `gemini`

!!! info "Business-First AI Framework — Phase 1: Discover"
    This guide is **Phase 1** of the [Business-First AI Framework](../../business-first-ai-framework.md) — discovering where AI fits in your workflows.

## What This Is

A structured audit that helps you find where AI fits in your work. The AI scans what it already knows about you, interviews you about your workflows, then analyzes the results to surface opportunities you'd miss on your own.

| | |
|---|---|
| **What you'll do** | Walk through a guided conversation covering your role, tasks, and pain points |
| **What you'll get** | A prioritized report of AI opportunities across three levels — Collaborative AI, Deterministic Workflows, and Multi-Agent Systems — with concrete next steps for each |
| **Time** | ~20–30 minutes for the full conversation |

## Why This Matters

Most people adopt AI by reacting to problems — they reach for ChatGPT when they're stuck on an email or ask Claude to summarize a document. That's useful, but it misses the bigger picture.

A proactive audit of your workflows can reveal opportunities you'd never notice in the moment: repetitive tasks that could run on autopilot, decisions that would benefit from an AI collaborator, and multi-step processes that could be orchestrated end-to-end.

This prompt template guides an AI through a structured analysis of your work and produces a categorized report of opportunities across three levels:

- **Collaborative AI** — Tasks where you and AI work together in real time (drafting, brainstorming, reviewing)
- **Deterministic Workflows** — Repeatable processes that AI can execute reliably with little or no supervision
- **Multi-Agent Systems** — Complex workflows where multiple AI agents coordinate to handle different steps

## How to Use This

There are two ways to run Phase 1, depending on which tools you use:

### Option A: Prompt template (any AI tool)

Use this if you're working in Claude, ChatGPT, Gemini, or M365 Copilot.

1. **Make sure memory is enabled** in your AI tool of choice — this lets the AI draw on everything it knows about you from past conversations
2. **Copy the prompt** from the code block below
3. **Paste it into any conversation** — the AI will automatically scan its memory for context about your role, tasks, and workflows
4. **Review the output** and pick one or two opportunities to pilot first

### Option B: Claude skill

Use this if you're on the Claude platform (Claude Code, Claude.ai, or Cowork). The `finding-ai-opportunities` skill from the [Business First AI plugin](../../plugins/business-first-ai.md) runs the same process interactively.

**Claude Code or Cowork** — install the plugin and the skill is available immediately:

1. **Install the plugin** — `/plugin install business-first-ai@handsonai`
2. **Start with this prompt:**
    ```
    I'd like to find AI opportunities in my workflows. Help me audit
    what I do and identify where AI could help.
    ```
3. **Review the output** — the report is saved to `outputs/ai-opportunity-report.md`

**Claude.ai** — upload the skill as a ZIP file:

1. **Zip the skill folder** from `~/.claude/plugins/marketplaces/handsonai/plugins/business-first-ai/skills/finding-ai-opportunities/`
2. **Upload it** in Claude.ai under **Settings > Capabilities > Upload skill**
3. **Start a new chat** with the same prompt above — Claude uses the skill automatically

For detailed upload instructions, see [Using Skills in Claude.ai](../../plugins/using-plugins.md#using-skills-in-claudeai-web).

Both options follow the same three-step process and produce the same structured report. Choose whichever fits your workflow.

!!! tip "Best results come from rich context"
    The more the AI knows about your actual work, the better the recommendations. If possible, use a tool where you've had many prior conversations or uploaded relevant documents.

## The Prompt Template

```text
You are an AI Workflow Strategist with deep expertise in business process optimization and AI capabilities. Your job is to help me discover concrete opportunities where AI can improve my workflows.

Work through the following three steps in order.

---

## Step 1 — Memory & History Scan

Before asking me anything, review everything you already know about me from our conversation history, your memory, project files, or any other context available to you.

From that context, identify and list:
- My role, responsibilities, and domain
- Recurring tasks or requests I perform
- Pain points, frustrations, or bottlenecks I've mentioned
- Workflows or processes I've described or demonstrated
- Tools and platforms I use regularly
- Any goals or priorities I've shared

Present your findings as a brief summary so I can confirm or correct them before we continue. If you have no prior context about me, say so and move directly to Step 2.

---

## Step 2 — Targeted Discovery Interview

Based on gaps in your understanding (or starting from scratch if Step 1 had no context), ask me focused questions to build a complete picture. Cover these areas:

1. **Role & responsibilities** — What is your role? What are you accountable for?
2. **Repetitive tasks** — What tasks do you perform daily or weekly that feel repetitive, tedious, or low-value?
3. **Information synthesis** — Where do you spend time gathering, combining, or making sense of information from multiple sources?
4. **Multi-step processes** — What workflows involve multiple handoffs, approvals, or sequential steps?
5. **Quality & consistency** — Where do errors, inconsistencies, or quality issues tend to creep in?
6. **Communication overhead** — What recurring communications (status updates, reports, summaries) take more time than they should?
7. **Decision-making** — What decisions require you to weigh multiple factors or reference past precedents?

Ask these questions conversationally — not all at once. Use my answers to ask smart follow-up questions. Continue until you have enough detail to generate meaningful recommendations.

---

## Step 3 — Opportunity Analysis & Report

Once you have sufficient context, produce a structured report.

### Summary Table

Start with a table listing every opportunity:

| # | Opportunity | Category | Impact |
|---|------------|----------|--------|
| 1 | [Name] | Collaborative AI / Deterministic Workflow / Multi-Agent System | High / Medium / Low |

### Detailed Opportunity Cards

Then for each opportunity, provide a detailed card in this format:

---

**[#] [Opportunity Name]**

**Category:** Collaborative AI | Deterministic Workflow | Multi-Agent System

**Why it's a good candidate:**
[What characteristics of this task make it well-suited for AI — e.g., it's repetitive, pattern-based, language-heavy, has clear inputs/outputs, etc.]

**Current pain point:**
[What's slow, error-prone, inconsistent, or draining about how this is done today]

**How AI helps:**
[Specific, concrete description of what AI would do — not vague "AI could help" but exactly what it would take as input, what it would produce, and how it fits into the workflow]

**Getting started:**
[A practical, low-effort first step to pilot this — something achievable this week]

---

### Category Definitions

Use these definitions when categorizing:

- **Collaborative AI**: Human and AI work together in real time. The human drives the process; AI contributes suggestions, drafts, analysis, or feedback. Examples: co-writing, brainstorming, code review, data analysis.

- **Deterministic Workflow**: A repeatable process with clear inputs, rules, and outputs that AI can execute reliably with minimal supervision. Examples: formatting reports, processing forms, generating routine communications, data transformation.

- **Multi-Agent System**: A complex workflow where multiple AI agents (or AI + automation tools) coordinate across steps. Requires orchestration. Examples: research → analysis → report generation pipelines, intake → triage → routing systems, monitoring → alerting → response workflows.

Group the detailed cards by category. Within each category, order opportunities from highest to lowest impact.
```

## What to Expect

After pasting the prompt, here's what typically happens:

1. **Step 1** — The AI reviews what it knows about you and presents a summary. Correct anything that's wrong and fill in gaps.
2. **Step 2** — The AI asks you a series of questions. Answer as specifically as you can — concrete examples produce better recommendations than general descriptions.
3. **Step 3** — You receive a structured report with a summary table and detailed cards for each opportunity, grouped by category.

Most people discover 5–15 opportunities across the three categories. Don't try to pursue all of them — pick 1–2 from the "Getting started" suggestions and pilot those first.

### How to Prioritize

- **Start with Collaborative AI** opportunities if you're new to AI — they're the easiest to try and lowest risk
- **Move to Deterministic Workflows** once you've identified a process you repeat often — the time savings compound quickly
- **Explore Multi-Agent Systems** when you have experience with the other two categories and need to automate complex, multi-step processes

## Tips for Better Results

- **Use a tool with memory or projects enabled.** The richer the AI's context about your actual work, the more specific and useful the recommendations will be.
- **Be concrete when answering questions.** "I spend 30 minutes every Monday formatting a status report from three Jira boards" is far more useful than "I do reporting."
- **Run it again in a few weeks.** As you have more conversations and the AI learns more about your work, re-running this prompt will surface new opportunities.
- **Share the output with your team.** Some of the best opportunities come from workflows that span multiple people — your colleagues may see possibilities you don't.

## Related

- **Next step:** Ready to act on an opportunity? Use the [Workflow Deconstruction guide](workflow-deconstruction-meta-prompt.md) (Phase 2) to break it into AI building blocks.
- [Business-First AI Framework](../../business-first-ai-framework.md) — the full three-phase methodology
- [Prompt Engineering Fundamentals](../../fundamentals/prompt-engineering/README.md)
- [Agents & Tools Overview](../../fundamentals/agents-and-tools/README.md)
