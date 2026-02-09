---
title: Skills
description: The Skill building block — reusable routines the AI discovers and loads dynamically when relevant to a task
---

# Skills

> **Platforms:** `claude` `openai` `gemini` `m365-copilot`

## What Skills Are

**Skills** are folders containing instructions, scripts, and resources that the AI discovers and loads dynamically when relevant to a task. They encapsulate a specific capability — instructions, context, and output format bundled together — so you don't have to re-explain the same task every time.

Skills are now an open standard and being adopted broadly across platforms. Think of them as upgraded prompts: they package a prompt with its context into something reusable, shareable, and automatically invocable.

## Key Characteristics

- **Encapsulates a specific capability** — instructions, context, and output format bundled together
- **Dynamically loaded** — the AI discovers and invokes skills when they're relevant to the task
- **Reusable across conversations** — write once, use every time the task comes up
- **Shareable** — skills can be distributed to others through plugins or file sharing
- **Becoming an open standard** — the skill format is being adopted across compatible platforms

## When to Use a Skill

Use a skill when:

- You find yourself writing the same prompt repeatedly
- A workflow step is well-defined enough to package as a repeatable routine
- Consistency matters — the output should follow the same structure every time
- You want others to be able to run the same task with the same quality

A good rule of thumb: if you give an AI the same instructions more than three times, it's time to package those instructions as a skill.

!!! info "Skills vs. Agents"
    A skill is a **routine** — it does one thing well when invoked. An agent is **autonomous** — it decides what to do, which tools to use, and when to invoke skills. Think of skills as tools in a toolbox and agents as the person using the toolbox.

## Platform Implementations

| Platform | How It Works |
|----------|-------------|
| **Claude** | Claude Code Skills (SKILL.md files with instructions and references) |
| **OpenAI (ChatGPT)** | Custom GPTs, or Actions within a GPT |
| **Gemini** | Gems with structured instructions |
| **M365 Copilot** | Copilot agent actions, Power Automate flows triggered by Copilot |

## Anatomy of a Claude Skill

On Claude, a skill is a folder containing:

```
skill-name/
├── SKILL.md          # Instructions — what the skill does and how
└── references/       # Optional context files the skill needs
    ├── style-guide.md
    └── template.md
```

The `SKILL.md` file contains the instructions. The `references/` folder holds any context the skill needs — style guides, templates, examples, or data.

## Skill, Project, or Prompt?

| Approach | Best For | Example |
|----------|----------|---------|
| **Prompt** | One-off or infrequent tasks | "Summarize this PDF" |
| **Project** | Recurring context without rigid steps | Client research workspace |
| **Skill** | Repeatable process with consistent format and standards | Weekly status report generation |

## Guides

| Guide | Description |
|-------|-------------|
| [Discover Your Best Claude Skills](../../platforms/claude/skills/skills-discovery-meta-prompt.md) | Guided process to identify your highest-value skill candidates |

## Related

- [Agentic Building Blocks](../index.md) — Skills in the context of all six building blocks
- [AI Use Cases](../../use-cases/index.md) — what teams build with skills, organized by six primitives
- [Prompts](../prompts/index.md) — the foundation that skills build on
- [Agents](../agents/index.md) — autonomous systems that invoke skills as part of multi-step workflows
- [Plugin Marketplace](../../plugins/index.md) — pre-built skills you can install
