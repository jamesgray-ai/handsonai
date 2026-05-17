---
question: "How do I connect an MCP server to Claude Code?"
short_answer: "Use the claude mcp add command to connect MCP servers to Claude Code with three transport options: HTTP for remote servers (recommended), stdio for local processes, or SSE for server-sent events."
platforms: [claude]
topic: mcp
date: 2026-02-07
author: James Gray
title: "How do I connect an MCP server to Claude Code?"
---**Short answer:** Use the `claude mcp add` command to connect MCP servers to Claude Code with three transport options: HTTP for remote servers (recommended), stdio for local processes, or SSE for server-sent events.

## The Full Answer

Claude Code connects to external tools and data sources through the Model Context Protocol (MCP), an open source standard for AI-tool integrations (*[Model Context Protocol documentation](https://modelcontextprotocol.io/docs/develop/connect-local-servers)*). When you add an MCP server, you're giving Claude Code access to tools, databases, and APIs that extend what it can do beyond the conversation.

There are three main ways to connect MCP servers to Claude Code, depending on whether the server runs remotely or locally. HTTP servers are the recommended option for cloud-based services and remote MCP servers. This is the most widely supported transport method. Stdio servers run as local processes on your machine, making them ideal for tools that need direct system access or custom scripts. SSE (Server-Sent Events) servers provide another option for remote services, though this transport method is deprecated in favor of HTTP (*[official Claude Code MCP documentation](https://code.claude.com/docs/en/mcp)*).

The difference between Claude Code and Claude Desktop is important to understand here. Claude Desktop uses a configuration file at `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows) (*[Getting Started with Local MCP Servers on Claude Desktop](https://support.claude.com/en/articles/10949351-getting-started-with-local-mcp-servers-on-claude-desktop)*). Claude Code, on the other hand, uses command-line configuration through the `claude mcp add` command and stores settings in `~/.claude.json` or `.mcp.json` files. While both products support MCP, Claude Code is designed for developers working in the terminal and integrates directly with your development workflow.

MCP servers can be configured at three scope levels: local (default, stored in `~/.claude.json` under your project path and available only to you in the current project), project (stored in `.mcp.json` at your project root and shared with the team via version control), and user (stored in `~/.claude.json` and available to you across all projects). Understanding these scopes helps you decide whether a server should be personal, project-specific, or available everywhere you work.

## Adding MCP Servers

### HTTP Server (Remote, Recommended)

```bash
# Basic syntax
claude mcp add --transport http <name> <url>

# Example: Connect to Notion
claude mcp add --transport http notion https://mcp.notion.com/mcp

# Example with authentication header
claude mcp add --transport http secure-api https://api.example.com/mcp \
  --header "Authorization: Bearer your-token"
```

### Stdio Server (Local Process)

```bash
# Basic syntax
claude mcp add --transport stdio <name> -- <command> [args...]

# Example: Add Airtable server
claude mcp add --transport stdio --env AIRTABLE_API_KEY=YOUR_KEY airtable \
  -- npx -y airtable-mcp-server

# Windows users need cmd /c wrapper for npx
claude mcp add --transport stdio my-server -- cmd /c npx -y @some/package
```

The double dash (`--`) separates Claude's options from the server command and its arguments. All Claude options like `--transport`, `--env`, and `--scope` must come before the server name.

### SSE Server (Deprecated)

```bash
# Basic syntax (use HTTP instead where available)
claude mcp add --transport sse <name> <url>

# Example: Connect to Asana
claude mcp add --transport sse asana https://mcp.asana.com/sse
```

### Managing Servers

```bash
# List all configured servers
claude mcp list

# Get details for a specific server
claude mcp get github

# Remove a server
claude mcp remove github

# Within Claude Code, check server status
/mcp
```

## Authentication

Many cloud-based MCP servers require OAuth 2.0 authentication. After adding a server that requires authentication, use the `/mcp` command within Claude Code and follow the browser login flow. Authentication tokens are stored securely and refreshed automatically.

Some servers require pre-configured OAuth credentials. If you see an error about "dynamic client registration," you'll need to register an OAuth app through the server's developer portal first, then provide your client ID and secret:

```bash
# Provide OAuth credentials when adding the server
claude mcp add --transport http \
  --client-id your-client-id --client-secret --callback-port 8080 \
  my-server https://mcp.example.com/mcp
```

## Key Takeaways

- Use `claude mcp add` with one of three transport types: HTTP (recommended for remote), stdio (for local processes), or SSE (deprecated)
- Choose the right scope: local (default, project-specific and private), project (shared via version control), or user (available across all projects)
- Authentication is handled through OAuth 2.0 for remote servers, with automatic token refresh
- Claude Desktop and Claude Code use different configuration methods - Desktop uses a JSON file or Extensions UI, while Code uses CLI commands
- All options like `--transport`, `--env`, and `--scope` must come before the server name, followed by `--` to separate from the server command

## Related Questions

- [What is MCP and when should I use it?](/agentic-building-blocks/mcp/)
- [How do I set up Claude Code?](/platforms/claude/getting-started/#3-install-claude-code)
