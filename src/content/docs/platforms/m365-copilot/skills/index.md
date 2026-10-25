---
title: Skills on M365 Copilot
description: How Agent Skills work in Microsoft 365 Copilot Cowork — upload a ZIP from the Customize page, or drop a SKILL.md folder in OneDrive
---

Microsoft 365 Copilot supports Agent Skills natively in **Copilot Cowork**, which is generally available to Microsoft 365 Copilot license holders (your admin enables it; it uses usage-based billing). Copilot Cowork reads `SKILL.md` files from a folder in your OneDrive, and the Customize page can put them there for you — no plugin install, no terminal.

**Before you start:** open Microsoft 365 Copilot at [copilot.cloud.microsoft](https://copilot.cloud.microsoft), signed in with your work or school account, and look for Copilot Cowork (labelled **Cowork**) in the toggle at the top, next to **Chat**. If it isn't there, ask your IT admin to enable it. Custom skills aren't available in Copilot Cowork on mobile.

## Upload a skill (easiest)

In Copilot Cowork: **Customize → Skills → the arrow next to Add → Upload skill**, then choose a `.md`, `.zip`, or `.skill` file. Copilot Cowork validates it and saves it to your OneDrive; it appears under **Your skills** after a few moments. Upload the Hands-on AI ZIPs as downloaded (for example `analyze.zip`). If Copilot Cowork rejects one, unzip it and put the skill folder in `Documents/Cowork/skills/` in your OneDrive instead. Uploading a skill with the same name again creates a numbered copy rather than replacing — delete the old one first to update.

→ [Upload a skill](https://learn.microsoft.com/en-us/microsoft-365/copilot/cowork/cowork-customize#upload-a-skill) (Microsoft Learn)

## Or put the folder in OneDrive yourself

- **Where they live:** `Documents/Cowork/skills/<skill-name>/SKILL.md` in your OneDrive (lowercase `skills`)
- **How they're discovered:** automatically at the start of each session; loaded skills appear as chips in the side panel under **Skills**
- **Companion files:** up to 20 per skill (reference documents, scripts), 10 MB per skill

1. In OneDrive, open `Documents/Cowork/skills/` — create the folders if they don't exist.
2. Create a subfolder named for the skill and put `SKILL.md` inside it.
3. Start a new Copilot Cowork conversation — the skill is available immediately.

→ [Copilot Cowork skills](https://learn.microsoft.com/en-us/microsoft-365/copilot/cowork/use-cowork#cowork-skills) (Microsoft Learn)

**Limits:** up to 50 custom skills; 1 MB per `SKILL.md`; 20 companion files and 10 MB per skill. An uploaded `.zip` or `.skill` file can be up to 10 MB compressed (50 MB uncompressed) and 100 files. (Microsoft Learn, read 2026-10-24.)

**Classic M365 Copilot:** no native skill support outside Copilot Cowork.

## Skills here, agents in Agent Builder

Microsoft 365 Copilot has two places to build, and the AI Workflow Framework uses both (verified 2026-10-24):

- **Skills** are made in Copilot Cowork, as on this page.
- **Agents** are made in Agent Builder: **Copilot › Chat › Agents › New agent**. The ordinary Copilot Chat can describe an agent, but it can't create one. See [Building Agents on M365 Copilot](/platforms/m365-copilot/agents/building-agents/#build-an-agent-with-agent-builder).

**Your framework files** live in a folder called `Framework` in your OneDrive, separate from Copilot Cowork's own `Documents/Cowork/` folder. Run each framework step in a new Copilot Cowork chat and name the folder ("My files are in OneDrive, in Framework/weekly-status-report."): the chat reads the files there with nothing attached. Copilot Cowork can see your whole OneDrive, so the framework reads and saves only inside that folder. If Copilot Cowork can't read the folder (an admin may limit its OneDrive access), the step asks you to attach your Framework folder to the chat.

## Related

- [Skills building block](/agentic-building-blocks/skills/) — what skills are and how they work across platforms
- [Building Agents on M365 Copilot](/platforms/m365-copilot/agents/building-agents/) — Agent Builder, the place to build agents
- [AI Workflow Framework skills setup](/ai-workflow-framework/skills/) — step-by-step setup for the five framework skills in Copilot Cowork
