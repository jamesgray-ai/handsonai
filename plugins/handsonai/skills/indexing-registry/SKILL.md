---
name: indexing-registry
description: >
  This skill should be used when the user wants to generate or refresh their AI Registry —
  the REGISTRY.md index of skills, agents, workflows, business processes, and apps at the
  workspace root. Triggers when the user asks to "update my registry", "regenerate the index",
  "what have I built", "show my AI inventory", after creating skills or agents, or when another
  framework skill's closing step calls for a registry refresh. Also handles the optional Notion
  mirror: "register this skill/agent/workflow/process in Notion", "add this to my Notion
  registry", "update this workflow in Notion", "mirror my registry to Notion", "what's in my
  Notion registry". Also use to repair a stale or hand-edited REGISTRY.md, or to migrate from
  a Notion-based registry.
user-invocable: true
---

# Indexing the AI Registry

The **AI Registry** is a single generated file — `REGISTRY.md` at the workspace root — that gives an at-a-glance view of everything the user has built: skills, agents, workflows, business processes, and the apps they connect to.

**The registry is derived state, never maintained state.** The source of truth is always the underlying files:

| Registry section | Source of truth |
|---|---|
| Skills | `SKILL.md` frontmatter (`name`, `description`, optional `quick_start_prompt`) |
| Agents | agent `.md` frontmatter or filename + opening paragraph |
| Workflows | `outputs/*/workflow.yaml` manifests (see `references/manifest-schema.md`) |
| Business Processes | `process-guides/*.md` frontmatter + `business_process` values in manifests |
| Apps | union of `apps:` lists across manifests |

To change what the registry shows, edit the source file and regenerate. Never edit `REGISTRY.md` by hand.

> **Manifest resolution:** if the workspace has `registry/SCHEMA.md`, the manifest is the Workflow concept node — see `references/manifest-resolution.md` and follow its bundle backend for all manifest reads/writes in this skill; otherwise use `workflow.yaml` as described below.

> **Terminology:** "AI Registry" always means `REGISTRY.md` and the files it indexes. It is unrelated to the framework's *platform registry* (`registries/platform-registry.json`), which catalogs platforms and integrations for the Design and Build skills.

## Location & Scope

**One workspace = one registry.** `REGISTRY.md` lives at the root of the folder the framework operates in — beside `outputs/`, `sops/`, and `process-guides/`:

- **Claude Code** → repository root.
- **Cowork** → project folder root (the writable scope). Each Cowork project gets its own registry; users who want one unified view should keep a single "AI workspace" folder for all their workflows.
- **claude.ai (no persistent workspace)** → generate the file as a download and tell the user to keep it in their Project knowledge and re-upload it alongside `workflow.yaml` when continuing work.

**The registry inventories what the user built — not the tooling they installed.** Plugin-installed skills and agents (the AI Workflow Framework skills themselves, marketplace plugins, platform-provided agents) are **excluded by default**: listing framework tooling in a student's registry is noise, not inventory. What belongs in the Skills and Agents tables:

- Skill/agent **files in the workspace** (including artifacts the Build step generated into the project)
- Personal `~/.claude/skills/` entries only if the user asks to include them

If the user explicitly asks to see installed tooling ("include my installed skills"), add an "Installed (user/plugin)" subsection listing them from session context with Location `installed` — otherwise omit that section entirely. File scanning stays workspace-local.

## Regeneration Procedure

Other framework skills reference this procedure from their closing steps ("refresh REGISTRY.md"). Run it the same way whether invoked standalone or as a closing step. **Best-effort rule:** if the environment can't write to the workspace root, say so and continue — a failed refresh must never fail the step that requested it.

**Workspace-owned generator takes precedence:** if the workspace contains `tools/compose-registry.js`, run `node tools/lint-registry.js && node tools/compose-registry.js` instead of assembling `REGISTRY.md` by hand — the workspace's own generator is authoritative.

### Step 1: Scan sources

Scan **within the workspace only**, in this order:

1. **Skills** — glob `**/skills/*/SKILL.md` (covers `.claude/skills/` and any plugin-style layout in the workspace, including skills the Build step generated into the project). Read frontmatter `name`, `description`, optional `quick_start_prompt`. Exclude plugin cache/install directories if any fall inside the workspace.
2. **Agents** — glob `.claude/agents/*.md` and `agents/*.md`. Name from frontmatter `name` or filename; description from frontmatter `description` or the opening paragraph.
3. **Prompts** (optional section) — glob `prompts/*.md` if the directory exists. Name from frontmatter or filename; description from frontmatter or first line.
4. **Context files** (optional section) — `CLAUDE.md` at the workspace root (and notable nested ones). Describe from the first heading or summary line.
5. **Workflows** — every `outputs/*/workflow.yaml`. Read all fields (schema in `references/manifest-schema.md`). Also:
   - **Legacy flat layout** (`outputs/<name>-requirements.md` with no folder/manifest): list the workflow with an em-dash in metadata columns and the note *"legacy — run deconstruct to migrate"*.
   - **Standalone SOPs** (`sops/*.md` whose `workflow:` frontmatter matches no manifest, or with no `workflow:` key): list them in the Workflows table using SOP frontmatter (`title`, `execution_mode`, `autonomy_level`, `owner`) for whatever columns they can fill.
6. **Process guides** — `process-guides/*.md` frontmatter (`title`, `domain`, `owner`, optional `workflows`).

**Tolerance rules:** every field is optional — a missing value renders as `—`, never an error. Accept `Outcome-Driven` as `Goal-Driven`. Accept Title Case or kebab-case enum values (`In Production` = `in-production`).

### Step 2: Build the file

Use this template. Order every table **alphabetically by name** so regeneration produces clean diffs. Omit the Prompts & Context Files section entirely when there is nothing to list.

```markdown
<!-- GENERATED by the indexing-registry skill — do not edit by hand.
     Edit the source files (SKILL.md frontmatter, workflow.yaml,
     SOP/process-guide frontmatter) and regenerate. -->

# AI Registry

Your inventory of AI assets and workflows. Sources of truth are the files themselves — this index is generated.

## Skills

| Skill | Description | Location | Quick Start Prompt |
|---|---|---|---|
| [name] | [description, first sentence] | [path] | [prompt or —] |

<!-- "Installed (user/plugin)" subsection: only when the user explicitly asks
     to include installed tooling — omit by default. -->

## Agents

| Agent | Description | Location | Quick Start Prompt |
|---|---|---|---|
| [name] | [description, first sentence] | [path] | [prompt or —] |

## Workflows

| Workflow | Business Process | Owner | Status | Health | Last Run |
|---|---|---|---|---|---|
| [display_name] | [business_process] | [owner] | [status] | [health] | [last_run] |

### Workflow details

| Workflow | Type | Autonomy | Platform | Trigger | Apps | Step | SOP | Requirements | Design Spec |
|---|---|---|---|---|---|---|---|---|---|
| [display_name] | [type] | [autonomy] | [platform] | [trigger] | [apps, comma-joined] | [current_step]/7 | [link or —] | [link or —] | [link or —] |

## Business Processes

| Process | Domain | Workflows | Guide |
|---|---|---|---|
| [title] | [domain] | [workflow names in this process, comma-joined] | [link or "no guide yet"] |

## Apps

| App | Used by |
|---|---|
| [app name] | [workflow names, comma-joined] |

## Prompts & Context Files

| Name | Type | Description | Location |
|---|---|---|---|
| [name] | Prompt / Context | [description] | [path] |

---
*Generated: YYYY-MM-DD · [N] skills · [N] agents · [N] workflows · [N] processes · [N] apps*
```

Links use relative paths from the workspace root (e.g., `[SOP](sops/lead-qualification-sop.md)`).

The two Workflows tables split the columns deliberately: the first is the operational dashboard (who owns it, is it healthy, when did it last run), the second holds configuration detail. Keep both even for a single workflow.

### Step 3: Report

After writing, summarize what changed: counts per section, plus:

- **Collisions** — two assets with the same name in different locations: list both paths and ask the user which is canonical (don't guess).
- **Orphans** — a manifest whose `business_process` has no process guide ("no guide yet" — suggest `writing-process-guides`); an SOP with no manifest; an `assets_used` entry matching no scanned skill/agent.
- **Legacy layouts** found (suggest running `deconstruct` to migrate).

## Quick Start Prompts

A Quick Start Prompt is a single copy-paste-ready prompt demonstrating the asset's primary use case. When an asset has no `quick_start_prompt` frontmatter field, generate one and **offer to write it back into the asset's frontmatter** (with the user's confirmation — this is the only write this skill makes outside `REGISTRY.md`). Until it's written back, show the generated prompt in the table but note it's unsaved.

**Guidelines:**
- One sentence that triggers the asset's main workflow
- Specific enough to be immediately useful
- Generic enough to work across different contexts
- Should produce a complete result, not just start a conversation

**Examples:**

| Type | Name | Quick Start Prompt |
|------|------|--------------------|
| Skill | reviewing-student-goals | "Review student learning goals from my course platform, update each student's record in Notion, and give me a cohort theme analysis." |
| Skill | writing-linkedin-posts | "Write a LinkedIn post about [topic] using my brand voice." |
| Agent | playbook-question-answerer | "Answer the question 'What are the six AI building blocks?' using the Hands-on AI site content." |
| Agent | hbr-editor | "Review this article for HBR publication quality and give me prescriptive feedback." |
| Prompt | meeting-prep-quick | "Prepare me for my meeting with [name] at [company] tomorrow." |

Context files typically don't need a Quick Start Prompt — use `—`. If unsure, ask the user rather than guessing.

## Optional: Mirror to Notion

For users who work across multiple machines and tools, the Notion AI Registry template is a supported **visualization mirror** — database views of the same registry, with grouped views by process and clickable workflow↔asset relations. It is never required and never the source of truth: the mirror is one-way (Markdown → Notion).

The mirror targets **four core databases**: Workflows, Processes, Skills, and Agents. The full procedure, field mapping, link derivation, and sync rules live in `references/notion-mirror.md` — follow it exactly.

- After regenerating the registry, **offer** to mirror if the Notion MCP is connected — first-time mirroring always requires the user's confirmation.
- A **single asset** can be registered or updated without a full mirror ("register this skill in Notion") — see the Targeted registration section of the reference.
- Once a workflow's manifest has a `notion_url`, that is a standing opt-in: framework skills auto-sync that workflow's Notion row in their closing steps (best-effort, never blocking).
- After any mirror, confirm what changed and remind the user the Markdown files remain the source of truth.
- A workspace whose manifests carry no `notion_url` fields at all has the mirror **off** — don't offer per-workflow auto-sync there unless the user asks to set the mirror up.

**Migrating *from* Notion:** to move an existing Notion registry into Markdown, follow the migration procedure in `references/notion-mirror.md` — read the core databases, merge fields into manifests and frontmatter, create stub process guides, then regenerate.
