---
title: Skills on Cursor
description: How Agent Skills work in Cursor — where they live, how to install, and cross-editor portability
---

Cursor supports Agent Skills natively. It reads skill folders from multiple locations, so skills installed for Claude Code or Codex are picked up automatically — no duplication required.

## Where skills live

Cursor reads `SKILL.md` files from any of these directories at your project root:

- `.cursor/skills/` — Cursor-specific
- `.claude/skills/` — shared with Claude Code
- `.codex/skills/` — shared with Codex
- `.agents/skills/` — shared convention across Cursor, Codex CLI, Gemini CLI, and VS Code Copilot

The `.agents/skills/` directory is the most portable — place skills there to share them across multiple editors from one location.

## Installing skills

1. Place the skill folder in `.cursor/skills/` (or one of the shared directories above) at your project root.
2. Open the project in Cursor — skills are discovered automatically.

→ [Cursor Skills documentation](https://cursor.com/docs/context/skills) (official Cursor docs)

## Related

- [Skills building block](/agentic-building-blocks/skills/) — what skills are and how they work across platforms
- [Business-First AI Framework skills setup](/business-first-ai-framework/skills/) — step-by-step setup for the seven framework skills on Cursor
