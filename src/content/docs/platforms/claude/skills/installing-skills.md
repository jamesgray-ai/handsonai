---
title: Installing Skills on Claude
description: How to add Agent Skills to Claude.ai, Claude Cowork, and Claude Code
---

Claude supports Agent Skills natively across all three products. Skills uploaded to **claude.ai → Customize → Skills** appear in both Claude Chat and Cowork — they share the same personal skill library. Skills bundled in a **Cowork plugin** (like `handsonai`) are Cowork-only — Claude Chat has no plugin install surface, so plugin-installed skills don't cross over.

## Claude.ai (web)

Upload a skill `.zip` under **Settings > Capabilities > Upload skill**. Requires Claude Pro, Max, Team, or Enterprise and Code execution turned on.

→ [Use Skills in Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude) (official Anthropic docs)

## Claude Cowork

Open the **Cowork** tab in the Claude Desktop app, then go to **Customize → Browse plugins → Personal** and add a marketplace. Skills bundled in the plugin (including the `framework-agent` orchestrator) run in **Cowork only** — they're not available in Claude Chat. If you also want the seven framework skills in Claude Chat, upload them via **claude.ai → Customize → Skills** (covered above) — skills uploaded that way appear in both Chat and Cowork.

→ Step-by-step instructions: [AI Workflow Framework skills setup — Claude Cowork](/ai-workflow-framework/skills/#set-up-these-skills)

→ [Getting started with Cowork](https://support.claude.com/en/articles/13345190-getting-started-with-cowork) (official Anthropic docs)

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
- [Discover Your Best Claude Skills](/platforms/claude/skills/skills-discovery-meta-prompt/) — find your highest-value skill candidates
