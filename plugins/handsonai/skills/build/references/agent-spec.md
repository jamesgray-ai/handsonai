# Agent Specification — Claude Code Subagent Format

When generating agents for Claude Code, follow this format exactly. Agents are single `.md` files with YAML frontmatter and a markdown body.

## File Format

A single markdown file: `agent-name.md`

## YAML Frontmatter (Required)

```yaml
---
name: agent-name
description: "Use this agent when [trigger description]. This includes [additional trigger conditions].\n\nExamples:\n\n<example>\nContext: [scenario]\nuser: \"[user message]\"\nassistant: \"[how the assistant introduces the agent]\"\n<Task tool call to agent-name agent>\n</example>\n\n<example>\nContext: [another scenario]\nuser: \"[user message]\"\nassistant: \"[assistant response]\"\n<Task tool call to agent-name agent>\n</example>"
model: sonnet          # Optional. One of: opus, sonnet, haiku, inherit. Defaults to inherit.
color: blue            # Optional. Agent color in UI.
tools:                 # Optional. Restrict which tools the agent can use.
  - WebSearch
  - WebFetch
  - Read
  - Glob
  - Grep
skills:                # Optional. Skills to preload into the agent's context.
  - skill-name
---
```

### Field Rules

The authoritative reference is the [Claude Code subagents documentation](https://code.claude.com/docs/en/sub-agents). Only `name` and `description` are required.

| Field | Required | Rules |
|-------|----------|-------|
| `name` | Yes | Lowercase, hyphens. Must match the filename (without `.md`). |
| `description` | Yes | Starts with "Use this agent when...". Should include 2-3 `<example>` blocks showing user message → assistant response → Task tool call. Examples help the host model decide when to launch this agent. |
| `model` | No | `opus`, `sonnet`, `haiku`, or `inherit`. Defaults to `inherit` (uses the parent conversation's model). Choose based on task complexity. |
| `color` | No | UI color for identifying the agent. |
| `tools` | No | Allowlist of tools. Omit to inherit all tools from the parent conversation. |
| `disallowedTools` | No | Denylist of tools, removed from inherited or specified list. |
| `skills` | No | Skills to preload into the agent's context at startup. Full skill content is injected, not just made available for invocation. |
| `permissionMode` | No | One of: `default`, `acceptEdits`, `dontAsk`, `bypassPermissions`, `plan`. Controls how the agent handles permission prompts. |
| `maxTurns` | No | Maximum number of agentic turns before the agent stops. |
| `mcpServers` | No | MCP servers available to this agent. Each entry is a server name referencing an already-configured server or an inline definition. |
| `hooks` | No | Lifecycle hooks scoped to this agent (e.g., `PreToolUse`, `PostToolUse`, `Stop`). |
| `memory` | No | Persistent memory scope: `user`, `project`, or `local`. Enables cross-session learning. |
| `background` | No | Set to `true` to always run as a background task. Default: `false`. |
| `isolation` | No | Set to `worktree` to run in a temporary git worktree for repository isolation. |

### Description Format

The `description` field is critical — it's what the host model reads to decide whether to launch the agent. It must:

1. **Start with a trigger phrase**: "Use this agent when..."
2. **List trigger conditions**: What user requests or situations activate this agent
3. **Include 2-3 examples**: Each showing context, user message, and assistant response

Examples use this exact format (with escaped newlines in the YAML string):

```
<example>
Context: [Brief scenario description]
user: "[What the user says]"
assistant: "[How the assistant responds before launching]"
<Task tool call to agent-name agent>
</example>
```

## Markdown Body

The body defines the agent's behavior — its role, process, constraints, and output format.

### Structure

```markdown
You are [role description with expertise and personality].

## Your Core Responsibilities

1. **Area 1**: [What the agent does in this area]
2. **Area 2**: [What the agent does in this area]

## Process

[Step-by-step process the agent follows]

## Output Format

[How the agent structures its output]

## Constraints

- [Behavioral rules]
- [Quality standards]
- [What the agent should NOT do]
```

### Writing Guidelines

- **Open with a role statement** — "You are a..." sets the agent's expertise and tone.
- **Be directive** — Write instructions, not descriptions. "Search for X" not "The agent searches for X".
- **Include output delivery** — Specify where to save files (e.g., `outputs/` directory) and what to tell the user.
- **No filesystem references to `context/` or `skills/`** — agents receive skills via the `skills:` frontmatter field, not by reading files.

## Anti-Patterns

| Don't | Do Instead |
|-------|-----------|
| Bare markdown without frontmatter | Always include YAML frontmatter with name, description, model |
| `Read context/some-file.md` in body | Use `skills:` frontmatter to attach skills |
| Description without examples | Include 2-3 `<example>` blocks |
| Vague description: "A helpful agent" | Specific triggers: "Use this agent when the user wants to..." |
| Hardcoded platform instructions | Let the agent research platform specifics at runtime |

## Example

```yaml
---
name: weekly-report-generator
description: "Use this agent when the user wants to generate a weekly status report from project data. This includes requests to summarize weekly progress, compile team updates, or create stakeholder reports.\n\nExamples:\n\n<example>\nContext: User wants their weekly report generated\nuser: \"Generate my weekly status report\"\nassistant: \"I'll use the weekly report generator agent to compile your status report from project data.\"\n<Task tool call to weekly-report-generator agent>\n</example>\n\n<example>\nContext: User needs a stakeholder update\nuser: \"Put together a progress summary for the leadership meeting\"\nassistant: \"Let me launch the weekly report generator agent to compile a progress summary from your project data.\"\n<Task tool call to weekly-report-generator agent>\n</example>"
model: sonnet
color: green
skills:
  - writing-status-reports
---

You are a meticulous Project Report Analyst who compiles clear, actionable status reports from project data. You focus on what matters to stakeholders: progress, blockers, and next steps.

## Process

1. Identify the user's project tracking tools and data sources
2. Collect the last 7 days of activity
3. Synthesize updates into themes: Completed, In Progress, Blocked, Upcoming
4. Draft the report and present for review
5. Save to `outputs/status-report-YYYY-MM-DD.md`

## Output Format

Structure reports with: date range, key metrics, category sections, blockers (highlighted), and next week priorities.

## Constraints

- Use plain language — no jargon
- Keep bullets to one sentence
- Flag blockers prominently at the top
- Always save the report to `outputs/` and confirm the file path
```
