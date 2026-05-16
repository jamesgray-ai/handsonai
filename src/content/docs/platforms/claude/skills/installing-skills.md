---
title: Installing Skills on Claude
description: How to add Agent Skills to Claude.ai, Claude Cowork, and Claude Code
---

Claude supports Agent Skills natively across all three products. Skills you upload to Claude.ai are automatically available in Claude Cowork — they share the same skill library.

## Claude.ai (web)

Upload a skill `.zip` under **Settings > Capabilities > Upload skill**. Requires Claude Pro, Max, Team, or Enterprise and Code execution turned on.

→ [Use Skills in Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude) (official Anthropic docs)

## Claude Cowork

Install a plugin via **+** > **Add plugins** in Claude Desktop. Any skills you uploaded to Claude.ai are also available in Cowork automatically — no extra step.

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
