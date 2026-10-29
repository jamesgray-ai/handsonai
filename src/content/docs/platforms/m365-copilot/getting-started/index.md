---
title: Getting Started with M365 Copilot
description: "Set up Microsoft 365 Copilot — confirm your subscription, install the apps, enable Copilot features, and configure the settings you need to start building."
---

Complete setup checklist for Microsoft 365 Copilot. Work through each section in order.

**Time:** ~20 minutes
**Requires:** A Microsoft 365 subscription with Copilot enabled.

---

## 1. Verify Your Subscription

1. Go to Microsoft 365 Copilot at [copilot.cloud.microsoft](https://copilot.cloud.microsoft) and sign in with your work or school account (copilot.microsoft.com is the consumer Copilot for personal accounts, which isn't where Copilot Cowork and Agent Builder run for your organization)
2. Ensure your **Microsoft 365** subscription has **Copilot** enabled
3. If Copilot isn't available, check with your IT admin or see [Microsoft 365 Copilot plans](https://www.microsoft.com/en-us/microsoft-365/copilot)

**Official docs:** [Microsoft Copilot Help](https://support.microsoft.com/en-us/copilot)

---

## 2. Install and Update Apps

Update your Microsoft 365 apps to the latest version to enable Copilot features.

- **Desktop:** Update Word, Excel, PowerPoint, Outlook, and Teams to the latest version
- **Mobile:** [App Store](https://apps.apple.com/app/microsoft-copilot/id6738321700) or [Google Play](https://play.google.com/store/apps/details?id=com.microsoft.copilot)
- **Web:** Access Microsoft 365 Copilot at [copilot.cloud.microsoft](https://copilot.cloud.microsoft) (Copilot Cowork) or [microsoft365.com/chat](https://www.microsoft365.com/chat) (Copilot Chat and Agent Builder)

Sign in to each app with your work or school account.

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

M365 Copilot natively supports Agent Skills through **Copilot Cowork**. After adding the framework skills, say "run the analyze skill" and Analyze starts: first it asks for your working folder (without one, it makes a folder called ai-workspace in your OneDrive).

**Requires:** A Microsoft 365 Copilot license, with Copilot Cowork enabled by your admin (it's generally available; admins turn on its usage-based billing).

**Before you start:** open Microsoft 365 Copilot at [copilot.cloud.microsoft](https://copilot.cloud.microsoft) and look for Copilot Cowork (labelled **Cowork**) in the toggle at the top, next to **Chat**. Not there → ask IT to enable it.

1. Download the skill's `.zip` from the [skill downloads](../../../ai-workflow-framework/skills/#download-the-skill-zips) — don't unzip it
2. In Copilot Cowork, open **Customize → Skills**, click the arrow next to **Add**, then **Upload skill**, and choose the ZIP
3. Start a new conversation — the skill appears under **Your skills** and loads automatically when relevant

Prefer folders? Unzip the skill and drop its folder into OneDrive at `Documents/Cowork/skills/<skill-name>/`. Up to 50 custom skills, 1 MB per `SKILL.md`, 20 companion files and 10 MB per skill (Microsoft Learn, read 2026-10-24).

[→ Full Copilot Cowork skills setup walkthrough](../../../ai-workflow-framework/skills/) · [→ How to Add Skills to Your Platform](../../../agentic-building-blocks/skills/#how-to-install-skills)

---

## You're Done When

- [ ] Microsoft 365 subscription with Copilot enabled
- [ ] Microsoft 365 desktop apps updated to latest version
- [ ] Mobile app installed on at least one device
- [ ] Copilot icon visible in at least one Microsoft 365 app (Word, Excel, Teams, etc.)
- [ ] At least one skill uploaded in Copilot Cowork (optional)
