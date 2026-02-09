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

Without MCP, the AI only knows what you paste into the conversation. With MCP, it can look up records in your CRM, check task status in your project management tool, search your Notion workspace, or pull live data from a database — all within the conversation, without you copying and pasting.

| | |
|---|---|
| **What you'll do** | Review your Building Block Map for steps requiring external tool access, then configure the MCP connections those steps need |
| **What you'll get** | Working connections between your AI workflow and external systems |
| **Time** | 10-30 minutes per connection (varies by tool complexity) |

!!! info "Most workflows don't need MCP"
    If your workflow runs on information you can paste into a conversation or upload as files, you don't need MCP. Only add it when your workflow requires live data from external systems or needs the AI to take actions in other tools (creating tasks, updating records, sending messages).

## When You Need MCP

Look at your AI Building Block Map:

- Steps tagged with **"MCP"** in the AI Building Block(s) column
- The **Tools and Connectors Required** section lists every external integration
- Steps requiring **web browsing, database access, file system access, or API calls**

If your Building Block Map doesn't tag any steps with MCP, skip this page and go straight to [Run](run.md).

## What Configuring MCP Looks Like

Connecting an external tool works like connecting an app to your phone — you set it up once, authorize access, and then it's available whenever you need it.

Each connection has three parts:

1. **Get access credentials** — Most tools require an API key (a password-like code that authorizes the connection). You create this in the external tool's settings, usually under "Integrations" or "Developer."
2. **Add the connection to your AI tool** — Tell your AI tool where to find the external service and how to authenticate. The specifics depend on your platform (see table below).
3. **Test it** — Ask the AI to do something simple with the connected tool ("Search my Notion workspace for...") to verify the connection works.

### How different platforms handle external connections

| Platform | What it's called | How to set it up |
|----------|-----------------|-----------------|
| **Claude Code** | MCP servers | Add server configuration to your project's settings file. Claude Code runs the server locally on your computer. |
| **Claude Desktop** | MCP servers | Same as Claude Code — add to the app's configuration file. |
| **ChatGPT** | Actions (in Custom GPTs) | Build into a Custom GPT using the **Actions** section of the GPT builder. Define the external API endpoint and authentication. |
| **Gemini** | Extensions | Enable built-in extensions (Google Workspace, Maps, YouTube) in settings, or connect custom services via the API. |
| **M365 Copilot** | Connectors + Power Platform | Configure in **Copilot Studio** or through the Microsoft 365 admin center. Pre-built connectors available for many business tools. |

The concept is the same on every platform: you're giving AI authorized access to read from or write to an external system. The setup steps differ, but the result is the same.

## Common MCP Patterns

| Pattern | What the AI can do | Example tools |
|---------|-------------------|---------------|
| **Knowledge management** | Read and write to your knowledge bases — search pages, create entries, update records | Notion, Confluence, Google Drive |
| **Project management** | Create tasks, update status, query boards | Linear, Jira, Asana, Trello |
| **Communication** | Read messages, send updates, manage threads | Slack, Email, Teams |
| **Data access** | Query databases, retrieve records, run reports | PostgreSQL, Supabase, Airtable |
| **Web research** | Search the web, visit pages, collect information | Browser automation, web search |
| **File systems** | Read and write local files, process documents | Local file system access |

## Example: Connecting Notion

Here's what it looks like to connect a common tool — Notion — so you can see the shape of the process:

1. **Create a Notion integration** — Go to [notion.so/my-integrations](https://www.notion.so/my-integrations), click **New integration**, give it a name, and copy the API key it generates
2. **Share your Notion pages with the integration** — In Notion, open each database or page you want the AI to access, click **...** > **Connections** > select your integration
3. **Add the connection to your AI tool** — On Claude Code, this means adding the Notion MCP server to your configuration with the API key. On ChatGPT, you'd add Notion as an Action in your Custom GPT.
4. **Test it** — Ask the AI: *"Search my Notion workspace for [something you know exists]"* — if it finds it, you're connected

After setup, the AI can search your databases, create pages, and update records as part of your workflow — no more copying and pasting data between Notion and your AI tool.

## How MCP Connects to Your Workflow

1. **Check "Tools and Connectors Required"** in your Building Block Map — each external tool listed needs a connection
2. **Start with one connection** — Pick the single external system your workflow depends on most. Get that working before adding more.
3. **Identify available servers** — Many common tools already have pre-built MCP servers or connectors. See [Agentic Building Blocks > MCP](../../agentic-building-blocks/mcp/index.md) for available options and setup guides.
4. **Configure and test** — Follow the setup steps for your platform, then verify the AI can read from and write to the external system before running the full workflow
5. **Add more as needed** — Once your first connection works, add others from your Building Block Map's requirements list

## What's Next

With your MCP connections configured, your workflow has everything it needs. [Run your workflow](run.md) on a real scenario, or return to the [Build overview](index.md) to review the full build process.
