# Tier 2 data island — derivation contract

How to hand-build the JSON data island for `registry-dashboard.html` when the workspace has no `tools/compose-registry.js` (a plain-folder registry on a platform without Node). Every rule below is what compose does, so a hand-built island and a composed one render identically. The shape is `data-island.schema.json` (beside this file); this page says where each value comes from. When `tools/compose-registry.js` exists, run it instead — see "Workspace-generator precedence" in SKILL.md.

## Rules that apply everywhere

| Rule | Value |
|---|---|
| `id` | the node's filename without `.md` (`registry/workflows/weekly-status-report.md` → `weekly-status-report`) |
| `nodePath` | the node's path from the workspace root, always starting `registry/` |
| `nodeUrl` | only when the workspace's own `.git/config` has a `[remote "origin"]` pointing at GitHub: `https://github.com/<owner>/<repo>/blob/main/` + `nodePath`. No remote (or not GitHub) → omit the key. Never read a parent directory's git config. Omitting it loses every "Source" link on a GitHub-hosted registry, so check the remote before deciding to omit |
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
| `workflows` | traversal order (LOB → Process → `# Workflows` list), then every Workflow no Process lists, sorted by path, with `processId: null` and `lobId: null` | `processId`, `lobId` = parent slugs; `step` (below); `skills` and `agents` = the link targets (workspace paths) from the node's `# Skills` and `# Agents` sections, in order |
| `notes` | every Note node, sorted by path | `links` = the node body's bundle-root-relative links (those starting with `/`), in order |
| `skills` | every `SKILL.md` found as `**/skills/<name>/SKILL.md` under the workspace (skip `.git`, `node_modules`, `tools/fixtures`), sorted by path | `id` = the `<name>` directory; `title` = frontmatter `name` or `title`, else `id`; `description` = frontmatter `description` or `""`; `quickStartPrompt` = frontmatter `quick_start_prompt` or `quickstart_prompt`, else omit; `usedBy` = slugs of the Workflow nodes whose `# Skills` link points at this file; `nodePath` = the workspace path; no `nodeUrl` |
| `agents` | every `.md` in `.claude/agents/` and `agents/`, sorted by path | as `skills`, with `id` = the filename without `.md` and `usedBy` from `# Agents` links |

### `step` on a workflow

`step` is framework progress, 1–7, inferred from what the node links (registry-bundle.md §4). Start at 1 (the node exists). Add 1 for each of these `# Artifacts` link titles present, compared case-insensitively: `Requirements`, `Design spec`, `Test results`, `Run guide`, `Improvement plan`. Add 1 more if the node has at least one `# Skills` or `# Agents` link. There is no stored step field; never read one.

## Serialization and injection

1. Serialize the island as JSON.
2. Replace every `<` with `\u003c` **before** embedding. A description such as "handles <200 leads/day" would otherwise close the `<script>` element and leave the page blank; `\u003c` is valid JSON and decodes to the same character.
3. Replace only the text content of `<script type="application/json" id="data">` in `dashboard-template.html`. Nothing else in the template changes.
4. Save as `registry-dashboard.html` at the workspace root. Open it from `file://` — a blank page or a console error means the island is malformed; the most common causes are an unescaped `<` or a missing comma.

## Settled questions

- **Which frontmatter keys travel.** Only the fields the schema lists. `type` and `generated` never appear in the island.
- **Dates.** Frontmatter dates (`stale_after`) are written as `YYYY-MM-DD` strings.
- **Empty sets.** Array fields (`skills`, `agents`, `usedBy`, `owns`, `processes`, `workflows`, `links`, and the top-level collections) are always present, `[]` when empty. "Omit the key" applies to scalar fields only.
- **Link targets in `skills` / `agents`.** Copy the `# Skills` / `# Agents` link target exactly as written in the node (a workspace path such as `.claude/skills/some-skill/SKILL.md`); `usedBy` matches on that same string.
- **Skill title precedence.** Frontmatter `name` wins over `title` when both exist.
- **`owns` source.** Derive from each Process's `owner:` frontmatter, never from a Function's GENERATED `# Owns` block (that block is itself derived and may be stale).
- **Lint before a hand-build.** Nothing to run on a platform without Node: read the bundle for the lint conditions you can see (every node indexed, every curated-list link resolves, no banned fields) and rely on the self-check below; say in the hand-off that lint did not run.
- **Formatting.** Any valid JSON; indentation and key order do not matter to the renderer.

## Self-check before saving

- Every `processId`, `lobId`, `ownerId`, and every slug in `processes`, `workflows`, `owns`, and `usedBy` names an `id` that exists in the island.
- Every Workflow node in the bundle appears exactly once in `workflows`.
- `nodeUrl` is present on all bundle nodes or on none.
- The island contains no `<`.
