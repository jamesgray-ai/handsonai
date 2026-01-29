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

Browse the [Plugin Marketplace](./) to find a plugin that matches your workflow. Each plugin lists the agents and skills it includes.

To install a plugin, use the install command shown on the marketplace page:

```bash
/plugin install <plugin-name>@handsonai
```

For example:

```bash
/plugin install hbr-content-suite@handsonai
```

After installing, the plugin's agents and skills are available in your Claude Code session.

!!! tip
    You can install as many plugins as you like. They don't conflict with each other.

## Step 3: Use Plugin Commands

Installed plugins add agents and skills that Claude Code can use automatically. You don't need to call them by name — just describe what you need and Claude will use the right agent or skill.

**Example prompts:**

- "Write a LinkedIn post about how RAG is transforming enterprise search"
- "What's new in AI today?"
- "Write an SOP for the Email Response Drafting workflow"

Each plugin on the [marketplace page](./) includes a recommended workflow and example prompts so you know exactly what to ask.

## Updating Plugins

When a plugin is updated with new agents, skills, or improvements, pull the latest version:

```bash
/plugin update <plugin-name>@handsonai
```

Or update all installed plugins at once:

```bash
/plugin update --all
```

## Uninstalling

To remove a plugin you no longer need:

```bash
/plugin uninstall <plugin-name>@handsonai
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
