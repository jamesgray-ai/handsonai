---
title: Context
description: Create the context your workflow needs — the documents, data, rules, and examples that make AI output specific to your business.
---

# Context

> **Part of:** [Build Workflows](index.md)

!!! tip "New to context as a building block?"
    See [Agentic Building Blocks > Context](../../agentic-building-blocks/context/index.md) for definitions, examples, and cross-platform implementation details.

## What This Is

Context is all the knowledge the AI needs to do your workflow well but doesn't have within the model itself. Your company's style guide, your buyer persona, your CRM data, your scoring rubric — the AI has broad general knowledge, but it doesn't know your specific business. Context bridges that gap. Without the right context, even a perfect prompt produces generic output.

Your AI Building Block Map includes a **Context Inventory** — a table listing every piece of context the workflow needs. This page shows you how to create the ones that don't exist yet.

| | |
|---|---|
| **What you'll do** | Open your Building Block Map's Context Inventory, identify which artifacts need creation, and create them |
| **What you'll get** | A set of context artifacts ready to attach or pre-load when running your workflow |
| **Time** | Varies by artifact count (15-60 minutes for most workflows) |

## What Context Looks Like

Context isn't just documents. It's any information from your world that the AI needs to produce specific, accurate output. Here are common types with examples:

### Documents and files

Written materials that capture your standards, knowledge, or requirements.

| Example | What it gives the AI |
|---------|---------------------|
| Buyer persona | Who you're targeting — job titles, pain points, qualifying criteria |
| Brand style guide | How to sound like your company — tone, vocabulary, formatting rules |
| Product documentation | What your product does, features, pricing, competitive positioning |
| Company policies | Rules and constraints the workflow must respect |
| Past reports or approved examples | What "good output" looks like — the AI matches quality and format |
| Output templates | The exact structure you want results delivered in |

### Data from applications

Information pulled from the tools your team already uses. When connected via MCP, AI can access this directly. Otherwise, you export and attach it.

| Source | What it gives the AI |
|--------|---------------------|
| CRM (HubSpot, Salesforce) | Deal pipeline, contact history, account details |
| Project management (Jira, Asana, Linear) | Task status, sprint data, issue history |
| Analytics (Google Analytics, Mixpanel) | Traffic patterns, conversion data, user behavior |
| Email and calendar | Meeting context, conversation threads, scheduling history |
| Support tickets (Zendesk, Intercom) | Customer issues, resolution patterns, FAQ trends |

### Spreadsheets and databases

Structured data the AI processes, analyzes, or references during the workflow.

| Example | What it gives the AI |
|---------|---------------------|
| Customer lists or segments | Who to target, filter, or prioritize |
| Transaction or sales data | Numbers to analyze, trends to surface |
| Survey responses or feedback | Voice-of-customer data to synthesize |
| Pricing tables or rate cards | Accurate pricing for proposals or quotes |
| Inventory or product catalogs | What's available, specifications, categories |

### Rules and criteria

Logic that tells the AI how to make decisions within the workflow. These are critical — without them, the AI guesses instead of following your standards.

| Example | What it gives the AI |
|---------|---------------------|
| Scoring rubric | How to evaluate and rank (lead scoring, content grading, vendor comparison) |
| Qualification criteria | What makes something pass or fail (lead qualification, application screening) |
| Classification rules | How to categorize items (support ticket routing, content tagging) |
| Decision trees | If/then logic for specific scenarios (escalation paths, approval flows) |
| Compliance checklists | Required checks before output is finalized |

### Domain knowledge

Specialized information about your industry or field that the AI's general training doesn't cover well.

| Example | What it gives the AI |
|---------|---------------------|
| Industry terminology glossary | Correct usage of field-specific terms |
| Regulatory requirements | Constraints the workflow must satisfy (HIPAA, SOC 2, GDPR) |
| Competitive intelligence | How competitors position, price, or operate |
| Internal process documentation | How your team actually does things (not how the org chart says) |

## How to Create Missing Context

Your Building Block Map's Context Inventory identifies what the workflow needs and whether each item already exists or needs to be created. To fill the gaps:

1. **Open your Building Block Map** — Find the Context Inventory table from your [AI Building Block Map](../deconstruct/building-blocks.md)
2. **Focus on "Needs Creation" items** — These are the gaps you need to fill
3. **Start with rules and criteria** — Scoring rubrics, qualification criteria, and decision logic are often required for the workflow to function correctly. Without them, the AI guesses instead of following your standards.
4. **Use the "Key Contents" column as your outline** — The Building Block Map already identified what each artifact should contain. A buyer persona artifact might list: target job titles, company size range, industry verticals, pain points, and qualifying criteria. Use that as your drafting checklist.
5. **Create each artifact** — Most context works well as a standalone Markdown file (e.g., `buyer-persona.md`, `scoring-rubric.md`). Data exports work as CSV or spreadsheet files.
6. **Then fill in background knowledge** — Documents like style guides and product specs improve output quality but aren't usually blockers. Create these after the critical pieces are in place.

## Where Context Lives

How you provide context depends on your platform and how often you run the workflow:

| Method | Best for | How it works |
|--------|----------|-------------|
| **Attached to a conversation** | One-off runs, infrequent workflows | Drag and drop files when you paste the prompt |
| **In a Project** | Frequent workflows (weekly+) | Upload as project files that persist across conversations. See [Projects](projects.md). |
| **Connected via MCP** | Live data from apps and databases | AI reads directly from the source — no manual export needed. See [MCP](mcp.md). |
| **In CONTEXT.md files** | Developer workflows (Claude Code) | Markdown files named `CONTEXT.md` placed in your project folder — Claude Code (an AI coding tool that runs in the terminal) reads them automatically when you start a conversation |

When you run the [Prompt](prompt.md) step later, the generated output will include a **Where to Run** section that recommends which approach fits your workflow based on how many context files you have and how often you'll run it.

## Testing Your Context

Run a workflow step with and without a context artifact. Compare the output quality. This tells you which artifacts are truly essential vs. nice-to-have.

If the output is noticeably worse without an artifact, it's essential — keep it. If the output is roughly the same, the artifact is optional — you can deprioritize or skip it.

## What's Next

With your context artifacts created, set up a [Project](projects.md) workspace if your workflow runs frequently, then build [Skills](skills.md) for complex steps before generating your [Prompt](prompt.md).
