# Hands-on AI

Everything you need to design, build, and document AI workflows.

The AI Workflow Framework as executable skills for Claude, ChatGPT/Codex, and Claude Code, plus a knowledge-graph builder, an AI registry toolkit, and a feature-spec toolkit. One install, one namespace, one mental model.

## Install

One plugin, three places it installs — pick yours. Full step-by-step (with screenshots) on the
[skills setup page](https://handsonai.info/ai-workflow-framework/skills/).

- **Claude** (web and desktop app — paid plans): **Customize → Plugins → + → Add marketplace → Add from a repository** → `jamesgray-ai/handsonai-plugins` → install **handsonai**.
- **ChatGPT** (the plugin installs on any paid plan; single skill uploads are documented for Business, Enterprise and Edu) **and Codex**: **Plugins → Add marketplace** → `jamesgray-ai/handsonai-plugins` → install **Hands-on AI**. Then `@analyze` (ChatGPT) or `$analyze` (Codex).
- **Claude Code**:

  ```
  /plugin marketplace add jamesgray-ai/handsonai-plugins
  /plugin install handsonai@handsonai
  ```

No plugin support on your platform (Claude Free, ChatGPT Free/Go, Gemini, Cursor, Gemini CLI)? Download the skills as ZIPs from the [Releases page](https://github.com/jamesgray-ai/handsonai-plugins/releases/latest).

- **Microsoft 365 Copilot** runs the framework in Copilot Cowork as custom skills: upload the skill ZIPs, or `handsonai-plugin.zip` (Copilot Cowork converts a Claude plugin on upload). Build makes any agent the workflow needs in Agent Builder. Your framework files live in a `Framework` folder in OneDrive, separate from Copilot Cowork's own folder.
- **Gemini, Cursor and others:** the Knowledge Graph, AI Registry and Building Skills skills install as ZIPs. The five framework skills are built for Claude, ChatGPT, Codex, Claude Code and Microsoft 365 Copilot; on those, if no drive connection can save, each step gives you its files to save and you paste or attach them when you start the next step.

## What's Included

### Skills — AI Workflow Framework

| Skill | Description |
|-------|-------------|
| `analyze` | Find where AI can create value in your work, and register every candidate as a backlog Workflow node in your registry (or a backlog list in your Framework folder, without one) |
| `deconstruct` | Turn one workflow into its Workflow Requirements: starting from anything you've written down, it pins down what every output must get right, the rules it follows, where it asks you first, and practice inputs based on your real work |
| `design` | Plan how AI will do the work: a Design Plan you review and approve, ending in a task list |
| `build` | Build the workflow from your approved plan, task by task, each part checked with dry runs that show changes instead of making them, plus a build record of what was built and what it can access |
| `test` | Check it on realistic inputs, including one it hasn't seen, against every requirement, then take it live on your yes; later, re-check it any time |

### Skills — Knowledge Graph

| Skill | Description |
|-------|-------------|
| `building-knowledge-graph` | Build your `knowledge/` knowledge graph — a guided interview finds the types and relationships of your work, then writes SCHEMA.md, seeded pages, standing rules, and local `ingest` and `lint` skills |

### Skills — AI Registry

| Skill | Description |
|-------|-------------|
| `scaffolding-registry` | Stand up your `registry/` knowledge bundle — SCHEMA.md and real Business, Line of Business, Function, and Process nodes (Analyze adds the workflows) |
| `naming-workflows` | Apply consistent naming conventions across your registry |
| `writing-workflow-sops` | Author standard operating procedures for AI-assisted workflows |
| `writing-process-guides` | Document multi-step processes for repeatable execution |
| `indexing-registry` | Lint your registry bundle and regenerate REGISTRY.md and its visual dashboard — the derived views of your skills, agents, workflows, and apps |

### Skills — Agentic Coding

| Skill | Description |
|-------|-------------|
| `writing-vision-briefs` | Capture a fuzzy idea as a structured Vision Brief before writing a PRD |
| `writing-feature-prds` | Create a PRD with user stories, acceptance criteria, and a GitHub issue |

### Skills — Building Skills

| Skill | Description |
|-------|-------------|
| `applying-skill-best-practices` | Best-practice standards for building any Agent Skill, applied alongside your platform's skill creator: reuse, scope, descriptions, content, settings, and test cases |
| `auditing-agent-skills` | Audits your existing skills for anything gone out of date (retired models, broken references, stale facts, overlaps, missing test cases, registry gaps) and proposes a fix for each; changes nothing without approval |

## Quick Start

Five steps, each in a new chat (a new session in Claude Code). Say the step's phrase on any platform, or use its slash command in Claude Code:

- **Analyze** (`/handsonai:analyze`) — find where AI can create value in your work, and build a backlog of candidate workflows
- **Deconstruct** (`/handsonai:deconstruct`) — turn one workflow into its Workflow Requirements
- **Design** (`/handsonai:design`) — get a Design Plan you review and approve
- **Build** (`/handsonai:build`) — build and install the workflow from your plan
- **Test** (`/handsonai:test`) — prove it on practice inputs, then take it live

Keeping it working is part of the workflow, not a step: each run flags anything it wasn't designed for, "change my workflow" starts any change, and "test the workflow I built" re-checks it. Say "continue my workflow" any time: the skill works out the step your workflow needs next, and either picks up there or gives you the phrase to start it in a new chat. Each step ends by giving you the phrase that starts the next one.

**Where the files live.** In Claude Code and Codex, the framework's files are in a `framework/` folder in your workspace, one folder per workflow. On Claude on the web and ChatGPT, they're in a `Framework` folder in your Google Drive, through the platform's connection (if no connection can save, each step gives you its files to save); on Microsoft 365, in a `Framework` folder in OneDrive. The workflow itself runs in its own place (its own Project, or its own folder), kept apart from the framework's files, and the framework's chats run outside it.

**Scripts that ship with the plugin.** In `tools/`, beside the registry tools (`compose-registry.js`, `lint-registry.js`): `framework-state.js` works out where a workflow is and which step is next, and `requirements-check.js` checks a Workflow Requirements file after each write, so a step fixes any problem before it goes on. Node 18 or later, no dependencies. Where code can't run, each skill follows the same rules from its own written copy.

## Worked Examples

Looking for example agents and skills (executive writing, editorial review, research, meeting prep, AI news)? They live in the [Example Gallery](https://handsonai.info/use-cases/example-gallery/) on the docs site as study material you can copy and customize for your own workflows.

## Full Documentation

[handsonai.info/use-the-playbook/build/handsonai/](https://handsonai.info/use-the-playbook/build/handsonai/)

## License

MIT
