---
title: Skills on M365 Copilot
description: How Agent Skills work in Microsoft 365 Copilot Cowork — what's supported, how to install, and gotchas
---

Microsoft 365 Copilot Cowork supports Agent Skills natively via OneDrive. Cowork reads `SKILL.md` files directly from your OneDrive folder — no plugin install, no terminal.

Cowork is currently a **Frontier preview** feature, available only to customers enrolled in the [Frontier program](https://adoption.microsoft.com/en-us/copilot/frontier-program/).

## What skills look like on M365 Copilot

- **Where they live:** `Documents/Cowork/Skills/<skill-name>/SKILL.md` in your OneDrive
- **How they're discovered:** auto-discovered each conversation; skills appear as chips in the Cowork side panel when invoked
- **Format:** same `SKILL.md` open standard used by Claude, OpenAI, and other native-skill platforms
- **Classic M365 Copilot:** no native skill support outside Cowork

## Installing skills

1. Confirm you have an M365 Copilot license and Frontier preview access.
2. Open OneDrive and navigate to `Documents/Cowork/Skills/` — create the folders if they don't exist.
3. Place the skill folder (containing `SKILL.md`) inside `Skills/`.
4. Start a new Cowork conversation — the skill is available immediately.

**Limits:** Up to 20 custom skills, 1 MB per `SKILL.md`.

→ [Cowork skills documentation](https://learn.microsoft.com/en-us/microsoft-365/copilot/cowork/use-cowork#cowork-skills) (official Microsoft docs)

## Related

- [Skills building block](/agentic-building-blocks/skills/) — what skills are and how they work across platforms
- [AI Workflow Framework skills setup](/ai-workflow-framework/skills/) — step-by-step setup for the seven framework skills on M365 Copilot
