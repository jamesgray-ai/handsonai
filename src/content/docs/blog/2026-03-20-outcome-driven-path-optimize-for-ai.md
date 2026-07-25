---
date: 2026-03-20
authors:
  - jamesgray
categories:
  - Plugins
description: "Deconstruct skill adds outcome-driven path for agent systems and optimize-for-AI step for step-decomposed workflows"
title: "Outcome-Driven Path and Process Optimization in Deconstruct"
---The Deconstruct skill now supports three entry paths — giving you more flexibility in how you define what AI should do.

<!-- more -->

**Outcome-driven path (new).** When you know what you want produced but don't want to prescribe how the agent gets there, choose option (c). Instead of decomposing into fixed steps, the skill interviews you about your goal, inputs, expected outputs, constraints, quality criteria, and capability domains — producing a definition that feeds directly into agent-oriented Design. Best for autonomous workflows like research pipelines, monitoring systems, or content generation where the agent should determine its own approach.

**Optimize for AI (new).** For step-decomposed workflows, the skill now includes a process optimization pass after the deep dive. Once your current process is fully mapped, the model challenges it — identifying steps to eliminate (manual transfers an integration removes), collapse (draft + format in one pass), parallelize (no data dependency), or simplify (reduce review gates). You accept or reject each recommendation. The [Deconstruct guide](../../business-first-ai-framework/deconstruct/) has the full details.

**Design skill updated.** The Design skill now detects outcome-driven definitions and routes through capability-domain mapping instead of per-step classification — with pre-determined Autonomous autonomy and Agent orchestration. See the [Outcome-Driven Design Flow](../../ai-workflow-framework/design/#design-has-three-layers) section.

Plugin version: `business-first-ai` v7.1.0.
