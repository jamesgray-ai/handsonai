---
date: 2026-02-10
authors:
  - jamesgray
categories:
  - Announcements
description: "Why I built the Hands-on AI Playbook -- a free, open-source resource with a framework, building blocks, and ready-made tools for applied AI."
title: "I Built an Open-Source AI Playbook for Builders. Here's What's Inside."
---If you have a business workflow you want to make AI-first, the last thing you need is another slick demo. You need clarity — what are the building blocks, how do they fit together, and how do you go from idea to production?

That's what the Hands-on AI Playbook is. Complex AI topics distilled into clear frameworks, building blocks, and practical tools so builders can stop experimenting and start operationalizing.

And by builders, I don't mean developers. If you're a leader, entrepreneur, or professional with a business idea and the willingness to get hands-on — you're a builder.

<!-- more -->

## Why I Built This

After working with 6,000+ executives — at Berkeley Haas, through enterprise AI programs, and in hands-on cohorts — I kept seeing the same pattern. People would show up excited about AI. They'd tried the tools. They'd written some prompts. But they couldn't close the distance between experimenting and executing.

The gap wasn't about prompts. It was about *thinking*. People didn't need another "50 prompts for marketers" listicle. They needed a framework for figuring out *where* AI fits in their work and *how* to build it into their workflows — systematically, not randomly.

So I started building. Openly, publicly, on GitHub. Because I believe AI knowledge should be free and open to everyone.

Here's the thing — we all have a finite amount of time. The best gift I can give anyone is the gift of time and clarity to maximize their impact. My hope is that this playbook shortens the distance between where you are and what you're capable of — bringing the future forward, so you can spend your time on the work that actually matters.

## What's Inside

The playbook is built in four layers. Each one takes you deeper.

### Layer 1: A Framework for Going from Idea to Production

Most people have a sense of which workflows could benefit from AI. The hard part is going from that idea to something that actually runs — reliably, repeatedly, in the real world.

The [Business-First AI Framework](../../business-first-ai-framework/index.md) guides you through that entire journey:

1. **[Analyze](../../business-first-ai-framework/analyze.md)** — Run a structured audit of your workflows to identify where AI creates the most value
2. **[Deconstruct](../../business-first-ai-framework/deconstruct/index.md)** — Break those workflows into discrete steps and map each one to AI building blocks
3. **[Build](../../business-first-ai-framework/build/index.mdx)** — Turn that analysis into a working AI workflow, ready for production

You don't need to be technical to use any of this. The framework works on paper, in a conversation with any AI tool, or with installable plugins that walk you through it step by step. The Analyze step takes 20 minutes and produces a prioritized list of AI opportunities — a tangible output in one sitting.

### Layer 2: Use Cases — Where AI Creates Value

The playbook includes [six use case primitives](../../use-cases/index.md) — [Content Creation](../../use-cases/content-creation/index.md), [Research](../../use-cases/research/index.md), [Coding](../../use-cases/coding/index.md), [Data Analysis](../../use-cases/data-analysis/index.md), [Ideation & Strategy](../../use-cases/ideation-and-strategy/index.md), and [Automation](../../use-cases/automation/index.md) — adapted from OpenAI's analysis of 600+ enterprise AI deployments. These primitives describe *what type of work* AI actually does in the real world. They give you a classification system so you can look at any workflow and immediately know which category it falls into and which building blocks to reach for.

### Layer 3: The Building Blocks

Every AI workflow — from a single prompt to a multi-agent pipeline — is assembled from eleven building blocks organized in three layers:

- **[Model](../../agentic-building-blocks/models/index.md)** — The AI engine that powers everything
- **[Prompt](../../agentic-building-blocks/prompts/index.md)** — Instructions you give the AI
- **[Context](../../agentic-building-blocks/context/index.md)** — Background knowledge the AI needs (your data, your docs, your domain)
- **[Project](../../agentic-building-blocks/projects/index.md)** — A persistent workspace that holds everything together
- **[Memory](../../agentic-building-blocks/memory/index.md)** — Accumulated knowledge the AI retains across conversations
- **[Skill](../../agentic-building-blocks/skills/index.mdx)** — A reusable routine the AI can invoke on demand
- **[Agent](../../agentic-building-blocks/agents/index.md)** — An autonomous AI that plans and executes multi-step work
- **[MCP](../../agentic-building-blocks/mcp/index.md)** — A connector that lets AI access external tools and data
- **[API](../../agentic-building-blocks/api/index.md)** — Programmatic interface for calling AI from code
- **[SDK](../../agentic-building-blocks/sdk/index.md)** — Frameworks for building AI workflows and agent systems
- **[CLI](../../agentic-building-blocks/cli/index.md)** — Terminal-native interface for interacting with AI

These are platform-agnostic concepts. The playbook maps each block across Claude, ChatGPT, Gemini, and M365 Copilot in a single [comparison table](../../agentic-building-blocks/index.md). So instead of learning four different systems, you learn the blocks once and apply them everywhere.

This is the vocabulary that makes AI adoption repeatable. Once you understand building blocks, you can look at any workflow and say: "This needs a skill with context and an MCP connection" — regardless of which platform you're using.

### Layer 4: Accelerators — Domain Expertise You Can Install

As I learn, I codify that knowledge into AI agents and skills — pre-built tools you can install in one command to accelerate your own learning and implementation. This is an evolving library, not a finished product.

The playbook's [Plugin Marketplace](../../use-the-playbook/build/index.md) is where these live. The Business-First AI plugin alone packages 8 agents, 6 skills, and 3 prompts that implement the entire [Business-First AI Framework](../../business-first-ai-framework/index.md) as executable tools. Tell it "help me find where AI can improve my workflows" and it runs a structured audit. Tell it "deconstruct my client onboarding process" and it walks you through the full analysis.

There's also a [Builder Tools Setup Guide](../../builder-setup/index.md). This is where I see people get stuck — the tools that let you build and run real AI workflows are unfamiliar to most people. Terminal, Git, AI coding CLIs — many of these will be new. But they're what unlock the ability to go from idea to production. The guide walks you through each tool with checkboxes to track your progress. One VP of Product used it to go from zero terminal experience to a fully configured builder toolkit in a single afternoon.

And the playbook is full of patterns, walkthroughs, and direct answers to the questions that come up most often — from "[what is a system prompt?](../../agentic-building-blocks/prompts/questions/what-is-a-system-prompt.md)" to "[how do I schedule an AI agent to run automatically?](../../platforms/claude/subagents/scheduling-subagents.mdx)"

## Who It's For

Anyone stuck between "experimenting" and "executing" — leaders auditing where AI fits, entrepreneurs building their first AI-powered workflow, professionals who want to get hands-on and take an idea all the way to production.

No coding experience required for the strategy content. The builder content scales from first-time terminal users to teams orchestrating multi-agent pipelines.

## Go Build Something

In a world changing this fast, there are no shortcuts. You have to get hands-on with the tools. You have to touch them, experiment, and develop your own sense of what's possible.

I've trained CEOs and C-suite leaders on the same tools covered in this playbook. Every one of them came out with greater clarity — not because AI gave them answers, but because getting hands-on calibrated their mindset to what's actually possible.

That's my challenge to you: start small. Build the muscle of a business-first approach to AI. Value creation isn't just the power of the tools — it's your ability to innovate from within and evolve what you're capable of. That inner transformation is what lets you bring out your full potential, together with AI, to make your ideas come to life.

The Hands-on AI Playbook is free, open-source, and always evolving.

**Start here:** Head to [Analyze Workflows](../../business-first-ai-framework/analyze.md) and run the audit. In 20 minutes, you'll have a prioritized list of AI opportunities.

Or jump to what interests you:

- [Business-First AI Framework](../../business-first-ai-framework/index.md)
- [Use Cases](../../use-cases/index.md)
- [Agentic Building Blocks](../../agentic-building-blocks/index.md)
- [Plugin Marketplace](../../use-the-playbook/build/index.md)
- [Builder Tools Setup Guide](../../builder-setup/index.md)

*Originally published on [Graymatter](https://graymatter.jamesgray.ai).*
