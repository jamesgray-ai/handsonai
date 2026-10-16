# Re-running an existing requirements file

Read when Phase 1's check 3 finds that the workflow already has a requirements file and nothing is built: no `# Skills` or `# Agents` link and no Test results (no registry: a listed `framework/*/requirements.md` matches the workflow the student named, with no `test-results.md` and no built skill or agent in its folder, or the student said it isn't built yet). Once something is built, Deconstruct doesn't re-run; the entry messages in SKILL.md apply.

The re-run is a fresh interview: say the opening, then run Parts 1 to 5 as usual, with every part prefilled from the old file for the student to confirm. Prefilled content counts as *(you said)*. The progress file works as usual, so a re-run stopped midway resumes from it.

## 1. Detect the format

Read the existing `framework/[name]/requirements.md` and decide which format it is:

- **New format:** it has `## Path`. Prefill directly; every label keeps its number.
- **Old step-driven:** a `Definition Type: Step-Driven` row with `## Steps Overview`, or a `## Steps Overview` with no `Definition Type` row.
- **Old goal-driven:** a `Definition Type: Goal-Driven` row with `## Inputs` and no `## Path`, including the legacy `Outcome-Driven` value and an `## Outcome` heading.
- **No markers:** no `## Path` and none of the above. Ask, don't assume: [[3a: question asking the student how to read an old requirements file that carries none of the format markers, before anything is prefilled]]

## 2. Prefill every part

Prefill every part from the old file, value, name and regulation included, and play each back for the student to confirm rather than asking each question fresh.

- **Part 1:** the `Value & Measurement` rows.
- **Part 2:** the name, trigger and deliverable from `Metadata`; the regulation answer from the old `Governing regime` (a heading or a line); with none recorded, ask the law-or-regulation question.
- **Part 3:** the old goal and `Acceptance Criteria` (criteria keep their AC numbers; a criterion the send-back test marks (must) keeps its number), the `Reference example:` and the real output in the Context Inventory. A goal written as a paragraph is sharpened into the goal sentence with the usual blank questions.
- **Part 4, old step-driven:** each old step becomes a step line. Keep the step numbers where the steps match; a new step gets the next number. Fold each step's `Step Details` into the step line and a detail block: `Outputs` → `produces`; `Context Needed` → `uses`; `External Action` (other than `None (read-only)`) → a W# line under `### Writes` and a `writes` tag; `Rules & Edge Cases` → `**Rule:**` or `**Check or handoff:**`, and decision criteria → Decision lines; `Role` → the role tag. Parallel steps in an old `## Sequence` become `· parallel with` tags. Then ask the questions the old file can't answer (fixed or flexible and why, who settles each decision).
- **Part 4, old goal-driven:** the old file has no steps. Run the method question and its follow-ups as usual (or, if the student has no method, propose the path, each AI-added step marked `· proposed by AI`); never present invented steps as the student's. The old `## Inputs` bullets prefill the Inputs and the range. [[3a: line telling the student, at Part 4 of a re-run from an old goal-driven file, that the old file recorded no steps, before the method question]]
- **Part 5:** the old `Rules & Constraints`, `Human Gates`, `Context Inventory` and `Security, Privacy & Safety` prefill the four draft messages. Existing scenarios keep their E numbers and input files; a new input gets the next number.

Dropped from the old file: the `Definition Type` row, `## Steps Overview` and `## Step Details` (folded into `## Path`), `## Sequence` and `## Optimization Notes`.

## 3. When the new file is saved

Nothing downstream changes until the new `requirements.md` is saved; stopping the re-run partway changes nothing. Then, in this order:

1. Save the old requirements file with today's date suffix (`requirements-YYYY-MM-DD.md`), unchanged, before writing the new one ("Never silently overwrite").
2. If a Design Plan or Design Spec exists (`design-plan.md` or `design-spec.md`, approved or a draft), save it with today's date suffix (`design-plan-YYYY-MM-DD.md` or `design-spec-YYYY-MM-DD.md`), unchanged, and remove its link from the node's `# Artifacts`. Then say the plan-set-aside message (SKILL.md). Design runs fresh. With no plan, don't say it.
3. Leave the node's `status` as it is, and leave any old `definition_type` field on the node (it is ignored; never add or change it).
