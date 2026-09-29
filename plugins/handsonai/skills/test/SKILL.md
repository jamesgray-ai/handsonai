---
name: test
description: >
  Guide structured testing of AI workflow artifacts, evaluate output quality, identify which building blocks need adjustment, and determine readiness for deployment. Use when the user has built workflow artifacts and needs to test them. Say *test this* after running the workflow in a new chat to grade that run. Also use when the user says "continue my workflow" and the Workflow node shows Step 5 (Test) is next. This is Step 5 (Test) of the AI Workflow Framework.
user-invocable: true
---

# Test Workflow

Check the built workflow against the yes/no criteria captured in Deconstruct, one realistic input at a time, and decide whether it is ready to use.

## Workflow

**Set expectations up front (first message of the opener).** Say: "This step takes about 45 minutes per round, and most workflows need two to four rounds before they're ready — that's normal, not failure. Six rules for judging your workflow: (1) judge it against what you wrote in Deconstruct, not how it feels; (2) use real inputs, including one hard case; (3) run each input in a new chat that has never seen your requirements or design, then grade it right there; (4) every criterion is met or it isn't — one miss is a miss; (5) I grade first with evidence, you make the call; (6) test, fix, test again — don't fix mid-test."

### How a round works

Say this to the user, in the opener only, in three sentences, in your own words but with this substance:

1. **Open the round.** In this chat I load your requirements and design, confirm the passing rule, write the check list, and check the connectors.
2. **Run and grade each input.** Open a new chat, run the workflow on one input, then say **test this** — I grade the conversation above, line by line, with evidence you confirm. One input per chat.
3. **Verdict.** After the last input, in that same chat, I diagnose every miss, give the verdict, and list any test records to clean up.

**Which chat you are in — you work this out, you never ask.** If this chat already contains a workflow run above the invocation, whether it ran here or was pasted in from another chat, go straight to Phase 5; the workflow is the one whose skill ran above. If that is not obvious, look for the in-progress `outputs/*/test-results.md`, and if there is more than one, list them and ask which workflow. Otherwise, settle the workflow first if you do not already know it: resolve it from `registry/workflows/` as Phase 1's resume orientation describes, and if more than one workflow has an in-progress round, list them and ask which one (a question about which workflow, never about which phase). Then read that workflow's `outputs/[workflow-name]/test-results.md` and take the branch it matches:

- `round_status: in-progress`, every scenario in **Scenarios to run** graded → **closing the round**, Phases 6–8.
- `round_status: in-progress`, scenarios still ungraded → **resuming**: say "N of M graded — run E(next) in a new chat next", hand that scenario over exactly as in Phase 4's closing line (the file's contents pasted here, asking for the real input first if the file holds only a placeholder, then the one-line start instruction), and stop — do not rewrite the file.
- `round_status: complete` and the user asks to finish or close the round → say the round is already finished and point to the verdict's next step.
- No file, a `complete` file with no such request, or a file written before this protocol (a `readiness` key and no `round_status`) → **opening the round**, Phases 1–4.

Never put this choice to the user.

**Where the results go — you work this out, you never ask.** After a run, look for the workflow's `outputs/[workflow-name]/test-results.md` with `round_status: in-progress`. Found and writable → grade here and append this scenario's confirmed results to it. A round file this chat wrote itself earlier — on disk or, with no workspace, in this conversation — counts as found. Found but `round_status: complete` → the round is closed; say so and do not append. Not found (no folder or workspace reachable from this chat), or the platform's `capabilities.context_location` — or, if the entry has no `capabilities`, its `notes` — says chats on this platform do not share files → say one sentence and stop: "This chat can't reach your results file — copy this whole conversation and paste it into the chat where we opened the round; I'll grade it there." The opener chat grades a pasted run with the same Phase 5 and writes the same report card into the same file. Never call the two paths "modes" or offer them as a choice.

**Contamination guard.** Before grading a run, check that the requirements, the Design Spec, or the built artifacts were not read, attached, or discussed in the chat where the run happened before it started — for a run in this chat, that is this chat; for a run pasted into the opener, ask one question: "Did that chat see your requirements, design, or built files before you started?" If they were, refuse in one sentence — "this run saw your design before it started, so it would look better than real use — run it again in a fresh chat" — and record nothing, then hand them the same scenario again as in Phase 4's closing line.

**Starting a run.** When you send the user off to a new chat, tell them in one line how to start the workflow there: read the platform's `capabilities.skill_install` in the platform registry (or, if the entry has no `capabilities`, its `notes`) for the exact way, and give them that. If the workflow lives in a project or folder with context files, the new chat is opened inside it.

If the skill is not yet installed on a platform that needs installation, stop and route the user back to Build's install step first. If files were edited since installation, remind the user the installed copy is stale — repackage and reinstall before running.

#### Phase 1 — Load context

> **Registry entry:** the workflow's registry entry is its Workflow concept node in the workspace's `registry/` bundle — see `indexing-registry/references/registry-bundle.md` (in this plugin) for resolution, write rules, and your fields. If the workspace has no `registry/SCHEMA.md`, offer the `scaffolding-registry` skill first (it also migrates legacy `workflow.yaml` workspaces); do not write registry entries until the bundle exists.

This is the opener. Read the workflow's Workflow node (`registry/workflows/<slug>.md`) to locate the artifacts, then read the Design Spec and the Workflow Requirements it references. **Resume orientation:** if the user arrived via "continue my workflow" or with no stated workflow, check `registry/workflows/` for existing Workflow nodes (if several, list them), infer progress from what each node already links — its `# Artifacts` labels, plus its `# Skills` / `# Agents` links for Step 4 — and if Test isn't the next step, say so and route to the right skill. Verify both files exist — if either is missing, stop and say which.

From the Requirements, build the **check list** the report card will use: every Acceptance Criterion (`AC1…`, with **(must)** marks), every Rules & Constraints row (`R1…`), every Human Gate (`G1…`), and each step's stated output (`Step N output`). If a step's stated output is the human decision a gate already grades, do not add a separate `Step N output` line for it — one behaviour, one line. Load the Example Scenarios (`E1…`), their `; tests …` tails, and any Golden Examples — each scenario's input is a file, at the path its **Input** cell in the Example Scenarios table begins with; read it from there when you need its contents. If a cell has no path (a Requirements written before inputs were saved as files), the cell's text is the input — use it as written. Introduce the vocabulary in plain language once: a *scenario* is one realistic input; the *report card* is the table of every expected behaviour and whether the run met it.

**Rename a finished previous round here, and only here.** If a `test-results.md` already exists with `round_status: complete` — or with a `readiness` key and no `round_status`, which is a file written before this protocol — rename it with a date suffix (`test-results-YYYY-MM-DD.md`) now; earlier rounds are history, not waste. Renaming happens once, in this phase, never per scenario. Never write this file over one whose `round_status` is `in-progress`. Keep the check list and the scenarios in memory for now: the round's file is written at the end of Phase 2, once the passing rule is confirmed, so a criterion added or dropped there is never written stale.

If the Requirements predates this format (has "Dimensions that matter" and a prose "Minimum bar" instead of numbered `AC` lines), convert it now with the user: turn each dimension and the "what good looks like" text into numbered yes/no statements, write them back into the Requirements file under `## Acceptance Criteria`, and note the conversion in this run's results.

#### Phase 2 — Confirm the passing rule

Restate it so nobody is surprised later: "The workflow is **ready** when every line of the report card is Met on every scenario. A miss on a **(must)** line always fails the scenario. Any other miss you can either fix or explicitly accept — an accepted miss is recorded, not hidden." Ask whether any criterion should be added or dropped before running. Changes go into the Requirements file, not into this conversation only.

**Now write the round's file — here, and only here.** With the check list settled — including any line just added or dropped — write `outputs/[workflow-name]/test-results.md` with `round_status: in-progress`, no `readiness` key, `criteria_total: 0`, `criteria_met: 0`, an empty `results` map, and two body sections filled in: **Check list** (every `AC`, `R`, `G`, and `Step N output` line) and **Scenarios to run** (each `E` with its input — the file path first, then the short description — its `; tests …` tail, and its Golden Example if it has one). That file is what each run chat appends to.

#### Phase 3 — Smoke run

One scenario, logic only. Before the full round, walk one scenario mentally against the built skill's text — read the orchestrator and check that each Requirements step, rule, and gate is actually represented. This catches obvious gaps (a missing gate, an unreferenced context file) before the user spends a run on them. It is not a graded run.

While reading the orchestrator, confirm it ends every run with the closing **What I did** summary — the steps it took in order, each gate where it paused and what was decided there, each tool action, and where the deliverable is. That list is the evidence Phase 5 quotes for the path lines. If it is missing, say so now, expect the path lines to lean on the transcript instead, and offer to send the user back to Build to add it.

#### Phase 4 — Integration pre-flight

If the workflow uses no connectors, say so in one line — "Nothing to check here: your workflow connects to nothing" — and move on to the hand-off below.

For each connector the scenarios exercise, confirm the access it needs (read vs. write) is authorized in the account that will run the workflow. If a write path is blocked, do not abort: run everything else and mark the blocked step **simulated** in the report card (`Result: Not run — waiting on [tool] write access`). The round's verdict is then `waiting-on-access`, which is an authorization gap for the user to fix, not a defect to rebuild.

**Live-system caution.** A real run can create real drafts, rows, or events. Prefer a clearly marked test record; after the round, list everything created and where, and offer to remove it (Phase 8).

Close the opener by handing the user the first scenario: read its input from the file path its entry in **Scenarios to run** begins with (or, if the entry has no path, use its text as the input) and paste the file's contents into this chat so they can copy it straight into the new chat, then how to start the workflow in that new chat, and "when it finishes, say *test this* in that chat". If the file holds only a placeholder line naming what to paste, ask for that input now, save it over the placeholder, and then hand it over.

#### Phase 5 — Run and grade each scenario

This phase happens **once per scenario**, in the chat where that scenario ran — or, when that chat cannot reach the results file, in the opener on a run the user pasted back. In a run chat it is the whole of what you do — unless this was the last scenario, in which case Phases 6–8 follow here.

Say where you are grading before you grade, in one sentence: in a run chat, "I can see the run above, so I'll grade it here." In the opener, on a run the user pasted back, "I'll grade the run you pasted."

In a run chat, take the check list, each scenario's input, and its `; tests …` tail from the results file's **Check list** and **Scenarios to run** sections — do not rebuild them from the Requirements. Golden Examples come from the same section.

1. **Identify the scenario.** Work out from the input which of `E1…` this run is. If it is not obvious, ask one question: "Which input was this — E1, E2…?"
2. **Grade first, with evidence.** Decide Met / Not met for every line of the check list and quote the evidence — a count, a phrase, a missing element. Grade the **output checks (`AC…`) first, then the path checks (`R…`, `G…`, `Step N output`)**, all in one table. An output check is proven from the run's final output. A path check is proven from the run's closing **What I did** summary — the steps, the gates and what was decided at each, the tool actions, and where the deliverable is — or, failing that, from the conversation above. A path line that neither one shows is `not-run` with its reason (`not-run — the run shows no tool activity for this step`), never a guess. Where the scenario has a Golden Example, compare against it (missing / extra / substantively different), remembering it is one good answer, not the only one: the question is "would the user send this instead?" Say once, the first time it comes up, that the golden example comparison covers the output only, not the path. Grade every line of the check list on every scenario. The scenario's `; tests …` tail says which lines it was designed to stress — quote it in those lines' Evidence — it is not a filter.
3. **Present the report card** for that scenario — one table, the `AC` rows first, then the path rows:

   | Expected | From | Result | Evidence |
   |---|---|---|---|
   | Every prospect row has contact info | AC1 (must) | Met | 20 of 20 rows |
   | Never includes previously contacted people | R3 | Not met | 2 rows already in the CRM export |
   | Pauses before sending | G1 | Met | What I did: "paused for your approval before sending — you approved 18 of 20" |
   | Step 2 output: ranked list | Step 2 output | Met | 20 rows, ranked best-fit first |

4. **The user confirms or overrides each result.** "I marked R3 Not met because two rows were already contacted — agree?" Record the confirmed result. The user is the judge; the grading is the starting point.
5. Ask one closing question per scenario: "How much would you have to edit this before using it — nothing, a little, or a lot?" Record as `edits: none | minor | major`.
6. **Append, then say what's left.** If `results` already has an entry for this scenario, say so and ask whether to replace it. Append this scenario's confirmed report card to `test-results.md` under **Report card**, its golden example delta under **Golden example deltas** and any `not-run` reasons under **Not run**, and add its entry to the frontmatter `results` map. Leave `round_status`, `readiness`, and the counts alone — the verdict sets those. Then say how many scenarios remain: "2 of 4 graded — run E3 in a new chat next." When that was the last one, go on to Phase 6.

#### Phase 6 — Diagnose every miss

This phase runs after the last scenario is graded, in that chat — or in the opener if the runs were pasted back there, or in whichever chat picks the round up with every scenario graded. If this chat has not already loaded them, the run is over, so read the Workflow node, Design Spec, and Requirements now to name the building blocks — the contamination rule covers only what the chat saw before the run started.

Map each Not met line to the building block that caused it:

| What went wrong | What to change |
|---|---|
| Output is generic or off-brand | **Context** — add examples, style guide, reference material |
| A step was skipped or misunderstood | **Orchestrator skill** — make that step's instruction explicit |
| A step needs expertise the AI doesn't have | **Component skill** — build or extend one for that step |
| Output format is wrong | **Orchestrator skill** — add an explicit format example |
| The AI ignored a reference file | **Context** — check the file is where the skill expects it and is readable |
| A tool call failed | **Connector** — verify the connection independently, then re-run |
| The output looks right but the path was wrong (a gate skipped, a rule broken on the way) | **Orchestrator skill** — make the gate or rule explicit; **Design** if no rule covers it |
| The AI had to make decisions the rules didn't cover | **Design** — the workflow may need an agent, or clearer rules |

If a miss's cause is not obvious from the table, isolate it: run that one building block alone in a fresh chat with the same input and see whether the miss reproduces.

Write the diagnosis as `## Issues identified`, one row per miss: `Scenario | Line | Building block (S1, S2, A1, C3, orchestrator, connector) | What to change`. Build's fix mode reads this table.

#### Phase 7 — Verdict

Set `round_status: complete` in the results file, add the `readiness` key, and fill in `criteria_total` and `criteria_met` from the confirmed results. The round is finished only once those four are written. If the verdict is `Ready`, this round's report card is the **baseline** — the one the file named `test-results.md` carries into Run, and the one Improve later diffs against; it is the round that passed, not the first attempt.

- **Ready** — every line Met on every scenario (accepted misses recorded with the user's reason). Close with: "It's ready. To put it to work, run the `run` skill (Step 6) — 15–20 minutes."
- **Not ready** — at least one unaccepted miss. → `build` skill; it will regenerate only the building blocks named in Issues identified, then come back here and re-run the failed scenarios, then the full set — less than a full build (30–60 min), since fix mode rebuilds only what is named.
- **Waiting on access** — the logic passed but a connector's write access is not authorized. Name the connector and what to authorize. Not a rebuild.

If the Workflow node's `status` is `in-production`, this round is Improve's regression check: close the file as above, then send the user back to the `improve` skill instead of `run` or `build`.

#### Phase 8 — Clean up test records

List every draft, row, message, or event the round created in live systems, with its location, and offer to remove each one.

## Output

The whole round lives in one file: `outputs/[workflow-name]/test-results.md`. The opener writes it at the end of Phase 2, once the passing rule is confirmed; each graded scenario appends to it in Phase 5, and the verdict closes it in Phase 7. It is never renamed part-way through a round — renaming the *previous* round's file happens once, in Phase 1. Once, after the verdict (Phase 7), update the Workflow node (`registry/workflows/<slug>.md`) to link the results under `# Artifacts`, then invoke the `indexing-registry` skill for a maintenance pass (best-effort — a failed refresh never fails this step). No persistent workspace? Tell the user to save the file and re-supply it at the next step.

**Open with YAML frontmatter** so Improve can diff rounds mechanically and Build can detect fix mode:

```yaml
---
workflow: [kebab-case name]
design_spec: outputs/[workflow-name]/design-spec.md
requirements: outputs/[workflow-name]/requirements.md
date: YYYY-MM-DD
environment: "[platform + notable conditions, e.g., Cowork, HubSpot connector live]"
round_status: in-progress   # in-progress from the end of Phase 2; complete only at the verdict
readiness: ready | not-ready | waiting-on-access   # written only when round_status is complete
criteria_total: 10          # countable lines across scenarios run (not-run lines excluded)
criteria_met: 9
results:                    # one entry per graded scenario, appended as each is confirmed
  E1: { AC1: met, AC2: met, R3: not-met, G1: met, "Step 2 output": met, edits: minor }
  E2: { AC1: met, AC2: met, R3: met, R5: not-run, G1: met, "Step 2 output": met, edits: none }
---
```

The opener writes this block with `round_status: in-progress`, no `readiness` key, `criteria_total: 0`, `criteria_met: 0`, and an empty `results` map. Use the real IDs. `results` values are `met`, `not-met`, or `not-run` (a line that could not be exercised — a blocked write, or a path line the run showed no evidence for); `not-run` lines are excluded from `criteria_total` and `criteria_met`, and each one's reason goes in the **Not run** section below, not in the frontmatter. Below the frontmatter:

- **Check list** — every `AC`, `R`, `G`, and `Step N output` line this round grades (written by the opener)
- **Scenarios to run** — each `E` with its input (the file path first, then the short description), its `; tests …` tail, and its Golden Example if it has one (written by the opener)
- **Report card** — one table per scenario, the confirmed results, appended as each scenario is graded
- **Golden example deltas** — per scenario with a golden example: missing / extra / substantively different
- **Not run** — any line simulated or skipped, and why
- **Environment** — which connectors were live vs. simulated
- **Issues identified** — the diagnosis table from Phase 6
- **Accepted misses** — any Not met the user accepted, with the reason
- **Verdict** — Ready / Not ready / Waiting on access, with the count ("11 of 12 lines met across 2 scenarios")
- **Test records created** — and whether they were removed

## Guidelines

- Two to four rounds is normal. Say so before the first round and again after it.
- Never say "eval", "dimension", or "score". Say "check", "line", "met", "not met".
- Keep the user on concrete evidence: "show me the row that's wrong" beats "was it good?"
- Never run a scenario in a chat that has already loaded the requirements, design, or build. Grade it in the chat where it ran, or from a pasted run in the opener — never from the final output alone.
- If the Requirements has no Acceptance Criteria or Example Scenarios, help the user write them now as yes/no lines and 3–5 inputs, write them into the Requirements file, and note the gap.
- **Signpost each phase transition.** Announce each phase in one short line as you reach it ("Phase 5 of 8 — grading E2") so the user always knows where they are.
