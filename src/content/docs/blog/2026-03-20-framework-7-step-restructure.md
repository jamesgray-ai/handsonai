---
date: 2026-03-20
authors:
  - jamesgray
tags:
  - Plugins
  - New Content
description: "The Business-First AI Framework expands from 3 steps to 7 — with new Test and Improve steps, renamed skills, evaluation criteria, and a skills-only approach replacing portable prompts."
title: "Business-First AI Framework: 7-Step Restructure"
---The framework grows from three steps to seven — promoting Design, Build, Test, Run, and Improve to top-level steps with their own skills, deliverables, and documentation pages.

<!-- more -->

## What Changed

**3 steps → 7 steps.** The old "Step 3: Build" umbrella (with sub-steps 3.1 Design, 3.2 Construct, 3.3 Run) is gone. Each is now a top-level step, "Construct" is renamed to "Build", and two new steps join the framework:

| Step | Skill | Deliverable |
|------|-------|-------------|
| 1. Analyze | `analyze` | Opportunity Report |
| 2. Deconstruct | `deconstruct` | Workflow Definition |
| 3. Design | `design` | AI Building Block Spec |
| 4. Build | `build` | Platform artifacts |
| 5. Test | `test` | Test Results with eval scorecard |
| 6. Run | `run` | Run Guide |
| 7. Improve | `improve` | Improvement Plan |

**Step 5: Test** — structured evaluation using criteria defined during Design. Smoke test, full eval suite with 1-5 scoring, building block evals in isolation, baseline establishment, and a diagnosis table mapping problems to building blocks. [Test page](../../business-first-ai-framework/test/).

**Step 7: Improve** — periodic evaluation of running workflows. Watch for quality signals, re-run evals against baseline, assess graduation to a more capable orchestration mechanism, and decide: no changes needed, tune, redesign, or evolve. [Improve page](../../business-first-ai-framework/improve/).

**Evaluation Criteria in Design.** The [Design skill](../../business-first-ai-framework/design/) now prompts for what good output looks like, quality dimensions, 3-5 test scenarios, and a minimum quality bar. These feed directly into Test and Improve.

**Skills renamed.** All five existing skills shortened from verbose forms (`analyzing-workflows`, `deconstructing-workflows`, etc.) to `analyze`, `deconstruct`, `design`, `build`, `run`. Slash commands updated accordingly — e.g., `/business-first-ai:build` replaces `/business-first-ai:construct-workflow`.

**Portable prompts retired.** Skills now work on every major platform (Claude Code, Cowork, Claude.ai, ChatGPT, Codex CLI, Gemini CLI, Cursor), so maintaining separate copy-paste prompts is no longer necessary. The three prompt pages redirect to their step pages.

**Plugin version: 7.0.0** — a major version bump reflecting breaking skill renames and new skills. Update with `/plugin install business-first-ai@handsonai`.

**[Start with the framework overview →](../../business-first-ai-framework/)**
