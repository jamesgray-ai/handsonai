---
title: Installing Skills on Claude
description: How to add Agent Skills to Claude — one plugin install covers Claude Chat, the Claude app, and Cowork; ZIP upload works on every plan; Claude Code uses two commands
---

Claude supports Agent Skills natively everywhere: Claude Chat on the web, the Chat tab in the Claude app, Cowork, and Claude Code. There are two ways to add them, and both are managed from **Customize** in the left sidebar.

**Before you start:** click **Customize**. If you see a **Plugins** tab, you can install plugins (paid plans). If you only see **Skills**, use the ZIP upload — it works on every plan, including Free.

## Install a plugin (recommended on paid plans)

A plugin bundles a set of skills so you install them once. **Customize → Plugins → + → Add marketplace → Add from a repository**, paste the marketplace address (for the Hands-on AI plugin: `jamesgray-ai/handsonai-plugins`), click **Sync**, then **Install** on the plugin card.

Skills from a plugin work in Claude Chat on the web, the Chat tab in the Claude app, and Cowork. Hooks and sub-agents (like the `framework-agent` orchestrator) run only in Cowork.

→ [Use plugins in Claude](https://support.claude.com/en/articles/13837440-use-plugins-in-claude) (official Anthropic docs)

## Upload a skill ZIP (every plan)

**Customize → Skills → + → Create skill → Upload a skill**, then choose the `.zip` — don't unzip it first. Turn the skill on in the list. Requires **Code execution** to be on under **Settings → Capabilities**. Uploaded skills appear in both Chat and Cowork on your account.

→ [Use skills in Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude) (official Anthropic docs)

→ Step-by-step for the framework skills, with screenshots: [Set Up the Skills — Claude](/ai-workflow-framework/skills/#set-up-these-skills)

## Claude Code

Install a plugin from a marketplace, or drop skill folders into `.claude/skills/`:

```bash
/plugin marketplace add <owner>/<repo>
/plugin install <plugin>@<marketplace>
```

→ [Skills in Claude Code](https://code.claude.com/docs/en/skills) (official Anthropic docs)

## Related

- [Skills building block](/agentic-building-blocks/skills/) — what skills are and how they work
- [AI Workflow Framework skills setup](/ai-workflow-framework/skills/) — step-by-step setup for the seven framework skills
- [How to Discover Your Best Agent Skills](/agentic-building-blocks/skills/skills-discovery-meta-prompt/) — find your highest-value skill candidates
