---
name: scaffolding-registry
description: >
  This skill should be used when the user wants to set up their AI Registry as a
  knowledge bundle — a registry/ folder with SCHEMA.md and concept nodes for their
  business. Triggers: "set up my registry", "set up my AI registry", "create my
  registry", "stand up my knowledge base", "scaffold my registry", starting the
  registry lab, or when any framework skill finds no registry/SCHEMA.md in the
  workspace. Also handles migrating legacy workspaces (outputs/*/workflow.yaml
  manifests or flat requirements files) into the bundle. Re-running on an existing
  bundle fills gaps; it never re-scaffolds.
user-invocable: true
---

# Scaffolding Registry

Stand up a student's AI Registry as an [OKF v0.2](https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf) knowledge bundle: a `registry/` folder with a `SCHEMA.md` producer profile and concept nodes for their real business. This is the on-ramp — a ~30-minute guided interview that gets a first, real Workflow node written and linked, not a demo.

## What this builds

```
<workspace or repo root>/
├── REGISTRY.md              ← Tier 1 dashboard (derived, never hand-edited)
├── registry-dashboard.html  ← Tier 2 dashboard (derived, optional)
├── registry/                ← the OKF v0.2 bundle
│   ├── SCHEMA.md            ← producer profile (written by scaffolding-registry)
│   ├── index.md             ← bundle root; frontmatter okf_version: "0.2"
│   ├── log.md                ← migrations + schema changes only
│   ├── businesses/  lines-of-business/  functions/
│   ├── processes/   workflows/          notes/
│   │       (each typed directory has its own index.md)
├── outputs/<workflow>/      ← raw-source layer, unchanged (requirements,
│                              design-spec, runs.md, generated artifacts;
│                              event-facts live here, never in nodes)
├── sops/  process-guides/   ← unchanged homes; nodes link to them
```

The registry is the structured record every framework skill reads and writes — `naming-workflows` stubs a Workflow node in it, `deconstruct` fills in requirements, `run` flips status to `in-production`, and so on all the way through `improve`. `registry/SCHEMA.md` is the contract that makes that possible: it defines the six concept types (Business, LineOfBusiness, Process, Workflow, Note, Function), their required frontmatter, and the rules — enum values, link discipline, banned fields — that every skill's writes and every maintenance pass's lint checks agree on. Write it once per workspace, using `references/schema-template.md` verbatim; after that, the student's own copy is authoritative and every skill re-reads it before writing.

## Platform & Workspace

The procedure below is identical everywhere — the same six phases, the same node shapes, the same SCHEMA.md. Platforms differ only in how the skill instructions arrive and how bytes get written to the bundle.

| Platform | Skill delivery | Bundle access | Write path |
|---|---|---|---|
| Claude Code | handsonai plugin | local clone | direct edits; student commits |
| Cowork | plugin via marketplace | repo folder as project | direct edits |
| ChatGPT desktop (Codex) | same SKILL.md dirs at `~/.agents/skills/` (user-level default) or repo `.agents/skills/` (optional pin) | local clone | direct edits; student commits |
| claude.ai | skill ZIP (existing Releases channel) | GitHub connector / uploaded copy | generate-and-commit via github.com; the skill states explicitly what is unwritten |
| ChatGPT web (Business/Enterprise) | Personal Skill upload (same ZIP) | GitHub connector | generate-and-commit |
| M365 Copilot | agent-instructions packaging | SharePoint or GitHub connector | generate-and-commit |

A few rules follow from that table:

- **(a) Assistant-agnostic procedures.** Everything in this file — the phases, the write rules, the interview questions — is written for "your AI assistant" in general. Platforms differ only in delivery and write path, never in what gets written or asked.
- **(b) Generate-and-commit surfaces must say what's unwritten.** On claude.ai, ChatGPT web, and M365 Copilot, the assistant cannot push to the student's repo directly — it generates the bundle files in the conversation and the student commits them by hand (via the GitHub connector, github.com's file editor, or a SharePoint sync). Every time content is generated rather than written, say so explicitly — never leave the student assuming a file landed somewhere it didn't.
- **(c) Default home: a GitHub repo the student owns.** Both courses this skill supports teach GitHub, and a repo the student controls is the one home every platform in the table above can reach one way or another (clone, connector, or manual commit).
- **(d) One skill artifact, three channels.** The same agentskills.io-standard SKILL.md — built by the existing `build-skill-zips.sh` pipeline — is what Codex desktop scans locally, what ChatGPT web's Personal Skills accepts as an upload, and what claude.ai accepts as an uploaded skill. There is no separate packaging for each.
- **(e) Repo-checked-in skills are optional, not the default.** Codex desktop can read `.agents/skills/` inside the student's repo, but the default is a user-level install (`~/.agents/skills/`) — checking a skill into every repo it's used in invites version drift between repos. Only pin a repo-local copy when the student has a specific reason to.

**Platform note (Claude Code / Cowork):** on these two, the Tier 2 dashboard this skill's closing step offers can be published as a Claude Artifact for easy sharing — a mechanic specific to these platforms, not part of the cross-platform procedure above.

## Before scaffolding

Before running the interview, check what's already in the workspace:

1. **`registry/SCHEMA.md` exists** → this is **gap-filling mode**, not a fresh scaffold. List which concept types have zero nodes and which typed directories are missing their `index.md`, tell the student what's missing, and offer to fill only those gaps. Never overwrite an existing node, and never rewrite `SCHEMA.md` once the student has one — their copy is authoritative from here on.
2. **No `registry/SCHEMA.md`, but a legacy layout is detected** — `outputs/*/workflow.yaml` (the old manifest layout) or an `outputs/<name>-requirements.md` with no matching `outputs/<name>/` folder (the old flat layout) — offer the migration path in `references/migrating-legacy-workspaces.md` instead of, or before, a fresh scaffold. Migration writes into a newly scaffolded bundle; it never invents its own structure.
3. **Neither exists** → run the interview below from Phase 0.

## The interview

Six phases, ~30 minutes total, run in order. Follow `references/interview-guide.md` for the exact opening questions, follow-ups, worked examples, and fast paths for each phase — this section is the map; that file is the script.

**Phase 0 — Home (2 min).** Establish where the registry will live — new repo from the template (`https://github.com/jamesgray-ai/ai-registry-template`), an existing repo/workspace, or a cloud generate-and-commit fallback — and run the legacy-detection check. Follow `references/interview-guide.md`.

**Phase 1 — Business (3 min).** One Business node: name, one-sentence identity, `status`, optional `url`. Almost always exactly one business per registry. Follow `references/interview-guide.md`.

**Phase 2 — Lines of Business (4 min).** One or more LineOfBusiness nodes in a curated, ordered list under the Business node. Solo consultants get one default LOB named after the business — no artificial splitting. Follow `references/interview-guide.md`.

**Phase 3 — Functions (3 min).** Offer the starter set (Marketing, Sales, Service Delivery, Operations, Product, Customer Success, IT/Engineering); the student trims and renames it. Every Function node is written with its empty GENERATED `# Owns` block from the start. Follow `references/interview-guide.md`.

**Phase 4 — Processes (8 min).** Per LOB, the two or three highest-value processes — not an exhaustive list; Analyze grows this later. Each needs a required `owner:` function slug. Once Processes name their owners, the owning Functions' `# Owns` blocks written empty in Phase 3 are now stale — that's expected, not an error; the Phase 6 maintenance pass regenerates them, and lint only ever flags stale content as a warning, never a blocker. Follow `references/interview-guide.md`.

**Phase 5 — First Workflow (7 min).** The one workflow the student will carry through the rest of the framework, written as a full Workflow node and slotted into its Process's curated list. Follow `references/interview-guide.md`.

The Brightwork examples in `references/example-registry.md` are shown, never copied. Every node written is the user's real business.

**Phase 6 — Close (3 min).** Optional Note, founding `log.md` entry, and hand-off — see Close below. Follow `references/interview-guide.md`.

If a phase runs over its timebox, write what's been gathered, note the gap for the close-out summary, and move on — missing nodes are homework for later; fictional ones are never an acceptable substitute.

## Write rules

- **The student's `registry/SCHEMA.md` is authoritative once it exists.** Re-read it immediately before every write in this skill, including during gap-filling and migration — never write from memory of what the schema template said.
- **Stamp `generated: { by: process:scaffolding-registry, at: <date> }`** (single-line flow map, `at` as `YYYY-MM-DD`) on every node this skill creates or edits.
- **Function nodes are always written with their empty GENERATED `# Owns` block** at creation time — never deferred to a later maintenance pass. A Function missing that block is a lint error, because the maintenance pass has nothing to fill.
- **Every new node gets added to its typed directory's `index.md`.** A concept file with no entry in its directory index is a lint error; write or update the index in the same pass as the node.

## Close

End Phase 6 by writing a founding `registry/log.md` entry describing the scaffolding run (what was created, and — for a migration — every workflow migrated in that run), and making sure every typed directory has an `index.md`, even a stub one.

Then invoke the `indexing-registry` skill for the workspace's first maintenance pass: it lints the new bundle, generates the Tier 1 `REGISTRY.md`, and offers the Tier 2 visual dashboard. This is a best-effort hand-off — if the maintenance pass can't run for some reason, say so plainly rather than leaving the student assuming it happened. The lab should end with something visual on screen, not a blank terminal.
