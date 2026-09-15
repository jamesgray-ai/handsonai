# Plugins

This directory is the **canonical source** of the [Hands-on AI](https://handsonai.info) plugins. Edit here; `scripts/sync-plugins.sh` pushes to the distributable [`jamesgray-ai/handsonai-plugins`](https://github.com/jamesgray-ai/handsonai-plugins) repo, which Claude, ChatGPT/Codex, and Claude Code install from.

Each plugin carries two manifests — `.claude-plugin/plugin.json` (Claude) and, where Codex can run it, `.codex-plugin/plugin.json` (ChatGPT/Codex). `sync-plugins.sh` keeps their versions in lock-step; never hand-edit one without the other.

## Available Plugin

| Plugin | Description |
|--------|-------------|
| [handsonai](./handsonai/) | Everything you need to design, build, and document AI workflows — the AI Workflow Framework, AI registry, and feature-spec toolkit in one plugin |

## Install

The same plugin installs on Claude, ChatGPT/Codex, and Claude Code. Step-by-step
instructions with screenshots, plus ZIP downloads for every other platform, are on the
[skills setup page](https://handsonai.info/ai-workflow-framework/skills/).

**Claude (claude.ai web, Claude Desktop, Cowork)** — paid plans:
**Customize → Plugins → + → Add marketplace → Add from a repository** → `jamesgray-ai/handsonai-plugins` → install **handsonai**.
The skills then work in Chat and Cowork; the `framework-agent` orchestrator runs in Cowork.

**ChatGPT (any paid plan) and Codex:**
**Plugins → Add marketplace** → `jamesgray-ai/handsonai-plugins` → install **Hands-on AI**.
Type `@analyze` in ChatGPT or `$analyze` in Codex. From the Codex CLI instead:

```
codex plugin marketplace add jamesgray-ai/handsonai-plugins
codex plugin add handsonai@handsonai
```

**Claude Code (terminal or the Desktop app's Code tab):**

```
/plugin marketplace add jamesgray-ai/handsonai-plugins
/plugin install handsonai@handsonai
```

**Everything else (Claude Free, ChatGPT Free/Go, Gemini Spark / Gemini Enterprise, M365 Copilot Cowork, Cursor, Gemini CLI):**
download the skill ZIPs from the [Releases page](https://github.com/jamesgray-ai/handsonai-plugins/releases/latest).
Each skill ships in two layouts — `<skill>.zip` (skill folder at the root, for claude.ai)
and `<skill>-flat.zip` (`SKILL.md` at the root, for platforms that ask for that).

For full documentation, visit [the Hands-on AI plugin page](https://handsonai.info/use-the-playbook/build/handsonai/).

For example agents, skills, and prompts you can adapt for your own workflows, see the [Example Gallery](https://handsonai.info/use-cases/example-gallery/).
