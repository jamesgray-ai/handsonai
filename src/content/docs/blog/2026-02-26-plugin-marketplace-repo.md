---
date: 2026-02-26
authors:
  - jamesgray
tags:
  - Plugins
description: "The plugin marketplace moved to a dedicated lightweight repo for faster installs in Cowork and other tools."
title: "Plugin Marketplace Moved to Dedicated Repo"
---The Hands-on AI plugin marketplace now lives in its own repository: [`jamesgray-ai/handsonai-plugins`](https://github.com/jamesgray-ai/handsonai-plugins). This fixes timeout issues when adding the marketplace in Cowork and other tools that clone the repo during setup.

<!-- more -->

## Why the change

The main `handsonai` repo includes docs, images, and PDFs — over 100MB of git history. Tools like Cowork have a 120-second timeout for cloning marketplace repos, and the full repo was too large to clone in time. The new repo contains only plugin files (~45 files of plain-text Markdown), so it clones in seconds.

## What changed

**The marketplace add command is now:**

```bash
/plugin marketplace add jamesgray-ai/handsonai-plugins
```

**Install commands stay the same:**

```bash
/plugin install business-first-ai@handsonai
```

The `@handsonai` suffix is unchanged — only the marketplace URL is different.

## Migration for existing users

If you previously added the marketplace with `jamesgray-ai/handsonai`, update it:

```bash
/plugin marketplace remove handsonai
/plugin marketplace add jamesgray-ai/handsonai-plugins
```

Your installed plugins will continue to work. The next `/plugin update --all` will pull from the new repo.
