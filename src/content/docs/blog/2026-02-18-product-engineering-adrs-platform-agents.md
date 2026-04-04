---
date: 2026-02-18
authors:
  - jamesgray
categories:
  - New Content
  - Plugins
description: "New Product & Engineering section, Architecture Decision Records page, platform-specific agent examples, and fixed agentic-coding slash commands."
title: "Product & Engineering section, ADRs, and platform agent examples"
---Three updates this week: a new documentation section for non-technical readers, a cleaner development workflow, and platform-specific agent implementation guides.

<!-- more -->

## Product & Engineering section

A new top-level section covering software engineering and product management concepts written for people who are new to building software. Six pages cover the [Software Development Lifecycle](../../product-engineering/sdlc.md), [Product Requirements Documents](../../product-engineering/requirements.md), [User Stories & Acceptance Criteria](../../product-engineering/user-stories.md), [Roadmaps & Prioritization](../../product-engineering/roadmapping.md), [Stakeholder Management](../../product-engineering/stakeholder-management.md), and [Project Tracking with GitHub](../../product-engineering/tracking.md). Each page includes a section on how AI changes the practice.

## Architecture Decision Records

New page: [Architecture Decision Records](../../product-engineering/architecture-decisions.md) explains what ADRs are, when to write one, and provides a simple template. The [Agentic Coding workflow template](../../use-cases/coding/agentic-coding.mdx#feature-development-workflow-template) now includes ADR reminders in the Discover, Define, and Plan steps — so decisions get captured as they happen, not reconstructed months later.

## Platform-specific agent implementation guides

The Business-First AI `building-workflows` skill now generates platform-specific implementation guides when building agents. New pages for [Claude](../../platforms/claude/agents/building-agents.mdx), [OpenAI](../../platforms/openai/agents/building-agents.md), [Google Gemini](../../platforms/google-gemini/agents/building-agents.md), and [M365 Copilot](../../platforms/m365-copilot/agents/building-agents.md) show how to take a workflow design and implement it on each platform.

## Agentic Coding plugin fixes

The `/agentic-coding:writing-vision-briefs` and `/agentic-coding:writing-feature-prds` slash commands now resolve correctly — the old `command:` frontmatter field was deprecated and the commands weren't working. Spec file paths are now standardized: PRDs use `-prd.md`, plans use `-plan.md`, and architecture decisions go in `specs/decisions/`.
