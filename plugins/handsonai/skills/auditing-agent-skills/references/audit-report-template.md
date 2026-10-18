# Skill audit report: template

Use this format for every audit. It follows the same conventions as the skill test report in `applying-skill-best-practices` (plain words, a "Fix next" list, nothing changed without approval).

```markdown
# Skill audit · [date]

Platform: [platform] · Checklist: [where it was loaded from]
Checks run: [every criterion in the checklist, by name]
Skills read: [n] ([names]) · Couldn't read: [n] ([names, and why])

| Findings | Skills with findings | Skills with no findings |
|---|---|---|
| [n] | [n] | [n] |

## Findings

| # | Skill | Check | Where | What's wrong | Proposed change |
|---|---|---|---|---|---|
| 1 | [skill] | [criterion] | [line or field] | [plain words] | [before → after] |

## Proposed changes

For each finding that changes a file, the exact change:

**1. [skill] · [field or line]**
Before: `[current text]`
After: `[proposed text]`

## Registry coverage

- Not recorded in the registry: [skill] → suggested workflow: [workflow]
- Not cataloged yet (lives only in a platform account): [skill]
- Registry entries pointing at skills that no longer exist: [entry → skill]

## Fix next

1. [the most important fix first]
2. [...]

Changed: nothing. Reply with the numbers of the fixes to apply, or "all".
```

Rules:

- Number findings so the user can approve them by number.
- Each finding names the exact line or field; never a vague "consider reviewing".
- Leave out empty sections rather than writing "none"; the "Checks run" line shows a check ran even when it found nothing.
- The three counts add up: skills with findings plus skills with no findings equals skills read.
- However many skills you audit, every finding keeps its number and its proposed change. A long report may open with a summary by severity and move the full findings table and changes to an appendix, but never drops them.
- The last line always says what was changed, which before approval is "nothing".
