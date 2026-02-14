---
title: "The Complete Guide to Building Skills for Claude"
description: "Anthropic's end-to-end guide to planning, building, testing, and distributing Claude skills — from fundamentals and progressive disclosure to patterns and troubleshooting"
---

# The Complete Guide to Building Skills for Claude

*Source: [Anthropic](https://claude.com/blog/complete-guide-to-building-skills-for-claude) · PDF · Published 2026*

## Why This Matters

Skills are one of the most powerful ways to customize Claude. Instead of re-explaining your preferences, processes, and domain expertise in every conversation, skills let you teach Claude once and benefit every time. This guide is the authoritative reference for building effective skills — covering structure, design principles, testing, distribution, and real-world patterns.

## Key Takeaways

- **A skill is a folder, not a file.** At minimum, a skill contains a `SKILL.md` file with YAML frontmatter and markdown instructions. It can optionally include `scripts/`, `references/`, and `assets/` directories for executable code, documentation, and templates.
- **Progressive disclosure keeps skills efficient.** Skills use a three-level system: the YAML frontmatter (always loaded), the SKILL.md body (loaded when relevant), and linked files (loaded on demand). This minimizes token usage while maintaining deep expertise.
- **Two paths through the guide.** Standalone skill builders focus on fundamentals, planning, and design. MCP builders also learn how skills layer on top of MCP server connections to add workflows and best practices to raw tool access.
- **Testing is iterative, not one-shot.** The guide recommends testing skills across diverse scenarios, edge cases, and different conversation contexts. Expect 15–30 minutes to build and test your first working skill.
- **Distribution scales from personal to organizational.** Skills work identically across Claude.ai, Claude Code, and the API. Share via file sharing, Git repositories, or plugin marketplaces.
- **Patterns cover common use cases.** The guide includes patterns for content generation, code review, data analysis, research workflows, and multi-step processes — each with structural guidance and troubleshooting tips.

## How the Cookbook Uses This

This guide is the primary reference for the [Skills](../agentic-building-blocks/skills/index.md) building block and directly informs the cookbook's [Build (Plugins)](../use-the-cookbook/build/index.md) section. The skill structure and progressive disclosure concepts appear throughout the cookbook's plugin development guides.

## Access

[:material-download: Download PDF](../assets/pdfs/anthropic-skills-guide.pdf){ .md-button }

[View original :octicons-link-external-16:](https://claude.com/blog/complete-guide-to-building-skills-for-claude)
