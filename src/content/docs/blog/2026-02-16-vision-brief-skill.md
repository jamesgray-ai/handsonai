---
date: 2026-02-16
authors:
  - jamesgray
tags:
  - Plugins
description: "Agentic Coding plugin update: PRD skill gets paired AC/user stories and scope sections; Vision Brief skill adds strategic depth with 10 questions and inline examples."
title: "Agentic Coding Plugin: Stronger PRDs and Vision Briefs"
---Two back-to-back updates to the Agentic Coding plugin make both the PRD and Vision Brief skills significantly more rigorous — the PRD template now pairs acceptance criteria with user stories, and the Vision Brief asks the strategic questions that experienced product leaders always probe.

<!-- more -->

## Feature PRD skill improvements

The PRD template and workflow got a structural overhaul:

- **Acceptance criteria now sit directly beneath each user story** instead of being separated by three sections — this makes PRDs easier to review and keeps each story self-contained
- **New sections:** Scope (In/Out), Verification, and Global Acceptance Criteria
- **Stronger stress-test phase** with 6 specific checks for edge cases and ambiguity
- **5th intake question** for scope boundaries, so constraints are captured early
- PRDs now use `-prd.md` naming convention

## Vision Brief skill: strategic depth upgrade

The discovery phase grows from 6 to 10 questions, adding four new probes:

- **Current State** — how the problem is handled today (reveals pain severity and implicit requirements)
- **Strategic Context** — why now, and what happens if you don't act (separates urgent from nice-to-have)
- **Inspiration** — products or experiences that capture something close to the vision (optional)
- **Risks & Assumptions** — the hidden bet you're making and what could derail the plan

Success criteria are restructured into **early signal** (1-2 weeks) and **real outcome** (1-3 months) timeframes. Capabilities now get prioritized into **must-have** vs **nice-to-have**. When breaking a vision into features, the skill presents three sequencing strategies — **riskiest first**, **quickest win**, or **highest value** — instead of ad-hoc recommendations.

The previously missing `vision-brief-template.md` is now included with world-class inline examples for five sections: Problem, Vision, Capabilities, Success, and Risks & Assumptions.

## Install or update

```bash
/plugin install agentic-coding@handsonai
```

Plugin version bumped to **1.2.2**.
