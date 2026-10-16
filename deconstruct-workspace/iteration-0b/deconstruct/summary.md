# Round summary

## I1 — sales-pre-call-brief

Runs: run-1 valid 11/53

- FAIL 0/1 (needs 1) [scripted] The first message contains the opening said exactly as in the spec (section 2), beginning "Deconstruct turns this workflow into a clear, tes
- PASS 1/1 (needs 1) [scripted] Each part opens with "Part N of 5", Part 1 to Part 5 in order
- PASS 1/1 (needs 1) [scripted] No part announces its own time (no minutes on a "Part N of 5" line)
- PASS 1/1 (needs 1) [scripted] The label "Ask:" never appears in any AI message
- FAIL 0/1 (needs 1) [scripted] The words step-driven and goal-driven never appear in any AI message
- FAIL 0/1 (needs 1) [scripted] `requirements.md` has the 12 sections of spec section 4a in this order and no others: `# [Name] — Workflow Requirements`, `## Goal`, `## Val
- PASS 1/1 (needs 1) [scripted] `requirements.md` has no YAML frontmatter
- FAIL 0/1 (needs 1) [scripted] `requirements.md` has no `Definition Type` row and no Sequence or Optimization Notes heading at any level
- FAIL 0/1 (needs 1) [scripted] `## Human Gates` opens with the line `Runs: with you` or `Runs: without you`
- FAIL 0/1 (needs 1) [scripted] `## Security, Privacy & Safety` contains the line `Governing regime: …` before a `### Writes` heading; under `### Writes` there is either a 
- FAIL 0/1 (needs 1) [scripted] Every line under `## Path` that is a step is written `- Step N — [Name] · produces …` with a `fixed (…)` or `flexible` mark, optional tags i
- FAIL 0/1 (needs 1) [scripted] `framework/[name]/deconstruct-in-progress.md` existed during the interview and is deleted once `requirements.md` is written
- PASS 1/1 (needs 1) [scripted] The AI says nothing about the progress file (its name never appears in an AI message)
- FAIL 0/1 (needs 1) [scripted] The close is said word for word: "Workflow Requirements saved to `framework/[name]/requirements.md`. It holds your goal, [N] steps, [M] cont
- FAIL 0/1 (needs 1) [scripted] The Workflow node `registry/workflows/sales-pre-call-brief.md` has `status: under-development`, links `[Requirements](framework/[name]/requi
- PASS 1/1 (needs 1) [scripted] Phase 1 asks "Which workflow from your backlog do you want to map?" with today's Not sure? line ("I'll use those three tests on your backlog
- PASS 1/1 (needs 1) [scripted] Backlog entry uses the candidate's fields: the describe-first question is never asked
- FAIL 0/1 (needs 1) [scripted] Part 2 asks "Is there a law or regulation that governs this work?"
- PASS 1/1 (needs 1) [scripted] After "no" to the law question, no regulation questions and no takes-longer message appear
- FAIL 0/1 (needs 1) [scripted] Part 3 shows the recipe by name: "We'll shape this in three steps: say it, sharpen it, make it checkable."
- FAIL 0/1 (needs 1) [scripted] Part 3 asks the real-example question word for word: "Do you have a recent output of this work that you were happy with — one you'd point to
- FAIL 0/1 (needs 1) [scripted] After the student says yes and pastes the output, the AI asks "What did you start from for that one?"
- FAIL 0/1 (needs 1) [scripted] "Say it" asks "Imagine it's built and working. What does a good one look like?" and then "And what do you do with it next?"
- FAIL 0/1 (needs 1) [scripted] "Make it checkable" opens with "If the AI handed you one of these, could you say done or not done just by looking? What would you look for?"
- FAIL 0/1 (needs 1) [scripted] The goal played back has no "containing" blank, and a second playback after the send-back test begins "Here's your goal now:"
- FAIL 0/1 (needs 1) [scripted] `## Acceptance Criteria` uses the form `1. **AC1 (must)** — …`, has at most two (must) checks, and a `Reference example:` line naming the re
- FAIL 0/1 (needs 1) [scripted] "never name another client" is recorded in `## Rules & Constraints`, not as an acceptance criterion
- FAIL 0/1 (needs 1) [scripted] The AI asks "If you handed this to a skilled colleague, how would you want them to go about it?", then "What comes after that?" after the st
- FAIL 0/1 (needs 1) [scripted] The AI asks "Today you also … Should that stay?" about the LinkedIn-notes workaround, and the dropped workaround is not a step
- FAIL 0/1 (needs 1) [scripted] The AI asks "Which of these does a person do?" and "Which of those must happen exactly that way, every time?", and defines the terms with "*
- FAIL 0/1 (needs 1) [scripted] The CRM-check step is recorded as `fixed (policy)`
- FAIL 0/1 (needs 1) [scripted] The step the student does (reading the brief and adding questions) carries the `(you)` role tag
- FAIL 0/1 (needs 1) [scripted] The student's review point becomes a Human Gates row and the line `Runs: with you`
- FAIL 0/1 (needs 1) [scripted] Decision line D1 is recorded with `settled by: a rule on a value`
- FAIL 0/1 (needs 1) [scripted] Part 4 asks the decisions, range and expertise questions word for word, and ends "Design uses this to decide how much the AI works out on it
- FAIL 0/1 (needs 1) [scripted] With no `writes` tags, live writes is asked with today's question word for word: "Does this workflow write to anything live — send, post, cr
- FAIL 0/1 (needs 1) [scripted] The taking-part and when-unsure questions are asked word for word
- FAIL 0/1 (needs 1) [scripted] Part 5 message 2 introduces context with the R9-1 sentence: "These are the sources it uses, what we call its **context**: any information a 
- FAIL 0/1 (needs 1) [scripted] Part 5 message 4 ends with today's Hand-it-back message word for word
- FAIL 0/1 (needs 1) [scripted] Value & Measurement is closed with "Now that we've reshaped this — what should the number be? What's the target?" and "How long after this g
- PASS 1/1 (needs 1) [scripted] The test inputs are saved as `framework/[name]/inputs/E<n>-<short-name>.md`, numbered from E1, with at least three
- PASS 1/1 (needs 1) [scripted] The real output is saved in the Context Inventory as `framework/[name]/context/C<n>-<short-name>.md`
- FAIL 0/1 (needs 1) [judged, must] Every AI message asks at most one question (a draft message ending "What's wrong or missing?" counts as one)
- FAIL 0/1 (needs 1) [judged] The AI never asks the student to choose a path type (steps versus goal)
- PASS 1/1 (needs 1) [judged] The backlog question's Why names the three tests for a good first workflow (a handful of steps, starts when you decide, works from material 
- FAIL 0/1 (needs 1) [judged] The law question is the last question of Part 2
- FAIL 0/1 (needs 1) [judged] The checks are written with the student during Part 3 (played back before "Part 4 of 5"), not left to the end of the interview
- FAIL 0/1 (needs 1) [judged] "never name another client" is recorded as a Must never rule (an R row), not a check
- FAIL 0/1 (needs 1) [judged, must] The student's long answer about how they do it today (well past a short paragraph) is played back in plain words, one line per step, and tha
- FAIL 0/1 (needs 1) [judged] When the AI plays back steps or sources, it names sources in plain words ("uses your CRM notes"), never as IDs (C#, W#, D#) or the tagged li
- FAIL 0/1 (needs 1) [judged] Part 5 is delivered as four short draft messages, in order: (1) rules and never-dos, (2) the human gates collected so far plus the sources i
- FAIL 0/1 (needs 1) [judged] Before generating, the AI shows the report card Test will fill in and introduces the labels AC, R and G (the labels preview)
- FAIL 0/1 (needs 1) [judged] E1 is the input behind the Golden Example (the calendar invite and CRM record the student started from), and the Golden Example column holds

## R5 — renamed-resume-from-other-skills

Runs: run-1 valid 4/9

- FAIL 0/1 (needs 1) [scripted] Sessions 1 and 2 ("continue my workflow", Deconstruct): the first AI message uses the resume line and the Part 4 signpost
- PASS 1/1 (needs 1) [scripted] Sessions 1 and 2 do not say the Deconstruct opening
- FAIL 0/1 (needs 1) [scripted] Sessions 3 and 4 (Design, Build) name the workflow
- PASS 1/1 (needs 1) [scripted] No session writes a Design Plan or builds a skill
- PASS 1/1 (needs 1) [scripted] No file changes in any session (the progress file stays as saved)
- FAIL 0/1 (needs 1) [judged, must] Sessions 1 and 2: the resume line names Parts 1 to 3 and summarises what was noted; the AI does not show the backlog choice
- FAIL 0/1 (needs 1) [judged] Sessions 1 and 2 resume Monthly Risk Register as the progress file's `Workflow node:` workflow (registry/workflows/program-risk-register.md)
- PASS 1/1 (needs 1) [judged, must] Session 3 (Design): the AI says Deconstruct is unfinished for Monthly Risk Register and routes to Deconstruct (points the student there, or 
- FAIL 0/1 (needs 1) [judged, must] Session 4 (Build): the AI says Deconstruct is unfinished for Monthly Risk Register and routes to Deconstruct; it builds nothing

## R9 — no-registry-built

Runs: run-1 valid 5/14

- FAIL 0/1 (needs 1) [scripted] Session 1: the AI asks "Has this workflow been built yet, even if you haven't tested it?"
- FAIL 0/1 (needs 1) [scripted] Session 1: after "yes" the AI says "This workflow is built but isn't running yet, so the next step is to finish it. Say 'run the test skill'
- PASS 1/1 (needs 1) [scripted] Session 1 never tells the student to say 'continue my workflow'
- FAIL 0/1 (needs 1) [scripted] Session 2: the AI asks the built question, and after "no" the re-run starts with the opening
- FAIL 0/1 (needs 1) [scripted] Session 3 (`readiness: not-ready`, round complete): the built-but-not-running message naming the build skill
- FAIL 0/1 (needs 1) [scripted] Session 4 (`readiness: ready`): the built-but-not-running message naming the run skill
- FAIL 0/1 (needs 1) [scripted] Session 5 (round in progress): the built-but-not-running message naming the test skill
- PASS 1/1 (needs 1) [scripted] Sessions 3 to 6: the built question is not asked
- FAIL 0/1 (needs 1) [scripted] Session 6 (`run-guide.md` present, so running; check 2): the AI says "This workflow already has a Design Plan, so changes to its requirement
- PASS 1/1 (needs 1) [scripted] Session 6 does not say the built-but-not-running message
- PASS 1/1 (needs 1) [scripted] Sessions 1, 3, 4, 5 and 6 do not say the Deconstruct opening
- PASS 1/1 (needs 1) [scripted] No file changes in sessions 1, 3, 4, 5 and 6
- FAIL 0/1 (needs 1) [judged, must] Session 1: the built question is a plain question, with no Why or Not sure? line
- FAIL 0/1 (needs 1) [judged] Session 2: after "no", the AI goes on to prefill from the old requirements file (or says it will) rather than asking every question fresh
