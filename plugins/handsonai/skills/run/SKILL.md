---
name: run
description: >
  This skill should be used when the user has built and tested workflow artifacts and is ready to put the
  workflow into production. It guides the first real run, writes the Run Card, and sets up the run log and
  the first review date. Say *log this run* after the first real run finishes in a new chat to check it,
  write the Run Card, and go live; once a workflow is live, *log this run* adds a row to its run log.
  Also use when the user says "continue my workflow" and the Workflow node shows Step 6 (Run) is next. This is Step 6 (Run) of the AI Workflow Framework.
---

# Workflow Run

Put a tested AI workflow into production: do the first real run on real work, then leave a one-page Run Card, a run log, and a review date behind.

**Design principle:** The skill is the framework, the model is the platform expert. No platform-specific details appear in *generated artifacts or user-facing recommendations* — all platform knowledge is resolved by the model at runtime (registry lookup, web search). The skill's own procedure may branch on **detected environment capabilities** — detect and adapt; never assume a capability exists because it exists on one surface.

**Role:** You are an **Agentic AI Architect**. Your role is to get the workflow running on real work and leave the user a Run Card they can follow on any given day.

## Workflow

**Set expectations up front (first message of the opener).** Say: "This takes about 15–20 minutes of framework work, plus one real run of your workflow — however long that normally takes — and about 15 minutes more if it will run on a schedule. You've tested the workflow; now we use it on real work for the first time, in a new chat, exactly the way you'll start it every time. Then I write you a one-page Run Card, start the run log, and set the review date."

### How this step works

Say this to the user, in the opener only, in three sentences, in your own words but with this substance:

1. **Get ready.** In this chat I confirm the test verdict was Ready, check what this run will touch for real, and hand you the exact way to start the workflow.
2. **The first real run.** You open a new chat — the *run chat*, a brand-new chat started where you'll start the workflow every time from now on — and run it there on this week's real work, with this week's real input, or nothing if it pulls its own. When it finishes, say **log this run** — I check the run against your criteria.
3. **Go live.** I write the Run Card, log the run, mark the workflow in production, and set the review date — and, only if it was designed to run without you, set up the schedule.

**Which chat you are in — you work this out, you never ask.** If this chat already contains a workflow run above the invocation, whether it ran here or was pasted in from another chat, go straight to Phase 2; the workflow is the one whose skill ran above. If that is not obvious, look for the `outputs/*/test-results.md` whose frontmatter says `readiness: ready` and whose folder has no `run-guide.md`, and if there is more than one, list them and ask which workflow. Otherwise, settle the workflow first if you do not already know it: resolve it from `registry/workflows/` as Phase 1's resume orientation describes, and if more than one workflow is at this step, list them and ask which one (a question about which workflow, never about which phase). Then take the branch it matches:

- The Workflow node is `in-production` and `outputs/[workflow-name]/run-guide.md` exists, and the user said *log this run* → this is a later run, not the first: add its row to `runs.md` as Phase 4's row rules say (or, where the orchestrator logged it, confirm the row is right), and stop. Nothing else is rewritten.
- The Workflow node is `in-production` and the user did not paste or run a workflow → the workflow is already live; say so, show the Run Card's "How to start it", and if `stale_after` has passed, route to the `improve` skill.
- Otherwise → **opening**, Phase 1.

Never put this choice to the user.

**Where the run is visible — you work this out, you never ask.** After the real run, the check in Phase 2 needs the run itself: the final output, each place the workflow paused and what the user decided, and its closing **What I did** summary. Read the `capabilities.context_location` of the platform this chat is running on — not the Design Spec's platform. Where it says every chat opened in the workspace folder shares the same files, the user says *log this run* in the run chat and you continue there: Phases 2–5 run in that chat, which can reach the workspace. Where it says the workflow's context lives in a project or inside the skill package rather than in a folder every chat shares (or, if the entry has no `capabilities`, its `notes` say so), say this in the opener's hand-off and stop: "When the run finishes, ask the workflow there to put its final output and its What I did summary together in one message, copy that message, paste it into this chat, and say *log this run* under it." If a pasted run has no What I did summary, ask for the final output and every message where the workflow paused and the user decided. Never call the two paths "modes" or offer them as a choice.

**Starting the run.** When you send the user off to the new chat, tell them in one line how to start the workflow there: the exact phrase or click from the platform's `capabilities.skill_install` (or, if the entry has no `capabilities`, its `notes`) and the spec's Deployment Plan entry point — for a `Skill` mechanism the orchestrator skill named after the workflow; for an `Agent` mechanism the orchestrator skill Build created on a platform where the primary session orchestrates, or the configured agent (a Workspace Agent, a Copilot agent) where the platform's `capabilities.custom_agents` says agents are a separate thing to open. Say where to open the new chat, from `capabilities.context_location`: in the same workspace folder on a platform where chats share one, or inside the project that holds the workflow's context files. Say **not as a test run** when Test's results or the orchestrator show it has a test-run mode — the real run writes its real output and its own log row. Say it once, in the opener's hand-off.

**The platform.** The workflow runs on the platform the Design Spec's `platform:` names; that is the platform whose `capabilities` the Run Card quotes. If this chat is on a different platform, say so and ask once which platform the workflow runs on. If the answer differs from the spec, the workflow must have been tested where it runs: read the results file's `environment:` field. If it names the platform the user just named, continue, quote that platform's `capabilities` everywhere below, and record the change in one line under **Your first real run** on the Run Card ("Designed for Cowork; runs on Claude Chat since [date]"). If it does not, say in two sentences that the workflow was built and tested for a different platform than it now runs on, and route to the `build` skill to regenerate it for the new platform, then Test — do not go live on a platform the round never ran on. If the platform has no registry entry at all, say its instructions are unverified, take them from the framework's install page (https://handsonai.info/ai-workflow-framework/skills/) plus one web check, and mark them as such on the Run Card.

**Is it installed?** On a platform whose skills are folders in the workspace, check the path `capabilities.skill_install` names; on a platform whose skill directory is system-managed (Cowork, Claude Chat, ChatGPT), the workspace cannot show it, so ask once, in the opener, one question that names every skill and agent the Workflow node links and every connector the Design Spec's Integration Options names: "Are the [skill and agent names] installed, unchanged since you installed them, and [connector names] authorized, in the account that will run it?" — this is the one question about setup the "you never ask" rules above do not cover; never split it into several. If a skill or agent is missing, stop and route the user back to Build's install step; nothing else in this skill works until it is. If a skill was edited after it was installed, the installed copy is stale — repackage and reinstall before the real run. If a connector is not authorized, the user authorizes it now, in that account, before the run.

#### Phase 1 — Load context

> **Registry entry:** the workflow's registry entry is its Workflow concept node in the workspace's `registry/` bundle — see `indexing-registry/references/registry-bundle.md` (in this plugin) for resolution, write rules, and your fields. If the workspace has no `registry/SCHEMA.md`, offer the `scaffolding-registry` skill first (it also migrates legacy `workflow.yaml` workspaces); do not write registry entries until the bundle exists.

> **Platform registry:** platform facts (how a skill is installed, where context lives, scheduling, agents) come from the platform registry. Read it from `references/platform-registry.json` in this skill's own folder; if that file isn't there, from `registries/platform-registry.json` at the plugin root; if neither exists, fetch `https://raw.githubusercontent.com/jamesgray-ai/handsonai/main/plugins/handsonai/registries/platform-registry.json`. Read it once per session and reuse it.

This is the opener. Read the Workflow node (`registry/workflows/<slug>.md`), then the Design Spec and the Workflow Requirements it links, the artifacts and skills linked under `# Artifacts` / `# Skills` / `# Agents` (the paths from Build Phase 10, the reconciliation table), and `outputs/[workflow-name]/test-results.md`. **Resume orientation:** if the user arrived via "continue my workflow" or with no stated workflow, check `registry/workflows/` for existing Workflow nodes (if several, list them), infer progress from what each node already links — its `# Artifacts` labels, plus its `# Skills` / `# Agents` links for Step 4 — and if Run isn't the next step, say so and route to the right skill.

**The Ready gate.** Run goes ahead only on a finished round whose verdict is Ready. Read the results file's frontmatter and take the one branch it matches — say which, in one sentence, then stop if it is not the last:

- No `test-results.md` → "This workflow hasn't been tested yet" → the `test` skill.
- `round_status: in-progress` → "Your test round isn't finished — N of M inputs graded" → the `test` skill, which resumes the round.
- `readiness: not-ready` → the `build` skill, in fix mode: it regenerates only the building blocks named under Issues identified, then Test runs a new round.
- `readiness: waiting-on-access` → the `build` skill, to authorize the named connector in the account that will run the workflow; Build sends the user back to Test.
- `readiness: ready` → continue. This round's report card is the baseline Improve diffs against; say so in passing.

Then read the Workflow node's `status`: `under-development` is expected. `in-production` is handled by the "Which chat you are in" rules above. Anything earlier (`backlog`) means a step was skipped — say which artifact is missing and route there.

Read the platform's `capabilities.skill_install`, `capabilities.context_location`, and `capabilities.unattended_runs` (or, if the entry has no `capabilities`, its `skill` documentation URL(s) and `notes`) — every concrete instruction below comes from there, never from this file.

**Guided-mode platforms** (spec `platform_mode: guided` with GUI instruction documents instead of files): the Run Card still has the same six headings; "How to start it" points at the configured agent or skill in the platform UI and the instruction documents Build produced.

**This run is real — say what it touches.** Test ran on test inputs, often in a test-run mode that saved under `test-runs/` and wrote nothing real. The first real run does what the workflow was designed to do, for real, including every write. From the Design Spec's Safety & Permissions section, Integration Options, and Deployment Plan, list in plain words everything the run will write or send — a file saved, a draft created, a row added, an email sent, a calendar event made — one line each, and which human gate stands in front of each. If the workflow writes nothing beyond its own output file and log row, the list is those two lines, with the contrast made explicit: "Unlike the test runs, this one saves the real report to [path] and adds a row to the run log — nothing else." On a platform where the run chat cannot write files (context lives in a project), say instead that the workflow prints its output and its log row at the end for the user to save, and where. Either way, end with: "Once you approve at the gate, that happens for real — this is the week's actual work, not a rehearsal." Then say, as a statement not a question, whether the user needs this week's real input in hand or the workflow pulls it itself (the Requirements' Step 1 says which).

**Scheduling is never part of the first run.** Even for an `automated` workflow, the first real run is started by hand with the user watching; the schedule is set up in Phase 5, after the Run Card exists.

Close the opener — after the install question is answered, never before — by handing over, in this order: where to open the new chat, the exact start phrase (not as a test run), what to give it (the real input, or nothing if it pulls its own), and "when it finishes, say *log this run*" — in the run chat, or, on a platform whose chats don't share files, with the run pasted back here, as "Where the run is visible" says.

#### Phase 2 — The first real run

This phase happens in the chat where the run is visible — the run chat, or the opener with the run pasted back. In a run chat, re-read Phase 1's sources (the node, Requirements, Design Spec, results file, platform registry) silently — this chat has no memory of the opener — and do not narrate Phase 1 again. Say where you are checking before you check, in one sentence: "I can see the run above, so I'll check it here" or "I'll check the run you pasted."

Take the check list from `test-results.md`'s **Check list** section — do not rebuild it from the Requirements. Check, with evidence quoted the way Test does (a count, a phrase, a line from the What I did summary):

1. **Every human gate (`G1…`) paused**, and what the user decided there — from the What I did summary. A gate whose trigger did not arise on this input is fine when the summary says so.
2. **Every `(must)` line holds** on the real output.
3. **The output landed where the Design Spec says it lands** (its Deployment Plan) — the saved file, the draft in the right folder, the row in the right sheet. Where the run chat cannot write files, the output was printed under its path and the user confirms they saved it there; that counts as landed. Say "the output" or name the thing — never "the deliverable".
4. **Every connector acted in the account that ran it** — the summary names each tool read or written; a tool the summary says it could not reach is an environment problem (next paragraph).
5. **The log row.** Where `capabilities.context_location` says chats share a workspace folder, the orchestrator was built to append its own row to `outputs/[workflow-name]/runs.md` at the end of every production run — read the file and confirm today's row is there and right. If it is missing, say so: the fix is in the orchestrator skill (add the step back), and Phase 4 writes today's row by hand this once. Where context lives in a project and the orchestrator cannot write files, there is no row to check — the workflow prints its row (or you compose it in Phase 4), and the user keeps the log.

Present the result as one short table — each line, Met or Not met, evidence — and ask the user to confirm or override, as the judge, before going on. Then ask one question: "How much did you edit the output before using it — nothing, a little, or a lot?" and what, in a few words; that is the `Edits needed` cell. If the Requirements' Value & Measurement names a Measure a single run can read (minutes door to door, items processed, drafts sent), ask for this run's reading in the same breath ("and how long did it take, start to finish?"); that is the `Notes` cell, and the one cell of a self-logged row this skill fills in.

**If something failed that Test passed**, it is one of two things, and the rule decides which:

- **The environment** — a connector not authorized in this account, a context file the run could not find, the skill not installed where the run started. The What I did summary or the transcript names a tool or file it could not reach. Fix that with the user (authorize the connector in *that* account, put the file where `capabilities.context_location` says, install the skill), then have them run the same input again in a new chat. Don't rebuild anything.
- **The workflow** — a gate that did not pause, a `(must)` line not met, a rule broken on the way, with the environment intact. Do not go live. Leave the Workflow node as it is, write no Run Card, and send the user to the `test` skill to open a new round on this input: "Test passed this and the real run didn't — that's a defect Test needs on record so Build can fix it. Run the test skill; it will hand this input to Build's fix mode." A miss on a line that is not `(must)` and that the user accepts for a stated reason is the one exception: record it under **Your first real run** on the Run Card, and go on.

The output is real: once the user approved at the gate, it is used as designed — sent, filed, shared. Say that in one line, then go on to Phase 3.

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

Rules for filling it in — each section comes from a named source, never from memory:

- **Your first real run** — Phase 2's result: the input, what the workflow did, where the output went, the user's edits answer. Any accepted miss goes here, with the reason.
- **How to start it** — the start line as "Starting the run" above builds it (platform `capabilities.skill_install` + the spec's Deployment Plan entry point); if this chat is not the opener, build it again from those sources — the run chat has no memory of the opener. Then what to give it. **Teammates:** only when the Requirements or Design Spec says the workflow serves others (a lens of Team or Organization, or a named teammate who will run it): the package Build produced — the path from the Phase 10 reconciliation table or the Deployment Plan — installed the way `capabilities.skill_install` says, in *their* account; every connector in "What to have ready" authorized in their account too; the context files reachable to them; the same start phrase. Otherwise leave teammates out. **Scheduling:** one line, by the node's `execution_mode` — `augmented`: "This runs when you start it. If you later want it on a schedule, come back to this step and we'll set that up." `automated`: the platform's scheduling mechanism in one sentence from `capabilities.unattended_runs`, "set up in the next phase", and the pre-granted permissions and non-interactive credentials it needs — the detail lives in Phase 5.
- **What to have ready** — every connector row and every context row of Build's Phase 10 reconciliation table (location from `capabilities.context_location`), every skill and agent the Workflow node links, and the real input the Requirements' Step 1 names. Say once, on the card, that authorization does not carry over from another project, session, or account.
- **What to check before you act on the output** — every Human Gate `G1…` from the Requirements, in plain words (what it pauses for, what the user is deciding); then every `(must)` line, each in one line; then at most two other lines from the check list most worth a glance (the ones a wrong output would most likely break — Test's Issues identified from earlier rounds, if any, name them). Never more than that: this section is read in the minute before acting, not studied.
- **Log the run** — the path, the five columns, and which of the two logging rules applies (self-logged and verified today, or printed for the user to add). If the Requirements' Value & Measurement names a Measure a single run can read (minutes door to door, items processed, drafts sent), say that the Notes cell carries that reading and that the Baseline, if `Unknown`, becomes readable after the number of runs the Requirements names.
- **Your first review** — the date from the rule in Phase 4, written as a date, with the reason in four words ("monthly, for a weekly workflow"); the exact sentence "Run the improve skill on [workflow name]"; "sooner if the output starts needing more edits"; what to bring: nothing.

Present the Run Card in the conversation as well as saving it. Where this chat cannot write to the workspace, every file you print — here and in Phase 4 — starts with the line "Save this as `[path]`" above the fence, so the user never has to ask where it goes; Phase 4 still ends with the full list.

#### Phase 4 — Run log, registry, review date

**The run log.** Create `outputs/[workflow-name]/runs.md` with the header row and add today's first real run as row one — unless the orchestrator already appended it during Phase 2, in which case check the row against the rules below and fill the `Notes` cell it left for the user (the Measure reading from Phase 2); change nothing else in a row the orchestrator wrote:

```markdown
| Date | Input / trigger | Result | Edits needed | Notes |
|---|---|---|---|---|
```

Row rules, every row: **Date** today, `YYYY-MM-DD`. **Input / trigger** — what started it and what it was given, in five words or fewer ("Manual, Friday run"; "Scheduled, Monday 8am"; "Pasted brief, Acme renewal"). **Result** — where the deliverable landed ("Report saved"; "Draft in Gmail"; "3 rows added"); a run that stopped at a gate without finishing says so ("Stopped at G1 — not approved"). **Edits needed** — the user's answer from Phase 2, `None` or what changed in a few words. **Notes** — the Measure reading when a single run can read it (minutes door to door, counts), else anything the user wants their future self to know, else empty. Where the orchestrator cannot write files (context lives in a project), print the row and tell the user to add it to `runs.md` in their workspace; the Run Card already says so.

**The review date.** Set it by the Workflow node's `trigger` and `execution_mode`, then confirm it with the user as a date, not a cadence: the workflow runs weekly or more often → one month from today; less often than weekly → three months from today; `automated`, whatever the cadence → one month from today, because nobody is watching the runs. If the `trigger` names a run day (Fridays, the first of the month), move the date back to the last run day on or before it, so the review falls on a day the workflow runs; say the date and the reason in one line ("2026-07-10 — a month out, on a Friday"). Tell the user to put the date in their calendar now, with the sentence "Run the improve skill on [workflow name]" as the event title. Where the platform's `capabilities.unattended_runs` says scheduled tasks or reminders exist, also offer to set a one-time reminder for that date — an offer, not a default.

**The Workflow node.** Once the date is agreed, in the same session as the run — never leave it for later, because a log with rows and a node that is not `in-production` fails lint — update the node: `status: in-production`, `stale_after: YYYY-MM-DD` (the date just agreed), restamp `generated: { by: process:run, at: <today> }`, and add `- [Run guide](outputs/[workflow-name]/run-guide.md)` and `- [Run log](outputs/[workflow-name]/runs.md)` under `# Artifacts`, after the Test results link. Touch nothing else on the node. Then invoke the `indexing-registry` skill for a maintenance pass (best-effort — a failed refresh never fails this step). No persistent workspace? Print the Run Card, the run log, and the updated node in full, each under its path, and tell the user to save all three into their workspace.

If the node's `execution_mode` is `augmented`, go to the close. If it is `automated`, continue to Phase 5.

#### Phase 5 — Put it on a schedule

Only when the Workflow node's `execution_mode` is `automated`. For an `augmented` workflow this phase is skipped silently — the Run Card's one line already covers it, and the user never hears "Phase 5 does not apply". If the user asks for a schedule on an `augmented` workflow, say in two sentences that scheduling removes the person the design assumed would be there at its gates, and that the route is Design (re-decide the involvement mode), not this step.

Read the platform's `capabilities.unattended_runs` (or, if the entry has no `capabilities`, its `notes`):

- If it says unattended runs are not supported, say so in one line and name the platforms whose entries say they are — do not improvise a workaround, and do not suggest leaving a chat open. The Run Card's scheduling line then says the same.
- If it is supported, read the condition it states about where context must live (a remote schedule may not reach local files) and check the workflow's context rows from Phase 3 against it; a workflow whose context the schedule cannot reach is not schedulable as built — say what has to move (into the package, into a connected source) and route to Build for that change before scheduling.

Then walk the setup, from the capability entry: the mechanism, the cadence (from the node's `trigger`), and the pre-granted permissions and non-interactive credentials it needs — every connector authorized in the account that owns the schedule, before the first scheduled run. Before enabling it, go through the **safety checklist** from the spec's Safety & Permissions section in plain words, each as a yes/no the user answers from the deployed artifacts, not from the spec:

1. Least-privilege scopes — the schedule's account has only the access the workflow actually uses, nothing broader.
2. Human gates and draft-don't-send are enforced in the installed artifacts — the workflow stops or drafts where the design says, without a person present to stop it.
3. Content the user didn't author (inbound email, web pages, form submissions) is treated as data, never as instructions — the orchestrator says so.
4. A cap on actions per run — a number, written in the orchestrator.
5. Every write is visible in the run log.

A "no" on any line means do not enable the schedule yet: name the artifact that needs the change and route to Build. With five yeses, enable it, and tell the user the first scheduled run becomes row two in the run log — ask them to open the log after it fires and check the row is there, because that is the first run nobody watched.

## Outputs

- `outputs/[workflow-name]/run-guide.md` — the Run Card (six fixed headings above).
- `outputs/[workflow-name]/runs.md` — the run log, one line per run.
- Workflow node updated: `status: in-production`, `stale_after`, artifact links, `generated` restamped.

## Guidelines

- Plain language; every concrete instruction comes from the platform's `capabilities`, never from memory of a platform's UI — verify with one web check if a capability value looks stale.
- Never say "deploy", "production environment", "orchestrator artifact", "non-interactive credentials", or "deliverable" to the user (naming the spec's Deployment Plan section is fine). Say "go live", "the account that runs it", "the workflow's skill", "permissions granted in advance".
- Close with the inventory of everything produced across Steps 3–6 (Design Spec, built skills/agents, test results, Run Card, run log) and the review date, then: "When [date] arrives — or sooner if the output starts needing more edits — start a new conversation and say: *Run the improve skill on [workflow name]* — a review takes 30–45 minutes."
- For organizational workflows, after the summary offer the `writing-workflow-sops` skill to document the workflow as an SOP for the team.
- **Signpost each phase transition.** Announce each phase in one short line as you reach it ("Phase 3 of 5 — writing the Run Card") so the user always knows where they are. Keep one running count the user hears; a phase that does not apply is skipped silently.
