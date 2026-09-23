# CLAUDE.md

This file provides guidance to Claude Code when working with this repository.

## Repository Overview

Hands-On AI (handsonai.info) — the consolidated site for James Gray's AI courses, setup guides, reference content, and practical AI resources. Built with Astro/Starlight and deployed to Cloudflare Pages.

## Quick Start

```bash
npm install                      # Astro/Starlight + plugins
npm run dev                      # Local dev server at http://localhost:4321
npm run build                    # Production build (CI verification command)
```


For the MCP server (`mcp-server/`):
```bash
cd mcp-server && npm install && wrangler dev
```

## Repository Structure

- `docs/agentic-building-blocks/` - The AI building blocks (Model, Prompt, Context, Project, Memory, Skill, Agent, MCP, API, SDK, CLI)
- `docs/ai-workflow-framework/` - Seven-step methodology (Analyze, Deconstruct, Design, Build, Test, Run, Improve)
- `docs/use-cases/` - Six use case primitives (Content Creation, Research, Coding, Data Analysis, Ideation & Strategy, Automation)
- `docs/product-engineering/` - Product management and software engineering concepts (SDLC, PRDs, user stories, roadmapping, stakeholder management, project tracking)
- `docs/ai-engineering/` - AI engineering concepts (context engineering) — nested under Product & Engineering in nav
- `docs/platforms/` - Platform-specific content (Claude, OpenAI, Gemini, M365 Copilot)
- `docs/use-the-playbook/` - Three consumption modes: Ask (MCP Server), Build (Plugins), Learn (Courses)
- `docs/mcp-server/` - MCP server connection guide (connect from Claude, ChatGPT, Cursor, VS Code, etc.)
- `docs/use-the-playbook/build/` - Plugin marketplace, getting started, plugin detail pages
- `docs/builder-setup/` - Builder Tools Setup guides (terminal, editor, Git, GitHub, voice-to-text, skills, MCP server, AI registry). Git/GitHub is three prerequisite pages in this order — `github-setup.md` (account only; tokens are an optional trailing section), `git-install.md`, `github-cli-setup.md` — each ending in a "Done When" table whose rows must stay byte-identical across the three guides, `builder-setup/index.md`, and `courses/tools-setup-checklist.md` (check: `grep -h "^| \*\*[123]\. " <files> | sort | uniq -c` → 3 each). Platform setup (accounts, personalization, memory, MCP connections) lives in per-platform `getting-started/` pages under `docs/platforms/`
- `docs/patterns/` - Reusable patterns and best practices
- `docs/courses/` - Structured course content (builders, leaders)
- `docs/resources/` - Curated resource pages for external PDFs/reports (with local PDF copies in `docs/assets/pdfs/`)
- `docs/blog/` - Changelog entries (Starlight Blog plugin)
- `docs/feed/` - RSS/Atom feed page
- `src/_templates/` - Content templates for contributors
- `docs/what-people-built.md` - Community showcase of projects built using the playbook
- `docs/CONTRIBUTING.md` - Contributor guidelines
- `.claude/agents/` - Repo-specific subagents not packaged into any plugin (e.g., `playbook-question-*`, `release-notes-generator`, content/editorial agents). Auto-loaded by Claude Code sessions in this repo.
- `.claude/skills/` - Repo-specific skills not packaged into any plugin (e.g., `publishing-playbook-updates`). Auto-loaded by Claude Code sessions in this repo. `editing-hbr-articles` also lives here, but as a **mirror** of the copy in `plugins/multi-agent-example/` — edit the plugin copy, not this one.
- `.claude/hooks/` - Repo hook scripts wired in `.claude/settings.json`, each with a test harness alongside it (`test-*.sh`). Currently `subagent-gate.sh` (`SubagentStop` — validates each pipeline stage's artifacts) and `publish-gate.sh` (`PreToolUse` — blocks the publisher subagent until a human approval marker exists). Both are armed only by the `outputs/articles/.active-run` flag and are otherwise inert. **Hooks load only at session start** — after editing `.claude/settings.json` or a hook script, restart Claude Code or the change silently does not apply. Verify with `/hooks`.
- `.claude/commands/` - Project slash commands. `/hbr-article` (automatic delegation — states the outcome and lets Claude choose the specialists) and `/hbr-article-strict` (deterministic — explicit fixed sequence). The two exist as a deliberate teaching contrast; keep them in sync when the pipeline changes. See the [Autonomous Agent example](src/content/docs/ai-workflow-framework/examples/autonomous-agent.mdx), which is the reference documentation for how that pipeline works.
- `plugins/handsonai/` - **Canonical** source of plugin-packaged agents and skills. Edit here; `scripts/sync-plugins.sh` pushes to the distributable [`jamesgray-ai/handsonai-plugins`](https://github.com/jamesgray-ai/handsonai-plugins) repo (which Claude Chat/Cowork, ChatGPT/Codex, and Claude Code all install from as a marketplace). Each plugin carries `.claude-plugin/plugin.json` and, where Codex can run it, `.codex-plugin/plugin.json`; `sync-plugins.sh` bumps both in lock-step and refuses to run if they disagree.
  - **Framework skill conventions (v8):** inside a skill, the internal sequence is `#### Phase N — Name` (path-specific: `#### Phase N (goal-driven) — Name`); "Step N" always means one of the seven framework steps. Each docs page's "How the Skill Works" list mirrors its skill's phases one-for-one — `scripts/check-framework-consistency.sh` asserts this and the `Skill | Agent` mechanism spelling across the spec template, self-test checklist, Build, and the index page; `sync-plugins.sh` runs it in preflight. Platform-specific facts (install paths, where context lives, agent primitives, scheduling, web search) live only in `registries/platform-registry.json` under each platform's `capabilities` — never in skill prose. The Design Spec is written as a draft with `approved: false` and flipped on approval; Build refuses anything else. Evaluation is binary: Deconstruct writes yes/no criteria (`AC1…`, rules `R1…`, gates `G1…`), Test grades a report card (Met / Not met with evidence), Improve reports which lines flipped.
- `plugins/multi-agent-example/` - **Canonical** source of the multi-agent worked-example plugin (4 agents, 1 skill, 2 hooks, 2 commands, the Word renderer). Separate from `handsonai` on purpose: it ships hooks, and installing a methodology toolkit must never silently change how a user's Claude Code behaves. This pipeline is **mirrored** under `.claude/` and `scripts/` so it runs in this repo without installing anything — run `./scripts/check-plugin-sync.sh` to catch drift between the two copies (`sync-plugins.sh` runs it automatically before syncing this plugin).
- `registry-template/` - **Canonical** payload for the [`jamesgray-ai/ai-registry-template`](https://github.com/jamesgray-ai/ai-registry-template) template repo: the empty registry bundle skeleton, the Node lint/compose tools, test fixtures, and the GitHub Pages Action. Synced by `scripts/sync-registry-template.sh` — edit here, never in the distributed template repo directly. See the Registry Template Sync section below.
- `mcp-server/migrations/` - Cloudflare D1 schema migrations
- `mcp-server/scripts/analytics-query.ts` - CLI for querying MCP analytics via Cloudflare REST API
- `scripts/` - Wrapper scripts for scheduled subagents, plus the multi-agent pipeline's checks and its Word renderer:
  - `check-plugin-sync.sh [plugin]` (drift detection, with a test suite in `test-check-plugin-sync.sh`): no argument or `multi-agent-example` compares the repo mirror against `plugins/multi-agent-example/`; any other plugin name (e.g. `handsonai`) compares `plugins/<name>/` against its distributed copy in the `handsonai-plugins` clone, skipping cleanly if that clone is absent. `sync-plugins.sh` runs it automatically before every sync — for distributed-mode plugins it shows the drift report and requires acknowledgment (interactive, or `SYNC_ACK_DRIFT=1`) rather than hard-failing, because at sync time drift is usually the release payload. Also `check-pipeline-consistency.sh` (asserts that agent, command, gate, and renderer all agree on filenames, chain order, tool privileges, and quality bars — it prints its own count). Run both before demonstrating the pipeline. No fixed count here on purpose: the previous one said 52 when the suite had grown to 64.
  - `article-to-docx.js` (markdown → Word, via the `docx` package), `render-docx.sh` (the wrapper agents call — it preflights the dependency, renders, then verifies the output is a real Word file), and `test-article-to-docx.sh`. Always invoke the wrapper, never the renderer directly: on a fresh install only the wrapper installs `docx`.
- `outputs/` - Local working directory for agent outputs (gitignored)
- `specs/` - Feature specs (`*-prd.md`), implementation plans (`*-plan.md`), and architecture decision records (`decisions/`) (gitignored)
- **Course content is not maintained here.** Instructor guides, self-study articles, assignments, and exercises live in Maven.
- **Course syllabi are not generated here.** The Notion pipeline that built
  `courses/*/syllabus.md` and `courses/*/lessons/` was retired with the Notion course
  databases (2026-07-15); the script and its deploy steps are gone. Course pages link
  to Maven for the syllabus. The source of truth is the OKF knowledge bundle in the
  private `business` repo — if a syllabus is ever published here again, it comes from
  there, not from Notion.

## Multi-Agent Article Pipeline — Conventions

When asked to produce an article through the multi-agent pipeline (the
`ai-productivity-researcher` → `tech-executive-writer` → `hbr-editor` → `hbr-publisher`
agents), apply these defaults without being told. They exist so the goal statement only
has to carry the topic.

1. **Workspace:** `outputs/articles/<kebab-slug-of-topic>/`. Create it, and write the
   goal you were given to `00-goal.md` inside it for provenance.
2. **Arm the gates** before dispatching anything:
   `echo "outputs/articles/<slug>" > outputs/articles/.active-run`
   Both hooks are inert until this exists. **Remove it when the run ends**, including if
   the run is abandoned.
3. **Pass every subagent the absolute workspace path.** Their Workspace Mode only
   activates when given one, and they already know which file to read and write — you do
   not need to restate the filenames.
4. **Never do a specialist's work yourself** — not the research, writing, editing, or
   publishing. Dispatch the agent instead.
5. **A human approves before publishing.** Ask with `AskUserQuestion`, showing the
   significant editorial changes and the file paths. On approval, write the marker
   `<workspace>/APPROVED`. A `PreToolUse` hook blocks `hbr-publisher` until it exists.
6. **Deliverables:** `04-article.md` and `04-article.docx`.

Quality bars live in the agents themselves (evidence floor in the researcher, length
target in the writer) — do not restate them in the dispatch prompt unless overriding.

Full documentation: `src/content/docs/ai-workflow-framework/examples/autonomous-agent.mdx`.
`/hbr-article` runs this with automatic delegation; `/hbr-article-strict` runs it as a
fixed sequence.

## Content Guidelines

- Write for students who may be new to developer tools
- Include screenshots where helpful
- Keep setup guides tool-focused (one tool per doc)
- Link to official documentation rather than duplicating it
- When adding new docs to `src/content/docs/`, also update the sidebar in `astro.config.mjs`
- Questions pages must include `question` and `short_answer` frontmatter for AEO schema
- Blog posts require `date`, `authors`, `tags`, and `description` frontmatter — `description` appears in the homepage What's New section. `tags` is starlight-blog's real schema field; `categories` was a MkDocs leftover that nothing read
- Tags are metadata only right now: starlight-blog's `/blog/tags/[tag]` and `/blog/authors/[author]` routes render nothing here, because the blog is hand-rolled via `BlogList.astro` over the `docs` collection rather than driven by the plugin's routes. Verified 2026-07-25 — the build produces no tag or author pages
- The blog covers both playbook updates and notable releases from Anthropic, OpenAI, and other platforms — keep `/blog/` and RSS scope copy consistent with that
- Markdown gotchas the build won't flag: a `---` divider directly under `</details>` renders as literal dashes — put a blank line between them; and `---## Heading` (heading glued to the frontmatter fence) happens to render but breaks `grep "^## "`, so keep the fence on its own line. Both patterns still exist in older pages
- Redirects live in `astro.config.mjs` → `redirects`. Astro renders each as a 200 + `noindex` HTML stub, so `src/integrations/cloudflare-redirects.mjs` also writes them to `dist/_redirects` at build, which Cloudflare Pages answers with a real 301 (test: `node scripts/test-cloudflare-redirects.mjs`). A redirect whose source path still has a content file **shadows the real page** — the build warns `conflicts with higher priority route`; treat that warning as an error and delete the stale redirect
- Meta descriptions: keep frontmatter `description` between 110 and 160 characters (Ahrefs flags outside that range). Q&A pages need an explicit `description` — `short_answer` is not used as a fallback
- `public/robots.txt` exists only to carry the `Sitemap:` line; Cloudflare prepends its managed Content Signals block at the edge
- `src/content/docs/llms.txt` and `llms-full.txt` are stale leftovers — the served `/llms.txt` is generated at build by `src/integrations/llms-txt.mjs` from questions and use-cases. Don't edit the `src/` copies

## Feature Development Workflow

For non-trivial changes (new pages, structural reorganization, script additions, multi-file updates), follow this workflow. Skip to step 3 for small edits.

### 0. Discover — `/handsonai:writing-vision-briefs`

For fuzzy or early-stage ideas, use the `/handsonai:writing-vision-briefs` slash command to create a Vision Brief before writing a PRD. It:
- Walks you through the problem, users, vision, capabilities, and success criteria in plain language
- Assesses the scope — is this one feature or multiple?
- Breaks bigger visions into **epics** (major themes) and **features** (individual buildable pieces)
- Creates `type:epic` GitHub issues for each epic
- Recommends which feature to build first
- Saves everything to `specs/[name]-vision.md`

If the vision is small enough to be a single feature, the breakdown is skipped.

Record architectural decisions about scope or direction (see [Architecture Decision Records](#architecture-decision-records)).

**Skip this step if** you already know exactly what single feature you want to build. Go straight to Step 1.

### 1. Define — `/handsonai:writing-feature-prds`

Use the `/handsonai:writing-feature-prds` slash command to create a PRD for **one feature**. It will:
- Check if you're coming from a Vision Brief — if so, scope the PRD to your chosen feature
- If starting fresh, gather requirements (and redirect to Step 0 if the idea is too big for one feature)
- Create a PRD at `specs/<feature-name>-prd.md` using the template
- Stress-test the PRD for edge cases and ambiguity
- Create a GitHub issue linking back to the PRD (and referencing the epic issue if applicable)

For early-stage ideas that need exploration, use the `brainstorming` superpowers skill first to validate the approach before writing a PRD.

A spec should include: **Summary**, **Motivation**, **Approach**, **Changes**, **Verification**. See `specs/google-analytics.md` for a format example.

Record scope and design decisions (see [Architecture Decision Records](#architecture-decision-records)).

**Skip specs for:** Bug fixes, trivial changes, urgent hotfixes.

### 2. Plan — plan mode

After the PRD is approved, **enter plan mode** to design the implementation before writing any code. Plan mode explores the codebase, designs the approach, and presents a plan for user approval.

- For complex features, use the `code-explorer` agent (from `feature-dev`) to trace execution paths and map dependencies, then the `code-architect` agent to design the architecture before planning
- The `writing-plans` superpowers skill converts specs into bite-sized tasks with exact file paths, code snippets, and commands
- Plans are saved to `specs/<feature-name>-plan.md` (alongside the PRD)
- **Always save the plan file before starting implementation** — even if the plan was provided inline or from a prior session, persist it to `specs/` first
- For features needing workspace isolation, use `using-git-worktrees` to create a clean worktree before starting

Record implementation approach decisions (see [Architecture Decision Records](#architecture-decision-records)).

For docs changes, a plan typically covers: new/modified files in `src/content/docs/`, `astro.config.mjs` sidebar updates, cross-links to existing pages, and redirects for moved pages.

### 3. Implement — `/feature-dev`

Use the `/feature-dev` slash command, referencing the spec and issue:
```
/feature-dev specs/feature-name-prd.md (issue #123)
```

**Repo-specific implementation:**
- **Content**: Write Markdown in `src/content/docs/`, following Content Guidelines above
- **Nav**: Add new pages to the sidebar in `astro.config.mjs`
- **Scripts**: Add or modify scripts in `scripts/`
- **Plugins**: Follow the Plugin Marketplace checklist below

**Implementation approach:**
- Use the `test-driven-development` superpowers skill: write a failing test first, then write minimal code to pass, then refactor. No production code without a failing test.
- For long implementations, use `executing-plans` to work through the plan in batches with review checkpoints between each batch.
- For plans with independent tasks, use `dispatching-parallel-agents` to implement multiple tasks concurrently.

**Safety net:** The `security-guidance` plugin (Anthropic) runs a hook that automatically warns about potential security issues (command injection, XSS, unsafe patterns) when editing files.

**When things break:**
- Use `systematic-debugging` for any test failure or unexpected behavior — 4-phase structured debugging instead of guessing. Stops after 3 failed fixes to rethink the approach.

### 4. Verify — `verification-before-completion`

Before claiming work is complete, use the `verification-before-completion` superpowers skill. It enforces evidence-based completion — must show actual passing output from:

```
npm run build && node scripts/check-links.js
```

The build catches config errors, template issues, and missing pages; `check-links.js` runs against `dist/` and catches broken `#fragment` anchors (a reworded heading) and docs missing from the sidebar — the same check CI's `link-check` job runs. Use `npm run dev` for visual spot-checking.

No "should work" or "seems correct" — only verified passing output.

### 5. Review — Quality Gate

**Automated code review:**
- Use `requesting-code-review` superpowers skill to dispatch a code review subagent against the implementation
- When receiving PR feedback, use `receiving-code-review` to evaluate feedback technically rather than blindly accepting all suggestions

**Review agents** — run via the Task tool before shipping:

**Always run:**

| Agent | Task tool identifier | Purpose |
|-------|---------------------|---------|
| Code Reviewer | `feature-dev:code-reviewer` | Review for bugs, security vulnerabilities, and logic errors |
| Test Analyzer | `pr-review-toolkit:pr-test-analyzer` | Verify test coverage and identify gaps |
| Code Simplifier | `pr-review-toolkit:code-simplifier` | Simplify code for clarity and maintainability |

**Run if applicable:**

| Agent | Task tool identifier | When to use |
|-------|---------------------|-------------|
| Silent Failure Hunter | `pr-review-toolkit:silent-failure-hunter` | Changes include error handling, catch blocks, or fallbacks |
| Type Design Analyzer | `pr-review-toolkit:type-design-analyzer` | New types or interfaces introduced |
| Comment Analyzer | `pr-review-toolkit:comment-analyzer` | Significant documentation or comments added |

### 6. Ship — `/commit-push-pr`

Use the `/commit-push-pr` slash command to commit, push, and open a PR in one step. The PR should reference the issue number so it auto-closes on merge. CI deploys automatically on merge to `main`.

For structured merge decisions (merge locally vs PR vs keep branch), use the `finishing-a-development-branch` superpowers skill.

CI's `claude-review` job reviews every push to a PR and leaves findings as inline comments — read them with `gh api repos/jamesgray-ai/handsonai/pulls/<n>/comments` (and `issues/<n>/comments` for the summary) before merging.

After shipping, use `/revise-claude-md` to capture any session learnings.

## Issue Types

| Type | Label | Use For |
|------|-------|---------|
| Feature | `type:feature` | New functionality, references spec file |
| Bug | `type:bug` | Unexpected behavior, no spec needed |
| Task | `type:task` | Refactoring, cleanup, no spec needed |
| Epic | `type:epic` | Groups related features |

## Requirements Format

When writing acceptance criteria:
- Use numbered list (not checkboxes)
- Write yes/no verifiable statements
- Focus on *what*, not *how*
- Use active voice ("Error message is displayed" not "User sees error")
- Include concrete expected values when possible

## Architecture Decision Records

When choosing between meaningful alternatives during Steps 0–2, capture the decision as an ADR in `specs/decisions/`. Not every feature needs one — only when there's a real fork in the road (e.g., "JWT vs session auth", "one plugin or two", "flat structure vs nested").

**File naming:** `specs/decisions/NNN-short-title.md` (zero-padded, e.g., `001-plan-files-alongside-prds.md`)

**Template:**

```markdown
# NNN — Title

**Status:** Accepted | Superseded by NNN
**Date:** YYYY-MM-DD
**Step:** Discover | Define | Plan

## Context
What prompted the decision and why it matters.

## Options Considered
1. **Option A** — tradeoffs
2. **Option B** — tradeoffs

## Decision
Which option and why.

## Consequences
What changes as a result — both positive and negative.
```

## Slash Commands

### Core Workflow

| Command | Description |
|---------|-------------|
| `/handsonai:writing-vision-briefs` | Capture a fuzzy idea as a structured Vision Brief |
| `/handsonai:writing-feature-prds` | Create a feature PRD, stress-test it, and open a GitHub issue |
| `/feature-dev` | Guided feature development with codebase understanding |
| `/commit` | Create a git commit |
| `/commit-push-pr` | Commit, push, and open a PR |
| `/revise-claude-md` | Capture session learnings back into CLAUDE.md |

### Review & Quality

| Command | Description |
|---------|-------------|
| `/review-pr` | Comprehensive PR review using specialized agents |
| `/code-review` | Code review a pull request |

### AI Workflow Framework

| Command | Description |
|---------|-------------|
| `/handsonai:analyze` | `analyze` — Step 1 |
| `/handsonai:deconstruct` | `deconstruct` — Step 2 |
| `/handsonai:design` | `design` — Step 3 |
| `/handsonai:build` | `build` — Step 4 |
| `/handsonai:test` | `test` — Step 5 |
| `/handsonai:run` | `run` — Step 6 |
| `/handsonai:improve` | `improve` — Step 7 |

### Superpowers Skills

Skills from the `superpowers` plugin, invoked automatically based on context:

| Skill | When it activates |
|-------|-------------------|
| `brainstorming` | Before creative work — explores intent, proposes approaches, validates design |
| `writing-plans` | After spec approval — converts specs into bite-sized implementation tasks |
| `using-git-worktrees` | Starting feature work that needs workspace isolation |
| `test-driven-development` | During implementation — enforces RED→GREEN→REFACTOR cycle |
| `executing-plans` | Long implementations — works through plan in batches with review checkpoints |
| `dispatching-parallel-agents` | Multiple independent tasks that can be worked concurrently |
| `systematic-debugging` | Any bug or test failure — structured 4-phase debugging |
| `verification-before-completion` | Before claiming done — requires actual passing evidence |
| `requesting-code-review` | After implementation — dispatches automated code review subagent |
| `receiving-code-review` | After PR feedback — enforces technical evaluation of suggestions |
| `finishing-a-development-branch` | After verification — structured merge/PR decision |

### Agents (via Task tool)

See [Step 2 (Plan)](#2-plan-plan-mode) for codebase analysis agents and [Step 5 (Review)](#5-review--quality-gate) for review agents — full tables with identifiers and usage guidance.

## Quick Reference

| Step | Action | Tools |
|------|--------|-------|
| 0. Discover | Capture idea as Vision Brief, break into epics + features | `/handsonai:writing-vision-briefs` (skip if single feature is clear) |
| 1. Define | Create PRD + issue for one feature | `/handsonai:writing-feature-prds` (use `brainstorming` for early ideas) |
| 2. Plan | Enter plan mode, explore codebase, create plan | plan mode + `code-explorer` + `code-architect` agents, `writing-plans` skill |
| 3. Implement | Build with TDD | `/feature-dev` + `test-driven-development` + `security-guidance` hook |
| 4. Verify | Prove it works | `verification-before-completion` |
| 5. Review | Quality gate | `requesting-code-review` + `code-reviewer` + review agents |
| 6. Ship | Commit, push, PR | `/commit-push-pr` + `/revise-claude-md` |

!!! note "Keeping the website template in sync"
    The Feature Development Workflow above is the source of truth for this repo. A generic (repo-agnostic) version lives on the [Agentic Coding plugin page](docs/use-cases/coding/agentic-coding.md) as a copyable template for students. **When you change the workflow structure** (add/remove steps, change which skills or agents are referenced), also update the template on that page. Repo-specific changes (verify commands, implementation details) don't need to be synced — the template uses placeholders for those.

## Plugin Marketplace

The `plugins/` directory contains a staging copy of Claude Code plugins. Each plugin bundles related agents and skills into a themed toolkit that students can install via `/plugin install`.

The **distributable** copy lives in the separate [`jamesgray-ai/handsonai-plugins`](https://github.com/jamesgray-ai/handsonai-plugins) repo — a lightweight repo that Claude, ChatGPT/Codex, and Claude Code can clone quickly. Both catalogs live there, not here: `.claude-plugin/marketplace.json` (Claude) and `.agents/plugins/marketplace.json` (Codex — lists only plugins with a `.codex-plugin/` manifest, so Claude-only plugins like `multi-agent-example` stay hidden from Codex users). `sync-plugins.sh` maintains both.

### Directory layout

- `plugins/<plugin-name>/.claude-plugin/plugin.json` — Per-plugin metadata
- `plugins/<plugin-name>/agents/` — Agent `.md` files
- `plugins/<plugin-name>/skills/` — Skill directories (with `SKILL.md` and optional `references/`)

### Keeping `plugins/` and `handsonai-plugins` in sync

Plugin-packaged content lives in **two** places:

1. **`plugins/handsonai/`** in this repo — canonical source. Edit here, alongside the framework docs the skills implement.
2. **`jamesgray-ai/handsonai-plugins`** — distributable repo that Claude Chat/Cowork (Customize → Plugins → Add marketplace), ChatGPT (Plugins → Add marketplace), Claude Code (`/plugin marketplace add`), and Codex CLI (`codex plugin marketplace add`) all install from. Cloned locally at `~/Code/jamesgray/handsonai-plugins`.

(`handsonai`'s packaged content is **not** duplicated under `.claude/` — local testing is done by installing the plugin from the marketplace, not by symlinking. **`multi-agent-example` is the deliberate exception:** it is mirrored under `.claude/` and `scripts/` so the pipeline runs in this repo without anyone installing anything, which is the whole point of a worked example you can demonstrate live. `check-plugin-sync.sh` is what stops the two copies drifting. Do not generalise that exception to new plugins without the same drift check.)

When updating:

1. Edit the agent or skill in `plugins/handsonai/agents/` or `plugins/handsonai/skills/`.
2. Update the catalog and detail pages in `docs/use-the-playbook/build/` if you added or renamed anything.
3. Run `./scripts/sync-plugins.sh [plugin] patch|minor|major` — this bumps `plugin.json` here, rsyncs to `handsonai-plugins`, updates that plugin's entry in its `marketplace.json` (adding the entry if it's new), and patch-bumps the marketplace's own top-level version. The plugin name defaults to `handsonai` when omitted, so `./scripts/sync-plugins.sh patch` still works. The bump arg is required; semver applies (PATCH = update, MINOR = add new agent/skill, MAJOR = breaking). Before rsyncing it runs `check-plugin-sync.sh` and shows the drift report — usually just the changes you're about to ship — and asks you to confirm (y/N). In a non-interactive context (CI, headless agent) that confirmation is impossible, so the script exits with `Error: unacknowledged drift and no terminal to confirm on.`; re-run with `SYNC_ACK_DRIFT=1` after reviewing the report to proceed.
4. Commit and push **this repo first**.
5. In `~/Code/jamesgray/handsonai-plugins`: rebuild ZIPs if skills changed (`./scripts/build-skill-zips.sh`), create a GitHub Release (`gh release create vX.Y.Z dist/*.zip`), commit and push **last**.

**Critical — push `handsonai-plugins` last:** Claude (Chat and Cowork) detects plugin updates by comparing commit hashes, and Codex caches by `<marketplace>/<plugin>/<version>`. If Cowork syncs to a commit before the version bump lands, it treats that commit as "already synced" and won't re-process it — even though the files contain the new version. By making the `handsonai-plugins` push the final action in the session, Cowork only ever sees the complete, version-bumped state. Never push `handsonai-plugins` mid-session while still making changes. (`sync-plugins.sh` deliberately does not commit or push anywhere — both pushes stay in your hands.)

### Registry Template Sync

`registry-template/` in this repo is **canonical** for the separate
[`jamesgray-ai/ai-registry-template`](https://github.com/jamesgray-ai/ai-registry-template)
repo (a GitHub template repo students click "Use this template" on to get an
empty AI Registry with the Pages Action pre-wired). Edit here, then run
`./scripts/sync-registry-template.sh` to push. Drift between the two is
caught by `./scripts/check-plugin-sync.sh registry-template` (same
drift-detection script the plugin sync uses, pointed at a different pair of
directories).

The `scaffolding-registry` skill's `references/schema-template.md` must stay
**byte-identical** to `registry-template/registry/SCHEMA.md` — two copies of
the same schema, one shipped as plugin content, one shipped as template-repo
content, and they will silently diverge if hand-edited independently. This is
enforced by `scripts/check-registry-consistency.sh`, which `sync-plugins.sh`
runs with `--full` in its preflight for **every** plugin sync, not just
registry changes — meaning schema or skill-doc drift blocks shipping
anything, unrelated agents and skills included. If a sync fails here, fix the
drift (or re-run the sync script) before assuming the unrelated change you
were shipping is broken.

#### Registry release checklist (manual)

Performed at this release, at every MAJOR `handsonai` plugin bump, and before
each course run. Not automatable — see `specs/okf-registry-redesign-prd.md`
Part 8 for the full rationale:

1. **Behavioral run** — scaffold a throwaway registry, run framework steps
   1–2, grep the registry nodes for retired/banned fields (exclude
   `registry/SCHEMA.md`, which lists them on purpose), confirm lint passes clean.
2. **Migration fixtures run** — migrate the `workflow.yaml` and flat-layout
   fixtures; post-check greps + lint pass; `log.md` entries present;
   `process_outcome` content survives into the description.
3. **Tier 2 render check** — AI-generated data island from the fixture bundle
   validates against the schema; dashboard renders from `file://` with no
   console errors.
4. **Action canary (optional — only when the Pages Action or the compose
   script changed)** — on a throwaway instantiation of the template repo,
   push a sample node (Pages updates) and a deliberately broken node (Action
   fails with a legible message). ~5 minutes.
5. **Platform checklist re-verification** — re-verify every row in
   `specs/okf-registry-platform-verification.md` and sign it with
   date/verifier/platform version. This is an internal release gate, not a
   docs gate: the setup page (`builder-setup/ai-registry-setup.md`) is
   written platform-neutrally and carries no per-platform "unverified"
   caveats (decided 2026-09-19 — the registry is not a Claude Code feature
   and students must be able to self-serve on every platform). Unsigned rows
   are work for the instructor before a course run, never a reason to point
   students back to the instructor.
6. **Framework-skill ZIP bundling** — `build-skill-zips.sh` (in
   `handsonai-plugins`) must bundle
   `indexing-registry/references/registry-bundle.md` into every
   framework-skill ZIP. Each framework skill's dispatch blockquote defers to
   that file for the registry contract, but a standalone skill install (a ZIP
   uploaded to Claude, ChatGPT, Gemini, or Copilot) only has what's in its own ZIP — omitting it
   silently breaks standalone installs.

### Updating skill ZIP downloads (GitHub Releases)

Users on platforms without the plugin (Gemini Spark/Enterprise, M365 Copilot Cowork, Cursor, Gemini CLI — and Claude or ChatGPT users whose plan or org blocks plugins) download pre-built skill ZIPs from GitHub Releases on `handsonai-plugins`. Each skill is published in two layouts: `<skill>.zip` (skill folder at the root — what claude.ai requires) and `<skill>-flat.zip` (`SKILL.md` at the root — what Gemini Enterprise documents). `scripts/test-build-skill-zips.sh` in that repo asserts both layouts carry identical content. When skills are updated, rebuild and publish a new release:

1. From the `handsonai-plugins` repo, run `./scripts/build-skill-zips.sh` — this creates ZIPs in `dist/`
2. Create a new release: `gh release create vX.Y.Z dist/*.zip --title "vX.Y.Z" --notes "Description of changes"`

The skills page (`docs/ai-workflow-framework/skills.mdx`) uses `/releases/latest/download/` URLs, so they always point to the most recent release automatically.

### Adding a new agent or skill to an existing plugin

1. Create the agent `.md` in `plugins/<plugin-name>/agents/` or the skill in `plugins/<plugin-name>/skills/<skill-name>/SKILL.md`.
2. Update the plugin's section on `docs/use-the-playbook/build/index.md` — add the agent/skill to the table with a link to the detail page anchor.
3. Update the plugin's detail page (`docs/use-the-playbook/build/<plugin-name>.md`) — add the agent/skill section following the existing component format.
4. Run `./scripts/sync-plugins.sh minor` (MINOR for new content).
5. Commit and push this repo.
6. In `~/Code/jamesgray/handsonai-plugins`: rebuild skill ZIPs if you added a skill, create a GitHub Release, commit and push **last**.

### Creating a new plugin

1. Create the plugin directory structure directly under `plugins/`:
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
2. Write `plugin.json` with name, description, version (start at `1.0.0`), author, keywords.
3. Add a grid card + collapsible detail section to `docs/use-the-playbook/build/index.md` — include links to the detail page anchors for every agent and skill.
4. Create a detail page at `docs/use-the-playbook/build/<plugin-name>.md` following the template used by existing detail pages (see `docs/use-the-playbook/build/handsonai.mdx` for reference).
5. Add the detail page to the sidebar in `astro.config.mjs` under "Tools & Resources > Agents & Skills".
6. Run `./scripts/sync-plugins.sh <plugin-name> minor` — it adds the plugin's `marketplace.json` entry if it is not there yet, so no hand-editing is needed. (It also refuses to proceed if `plugin.json` has no valid semver version or no description, rather than publishing `null` into the marketplace.)
7. Commit and push this repo first, then build ZIPs, create a Release, and push `handsonai-plugins` **last**.

To locally test a plugin during development, install it from the marketplace (`/plugin marketplace add ~/Code/jamesgray/handsonai-plugins` then `/plugin install <name>@handsonai`).

### Catalog page linking convention

Every agent and skill name in the `docs/use-the-playbook/build/index.md` tables **must** link to the corresponding section on the plugin's detail page:

- **Agents** → link to the detail page anchor: `[`agent-name`](<plugin-name>.md#<agent-name>)`
- **Skills** → link to the detail page anchor: `[`skill-name`](<plugin-name>.md#<skill-name>)`

This directs users to human-readable documentation instead of raw source code. Every time an agent or skill is added to the marketplace, add both the catalog table entry and the detail page section.

### Versioning convention

- **Semantic versioning**: `MAJOR.MINOR.PATCH`
- Adding a new agent/skill to a plugin = bump MINOR (e.g., 1.0.0 → 1.1.0)
- Updating an existing agent/skill = bump PATCH (e.g., 1.1.0 → 1.1.1)
- Adding a new install surface or manifest (e.g. the Codex `.codex-plugin/` manifest) = bump MINOR — new capability for users, even if no skill changed
- Breaking changes (renaming, removing, restructuring) = bump MAJOR

## Adding a PDF Resource

The `docs/resources/` section hosts curated resource pages for external PDFs and reports. Each PDF gets a markdown page (for MCP search indexing) and a local copy (to prevent link rot).

### Adding a new resource

1. Download the PDF to `docs/assets/pdfs/<descriptive-filename>.pdf`
2. Create a resource page at `docs/resources/<slug>.md` with frontmatter (`title`, `description`), source attribution, "Why This Matters" section, "Key Takeaways" bullets, "How the Playbook Uses This" cross-links, and a download button linking to `../assets/pdfs/<filename>.pdf`
3. Add the page to `docs/resources/index.md` catalog table
4. Add the page to the sidebar in `astro.config.mjs` under "Tools & Resources > Resources"
5. Update any existing pages that linked to the external PDF URL to point to the new resource page instead

The MCP server indexes resource pages automatically — no changes to `build-index.ts` or `tools.ts` needed (the `resources` section mapping is already configured).

## MCP Server Analytics

The MCP server (`mcp-server/`) logs tool calls and resource reads to a Cloudflare D1 database (`handsonai-mcp-analytics`) for content gap analysis. Analytics is non-blocking — failures never affect MCP responses.

### Key files

- `mcp-server/src/analytics.ts` — `logEvent()`, `sanitizeParams()`, `getResultSize()` functions
- `mcp-server/src/index.ts` — `ctx.waitUntil()` instrumentation in the fetch handler
- `mcp-server/src/dashboard.ts` — Analytics dashboard: auth, 11 API endpoints, HTML UI with Chart.js
- `mcp-server/migrations/` — D1 schema migrations (applied via `wrangler d1 migrations apply`)
- `mcp-server/scripts/analytics-query.ts` — CLI for querying analytics (`npm run analytics <command>`)
- `mcp-server/.env.example` — Required env vars for the CLI script
- `docs/mcp-server/index.md` — MCP server page with privacy disclosure ("Analytics & Privacy" section)

### What's logged

Tool name, sanitized params (query/path only, max 200 chars), result size, error status, duration, User-Agent, and country. Only `tools/call` and `resources/read` methods — protocol handshakes (`initialize`, `ping`, `tools/list`) are excluded. No PII is collected.

### CLI commands

Run from `mcp-server/`: `npm run analytics <command> [--days=N]`

Commands: `top-queries`, `tool-usage`, `daily-volume`, `top-pages`, `errors`, `zero-results`, `clients`, `raw-sql` (SELECT only).

### Adding a new migration

1. Create `mcp-server/migrations/NNNN_description.sql`
2. Apply locally: `wrangler d1 migrations apply handsonai-mcp-analytics --local`
3. Test with `wrangler dev`
4. Apply to production: `wrangler d1 migrations apply handsonai-mcp-analytics --remote`

### Deployment

Merging to `main` deploys the MCP server automatically — `deploy.yml` rebuilds `content-index.json` (gitignored; `npm run build:index` regenerates it locally) and runs `wrangler deploy`. Run `wrangler deploy` from `mcp-server/` by hand only to ship a hotfix outside that flow. The D1 database ID is in `wrangler.toml` (not a secret).

`SETUP_TOOLS` in `mcp-server/src/tools.ts` maps `get_setup_guide` keys to `builder-setup/` page paths and generates the tool's enum and description — update it whenever a builder-setup page is added, renamed, or removed, or the tool silently returns "not found".

### Analytics Dashboard

Live at `mcp.handsonai.info/dashboard` (custom domain configured in `wrangler.toml`). Admin-only, cookie-based auth via `ANALYTICS_TOKEN` Worker secret. Visit `/dashboard?token=<token>` once to set cookie, then bookmark `/dashboard`.

For local dev: create `mcp-server/.dev.vars` with `ANALYTICS_TOKEN=<test-value>`, then `wrangler dev`. The `.dev.vars` file is gitignored by Wrangler defaults.

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