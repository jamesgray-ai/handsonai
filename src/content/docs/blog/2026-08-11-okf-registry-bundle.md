---
date: 2026-08-11
authors:
  - jamesgray
tags:
  - Framework
  - Plugins
  - Announcements
description: "Your AI Registry is now a knowledge bundle: a guided 30-minute setup interview, a visual dashboard that publishes itself, and a starter template repo."
title: "Your AI Registry is now a knowledge bundle"
---

The AI Workflow Framework's registry got its biggest upgrade yet (handsonai plugin v7.0.0). Your registry is no longer a single generated index file — it's a structured knowledge bundle your AI assistant reads, writes, and maintains: one file per business, process, and workflow, all linked, all in plain Markdown you own.

<!-- more -->

**Set it up in one conversation.** The new `scaffolding-registry` skill builds your registry as a guided interview — about 30 minutes from "set up my AI registry" to a complete picture of your business: your lines of business, the processes where AI can help most, and your first workflow, ready to take through the framework. Start from the [AI Registry template repo](https://github.com/jamesgray-ai/ai-registry-template) or let the skill scaffold any workspace. Full guide: [AI Registry Setup](/builder-setup/ai-registry-setup/).

**A dashboard that keeps itself current.** Every maintenance pass regenerates `REGISTRY.md` (your at-a-glance inventory) and a visual dashboard — your business's value chain, workflow status, and per-workflow drill-ins — as a single HTML file that opens in any browser. If your registry lives in a GitHub repo created from the template, a built-in automation republishes the dashboard to a live web page on every change. You never run any of it by hand.

**Works where you work.** The registry is plain Markdown, so the same bundle works across Claude Code, Cowork, the ChatGPT desktop app, and upload-based setups — the [setup guide](/builder-setup/ai-registry-setup/) has a complete path for each platform.

**Already using the framework?** Nothing to redo by hand: the next time a framework skill touches an older workspace, it offers to migrate your existing workflows into the bundle automatically.

Update the plugin (`/plugin install handsonai@handsonai`, or "Check for updates" in Cowork) to get the new skills — all fourteen are also available as [downloads](/use-the-playbook/build/handsonai/) for claude.ai and ChatGPT.
