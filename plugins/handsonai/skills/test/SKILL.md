---
name: test
description: >
  Guide structured testing of AI workflow artifacts, evaluate output quality, identify which building blocks need adjustment, and determine readiness for deployment. Use when the user has built workflow artifacts and needs to test them. Also use when the user says "continue my workflow" and the workflow manifest shows Step 5 (Test) is next. This is Step 5 (Test) of the AI Workflow Framework.
user-invocable: true
---

# Test Workflow

Check the built workflow against the yes/no criteria captured in Deconstruct, one realistic input at a time, and decide whether it is ready to use.

## Workflow

**Set expectations up front (first message).** Say: "This step takes about 45 minutes per round, and most workflows need two to four rounds before they're ready — that's normal, not failure. Six rules for judging your workflow: (1) judge it against what you wrote in Deconstruct, not how it feels; (2) use real inputs, including one hard case; (3) run it in a fresh conversation, not this one; (4) every criterion is met or it isn't — one miss is a miss; (5) I grade first with evidence, you make the call; (6) test, fix, test again — don't fix mid-test."

**Where the workflow runs — read this before anything else.** The workflow never runs inside this conversation. This conversation already holds the requirements, the design, and everything said while building, so a run here would see all of it and look better than it will in real use. Every scenario runs in a **fresh conversation** with only the installed skill (or agent) and the scenario's input, started the way an operator would start it — read the platform's `capabilities.skill_install` in the platform registry (or its `notes` if `capabilities` is absent) for the exact way to start it. The user brings the output back here (paste or attach), and this conversation **scores**. Tell the user this in one sentence at the start: "You'll run each input in a new chat; I'll grade the results here."

If the skill is not yet installed on a platform that needs installation, stop and route the user back to Build's install step first. If files were edited since installation, remind the user the installed copy is stale — repackage and reinstall before running.

### 1. Load context

> **Registry entry:** the workflow's registry entry is its Workflow concept node in the workspace's `registry/` bundle — see `indexing-registry/references/registry-bundle.md` (in this plugin) for resolution, write rules, and your fields. If the workspace has no `registry/SCHEMA.md`, offer the `scaffolding-registry` skill first (it also migrates legacy `workflow.yaml` workspaces); do not write registry entries until the bundle exists.

Read the workflow's Workflow node (`registry/workflows/<slug>.md`) to locate the artifacts, then read the Design Spec and the Workflow Requirements it references. **Resume orientation:** if the user arrived via "continue my workflow" or with no stated workflow, check `registry/workflows/` for existing Workflow nodes (if several, list them), infer progress from which artifacts each node's `# Artifacts` section links, and if Test isn't the next step, say so and route to the right skill. Verify both files exist — if either is missing, stop and say which.

From the Requirements, build the **check list** the report card will use: every Acceptance Criterion (`AC1…`, with **(must)** marks), every Rules & Constraints row (`R1…`), every Human Gate (`G1…`), and each step's stated output (`Step N output`). Load the Example Scenarios (`E1…`) and any Golden Examples. Introduce the vocabulary in plain language once: a *scenario* is one realistic input; the *report card* is the table of every expected behaviour and whether the run met it; the *baseline* is the first completed report card, kept so a later review can see what changed.

If the Requirements predates this format (has "Dimensions that matter" and a prose "Minimum bar" instead of numbered `AC` lines), convert it now with the user: turn each dimension and the "what good looks like" text into numbered yes/no statements, write them back into the Requirements file under `## Acceptance Criteria`, and note the conversion in this run's results.

### 2. Confirm the passing rule

Restate it so nobody is surprised later: "The workflow is **ready** when every line of the report card is Met on every scenario. A miss on a **(must)** line always fails the scenario. Any other miss you can either fix or explicitly accept — an accepted miss is recorded, not hidden." Ask whether any criterion should be added or dropped before running. Changes go into the Requirements file, not into this conversation only.

### 3. Smoke run (one scenario, logic only)

Before the full round, walk one scenario mentally against the built skill's text — read the orchestrator and check that each Requirements step, rule, and gate is actually represented. This catches obvious gaps (a missing gate, an unreferenced context file) before the user spends a run on them. It is not a scored run.

### 4. Integration pre-flight

For each connector the scenarios exercise, confirm the access it needs (read vs. write) is authorized in the account that will run the workflow. If a write path is blocked, do not abort: run everything else and mark the blocked step **simulated** in the report card (`Result: Not run — waiting on [tool] write access`). The round's verdict is then `waiting-on-access`, which is an authorization gap for the user to fix, not a defect to rebuild.

**Live-system caution.** A real run can create real drafts, rows, or events. Prefer a clearly marked test record; after the round, list everything created and where, and offer to remove it (Step 8).

### 5. Run and grade each scenario

For each scenario `E1…`:

1. The user runs it in a fresh conversation and brings back the output.
2. **Grade first, with evidence.** For every line of the check list, decide Met / Not met and quote the evidence — a count, a phrase, a missing element. Compare against the Golden Example where one exists (missing / extra / substantively different), remembering it is one good answer, not the only one: the question is "would the user send this instead?"
3. **Present the report card** for that scenario:

   | Expected | From | Result | Evidence |
   |---|---|---|---|
   | Every prospect row has contact info | AC1 (must) | Met | 20 of 20 rows |
   | Never includes previously contacted people | R3 | Not met | 2 rows already in the CRM export |
   | Pauses before sending | G1 | Met | Draft created, not sent |
   | Step 2 output: ranked list | Step 2 output | Met | 20 rows, ranked by fit score |

4. **The user confirms or overrides each result.** "I marked R3 Not met because two rows were already contacted — agree?" Record the confirmed result. The user is the judge; the grading is the starting point.
5. Ask one closing question per scenario: "How much would you have to edit this before using it — nothing, a little, or a lot?" Record as `edits: none | minor | major`.

### 6. Diagnose every miss

Map each Not met line to the building block that caused it:

| What went wrong | What to change |
|---|---|
| Output is generic or off-brand | **Context** — add examples, style guide, reference material |
| A step was skipped or misunderstood | **Orchestrator skill** — make that step's instruction explicit |
| A step needs expertise the AI doesn't have | **Component skill** — build or extend one for that step |
| Output format is wrong | **Orchestrator skill** — add an explicit format example |
| The AI ignored a reference file | **Context** — check the file is where the skill expects it and is readable |
| A tool call failed | **Connector** — verify the connection independently, then re-run |
| The AI had to make decisions the rules didn't cover | **Design** — the workflow may need an agent, or clearer rules |

Write the diagnosis as `## Issues identified`, one row per miss: `Scenario | Line | Building block (S1, S2, A1, C3, orchestrator, connector) | What to change`. Build's fix mode reads this table.

### 7. Verdict

- **Ready** — every line Met on every scenario (accepted misses recorded with the user's reason). → `run` skill (Step 6).
- **Not ready** — at least one unaccepted miss. → `build` skill; it will regenerate only the building blocks named in Issues identified, then come back here and re-run the failed scenarios, then the full set.
- **Waiting on access** — the logic passed but a connector's write access is not authorized. Name the connector and what to authorize. Not a rebuild.

### 8. Clean up test records

List every draft, row, message, or event the round created in live systems, with its location, and offer to remove each one.

## Output

Write results to `outputs/[workflow-name]/test-results.md`. If a results file already exists from a previous round, rename it with a date suffix (e.g., `test-results-2026-06-10.md`) first — earlier rounds are history, not waste. Update the Workflow node (`registry/workflows/<slug>.md`) to link the results under `# Artifacts`, then invoke the `indexing-registry` skill for a maintenance pass (best-effort — a failed refresh never fails this step). No persistent workspace? Tell the user to save the file and re-supply it at the next step.

**Open with YAML frontmatter** so Improve can diff rounds mechanically and Build can detect fix mode:

```yaml
---
workflow: [kebab-case name]
design_spec: outputs/[workflow-name]/design-spec.md
requirements: outputs/[workflow-name]/requirements.md
date: YYYY-MM-DD
environment: "[platform + notable conditions, e.g., Cowork, HubSpot connector live]"
readiness: ready | not-ready | waiting-on-access
criteria_total: 12          # lines on the check list × scenarios run
criteria_met: 11
results:
  E1: { AC1: met, AC2: met, R3: not-met, G1: met, edits: minor }
  E2: { AC1: met, AC2: met, R3: met, G1: met, edits: none }
---
```

Use the real IDs. Below the frontmatter:

- **Scenarios tested** — each scenario with its input
- **Report card** — one table per scenario, the confirmed results
- **Golden example deltas** — per scenario with a golden example: missing / extra / substantively different
- **Not run** — any line simulated or skipped, and why
- **Environment** — which connectors were live vs. simulated
- **Issues identified** — the diagnosis table from Step 6
- **Accepted misses** — any Not met the user accepted, with the reason
- **Verdict** — Ready / Not ready / Waiting on access, with the count ("11 of 12 lines met across 2 scenarios")
- **Test records created** — and whether they were removed

## Guidelines

- Two to four rounds is normal. Say so before the first round and again after it.
- Never say "eval", "dimension", or "score". Say "check", "line", "met", "not met".
- Keep the user on concrete evidence: "show me the row that's wrong" beats "was it good?"
- Never run a scenario inside this conversation. If the user asks you to, explain why in one sentence and ask them to open a new chat.
- If the Requirements has no Acceptance Criteria or Example Scenarios, help the user write them now as yes/no lines and 3–5 inputs, write them into the Requirements file, and note the gap.
