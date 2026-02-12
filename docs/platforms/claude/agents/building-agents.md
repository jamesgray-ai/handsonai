---
title: Building Agents on Claude
description: How to build agents on the Claude platform — custom subagents for focused tasks and agent teams for multi-agent coordination.
---

# Building Agents on Claude

> **Part of:** [Build Workflows > Agents](../../../business-first-ai-framework/build/agents.md)

Claude Code provides two approaches to building agents, each suited to different workflow patterns. Both use Markdown files with YAML frontmatter — no code required.

| Approach | Best for | Complexity |
|----------|----------|------------|
| [Custom subagents](#custom-subagents) | Focused, single-responsibility tasks | Low — one `.md` file per agent |
| [Agent teams](#agent-teams) | Multi-agent coordination with parallel execution | Higher — experimental feature, multiple agents collaborating |

## Custom Subagents

A custom subagent is a Markdown file that defines an agent's role, instructions, and capabilities. Claude Code spawns it as a subprocess with its own context window, tools, and permissions.

**Official docs:** [Claude Code Sub-agents](https://code.claude.com/docs/en/sub-agents)

### Where agent files live

| Location | Scope |
|----------|-------|
| `.claude/agents/` (in your project) | Available to anyone working in this project |
| `~/.claude/agents/` (in your home directory) | Available across all your projects |

### Agent file structure

Each agent is a single `.md` file with YAML frontmatter for configuration and Markdown body for instructions:

```markdown
---
name: research-analyst
description: Use this agent to research companies and summarize findings
model: sonnet
tools:
  - WebSearch
  - WebFetch
  - Read
  - Write
---

# Research Analyst

You are a research analyst who investigates companies and produces structured briefs.

## Process

1. Search for the company using web search
2. Visit the company website and key pages
3. Summarize findings in a structured format

## Output Format

Write findings to `outputs/[company-name]-research.md` with sections for:
- Company overview
- Key products/services
- Recent news
- Relevant insights
```

### Frontmatter options

| Field | Required | Description |
|-------|----------|-------------|
| `name` | No | Display name (defaults to filename) |
| `description` | Yes | When to use this agent — Claude reads this to decide whether to activate it |
| `model` | No | Which model to use (`opus`, `sonnet`, `haiku`) |
| `tools` | No | Which tools the agent can access (e.g., `Read`, `Write`, `WebSearch`, `Bash`) |
| `permissionMode` | No | How tool permissions are handled (`default`, `acceptEdits`, `bypassPermissions`) |
| `skills` | No | Skills the agent can use (list of skill names) |
| `mcpServers` | No | MCP servers the agent can connect to |
| `maxTurns` | No | Maximum number of turns before the agent stops |
| `memory` | No | Path to a persistent memory file the agent can read and update |
| `hooks` | No | Shell commands triggered by agent lifecycle events |

### Creating an agent

Two options:

1. **Use the `/agents` command** — Claude Code walks you through creating an agent interactively
2. **Create the file manually** — Write a `.md` file in `.claude/agents/` following the structure above

### How agents activate

When you describe a task in Claude Code, it checks agent descriptions to decide whether to delegate. You can also invoke an agent directly:

```bash
# Run from the command line
claude --agent research-analyst

# Or describe the task and let Claude choose the right agent
claude "Research Acme Corp and write a brief"
```

Agents can run in the foreground (you see their work in real-time) or in the background (they work independently while you continue).

### Key capabilities

- **Tool restrictions** — limit which tools an agent can use, preventing unintended actions
- **Skills** — attach reusable skills that give the agent domain expertise
- **MCP servers** — connect to external services (databases, APIs, browsers) via the Model Context Protocol
- **Persistent memory** — give the agent a memory file it reads at startup and updates as it learns
- **Hooks** — trigger shell commands when the agent starts, stops, or encounters specific events

### Mapping your Design blueprint

Your [Design phase](../../../business-first-ai-framework/build/design.md) produced a platform-agnostic agent blueprint. Here's how each component maps to a Claude Code agent file:

| Design blueprint | Claude Code agent file |
|-----------------|----------------------|
| **Name** | Filename (e.g., `research-analyst.md`) and optional `name` frontmatter |
| **Description** | `description` frontmatter — write it so Claude knows when to activate this agent |
| **Instructions** | Markdown body — the agent's role, process, constraints, and output format |
| **Model** | `model` frontmatter (`opus`, `sonnet`, `haiku`) |
| **Tools** | `tools` frontmatter (list of tool names) + `mcpServers` for external connections |
| **Context** | `skills` frontmatter + reference files mentioned in the instructions |
| **Goal** | Captured in the `description` (activation trigger) and instructions (success criteria) |

## Agent Teams

Agent teams let multiple Claude Code instances work together on complex tasks — a team lead coordinates while teammates handle specialized subtasks in parallel.

**Official docs:** [Claude Code Agent Teams](https://code.claude.com/docs/en/agent-teams)

!!! warning "Experimental feature"
    Agent teams require the `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` environment variable. The feature is under active development and behavior may change.

### How teams work

A **team lead** (a Claude Code agent) can spawn **teammates** — independent Claude Code instances that each get their own context window and tools. The team lead coordinates work through a shared task list and inter-agent messaging.

```
Team Lead
├── Teammate A (e.g., research analyst)
├── Teammate B (e.g., writer)
└── Teammate C (e.g., editor)
```

### Key capabilities

- **Shared task list** — the team lead creates tasks, teammates claim and complete them
- **Inter-agent messaging** — teammates can send messages to the team lead and to each other
- **Parallel execution** — teammates work simultaneously on independent tasks
- **Plan approval** — the team lead can present a plan for your approval before dispatching work

### When to use teams vs. single agents

| Use single agents when... | Use agent teams when... |
|--------------------------|------------------------|
| The task has one focus area | The task spans multiple expertise domains |
| Steps are sequential | Steps can run in parallel |
| One agent can handle everything | Different steps need different tools or knowledge |
| You want simple, predictable execution | You want to maximize throughput on complex tasks |

### Good use cases for teams

- **Parallel research** — multiple teammates research different aspects simultaneously
- **Competing approaches** — teammates try different solutions, team lead picks the best
- **Cross-layer coordination** — frontend, backend, and testing teammates work on related changes
- **Pipeline processing** — research → write → edit with specialized teammates for each stage

### Mapping your Design blueprint

For multi-agent workflows, the Design phase produced configurations for multiple agents. On Claude Code:

1. **Each specialist agent** becomes a teammate definition
2. **The orchestrator** becomes the team lead's instructions
3. **Handoff points** map to task list entries and messaging patterns
4. **Human review gates** map to plan approval checkpoints

## What's Next

- [Agents overview](../../../business-first-ai-framework/build/agents.md) — the platform-agnostic agent decision framework
- [Design Your AI Workflow](../../../business-first-ai-framework/build/design.md) — produce the agent blueprint that feeds into these implementations
- [Scheduling Subagents](../subagents/scheduling-subagents.md) — run agents automatically on a schedule
