---
title: MCP Server
description: Connect to the Hands-on AI Cookbook from Claude, ChatGPT, Claude Code, and other MCP-compatible tools
---

# MCP Server

The Hands-on AI Cookbook is available as an MCP (Model Context Protocol) server, so you can get cookbook-informed answers directly in your AI tools — no API keys or authentication required.

**MCP server URL:** `https://mcp.handsonai.info/mcp`

## What You Get

The MCP server gives your AI assistant access to:

- **Search** across all cookbook pages by keyword
- **Read** the full content of any page
- **Browse** sections like Building Blocks, Framework, Use Cases, and more
- **Deep dive** into building blocks or framework steps with all sub-pages
- **Q&A lookup** with quick answers from the cookbook's question pages
- **Setup guides** for every tool in the Builder Stack

## Connect from Claude

Claude supports remote MCP servers as custom connectors across all its products. Add the connector once, and it's available in Claude chat, Claude Desktop, and Cowork.

### Claude (claude.ai) and Claude Desktop

1. Go to **Settings** → **Connectors**
2. Scroll to the bottom and click **Add custom connector**
3. Enter the MCP server URL: `https://mcp.handsonai.info/mcp`
4. Click **Add**

To use it in a conversation, click the **+** button in the chat input area, select **Connectors**, and toggle the Hands-on AI Cookbook connector on.

!!! tip "Works on Pro, Max, Team, and Enterprise plans"
    Custom connectors are available on all paid Claude plans. Team and Enterprise owners configure connectors in **Organization settings** → **Connectors**, then members enable them individually in their personal settings.

### Claude Cowork

Once you've added the connector using the steps above, it's automatically available in Cowork. When Cowork runs a task, it can use the cookbook connector to search for relevant content, look up setup guides, or reference building block definitions.

### Claude Code

Run this command in your terminal:

```bash
claude mcp add handsonai-cookbook --transport http https://mcp.handsonai.info/mcp
```

That's it. Claude Code will now have access to all cookbook tools in every conversation.

## Connect from ChatGPT

ChatGPT supports remote MCP servers as apps. Available on Plus, Pro, Team, Enterprise, and Edu plans.

**Enable Developer Mode (one-time setup):**

1. Go to **Settings** → **Apps**
2. Under **Advanced settings**, toggle **Developer Mode** on

**Add the app:**

1. In **Settings** → **Apps**, click **Create app**
2. Fill in:
    - **Name:** Hands-on AI Cookbook
    - **URL:** `https://mcp.handsonai.info/mcp`
3. Check the box confirming you trust this application
4. Click **Create**

**Use it in a conversation:**

1. Start a new chat
2. Click **+** → **More** → **Developer Mode**
3. Select the Hands-on AI Cookbook app to enable it

!!! note "Enable per conversation"
    The app must be explicitly added to each new chat session via Developer Mode. It works in both regular chat and Deep Research mode.

## Connect from Other MCP Clients

Any MCP client that supports Streamable HTTP transport can connect:

- **URL:** `https://mcp.handsonai.info/mcp`
- **Transport:** Streamable HTTP (POST with JSON-RPC 2.0)
- **Authentication:** None required (public, read-only)

## Available Tools

| Tool | Description |
|------|-------------|
| `search_cookbook` | Search pages by keyword, optionally filtered to a section |
| `get_page` | Get the full content of a specific page by path |
| `list_section` | List all pages in a section (building-blocks, framework, use-cases, etc.) |
| `get_building_block` | Get a building block and all its sub-pages (prompts, agents, mcp, etc.) |
| `get_framework_step` | Get a framework step and all its sub-pages (discover, deconstruct, build) |
| `list_questions` | List all Q&A pages with question text and short answers |
| `get_setup_guide` | Get a Builder Stack setup guide (terminal, editor, git, claude-code, etc.) |

## Example Prompts

Once connected, try asking your AI assistant:

- "What are the agentic building blocks?"
- "How do I set up Claude Code?"
- "Search the cookbook for prompt engineering techniques"
- "What's the Business-First AI Framework?"
- "Show me the automation use case"

The AI will use the cookbook MCP tools to pull relevant content and answer with cookbook knowledge.
