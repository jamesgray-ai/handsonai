# Choosing model and effort

First check the platform's `skill_settings` in the platform registry. Only where it says a skill can choose its own model and effort does any of this go in the skill. Everywhere else, the model and settings chosen for the conversation apply, and the skill should say nothing about them.

## Where a skill can choose (Claude Code)

Two frontmatter fields, both optional:

```yaml
model: sonnet        # a /model value, or inherit (the default: use the session's model)
effort: medium       # low, medium, high, xhigh or max
```

They apply while the skill runs. With `context: fork`, `model` sets the forked subagent's model.

## Effort levels

| Level | Use for |
|---|---|
| `low` | Short, well-scoped jobs where speed matters: formatting, simple lookups, subagents that do one thing |
| `medium` | Most everyday skills: a balance of quality, speed and cost |
| `high` | Complex reasoning, careful judgment, long instructions to follow strictly |
| `xhigh` | Long agentic runs (30 minutes or more) with many steps and tool calls |
| `max` | Only the hardest problems; it costs far more and can overthink simpler work |

Defaults differ by model (at the time of writing, medium on Claude Opus 5.5 and Haiku 5.5, high on other models), which is one reason to set effort deliberately rather than inherit it.

## How to choose

1. Start from the job, not the model: how much judgment does a typical run need?
2. Pick the lowest level that clears your test cases. Run the tests at that level and one level up; keep the lower one if the results hold.
3. Pin a model only when the skill needs it (a fast, cheap model for a high-volume helper; the most capable model for a skill whose mistakes are costly). Otherwise leave `model` unset so the skill follows the user's choice.
4. Give the user the reason in one line, so they can change it knowingly.

A skill with no tests has no basis for choosing a level. Prepare the tests first (see `evaluations.md`).
