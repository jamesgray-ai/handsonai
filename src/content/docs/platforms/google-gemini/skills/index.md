---
title: Skills on Google Gemini
description: How Agent Skills work on Google Gemini — what's supported in Gemini CLI and Antigravity, and workarounds for the Gemini app and Gemini Enterprise
---

Google's developer tools — **Gemini CLI** and **Antigravity** — support Agent Skills natively. The consumer **Gemini app** and **Gemini Enterprise** don't have native skill support, but you can use **Gems** or paste the `SKILL.md` contents into your prompt to get the same result.

## Gemini CLI / Antigravity

Gemini CLI and Antigravity read skill folders from your project root using the same `SKILL.md` open standard as Claude and other native-skill platforms.

**Installing skills:**

1. Place the skill folder in `.gemini/skills/` (or `.agents/skills/`) at your project root.
2. Start Gemini CLI or open the project in Antigravity — skills are discovered automatically.

→ [Skills in Gemini CLI](https://geminicli.com/docs/cli/skills/) (official docs)

## Gemini app (consumer)

No native skill support. Use a **Gem** as the workaround:

1. Open [Gemini](https://gemini.google.com) and create a new Gem.
2. Paste the `SKILL.md` contents into the Gem's instructions field.
3. Select the Gem from the sidebar whenever you want to run the skill.

→ [Create a Gem](https://support.google.com/gemini/answer/15235603) (official Google docs)

## Gemini Enterprise

No native skill support. Paste the `SKILL.md` contents into your prompt each time, or into a saved instruction set if your plan supports one.

## Related

- [Skills building block](/agentic-building-blocks/skills/) — what skills are and how they work across platforms
- [Business-First AI Framework skills setup](/business-first-ai-framework/skills/) — step-by-step setup for the seven framework skills on Google Gemini tools
