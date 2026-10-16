# Baseline on today's skills (Task 1 Step 9, isolated)

One run each under the Eval safety constraint (harness.py). Expected: I1, R5, R9 and B1 fail against today's skills (RED); the upgrade guard passes. These replace iteration-0/, which ran without isolation.

The first Deconstruct round was voided by the fail-closed check, a false alarm from the account skill sync (R12-3 correction); it was discarded and re-run as `deconstruct/`.

## B1-approved — 8/10 (build/B1-approved)

- FAIL [scripted] Build's opening is today's, word for word
- FAIL [scripted] Build creates the orchestrator skill in the project's skill folder

## B1-unapproved — 4/4 (build/B1-unapproved)


## I1 — 11/53 (deconstruct/I1)

- FAIL [scripted] The first message contains the opening said exactly as in the spec (section 2), beginning "Deconstruct turns this workflow into a clear, testable description of
- FAIL [scripted] The words step-driven and goal-driven never appear in any AI message
- FAIL [scripted] `requirements.md` has the 12 sections of spec section 4a in this order and no others: `# [Name] — Workflow Requirements`, `## Goal`, `## Value & Measurement`, `
- FAIL [scripted] `requirements.md` has no `Definition Type` row and no Sequence or Optimization Notes heading at any level
- FAIL [scripted] `## Human Gates` opens with the line `Runs: with you` or `Runs: without you`
- FAIL [scripted] `## Security, Privacy & Safety` contains the line `Governing regime: …` before a `### Writes` heading; under `### Writes` there is either a `- W1 · …` line or t
- FAIL [scripted] Every line under `## Path` that is a step is written `- Step N — [Name] · produces …` with a `fixed (…)` or `flexible` mark, optional tags in the spec's order (
- FAIL [scripted] `framework/[name]/deconstruct-in-progress.md` existed during the interview and is deleted once `requirements.md` is written
- FAIL [scripted] The close is said word for word: "Workflow Requirements saved to `framework/[name]/requirements.md`. It holds your goal, [N] steps, [M] context items, [K] accep
- FAIL [scripted] The Workflow node `registry/workflows/sales-pre-call-brief.md` has `status: under-development`, links `[Requirements](framework/[name]/requirements.md)` in `# A
- FAIL [scripted] Part 2 asks "Is there a law or regulation that governs this work?"
- FAIL [scripted] Part 3 shows the recipe by name: "We'll shape this in three steps: say it, sharpen it, make it checkable."
- FAIL [scripted] Part 3 asks the real-example question word for word: "Do you have a recent output of this work that you were happy with — one you'd point to and say 'exactly li
- FAIL [scripted] After the student says yes and pastes the output, the AI asks "What did you start from for that one?"
- FAIL [scripted] "Say it" asks "Imagine it's built and working. What does a good one look like?" and then "And what do you do with it next?"
- FAIL [scripted] "Make it checkable" opens with "If the AI handed you one of these, could you say done or not done just by looking? What would you look for?" and the send-back t
- FAIL [scripted] The goal played back has no "containing" blank, and a second playback after the send-back test begins "Here's your goal now:"
- FAIL [scripted] `## Acceptance Criteria` uses the form `1. **AC1 (must)** — …`, has at most two (must) checks, and a `Reference example:` line naming the real output's C# ID
- FAIL [scripted] "never name another client" is recorded in `## Rules & Constraints`, not as an acceptance criterion
- FAIL [scripted] The AI asks "If you handed this to a skilled colleague, how would you want them to go about it?", then "What comes after that?" after the student's method stops
- FAIL [scripted] The AI asks "Today you also … Should that stay?" about the LinkedIn-notes workaround, and the dropped workaround is not a step
- FAIL [scripted] The AI asks "Which of these does a person do?" and "Which of those must happen exactly that way, every time?", and defines the terms with "**Fixed** means it mu
- FAIL [scripted] The CRM-check step is recorded as `fixed (policy)`
- FAIL [scripted] The step the student does (reading the brief and adding questions) carries the `(you)` role tag
- FAIL [scripted] The student's review point becomes a Human Gates row and the line `Runs: with you`
- FAIL [scripted] Decision line D1 is recorded with `settled by: a rule on a value`
- FAIL [scripted] Part 4 asks the decisions, range and expertise questions word for word, and ends "Design uses this to decide how much the AI works out on its own."
- FAIL [scripted] With no `writes` tags, live writes is asked with today's question word for word: "Does this workflow write to anything live — send, post, create, or change some
- FAIL [scripted] The taking-part and when-unsure questions are asked word for word
- FAIL [scripted] Part 5 message 2 introduces context with the R9-1 sentence: "These are the sources it uses, what we call its **context**: any information a step needs to do its
- FAIL [scripted] Part 5 message 4 ends with today's Hand-it-back message word for word
- FAIL [scripted] Value & Measurement is closed with "Now that we've reshaped this — what should the number be? What's the target?" and "How long after this goes live before that
- FAIL [judged] Every AI message asks at most one question (a draft message ending "What's wrong or missing?" counts as one)
- FAIL [judged] The AI never asks the student to choose a path type (steps versus goal)
- FAIL [judged] The law question is the last question of Part 2
- FAIL [judged] The checks are written with the student during Part 3 (played back before "Part 4 of 5"), not left to the end of the interview
- FAIL [judged] "never name another client" is recorded as a Must never rule (an R row), not a check
- FAIL [judged] The student's long answer about how they do it today (well past a short paragraph) is played back in plain words, one line per step, and that playback ends "Wha
- FAIL [judged] When the AI plays back steps or sources, it names sources in plain words ("uses your CRM notes"), never as IDs (C#, W#, D#) or the tagged line format
- FAIL [judged] Part 5 is delivered as four short draft messages, in order: (1) rules and never-dos, (2) the human gates collected so far plus the sources it uses, (3) how you'
- FAIL [judged] Before generating, the AI shows the report card Test will fill in and introduces the labels AC, R and G (the labels preview)
- FAIL [judged] E1 is the input behind the Golden Example (the calendar invite and CRM record the student started from), and the Golden Example column holds the real output's C

## R5 — 4/9 (deconstruct/R5)

- FAIL [scripted] Sessions 1 and 2 ("continue my workflow", Deconstruct): the first AI message uses the resume line and the Part 4 signpost
- FAIL [scripted] Sessions 3 and 4 (Design, Build) name the workflow
- FAIL [judged] Sessions 1 and 2: the resume line names Parts 1 to 3 and summarises what was noted; the AI does not show the backlog choice
- FAIL [judged] Sessions 1 and 2 resume Monthly Risk Register as the progress file's `Workflow node:` workflow (registry/workflows/program-risk-register.md), not as a new workf
- FAIL [judged] Session 4 (Build): the AI says Deconstruct is unfinished for Monthly Risk Register and routes to Deconstruct; it builds nothing

## R9 — 5/14 (deconstruct/R9)

- FAIL [scripted] Session 1: the AI asks "Has this workflow been built yet, even if you haven't tested it?"
- FAIL [scripted] Session 1: after "yes" the AI says "This workflow is built but isn't running yet, so the next step is to finish it. Say 'run the test skill'."
- FAIL [scripted] Session 2: the AI asks the built question, and after "no" the re-run starts with the opening
- FAIL [scripted] Session 3 (`readiness: not-ready`, round complete): the built-but-not-running message naming the build skill
- FAIL [scripted] Session 4 (`readiness: ready`): the built-but-not-running message naming the run skill
- FAIL [scripted] Session 5 (round in progress): the built-but-not-running message naming the test skill
- FAIL [scripted] Session 6 (`run-guide.md` present, so running; check 2): the AI says "This workflow already has a Design Plan, so changes to its requirements go through Improve
- FAIL [judged] Session 1: the built question is a plain question, with no Why or Not sure? line
- FAIL [judged] Session 2: after "no", the AI goes on to prefill from the old requirements file (or says it will) rather than asking every question fresh

## U3 — 12/14 (upgrade-guard/U3)

- FAIL [scripted] The resume orientation names Step 5 (Test) as next (today's line: "You've completed through Step [N] ([name]) — next is Step [N+1] ([name]).")
- FAIL [scripted] Test resumes the round with today's line, naming 1 of 3 graded ("N of M graded — run E(next) in a new chat next")

## U4 — 2/5 (upgrade/U4)

- FAIL [scripted] The AI says "This workflow already has a Design Plan, so changes to its requirements go through Improve. Say 'run the improve skill'."
- FAIL [scripted] Deconstruct does not re-run: no AI message says the Deconstruct opening (the 10.0 opening or 9.1's)
- FAIL [judged] The AI gives the Improve message on its own (it may name the workflow) and starts no interview, design, build or test work

## Notes

- U4 checks the new Improve message, so it fails on today's skills by design; it is a forward test, not the guard. U3 is the guard (Test resume on a 9.1 round).
- U3's two misses were wording-only (today's skill paraphrased "Step 5 (Test) is next" and "graded 1 of 3"); the guard checks were loosened to behaviour after this run.
- B1-unapproved passes today: today's Build already refuses an unapproved plan, so only B1-approved is RED.
- B1-approved: today's Build skipped its opening line (build/SKILL.md:25), a real miss.
