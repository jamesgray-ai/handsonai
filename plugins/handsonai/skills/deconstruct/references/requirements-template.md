# Workflow Requirements: the drafts and the file

Read at entry, with the other files every interview needs (`saving-the-requirements.md`, its first paragraph), never between the leader's lines: it serves every draft and the file write from that one read. Lines marked *held* are said word for word; the rest is your own wording (`SKILL.md` rule 18). The file's format is fixed: later steps and scripts parse it.

## Contents

1. The drafts: what goes in each
2. Which security categories are worked
3. Standing rules
4. The summary
5. Writing the file: style
6. The file: frontmatter, sections and line formats
7. `inputs/`, `context/` and `history/`
8. The self-check

## 1. The drafts: what goes in each

Each is short, plays its items back in plain words (never IDs or the file's line format), and marks your suggestions in italics, said once at its top in the first person ("My suggestions are in italics; your own words are plain." *(your words)*, `SKILL.md` rule 6). The goal and output and the checks are drafted as `interview.md` says (parts 1 and 2).

**What it works from** (part 4).
- The sources it uses, introduced the first time with what **context** means in one plain line (any information it needs to do its job, such as documents, spreadsheets, emails, style guides, or knowledge in someone's head). For each: what it is, where it lives, and whether it exists or needs creating. A step's existing prompt or instructions count as a source. Content nobody on the team wrote that a step reads on each run (inbound emails, form submissions, web pages) gets its own `External` row as well as its Inputs line. For sources that trip no privacy test, draft whether the AI can reach them, as your suggestion. What a source holds and who wrote it are played back only as the leader said them; where they haven't, say it's not known yet, never a guess (SKILL.md rule 13).
- The Inputs drafted from the trigger and the checks, each with where it comes from and whether it exists yet; then the one question of where they live and whether the workflow reaches them there or the leader pastes them.

**The rules** (drafted in part 2, settled in part 5). Drafted from everything said so far, in the "When… it…" shape: what it always and never does (a prohibition the leader volunteered, an order the leader insisted on, and what you drafted from the goal and checks), what's in and what's out, any tone, format or length rule, and, when it runs without the leader, the Fallback. Offer matching standing rules and rules from the leader's other workflows or a policy document they named (section 3). A rule the leader gave stays a rule, never a step ("no shellfish"). Constraints about data and authority go to Security. A checkpoint isn't a prohibition: "never send without approval" is a checkpoint (part 6); "never send" is a prohibited action, offered in Security's Prohibited actions. An "It never…" that restates an "It always…" isn't added, and a step's own action isn't restated as a rule. Also in this draft:
- **When it runs without the leader,** the Fallback's conditions and where flags go:
  - **The Fallback's conditions:** when "it can't confidently handle it", proposed from the tricky case and the out-of-bounds rule, as your suggestion.
  - **Where flags go, when `Runs: without you`:** the Fallback proposes "…it does its best and flags it in [an email / a chat message] to you", as your suggestion: an email by default, a chat message only when the leader has named the chat tool they use (named as they named it). The leader keeps, changes or drops it. Kept, it's also a W line, `- W[n] · [email / chat] to you · send a flag · after each run`. Dropped, the flag stays in the end-of-run message.
- **An alternative output** for a case that's out of bounds: a `When` rule in the leader's words, "When [the case is out of bounds], it doesn't [produce the deliverable] and [does what instead]". The main output stays the one deliverable.
- **A policy removal:** a `When` rule with its role tag, "When [source] arrives, [role] removes [those details] before the AI sees it." (`interview.md`, *4. What it works from*).
- **A write whose place isn't known** and that no list has named: shown as "[place] not known yet".

Ends "What would you change or add?"

**The security limits** (part 5, after the rules in the same message; every workflow; the categories are in section 2). Work out the tripped tests and categories from the Context Inventory as corrected. Any line giving the reason for them names only what the leader said (for illustration only; use the leader's own words: "since you said your intake forms hold patients' health details"), never that a source holds confidential details they didn't mention, and never anything they said is made up. Then play back each constraint in plain words under its category, never by its `P` ID (where data may go, who sees it, what it must never do, what gets recorded), kept or dropped like the other drafts (a loosening is re-asked, `SKILL.md` rule 7). Offer matching standing limits (section 3). A prohibition already in the rules draft isn't repeated. A trace record says where it's kept, never inside the deliverable (for an invoice summary, for illustration only: "Each summary is logged with the invoice it came from, outside the summary itself."; write the leader's own version). A write whose place isn't known yet, and that the rules draft didn't name, is shown here as "[place] not known yet". Ends "What would you change or add?"

**The checkpoints** (part 6) and **the practice runs** (part 7) are played back as `interview.md` says. Offer matching standing checkpoints (section 3) in part 6.

## 2. Which security categories are worked

Derived from the Context Inventory and the writes, never asked again:
- any `Confidential` or `Regulated` row: it handles data the leader wouldn't want outside the company;
- any `External` row: it reads content nobody on the team wrote;
- any write, or `Runs: without you`: it writes to a live system.

Each tripped test works its categories, once each even when two tests point at the same one:

| What tripped | Categories to work |
|---|---|
| Writes to a live system | **Prohibited actions** (what it must never do, whoever asks) and **Traceability** (what has to be recorded, so a run can be reconstructed) |
| An `External` row | **Boundaries** (where that content may travel) and **Prohibited actions** (what it may never be allowed to trigger) |
| A `Confidential` row | **Boundaries** and **Access** (who may see the outputs and anything in between) |
| A `Regulated` row | Boundaries and Access, with the `Governing regime:` line naming the regime, or `Not sure — to check` |
| None of these | **Prohibited actions** alone |

With nothing tripped, `### Prohibited actions` holds the lines the leader kept, each with its Source and its `P` ID (`P1` for the first), and the section opens "No sensitivity constraints beyond the prohibition(s) below — personal data only, read-only, human-triggered." Only when the leader dropped every line does it take the one-line form: "No sensitivity constraints — personal data only, read-only, human-triggered." When a test tripped and the leader dropped every line of one of its categories, that category is written as its heading and an empty table (`| ID | Constraint | Source |` and its separator row): later steps read it as answered, never as missing. A prohibition the leader stated is always written down, unless they take it back themselves.

## 3. Standing rules

`standing-rules.md` in the framework folder holds the rules a leader keeps for every workflow: tone and voice, who approves what, data that's never shared, systems that are never touched.

**Proposing them.** In the rules draft and the security limits, offer matching lines from: `standing-rules.md`; the rules, checkpoints and security limits of the leader's other workflows in the registry; context files, and any policy document the leader named (an AI policy, a brand guide). Each is your suggestion, with its source in plain words ("from your standing rules", "as in your Client Follow-Up workflow", "from your AI policy") and needs a keep or drop. Offer only lines that fit this workflow. A kept line is copied into this workflow's requirements as an R or G line (or a security constraint), so each workflow's requirements stay its own source of truth. A first-time leader with none of these sees nothing extra.

**Keeping them.** Once the rules, checkpoints and security limits are settled (after the security limits), and only when at least one kept line looks like one the leader would want everywhere and isn't already a standing rule, ask in its own message. Ask it only from the leader's second workflow: another workflow's folder (not this one's) holding more than a progress file, or another node past `backlog`, not counting running work. In your own words, name the rules and ask whether to keep them as standing rules, suggested for their next workflows too; say that each workflow keeps its own copy, so changing one later doesn't touch workflows already built; if not sure, say no for now, and it's asked again next time.

The lines kept are written to `standing-rules.md` at the close (Phase 3); create the file the first time:

```markdown
# Standing rules

Rules you keep for every workflow. Deconstruct suggests the ones that fit each new workflow, and each workflow's requirements keep their own copy.

- It never shares client data outside the company. · rule · from weekly-status-report, 2026-10-18
- When a draft goes to a client, it stops until you approve it. · checkpoint · from client-follow-up, 2026-10-20
```

Each line is in the "When… it…" shape, with its kind (`rule` or `checkpoint`), the workflow it came from and the date. The leader may edit or remove lines directly, or ask you to; never change or remove a standing rule on your own. A changed standing rule applies to new workflows only; an existing workflow changes through "change my workflow".

## 4. The summary

Always, in its own message (`interview.md`, *8. The defaults and the summary*), after the defaults and before anything is written; never skipped. On one screen, in plain words, never IDs: the goal; the output and its structure; why it matters (the registry goal and one measure, your suggestion); the checks, each with where its information comes from; the rules and the safety limits (a rule tagged ` · (you)` that says the same as a checkpoint, such as "you send it yourself" beside "it stops until you approve the draft", is shown once, as the checkpoint, never twice); the policy answer, when asked, on its own line (never as a rule); the checkpoints; the practice runs; open items, each with who and when. Then how readiness works, said once, and the go-ahead, both as `interview.md` gives them.

Before it, trace every check's source in the draft (each `from:` names an input, a source or a rule in the draft, or the draft alone); a check whose information nothing supplies is listed as an open item, never saved with a guessed source. A test that trips here brings its limits first.

Everything the save needs is read at entry (`saving-the-requirements.md`, first paragraph), so the go-ahead's turn holds only writes; only a file that shows up later is read in the summary's turn, with no text.

**On a re-run or a redo,** a 10.x file is converted as `re-runs.md` says, and what changed is in the summary for correction.

## 5. Writing the file: style

The file reads like a requirements document, not an interview transcript:
- **Requirements voice:** every line states what must be true, not what the leader said: (for illustration only) "Output is a Markdown table with one row per open invoice", not "The user mentioned a table."
- **Active voice, present tense:** "Validate the input against the rubric."
- **One requirement per line;** lists, not paragraphs, wherever several requirements appear.
- **Concrete over abstract:** name the document, the field, the threshold: "Reject submissions over 500 words."
- **No interview residue:** no hedges ("I think", "usually"), narrative connectors ("then the user") or commentary ("we discussed").
- **Self-contained:** a reader who never saw the conversation can work from it.
- **Markdown hygiene:** no bare `~` for "about" (two in a paragraph render as strikethrough).

**Machine-readable:** the fixed headings in the fixed order; tables for lists of items with shared fields (context, practice inputs, rules, checkpoints, security constraints); list lines for steps, decisions, inputs and writes; the canonical values (Lens `Individual` or `Organizational`; Context Status `Exists` or `Needs Creation`; Sensitivity `Public`, `Internal`, `Confidential` or `Regulated`; Provenance `Authored` or `External`; AI Accessible `Yes`, `Partial` or `No`; Inputs Status `available`, `not available yet` or `Not sure — to check`; `settled by:` `a rule on a value`, `your criteria` or `open judgment`); every step line names what it produces, with `uses` and `writes` tags whenever the step reads context or writes outside.

## 6. The file: frontmatter, sections and line formats

`requirements.md` in the workflow folder. Frontmatter, then the title, then exactly these twelve `##` sections, named exactly, in this order, and no others. (A 10.x file has no `## Output` and is still read; Deconstruct converts it on its next save, `re-runs.md`.)

**Frontmatter:**

```yaml
---
revision: 2
track: full
revisions:
  - revision: 2
    by: deconstruct
    lines: [AC3, R2]
---
```

- **`revision`:** 1 on the first save; raised by one when a re-run or a redo changes a line (not when only practice inputs change).
- **`revisions`:** `[]` at revision 1, then one entry per revision: `revision`, `by` (`deconstruct`, `design` or `test`) and `lines` (the IDs added, changed or removed); Test adds `plan_unaffected: true` to its own entries. Keep every entry other steps wrote.
- **`track`:** `light` or `full`.
- **`big_change`:** never in a file Deconstruct saves (Design writes it with no registry while a redo is pending; the redo's saved file leaves it out).

````markdown
# [Workflow Name] — Workflow Requirements

## Goal
For each [trigger], a [deliverable] for [who], so [purpose].

## Output

What: [the deliverable]
For: [who receives or acts on it]
Form: [its form: length, format and any fixed parts, such as a subject line]
Voice: [whose voice, and the source that sets it, if any]
Structure:
    [a short Markdown skeleton of the deliverable, drafted from the checks]
Delivered as: set in Design

## Value & Measurement

| Field | Value |
|---|---|
| Business Objective | [which strategic objective this supports] |
| Desired Outcome | [what changes, and for whom] |
| Measure | [what gets counted] |
| Baseline | [today's number] · Measured / Estimated / Unknown (with no number: `— · Unknown`) |
| Target | [what it should achieve once running, or "—"] |

## Metadata

| Field | Value |
|---|---|
| Workflow Name | [name] |
| Description | [the one-sentence description] |
| Trigger | [what kicks it off] |
| Starts | [optional: you / you, when [event] / schedule: [when] / event: [event] · checked [interval / as often as it can]] |
| Per run | [optional, inferred: one [case] / a batch of [cases]] |
| Owner | [person or role] |
| Lens | Individual / Organizational |
| Stakeholders | [roles or teams; Organizational lens only] |
| Runs today | [running work brought in only: by hand; or set up as [a skill, an agent, an automation] in [where]; on a schedule or not. Or, at cold entry, what the leader said about the one that already runs, in their words, ending `· where: not asked`] |
| Remembers | [optional: nothing / [what] / not sure] |

## Path

Method preference: AI works it out each time
Path: none — the AI plans each run from the goal

(Every file this interview writes has this form, with no `### Decisions`: no question in this interview captures a decision line, and a decision the law gives a person is a checkpoint. An older file with steps, kept on a re-run, may have step lines, `### Decisions` and `### Step N` blocks: *Line formats*, `## Path`, below.)

## Inputs

- I1 · [what comes in] · from [source or C#] · Status: available

## Context Inventory
*The sources it uses, what we call its context.*

| ID | Artifact | Used By | Status | Sensitivity | Provenance | AI Accessible | Location / Source | Key Contents |
|---|---|---|---|---|---|---|---|---|
| C1 | [name] | [All, or —; in an older file with steps, Step N or the AI's part after Step N] | Exists / Needs Creation | Public / Internal / Confidential / Regulated | Authored / External | Yes / Partial / No | [`context/C1-[short-name].md`, a system or a URL, or "Create as `context/C1-[short-name].md` · by [who], [when]"] | [what's in it] |

## Acceptance Criteria

Each line is one thing a single run's output either does or doesn't do. Every practice run is checked against every line.

1. **AC1** — [yes-or-no statement] · from: [I#, C#, R# it needs, or "the output alone"]
2. **AC2** — [yes-or-no statement] · from: [I#, C#, R#, or "the output alone"]

Reference example: [C# of the real output, or "—"]

## Example Scenarios
*The practice runs: each input it's tested on, and what should happen.*

| ID | Scenario | Input | What to look for in the output | Golden Example |
|---|---|---|---|---|
| E1 | [short name] (real) | `inputs/E1-[short-name].md` — [description] | [the input's `expect:` line, word for word] | [C#, or "—"] |
| E2 | [short name] (made up) | Test writes it — [what the input holds] | [what should happen, in plain words] | — |

Every check is required: there are no must-haves, and `(must)` is never written. A form item (a subject line, a length) is in `## Output`, not a check. Each check's `from:` names where its information comes from; a check whose information nothing supplies is an open item in the summary, never saved with a guessed source. A scenario is `(real)` only when the leader gave a real input; otherwise `(made up)` and `Test writes it`.

## Rules & Constraints
*Its rules: what it always does, never does, and does when something happens.*

| ID | Kind | Rule |
|---|---|---|
| R1 | Always | It always [does that]. |
| R2 | Never | It never [does that]. |
| R3 | When | When [this happens], it [does that]. |
| R4 | When | When [the input is missing something it needs], it asks you for it before [producing the deliverable]. |
| R5 | Fallback | When [the conditions it can't confidently handle], it [stops and asks you / does its best and flags it[ in an email / a chat message] to you / skips that item]. |
| R6 | When | When [the case is out of bounds], it doesn't [produce the deliverable] and [does what instead]. |

## Human Gates
*The checkpoints: where a person checks or approves the work.*

Runs: with you

| ID | Where | Checkpoint |
|---|---|---|
| G1 | After the draft is ready | When the draft is ready, it stops until you approve it. · (you) |

## Security, Privacy & Safety

*Scope: [which tests apply: writes to a live system / reads content nobody on the team wrote / handles data you'd be uncomfortable seeing outside the company]*

### Boundaries
| ID | Constraint | Source |
|---|---|---|
| P1 | [where data may and may not travel] | [person, policy, control ID, or `Self`] |

### Access
| ID | Constraint | Source |
|---|---|---|
| P2 | [who may see the outputs and anything in between] | [...] |

### Traceability
| ID | Constraint | Source |
|---|---|---|
| P3 | [what must be recorded, and for whom] | [...] |

### Prohibited actions
| ID | Constraint | Source |
|---|---|---|
| P4 | It never [acts], whoever asks. | [...] |

Governing regime: [name] | None | Not sure — to check
Policy check: Allowed | No — [source] left out | No — details removed first (R[n]) | No — not live until approved | Not sure — to check

### Writes
- W1 · [system] [place, as the leader named it] · [action] · after [moment]
- W2 · [email / chat] to you · send a flag · after each run
````

**Line formats:**
- **Step line:** `- Step 3 — Draft brief · produces a one-page brief · uses C2, C4 · fixed (regulation | policy | your judgment) | flexible · writes W1 · (you) | (finance team) · parallel with Step 2 · proposed by AI`. The name, `produces` and the fixed-or-flexible mark are required, also on a step a person does (the role tag never replaces the mark). Every other tag is optional, left out when it doesn't apply, and in this order. The role tag means a person still performs the step; `· parallel with` only when the leader said two steps don't depend on each other; `· proposed by AI` marks a step you added that the leader hasn't fixed.
- **`## Path`, in order:** the `Method preference:` line, always first; `Path: proposed by AI` (only when you proposed the whole path) or `Path: none — the AI plans each run from the goal` (no step lines); the step lines, with `- The AI plans this part` where the AI plans (not a step: no number, no `produces`, no mark, never counted); `### Decisions`, left out when there are none; then a `### Step N — [Name]` detail block for each step that carries detail, one bold-labelled line per field that applies (what it uses stays on the step line).
- **Decision line:** `- D1 (Step 3): When [condition], it [path] · settled by: a rule on a value | your criteria | open judgment · criteria: [the leader's words] · value read by AI`. `· criteria:` whenever the leader gave criteria, after any of the three `settled by:` values, with no " · " inside its text (reword it if it would hold one); `· value read by AI` last, only when the AI reads the value. With no steps, `- D1: When …`.
- **Metadata's rows,** in this one order: Workflow Name, Description, Trigger, Starts, Per run, Owner, Lens, Stakeholders, Runs today, Remembers. The optional ones, each left out when it doesn't apply (old files without them pass):
  - `Starts`: `you`, `you, when [event]`, `schedule: [when]` or `event: [event] · checked [interval | as often as it can]`;
  - `Per run`: `one [case]` or `a batch of [cases]`, inferred, left out when it can't be told;
  - `Runs today`: running work brought in, or what the leader said at cold entry about a version that already runs (`· where: not asked` at its end, `choosing-a-workflow.md`);
  - `Remembers`: `nothing`, `[what]` or `not sure`;
  - `Stakeholders`: Organizational lens only.
- **The glosses:** one italic line of fixed text right under four headings, `## Context Inventory`, `## Example Scenarios`, `## Rules & Constraints` and `## Human Gates`, word for word as the template shows them, written on every file Deconstruct saves.
- **Input line:** `- I1 · [what] · from [source or C#] · Status: available | not available yet | Not sure — to check`, with the route where there is one (for illustration only: "from C1, through the [storage service] connection"). Inputs' Status is about what comes in on each run; the Context Inventory's Status is about reference material; a run input that doesn't exist yet is recorded in Inputs only.
- **Writes** under `### Writes`: `- W1 · [system] · [action] · Step 3`, or `· after [moment]` with no steps. A write's place sits inside `[system]`: `[system] [place, as the leader named it]`, or `[system] ([place] to confirm)` when it isn't known; there's no fifth field. A flag sent to the leader after each run is `- W[n] · [email / chat] to you · send a flag · after each run`, allowed with steps (that exact phrase only). With nothing written, the heading stays, with the line `None`.
- **Policy check:** one optional line, once, right after `Governing regime:` and before `### Writes`, with one of five values: `Allowed`; `No — [source] left out`; `No — details removed first (Step [N])`, or `(R[n])` for a `When` rule, written as `(Step 2)` or `(R4)` and naming a step or rule in this file (filled from the final numbering); `No — not live until approved`; `Not sure — to check`. No line means the question wasn't asked. A removal step or rule also has a Boundaries P line: [source] reaches the AI only after that step or rule.
- **Rules:** each in the "When… it…" shape, in the leader's words where they gave them; `Kind` is `Always`, `Never`, `When` or `Fallback`. The Fallback carries the conditions it can't confidently handle and, when it runs without the leader, where flags go. An out-of-bounds case's alternative output is a `When` rule. A rule a person carries out ends with its role tag (`· (you)` or `· ([role])`) and isn't graded on the output. A `Never` rule with no role tag, like every Prohibited-actions P line, can never be accepted as a miss when it's tested; no marker records it. Rules are behavioural ("It never invents a figure"); a prohibition on acting ("It never emails a customer") is a prohibited action in Security. A "stop and ask" Fallback also has a checkpoint.
- **Human Gates:** the first line is `Runs: with you` or `Runs: without you`. Each checkpoint is in the shape "When [this happens], it [stops / waits] …", names who performs it, and ends with the role tag: "When the draft is ready, it waits for you to read and edit it before you send it. · (you)", never "When the draft is ready, you read and edit it…" (the validator rejects a checkpoint whose second half doesn't start with "it"). With none, under the `Runs:` line: "No human gates — the workflow runs end-to-end with final review only."
- **Security:** every constraint has a `P` ID, numbered in one series across the four tables in the order they're written (only the categories that were worked appear), and a Source (`Self` when the leader is the source). Design and Test name a constraint by its ID, never by copying its words. Prohibited actions are absolute; checkpoints are conditional (if an approval can satisfy it, it's a checkpoint). The sensitivity of what the workflow produces belongs in Access. `Governing regime:` and `### Writes` appear in both the full and the one-line form.
- **Context Inventory:** a `Needs Creation` item's location is where it will be created (`context/…`). On the Organizational lens, existing process documents (SOPs, training guides, compliance requirements, service levels) are included.

**Labels:** steps `Step 1`, `Step 2`…; decisions `D1`… (linked to their step when there is one); inputs `I1`…; writes `W1`…; context `C1`…; practice inputs `E1`…; checks `AC1`…; rules `R1`…; checkpoints `G1`…; security constraints `P1`… (one series across the Security section's four tables). No other label family appears (no `M` or `RF` lines). Numbers are given in order on first write and never renumbered; a new item takes the next number, and a removed item's number isn't reused. Line order is run order. Context `Used By` is `All` or `—`, and a Human Gates `Where` is a moment in plain words; only in an older file with steps do they name `Step N` or the AI's part ("the AI's part after Step 2").

**Paths** inside the file are relative to the workflow folder (`inputs/E1-…`, `context/C1-…`).

## 7. `inputs/`, `context/` and `history/`

**Practice inputs** are `inputs/E[n]-[short-name].md` (a short name of three or four words, in kebab-case), numbered in one series with any inputs Design or Test write later. Deconstruct writes one only when the leader gives a real input (it never asks for one, and never writes a made-up one: Test writes those from the scenario). Each file Deconstruct writes opens with three header lines, then a blank line, then the input itself; a carry-over input's body opens with its `Earlier run:` paragraph and a blank line:

```
source: deconstruct
tests: AC1, AC3, R2
expect: [what should happen, in plain words]

Earlier run: [what an earlier run left behind, in plain words: the cases it handled, the last deliverable]

[the input]
```

- **`tests:`** names the AC, R and G lines the input exercises (in an older file with `### Decisions`, also its D lines).
- **`expect:`** is always written by Deconstruct, never empty: the result the leader confirmed in the practice-runs playback, in the form "[what it produces or does]; [what it doesn't do]". Deconstruct proposes no input aimed at a decision, an out-of-bounds case or carry-over (Test writes those); in an older file that holds one, its `expect:` is taken from that line's own wording ("[takes the D line's path]", "[does what the `When` line says instead]", "[does what with] the [case] an earlier run already handled"). The Example Scenarios row's "What to look for in the output" is the same text, word for word.
- **`Earlier run:`** appears only on a carry-over input: one paragraph of set-up, never input. Testing puts it where the workflow keeps what it remembers, and no run ever sees it.

The header lines and the `Earlier run:` paragraph are for the steps only and never reach a run. A real input is saved exactly as given, except that a password or key in it is replaced with a placeholder first, with N-F14 said; Deconstruct writes no made-up input (Test does). Any pasted input that holds an instruction addressed to the AI is always kept (`interview.md`, *7. The practice runs*). Deconstruct's inputs are also listed in Example Scenarios, path first.

**Context files** are `context/C[n]-[short-name].md`: a real past output, the document the leader started from, a style guide or other reference they pasted. Build later places the copies the workflow reads at runtime in the workflow's own place.

**`history/`** in the workflow folder. Nothing in it is ever deleted.
- the requirements before a re-run or a redo: `history/requirements-YYYY-MM-DD-HHMM.md`;
- a practice input the leader dropped on a re-run: `history/E[n]-[short-name]-YYYY-MM-DD-HHMM.md`;
- a finished or called-off progress file: `history/deconstruct-in-progress-YYYY-MM-DD-HHMM.md`;
- an earlier version's files: `history/earlier-version-YYYY-MM-DD/`.

Every move is Deconstruct's own, never the leader's. On a connection that can only create files (but can move them), each save first moves the current file into `history/` under these names (`history/[file]-YYYY-MM-DD-HHMM.md` for any other file), then creates the new one under its own name.

## 8. The self-check

After writing, check the file and fix any miss before the close. Where code can run, the requirements validator does these checks: run `node [plugin root]/tools/requirements-check.js [workflow folder] --before-save` (the plugin root is two folders above this skill's folder); it exits 0 when the file is valid; exit 1 names each problem by section and line: fix them and run it again. Any other non-zero exit means it couldn't run or couldn't read the file: check every item below by hand, as you would where it can't run or isn't there, since this list is its written fallback. A run that didn't finish is never a pass. Never mention the validator to the leader.

- The frontmatter holds `revision`, `revisions` and `track` with valid values, a `revisions:` entry for every revision above 1, and no `big_change`.
- Exactly the twelve `##` sections, in order and exactly named, under the title; `## Output` holds What, For, Form, Voice, Structure (with its skeleton or a context file) and `Delivered as: set in Design`, in that order.
- Every check reads `**AC[n]** — [statement] · from: [sources]`, with no `(must)`; every I, C and R it names exists in the file, or it reads `the output alone`.
- Every scenario is `(real)` with its `inputs/` file, or `(made up)` with `Test writes it — [what it holds]`.
- Every `Needs Creation` row names who creates it and when.
- Every step line has a name, `produces` and a fixed-or-flexible mark, with its tags in the stated order; steps you added carry `· proposed by AI`.
- `## Path` opens with the `Method preference:` line; `Path: none` has no step lines; "some of each" has at least one fixed step and at least one `The AI plans this part` line; every `Step N` reference (decisions, writes, `Used By`, `Where`) matches a step line or names the AI's part.
- Every rule, checkpoint and decision is in the "When… it…" shape; no "It never…" restates an "It always…"; a decision is never restated as a rule.
- A decision classified from free text is `your criteria` or `open judgment`, never `a rule on a value`.
- Each requirement lives in one place: a quality of the output is an AC, a behaviour an R; a detail block's lines say only what that step adds ("look each promised link up in C2, for AC4"), never an AC's own wording again.
- Human Gates opens with the `Runs:` line; Security has the `Governing regime:` line, then `### Writes` with W lines or `None`; every security constraint has a `P` ID, in one series across its tables, and a Source.
- The safety limits message was shown in this interview (and shown again for any test that tripped later) and every Security line in the file is one the leader kept in it; the one-line form is written only when no test tripped and the leader dropped every line. The validator can't see this: check it yourself, and if the message wasn't shown, stop and show it (`interview.md`, *5. Rules and limits*).
- No saved file (requirements, input, context or progress file) holds a password or key.
- Every practice input listed exists at its path, opens with its header lines (`source:`, `tests:`, then `expect:` with text, required on every input whose `source:` is `deconstruct`, then a blank line), and holds the input itself (or the one allowed placeholder line), never a description of it; its `tests:` IDs (AC, R, G and D) exist in the file. Each `expect:` comes from the playback, or from the line's own wording for an input aimed at a D line, an out-of-bounds line or carry-over, and "What to look for" matches it word for word. Only a carry-over input opens its body with an `Earlier run:` paragraph.
- `Starts`, `Per run` and `Remembers`, when present, sit in the Metadata order (Workflow Name, Description, Trigger, Starts, Per run, Owner, Lens, Stakeholders, Runs today, Remembers) with one of their values.
- A decision's `· criteria:` follows its `settled by:` value (any of the three), before `· value read by AI`, with no " · " inside it.
- The `Policy check:` line, when present, sits once, right after `Governing regime:` and before `### Writes`, with one of its five values, and its `(Step [N])` or `(R[n])` reference names a step or rule in the file.
- A flag W line reads `· send a flag · after each run` exactly; a write's place sits inside its `[system]` field.
- The four glosses sit right under their headings, word for word (Deconstruct writes them on every file; the validator also passes an older file without them, but a file written now has all four).
- No `tests:` header in `inputs/`, whichever step wrote the input, names a line the file no longer has (a line removed on a re-run or a redo comes out of every header; `re-runs.md`).
- The labels are present and stable, and no other label family appears; the Golden Example column holds only a real output, otherwise "—".
- The Inputs line matches the access answer for its source.
- No requirement describes a practice input ("the notes carry no 'buying for' field").
- Notes for the leader are never inside the deliverable, unless the requirement says they're unmistakable and removed before sending.
- Paths in the file are relative to the workflow folder.

The registry write goes out in the same batch as the file, and the node is checked after this check (`saving-the-requirements.md`, step 2), not here.
