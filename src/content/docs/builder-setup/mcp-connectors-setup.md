---
title: "MCP Connectors Setup Guide"
---Quick reference for connecting Claude to external applications and MCP servers.

## Overview

Claude can connect to external tools and data sources through:

1. **Integrations** — Built-in connections to cloud services (Google Drive, Gmail, GitHub)
2. **Custom Connectors** — Remote MCP servers you configure
3. **Desktop Extensions** — Local MCP servers on your machine (Desktop only)

## Part 1: Built-in Integrations

Claude offers built-in integrations with popular services.

### Available Integrations

| Integration | Free | Pro | Max | Team | Enterprise |
|-------------|------|-----|-----|------|------------|
| GitHub | ✓ | ✓ | ✓ | ✓ | ✓ |
| Google Drive | ✓ | ✓ | ✓ | ✓ | ✓ |
| Gmail | ✓ | ✓ | ✓ | ✓ | ✓ |
| Google Calendar | ✓ | ✓ | ✓ | ✓ | ✓ |

### Enable an Integration

**From the chat interface:**
1. Click the **+** button in the lower left of the chat window
2. Select the integration you want to connect
3. Complete the authentication flow

**From settings:**
1. Go to **Settings → Connectors**
2. Find the integration and click **Connect**
3. Complete the authentication flow

### For Team/Enterprise Plans

Organization Owners must first enable integrations:
1. Go to **Admin settings → Connectors**
2. Click **Enable** next to the integration
3. Team members can then connect individually through their settings

## Part 2: Custom Connectors (Remote MCP Servers)

Custom connectors let you connect Claude to remote MCP servers.

**Available on:** Claude web and Desktop (Pro, Max, Team, Enterprise)

### Add a Custom Connector

1. Go to **Settings → Connectors**
2. Click **Add custom connector**
3. Enter the remote MCP server URL
4. (Optional) Configure OAuth credentials in Advanced settings
5. Complete setup

### Enable Connectors in a Conversation

1. Click the **+** button in the chat interface
2. Select **Connectors**
3. Toggle on the connectors you want to use

## Part 3: Desktop Extensions (Local MCP Servers)

Desktop Extensions connect Claude to MCP servers running on your local machine.

**Available on:** Claude Desktop only (not web)

### Browse and Install Extensions

1. Open Claude Desktop
2. Go to **Settings → Extensions**
3. Browse available extensions
4. Click to install

### Manual Configuration

For custom MCP servers, edit the configuration file directly.

**Configuration file location:**

| Platform | Path |
|----------|------|
| macOS | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Windows | `%APPDATA%\Claude\claude_desktop_config.json` |

**Example configuration:**

```json
{
  "mcpServers": {
    "my-server": {
      "command": "node",
      "args": ["/path/to/your/server.js"]
    }
  }
}
```

After editing, restart Claude Desktop for changes to take effect.

## Configure Tool Permissions

Each connector has individual tool permissions that control when Claude can use specific capabilities.

### Access Tool Permissions

1. Go to **Settings → Connectors**
2. Click on a connected integration (e.g., Notion)
3. View the **Tool permissions** section

### Permission Levels

Each tool can be set to one of three permission levels:

| Icon | Level | Behavior |
|------|-------|----------|
| ✓ | Always allow | Claude can use without asking |
| ✋ | Ask each time | Claude requests permission before using |
| ⊘ | Never | Claude cannot use this tool |

### Tool Categories

Tools are grouped by their capabilities:

**Read-only tools** — Fetch and search data (lower risk)
- Example: `notion-fetch`, `notion-search`, `notion-get-users`
- Default: Often set to "Always allow"

**Write/delete tools** — Create, modify, or delete data (higher risk)
- Example: `notion-create-pages`, `notion-update-database`, `notion-move-pages`
- Default: Often set to "Ask each time" or custom per-tool

### Recommended Approach

- **Read-only tools**: "Always allow" for smoother workflows
- **Write/delete tools**: "Ask each time" until you're comfortable with how Claude uses them
- Review permissions when first connecting a new integration

## Verify Connectors Are Working

1. Start a new conversation
2. Click the **+** button
3. Hover over **Connectors** to see available servers
4. Your configured connectors should appear in the list

## Security Considerations

- Only connect to servers from organizations you trust
- Review permission requests during OAuth authentication
- All data transfers use encryption
- Integrations work only in private projects
- Chats with synced content cannot be shared

## Troubleshooting

**Integration not appearing?**
- Check you have the required plan
- For Team/Enterprise, verify the Owner has enabled it
- Try disconnecting and reconnecting

**Custom connector not connecting?**
- Verify the MCP server URL is correct
- Check the server is running and accessible
- Review OAuth credentials if required

**Desktop extension not loading?**
- Check the configuration file syntax (valid JSON)
- Verify the path to your server is absolute
- Restart Claude Desktop completely (quit, not just close window)
- Check logs at `~/Library/Logs/Claude/mcp.log` (macOS)

## Next Steps

- Review the course slide deck for detailed walkthrough
- Explore the MCP server directory for available integrations
- Post in Slack if you encounter issues

## Resources

- [About Custom Integrations Using Remote MCP](https://support.claude.com/en/articles/11175166-about-custom-integrations-using-remote-mcp)
- [Setting Up Claude Integrations](https://support.claude.com/en/articles/10168395-setting-up-claude-integrations)
- [Model Context Protocol Documentation](https://modelcontextprotocol.io)
- [MCP Quickstart Guide](https://modelcontextprotocol.io/quickstart)
