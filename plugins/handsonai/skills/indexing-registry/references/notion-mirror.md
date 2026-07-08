# Notion Mirror (Optional)

For users who work across multiple machines and tools, the [Notion AI Registry template](https://jamesgray007.notion.site/AI-Operations-Registry-Template-2f3edcfdb924813f86f3eacca6b836bb) provides a visual database view of the registry — grouped views by process, status dashboards, and clickable relations between workflows and their assets. The mirror is **one-way** (Markdown → Notion) and **never required**: the Markdown files remain the source of truth, and nothing in the framework depends on Notion.

Requires the Notion connector/MCP. If Notion is not connected, skip everything in this file silently.

## Supported databases

The template contains **exactly the four core databases**, and the mirror targets only these:

| Database | Mirrors from |
|---|---|
| **Workflows** | `outputs/*/workflow.yaml` manifests |
| **Processes** | `process-guides/*.md` frontmatter + `business_process` values in manifests |
| **Skills** | `SKILL.md` frontmatter (workspace skills) |
| **Agents** | agent `.md` frontmatter (workspace agents) |

Older template duplicates may contain additional databases (Business, Lines of Business, Offerings, Prompts, Context, AI Projects, MCP Servers, Apps, or the deprecated Building Blocks). **Do not mirror to these and do not touch them** — leave any existing rows alone. Never delete or archive anything in the user's Notion workspace.

## Database discovery — zero configuration

No database IDs are ever hardcoded. Locate the user's databases at runtime: search Notion for databases titled "Workflows", "Processes", "Skills", and "Agents", preferring ones under a page titled "AI Registry" or duplicated from the template. If a database can't be found, or multiple candidates match, ask the user to paste a link to the right one rather than guessing — then use that resolved URL for the rest of the session. The user never edits this skill; their entire setup is: duplicate the template, connect the Notion connector.

## Field mapping

Mirror **links and summaries, not content**. Enum values map from kebab-case to Title Case (`under-development` → "Under Development", `augmented` → "Augmented", `guided` → "Guided", and so on).

### `workflow.yaml` → Workflows database

| Manifest field | Notion property |
|---|---|
| `display_name` | Name (title) |
| `description` | Description |
| `status` | Status |
| `type` | Execution Mode |
| `autonomy` | Autonomy Level |
| `trigger` | Trigger |
| `sequence` | Sequence |
| `apps` | Apps property (multi-select; comma-joined text if the user's copy has a text property instead) |
| `artifacts.sop` | SOP (link — see link derivation) |
| `business_process` | Business Process relation — find the process page by exact title; create it if missing |
| `assets_used` | Skills / Agents relations — match each name against the Skills and Agents databases |

### `SKILL.md` frontmatter → Skills database

| Source | Notion property |
|---|---|
| `name` | Name (title) |
| `description` | Description (first 1–2 sentences) |
| file URL (see link derivation) | GitHub |
| `quick_start_prompt` | Quick Start Prompt |
| manifests listing this skill in `assets_used` | Workflows relation |

### Agent frontmatter → Agents database

Same shape as Skills: `name` → Name, `description` → Description, file URL → GitHub, `quick_start_prompt` → Quick Start Prompt, `assets_used` back-references → Workflows relation.

### Process guide frontmatter → Processes database

| Source | Notion property |
|---|---|
| `title` | Name (title) |
| guide summary / first paragraph | Description |
| `domain` | Owner (or Discipline/LOB — whichever select the user's copy has) |
| guide file URL (see link derivation) | Guide |
| workflows whose `business_process` matches | Workflows relation |

## Link derivation

When the workspace is a git repository with a GitHub remote, convert relative artifact paths to permanent URLs:

```
sops/lead-qualification-sop.md
→ https://github.com/<org>/<repo>/blob/<default-branch>/sops/lead-qualification-sop.md
```

Derive `<org>/<repo>` from `git remote get-url origin` and the branch from the default branch. If there is no GitHub remote, record the relative path as plain text and tell the user the link is local-only.

## Sync rules

1. **Exact-title match before create.** Search the target database for the exact `display_name` / `name` / `title`. Update the match; create a new page only if none matches exactly. Partial title matches are **not** duplicates — when in doubt, ask.
2. **One-way.** Markdown → Notion only. Never read Notion values back over manifest/frontmatter values (except during migration, below).
3. **Never destructive.** Never delete, archive, or clear properties on Notion pages. Only set properties you have source values for.
4. **Write back the pointer.** After creating a Workflow page, record its URL in the manifest's `notion_url` field.
5. **Schema tolerance.** Users' template duplicates vary by version. If a mapped property doesn't exist in their database, skip that field silently — never error, never create new properties without asking.
6. **Confirm and report.** First-time mirroring always requires explicit user confirmation. After any mirror, summarize what was created and updated, and remind the user the Markdown files remain the source of truth.

## Auto-sync after opt-in

A populated `notion_url` in a manifest is a **standing opt-in** for that workflow. Framework skills honor it in their closing steps: whenever a step refreshes `REGISTRY.md` for a workflow whose manifest has a `notion_url`, also update that workflow's Notion row with the fields the step just wrote (per the mapping above).

- **Build** additionally creates Skills/Agents rows for new `assets_used` entries and wires their Workflows relations.
- Subsequent auto-syncs proceed without asking, but report what was updated in the step's closing summary.
- **Best-effort, always:** if Notion is disconnected, unavailable, or errors, skip silently — an auto-sync failure must never fail or block the framework step.

Workflows without a `notion_url` are never auto-synced; offer the mirror after a full registry regeneration instead.

## Targeted registration

Simple commands register or update a **single asset** without running a full mirror: "register this skill in Notion", "add this workflow to my Notion registry", "update this agent in Notion", "add this process to Notion".

1. **Resolve the asset type** from the request or file path: `SKILL.md` → Skill; `.claude/agents/*.md` or `agents/*.md` → Agent; `outputs/<name>/workflow.yaml` (or a workflow name) → Workflow; `process-guides/*.md` (or a process name) → Process. If ambiguous, ask.
2. **Read the asset's source of truth** — its frontmatter or manifest. Never register from memory of the conversation; read the file.
3. **Find-or-create** the row in the matching core database using the field mapping and sync rules above (exact-title match; update if found, create if not).
4. **Wire relations**: a workflow links to its process (find-or-create the Processes row) and to the Skills/Agents rows for its `assets_used`; a skill/agent links back to the workflows that use it.
5. **Workflows only:** write the page URL back to the manifest's `notion_url` — this enables auto-sync from then on.
6. Confirm what was created or updated.

Reading is even simpler: for "what's in my Notion registry", query the four databases and summarize — no writes.

## Migrating from Notion

To move an existing Notion registry into Markdown, work the other direction:

1. Read the four core databases (plus the legacy Building Blocks database if the user's copy has one).
2. Merge fields into the corresponding `workflow.yaml` manifests and asset frontmatter, mapping select values to kebab-case ("Under Development" → `under-development`, "Augmented" → `augmented`).
3. Create stub process guides for processes that have workflows but no guide.
4. Record each Workflow page's URL in its manifest's `notion_url`.
5. Flag Notion rows with no matching local file for the user to resolve — don't invent files for them.
6. Regenerate `REGISTRY.md`.
