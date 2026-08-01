# Manifest Resolution — Locating and Writing "the Manifest"

Every framework skill treats **the workflow manifest** as the single source of truth for workflow registry metadata. This document defines how any skill *resolves* that manifest — where it lives, how to read it, and how to write it — so the choice is made in one place instead of per-skill.

There are two backends. Detection is a single check:

> **Does `registry/SCHEMA.md` exist at the workspace root?**
>
> - **Yes** → **Bundle backend**: the workspace keeps its registry as an OKF-style knowledge bundle. The manifest is the **Workflow concept node** `registry/workflows/<slug>.md`.
> - **No** → **YAML backend** (default): the manifest is `workflow.yaml` in the workflow folder (`outputs/<name>/` or `<lob>/workflows/<name>/`), exactly as specified in `manifest-schema.md`.

Run the check once at skill load and use the same backend for every manifest read and write in that skill run. Never write both formats for the same workflow.

---

## YAML backend (default)

No `registry/SCHEMA.md` in the workspace root. Behavior is exactly today's contract: read and write `workflow.yaml` per `references/manifest-schema.md` (schema, field ownership table, and closing-step rules unchanged). Nothing in this document modifies the YAML backend.

---

## Bundle backend

`registry/SCHEMA.md` exists at the workspace root. The workspace's registry is a knowledge bundle; the manifest's role is taken by a markdown **Workflow concept node**:

```
registry/workflows/<slug>.md
```

where `<slug>` is the workflow's kebab-case ID (the same value the YAML backend stores in the `workflow:` field). The node is YAML frontmatter + markdown body sections. The workspace's own `registry/SCHEMA.md` is authoritative for node structure — read it before your first node write in a session and defer to it if it differs from anything here.

### Field mapping (workflow.yaml → Workflow node)

| workflow.yaml field | Workflow node equivalent |
|---|---|
| `workflow` | the filename slug (`registry/workflows/<slug>.md`) |
| `display_name` / `name` | frontmatter `title` |
| `description` | frontmatter `description` |
| `last_updated` | frontmatter `timestamp` |
| `status` | frontmatter `status`, kebab-case (see status mapping below) |
| `type` (execution mode) | frontmatter `execution_mode` — `manual` \| `augmented` \| `automated` |
| `autonomy` | frontmatter `autonomy` — `deterministic` \| `guided` \| `autonomous` |
| `definition_type` | frontmatter `definition_type` — `step-driven` \| `goal-driven` (kebab-case) |
| `trigger` | frontmatter `trigger` |
| `business_process` | a `N. [Title](/workflows/<slug>.md)` line in the Process node's curated ordered `# Workflows` list (`registry/processes/<process-slug>.md`) — the list is BOTH the Workflow→Process edge and the value-chain order. Never write a `process:` frontmatter field on the Workflow node (banned; lint errors). Place the line at the workflow's position in the process sequence (append at the end if unknown); a workflow must appear in exactly one process's list. |
| `next_review` | frontmatter `next_review` |
| `artifacts:` map | labeled links in the `# Artifacts` body section (see below) |
| `platform_artifacts` | links in the `# Skills` and `# Agents` body sections |
| `notes:` | body prose |

**Status mapping** (Title Case → kebab):

| workflow.yaml | Workflow node |
|---|---|
| `In Production` | `in-production` |
| `Under Development` | `under-development` |
| `Backlog` | `backlog` |
| `Archived` | `retired` |

**Artifacts section.** The `# Artifacts` body section holds one labeled link per artifact. Use these labels:

- Raw source
- Run log
- Output
- SOP
- Requirements
- Design spec
- Test results
- Run guide

Example:

```markdown
# Artifacts

- [Requirements](../../learning/workflows/lead-qualification/requirements.md)
- [Design spec](../../learning/workflows/lead-qualification/design-spec.md)
- [SOP](../../learning/sops/lead-qualification-sop.md)
```

**Skills and Agents sections.** Entries from `platform_artifacts` become links in the `# Skills` and `# Agents` body sections, split by artifact kind.

### Fields that do NOT exist in bundle mode

Never write these to a Workflow node — they have no equivalent and must not be invented as frontmatter:

`current_step`, `health`, `last_run`, `platform`, `owner`, `sequence`, `lob`, `notion_url`

**Framework progress without `current_step`.** Progress state lives in the workflow's artifact folder, not the node. A skill that needs to know "what step is next" infers it from which artifacts exist:

| Artifact present | Step completed |
|---|---|
| requirements | 2 (Deconstruct) |
| design-spec | 3 (Design) |
| platform artifacts (skills/agents) | 4 (Build) |
| test-results | 5 (Test) |
| run-guide | 6 (Run) |

### Write rules (bundle mode)

1. **Frontmatter values MUST be single-line.** No `>-` or `|` block scalars, no inline `#` comments. If a description is long, shorten it — don't wrap it in a block scalar.
2. **Link conventions:** a link with a leading `/` is **bundle-root-relative** (relative to `registry/`); a link without a leading `/` is **repo-root-relative**.
3. **Never edit generated content.** Any content between `<!-- GENERATED:... -->` and `<!-- /GENERATED -->` markers is machine-owned — write around it, never inside it.
4. **Regenerate after writing.** After any node write, if `tools/lint-registry.js` and `tools/compose-registry.js` exist in the workspace, run:

   ```bash
   node tools/lint-registry.js && node tools/compose-registry.js
   ```

   If the environment can't run Node, say so and note that CI will regenerate — a failed regeneration never fails the step that requested it.

### Process nodes

In bundle mode the business-process record is likewise a concept node: `registry/processes/<process-slug>.md`. Workflows join to it via the process's curated ordered `# Workflows` list (see the mapping table above) — child nodes carry no pointer. When a skill produces a process guide, the Process node's `guide:` frontmatter field points at the guide file (same link conventions as above).
