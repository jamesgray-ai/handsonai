---
title: MCP (Model Context Protocol)
description: The MCP building block — an open standard for connecting AI assistants to external systems where data lives
---

# MCP (Model Context Protocol)

> **Platforms:** `claude` `openai` `gemini` `m365-copilot`

## What MCP Is

**MCP (Model Context Protocol)** is an open standard for connecting AI assistants to external systems where data lives — content repositories, business tools, databases, and development environments. It bridges the gap between the AI and the outside world, enabling both read and write operations.

Without MCP, the AI is limited to what's in the conversation. With MCP, the AI can look up client history in your CRM, check deal status in your pipeline, create tasks in your project management tool, or query live data — all within the conversation.

## Key Characteristics

- **Bridges the gap** between the AI and the outside world where your data lives
- **Open standard** — one integration pattern that works across compatible platforms
- **Enables read and write operations** — the AI can both retrieve information and take actions
- **Composable** — multiple MCP connectors can be active simultaneously, giving the AI access to multiple external systems

!!! note "MCP is not Claude-only"
    While Anthropic created the MCP standard, it's an open protocol. OpenAI, Google, and Microsoft are adopting or building compatible approaches. The concept — giving AI standardized access to external tools — exists on every platform, even when the implementation differs.

## When to Use MCP

Use MCP when:

- The AI needs to interact with external systems — reading from or writing to tools you already use
- Your workflow requires live data that changes between runs (not static reference documents)
- You want the AI to take actions in other systems — creating tasks, sending messages, updating records
- You're building agents that need to coordinate across multiple tools

MCP is typically the last building block you need. Start with prompts, add context, organize in a project, package as skills, then add MCP when the workflow needs external system access.

## Platform Implementations

| Platform | How It Works |
|----------|-------------|
| **Claude** | MCP servers (local or remote) connected via Claude Code or Claude Desktop |
| **OpenAI (ChatGPT)** | Function calling, Actions in Custom GPTs, Assistants API tools |
| **Gemini** | Extensions and function calling |
| **M365 Copilot** | Connectors, plugins, Power Platform integrations |

## Common MCP Use Cases

| Use Case | What the AI Does | Example Tools |
|----------|-----------------|---------------|
| **Knowledge management** | Reads and writes to your knowledge bases | Notion, Confluence, Google Drive |
| **Project management** | Creates tasks, updates status, queries boards | Linear, Jira, Asana, Trello |
| **Communication** | Reads messages, sends updates, manages threads | Slack, Email, Teams |
| **Data access** | Queries databases, retrieves records | PostgreSQL, Supabase, Airtable |
| **Development** | Manages repos, reviews PRs, deploys code | GitHub, Vercel, AWS |
| **CRM** | Looks up clients, logs interactions, updates deals | HubSpot, Salesforce |

## Relationship to Other Blocks

MCP extends what agents and skills can do by connecting them to external systems. Without MCP, the AI is limited to what's in the conversation. With MCP, skills can pull live data and agents can take real-world actions as part of their workflows.

## Related

- [Agentic Building Blocks](../index.md) — MCP in the context of all seven building blocks
- [AI Use Cases](../../use-cases/index.md) — what teams build with MCP, organized by six primitives
- [Automation Use Cases](../../use-cases/automation.md) — MCP enables the data connections that power automated workflows
- [Agents](../agents/index.md) — autonomous systems that use MCP to interact with external tools
- [Skills](../skills/index.md) — reusable routines that MCP can enhance with external data
- [Projects](../projects/index.md) — workspaces where MCP connectors are configured
