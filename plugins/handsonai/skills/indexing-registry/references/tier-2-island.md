# Tier 2 data island — derivation contract

How to hand-build the JSON data island for `registry-dashboard.html` when the workspace has no `tools/compose-registry.js` or code can't run there (a plain-folder registry on a platform without Node, or a registry in a working folder on a drive, read through the connection). Every rule below is what compose does, so a hand-built island and a composed one render identically. The shape is `data-island.schema.json` (beside this file); this page says where each value comes from. When `tools/compose-registry.js` exists, run it instead — see "Workspace-generator precedence" in SKILL.md.

## Rules that apply everywhere

| Rule | Value |
|---|---|
| `id` | the node's filename without `.md` (`registry/workflows/weekly-status-report.md` → `weekly-status-report`) |
| `nodePath` | the node's path from the registry's parent folder (the working folder: the workspace on Claude Code and Codex), always starting `registry/` |
| `nodeUrl` | only when the workspace's own `.git/config` has a `[remote "origin"]` pointing at GitHub **and** the node's file exists on that remote's copy of the current branch (from `.git/HEAD`): `https://github.com/<owner>/<repo>/blob/<branch>/` + `nodePath`. Use that branch name — never assume `main`. Check with `git ls-tree --name-only origin/<branch> -- <nodePath>`; if you can't run that check, or the file isn't there (never committed, or not pushed), omit the key. No remote or not GitHub → omit. Never read a parent directory's git config. Leaders never edit registry files by hand, so this link is only for seeing where a node lives; the renderer shows `nodePath` as plain text whenever no link would work |
| Missing values | omit the key. Keep an explicit `null` only where the schema allows it and compose writes it: an unassigned workflow's `processId` and `lobId` |
| Frontmatter names | `definition_type` → `definitionType`, `execution_mode` → `executionMode`, `stale_after` → `staleAfter`, `owner` → `ownerId`; everything else keeps its name |
| Array order | the order the curated lists give (below); where no list orders a set, sort by node path |

## Per collection

| Collection | Which nodes, in what order | Field derivations beyond frontmatter |
|---|---|---|
| `business` | the single Business node (`null` if none) | `url`, `status` from frontmatter |
| `lobs` | in the Business node's `# Lines of Business` order | `processes` = slugs from the LOB's curated `# Processes` list, in that order; `folder` from frontmatter |
| `functions` | every Function node, sorted by path | `owns` = slugs of the Process nodes whose `owner:` equals this function's slug, sorted by path; `lead` from frontmatter |
| `processes` | traversal order: each LOB in curated order, then its `# Processes` list in order | `ownerId` = `owner:`; `lobId` = the parent LOB's slug; `guide` from frontmatter; `workflows` = slugs from the Process's curated `# Workflows` list, in order |
| `workflows` | traversal order (LOB → Process → `# Workflows` list), then every Workflow no Process lists, sorted by path, with `processId: null` and `lobId: null` | `processId`, `lobId` = parent slugs; `state` (below); `skills` and `agents` = the link targets (workspace paths) from the node's `# Skills` and `# Agents` sections, in order |
| `notes` | every Note node, sorted by path | `links` = the node body's bundle-root-relative links (those starting with `/`), in order |
| `skills` | every `SKILL.md` found as `**/skills/<name>/SKILL.md` under the workspace (skip `.git`, `node_modules`, `tools/fixtures`), sorted by path | `id` = the `<name>` directory; `title` = frontmatter `name` or `title`, else `id`; `description` = frontmatter `description` or `""`; `quickStartPrompt` = frontmatter `quick_start_prompt` or `quickstart_prompt`, else omit; `usedBy` = slugs of the Workflow nodes whose `# Skills` link points at this file; `nodePath` = the workspace path; no `nodeUrl` |
| `agents` | every `.md` in `.claude/agents/` and `agents/`, sorted by path | as `skills`, with `id` = the filename without `.md` and `usedBy` from `# Agents` links |

### `state` on a workflow

`state` is the workflow's progress: the routing state's **name**, never its number, read from the workflow's folder, never from which links the node has. The folder is `[framework folder]/<slug>/`: `framework/<slug>/` beside `registry/` on every platform. There is no stored progress field; never read one, and never count links.

- **Where code can run,** run the `framework-state` script on the folder (`node tools/framework-state.js --json <folder>`, from the workspace's `tools/` or the plugin's) and copy its `name`; for state 0, show "Retired" when its `kind` is `retired` and "Runs outside the framework" when it is `running-work`. A non-zero exit means: work it out by hand, below.
- **By hand,** read the folder's current files (and the node's `status` and `big_change`) and take the first row that matches. It is the same rule the five step skills route by; this copy is for display only.

| Name | The first that matches |
|---|---|
| Retired | the node is `retired` (routing's state 0) |
| Runs outside the framework | the node is `in-production` and has no folder: running work Analyze recorded (routing's state 0) |
| Earlier version | `requirements.md` with no `revision:` in its frontmatter (or with a `Definition Type` row, a `## Steps Overview` heading, or `## Inputs` with no `## Path`); a `design-spec.md`, or a `design-plan.md` with no `requirements_revision:`; `test-results.md` with no `build-record.md` and no `history/set-aside-*/`; `test-results.md` with no `round:` |
| Redo pending | the node has `big_change` |
| Requirements needed | no folder, no `requirements.md`, or a `deconstruct-in-progress.md` |
| Plan needed | no `design-plan.md`; the requirements' `revision` above the plan's `requirements_revision` (revisions marked `plan_unaffected` aside); or a `change_requests` entry in the build record or results whose `id` isn't in the plan's `changes:` (one whose only task is `SCH` aside) |
| Plan to approve | the plan isn't `approved: true` |
| Build needed | no `build-record.md`; a task not built and saved, or built at a lower `rev` than the plan's (one waiting on an unanswered open item aside); the record's `plan_revision` not set or not the plan's highest task `rev` (unless a task waits on an unanswered open item); or a Not ready last round with an Issues row at Level `build`, or `direct_edit: undo` in the results, with no Build close after it |
| Waiting on an open item | every task that can be built is built, and one waits on an unanswered open item |
| Test needed | no `test-results.md`; a round `in-progress`; a Build close after the last round; or a Not ready last round with nothing in it for Build |
| Waiting on access | the last round is `waiting-on-access` |
| Ready to go live | the last round is `ready` for the current plan revision, with `go_live: pending` |
| Live | the node is `in-production`, and nothing above matched |

When a file the table needs can't be read, or two rows seem to fit, omit `state` rather than guess.

## Serialization and injection

1. Serialize the island as JSON.
2. Replace every `<` with `\u003c` **before** embedding. A description such as "handles <200 leads/day" would otherwise close the `<script>` element and leave the page blank; `\u003c` is valid JSON and decodes to the same character.
3. Replace only the text content of `<script type="application/json" id="data">` in `dashboard-template.html`. Nothing else in the template changes.
4. Save as `registry-dashboard.html` in the registry's parent folder (beside `registry/`). Where it's a local file, open it from `file://` as a self-check (don't report the check to the leader) — a blank page or a console error means the island is malformed; the most common causes are an unescaped `<` or a missing comma.

## Settled questions

- **Which frontmatter keys travel.** Only the fields the schema lists. `type` and `generated` never appear in the island.
- **Dates.** Frontmatter dates (`stale_after`) are written as `YYYY-MM-DD` strings.
- **Empty sets.** Array fields (`skills`, `agents`, `usedBy`, `owns`, `processes`, `workflows`, `links`, and the top-level collections) are always present, `[]` when empty. "Omit the key" applies to scalar fields only.
- **Link targets in `skills` / `agents`.** Copy the `# Skills` / `# Agents` link target exactly as written in the node (a workspace path such as `.claude/skills/some-skill/SKILL.md`); `usedBy` matches on that same string.
- **Skill title precedence.** Frontmatter `name` wins over `title` when both exist.
- **`owns` source.** Derive from each Process's `owner:` frontmatter, never from a Function's GENERATED `# Owns` block (that block is itself derived and may be stale).
- **Lint before a hand-build.** Nothing to run on a platform without Node: read the bundle for the lint conditions you can see (every node indexed, every curated-list link resolves, no banned fields) and rely on the self-check below. Don't mention lint to the leader.
- **Formatting.** Any valid JSON; indentation and key order do not matter to the renderer.

## Self-check before saving

- Every `processId`, `lobId`, `ownerId`, and every slug in `processes`, `workflows`, `owns`, and `usedBy` names an `id` that exists in the island.
- Every Workflow node in the bundle appears exactly once in `workflows`.
- `nodeUrl` appears only on nodes whose file is on the remote branch; when in doubt, omit it.
- The island contains no `<`.
