---
title: Agents & Skills
description: The Hands-on AI plugin — agents and skills for designing, building, and documenting AI workflows. Plus a gallery of example components you can copy and customize.
---

A focused toolkit of **agents** and **skills** that give your AI tool everything it needs to design, build, and document AI workflows. Plain-text Markdown — install as a [Claude Code plugin](using-plugins/), or download individual skills as ZIPs for ChatGPT, M365 Copilot, Cursor, and other tools.

---

## 🛠️ The Hands-on AI Plugin

One plugin, one install. Bundles the AI Workflow Framework, the AI Registry skills, and the Agentic Coding feature-spec skills — everything you need to take an AI workflow from idea to documented production system.

```
/plugin marketplace add jamesgray-ai/handsonai-plugins
/plugin install handsonai@handsonai
```

[→ See what's included](handsonai/) · [Using Plugins](using-plugins/)

### What's inside

#### AI Workflow Framework — 1 agent + 7 skills

The seven-step methodology for going from a workflow idea to a deployed AI system.

| Component | What it does |
|---|---|
| [`framework-agent`](handsonai/#framework-agent) agent | Walks you through the full 7-step framework end-to-end |
| `analyze` skill | Audit your workflows to find where AI creates the most value |
| `deconstruct` skill | Break a workflow into structured steps using the 6-question framework |
| `design` skill | Design the AI workflow architecture and produce a Design Spec |
| `build` skill | Generate platform-appropriate artifacts from the approved spec |
| `test` skill | Test workflow artifacts and evaluate output quality |
| `run` skill | Generate a Run Guide for deploying and operating the workflow |
| `improve` skill | Evaluate a running workflow for quality and evolution opportunities |

#### AI Registry — 4 skills

For documenting and operating an AI workflow registry once you've built workflows worth tracking.

| Component | What it does |
|---|---|
| `naming-workflows` skill | Apply consistent naming conventions across your registry |
| `writing-workflow-sops` skill | Author standard operating procedures for AI-assisted workflows |
| `writing-process-guides` skill | Document multi-step processes for repeatable execution |
| `registering-building-blocks` skill | Register prompts, skills, agents, and MCP servers in a Notion-backed registry |

#### Agentic Coding — 2 skills

For turning ideas into shippable feature specs before you write code.

| Component | What it does |
|---|---|
| `writing-vision-briefs` skill | Capture a fuzzy idea as a structured Vision Brief before writing a PRD |
| `writing-feature-prds` skill | Create a PRD with user stories, acceptance criteria, and a GitHub issue |

---

## 🎨 Example Gallery

Looking for an agent that writes for executives? A researcher that scans AI news daily? A skill for prepping meetings? Templates you can copy and customize live in the [Example Gallery](../../use-cases/example-gallery/) — 7 agents, 5 skills, and 3 portable prompts adapted from real workflows.

These are not bundled in the plugin because they're scoped to specific personas, source lists, or industries. They're better as study material than installable defaults.

[→ Browse the gallery](../../use-cases/example-gallery/)
