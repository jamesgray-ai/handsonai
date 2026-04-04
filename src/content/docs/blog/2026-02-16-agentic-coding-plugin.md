---
date: 2026-02-16
authors:
  - jamesgray
categories:
  - Plugins
description: "New plugin for AI-assisted coding workflows — define requirements with structured PRDs before you build."
title: "New Plugin: Agentic Coding"
---The **Agentic Coding** plugin is now available in the marketplace — the third plugin alongside Business-First AI and AI Registry. It packages two skills for the "discover and define" phase of AI-assisted coding: `writing-vision-briefs` and `writing-feature-prds`.

<!-- more -->

## What's included

**`/agentic-coding:writing-vision-briefs`** — Capture a fuzzy idea as a structured Vision Brief. Walks you through the problem, users, vision, and success criteria, then breaks bigger ideas into epics and features you can build one at a time.

**`/agentic-coding:writing-feature-prds`** — Turn a Vision Brief (or a fresh idea) into a structured PRD through a 4-phase workflow:

1. **Define** — answer questions about the feature, get a PRD at `specs/[feature-name]-prd.md`
2. **Stress-test** — review for missing edge cases and ambiguous criteria
3. **Create issue** — GitHub issue with `type:feature` label linking to the PRD
4. **Handoff** — clear instructions to run `/feature-dev` for implementation

The two skills are designed to flow together — the Vision Brief feeds directly into the PRD — but each works standalone too.

## Install

```bash
/plugin install agentic-coding@handsonai
```

## Real-world usage

This plugin covers steps 0 (Discover) and 1 (Define) of the feature development workflow used to build this playbook. The full 6-step workflow — from vision brief through planning, implementation, review, and shipping — is documented in our [CLAUDE.md](https://github.com/jamesgray-ai/handsonai/blob/main/CLAUDE.md#feature-development-workflow) as a working example you can adapt for your own projects.

See the [Agentic Coding page](../../use-cases/coding/agentic-coding.mdx) for full documentation, example prompts, and a recommended CLAUDE.md workflow you can copy.
