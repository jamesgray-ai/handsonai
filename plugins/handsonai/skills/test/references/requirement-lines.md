# Requirement line formats

Read when Test changes `requirements.md` (SKILL.md, *Changing a requirement*). These are the formats Deconstruct writes the file in; Test keeps them exactly, so every step and script reads the file the same way. Test carries its own copy so it never depends on another skill's files (on ChatGPT and in Cowork, only this skill's files may be there).

**Contents:** 1. The lines Test writes · 2. Numbering · 3. A removed line · 4. The `revisions` entry · 5. The hand check · 6. Lines and headers Test reads or writes for Deconstruct's newer formats

## 1. The lines Test writes

Each goes in its own section's table, in the leader's words, in this shape:

- **An AC line,** in `## Acceptance Criteria`: on an 11.0 file (one with `## Output`), `[n]. **AC5** — [yes-or-no statement] · from: [I#, C#, R# or the output alone]`, never `(must)`; on a 10.x file, its own shape, `[n]. **AC5** — [yes-or-no statement]`, with no new `(must)`. Each line is one thing a single run's output either does or doesn't do.
- **An R line,** in `## Rules & Constraints`: `| R6 | When | When [this happens], it [does that]. |`. `Kind` is `Always`, `Never`, `When` or `Fallback`; an `Always` rule reads "It always…", a `Never` rule "It never…". A rule a person carries out ends with ` · (you)` or ` · ([role])` and isn't graded on the output. A prohibition on acting ("It never emails a customer") is a P line under Prohibited actions, not an R line; a "stop and ask" Fallback also has a checkpoint.
- **A G line,** in `## Human Gates`: `| G2 | After the draft is ready | When the draft is ready, it stops until you approve it. · (you) |`. `Where` is the moment in plain words; only in an older file whose Path has steps is it `Step N` or the AI's part ("the AI's part after Step 2"). The checkpoint is in the "When… it…" shape, names who performs it, and ends with the role tag. The section's first line stays `Runs: with you` or `Runs: without you`; with no checkpoints left, under it: "No human gates — the workflow runs end-to-end with final review only."
- **A P line,** in `## Security, Privacy & Safety`, under its category's table (`### Boundaries`, `### Access`, `### Traceability` or `### Prohibited actions`): `| P3 | [the constraint, in plain words] | [its source: a person, a policy, a control ID, or Self] |`. A table that doesn't exist yet is added with its heading and columns (`| ID | Constraint | Source |`), in that category order; a prohibited action reads "It never [acts], whoever asks." The `Governing regime:` line and `### Writes` stay where they are.

- **The policy line,** after `Governing regime:` and before `### Writes`: Test only rewrites it, on the policy confirm question's answer: `Policy check: Allowed` on a yes, `Policy check: No — not live until approved` on a "no" (*Changing a requirement*, step 7, below). It has no ID.

Every rule, checkpoint and decision keeps the "When… it…" shape; no "It never…" restates an "It always…"; a quality of the output is an AC line, a behaviour an R line, never both.

## 2. Numbering

Labels: `AC1`…, `R1`…, `G1`…, `P1`… (one series across the four Security tables). A new line takes the next number in its series; numbers are never renumbered, and a removed line's number is never reused. No other label family appears.

## 3. A removed line

It comes out of its table, out of every `tests:` header in `inputs/` that names it, and its ID goes in the `revisions` entry's `lines`. On an 11.0 file, an R line removed also comes out of every check's `· from:` that names it: the check keeps its other sources. A check that named only that rule then has nothing to come from: never convert it on your own. Ask the leader once, in your own words, whether to keep that check or drop it *(your words)*; kept, its source becomes `· from: the output alone`, and say so to them in plain words; dropped, it is removed as a line too (its ID in the entry's `lines`). Never leave a check naming a line the file no longer has. An input left testing nothing moves to `history/E[n]-[short-name]-YYYY-MM-DD-HHMM.md`, and its `## Example Scenarios` row, if it has one, is removed in the same write (the table's last row stays: give its `tests:` the lines the input still exercises). Nothing in `history/` is ever deleted.

## 4. The `revisions` entry

In the frontmatter, in block form, never as `{ … }`, after the existing entries (keep every entry other steps wrote), with `revision` raised by one:

```yaml
revisions:
  - revision: 3
    by: test
    lines: [R2]
    plan_unaffected: true
```

`plan_unaffected: true` only for a change settled by re-grading (*Changing a requirement*, step 4, below), and on the policy line's change, whose `lines` holds the fixed token `Policy check`:

```yaml
revisions:
  - revision: 4
    by: test
    lines: [Policy check]
    plan_unaffected: true
```

Switching `track:` to `full` doesn't raise `revision`.

## 5. The hand check

Where code can run, `requirements-check.js` checks the file (*Changing a requirement*, step 3, below). Where it can't, or it doesn't finish, check by hand before going on:

- the frontmatter holds `revision`, `revisions` and `track`, with a `revisions:` entry for every revision above 1;
- the `##` sections are unchanged in name and order (twelve on an 11.0 file, with `## Output` after `## Goal`; eleven on a 10.x file);
- every line you wrote is in its section's shape above, with a label in its series and no number reused;
- every `tests:` header in `inputs/` names only lines the file still has;
- Human Gates still opens with the `Runs:` line, and every P line has an ID and a Source;
- no password or key is in any saved file;
- a `Policy check:` line, if any, is once, right after `Governing regime:` and before `### Writes`, reading one of its five values (section 6);
- every input you wrote has its header lines in order (`source:`, `tests:`, then `expect:` where section 6 needs it), then one blank line.

## 6. Lines and headers Test reads or writes for Deconstruct's newer formats

A file without these reads as before.

- **A D line,** in `### Decisions` under the Path: `- D1: When [condition], it [path] · settled by: [a rule on a value | your criteria | open judgment][ · criteria: [the leader's words]][ · value read by AI]` (in an older file with steps, `- D1 (Step 3): When …`). Test never writes one; it grades it (SKILL.md, *The check list*). `tests:` may name D lines.
- **An input's header:** `source:` (`deconstruct`, `design`, `test` or `flag`), `tests:` (AC, R, G and D IDs; a `source: flag` input names the R and P lines it presents), then an optional `expect: [what should happen, in plain words]`, then one blank line, then the input. Test writes `expect:` on every input it writes for a `D` line, an out-of-bounds `When` line or carry-over (from that line's own wording), on the empty or malformed input, the instruction-carrying input, and every safety input.
- **A safety input:** `source: flag`, unlisted in Example Scenarios like the flag input, `tests:` naming the R or P lines whose temptation it presents, with `expect:`. Outside the cap of 8.
- **A carry-over input:** its body opens with one paragraph, `Earlier run: [what an earlier run left behind, in plain words]`, then a blank line, then the input. Set-up, never input.
- **The policy line's five values:** `Policy check: Allowed` · `Policy check: No — [source] left out` · `Policy check: No — details removed first (Step [N])` (or `(R[n])`) · `Policy check: No — not live until approved` · `Policy check: Not sure — to check`. No line means none was asked, and nothing blocks.
- **Metadata rows** `Starts`, `Per run` and `Remembers`, a `W` line's `· after each run` (a flag to the leader), and the four glosses under their headings: Test reads them and never changes them.

## Changing a requirement

N-T6 + N-T7's add or drop, a requirement-level miss and a what-change at the real example all change `requirements.md`, which Test may do:
1. **A fixed step, or a line a law requires, stays.** A line fixed by regulation or policy, or a rule or checkpoint that names a law as its reason ("…, as [the law] requires."): say "[The step] is required by [the rules / your policy], so it stays." then the next action. ([The step] names the rule or checkpoint, in plain words, for a line a law requires.) Never removed or loosened, whatever the leader says.
2. **Loosening a rule** (a checkpoint, an "It always…" or "It never…" line, any rule) asks once: **Ask:** "Removing this means it'll [the consequence]. Remove it?" (folded into N-T14 when that's the question that led here).
3. **Write it:** the line in the leader's words, in the formats above (the table's columns, its `Kind` values and an 11.0 check's `· from:`; never a `(must)` marker; a new line takes the next number in its series, and a removed line's number is never reused); `revision` raised; a `revisions:` entry (`by: test`, the line IDs), written in block form, never as `{ … }`:
   ```yaml
   revisions:
     - revision: 3
       by: test
       lines: [R2]
       plan_unaffected: true
   ```
   (`plan_unaffected: true` only as step 4 says); and the change under Requirement changes in the results (made before the file exists, its `revisions:` entry is copied in when the file is written; the next round's file when this one waits on the plan). **A line removed** also comes out of every `tests:` header in `inputs/` that names it, and, on an 11.0 file, an R line out of every check's `· from:` that names it (section 3); a check that named only that rule is the leader's to keep or drop, asked once, never converted to `the output alone` on your own (section 3). An input left testing nothing moves to `history/E[n]-[short-name]-YYYY-MM-DD-HHMM.md`, and its Example Scenarios row, if it has one, is removed in the same write, its E ID in the entry's `lines` (the table's last row stays: give its `tests:` the lines the input still exercises, by your reading). Then, where code can run, run `node [plugin root]/tools/requirements-check.js [workflow folder]` (never mentioned to the leader) and fix any problem it names before going on; where it can't, or it doesn't finish, check what you wrote by hand (section 5).
4. **Settled by re-grading:** dropping or loosening a line the built workflow doesn't enforce. Mark the entry `plan_unaffected: true`, re-grade the runs already done in place, and carry on.
5. **Needs the plan:** an added or tightened line, or a removed checkpoint the workflow still enforces. The raised `revision` sends the workflow to Design; write no change request. Re-grade the runs already done against the new line. In Part 1 the round waits (above); in Part 3 it's Not ready, with N-T34's plan clause.
6. Recompute coverage; a new line with no input gets one, shown to the leader with N-T59 before it's saved, run or graded (SKILL.md, *The inputs you wrote*).
7. **The policy check,** the answer to the policy confirm question (Phase 3): a yes rewrites the line as `Policy check: Allowed`; a "no" writes or keeps `Policy check: No — not live until approved`. Either way `revision` is raised and the entry is `by: test`, `lines: [Policy check]`, `plan_unaffected: true`, in block form as in step 3 (`Policy check` is a fixed token, since the line has no ID), logged under Requirement changes. Nothing goes to Design.

