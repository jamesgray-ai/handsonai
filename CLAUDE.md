# CLAUDE.md

This file provides guidance to Claude Code when working with this repository.

## Repository Overview

Hands-On AI (handsonai.info) — the consolidated site for James Gray's AI courses, setup guides, reference content, and practical AI resources. Built with MkDocs Material and deployed to GitHub Pages.

## Repository Structure

- `docs/platforms/` - Platform-specific content (Claude, OpenAI, Gemini, M365 Copilot)
- `docs/fundamentals/` - Cross-platform concepts, builder setup, patterns
- `docs/courses/` - Structured course content (builders, leaders)
- `docs/questions/` - AEO-optimized Q&A content
- `docs/how-to/` - Problem-focused guides
- `docs/troubleshooting/` - Common issues and solutions
- `docs/overrides/main.html` - FAQPage JSON-LD schema injection for AEO
- `docs/_templates/` - Content templates for contributors
- `.claude/agents/` - Claude Code subagent definitions (local/development copies)
- `.claude/skills/` - Claude Code skill definitions (local/development copies)
- `.claude-plugin/marketplace.json` - Plugin marketplace manifest
- `plugins/` - Distributable plugin bundles (agents + skills grouped by theme)
- `scripts/` - Wrapper scripts for scheduled subagents

## Content Guidelines

- Write for students who may be new to developer tools
- Include screenshots where helpful
- Keep setup guides tool-focused (one tool per doc)
- Link to official documentation rather than duplicating it
- When adding new docs to `docs/`, also update the `nav:` section in `mkdocs.yml`
- Questions pages must include `question` and `short_answer` frontmatter for AEO schema

## Plugin Marketplace

The `plugins/` directory contains distributable Claude Code plugins. Each plugin bundles related agents and skills into a themed toolkit that students can install via `/plugin install`.

### Directory layout

- `.claude-plugin/marketplace.json` — Top-level manifest listing all plugins
- `plugins/<plugin-name>/.claude-plugin/plugin.json` — Per-plugin metadata
- `plugins/<plugin-name>/agents/` — Agent `.md` files
- `plugins/<plugin-name>/skills/` — Skill directories (with `SKILL.md` and optional `references/`)

### Keeping `.claude/` and `plugins/` in sync

The `.claude/` directory is the **development/local** copy (used for repo-local scheduling, `claude --agent`, etc.). The `plugins/` directory is the **distributable** copy. When updating:

1. Always edit `.claude/agents/` or `.claude/skills/` first and test locally
2. Copy the updated file to the corresponding `plugins/<plugin-name>/` location
3. Bump versions (see below)

### Adding a new agent or skill to an existing plugin

1. Create/edit the agent `.md` in `.claude/agents/` (or skill in `.claude/skills/`) — test locally
2. Copy into `plugins/<plugin-name>/agents/` (or `skills/`)
3. Bump `version` in `plugins/<plugin-name>/.claude-plugin/plugin.json` (MINOR for new, PATCH for update)
4. Bump `version` for that plugin in `.claude-plugin/marketplace.json`
5. Update the plugin's section on `docs/plugins/index.md` — add the agent/skill to the table with a link to the detail page anchor
6. Update the plugin's detail page (`docs/plugins/<plugin-name>.md`) — add the agent/skill section following the existing component format
7. Commit and push

### Creating a new plugin

1. Create and test agents/skills locally in `.claude/agents/` and `.claude/skills/`
2. Create the plugin directory structure:
   ```
   plugins/<new-plugin>/
   ├── .claude-plugin/
   │   └── plugin.json
   ├── agents/
   │   └── <agent>.md
   └── skills/          (if applicable)
       └── <skill>/
           └── SKILL.md
   ```
3. Write `plugin.json` with name, description, version, author, keywords
4. Add a new entry to `.claude-plugin/marketplace.json`
5. Add a grid card + collapsible detail section to `docs/plugins/index.md` — include links to the detail page anchors for every agent and skill
6. Create a detail page at `docs/plugins/<plugin-name>.md` following the template used by existing detail pages (see `docs/plugins/course-examples.md` for reference)
7. Add the detail page to the `nav:` section in `mkdocs.yml` under Plugins
8. Commit and push

### Catalog page linking convention

Every agent and skill name in the `docs/plugins/index.md` tables **must** link to the corresponding section on the plugin's detail page:

- **Agents** → link to the detail page anchor: `[`agent-name`](<plugin-name>.md#<agent-name>)`
- **Skills** → link to the detail page anchor: `[`skill-name`](<plugin-name>.md#<skill-name>)`

This directs users to human-readable documentation instead of raw source code. Every time an agent or skill is added to the marketplace, add both the catalog table entry and the detail page section.

### Versioning convention

- **Semantic versioning**: `MAJOR.MINOR.PATCH`
- Adding a new agent/skill to a plugin = bump MINOR (e.g., 1.0.0 → 1.1.0)
- Updating an existing agent/skill = bump PATCH (e.g., 1.1.0 → 1.1.1)
- Breaking changes (renaming, removing, restructuring) = bump MAJOR

## Scheduling Subagents

When setting up scheduled tasks for subagents:
- Use `claude -p "prompt" --dangerously-skip-permissions` to allow headless tool use (required for agents that write files)
- Use the full path to claude binary (e.g., `~/.local/bin/claude`) since launchd/Task Scheduler have minimal PATH
- Always include logging to capture stdout/stderr for troubleshooting
- Store logs in the project's `logs/scheduled/` folder so they're easy to find
- Include timestamps in log filenames for easy debugging

### Windows-specific
- **Always write PowerShell to `.ps1` files** rather than running inline commands - `$` variables get stripped when passing PowerShell through Git Bash
- Create a runner script (e.g., `scripts/run-<agent-name>.ps1`) and a setup script (e.g., `scripts/setup-<agent-name>-schedule.ps1`)
- Use `Register-ScheduledTask` in the setup script to register with Task Scheduler