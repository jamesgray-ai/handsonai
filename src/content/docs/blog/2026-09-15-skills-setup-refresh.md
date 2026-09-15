---
date: 2026-09-15
authors:
  - jamesgray
tags:
  - Framework
  - Plugins
  - Platform Updates
description: "One plugin install now covers Claude Chat and Cowork, ChatGPT and Codex, and Claude Code; Gemini Spark, Gemini Enterprise, and Copilot Cowork load the skills natively; the setup page is rebuilt for non-technical readers."
title: "Skills setup, rebuilt: one plugin for Claude and ChatGPT, native skills everywhere else"
---

The platforms moved and the setup instructions caught up. Claude now runs plugin skills in Chat, the desktop app, and Cowork from a single install. ChatGPT installs the same plugin from its Plugins page. Gemini Spark, Gemini Enterprise, and Microsoft 365 Copilot Cowork all take the skill files directly — no more pasting instructions into a Project or a Gem. And the [Set Up the Skills](/ai-workflow-framework/skills/) page has been rewritten so someone who has never opened a terminal can be running Analyze in about three minutes.

<!-- more -->

**One plugin, three homes.** On Claude, **Customize → Plugins → Add marketplace** with `jamesgray-ai/handsonai-plugins` gives you all seven framework skills in Claude Chat on the web, the Chat tab in the Claude app, and Cowork — the old "plugin skills are Cowork-only" limitation is gone (the `framework-agent` orchestrator still runs in Cowork). On ChatGPT, **Plugins → Add marketplace** with the same address installs it for Chat, Work, and Codex on any paid plan; the plugin now ships a native Codex manifest, so it lists as **Hands-on AI** with its own description and starter prompts (handsonai plugin v7.1.0). Claude Code is unchanged: two commands.

**Native skills on Gemini and Copilot.** Google added skills to [Gemini Spark](/platforms/google-gemini/skills/) for personal accounts (Google AI Pro or Ultra) and to Gemini Enterprise for work accounts, and [Microsoft 365 Copilot Cowork](/platforms/m365-copilot/skills/) is now generally available with an **Upload skill** button, 50-skill capacity, and companion-file support. All three take the same ZIPs. The Gems and ChatGPT Projects paste-in workarounds are retired.

**A setup page built for everyone.** The [rewritten page](/ai-workflow-framework/skills/) opens with a "Which one are you?" table, defines the four words you'll meet (skill, plugin, marketplace, ZIP), and gives every platform the same shape: a 20-second "before you start" check, click-by-click steps, what success looks like, and what to try if it didn't work. Builders' paths (Claude Code, Cursor, Codex CLI, Gemini CLI, Antigravity) moved to the bottom. Every download is a direct link; each skill also ships as a `-flat.zip` for platforms that want `SKILL.md` at the top of the archive.

**Also:** the skill-discovery prompts ([Find Your Skill Candidates](/agentic-building-blocks/skills/find-skill-candidates/) and [Discover Your Best Skills](/agentic-building-blocks/skills/skills-discovery-meta-prompt/)) are now tool-agnostic and live under the Skills building block rather than the Claude section.

Two sections — Gemini Enterprise and Copilot Cowork — follow the vendors' documentation and are marked as not yet walked through hands-on; if a label on your screen differs, tell us.
