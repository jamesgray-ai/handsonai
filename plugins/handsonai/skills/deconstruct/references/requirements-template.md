# Workflow Requirements: template and Part 5 drafts

Read at the start of Part 5 and again when writing the file. Every quoted line is said exactly.

## Contents

1. The draft messages
   - Message 1: rules and never-dos
   - Message 2: gates, sources and inputs, then the privacy questions
   - Only when a sensitivity test trips: the security limits
   - Message 3: what every [deliverable] must get right
   - Message 4: the practice runs
2. Security, Privacy & Safety handling
3. The labels preview
4. Writing the file: style and machine-readability rules
5. Template skeleton and line formats
6. Self-check before finishing

## 1. The draft messages (four, plus the security limits when a test trips)

Each is short, plays its items back in plain words (never IDs or the tagged line format), and tags every line *(you said)* or *(my suggestion)*. Each suggestion needs an explicit keep or drop; "looks right" triggers the rubber-stamp re-ask.

### Message 1: rules and never-dos

Draft the Rules & Constraints rows from everything said so far: what it must always do, what it must never do (including any prohibition volunteered at the send-back test), what's in and out of scope, any tone, format or length rules, and the Fallback answer. A rule the student gave stays a rule, never a step ("no shellfish"). Keep rules behavioral; constraints about data and authority go to Security, Privacy & Safety. A gate is not a prohibition: "never send without approval" is a gate; "never send" is a Prohibited action. Every "never" recorded as an M line in Part 4 is offered here, as a Must never rule or, for a prohibition on acting, a Prohibited action; whichever is kept removes its M line, and if dropped the M line stays. A Never that restates an Always isn't added, and a step's own action isn't restated as a rule. End: "What would you change or add?"

### Message 2: gates, sources and inputs, then the privacy questions

- **The checkpoints collected so far** (the file's Human Gates; say "checkpoints"), to confirm, with where each sits and who performs it, and whether it runs with the student or without them. No new gate questions.
- **The sources it uses**, introduced the first time in these words: "These are the sources it uses, what we call its **context**: any information a step needs to do its job, such as documents, spreadsheets, emails, style guides, or knowledge that lives in someone's head." For each: what it is, where it lives, whether it exists or needs creating. If a step already uses AI, its existing prompt or instructions are a source too (Build reads them). Content nobody on the team wrote that a step reads on each run (inbound customer emails, form submissions, web pages) is a source too: it gets its own Context Inventory row marked `External`, as well as its Inputs line, and the privacy questions cover it. For sources that trip no privacy check, draft whether the AI can reach them, tagged *(my suggestion)*.
- **The Inputs** drafted in Part 4, each with where it comes from and whether it exists yet; the Inputs line follows the access answer ("from C1, through the Google Drive connection").

End: "What would you change or add?"

**Then the privacy questions.** They follow today's tests: any Context Inventory row marked `Confidential` or `Regulated`, or any `External` source. Right after message 2, one question per tripped source the AI can't reach, each its own message:

**Ask:** "When this runs, can the workflow reach [source] itself, for example through a connection to [tool], or will you paste it in each time?"
- *Why:* If it can't reach it, it has to ask you for it on every run.
- *Not sure?* Say you'll paste it. You can connect it later.

The answer sets the Context Inventory's `AI Accessible` column. When a write's system needs a connection, say once, after the access questions: "Saving drafts in [system] also needs a connection; we'll set that up when it's built." (name what it writes). A write (W#) trips only the Security categories below (Prohibited actions and Traceability), not this question, which is about sources.

A row saved as `Regulated` when the Part 2 answer was no or not sure: **Ask:** "Which one? A name or a description is fine." once; if it is still unknown, record `Governing regime: Not sure — to check`. This doesn't switch on the detail table.

### Only when a sensitivity test trips: the security limits

Its own short message, after the privacy questions and before message 3. Work out the tripped tests and categories as in section 2 (from the Context Inventory marks as corrected in reply to message 2), then play back each constraint in plain words under its category (where data may go, who sees it, what it must never do, what gets recorded), tagged *(you said)* or *(my suggestion)*, each kept or dropped as in the other drafts. A prohibition already in message 1 isn't repeated. A trace record says where it is kept, never inside the deliverable ("Each draft is logged with the call notes it came from, outside the email itself."). When nothing trips, there is no such message. End: "What would you change or add?"

### Message 3: what every [deliverable] must get right

Open "Here's what every [deliverable] must get right:" then the list from Part 3, with the must-haves marked in plain words, plus the quality standards held from Part 4 (tagged *(you said)*, skipping any the list already covers). Rules and checkpoints are graded from their own sections, so don't copy them into the list. A number the student gave is *(you said)*. End: "What would you change or add?"

### Message 4: the practice runs

Build the set, 3–5 in total:

- **Real rows:** the input behind the Golden Example is E1; the typical case from Part 4 is `(real)` and the tricky case `(real, hard)`.
- **Proposed rows**, marked `(proposed)`, or `(proposed, hard)` when it is the hard case, each aimed at one risk named in plain words, skipping any a real row already covers: an empty or malformed input; one aimed at a Must never rule or a gate (one such scenario, not one per rule or gate); and, only when the Context Inventory has an `External` source row, an input that carries an instruction addressed to the AI. Propose only inputs the student could actually put their hands on.
- **Name risks, not labels.** Say "this one checks it never contacts someone we've already emailed", not `R3`: the labels come in the preview.

Open with "Here are the practice runs we'll test it on." and play each back in plain words (never the `(real)` or `hard` tags). End the message with this, word for word: "Change, replace or drop any; keep three to five, including your typical and tricky [cases]. When we test it, you'll paste in [inputs] for each, with names and details made up."

Then:

- **Keep a hard one.** If fewer than 3 scenarios or no hard case remain after their changes, propose replacements and get each one kept before going on; the rule-or-gate scenario doesn't count as the hard case.
- **Golden example per real row.** Skip this when Part 3 recorded no reference example. Otherwise, for each `(real)` row without one, in its own message, **Ask:** "Have you sent a [deliverable] after a [case] like this that you'd want every one to match?" Record its Context Inventory ID, a short excerpt, or "—". A `(proposed)` row has "—"; never write a golden example you generated yourself.
- **Paste the real inputs now.** For a real input named but not pasted ("last Friday's tracker export"), **Ask:** "Paste a set of [inputs], or say 'draft one' and I'll write a made-up example from your description for you to check." Where files can't be kept: "paste it in and I'll include it in the files you save, so testing is copy-and-paste rather than a hunt". A made-up example is shown in full and checked ("Does this look like your real [inputs]?"); it never states what the workflow must work out (no "Buying for:" line, no flag it should raise); a made-up example of the student's own typical or tricky case stays `(real)`. The confidential check runs before saving. Only if they genuinely can't get hold of it today, write the file with a single placeholder line naming exactly what to paste in before testing, and say that is what the file holds.
- **Number and save.** Number the confirmed set E1, E2, … in order on first write (after that, numbers are stable IDs). Save each as `framework/[name]/inputs/E<n>-<short-name>.md` (`<short-name>`: three or four words, kebab-case): a real input exactly as given, a proposed one written out in full so it can be pasted as is.
- **Fill the table.** Each `Input` cell starts with the file path in backticks, then ` — `, then the short description. Each Scenario cell ends with `(real)`, `(proposed)`, or either with `, hard`. Each "What to look for in the output" cell ends with what it tests (`; tests R2, G1`, or `; tests the Step 2 duplicate-company case`).

## 2. Security, Privacy & Safety handling

The Context Inventory's columns answer two of the three sensitivity tests, so derive them rather than asking again:

- any row `Confidential` or `Regulated` → it handles data the student would be uncomfortable seeing outside the company;
- any row `External` → it consumes content nobody on the team authored;
- any write (a `### Writes` line) → it writes to a live system. Running without you is the higher-risk form of the same thing, so `Runs: without you` counts too.

If anything is tripped, work only the categories the tripped tests implicate:

| What tripped | Categories to work |
|---|---|
| Writes to a live system | **Prohibited actions** (what it must never do, whoever asks) and **Traceability** (what has to be recorded, so a run can be reconstructed afterwards) |
| An `External` row | **Boundaries** (where that content may travel) and **Prohibited actions** (what it may never be allowed to trigger) |
| A `Confidential` row | **Boundaries** (where the data may travel) and **Access** (who may see the outputs and intermediate state) |
| A `Regulated` row | Boundaries and Access as above, with the `Governing regime:` line naming the regime, or `Not sure — to check` |

Work each implicated category once, even when two tests point at the same one. Capture a Source for every constraint; `Self` when the student is the source.

If nothing is tripped, write the one-line form: "No sensitivity constraints — personal data only, read-only, human-triggered." A stated prohibition is always written down: if nothing was tripped but the student stated a "never do", keep `Prohibited actions` with that constraint and its Source, and open the section with "No sensitivity constraints beyond the prohibition(s) below — personal data only, read-only, human-triggered." Both forms still carry the `Governing regime:` line and `### Writes` (with `None` when nothing writes).

## 3. The labels preview

Before generating the file, in its own message, show a few lines of the report card, so the student sees where their answers go:

> "Here are a few of the lines each practice run is checked against:
>
> | What's checked | Label |
> |---|---|
> | Every row has contact info (a must-have) | AC1 |
> | Uses our three headings | AC2 |
> | Never includes someone we've already contacted | R3 |
> | Pauses before sending | G1 |
>
> The workflow is ready when every line is Met on every input — or when you've looked at a miss and decided you can live with it. In the file, each line has a short label, like AC1 or R3, so we can refer to it later.
>
> Next, I'll write your Workflow Requirements file. Say 'go ahead', or tell me anything to change first."

Fill the table from the student's own list, rules and checkpoints.

## 4. Writing the file

Write `framework/[name]/requirements.md`, creating the folder if needed.

**Style (MUST follow).** The file reads like a requirements document, not an interview transcript:

- **Requirements voice.** Every bullet states what must be true, not what the student said: "Output is a Markdown table with one row per prospect", not "The user mentioned a table."
- **Active voice, present tense.** "Validate the input against the rubric."
- **One requirement per line.** Bulleted lists, not paragraphs, wherever several discrete requirements appear.
- **Concrete over abstract.** Name the document, the field, the threshold: "Reject submissions over 500 words."
- **No interview residue.** No hedges ("I think", "usually"), narrative connectors ("then the user") or meta-commentary ("we discussed").
- **Self-contained.** A reader who never saw the conversation can implement against it.
- **Markdown hygiene.** No bare `~` for "approximately" (two in one paragraph render as strikethrough); write "about", or keep `~` inside backticks.

**Machine-readability (MUST follow)**, so Design and any later step can read it without re-asking:

- **Fixed headings in fixed order**, exactly as in the skeleton; no synonyms, no reordering, no YAML frontmatter.
- **Tables** for lists of items with shared fields (context, scenarios, rules, gates); list lines for steps, decisions, inputs and writes, in the formats below.
- **Canonical values:** Lens `Individual` or `Organizational`; Context Status `Exists` or `Needs Creation`; Sensitivity `Public`, `Internal`, `Confidential` or `Regulated`; Provenance `Authored` or `External`; AI Accessible `Yes`, `Partial` or `No`; Inputs Status `available` or `not available yet`; `settled by:` `a rule on a value`, `your criteria` or `open judgment`.
- **Stable labels:** steps `Step 1, Step 2…`; decisions `D1…` (each linked to its step when there is one); inputs `I1…`; writes `W1…`; must-always and must-never lines `M1…`; context `C1…`; scenarios `E1…`; criteria `AC1…`; rules `R1…`; gates `G1…`. Numbers are assigned in order on first write and never renumbered; a new item gets the next number. Line order is the run order.
- **Every step line names what it produces;** `uses` and `writes` tags are present whenever the step reads context or writes outside.
- Context Inventory `Used By`, Human Gates `Where` and the `; tests …` tails name steps as `Step N`, or the AI's part ("the AI's part after Step 2") where an unpicked AI step was collapsed.

## 5. Template skeleton and line formats

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
| Target | [what the revised workflow should achieve] |
| Readable When | [how long after go-live the number can be read] |

Notes:
- `Baseline: Unknown` is a legitimate value, recorded as `Unknown — must measure before go-live`.
- Measure quantifies Desired Outcome; it does not replace it.

## Metadata

| Field | Value |
|---|---|
| Workflow Name | [name] |
| Description | [short description] |
| Trigger | [what kicks the workflow off] |
| Owner | [person or role] |
| Lens | Individual / Organizational |
| Stakeholders | [roles or teams involved — Organizational lens only] |

## Path

Method preference: same way every time
Path: proposed by AI

- Step 1 — [Name] · produces [what it produces] · uses C1 · flexible
- Step 2 — [Name] · produces [what it produces] · uses C2, C4 · fixed (policy) · writes W1 · (you) · parallel with Step 1
- Step 3 — [Name] · produces [what it produces] · flexible · proposed by AI

### Must always / never

- M1 · always [x]
- M2 · never [y]

### Decisions

- D1 (Step 2): if [X] → [path] · settled by: a rule on a value · value read by AI

### Step 2 — [Name]
**Rule:** [the rule it must follow]
**Check or handoff:** [what must be checked, or who it passes to]
**Expertise:** [what a capable beginner would get wrong]

## Inputs

- I1 · [what comes in] · from [source or C#] · Status: available

## Context Inventory

| ID | Artifact | Used By | Status | Sensitivity | Provenance | AI Accessible | Location / Source | Key Contents |
|---|---|---|---|---|---|---|---|---|
| C1 | [name] | [Step N, or "All"] | Exists / Needs Creation | Public / Internal / Confidential / Regulated | Authored / External | Yes / Partial / No | [path, URL, system name, or "Create as [path]"] | [what's in it] |

## Acceptance Criteria

Each line is one thing a single run's output either does or does not do. Test checks every line per scenario. One miss on a must line fails that test case.

1. **AC1 (must)** — [yes/no statement]
2. **AC2** — [yes/no statement]

Reference example: [Context Inventory ID of the real output, or "—"]

## Example Scenarios

| ID | Scenario | Input | What to look for in the output | Golden Example |
|---|---|---|---|---|
| E1 | [short name] (real) | `framework/[name]/inputs/E1-[short-name].md` — [description] | [what makes this output good]; tests [AC/R/G IDs or the named case] | [C# of the real output, or "—"] |
| E2 | [short name] (proposed, hard) | `framework/[name]/inputs/E2-[short-name].md` — … | …; tests [IDs] | — |

## Rules & Constraints

| ID | Type | Rule |
|---|---|---|
| R1 | Must do | [behavioral rule] |
| R2 | Must never do | Never [behavioral only, written as a sentence that starts "Never"] |
| R3 | Scope | [what's in scope, what's out] |
| R4 | Tone / format / length | [if applicable] |
| R5 | Fallback | [stop and ask / do its best and flag it / skip that item] |

## Human Gates

Runs: with you

| ID | Where | What requires human input |
|---|---|---|
| G1 | Step N | [decision, approval, review — and who performs it] |

## Security, Privacy & Safety

*Scope: [which of the three tests applies — writes to a live system / consumes content nobody on the team authored / handles data you would be uncomfortable seeing outside the company]*

### Boundaries
| Constraint | Source |
|---|---|
| [where data may and may not travel] | [person, policy, control ID, or `Self`] |

### Access
| Constraint | Source |
|---|---|
| [who may see outputs and intermediate state] | [...] |

### Traceability
| Constraint | Source |
|---|---|
| [what must be recorded, and for whom] | [...] |

### Prohibited actions
| Constraint | Source |
|---|---|
| [what the workflow must never do — absolute, not conditional] | [...] |

Governing regime: [name] | None | Not sure — to check

### Writes
- W1 · [system] · [action] · Step 2
````

**Line formats:**

- **Step line:** `- Step 3 — Draft brief · produces a one-page brief · uses C2, C4 · fixed (regulation | policy | your judgment) | flexible · writes W1 · (you) | (finance team) · parallel with Step 2 · proposed by AI`. The name, `produces` and the fixed/flexible mark are required; every other tag is optional and left out when it doesn't apply, and tags appear in this order. The role tag means a person still performs the step; `· proposed by AI` marks a step the AI added that the student hasn't insisted on; `· parallel with` is added only when the student said two steps don't depend on each other.
- **`## Path` order:** the `Method preference: same way every time | AI works it out each time | some of each` line, always first; the `Path: proposed by AI` line (only when the AI proposed the whole path), or `Path: none — the AI plans each run from the goal` (AI works it out each time, with no step lines); the step lines, with `- The AI plans this part` where the AI plans ("some of each": not a step, no number, no `produces` or fixed/flexible mark, and not counted as a step); `### Must always / never` with the M lines (when there are any); `### Decisions` (left out when there are none); then a `### Step N — [Name]` detail block for each step that carries detail, one bold-label line per field that applies (`**Rule:**`, `**Check or handoff:**`, `**Expertise:**`; what it uses stays on the step line).
- **Decision line:** `- D1 (Step 3): if [X] → [path] · settled by: a rule on a value | your criteria | open judgment · value read by AI` (the last tag only when the AI reads the value); with no steps, `- D1: if [X] → [path] · …`. `a rule on a value` only for a number, date, field or category stated in the input; a classification from free text is `your criteria` or `open judgment`.
- **M line:** `- M1 · always [x]` or `- M2 · never [y]`, with an optional role tag (`- M3 · always you send it · (you)`). No detail block.
- **Input line:** `- I1 · [what] · from [source or C#] · Status: available | not available yet`. Inputs' Status is about what comes in on each run; the Context Inventory's Status is about reference material. A run input that doesn't exist yet is recorded in Inputs only.
- **Writes list** under `### Writes`: `- W1 · [system] · [action] · Step 3` (or `· after [moment]` with no steps); when nothing writes, the heading stays with the line `None`.
- **Human Gates:** the first line is `Runs: with you` or `Runs: without you`. With no gates, write under it: "No human gates — the workflow runs end-to-end with final review only."
- **Rules:** write each Must never rule as a sentence that starts "Never" ("Never name another client"), in the student's words where they gave them. This section is behavioral. "Must never do" here means behavioral (never invent a figure); a prohibition on acting (never email a customer) is a Prohibited action. A "stop and ask" Fallback also has a Human Gates row.
- **Security:** every constraint carries a Source (`Self` on the Individual lens rather than a blank). Prohibited actions are absolute; Human Gates are conditional: if an approval can satisfy it, it is a gate. The sensitivity of what the workflow produces belongs in `Access`. `Governing regime:` and `### Writes` appear in both the full and the one-line form.
- **Context Inventory:** a `Needs Creation` item's location is where it should be kept so the AI can reach it. For Organizational workflows, include existing process documents (SOPs, training guides, compliance requirements, SLAs).

## 6. Self-check before finishing

After writing, check the file and fix any miss before the close:

- It lives at `framework/[name]/requirements.md`; the Workflow node has `status: under-development` (unless a re-run kept another status) and links the requirements under `# Artifacts`.
- It has exactly the twelve sections, in this order and exactly named: `# [Name] — Workflow Requirements`, `## Goal`, `## Value & Measurement`, `## Metadata`, `## Path`, `## Inputs`, `## Context Inventory`, `## Acceptance Criteria`, `## Example Scenarios`, `## Rules & Constraints`, `## Human Gates`, `## Security, Privacy & Safety`. No YAML frontmatter, no other `##` section.
- Every step line has a name, `produces` and a fixed/flexible mark (a step a person does too: the role tag never replaces the mark), with tags in the stated order (`produces`, `uses`, the fixed/flexible mark, `writes`, the role, `parallel with`, `proposed by AI`); AI-added steps carry `· proposed by AI`.
- Human Gates opens with the `Runs:` line; Security has the `Governing regime:` line, then `### Writes` with W lines or `None`.
- Every scenario's input file exists at the path its `Input` cell names and holds the input itself (or the one allowed placeholder line), never a description of it. Write any that are missing.
- Labels are present and stable (Step N, D, I, W, M, C, E, AC, R, G); the Golden Example column holds only a real output, else "—".
- `## Path` opens with the `Method preference:` line; `Path: none` has no step lines; "some of each" has at least one fixed step and at least one `The AI plans this part` line; every `Step N` reference (Decisions, Writes, `Used By`, Human Gates `Where`, `; tests` tails) matches a step line or names the AI's part ("the AI's part after Step 2"); every M label is defined once, and a never kept as a Must never rule or a Prohibited action has no M line; no `fixed (check)` (write `fixed (your judgment)`).
- A decision classified from free text is `your criteria` or `open judgment`, never `a rule on a value`.
- No Must never rule restates a Must do rule or an always M line.
- Each requirement lives in one place: a quality of the output is an AC, a behaviour an R; a detail block's Rule line says only what that step adds (how or where: "look each promised link up in C2, for AC4"), never the AC's own wording again, and a Decision isn't restated as an R row.
- The Inputs line matches the access answer for its source.
- No requirement describes a test input ("the notes carry no 'buying for' field").
- Notes for the student (a trace record, a missing-link flag) are never inside the deliverable unless the requirement says they're unmistakable and removed before sending.
- The Workflow node's `generated` is restamped `by: process:deconstruct` with today's date.
