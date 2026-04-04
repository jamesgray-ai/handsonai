---
date: 2026-02-19
authors:
  - jamesgray
categories:
  - New Content
  - Plugins
description: "Step 3 — Build Workflows redesigned around skill-driven orchestration with a new Construct page, Launch Guide, and cross-platform skills standard."
title: "Step 3 Redesigned: Skills Drive the Build"
---The Build Workflows step has been redesigned around a core idea: the model and user collaborate through skills to design and construct AI building blocks together. Instead of six separate reference pages, Build is now a streamlined three-part flow — Design, Construct, Run — with a new visual diagram and clear deliverables at each stage.

<!-- more -->

## Skill-driven framework orchestration

The [Build Workflows](../../business-first-ai-framework/build/index.mdx) step now works through the `building-workflows` skill, which orchestrates the full Design and Construct phases. In Design, the model collaborates with you on architecture decisions, execution patterns, and building block mapping — producing an AI Building Block Spec. In Construct, the model executes against that spec to generate your platform's building blocks, then delivers a **Launch Guide** with step-by-step setup instructions, a guided first run, and next steps.

The skill now starts each build by reading the playbook's [curated platform documentation](../../business-first-ai-framework/build/index.mdx) for your specific platform, then verifies currency via web search — so recommendations stay current without relying on stale static mappings.

## New Construct page replaces six building block pages

Six individual pages (Context, Projects, Skills, Prompt, Agents, MCP) have been consolidated into a single [Construct](../../business-first-ai-framework/build/index.mdx) page. The model handles most of the build process automatically, so the page now focuses on what you need to do yourself: gather business-specific context, configure external tool connections, and operationalize agents on your platform — with links to platform-specific guides for [Claude](../../platforms/claude/agents/building-agents.mdx), [OpenAI](../../platforms/openai/agents/building-agents.md), [Google](../../platforms/google-gemini/agents/building-agents.md), and [M365 Copilot](../../platforms/m365-copilot/agents/building-agents.md).

## Analyze and Deconstruct shift to skills

The [Analyze](../../business-first-ai-framework/analyze.md) and [Deconstruct](../../business-first-ai-framework/deconstruct/index.md) pages have been updated to reference skills instead of raw prompt templates. The standalone prompt page for Deconstruct has been removed — the `deconstructing-workflows` skill now drives the process directly.

## Cross-platform skills standard

The [Skills](../../agentic-building-blocks/skills/index.mdx) building block page now documents the Agent Skills open standard across five platforms — Claude Code, Cursor, Codex CLI, Gemini CLI, and VS Code Copilot — with a new [How to Add Skills to Your Platform](../../agentic-building-blocks/skills/index.mdx#how-to-add-skills-to-your-platform) installation guide. The [Agents & Skills](../../use-the-playbook/build/index.md) section (formerly "Marketplace") now leads with GitHub download as the primary access method, reflecting the cross-platform positioning.
