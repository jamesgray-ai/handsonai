# Workflow Requirements: the drafts and the file

Read at the start of Part 5 (on the light track, at "what it works from") and again when writing the file. Every quoted line is said exactly. The format is fixed: later steps and scripts parse it.

## Contents

1. The drafts: what goes in each
2. Which security categories are worked
3. Standing rules
4. The preview
5. Writing the file: style
6. The file: frontmatter, sections and line formats
7. `inputs/`, `context/` and `history/`
8. The self-check

## 1. The drafts: what goes in each

Each is short, plays its items back in plain words (never IDs or the tagged line format), and tags every line *(you said)*, *(from your [document])* or *(my suggestion)*.

**Draft 1, the rules.** Drafted from everything said so far, in the "When… it…" shape: what it always and never does (the always/never answers, a prohibition volunteered at the send-back test, expertise that became a rule), what's in and out of scope, any tone, format or length rule, and the Fallback. Offer matching standing rules and rules from the leader's other workflows or a policy document they named (section 3). A rule the leader gave stays a rule, never a step ("no shellfish"). Constraints about data and authority go to Security. A checkpoint isn't a prohibition: "never send without approval" is a checkpoint; "never send" is a prohibited action, offered in Security's Prohibited actions. An "It never…" that restates an "It always…" isn't added, and a step's own action isn't restated as a rule. Ends "What would you change or add?"

**Draft 2, checkpoints, sources and inputs.**
- The checkpoints collected so far, to confirm, with where each sits, who performs it, and whether it runs with the leader; no new checkpoint questions. Offer matching standing checkpoints (section 3).
- The sources it uses, introduced the first time in these words: "These are the sources it uses, what we call its **context**: any information a step needs to do its job, such as documents, spreadsheets, emails, style guides, or knowledge that lives in someone's head." For each: what it is, where it lives, and whether it exists or needs creating. A step's existing prompt or instructions count as a source. Content nobody on the team wrote that a step reads on each run (inbound emails, form submissions, web pages) gets its own `External` row as well as its Inputs line. For sources that trip no privacy test, draft whether the AI can reach them, tagged *(my suggestion)*.
- The Inputs drafted in Part 4, each with where it comes from and whether it exists yet.
- Ends "What would you change or add?"

**The security limits** (only when a test trips, section 2). Work out the tripped tests and categories from the Context Inventory as corrected, then play back each constraint in plain words under its category, never by its `P` ID (where data may go, who sees it, what it must never do, what gets recorded), tagged, and kept or dropped like the other drafts. Offer matching standing limits (section 3). A prohibition already in draft 1 isn't repeated. A trace record says where it's kept, never inside the deliverable (for a follow-up email, for illustration only: "Each draft is logged with the call notes it came from, outside the email itself."; write the leader's own version). Ends "What would you change or add?"

**Draft 3, what every [deliverable] must get right.** Opens "Here's what every [deliverable] must get right:", then the list from Part 3 with the must-haves named in plain words, plus the quality standards held from Part 4, *(you said)*, unless the list already covers them. Rules and checkpoints are graded from their own sections and aren't copied into the list. Ends "What would you change or add?"

**Draft 4, the practice runs.** Three to five in total (two or three on the light track):
- **Real rows:** the input behind the Golden Example is E1; the typical case from Part 4 is `(real)`; the tricky case is `(real, hard)`.
- **Proposed rows,** marked `(proposed)`, or `(proposed, hard)` for the hard case, each aimed at one risk named in plain words, skipping any a real row already covers: an empty or malformed input; one aimed at an "It never…" rule or a checkpoint (one such input, not one per rule); and, only when there's an `External` source, an input that carries an instruction addressed to the AI. Propose only inputs the leader could actually get hold of.

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

With nothing tripped, the one-line form: "No sensitivity constraints — personal data only, read-only, human-triggered." A stated prohibition is always written down: with nothing tripped but a prohibition stated, `### Prohibited actions` holds it with its Source and its `P` ID (`P1` for the first), and the section opens "No sensitivity constraints beyond the prohibition(s) below — personal data only, read-only, human-triggered."

## 3. Standing rules

`standing-rules.md` in the framework folder holds the rules a leader keeps for every workflow: tone and voice, who approves what, data that's never shared, systems that are never touched.

**Proposing them.** In draft 1, draft 2 and the security limits (on the light track, its rules draft), offer matching lines from: `standing-rules.md`; the rules, checkpoints and security limits of the leader's other workflows in the registry; context files, and any policy document the leader named (an AI policy, a brand guide). Each is tagged *(my suggestion)* with its source in plain words ("from your standing rules", "as in your Client Follow-Up workflow", "from your AI policy") and needs a keep or drop. Offer only lines that fit this workflow. A kept line is copied into this workflow's requirements as an R or G line (or a security constraint), so each workflow's requirements stay its own source of truth. A first-time leader with none of these sees nothing extra.

**Keeping them.** Once the rules, checkpoints and security limits are settled (after draft 2, or after the security limits when there are any; on the light track, after its rules draft), and only when at least one kept line looks like one the leader would want everywhere and isn't already a standing rule, ask in its own message. On the light track, ask it only from the leader's second workflow: another workflow's folder (not this one's) holding more than a progress file, or another node past `backlog`, not counting running work. Never on print-to-save, where there's no framework folder to keep it in.

**Ask:** "Some of these sound like rules you'd want for every workflow: [rules, in plain words]. Should I keep them as standing rules, so I suggest them for your next workflows too?"
- *Why:* I'll suggest them whenever you start a new workflow, and each workflow keeps its own copy, so changing one later doesn't touch workflows already built.
- *Not sure?* Say no for now; I'll ask again the next time one of these comes up.

The lines kept are written to `standing-rules.md` at the close (Phase 7); create the file the first time:

```markdown
# Standing rules

Rules you keep for every workflow. Deconstruct suggests the ones that fit each new workflow, and each workflow's requirements keep their own copy.

- It never shares client data outside the company. · rule · from weekly-status-report, 2026-10-18
- When a draft goes to a client, it stops until you approve it. · checkpoint · from client-follow-up, 2026-10-20
```

Each line is in the "When… it…" shape, with its kind (`rule` or `checkpoint`), the workflow it came from and the date. The leader may edit or remove lines directly, or ask you to; never change or remove a standing rule on your own. A changed standing rule applies to new workflows only; an existing workflow changes through "change my workflow".

## 4. The preview

Always, in its own message, right after the target (on the light track, after the defaults message) and before anything is written; never skipped. Say, word for word, with "[ and where it asks first]" only when there's a checkpoint:

> Each practice run is checked against the lines we've written: what every [deliverable] must get right, its rules[ and where it asks first]. The workflow is ready when every line is met on the inputs that test it — or when you've looked at a miss on a line that isn't a must-have and decided you can live with it.
>
> Next, I'll write your Workflow Requirements file. Say 'go ahead', or tell me anything to change first.

Line IDs (AC1, R3, G1, P1) stay in the file and never reach the leader.

## 5. Writing the file: style

The file reads like a requirements document, not an interview transcript:
- **Requirements voice:** every line states what must be true, not what the leader said: "Output is a Markdown table with one row per prospect", not "The user mentioned a table."
- **Active voice, present tense:** "Validate the input against the rubric."
- **One requirement per line;** lists, not paragraphs, wherever several requirements appear.
- **Concrete over abstract:** name the document, the field, the threshold: "Reject submissions over 500 words."
- **No interview residue:** no hedges ("I think", "usually"), narrative connectors ("then the user") or commentary ("we discussed").
- **Self-contained:** a reader who never saw the conversation can work from it.
- **Markdown hygiene:** no bare `~` for "about" (two in a paragraph render as strikethrough).

**Machine-readable:** the fixed headings in the fixed order; tables for lists of items with shared fields (context, practice inputs, rules, checkpoints, security constraints); list lines for steps, decisions, inputs and writes; the canonical values (Lens `Individual` or `Organizational`; Context Status `Exists` or `Needs Creation`; Sensitivity `Public`, `Internal`, `Confidential` or `Regulated`; Provenance `Authored` or `External`; AI Accessible `Yes`, `Partial` or `No`; Inputs Status `available`, `not available yet` or `Not sure — to check`; `settled by:` `a rule on a value`, `your criteria` or `open judgment`); every step line names what it produces, with `uses` and `writes` tags whenever the step reads context or writes outside.

## 6. The file: frontmatter, sections and line formats

`requirements.md` in the workflow folder. Frontmatter, then the title, then exactly these `##` sections, named exactly, in this order, and no others.

**Frontmatter:**

```yaml
---
revision: 2
track: full
revisions:
  - revision: 2
    by: deconstruct
    lines: [AC3, R2, Step 4]
---
```

- **`revision`:** 1 on the first save; raised by one when a re-run or a redo changes a line (not when only practice inputs change).
- **`revisions`:** `[]` at revision 1, then one entry per revision: `revision`, `by` (`deconstruct`, `design` or `test`) and `lines` (the IDs added, changed or removed); Test adds `plan_unaffected: true` to its own entries. Keep every entry other steps wrote.
- **`track`:** `light` or `full`.
- **`big_change`:** never in a file Deconstruct saves (Design writes it with no registry while a redo is pending; the redo's saved file leaves it out).

````markdown
# [Workflow Name] — Workflow Requirements

## Goal
For each [trigger], a [format] [deliverable] to [who], ready for you to [review] [when].

## Value & Measurement

| Field | Value |
|---|---|
| Business Objective | [which strategic objective this supports] |
| Desired Outcome | [what changes, and for whom] |
| Measure | [what gets counted] |
| Baseline | [today's number] · Measured / Estimated / Unknown |
| Target | [what it should achieve once running, or "—"] |

## Metadata

| Field | Value |
|---|---|
| Workflow Name | [name] |
| Description | [the one-sentence description] |
| Trigger | [what kicks it off] |
| Owner | [person or role] |
| Lens | Individual / Organizational |
| Stakeholders | [roles or teams; Organizational lens only] |
| Runs today | [running work brought in only: by hand; or set up as [a skill, an agent, an automation] in [where]; on a schedule or not] |

## Path

Method preference: some of each

- Step 1 — [Name] · produces [what it produces] · uses C1 · fixed (policy)
- The AI plans this part
- Step 3 — [Name] · produces [what it produces] · uses C2 · flexible · writes W1 · (you)

### Decisions

- D1 (Step 3): When [this is true], it [goes this way] · settled by: a rule on a value · value read by AI

### Step 1 — [Name]
**Rule:** [the rule it follows at this step]
**Check or handoff:** [what's checked, or who it passes to]
**Expertise:** [what a capable beginner would get wrong]

## Inputs

- I1 · [what comes in] · from [source or C#] · Status: available

## Context Inventory

| ID | Artifact | Used By | Status | Sensitivity | Provenance | AI Accessible | Location / Source | Key Contents |
|---|---|---|---|---|---|---|---|---|
| C1 | [name] | [Step N, the AI's part after Step N, All, or —] | Exists / Needs Creation | Public / Internal / Confidential / Regulated | Authored / External | Yes / Partial / No | [`context/C1-[short-name].md`, a system or a URL, or "Create as `context/C1-[short-name].md`"] | [what's in it] |

## Acceptance Criteria

Each line is one thing a single run's output either does or doesn't do. Every practice run is checked against every line; one miss on a must-have sends it back.

1. **AC1 (must)** — [yes-or-no statement]
2. **AC2** — [yes-or-no statement]

Reference example: [C# of the real output, or "—"]

## Example Scenarios

| ID | Scenario | Input | What to look for in the output | Golden Example |
|---|---|---|---|---|
| E1 | [short name] (real) | `inputs/E1-[short-name].md` — [description] | [what makes this output good, in plain words] | [C#, or "—"] |
| E2 | [short name] (proposed, hard) | `inputs/E2-[short-name].md` — [description] | [what to look for] | — |

## Rules & Constraints

| ID | Kind | Rule |
|---|---|---|
| R1 | Always | It always [does that]. |
| R2 | Never | It never [does that]. |
| R3 | When | When [this happens], it [does that]. |
| R4 | When | When the draft is ready, you send it yourself. · (you) |
| R5 | Fallback | When it can't confidently handle a case, it [stops and asks you / does its best and flags it / skips that item]. |

## Human Gates

Runs: with you

| ID | Where | Checkpoint |
|---|---|---|
| G1 | Step 3 | When the draft is ready, it stops until you approve it. · (you) |

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

### Writes
- W1 · [system] · [action] · Step 3
````

**Line formats:**
- **Step line:** `- Step 3 — Draft brief · produces a one-page brief · uses C2, C4 · fixed (regulation | policy | your judgment) | flexible · writes W1 · (you) | (finance team) · parallel with Step 2 · proposed by AI`. The name, `produces` and the fixed-or-flexible mark are required, also on a step a person does (the role tag never replaces the mark). Every other tag is optional, left out when it doesn't apply, and in this order. The role tag means a person still performs the step; `· parallel with` only when the leader said two steps don't depend on each other; `· proposed by AI` marks a step you added that the leader hasn't fixed.
- **`## Path`, in order:** the `Method preference:` line, always first; `Path: proposed by AI` (only when you proposed the whole path) or `Path: none — the AI plans each run from the goal` (no step lines); the step lines, with `- The AI plans this part` where the AI plans (not a step: no number, no `produces`, no mark, never counted); `### Decisions`, left out when there are none; then a `### Step N — [Name]` detail block for each step that carries detail, one bold-labelled line per field that applies (what it uses stays on the step line).
- **Decision line:** `- D1 (Step 3): When [condition], it [path] · settled by: a rule on a value | your criteria | open judgment · value read by AI` (the last tag only when the AI reads the value); with no steps, `- D1: When …`.
- **Input line:** `- I1 · [what] · from [source or C#] · Status: available | not available yet | Not sure — to check`, with the route where there is one ("from C1, through the Google Drive connection"). Inputs' Status is about what comes in on each run; the Context Inventory's Status is about reference material; a run input that doesn't exist yet is recorded in Inputs only.
- **Writes** under `### Writes`: `- W1 · [system] · [action] · Step 3`, or `· after [moment]` with no steps. With nothing written, the heading stays, with the line `None`.
- **Rules:** each in the "When… it…" shape, in the leader's words where they gave them; `Kind` is `Always`, `Never`, `When` or `Fallback`. A rule a person carries out ends with its role tag (`· (you)` or `· ([role])`) and isn't graded on the output. Rules are behavioural ("It never invents a figure"); a prohibition on acting ("It never emails a customer") is a prohibited action in Security. A "stop and ask" Fallback also has a checkpoint.
- **Human Gates:** the first line is `Runs: with you` or `Runs: without you`. Each checkpoint is in the shape, names who performs it, and ends with the role tag. With none, under the `Runs:` line: "No human gates — the workflow runs end-to-end with final review only."
- **Security:** every constraint has a `P` ID, numbered in one series across the four tables in the order they're written (only the categories that were worked appear), and a Source (`Self` when the leader is the source). Design and Test name a constraint by its ID, never by copying its words. Prohibited actions are absolute; checkpoints are conditional (if an approval can satisfy it, it's a checkpoint). The sensitivity of what the workflow produces belongs in Access. `Governing regime:` and `### Writes` appear in both the full and the one-line form.
- **Context Inventory:** a `Needs Creation` item's location is where it will be created (`context/…`). On the Organizational lens, existing process documents (SOPs, training guides, compliance requirements, service levels) are included.
- **Metadata:** the `Runs today` row only for running work brought in; `Stakeholders` only on the Organizational lens.

**Labels:** steps `Step 1`, `Step 2`…; decisions `D1`… (linked to their step when there is one); inputs `I1`…; writes `W1`…; context `C1`…; practice inputs `E1`…; checks `AC1`…; rules `R1`…; checkpoints `G1`…; security constraints `P1`… (one series across the Security section's four tables). No other label family appears (no `M` or `RF` lines). Numbers are given in order on first write and never renumbered; a new item takes the next number, and a removed item's number isn't reused. Line order is run order. Context `Used By` and Human Gates `Where` name steps as `Step N`, or the AI's part ("the AI's part after Step 2").

**Paths** inside the file are relative to the workflow folder (`inputs/E1-…`, `context/C1-…`).

## 7. `inputs/`, `context/` and `history/`

**Practice inputs** are `inputs/E[n]-[short-name].md` (a short name of three or four words, in kebab-case), numbered in one series with any inputs Design or Test write later. Each file opens with two header lines, then a blank line, then the input itself:

```
source: deconstruct
tests: AC1, AC3, R2
```

`tests:` names the AC, R and G lines the input exercises. A real input is saved exactly as given, except that a password or key in it is replaced with a placeholder first, with N-F14 said; a proposed one is written out in full, so it can be pasted as it is. The full track saves three to five, the light track two or three. Deconstruct's inputs are also listed in Example Scenarios, path first.

**Context files** are `context/C[n]-[short-name].md`: a real past output, the document the leader started from, a style guide or other reference they pasted. Build later places the copies the workflow reads at runtime in the workflow's own place.

**`history/`** in the workflow folder. Nothing in it is ever deleted.
- the requirements before a re-run or a redo: `history/requirements-YYYY-MM-DD-HHMM.md`;
- a practice input the leader dropped on a re-run: `history/E[n]-[short-name]-YYYY-MM-DD-HHMM.md`;
- a finished or called-off progress file: `history/deconstruct-in-progress-YYYY-MM-DD-HHMM.md`;
- an earlier version's files: `history/earlier-version-YYYY-MM-DD/`.

Every move is Deconstruct's own, never the leader's. On a connection that can only create files (but can move them), each save first moves the current file into `history/` under these names (`history/[file]-YYYY-MM-DD-HHMM.md` for any other file), then creates the new one under its own name.

## 8. The self-check

After writing, check the file and fix any miss before the close. Where code can run, the requirements validator does these checks: run `node [plugin root]/tools/requirements-check.js [workflow folder] --before-save` (the plugin root is two folders above this skill's folder); it exits 0 when the file is valid and names each problem by section and line otherwise. Where it can't run, or isn't there, this list is its written fallback; check each item by hand. Never mention the validator to the leader.

- The frontmatter holds `revision`, `revisions` and `track` with valid values, a `revisions:` entry for every revision above 1, and no `big_change`.
- Exactly the eleven `##` sections, in order and exactly named, under the title.
- Every step line has a name, `produces` and a fixed-or-flexible mark, with its tags in the stated order; steps you added carry `· proposed by AI`.
- `## Path` opens with the `Method preference:` line; `Path: none` has no step lines; "some of each" has at least one fixed step and at least one `The AI plans this part` line; every `Step N` reference (decisions, writes, `Used By`, `Where`) matches a step line or names the AI's part.
- Every rule, checkpoint and decision is in the "When… it…" shape; no "It never…" restates an "It always…"; a decision is never restated as a rule.
- A decision classified from free text is `your criteria` or `open judgment`, never `a rule on a value`.
- Each requirement lives in one place: a quality of the output is an AC, a behaviour an R; a detail block's lines say only what that step adds ("look each promised link up in C2, for AC4"), never an AC's own wording again.
- Human Gates opens with the `Runs:` line; Security has the `Governing regime:` line, then `### Writes` with W lines or `None`; every security constraint has a `P` ID, in one series across its tables, and a Source.
- No saved file (requirements, input, context or progress file) holds a password or key.
- Every practice input listed exists at its path, opens with the two header lines, and holds the input itself (or the one allowed placeholder line), never a description of it; its `tests:` IDs exist in the file.
- The labels are present and stable, and no other label family appears; the Golden Example column holds only a real output, otherwise "—".
- The Inputs line matches the access answer for its source.
- No requirement describes a practice input ("the notes carry no 'buying for' field").
- Notes for the leader are never inside the deliverable, unless the requirement says they're unmistakable and removed before sending.
- Paths in the file are relative to the workflow folder.
- Where there's a registry, the node has the fields the registry write gives it, `generated` restamped.
