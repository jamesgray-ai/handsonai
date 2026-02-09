---
title: MCP
description: Connect your AI workflow to external tools, databases, and services using the Model Context Protocol.
---

# MCP

> **Part of:** [Build Workflows](index.md)

!!! tip "New to MCP as a building block?"
    See [Agentic Building Blocks > MCP](../../agentic-building-blocks/mcp/index.md) for definitions, available servers, and cross-platform setup instructions.

## What This Is

MCP (Model Context Protocol) gives AI access to external tools, databases, and services. It's the bridge between your AI workflow and the systems where your data lives and actions happen.

| | |
|---|---|
| **What you'll do** | Review your Building Block Map for steps requiring external tool access, then configure the MCP connections those steps need |
| **What you'll get** | Working connections between your AI workflow and external systems |
| **Time** | 10-30 minutes per connection (varies by tool complexity) |

## When You Need MCP

Look at your AI Building Block Map:

- Steps tagged with **"MCP"** in the AI Building Block(s) column
- The **Tools and Connectors Required** section lists every external integration
- Steps requiring **web browsing, database access, file system access, or API calls**

If your workflow only needs information you can paste into a conversation, you don't need MCP. If it needs to read from or write to external systems, you do.

## Common MCP Patterns

**Notion** — Read and write databases, create pages, update records. Useful for workflows that track status, store outputs, or pull reference data from Notion.

**Browser automation** — Web search, data collection, site interaction. Useful for research workflows, monitoring, and data gathering.

**File systems** — Read and write local files. Useful for workflows that process documents, generate reports, or manage file-based outputs.

**Custom APIs** — Domain-specific integrations (CRM, project management, communication tools). Useful for workflows that need to interact with your existing business tools.

## How MCP Connects to Your Workflow

1. **Check "Tools and Connectors Required"** in your Building Block Map — each external tool listed needs an MCP connection
2. **Identify available MCP servers** — Many common tools already have MCP servers (Notion, browser, file system). See [Agentic Building Blocks > MCP](../../agentic-building-blocks/mcp/index.md) for the list.
3. **Configure each connection** — MCP servers are configured once, then available to all agents and skills in your workspace
4. **Test the connection** — Verify the AI can read from and write to the external system before running the full workflow

## What's Next

With your MCP connections configured, your workflow has everything it needs. Return to the [Build overview](index.md) to review the full build process, or test your baseline prompt on a real scenario.
