---
date: 2026-03-02
authors:
  - jamesgray
categories:
  - Plugins
description: "The Build phase now uses a two-step decision model — autonomy assessment plus orchestration mechanism — replacing the old execution pattern spectrum."
title: "Build Phase: Autonomy Levels and Orchestration Mechanisms"
---The Business-First AI Framework's Build phase got a significant terminology and structural update. The old four-pattern execution spectrum (Prompt → Skill-Powered Prompt → Single Agent → Multi-Agent) has been replaced with a clearer two-step decision model.

<!-- more -->

**New two-step design model.** Instead of picking from four execution patterns, Design now walks through two distinct decisions: first, [assess the workflow's autonomy level](../../business-first-ai-framework/design.md#autonomy-assessment) (Deterministic → Guided → Autonomous), then [choose an orchestration mechanism](../../business-first-ai-framework/design.md#orchestration-mechanism) (Prompt → Skill-Powered Prompt → Agent). This separates *how much independence the AI needs* from *who drives the workflow* — making each decision simpler and more deliberate.

**Single Agent and Multi-Agent collapsed into "Agent."** Whether a workflow needs one agent or multiple is now an architecture detail decided during agent configuration — not a top-level pattern choice. This removes a premature decision point that often confused students.

**Coach pages retired.** The "Use AI as Your Coach" pages have been removed. The [MCP server](../../mcp-server/index.md) and [Business-First AI plugin](../../business-first-ai-framework/skills.mdx) now provide better guided experiences — the framework overview page links directly to them.

These changes are live across all [Build documentation](../../business-first-ai-framework/build/index.mdx), the `framework-orchestrator` agent, and the `building-workflows` skill (Business-First AI plugin v5.0.1).
