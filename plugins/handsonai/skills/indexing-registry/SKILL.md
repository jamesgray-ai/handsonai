---
name: indexing-registry
description: >
  This skill should be used when the user wants to generate or refresh their AI Registry —
  the REGISTRY.md index of skills, agents, workflows, business processes, and apps at the
  workspace root. Triggers when the user asks to "update my registry", "regenerate the index",
  "what have I built", "show my AI inventory", after creating skills or agents, or when another
  framework skill's closing step calls for a registry refresh. Also use to repair a stale or
  hand-edited REGISTRY.md, or to migrate from a Notion-based registry.
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

> **Terminology:** "AI Registry" always means `REGISTRY.md` and the files it indexes. It is unrelated to the framework's *platform registry* (`registries/platform-registry.json`), which catalogs platforms and integrations for the Design and Build skills.

## Location & Scope

**One workspace = one registry.** `REGISTRY.md` lives at the root of the folder the framework operates in — beside `outputs/`, `sops/`, and `process-guides/`:

- **Claude Code** → repository root.
- **Cowork** → project folder root (the writable scope). Each Cowork project gets its own registry; users who want one unified view should keep a single "AI workspace" folder for all their workflows.
- **claude.ai (no persistent workspace)** → generate the file as a download and tell the user to keep it in their Project knowledge and re-upload it alongside `workflow.yaml` when continuing work.

**Out-of-workspace assets:** personal skills (`~/.claude/skills/`) and plugin- or Cowork-installed skills/agents may not be readable as files. List them from session context instead (the names and descriptions of available skills and agents are visible to the model) in an "Installed (user/plugin)" subsection with Location `installed`. File scanning stays workspace-local. Ask the user before including personal `~/.claude/skills/` entries — the registry is workspace-scoped by default.

## Regeneration Procedure

Other framework skills reference this procedure from their closing steps ("refresh REGISTRY.md"). Run it the same way whether invoked standalone or as a closing step. **Best-effort rule:** if the environment can't write to the workspace root, say so and continue — a failed refresh must never fail the step that requested it.

### Step 1: Scan sources

Scan **within the workspace only**, in this order:

1. **Skills** — glob `**/skills/*/SKILL.md` (covers `.claude/skills/` and any plugin-style layout in the workspace). Read frontmatter `name`, `description`, optional `quick_start_prompt`.
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

### Installed (user/plugin)

| Skill | Description | Location |
|---|---|---|
| [name] | [description] | installed |

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

For users who keep the Notion AI Registry template (and have the Notion MCP connected), offer to mirror after regenerating — never as a required step:

1. For each workflow: search the Notion Workflows database for the exact `display_name`. Update the matching page's properties (Description, Status, Type, Trigger, Apps) or create a new page if none matches exactly. Record the page URL in the manifest's `notion_url`.
2. For each skill/agent: same exact-title search against the AI Building Blocks database; update Description and Quick Start Prompt, or create with Asset Type and Platform "Claude".
3. Never create without first checking for duplicates; partial title matches are not duplicates.
4. Confirm with the user after modifying Notion, and remind them the Markdown files remain the source of truth — the mirror is one-way.

**Migrating *from* Notion:** to move an existing Notion registry into Markdown, work the other direction — read the Notion databases, merge their fields into the corresponding `workflow.yaml` manifests / asset frontmatter (mapping select values to kebab-case: "Under Development" → `under-development`), create stub process guides for processes without one, then regenerate. Flag Notion rows with no matching local file for the user to resolve.
