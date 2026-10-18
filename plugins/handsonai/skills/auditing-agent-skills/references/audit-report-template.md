# Skill audit report: template

Use this format for every audit. It follows the same conventions as the skill test report in `applying-skill-best-practices` (plain words, a "Fix next" list, nothing changed without approval).

```markdown
# Skill audit · [date]

Platform: [platform] · Checklist: [where it was loaded from]
Checks run: [every criterion in the checklist, by name]
Skills read: [n] ([names]) · Couldn't read: [n] ([names, and why])
Batch: [k] of [m] · Next: [names, or "none, this is the last batch"]

| Findings | Skills with findings | Skills with no findings |
|---|---|---|
| [n] | [n] | [n] |

## Findings

| # | Severity | Skill | Check | Where | What's wrong | Proposed change |
|---|---|---|---|---|---|---|
| 1 | [high, medium or low] | [skill] | [criterion] | [line or field] | [plain words] | [before → after, or the action and the file it creates or updates] |

## Proposed changes

For each finding that changes a file (including registry entries and the sources list), the exact change:

**1. [skill] · [field or line]**
Before: `[current text]`
After: `[proposed text]`

## Registry coverage

- Not recorded in the registry: [skill] → add `[skill link]` to the skills list in `[workflow file]` (or create `[new workflow file]`, named [name])
- Not cataloged yet (lives only in a platform account): [skill]
- Registry entries pointing at skills that no longer exist: [entry → skill]

## Fix next

1. [the most important fix first]
2. [...]

Changed: nothing. Reply with the numbers of the fixes to apply, "all", or (when batching) "next" for the next batch.
```

Rules:

- Number findings so the user can approve them by number.
- Each finding names the exact line or field; never a vague "consider reviewing".
- Leave out empty sections rather than writing "none"; the "Checks run" line shows a check ran even when it found nothing.
- Severity, where a summary groups findings: **high** would do the wrong thing if the skill ran (a retired model, a broken reference, a write to a system no longer used); **medium** gives misleading guidance or leaves a gap (a dated fact, an overlap, a weak description, missing test cases, a skill the registry doesn't record, a stale source); **low** is naming and wording.
- The three counts add up: skills with findings plus skills with no findings equals skills read.
- Every finding keeps its number and its proposed change. A long report may open with a summary by severity and move the full findings table and changes to an appendix, but never drops them.
- Include the "Batch" line only when the set is audited in batches.
- The last line always says what was changed, which before approval is "nothing", and, when batching, offers the next batch.
