---
title: Prompts
description: The Prompt building block — natural language instructions that drive every AI interaction across all platforms
---

# Prompts

> **Platforms:** `claude` `openai` `gemini` `m365-copilot`

## What Prompts Are

**Prompts** are the instructions you provide to an AI in natural language during a conversation. They're ephemeral, conversational, and reactive — you provide context and direction in the moment.

Every AI interaction starts with a prompt. It's the most fundamental building block — a well-crafted prompt is often all you need to get useful output, without any of the other blocks.

## Key Characteristics

- **Natural language** — you write prompts the way you'd explain a task to a knowledgeable colleague
- **Ephemeral** — used in the moment, within a single conversation turn
- **Reactive** — you adjust and refine based on the AI's response
- **Range of complexity** — from a single sentence to a detailed multi-section instruction with role, task, context, and format guidance

## When to Use a Prompt Alone

A prompt by itself is sufficient when:

- The task is a one-off (no need to repeat it)
- The AI's training data has everything it needs (no specialized knowledge required)
- The output format is simple or you can describe it inline
- You don't need persistence across conversations

When you find yourself writing the same prompt repeatedly or needing to attach the same context every time, that's a signal to consider other building blocks — [Context](../context/index.md), [Projects](../projects/index.md), or [Skills](../skills/index.md).

## Anatomy of an Effective Prompt

The best prompts address four elements:

| Element | What It Covers | Example |
|---------|---------------|---------|
| **Role** | Who the AI should be — expertise, perspective, personality | "You are a senior copywriter specializing in B2B SaaS" |
| **Task** | What the AI should do — the specific action or output | "Write three subject line options for this product launch email" |
| **Context** | Background the AI needs — constraints, audience, standards | "Our audience is enterprise CTOs. Tone should be authoritative, not salesy" |
| **Format** | How the output should be structured | "Present each option with a subject line and a one-sentence rationale" |

Not every prompt needs all four elements. A simple question needs only the task. But as complexity grows, adding role, context, and format dramatically improves output quality.

## Platform Implementations

| Platform | How Prompts Work |
|----------|-----------------|
| **Claude** | Messages in conversation, system prompts, project instructions |
| **OpenAI (ChatGPT)** | Messages in conversation, system prompts, Custom GPT instructions |
| **Gemini** | Messages in conversation, Gem instructions |
| **M365 Copilot** | Chat messages, prompts within Copilot agents |

## Common Prompt Anti-Patterns

**Vague instructions** — "Help me with marketing" gives the AI nothing to anchor on. Be specific: "Draft a 200-word LinkedIn post announcing our Q3 product update, targeting engineering managers."

**Overloading a single prompt** — Asking the AI to research, analyze, write, format, and review in one prompt leads to shallow results. Break complex work into sequential prompts or use a [Skill](../skills/index.md).

**Ignoring format guidance** — If you don't specify output structure, you get whatever the model defaults to. State what you want: bullet points, a table, a specific word count, or a particular template.

**Repeating yourself every conversation** — If you're pasting the same preamble into every chat, you need a [Project](../projects/index.md) with custom instructions instead.

## Guides

| Guide | Description |
|-------|-------------|
| [Prompt Engineering](prompt-engineering/index.md) | Core techniques — context windows, system prompts, few-shot learning, chain-of-thought |
| [Project Instructions](../projects/workspace-instructions-meta-prompt.md) | When your prompts evolve into standing instructions for a project workspace |

## Related

- [Agentic Building Blocks](../index.md) — Prompts in the context of all six building blocks
- [AI Use Cases](../../use-cases/index.md) — see how prompts are used across content creation, research, coding, data analysis, ideation, and automation
- [Projects](../projects/index.md) — where prompts become persistent custom instructions
- [Patterns](../../patterns/index.md) — reusable prompt structures
