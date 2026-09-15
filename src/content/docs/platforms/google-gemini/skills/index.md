---
title: Skills on Google Gemini
description: How Agent Skills work on Google Gemini — native in Gemini Spark (personal accounts), Gemini Enterprise (work accounts), Gemini CLI, and Antigravity
---

Google supports Agent Skills natively in four places, all using the same `SKILL.md` open standard as Claude and other platforms. Which one you use depends on your account and your tools:

| You have… | Use | How skills get in |
|---|---|---|
| A **personal** Google Account (gmail.com) with Google AI Pro or Ultra | **Gemini Spark** — a mode of the Gemini app | **Skills → Upload** |
| A **work or school** account and your company has Gemini Enterprise | **Gemini Enterprise** | **Skills → + → Upload skill** |
| A terminal or an AI-native IDE | **Gemini CLI** or **Antigravity** | A folder in your project |

## Gemini Spark (personal Google Account)

Spark is Gemini's agent mode: in the Gemini web app, the Gemini app for Mac, or on your phone, click **Switch to Spark** in the sidebar. Requires a personal Google Account (work and school accounts can't use Spark), a Google AI Pro or Ultra subscription, and being 18 or older; not available in the EEA, UK, Switzerland, or Nigeria.

**Adding a skill:** in Spark, click **Skills** in the sidebar, then **Upload**, and choose a `SKILL.md` or a `.zip` containing one. If it shows as disabled, use **More → Enable**. Use it by typing `/` and the skill name in a task, or let Spark pick it automatically. To update, use **More → Replace skill**; to remove, **More → Delete**. Skill names must be lowercase with hyphens (the Hands-on AI skills already are).

→ [Create & manage skills for Gemini Apps](https://support.google.com/gemini/answer/17094296) · [Gemini Spark](https://support.google.com/gemini/answer/17094507) (official Google docs)

## Gemini Enterprise (work or school account)

Available on the Standard, Plus, and Pay-as-you-go editions (Frontline can use shared skills but not upload them).

**Adding a skill:** click **Skills** in the left navigation, then **+ → Upload skill**, drag in a Markdown file or a `.zip`, and click **Import**. Google's docs ask for `SKILL.md` at the top level of the ZIP — the Hands-on AI downloads come in both layouts (`analyze.zip` and `analyze-flat.zip`); use the flat one if the first is rejected. Use it with `@` or `/` and the skill name, or by describing the task. Sharing skills with colleagues is controlled by your admin. Skills don't run inside Gemini Enterprise Agents — use them in chat.

→ [Create and manage skills — Gemini Enterprise](https://docs.cloud.google.com/gemini/enterprise/docs/skills) (official Google docs)

## Gemini CLI / Antigravity

Gemini CLI and Antigravity read skill folders from your project root.

1. Place the skill folder in `.gemini/skills/` (or `.agents/skills/`, which is shared with Cursor, Codex, and VS Code Copilot) at your project root.
2. Start Gemini CLI or open the project in Antigravity — skills are discovered automatically.

→ [Skills in Gemini CLI](https://geminicli.com/docs/cli/skills/) (official docs)

## Related

- [Skills building block](/agentic-building-blocks/skills/) — what skills are and how they work across platforms
- [AI Workflow Framework skills setup](/ai-workflow-framework/skills/) — step-by-step setup for the seven framework skills on every Gemini surface
