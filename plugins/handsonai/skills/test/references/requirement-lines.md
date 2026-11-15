# Requirement line formats

Read when Test changes `requirements.md` (SKILL.md, *Changing a requirement*). These are the formats Deconstruct writes the file in; Test keeps them exactly, so every step and script reads the file the same way. Test carries its own copy so it never depends on another skill's files (on ChatGPT and in Cowork, only this skill's files may be there).

**Contents:** 1. The lines Test writes · 2. Numbering · 3. A removed line · 4. The `revisions` entry · 5. The hand check · 6. Lines and headers Test reads or writes for Deconstruct's newer formats

## 1. The lines Test writes

Each goes in its own section's table, in the leader's words, in this shape:

- **An AC line,** in `## Acceptance Criteria`: `[n]. **AC5 (must)** — [yes-or-no statement]`; ` (must)` only on a must-have. Each line is one thing a single run's output either does or doesn't do.
- **An R line,** in `## Rules & Constraints`: `| R6 | When | When [this happens], it [does that]. |`. `Kind` is `Always`, `Never`, `When` or `Fallback`; an `Always` rule reads "It always…", a `Never` rule "It never…". A rule a person carries out ends with ` · (you)` or ` · ([role])` and isn't graded on the output. A prohibition on acting ("It never emails a customer") is a P line under Prohibited actions, not an R line; a "stop and ask" Fallback also has a checkpoint.
- **A G line,** in `## Human Gates`: `| G2 | Step 3 | When the draft is ready, it stops until you approve it. · (you) |`. `Where` is `Step N` or the AI's part ("the AI's part after Step 2"); the checkpoint is in the "When… it…" shape, names who performs it, and ends with the role tag. The section's first line stays `Runs: with you` or `Runs: without you`; with no checkpoints left, under it: "No human gates — the workflow runs end-to-end with final review only."
- **A P line,** in `## Security, Privacy & Safety`, under its category's table (`### Boundaries`, `### Access`, `### Traceability` or `### Prohibited actions`): `| P3 | [the constraint, in plain words] | [its source: a person, a policy, a control ID, or Self] |`. A table that doesn't exist yet is added with its heading and columns (`| ID | Constraint | Source |`), in that category order; a prohibited action reads "It never [acts], whoever asks." The `Governing regime:` line and `### Writes` stay where they are.

- **The policy line,** after `Governing regime:` and before `### Writes`: Test only rewrites it, on the policy confirm question's answer: `Policy check: Allowed` on a yes, `Policy check: No — not live until approved` on a "no" (SKILL.md, *Changing a requirement*, step 7). It has no ID.

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

`plan_unaffected: true` only for a change settled by re-grading (SKILL.md, *Changing a requirement*, step 4), and on the policy line's change, whose `lines` holds the fixed token `Policy check`:

```yaml
revisions:
  - revision: 4
    by: test
    lines: [Policy check]
    plan_unaffected: true
``` Switching `track:` to `full` doesn't raise `revision`.

## 5. The hand check

Where code can run, `requirements-check.js` checks the file (SKILL.md). Where it can't, or it doesn't finish, check by hand before going on:

- the frontmatter holds `revision`, `revisions` and `track`, with a `revisions:` entry for every revision above 1;
- the eleven `##` sections are unchanged in name and order;
- every line you wrote is in its section's shape above, with a label in its series and no number reused;
- every `tests:` header in `inputs/` names only lines the file still has;
- Human Gates still opens with the `Runs:` line, and every P line has an ID and a Source;
- no password or key is in any saved file;
- a `Policy check:` line, if any, is once, right after `Governing regime:` and before `### Writes`, reading one of its five values (section 6);
- every input you wrote has its header lines in order (`source:`, `tests:`, then `expect:` where section 6 needs it), then one blank line.

## 6. Lines and headers Test reads or writes for Deconstruct's newer formats

A file without these reads as before.

- **A D line,** in `### Decisions` under the Path: `- D1 (Step 3): When [condition], it [path] · settled by: [a rule on a value | your criteria | open judgment][ · criteria: [the leader's words]][ · value read by AI]`. Test never writes one; it grades it (SKILL.md, *The check list*). `tests:` may name D lines.
- **An input's header:** `source:` (`deconstruct`, `design`, `test` or `flag`), `tests:` (AC, R, G and D IDs; a `source: flag` input names the R and P lines it presents), then an optional `expect: [what should happen, in plain words]`, then one blank line, then the input. Test writes `expect:` on every input it writes for a `D` line, an out-of-bounds `When` line or carry-over (from that line's own wording), on the empty or malformed input, the instruction-carrying input, and every safety input.
- **A safety input:** `source: flag`, unlisted in Example Scenarios like the flag input, `tests:` naming the R or P lines whose temptation it presents, with `expect:`. Outside the cap of 8.
- **A carry-over input:** its body opens with one paragraph, `Earlier run: [what an earlier run left behind, in plain words]`, then a blank line, then the input. Set-up, never input.
- **The policy line's five values:** `Policy check: Allowed` · `Policy check: No — [source] left out` · `Policy check: No — details removed first (Step [N])` (or `(R[n])`) · `Policy check: No — not live until approved` · `Policy check: Not sure — to check`. No line means none was asked, and nothing blocks.
- **Metadata rows** `Starts`, `Per run` and `Remembers`, a `W` line's `· after each run` (a flag to the leader), and the four glosses under their headings: Test reads them and never changes them.
