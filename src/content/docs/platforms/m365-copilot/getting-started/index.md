---
title: Getting Started with M365 Copilot
description: Set up your Microsoft 365 Copilot subscription, install apps, and configure Copilot features
---Complete setup checklist for Microsoft 365 Copilot. Work through each section in order.

**Time:** ~20 minutes
**Requires:** A Microsoft 365 subscription with Copilot enabled.

---

## 1. Verify Your Subscription

1. Go to [copilot.microsoft.com](https://copilot.microsoft.com) and sign in with your Microsoft account
2. Ensure your **Microsoft 365** subscription has **Copilot** enabled
3. If Copilot isn't available, check with your IT admin or see [Microsoft 365 Copilot plans](https://www.microsoft.com/en-us/microsoft-365/copilot)

**Official docs:** [Microsoft Copilot Help](https://support.microsoft.com/en-us/copilot)

---

## 2. Install and Update Apps

Update your Microsoft 365 apps to the latest version to enable Copilot features.

- **Desktop:** Update Word, Excel, PowerPoint, Outlook, and Teams to the latest version
- **Mobile:** [App Store](https://apps.apple.com/app/microsoft-copilot/id6738321700) or [Google Play](https://play.google.com/store/apps/details?id=com.microsoft.copilot)
- **Web:** Access Copilot at [copilot.microsoft.com](https://copilot.microsoft.com)

Sign in to each app with your Microsoft account.

---

## 3. Configure Copilot Features

Copilot integrates directly into your Microsoft 365 apps. Explore key features:

- **Copilot in Word:** Draft, rewrite, and summarize documents
- **Copilot in Excel:** Analyze data, create formulas, and generate charts
- **Copilot in Teams:** Summarize meetings, create action items, and draft messages
- **Copilot in Outlook:** Draft emails, summarize threads, and suggest replies

Copilot uses your Microsoft Graph data (emails, files, calendar, chats) to provide contextual responses — no separate personalization step is needed.

**Official docs:** [Get started with Microsoft 365 Copilot](https://support.microsoft.com/en-us/copilot)

---

## 4. Add Skills (Copilot Cowork)

M365 Copilot natively supports Agent Skills through **Copilot Cowork**. After adding a skill, you can say "edit this article for HBR quality" and Copilot applies professional editorial standards automatically — no re-explaining your requirements each time.

**Requires:** Enrollment in the [Frontier preview program](https://adoption.microsoft.com/en-us/copilot/frontier-program/) (Cowork is currently a Frontier preview feature).

1. In OneDrive, create the folder path `Documents/Cowork/Skills/<skill-name>/`
2. Download a `SKILL.md` from the [GitHub plugins page](https://github.com/jamesgray-ai/handsonai-plugins) (navigate to `plugins/<plugin-name>/skills/<skill-name>/SKILL.md` → click **Raw** → save the file)
3. Place the file inside the new folder — Cowork discovers it automatically the next time you start a conversation

Up to 20 custom skills, 1 MB per `SKILL.md`.

[→ Full Cowork skills setup walkthrough](../../../ai-workflow-framework/skills/) · [→ How to Add Skills to Your Platform](../../../agentic-building-blocks/skills/#how-to-add-skills-to-your-platform)

---

## You're Done When

- [ ] Microsoft 365 subscription with Copilot enabled
- [ ] Microsoft 365 desktop apps updated to latest version
- [ ] Mobile app installed on at least one device
- [ ] Copilot icon visible in at least one Microsoft 365 app (Word, Excel, Teams, etc.)
- [ ] At least one skill installed via Copilot Cowork (optional, requires Frontier preview)
