# Skill test report: template

Use this format for every test round, whether the tests ran automatically or by hand. On Claude Code it sits alongside skill-creator's review page as a summary, not a replacement.

```markdown
# Test report · [skill name]

Round [N] · Platform: [platform] · Ran: [automatically with the skill creator | by hand]
Model: [model, or "the conversation's model"] · [X] test prompts · [Y] trigger prompts

| With the skill | Without the skill | Trigger prompts |
|---|---|---|
| [a] / [b] checks met | [c] / [b] checks met | [d] / [Y] behaved correctly |

## Test prompts

| Test prompt | Check | Without the skill | With the skill | Evidence (with the skill) |
|---|---|---|---|---|
| [short name] | [check] | Met / Not met | Met / Not met | [quote or specific reference] |

## Trigger prompts

| Prompt | Should fire? | Fired? | Result |
|---|---|---|---|
| "[prompt]" | Yes / No (near-miss) | Yes / No | ✓ / ✗ |

## Fix next

1. [the change, and which failed check or trigger it addresses]
2. [...]

Then rerun everything as round [N+1].
```

Rules:

- Use **Met / Not met**, with evidence for every Met.
- Say "without the skill" and "with the skill"; don't call the run without it a "baseline", which some framework tools use for something else.
- Every Not met with the skill, and every trigger marked ✗, leads to a line under **Fix next**.
