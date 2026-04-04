---
date: 2026-02-19
authors:
  - jamesgray
categories:
  - Plugins
  - Platform Updates
description: "Building Workflows v3.1 adds plan mode gate, spec approval, and reference specs. Agents matrix expanded with SDK and browser agents. Architecture decisions streamlined."
title: "Build Workflows v3.1, Expanded Agents Matrix, and Streamlined Architecture Decisions"
---Three updates that tighten the framework's Build step and expand platform coverage for agents.

<!-- more -->

## Building Workflows skill upgraded to v3.1

The [`building-workflows`](../../business-first-ai-framework/build/index.mdx) skill now enforces a structured gate between Design and Construct. Step 3.1 (Design) opens with a **plan mode prompt** so you collaborate on architecture before any artifacts are generated. A **spec approval checkpoint** blocks progression until you explicitly approve the AI Building Block Spec. Step 3.2 (Construct) then offers a **build path choice** — the model generates artifacts, or you build manually from the spec with a construction guide. Integration research (web search) is deferred from Design to Construct so it doesn't interrupt planning. New [reference specs](../../business-first-ai-framework/skills.mdx) for the agentskills.io skill format and Claude Code subagent format ensure generated artifacts follow proper conventions.

## Agents by Platform matrix expanded

The [Agents](../../agentic-building-blocks/agents/index.md) index page now shows one row per agent approach across all four platforms — including browser-based offerings (Claude in Chrome, Atlas Browser, Gemini in Chrome) and the [Claude Agent SDK](../../platforms/claude/agents/building-agents.mdx#agent-sdk). Each row links to official docs and the corresponding platform guide.

## Architecture decisions simplified

The Design phase's architecture checklist has been replaced with an **extract-then-confirm** pattern. Instead of eight sequential questions, the skill asks one question (platform), extracts tool integrations, trigger/schedule, and browser access from the Workflow Definition, then presents a single confirmation block. Deployment surface, shareability, and code comfort are deferred to Construct where they're actually needed.

## Skills & Agents pages repositioned as platform-agnostic

The [Agents & Skills](../../use-the-playbook/build/index.md) section now leads with GitHub download as the primary access method across all four detail pages, with Claude Code plugin install as a secondary option. Verbose platform tabs replaced with concise "Using These Skills" sections.
