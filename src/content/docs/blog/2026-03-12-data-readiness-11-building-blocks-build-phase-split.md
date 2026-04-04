---
date: 2026-03-12
authors:
  - jamesgray
categories:
  - Plugins
description: "Data readiness probing, 11 building blocks, Design Prompt, and the Build phase split into three focused skills."
title: "Data Readiness, 11 Building Blocks, and a Redesigned Build Phase"
---The Business-First AI Framework gets its biggest skill update since the Organizational Lens — a new deep-dive dimension, expanded building block vocabulary, a portable Design Prompt, and a restructured Build phase.

<!-- more -->

## Data Readiness Probing (6-Question Framework)

The [Deconstruct step](../../business-first-ai-framework/deconstruct/index.md) now uses a **6-question framework**, adding **Data Readiness** as the sixth dimension alongside discrete steps, decision points, data flows, context needs, and failure modes. For every step's inputs, the skill now probes access (can AI reach the data?), interpretability (is the format AI-friendly?), and persistence (does this knowledge exist as a durable artifact, or is it stuck in someone's head?). The [Context Shopping List](../../business-first-ai-framework/deconstruct/index.md) output now includes **AI Accessible?** and **Readiness Notes** columns, and the [Design skill](../../business-first-ai-framework/design.md) extracts these flags to inform step classification and produces a **Data Readiness Summary** in the Building Block Spec.

## 11 Building Blocks in Three Layers

The framework vocabulary expands from 7 to **11 building blocks**, organized by the three-layer model: **Intelligence** (Model, Context, Memory, Project), **Orchestration** (Prompt, Skill, Agent), and **Integration** (MCP, API, SDK, CLI). The [design skill](../../business-first-ai-framework/skills.mdx#design) now maps every step against the full set, ensuring workflows that need API integrations, SDK code, CLI automation, or persistent memory get those blocks identified during Design rather than discovered mid-build.

## Build Phase Split into Three Skills

The monolithic `building-workflows` skill has been decomposed into three focused skills — **designing-workflows** (architecture decisions, autonomy assessment, step classification), **constructing-workflows** (artifact generation from the approved spec), and **running-workflows** (run guide creation). Each can be invoked independently, and the [Business-First AI plugin](../../business-first-ai-framework/skills.mdx) is now at **v6.0.2**.

## Design Prompt — Portable Version

The [Design step](../../business-first-ai-framework/design.md) is now available as a standalone skill. Install it on any platform to run the full Design phase — assess autonomy, choose orchestration, classify steps, and produce a Building Block Spec.

## Content Repurposing Demo Skills

The [AI Workflow Examples plugin](../../use-the-playbook/build/ai-workflow-examples.mdx) (v1.1.0) adds two demo skills for the Agentic AI course: **extracting-article-insights** and **drafting-linkedin-posts** — a two-step content repurposing pipeline that extracts key points from a source article and drafts a LinkedIn post from the results.

## GitHub Setup: Create a Repository

The [GitHub setup guide](../../builder-setup/github-setup.md) now includes a **Create a Repository** step, walking students through creating their first repo from the command line.
