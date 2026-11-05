# The Policy File

Write the policy as one Markdown file. Review mode reads it back, so keep this shape exactly.

## Shape

1. **Frontmatter:** `title` (for example `AI Governance Policy`), `owner` (the person or team from Part 1) and `last_reviewed` (`YYYY-MM-DD`).
2. **An intro paragraph**, in plain words: what the policy is for, who it covers (every AI workflow, skill and agent the company runs), who owns it, and that it is reviewed each quarter and after any incident. Close it with one sentence naming the NIST AI Risk Management Framework as the frame it maps to, citing only direct matches among the rules you wrote: a registry rule maps to Govern 1.6 (an inventory of AI systems), a rule on outside AI tools or vendors to Govern 6 (third-party risk), a re-check or monitoring rule to Manage 4.1 (monitoring after deployment), and the policy's own quarterly review to Govern 1.5 (periodic review of the risk process). Name NIST only in this paragraph.
3. **`## Rules`:** one table with the header exactly `| ID | Rule | Checked by | Since |`.
   - `ID` is `G` and a number (`G1`, `G2`, …), unique and ascending, never reused once a rule is retired.
   - `Rule` is one plain sentence.
   - `Checked by` is one or more items separated by `; `. Each item starts with the name of a check from `## Checks`, optionally followed by `: ` and a short qualifier. A qualifier never contains `;`.
   - **Planned checks.** `(planned)` at the end of a check's `Where it runs` (below) means the check doesn't run at all yet. A `, from` at the end of one `Checked by` item, under a check that does run, marks only that rule's use of it as planned. A check that isn't in place yet keeps its name and ends its qualifier with `, from` and what will deliver it, for example `Weekly registry look: not started yet, from the policy owner's first review`. In Review mode, treat a planned check as not real until it ships, then remove the marker.
   - `Since` is `YYYY-MM-DD`.
4. **`## Checks`:** one table with the header exactly `| Check | Where it runs | Covers |`.
   - `Check` is a plain name, with no link and no formatting.
   - `Where it runs` says where and how often, in plain words; links go here. A check that isn't in place yet ends this cell with `(planned)`, so the table never reads as if it already runs.
   - `Covers` lists rule IDs separated by `, `. Every check covers at least one rule.
5. **`## Retired rules`:** the header exactly `| ID | Rule | Checked by | Since | Retired |`, with `Retired` as `YYYY-MM-DD`. A retired rule moves here and its ID stays reserved. Leave the table empty on a first run.

## Sample

Two rules and the checks that confirm them.

```
## Rules

| ID | Rule | Checked by | Since |
|---|---|---|---|
| G1 | Every AI workflow is in the AI Registry, with a description and an owning team. | Weekly registry look | 2026-11-05 |
| G2 | Every change to a skill or agent is reviewed before it reaches the team. | Release review: before each plugin release; Weekly registry look: new workflows only | 2026-11-05 |

## Checks

| Check | Where it runs | Covers |
|---|---|---|
| Weekly registry look | The policy owner opens the registry dashboard each Monday | G1, G2 |
| Release review | A second person reads each change before a new plugin version is released | G2 |
```

## Updating it (Review mode)

- A reworded rule keeps its ID and gets a new `Since`. Changing only a rule's check (its `Checked by`) isn't a reword: the `Since` stays.
- A retired rule moves to `## Retired rules` with today's date; never delete it or reuse its ID.
- A check whose only rules are retired is retired with them, or moved to a rule that remains.
- After any rule is reworded or retired, re-check the intro's NIST sentence so each mapping still names a rule that exists.

## Before saving

- The three table headers match the exact strings above.
- IDs are unique and ascending, with none reused.
- Every `Checked by` item in `## Rules` names a check in `## Checks`. Retired rules are left out of this check.
- Every check covers at least one rule that isn't retired.
- Every rule has a real or marked-planned check.
- Dates are `YYYY-MM-DD`.
