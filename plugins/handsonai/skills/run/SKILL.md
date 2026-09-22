---
name: run
description: >
  This skill should be used when the user has built and tested workflow artifacts and is ready to put the
  workflow into production. It guides the first real run, writes the Run Card, and sets up the run log and
  the first review date.
  Also use when the user says "continue my workflow" and the Workflow node shows Step 6 (Run) is next. This is Step 6 (Run) of the AI Workflow Framework.
user-invocable: true
---

# Workflow Run

Put a tested AI workflow into production: do the first real run on real work, then leave a one-page Run Card, a run log, and a review date behind.

**Design principle:** The skill is the framework, the model is the platform expert. No platform-specific details appear in *generated artifacts or user-facing recommendations* — all platform knowledge is resolved by the model at runtime (registry lookup, web search). The skill's own procedure may branch on **detected environment capabilities** — detect and adapt; never assume a capability exists because it exists on one surface.

**Role:** You are an **Agentic AI Architect**. Your role is to get the workflow running on real work and leave the user a Run Card they can follow on any given day.

## Workflow

**Set expectations up front (first message).** Say: "This takes about 15–20 minutes. You've tested the workflow; now we use it on real work for the first time, and I'll leave you a one-page Run Card so you know exactly how to start it on any given day."

#### Phase 1 — Load context

> **Registry entry:** the workflow's registry entry is its Workflow concept node in the workspace's `registry/` bundle — see `indexing-registry/references/registry-bundle.md` (in this plugin) for resolution, write rules, and your fields. If the workspace has no `registry/SCHEMA.md`, offer the `scaffolding-registry` skill first (it also migrates legacy `workflow.yaml` workspaces); do not write registry entries until the bundle exists.

Read the Workflow node, the Design Spec, the artifacts and skills Build linked under the node's `# Artifacts` / `# Skills` (the paths from Build Phase 10, the reconciliation table), and `test-results.md`. **Resume orientation** as in every framework skill. If the verdict is not `ready`, say so and route to Build: `not-ready` enters Build's fix mode, `waiting-on-access` means authorizing the named connector there, and Build sends the user back to Test once that is done. Read the platform's `capabilities.skill_install` (or, if the entry has no `capabilities`, its `skill` documentation URL(s) and `notes`), `capabilities.context_location` and `capabilities.unattended_runs` (or, if the entry has no `capabilities`, its `notes`) — every concrete instruction below comes from there, never from this file.

**Guided-mode platforms** (spec `platform_mode: guided` with GUI instruction documents instead of files): the Run Card still has the same six headings; "How to start it" points at the configured agent or skill in the platform UI and the instruction documents Build produced.

#### Phase 2 — The first real run

Before the run: the user opens a new chat and confirms the skill (or agent) is listed; if it isn't, go back to Build's install handoff — nothing else here will work. This is the first time the workflow runs on *real* work rather than a test input. Name it: "Every run so far used test inputs. Let's do this week's real one together." The user starts it exactly as an operator would (fresh conversation, invoked by name, per the platform's `capabilities.skill_install`, or, if the entry has no `capabilities`, its `skill` documentation URL(s) and `notes`), with the real input. Watch for: the connectors being authorized in *that* account, context files resolving, each human gate actually pausing. Confirm the output against the report-card lines once more. If anything fails here that Test passed, it is almost always the run environment (a connector not authorized in this account, a context file in the wrong place) — fix that, don't rebuild.

#### Phase 3 — Write the Run Card

Save to `outputs/[workflow-name]/run-guide.md` with exactly these headings, in this order, each a short plain-language section:

```markdown
# [Workflow Name] — Run Card

## Your first real run
[What happened on the first real run today, in two sentences, and what to expect next time.]

## How to start it
[The exact phrase or click, taken from the platform's `capabilities.skill_install`, or, if the entry has no `capabilities`, its `skill` documentation URL(s) and `notes` — e.g., "Open a new chat in your Weekly Reports project and say: run the weekly status report skill." The input to give it. If the workflow serves others: how a teammate installs it (one or two steps from the same source) and the same start phrase.]

## What to have ready
[Inputs in hand. Connectors authorized in the account that runs it — list each. Context files in place — list each with its location from the platform's `capabilities.context_location`, or, if the entry has no `capabilities`, its `notes`. The skill and any agents installed in that account. For an automated workflow, the pre-granted permissions from "How to start it". A fresh conversation does not inherit this session's setup; this list is what it needs.]

## What to check before you act on the output
[The human gates (G1…) in plain words: what the workflow pauses for and what you're deciding. The (must) criteria as a two-line reminder.]

## Log the run
[One line per run in outputs/[workflow-name]/runs.md: date, input, result, edits needed, notes. If the workflow runs on-platform, the orchestrator skill appends the row itself — verify it did on today's run; if not, add that step to the orchestrator now. Ten seconds a run; it is the evidence your first review needs.]

## Your first review
[The date — monthly for high-frequency workflows, quarterly for occasional. The exact re-entry sentence: "Run the improve skill on [workflow name]." What to bring: nothing; the registry node, test results, and run log carry it.]
```

**Scheduling** is part of "How to start it" **only when the Workflow node's `execution_mode` is `automated`** and the platform's `capabilities.unattended_runs`, or, if the entry has no `capabilities`, its `notes`, says the platform supports it: then state the platform's scheduling mechanism, the pre-granted permissions and non-interactive credentials it needs, and the safety checklist from the spec's Safety & Permissions section in plain words — least-privilege scopes; human gates or draft-don't-send actually enforced in the deployed artifacts; content the user didn't author treated as data, never instructions; a cap on actions per run; every write visible in the run log. For an `augmented` workflow, one line: "This runs when you start it. If you later want it on a schedule, come back to this step and we'll set that up." If the workflow is `automated` but the platform's capability entry says unattended runs are not supported, say so in one line and name the platforms that do support them, from the same capability entry — do not improvise a workaround.

Present the Run Card in the conversation as well as saving it.

#### Phase 4 — Run log, registry, review date

Create `outputs/[workflow-name]/runs.md` with the header row, and add today's first real run as row one — unless the orchestrator already appended it during Phase 2, in which case just check the row is right:

```markdown
| Date | Input / trigger | Result | Edits needed | Notes |
|---|---|---|---|---|
```

Update the Workflow node: `status: in-production`, `stale_after: YYYY-MM-DD` (the review date agreed with the user), and link the Run Card and run log under `# Artifacts`. Invoke the `indexing-registry` skill for a maintenance pass (best-effort). If the platform supports reminders or scheduled tasks, offer to set the review reminder. No persistent workspace? Tell the user to save the Run Card and the run log.

## Outputs

- `outputs/[workflow-name]/run-guide.md` — the Run Card (six fixed headings above).
- `outputs/[workflow-name]/runs.md` — the run log, one line per run.
- Workflow node updated: `status: in-production`, `stale_after`, artifact links.

## Guidelines

- Plain language; every concrete instruction comes from the platform's `capabilities`, never from memory of a platform's UI — verify with one web check if a capability value looks stale.
- Close with the inventory of everything produced across Steps 3–6 (Design Spec, built skills/agents, test results, Run Card, run log) and the review date, then: "When [date] arrives — or sooner if the output starts needing more edits — start a new conversation and say: *Run the improve skill on [workflow name]* — a review takes 30–45 minutes."
- For organizational workflows, after the summary offer the `writing-workflow-sops` skill to document the workflow as an SOP for the team.
- **Signpost each phase transition.** Announce each phase in one short line as you reach it ("Phase 3 of 4 — writing the Run Card") so the user always knows where they are.
