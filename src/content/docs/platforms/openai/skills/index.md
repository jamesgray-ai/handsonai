---
title: Skills on OpenAI
description: How Agent Skills work on OpenAI Codex and ChatGPT — what's supported, how to install, and workarounds
---

OpenAI supports Agent Skills natively in **OpenAI Codex** (CLI, desktop app, and IDE extension). **ChatGPT** native skill support is rolling out on some plans; on plans without native support, **Projects** is the closest workaround.

## OpenAI Codex (CLI, desktop, IDE extension)

OpenAI Codex reads skill folders from your project root. The same `SKILL.md` open standard used by Claude and other native-skill platforms works here.

**Installing skills:**

1. Place the skill folder in `.agents/skills/` (or `.codex/skills/`) at your project root.
2. Open the project in OpenAI Codex — skills are discovered automatically.

→ [Skills in OpenAI Codex](https://developers.openai.com/codex/skills) (official OpenAI docs)

## ChatGPT

**Native skills:** rolling out on some plans (currently in beta). Every account includes a default `skill-creator` skill you can use to create, edit, and troubleshoot your own skills directly in chat. Enterprise and Edu accounts have skills disabled by default — admins can enable them in workspace settings.

→ [Skills in ChatGPT](https://help.openai.com/en/articles/20001066-skills-in-chatgpt) (official OpenAI docs)

**Projects workaround:** on plans without native skill support, use **Projects** to hold instructions and context. A Project with the skill's instructions pasted in behaves like a skill across a conversation — the model follows the same structure and output format every time.

→ [Using Projects in ChatGPT](https://help.openai.com/en/articles/10169521-using-projects-in-chatgpt) (official OpenAI docs)

## Related

- [Skills building block](/agentic-building-blocks/skills/) — what skills are and how they work across platforms
- [AI Workflow Framework skills setup](/ai-workflow-framework/skills/) — step-by-step setup for the seven framework skills on OpenAI Codex and ChatGPT
