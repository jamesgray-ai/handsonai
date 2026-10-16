# Round summary

## R9 — no-registry-built

Runs: run-1 valid 1/6

- 0/1 [judged] Session 1: the AI asks "Has this workflow been built yet, even if you haven't tested it?" (no Why or Not sure? line); after "yes" it says "T
- 1/1 [judged] Session 1 never tells the student to say 'continue my workflow'
- 0/1 [judged] Session 2: after "no", the re-run starts (the opening, then prefill from the old file)
- 0/1 [judged] Session 3 (`readiness: not-ready`, round complete): "This workflow is built but isn't running yet, so the next step is to finish it. Say 'ru
- 0/1 [judged] Session 4 (`readiness: ready`): "This workflow is built but isn't running yet, so the next step is to finish it. Say 'run the run skill'."; 
- 0/1 [judged] Session 5 (round in progress): "This workflow is built but isn't running yet, so the next step is to finish it. Say 'run the test skill'."; 

## I5 — no-method

Runs: run-1 valid 1/18

- 0/1 [scripted] The run ends before the turn cap
- 0/1 [judged] The first message contains the opening said exactly as in the spec (section 2), beginning "Deconstruct turns this workflow into a clear, tes
- 0/1 [judged] Each part opens with "Part N of 5" and its name (Part 1 What this is worth … Part 5 Rules, where you check or approve its work, the sources 
- 0/1 [judged] Every AI message asks at most one question (a draft message ending "What's wrong or missing?" counts as one)
- 1/1 [judged] The label "Ask:" never appears in any AI message
- 0/1 [judged] The words step-driven and goal-driven never appear in any AI message, and the AI never asks the student to choose a path type
- 0/1 [judged] `requirements.md` has these sections in this order: `# [Name] — Workflow Requirements`, `## Goal`, `## Value & Measurement`, `## Metadata`, 
- 0/1 [judged] `## Human Gates` opens with the line `Runs: with you` or `Runs: without you`
- 0/1 [judged] `## Security, Privacy & Safety` contains the line `Governing regime: …` before a `### Writes` heading; under `### Writes` there is either a 
- 0/1 [judged] Every line under `## Path` that is a step is written `- Step N — [Name] · produces …` with a `fixed (…)` or `flexible` mark, tags in the spe
- 0/1 [judged] `framework/[name]/deconstruct-in-progress.md` existed during the interview (after Part 2) and is deleted once `requirements.md` is written
- 0/1 [judged] The close says "Workflow Requirements saved to `framework/[name]/requirements.md`." with the counts, names Step 3 Design and "run the design
- 0/1 [judged] The Workflow node has `status: under-development`, links `[Requirements](framework/[name]/requirements.md)` in `# Artifacts`, and has no `de
- 0/1 [judged] `## Path` opens with the line `Path: proposed by AI`
- 0/1 [judged] The AI asks "Which of these would you insist on?" and does not ask "Which of those must happen exactly that way, every time?"
- 0/1 [judged] The customer-approval step is recorded `fixed (your judgment)` without `· proposed by AI`
- 0/1 [judged] Every other proposed step is `flexible` and carries `· proposed by AI`
- 0/1 [judged] The person-and-role question ("Which of these does a person do?") and questions 4 to 6 (decisions, range, expertise) are still asked
