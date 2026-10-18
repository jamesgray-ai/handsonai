---
name: authoring-framework-skills
description: >-
  Use when writing, editing, or reviewing any of the seven AI Workflow Framework skills
  (analyze, deconstruct, design, build, test, run, improve) or any other student-facing
  handsonai plugin skill that interviews a user. That includes adding or rewording a
  question, adding or splitting a phase, changing an opening or closing message, fixing a
  finding from a student walkthrough, and the consistency review across all seven skills
  before a release. Not for docs pages, lesson guides, or skills that never talk to a student.
---

# Authoring Framework Skills

The framework skills are the course's teacher whenever James is not in the room. Students are
non-technical business professionals (managers, consultants, operators, founders) running the
skills on Claude, Claude Code, ChatGPT, Codex, or M365 Copilot. **A skill must teach everything a
student needs to answer its questions, at the moment they need it**, without sending them to
handsonai.info, a slide deck, or a recording.

Every framework skill follows the same six-part teaching standard, the same language rules, and
the same file format, so moving from Analyze to Improve feels like one guide, not seven.

**Two readers, two voices.** A SKILL.md is instructions to the model, written in the imperative
("Ask…", "Record…"). Text in quotation marks is what the student hears. The language rules below
govern the quoted text strictly; instruction text can use internal terms (`Workflow node`,
`AC1`), because the student never sees it.

## The teaching standard

### 1. Open: the first message of the skill

The opening says five things, in this order, in a short paragraph (about five sentences; joining two is fine):

1. **What this step does**, in one plain sentence.
2. **What you'll have at the end**: the named deliverable and where it's saved.
3. **How long it takes**: an honest range for a first-timer.
4. **The parts**: "It runs in N parts: (1) …, (2) …".
5. **Why the next step needs it**, plus "Stopping early is safe — progress is saved, and 'continue my workflow' picks up where we left off."

Then, once per skill run, offer the switch: "I'll explain the questions that need it, and 'not sure'
is always a fine answer. If you've done this before, say 'skip the explanations'."

Define no framework terms in the opening, except the one or two the deliverable is named by, in one clause each (Analyze's **candidate workflow** and **backlog**). Each other term is defined where it first matters (see Terms);
front-loading three definitions before the first question overloads the student. A one-line
outline of what the step builds (with a two- or three-word gloss per level) is allowed, as long
as it comes once and in the student's persona words — it is a map, not a set of definitions.

Deconstruct's opening is the reference: it gives the agenda, not just the time.

### 2. Signposts: one line at each transition

Format: **"Part N of M — [plain name]."** The student hears *parts*. Phases are internal and
their numbers never appear in quoted text, so the student only ever sees one count. Group
phases into 3–6 parts; a part can hold several phases.

### 3. Question blocks: teaching at the point of asking

The students are savvy business professionals. Every line they read has to earn its place, and
every line in the skill costs context the model needs for the interview. So a question gets only
the teaching lines it needs, and each line is tested on its own:

- **Why:** only when answering needs a framework concept the student hasn't met yet (a gate, a
  check, fixed or flexible, an autonomy level), or when what the answer is used for isn't obvious
  from the question.
- **Example:** only when the question asks for a judgment the student has probably never made
  about their work ("what must it never do?", "what should the target be?"). Never when the
  question lists its own choices or examples, or opens with a draft.
- **Not sure?:** only when it records a specific default that later steps depend on ("Insist on
  none for now", "Leave it flexible"). Every other "not sure" is handled by the thin-answer recipe
  (section 5), with no scripted line.
- A walkthrough finding that shows students getting stuck on a question is a reason to add the
  line that would have unstuck them, and only that line.

A plain factual question about the student's own work ("What kicks it off?", "Who does this
step?", "Does it exist yet?") is just the question. Teaching every question bloats the skill,
buries the instructions that matter, and makes a capable reader wade through reasons they didn't
need.

Every question the student hears carries the **Ask:** label, so the model can always find the exact
wording. The label is for the model only; the student never sees it (on screen it reads like a form
field). Write one instruction near the skill's first question block: "Never show the **Ask:** label.
The student sees only the question itself; the *Why*, *Example*, and *Not sure?* lines keep their
labels." A plain factual question is just the **Ask:** line; any other question gets only the lines
that pass the tests above, in this order and format, exactly:

```markdown
**Ask:** "[the question, in the student's words]"
- *Why:* [one sentence: what this answer is used for, ideally by a later step]
- *Example:* [a short answer from a different line of work than the student's]
- *Not sure?* [the default the skill records, or one concrete way to find the answer]
```

Rules for each part:

- **Why**, when a question has one, is said in the same message as the question the first time it's asked, even after "skip the explanations"; when the same question repeats (once per step or item), later asks are the question alone. A question whose purpose isn't obvious from its words needs a *Why*: the student should never wonder why they're spending effort on it. The *Why* must be true today: never promise what a later step doesn't yet do. One sentence, tied to a use: "Test checks every gate you name here, so this sets what a passing run looks like." When a *Why* names what a later step does with the answer, check that step's skill says so before committing; a wrong *Why* teaches the student something false.
- **Example** comes from a deliberately different line of work (expense approvals, a recruiting coordinator, a property manager), at the same altitude as the question. It must never be an answer the student could copy for their own workflow. Pick the domain at authoring time and write it in; don't tell the model to "give an example". Like *Why*, *Example* and *Not sure?* go with a question's first ask only; a repeat of the same question is the question alone.
- **Example collision.** The student's line of work isn't known when the skill is written, so an example can land in their own field. Write this instruction once near the skill's first question block: "If the student works in the field an *Example* comes from, skip that *Example* and go straight to *Not sure?*." Don't write backup examples.
- **A draft replaces the example.** When a question opens with a draft built from the student's own source or earlier answers, leave out the *Example* line — the draft already shows the shape. Keep *Why* and *Not sure?*.
- **Exact wording.** Mark definitions, **Ask:** lines, and *Why* / *Example* / *Not sure?* lines as "say exactly this" in the skill, so the model doesn't paraphrase them or add reassurance (it turned "You can't pick wrong" into "There's no wrong answer"). Openings and playbacks may be paraphrased if every part is there; an outline of the step's structure is exact.
- **Proposals are not examples.** Proposing an answer drawn from what the student already told you ("From the steps we mapped, I'd put a gate before the send — does that fit?") is encouraged; it's how propose-and-react works. The *Example* line is different: it shows the shape of a good answer, so it must come from someone else's work.
- **Not sure?**, when a question has one, gives the safe default the skill will record and says it was a default. Never leave a student with no way forward: where a question has no *Not sure?* line, the thin-answer recipe is the way forward.
- Example and Not sure? are shown by default and dropped after "skip the explanations". The student can still ask for them.
- **Say how much is needed.** Where a conscientious student could over-answer (a typical case, a description of their method), write the "how much" line into the question block ("*Not sure?* One sentence is enough; you'll paste real notes later."). Never leave it to the model to improvise.
- **Every message ends with a question or a clear next action.** A message that only informs (a preview, a summary) ends by saying what happens next and what to say ("Next, I'll write your Workflow Requirements file. Say 'go ahead', or tell me anything to change first.").
- **No framework step numbers inside the interview.** In questions and teaching lines, name a later step in plain words ("when we test it", "Design, the next step"), never "Step 5": inside an interview it collides with the workflow's own steps. Routing and orientation lines ("You've completed through Step 2 (Deconstruct) — next is Step 3 (Design).") keep the number with the name.

### 4. Terms: defined on first use, paired with the plain meaning

The first time a framework term reaches the student, say the term and its plain meaning together
in one sentence, with the student's own case where possible: "That's a **human gate** — a point
where a person must review or approve before the workflow continues. In your case, that's you
reading the email before it goes." After that, the term alone is fine. Students learn the
vocabulary because they meet it explained, not as a label (Design's playback already works this way).

Use the canonical definitions so every skill says the same thing:

| Term | Plain meaning (say this) | Canonical source |
|---|---|---|
| Workflow | One piece of repeated work, from what kicks it off to the thing it produces | Analyze |
| Candidate workflow | A specific, repeatable piece of work worth building with AI | Analyze, opening |
| Lens | The point of view Analyze takes on your work: organizational (the processes across the business, end to end) or individual (the work you personally do each day) | Analyze, Phase 2 |
| Context | Any information a step needs to do its job: documents, spreadsheets, emails, style guides, or knowledge that lives in someone's head | Deconstruct, Phase 4 |
| Step-driven / goal-driven | Step-driven: you can describe every path the work takes. Goal-driven: you can describe what "done" looks like, but the path depends on what comes in | Deconstruct, The Two Paths |
| Human gate | A point where a person must review or approve before the workflow continues | Deconstruct, Phase 7 |
| Acceptance criterion | A yes/no statement about the output that you can check after one run | Deconstruct, Phase 12 |
| Value lever | The kind of value AI creates here: Streamline, Automate, Accelerate, or Create value | Analyze, Phase 4 |
| Autonomy level | How much the AI decides: Deterministic (you give instructions), Guided (it makes bounded decisions with your method), Autonomous (you give it a goal) | Design, Phase 4 |
| Building block | One of the pieces a workflow is built from: a prompt, a skill, an agent, a connection to another system | Design |
| Line of business | Something distinct the business offers — like a product line, a service, or a training program | scaffolding-registry, Phase 2 |
| Function | A team or department in your organization — Marketing, Sales, Finance — that owns a kind of work across every line of business. Lines of business are *what you offer*; functions are *who does the work*. Working alone, each function is one of the hats you wear | scaffolding-registry, Phase 3 (wording per persona in `personas.md`) |
| Process | A set of related work that delivers part of a line of business — like enrolling students or delivering a workshop. Each sits under one line of business and is owned by one function; Analyze later finds the workflows inside it | scaffolding-registry, Phase 4 |
| Registry | Your record of the business: what you do, the processes that deliver it, and the workflows built or planned for each | scaffolding-registry |
| Backlog | Your list of workflows to build: every candidate Analyze found, until you start one | Analyze, opening |

When a skill's own text defines a term differently, the skill named in the source column wins:
fix the table, not the skill, and check the other skills against the corrected wording.

### 5. Thin answers: coach, don't accept

When an answer is too vague to write a requirement from, follow this recipe:

1. Play back what you have: "So far I have: [their words]."
2. Ask one narrower follow-up anchored in a real instance: "Think of the last time you did this. What happened first?"
3. If it's still thin after two tries, propose an answer to react to: "Here's my guess — what's right and what's wrong?"
4. If they still don't know, record `Unknown` (or the stated default) and move on. Never invent an answer and record it as theirs.

### 6. Close: the last thing the student hears

The close says four things: **what you made** (with counts), **where it's saved**, **what the
next step does with it and how long it takes**, and **the exact phrase to start it**.
Deconstruct's close is the reference: "Workflow Requirements saved to `framework/[name]/requirements.md`. It holds your goal, [N] steps, … Step 3, Design, reads this file and decides how the workflow gets built … in about 30 minutes. Start it with 'run the design skill'."

## Language and tone for a business audience

The student is a capable professional who is new to building with AI. Write as a peer who
explains clearly, not as a teacher correcting them or an engineer briefing another engineer.

**Rules for quoted (student-facing) text:**

- **Plain words first.** Short sentences, second person, active voice. If a sentence would make a seller or an operations manager stop to decode it, rewrite it.
- **No technical vocabulary the student didn't introduce**, unless the step's job is to teach it (Design and Build name building blocks; pair each with its meaning, per Terms).
- **No clever compression.** No aphorisms, two-word punchlines, or metaphors standing in for the point ("the tell", "load-bearing", "the substrate").
- **No analogies by default.** Explain with the student's own workflow. Add an analogy only when a concept doesn't land from the real case.
- **Never frame the student as behind.** No "most people miss this", "what nobody tells you", "the part everyone gets wrong". State what the thing is and what it does.
- **No unsupported prevalence claims** in quoted text ("most people undercount steps by 30–50%"). If a pattern matters, say what to do about it: "Let's check for steps that happen without you thinking about them."
- **No stock phrases.** No "Sound familiar?", "Great question!", "Let's dive in", "There are no wrong answers", "Your turn".
- **Never show raw file syntax for approval.** Play a draft back as labeled plain text (Name · What it does · Owner), never as frontmatter, Markdown headings, or file names; write the format behind it and offer "Want to see the file itself?" once.
- **Label every level.** Any playback holding more than one level of the registry (lines of business and processes, processes and workflows) names each level on its line ("**Line of business:** …", "**Process:** … — what it covers. **Owner:** Marketing", owner last) and uses one kind of list marker.
- **Never offer a required step as an option.** If the step must happen (the dashboard at the end of registry setup), do it and say so. Offer a choice only when either answer is fine ("run Analyze now, or later?"). Students skip anything labeled optional.
- **Don't report empty checks or machinery.** Never list what a scan didn't find, and never give a lint rule, a GENERATED block, a template, JSON, or a maintenance pass as the reason for a question or in a close. Give the student's reason, or say nothing.
- **Platform-neutral.** Quoted text never names a feature only one platform has, except in a line the skill explicitly gates to that platform ("On Claude: …"), offered once. Platform-specific facts live only in `registries/platform-registry.json` (see the Framework skill conventions in `CLAUDE.md`).
- **Exact product names:** Claude, Claude Code, ChatGPT, Codex, M365 Copilot. "Markdown" takes a capital M in prose.

**Swap list for words that reach the student:**

| Instead of | Say |
|---|---|
| artifact (generic) | file, document, or the thing it produces (name it). "Claude Artifact" is a product name and stays |
| invoke / trigger the skill | run / start the skill |
| node, frontmatter, schema | your registry entry, the details at the top of the file |
| repo, directory | folder |
| orchestration | how the steps are coordinated |
| deterministic (unexplained) | follows your instructions the same way every time |
| edge case | an unusual case |
| input / output (unexplained) | what it starts from / what it produces |
| leverage, utilize | use |
| lint, check passed, warnings | (say nothing, or the plain consequence) |
| commit, push, branch, git | "save this point in your folder's history" — only when the folder is a git repository, with "it stays on your computer" |

## File format

Every framework skill keeps this shape (existing v8 conventions in `CLAUDE.md` still apply):

- **Frontmatter:** `name` and `description` only. The description is plain prose in a `>` folded scalar: no XML tags, no `<example>` blocks. It opens "This skill should be used when…", names the trigger phrases students actually type (including "continue my workflow"), and ends "This is Step N (Name) of the AI Workflow Framework."
- **Body order:** `# Title` → one-paragraph purpose → `## Workflow` (opening instruction, the `> **Registry entry:**` note, then `#### Phase N — Name` sections) → `## Output` or `## Outputs` → `## Guidelines`.
- **Phases:** `#### Phase N — Name`, or `#### Phase N (goal-driven) — Name`. The docs page's "How the Skill Works" list mirrors them one for one (`scripts/check-framework-consistency.sh`).
- **Self-contained teaching.** Question blocks, term definitions, and examples are written into each skill's own folder (its SKILL.md or its own `references/`). Never point a skill at another skill's file for its teaching: a skill uploaded alone to ChatGPT or M365 Copilot can't reach it.
- **Size limits.** The SKILL.md body stays **under 5,000 tokens and under 500 lines** (the Agent Skills standard, agentskills.io/specification; Anthropic's *Skill authoring best practices* gives the same 500-line limit). Estimate tokens as about 1.3 per word, so roughly 3,800 words. The whole SKILL.md loads when the skill starts and stays in context for the entire interview, so only what every student needs belongs in it.
- **Reference files for the rest.** Content only some students need (a variant, a template, handling old documents) goes in the skill's own `references/` folder, loaded only when needed. SKILL.md names each reference file and when to read it, one line each. References stay one level deep: a reference file never points on to another file. A reference file over 100 lines starts with a short table of contents.
- **One skill per framework step, and where each piece goes.** Students start a step with one phrase. Put each piece of a step where it fits:
  - **A separate skill** only when the piece is useful on its own (a student would run it by itself) or two or more steps need it: registry updates (`indexing-registry`), naming (`naming-workflows`). The step names it in one line.
  - **A reference file** when it is one part of one step's interview or a variant only some students need. Don't make interview parts into skills: a part-skill can start on its own with no goal behind it, breaks a step uploaded alone to ChatGPT or M365 Copilot, adds to every session's skill list, and saves no context over a full run.
  - **A script** when the work is procedural (file names and dates, registry links, progress, structure checks), with a written fallback in the skill's own `references/` for platforms that can't run code.
- **Test parts without splitting.** An evaluation can start a step from a saved, partly filled record (the resume path) and check one part's output, so a part is testable on its own without becoming a skill. Scripts are tested directly.
- **Size discipline.** Teaching adds words, so pay for them: when a teaching line goes in, cut the instruction text it replaces (a bare question, a restated rule, a "be clear" reminder). Report each skill's SKILL.md word count, estimated tokens and line count before and after in the commit message, and explain any growth across the walkthrough in the PR.
- **Guidance changes.** The limits above were checked against the Agent Skills standard, Anthropic and OpenAI guidance on 2026-10-15. Recheck them before each release review; skill guidance changes as the platforms mature.

## Before and after: Deconstruct, Phase 7

**Before** (instruction only; the student gets a bare question):

> Ask once, after the sequence is mapped: "Where must a person review or approve before the workflow continues — and where should it just run?" Record each answer as a row `G1, G2, …` in Human Gates.

**After:**

> Ask once, after the sequence is mapped. Introduce the term first: "That brings us to **human gates** — points where a person must review or approve before the workflow continues."
>
> **Ask:** "Looking at your steps, where must you (or someone else) check or approve before it moves on, and where should it just run?"
> - *Why:* Test checks every gate you name, and Design uses them to decide how much the AI can do on its own.
> - *Example:* A recruiting coordinator might say: "I approve the interview slots before invitations go out; scheduling the room can just run."
> - *Not sure?* Start with one gate: you review the result before anyone else sees it. You can add more after testing.
>
> Record each answer as a row `G1, G2, …` in Human Gates with the step it sits at. Apply the *Not sure?* default by the last step: if the workflow sends, posts, or hands its result to someone else, record a gate before that step and mark it `(default)`; if the student is the only one who receives the result, write "No human gates — the workflow runs end-to-end with final review only."

## Making a fix

A skill's rules are restated in many places, and a fix that changes one copy leaves the others
contradicting it. Every fix pass does these, in order, before it is committed. For a rewrite of a whole skill, write
its evaluations first (at least three scenarios that show what the skill must get right), following
Anthropic's evaluation-first guidance, and write only the instructions needed to pass them.

1. **Sweep.** For each rule you change, search for every place that restates it: the skill's
   `SKILL.md` and every file in its `references/`, the other framework skills, the `SCHEMA.md`
   copies (`plugins/handsonai/skills/scaffolding-registry/references/schema-template.md`,
   `registry-template/registry/SCHEMA.md`, `examples/weekly-status-report/registry/SCHEMA.md`),
   and the docs pages under `src/content/docs/`. Fix them in the same commit.
2. **Check claims about other skills.** Any *Why*, close, or "Step N will…" that says what another
   skill does must match that skill's file. If it doesn't do that yet, change it or change the claim.
3. **Run the checks:** `bash scripts/check-framework-consistency.sh`,
   `bash scripts/check-registry-consistency.sh`, `bash scripts/test-compose-registry.sh`.
4. **Independent review.** A reviewer with no conversation context checks every fixed finding
   against the diff and looks for contradictions across the skill folder, other skills, and docs.
   Fix what it finds and review again until it comes back clean. Only then re-run the skill.

## Evaluating a skill

The harness lives in `deconstruct-workspace/evals/` (`run_eval.py`, `check_scripted.py`, `grade_eval.py`; how to run it is in its `evals.json`). Reuse it for every framework skill.

- **What to write.** One eval per behaviour the skill must get right, plus a replay of each student walkthrough: a script holding the student's real answers, so every finding from that run is checked. A replay that holds real business details stays local and is never committed.
- **How it runs.** A second AI plays the student from a fixed script; the skill runs isolated from the real Claude config and every repo. Scripted checks test exact wording and file content; a grader judges behaviour from the transcript and the files alone.
- **Write checks the way the skill is written.** Quote approved lines word for word. A check accepts a known answer being said instead of asked. A judged item that depends on a reference (a question matrix) carries that reference in its text, because the grader sees nothing else. An approved line that asks two things in one sentence counts as one question, and the one-question item lists it. Student scripts use the skill's current wording. After every skill change and before every paid round, run the quote check (`python3 check_quotes.py`): every line an eval quotes word for word must still be in the skill, so no check tests retired wording. Format checks (a file's line order, a tag) aren't covered; review those by hand when a format changes.
- **Pass bar.** Scripted and must-level judged checks pass every run (3 of 3); other judged checks pass at least 2 of 3, and every miss is listed.
- **Diagnose every miss before changing anything.** It is a skill gap (fix the skill) or a check stricter or looser than the approved rule (fix the check). Never change a check just to make a run pass; when the rule itself is unclear, get a decision and record it.
- **Rounds.** A small smoke round first, to measure cost per run; then rounds scoped to what changed; then a full round. Get cost approval before each. Defer evals that exercise a skill not yet rewritten. After a fix, re-check and re-judge the saved runs first (no new runs), then re-run only what the fix touched.

## Review checklist

Run this on every edited skill before committing, and across all seven before a release:

- [ ] The opening has all five parts and offers "skip the explanations".
- [ ] Signposts read "Part N of M — name"; no phase number appears in quoted text.
- [ ] Every *Why*, *Example* and *Not sure?* line passes its own test in Question blocks; plain factual questions are just the question.
- [ ] Every quoted question carries **Ask:**.
- [ ] The skill tells the model never to show the **Ask:** label to the student.
- [ ] Every example comes from a different line of work and could not be copied as the student's answer; the example-collision line is present once.
- [ ] Every *Why* that names a later step has been checked against that step's skill, and every question whose purpose isn't obvious has a *Why*.
- [ ] Questions a student could over-answer say how much is needed; every message ends with a question or a next action; no interview line names a framework step by its number.
- [ ] Every *Not sure?* records a default later steps depend on, and defaults are recorded as defaults.
- [ ] Each framework term is defined on first use, matching the terms table.
- [ ] The thin-answer recipe is followed; nothing invented is recorded as the student's answer.
- [ ] The close names what was made, where, what's next, how long, and the exact phrase to start.
- [ ] Quoted text passes the language rules and the swap list.
- [ ] No playback shows raw file syntax; every multi-level playback labels each level.
- [ ] No required step is offered as "optional" or one of "options".
- [ ] The file format matches; `bash scripts/check-framework-consistency.sh` passes.
- [ ] SKILL.md is under 5,000 tokens and 500 lines; content only some students need is in `references/`, one level deep, each named in SKILL.md with when to read it.
- [ ] Word count, estimated tokens and line count before and after are reported.
- [ ] Every changed rule was swept across the skill folder, other skills, `SCHEMA.md` copies, and docs.
- [ ] Every claim about another skill was checked against that skill's file.
- [ ] An independent review came back clean before the re-run.

## Common mistakes

| Mistake | Fix |
|---|---|
| Telling the model "explain why you're asking" instead of writing the reason | Write the exact *Why* line. An instruction to explain produces seven different explanations. |
| An example from the student's own field (a sales example in a sales workflow) | Move it to a different line of work. The student will copy it. |
| A question block on every question | Test each line on its own: *Why* for a new concept or an unclear use, *Example* for a judgment never made before, *Not sure?* for a default later steps depend on. |
| A *Why* on a factual question ("Who does this step?") | Cut it. The use is obvious to a capable reader. |
| Splitting a step's interview into several skills | Keep one skill per step: interview parts and variants go in `references/`, procedural work in scripts; a separate skill only for a piece that stands on its own or that two or more steps share. |
| A teaching paragraph before the question | One-line *Why* with the question; the rest goes in Example and Not sure?. |
| "Adapt the example to their role" | Write a fixed example from another line of work. An adapted example is the student's answer. |
| Defining several terms in the opening | Define each term where it first matters. |
| "Phase 3 of 6" shown to the student | "Part 2 of 4 — [name]". |
| Defining a term differently from another skill | Use the terms table wording. |
| Fixing the output after a walkthrough but not the skill | Fix the skill text that produced it, then re-run the step. |
