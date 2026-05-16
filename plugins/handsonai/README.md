# Hands-on AI

Everything you need to design, build, and document AI workflows.

The AI Workflow Framework as executable Claude Code skills, plus an AI registry toolkit and feature-spec toolkit. One install, one namespace, one mental model.

## Install

```
/plugin marketplace add jamesgray-ai/handsonai-plugins
/plugin install handsonai@handsonai
```

## What's Included

### Agent

| Agent | Description |
|-------|-------------|
| `framework-agent` | Walks you through the full 7-step AI Workflow Framework end-to-end |

### Skills — AI Workflow Framework

| Skill | Description |
|-------|-------------|
| `analyze` | Audit your workflows to find where AI creates the most value |
| `deconstruct` | Break a workflow into structured steps using the 6-question framework |
| `design` | Design the AI workflow architecture and produce an AI Building Block Spec |
| `build` | Generate platform-appropriate artifacts from the approved spec |
| `test` | Test workflow artifacts and evaluate output quality |
| `run` | Generate a Run Guide for deploying and operating the workflow |
| `improve` | Evaluate a running workflow for quality and evolution opportunities |

### Skills — AI Registry

| Skill | Description |
|-------|-------------|
| `naming-workflows` | Apply consistent naming conventions across your AI workflow registry |
| `writing-workflow-sops` | Author standard operating procedures for AI-assisted workflows |
| `writing-process-guides` | Document multi-step processes for repeatable execution |
| `registering-building-blocks` | Register prompts, skills, agents, and MCP servers in a Notion-backed registry |

### Skills — Agentic Coding

| Skill | Description |
|-------|-------------|
| `writing-vision-briefs` | Capture a fuzzy idea as a structured Vision Brief before writing a PRD |
| `writing-feature-prds` | Create a PRD with user stories, acceptance criteria, and a GitHub issue |

## Quick Start

1. **Analyze** — Run `/handsonai:analyze` to audit your workflows and identify AI opportunities
2. **Deconstruct** — Run `/handsonai:deconstruct` to break down your highest-impact workflow
3. **Design** — Run `/handsonai:design` to design the architecture
4. **Build** — Run `/handsonai:build` to generate platform artifacts
5. **Test** — Run `/handsonai:test` to validate output quality
6. **Run** — Run `/handsonai:run` to get deployment instructions
7. **Improve** — Run `/handsonai:improve` to evaluate and evolve the workflow

Or run the agent and let it walk you through the whole flow:

```
@framework-agent
```

Outputs are saved to the `outputs/` folder.

## Worked Examples

Looking for example agents and skills (executive writing, editorial review, research, meeting prep, AI news)? They live in the [Example Gallery](https://handsonai.info/use-cases/example-gallery/) on the docs site as study material you can copy and customize for your own workflows.

## Full Documentation

[handsonai.info/use-the-playbook/build/handsonai/](https://handsonai.info/use-the-playbook/build/handsonai/)

## License

MIT
