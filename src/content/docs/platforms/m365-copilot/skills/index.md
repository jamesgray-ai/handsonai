---
title: Skills on M365 Copilot
description: How Agent Skills work in Microsoft 365 Copilot Cowork — upload a ZIP from the Customize page, or drop a SKILL.md folder in OneDrive
---

Microsoft 365 Copilot supports Agent Skills natively in **Copilot Cowork**, which is generally available to Microsoft 365 Copilot license holders (your admin enables it; it uses usage-based billing). Cowork reads `SKILL.md` files from a folder in your OneDrive, and the Customize page can put them there for you — no plugin install, no terminal.

**Before you start:** open Microsoft 365 Copilot and look for **Cowork** in the left navigation. If it isn't there, ask your IT admin to enable it. Custom skills aren't available in Cowork on mobile.

## Upload a skill (easiest)

In Cowork: **Customize → Skills → the arrow next to Add → Upload skill**, then choose a `.md`, `.zip`, or `.skill` file. Cowork validates it and saves it to your OneDrive; it appears under **Your skills** after a few moments. Microsoft's docs describe a ZIP with `SKILL.md` at its root and companion files beside it; the Hands-on AI downloads come in both layouts (`analyze.zip` and `analyze-flat.zip`) — use the flat one if the first is rejected. Uploading a skill with the same name again creates a numbered copy rather than replacing — delete the old one first to update.

→ [Upload a skill](https://learn.microsoft.com/en-us/microsoft-365/copilot/cowork/cowork-customize#upload-a-skill) (Microsoft Learn)

## Or put the folder in OneDrive yourself

- **Where they live:** `Documents/Cowork/skills/<skill-name>/SKILL.md` in your OneDrive (lowercase `skills`)
- **How they're discovered:** automatically at the start of each session; loaded skills appear as chips in the side panel under **Skills**
- **Companion files:** up to 20 per skill (reference documents, scripts), 10 MB per skill

1. In OneDrive, open `Documents/Cowork/skills/` — create the folders if they don't exist.
2. Create a subfolder named for the skill and put `SKILL.md` inside it.
3. Start a new Cowork conversation — the skill is available immediately.

→ [Cowork skills](https://learn.microsoft.com/en-us/microsoft-365/copilot/cowork/use-cowork#cowork-skills) (Microsoft Learn)

**Limits:** up to 50 custom skills; 1 MB per `SKILL.md`; 20 companion files and 10 MB per skill.

**Classic M365 Copilot:** no native skill support outside Cowork.

## Related

- [Skills building block](/agentic-building-blocks/skills/) — what skills are and how they work across platforms
- [AI Workflow Framework skills setup](/ai-workflow-framework/skills/) — step-by-step setup for the seven framework skills in Copilot Cowork
