---
title: Getting Started with Plugins
description: How to add the Hands-on AI marketplace, install plugins, and use them in Claude Code
---

# Getting Started with Plugins

This guide walks you through adding the Hands-on AI plugin marketplace, installing your first plugin, and using the agents and skills it provides.

## Prerequisites

- **Claude Code** installed and working ([Installation Guide](../fundamentals/developer-setup/claude-code-install.md))
- An active **Claude Pro, Team, or Enterprise** subscription

## Step 1: Add the Marketplace

A marketplace is a repository that hosts one or more plugins. You only need to add it once.

```bash
/plugin marketplace add jamesgray-ai/handsonai
```

This tells Claude Code where to find the Hands-on AI plugins. It does not install anything yet.

!!! tip
    You can see which marketplaces you've added with `/plugin marketplace list`.

## Step 2: Install a Plugin

Choose the plugin that matches your workflow:

=== "HBR Content Suite"

    ```bash
    /plugin install hbr-content-suite@handsonai
    ```

    Installs 3 agents and 1 skill for writing, editing, and publishing business articles.

=== "AI Research Agents"

    ```bash
    /plugin install ai-research-agents@handsonai
    ```

    Installs 3 research agents for AI news, productivity case studies, and daily Claude briefings.

After installing, the plugin's agents and skills are available in your Claude Code session.

## Step 3: Use Plugin Commands

Installed plugins add agents and skills that Claude Code can use automatically. Here's what each plugin provides:

### HBR Content Suite

| Command type | Name | How to trigger |
|-------------|------|----------------|
| Agent | `tech-executive-writer` | Ask Claude to write business content about a technical topic |
| Agent | `hbr-editor` | Ask Claude to review or edit an article for HBR quality |
| Agent | `hbr-publisher` | Ask Claude to prepare a finalized article for publication |
| Skill | `editing-hbr-articles` | Loaded automatically by the `hbr-editor` agent |

**Example prompts:**

- "Write a LinkedIn post about how RAG is transforming enterprise search"
- "Review this article against HBR editorial standards"
- "Prepare this article for web publication and create a PDF version"

### AI Research Agents

| Command type | Name | How to trigger |
|-------------|------|----------------|
| Agent | `ai-news-researcher` | Ask Claude about recent AI news or developments |
| Agent | `ai-productivity-researcher` | Ask Claude for AI productivity case studies |
| Agent | `claude-research-daily` | Ask Claude for the latest Claude/Anthropic updates |

**Example prompts:**

- "What's new in AI today?"
- "Find examples of companies using AI agents for customer support"
- "What are the latest Claude Code features?"

## Updating Plugins

When a plugin is updated with new agents, skills, or improvements, pull the latest version:

```bash
/plugin update hbr-content-suite@handsonai
```

Or update all installed plugins at once:

```bash
/plugin update --all
```

## Uninstalling

To remove a plugin you no longer need:

```bash
/plugin uninstall hbr-content-suite@handsonai
```

To remove the marketplace entirely:

```bash
/plugin marketplace remove handsonai
```

## Troubleshooting

### "Marketplace not found"

Make sure you've added the marketplace first:

```bash
/plugin marketplace add jamesgray-ai/handsonai
```

### "Plugin not found"

Check the plugin name is spelled correctly and includes the `@handsonai` suffix:

```bash
# Correct
/plugin install hbr-content-suite@handsonai

# Wrong — missing marketplace suffix
/plugin install hbr-content-suite
```

### "Permission denied" or authentication errors

The marketplace repository is public. If you see authentication errors, check your GitHub CLI configuration:

```bash
gh auth status
```

### Plugin agents not appearing

After installing a plugin, you may need to restart your Claude Code session for the agents and skills to become available.

### Checking installed plugins

List everything you have installed:

```bash
/plugin list
```
