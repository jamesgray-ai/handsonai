# Requirement line formats

Read when Test changes `requirements.md` (SKILL.md, *Changing a requirement*). These are the formats Deconstruct writes the file in; Test keeps them exactly, so every step and script reads the file the same way. Test carries its own copy so it never depends on another skill's files (on ChatGPT and in Cowork, only this skill's files may be there).

**Contents:** 1. The lines Test writes · 2. Numbering · 3. A removed line · 4. The `revisions` entry · 5. The hand check

## 1. The lines Test writes

Each goes in its own section's table, in the leader's words, in this shape:

- **An AC line,** in `## Acceptance Criteria`: `[n]. **AC5 (must)** — [yes-or-no statement]`; ` (must)` only on a must-have. Each line is one thing a single run's output either does or doesn't do.
- **An R line,** in `## Rules & Constraints`: `| R6 | When | When [this happens], it [does that]. |`. `Kind` is `Always`, `Never`, `When` or `Fallback`; an `Always` rule reads "It always…", a `Never` rule "It never…". A rule a person carries out ends with ` · (you)` or ` · ([role])` and isn't graded on the output. A prohibition on acting ("It never emails a customer") is a P line under Prohibited actions, not an R line; a "stop and ask" Fallback also has a checkpoint.
- **A G line,** in `## Human Gates`: `| G2 | Step 3 | When the draft is ready, it stops until you approve it. · (you) |`. `Where` is `Step N` or the AI's part ("the AI's part after Step 2"); the checkpoint is in the "When… it…" shape, names who performs it, and ends with the role tag. The section's first line stays `Runs: with you` or `Runs: without you`; with no checkpoints left, under it: "No human gates — the workflow runs end-to-end with final review only."
- **A P line,** in `## Security, Privacy & Safety`, under its category's table (`### Boundaries`, `### Access`, `### Traceability` or `### Prohibited actions`): `| P3 | [the constraint, in plain words] | [its source: a person, a policy, a control ID, or Self] |`. A table that doesn't exist yet is added with its heading and columns (`| ID | Constraint | Source |`), in that category order; a prohibited action reads "It never [acts], whoever asks." The `Governing regime:` line and `### Writes` stay where they are.

Every rule, checkpoint and decision keeps the "When… it…" shape; no "It never…" restates an "It always…"; a quality of the output is an AC line, a behaviour an R line, never both.

## 2. Numbering

Labels: `AC1`…, `R1`…, `G1`…, `P1`… (one series across the four Security tables). A new line takes the next number in its series; numbers are never renumbered, and a removed line's number is never reused. No other label family appears.

## 3. A removed line

It comes out of its table, out of every `tests:` header in `inputs/` that names it, and its ID goes in the `revisions` entry's `lines`. An input left testing nothing moves to `history/E[n]-[short-name]-YYYY-MM-DD-HHMM.md`, and its `## Example Scenarios` row, if it has one, is removed in the same write (the table's last row stays: give its `tests:` the lines the input still exercises). Nothing in `history/` is ever deleted.

## 4. The `revisions` entry

In the frontmatter, in block form, never as `{ … }`, after the existing entries (keep every entry other steps wrote), with `revision` raised by one:

```yaml
revisions:
  - revision: 3
    by: test
    lines: [R2]
    plan_unaffected: true
```

`plan_unaffected: true` only for a change settled by re-grading (SKILL.md, *Changing a requirement*, step 4). Switching `track:` to `full` doesn't raise `revision`.

## 5. The hand check

Where code can run, `requirements-check.js` checks the file (SKILL.md). Where it can't, or it doesn't finish, check by hand before going on:

- the frontmatter holds `revision`, `revisions` and `track`, with a `revisions:` entry for every revision above 1;
- the eleven `##` sections are unchanged in name and order;
- every line you wrote is in its section's shape above, with a label in its series and no number reused;
- every `tests:` header in `inputs/` names only lines the file still has;
- Human Gates still opens with the `Runs:` line, and every P line has an ID and a Source;
- no password or key is in any saved file.
