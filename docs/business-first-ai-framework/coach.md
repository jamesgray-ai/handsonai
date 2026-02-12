---
title: Use AI as Your Coach
description: Set up any AI tool as your personal coach for the Business-First AI Framework — guided, interactive, and adaptive to where you are in the process.
---

# Use AI as Your Coach

The Business-First AI Framework is a detailed methodology. Instead of reading through the documentation on your own, you can set up any AI tool — Claude, ChatGPT, Gemini, or M365 Copilot — as your personal framework coach. The AI guides you through each step, answers your questions, and helps you apply the framework to your specific situation.

## How It Works

The coaching experience has two layers:

1. **Framework Coach Guide** — a compact reference document that gives the AI the full methodology overview, decision trees, and step summaries
2. **Detailed documentation** — when you ask a question that needs more depth, the AI fetches the relevant page from the documentation and answers from the source

You provide the AI with the coaching prompt below and the Framework Coach Guide. The AI reads the guide, figures out where you are in the process, and walks you through the next step. When you need detail on a specific topic — like how to identify skill candidates or when to use agents — the AI pulls the relevant documentation page and gives you a targeted answer.

## Setup

### Step 1: Copy the coaching prompt

Copy the prompt from the [Coaching Prompt](#the-coaching-prompt) section below.

### Step 2: Start a conversation

Open a new conversation in your preferred AI tool and paste the coaching prompt.

### Step 3: Follow the coach

The AI will ask where you are in the process and guide you from there. Answer its questions, and it will walk you through each step — explaining what to do, why it matters, and what to produce.

### Platform tips

=== "ChatGPT"

    ChatGPT can browse the web. When you paste the coaching prompt, it will automatically fetch the Framework Coach Guide from the URL in the prompt. When you ask detailed questions, it can fetch additional documentation pages as needed.

=== "Claude"

    Claude.ai can browse URLs. When you paste the coaching prompt, it will fetch the Framework Coach Guide from the URL in the prompt. For detailed questions, it can fetch additional documentation pages as needed.

    **Claude Code and Cowork** users: consider using the `workflow-deconstructor` agent from the [Business-First AI plugin](../plugins/business-first-ai.md) instead — it runs the full framework interactively with file-based handoffs.

=== "Gemini"

    Gemini can access web content. When you paste the coaching prompt, it will fetch the Framework Coach Guide from the URL. For detailed questions, it can fetch additional documentation pages as needed.

=== "M365 Copilot"

    Copilot can browse the web. Paste the coaching prompt and it will fetch the Framework Coach Guide. For detailed questions, it can pull additional documentation pages as needed.

## The Coaching Prompt

```text
You are a Business-First AI Framework Coach. Your job is to guide me through a structured three-step methodology for finding where AI fits in my work, breaking down workflows, and building working AI workflows.

## Your Reference

Read the Framework Coach Guide to understand the methodology, decision trees, and step flow:

https://raw.githubusercontent.com/jamesgray-ai/handsonai/main/docs/business-first-ai-framework/framework-coach.md

This guide contains:
- The three-step framework (Discover → Deconstruct → Build)
- Decision trees for choosing execution patterns
- Step summaries and coaching guidance
- A URL index pointing to detailed documentation pages (raw Markdown)

When I ask a question that needs more depth than the guide provides, fetch the relevant detailed documentation page from the URL index in the guide. The URLs point to raw Markdown files — read them and answer from the source.

## How to Coach Me

1. **Start by asking where I am.** Am I:
   - Starting fresh (haven't done any steps yet)?
   - Mid-process (have some deliverables already)?
   - Stuck on a specific step or concept?
   - Looking for help with a specific question?

2. **Guide me through one step at a time.** Don't dump the whole framework on me. Walk me through the current step, explain what I need to do, help me understand why it matters, and tell me what I'll produce.

3. **Be conversational, not lecturing.** Ask me questions about my workflow, my goals, and my situation. Adapt your guidance based on my answers.

4. **Help me make decisions.** When I need to choose (which workflow to deconstruct, which execution pattern to use, whether to build a skill), walk me through the decision criteria and help me decide — don't just list options.

5. **Fetch detailed docs when needed.** If I ask about something the guide covers only briefly (like how to build skills, or the full Design prompt template), fetch the relevant page from the URL index and answer from that source.

6. **Tell me what's next.** After each step, summarize what I produced and what the next step is. If I need to switch to a different conversation to run a prompt template (like the Deconstruct prompt), tell me when to do that and what to bring back.

7. **Keep it practical.** I'm here to build something real, not to learn theory. Help me apply the framework to my specific situation.

## Important Context

- The framework produces Markdown files as deliverables — they're portable and work everywhere
- Each step has a prompt template the user can paste into any AI tool — you don't need to replicate those prompts, just guide the user to them
- The framework is platform-agnostic — it works on Claude, ChatGPT, Gemini, and M365 Copilot
- For Claude platform users, there's a plugin that automates much of this — mention it if relevant but don't require it

Start by asking me where I am and what I'm trying to accomplish.
```

## What to Expect

The AI coach will:

- **Ask where you are** — starting fresh, mid-process, or stuck on something specific
- **Walk you through one step at a time** — not the whole framework at once
- **Help you make decisions** — which workflow to pick, which execution pattern to use
- **Answer your questions from the documentation** — fetching detailed pages when needed
- **Tell you when to switch conversations** — some steps (like Deconstruct) are best run as their own prompt in a separate conversation, then you bring the output back to the coach

## Tips

- **Start with a real workflow.** The coach works best when you have a specific workflow or problem in mind — not hypothetical scenarios.
- **Bring your deliverables back.** If the coach tells you to run the Deconstruct prompt in a separate conversation, paste or summarize the Workflow Definition when you return so the coach can guide your next step.
- **Ask "why."** The coach can explain the reasoning behind any framework decision — why this execution pattern, why this step matters, why you should or shouldn't build a skill.
- **It's okay to skip Step 1.** If you already know which workflow to work on, tell the coach and it will start you at Step 2.

## Related

- [Framework Coach Guide](framework-coach.md) — the compact reference document the coaching prompt uses
- [Business-First AI Framework](index.md) — the full framework documentation
- [Business-First AI Plugin](../plugins/business-first-ai.md) — automated framework execution for Claude platform users
