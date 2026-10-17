# Re-running an existing requirements file

Read when Phase 1's check 3 finds that the workflow already has a requirements file and nothing is built: no `# Skills` or `# Agents` link and no Test results (no registry: a listed `framework/*/requirements.md` matches the workflow the student named, with no `test-results.md` and no built skill or agent in its folder, or the student said it isn't built yet). Once something is built, Deconstruct doesn't re-run; the entry messages in SKILL.md apply.

The re-run is a fresh interview: say the opening, then run Parts 1 to 5 as usual, with every part prefilled from the old file for the student to confirm. Prefilled content counts as *(you said)*. The progress file works as usual, so a re-run stopped midway resumes from it.

## 1. Detect the format

Read the existing `framework/[name]/requirements.md` and decide which format it is:

- **New format:** it has `## Path`. Prefill directly; every label keeps its number. A file with `## Path` but no `Method preference:` line (written before that line existed) plays back as "same way every time".
- **Old step-driven:** a `Definition Type: Step-Driven` row with `## Steps Overview`, or a `## Steps Overview` with no `Definition Type` row.
- **Old goal-driven:** a `Definition Type: Goal-Driven` row with `## Inputs` and no `## Path`, including the legacy `Outcome-Driven` value and an `## Outcome` heading.
- **No markers:** no `## Path` and none of the above. Ask, don't assume: **Ask:** "Your current file doesn't say how it was set up. Does it list the steps the work follows, or only the result you want?"

## 2. Prefill every part

Prefill every part from the old file, value, name and regulation included, and play each back for the student to confirm rather than asking each question fresh. For a file with no markers, the section 1 question comes first, before any playback. After that, this covers every question the old file answers, in every part: play back what the file says ("Your current file says [answer].") and ask "Does that match?" in place of the question. Ask a question as written only when the old file holds no answer to it.

- **Part 1:** the `Value & Measurement` rows, the target and when it can be read included.
- **Part 2:** the name, trigger and deliverable from `Metadata`; the regulation answer from the old `Governing regime` (a heading or a line). An old file with no regime and no `Regulated` row recorded none (old files named a regime only when one applied): say "Your current file records no law or regulation for this work." then ask "Does that match?". Only a `Regulated` row with no regime named gets the law-or-regulation question.
- **Part 3:** the old goal and `Acceptance Criteria` (criteria keep their AC numbers; a criterion the send-back test marks (must) keeps its number), the `Reference example:` and the real output in the Context Inventory. A goal written as a paragraph is sharpened into the goal sentence with the usual blank questions.
- **Part 4, the consistency answer:** an old step-driven file (and a new-format file with no `Method preference:` line) plays back as "same way every time"; an old goal-driven file as "AI works it out each time"; a new-format file plays back its own line. Each is confirmed with "Does that match?", never assumed; on a no, ask the consistency question.
- **Part 4, old step-driven:** each old step becomes a step line. The prefilled path replaces the method question and "What comes after that?". Play it back with the Part 4 playback; when the work is done today, that is the today form, word for word: "Here are your steps: [numbered steps]. Is this how you do it today, or how you'd like it done from now on?", then the one-per-message "Today you also [step or workaround]. Should that stay?" differences; otherwise it ends "What would you change or clarify?". Keep the step numbers where the steps match; a new step gets the next number. Something the student says an old step now also does stays on that step, not a new one. Fold each step's `Step Details` into the step line and a detail block: `Outputs` → `produces`; `Context Needed` → `uses`; `External Action` that sends, posts, creates or changes something in a real system → a W# line under `### Writes` and a `writes` tag (`None (read-only)`, or saving files only to the student's own folder, isn't a write: it's what the step produces); `Rules & Edge Cases` → `**Rule:**` or `**Check or handoff:**`, and decision criteria → Decision lines; `Role` → the role tag. Parallel steps in an old `## Sequence` become `· parallel with` tags. An old `fixed (check)` becomes `fixed (your judgment)`. Then ask the questions the old file can't answer (fixed or flexible and why, who settles each decision).
- **Part 4, old goal-driven:** the old file has no steps. Say: "Your current file records the result you want but no steps, so I've noted that the AI works it out each time. Does that match?" On a yes, follow the "AI works it out each time" branch (no method question, no proposed path); on a no, ask the consistency question. Never present invented steps as the student's. The old `## Inputs` bullets prefill the Inputs and the range.
- **Part 5:** the old `Rules & Constraints`, `Human Gates`, `Context Inventory` and `Security, Privacy & Safety` prefill Part 5's draft messages. They also answer Part 5's opening questions: a Fallback rule (such as "stop and ask") answers the when-unsure question, the Human Gates the taking-part question, and any `External Action` that writes the live-writes question. Existing scenarios keep their E numbers and input files; a new input gets the next number. Message 4 still proposes a row for each risk the old scenarios don't cover (Part 5's message 4), so a re-run usually adds at least one input.

Dropped from the old file: the `Definition Type` row, `## Steps Overview` and `## Step Details` (folded into `## Path`), `## Sequence` and `## Optimization Notes`.

## 3. When the new file is saved

Nothing downstream changes until the new `requirements.md` is saved; stopping the re-run partway changes nothing. Then, in this order:

1. Save the old requirements file with today's date suffix (`requirements-YYYY-MM-DD.md`), unchanged, before writing the new one ("Never silently overwrite").
2. If a Design Plan or Design Spec exists (`design-plan.md` or `design-spec.md`, approved or a draft), save it with today's date suffix (`design-plan-YYYY-MM-DD.md` or `design-spec-YYYY-MM-DD.md`), unchanged, and remove its link from the node's `# Artifacts`. Then say the plan-set-aside message (SKILL.md). Design runs fresh. With no plan, don't say it.
3. Leave the node's `status` as it is, and leave any old `definition_type` field on the node (it is ignored; never add or change it).
