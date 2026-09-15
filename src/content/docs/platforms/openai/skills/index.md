---
title: Skills on OpenAI
description: How Agent Skills work in ChatGPT and Codex — install a plugin, upload a skill, or drop a folder on disk
---

ChatGPT and Codex support Agent Skills natively, using the same open `SKILL.md` format as Claude and other platforms. Since July 2026 the ChatGPT app (Mac, Windows, Linux) has three modes — **Chat**, **Work**, and **Codex** — and ChatGPT and Codex share one plugin directory, so a plugin installed once works in all of them.

**Before you start:** in ChatGPT, click **Plugins** in the left sidebar. If you see **Add marketplace**, you can install plugins (Pro, Business, Enterprise). If you see a **Skills** tab with a **Create** button, you can upload skills (any paid plan except Free and Go; on Enterprise and Edu an admin turns Skills on). On Free or Go, use the Codex folder path below.

## Install a plugin (Pro, Business, Enterprise)

**Plugins → Add marketplace**, paste the marketplace address (for the Hands-on AI plugin: `jamesgray-ai/handsonai-plugins`), then **Install** the plugin. Plugin skills work in Chat and Work on the web, desktop, and mobile, and in Codex. In **Work**, type `@` and the skill name to use one; in Codex, type `$` and the name.

Business, Enterprise, and Edu admins can add a marketplace for the whole workspace: **Admin → Plugins → Add → Import marketplace** (it syncs daily).

→ [Plugins](https://learn.chatgpt.com/docs/plugins) (official OpenAI docs)

## Upload a skill (paid plans)

**Plugins → Skills → Create → Upload from your computer**, then choose the skill's `.zip` (don't unzip it). Uploaded skills are available in the ChatGPT app and in Codex.

→ [Skills in ChatGPT](https://help.openai.com/en/articles/20001066-skills-in-chatgpt) (official OpenAI docs)

## Codex — folders on disk (every plan, including Free)

Codex reads skill folders from disk, in this order: `.agents/skills/` in your current folder and up to the repository root, then `~/.agents/skills/` in your home folder (the usual place — it works in every project), then `/etc/codex/skills`. Unzip the skill and move its folder there; then type `$` in Codex to pick it, or `/skills` to list what's loaded. This works in the Codex CLI, the Codex tab in the ChatGPT app, and the IDE extension.

From the CLI, the plugin also installs with `codex plugin marketplace add jamesgray-ai/handsonai-plugins` then `codex plugin add handsonai@handsonai`.

→ [Build skills — Codex](https://learn.chatgpt.com/docs/build-skills) (official OpenAI docs)

## Related

- [Skills building block](/agentic-building-blocks/skills/) — what skills are and how they work across platforms
- [AI Workflow Framework skills setup](/ai-workflow-framework/skills/) — step-by-step setup for the seven framework skills on ChatGPT and Codex
