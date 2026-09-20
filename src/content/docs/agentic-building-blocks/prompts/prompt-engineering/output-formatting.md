---
title: Output Formatting
description: "Output formatting — tell the model exactly how to structure its response as tables, JSON, or templates you define, so results drop straight into your workflow."
---> **Platforms:** `claude` `openai` `gemini` `m365-copilot`

## What It Is

Output formatting means telling the model exactly how to structure its response — whether that's a table, JSON, bullet list, specific sections, or a template you define. Instead of hoping the model picks a useful format, you specify it upfront. This makes outputs immediately usable without manual reformatting.

## Why It Works

LLMs (large language models) are very good at following structural instructions because they've seen millions of formatted documents during training. Specifying format reduces ambiguity about what "a good response" looks like, and makes outputs immediately usable in downstream workflows. However, note that format restrictions can sometimes degrade reasoning performance — Tam et al. (2024) found a tradeoff between structure and thinking quality. For complex analysis, consider letting the model reason freely first, then reformatting.

## When to Use It

- Output needs to feed into another system (JSON, CSV, XML)
- Reports or analyses that need consistent structure across runs
- Comparing multiple items side-by-side (tables)
- When you'll reuse the same prompt and need predictable output
- When output will be parsed programmatically

## The Pattern

```text
{Task description}

Format your response as:
{Format specification — template, example structure, or explicit format name}
```

**Filled-in example:**

```text
Summarize the three main risks of migrating our database from MySQL to PostgreSQL.

Format your response as a markdown table with these columns:
| Risk | Likelihood (High/Med/Low) | Impact | Mitigation |
```

## Examples in Practice

### Example 1 — Table format

**Context:** You need to compare tools and want a scannable side-by-side view.

```text
Compare the following 4 project management tools on these dimensions: price, team size
limit, integrations, and learning curve. Tools: Asana, Linear, Monday.com, Notion.

Present as a markdown table with tools as columns and dimensions as rows.
```

**Why this works:** Tables make comparisons scannable, and specifying rows vs. columns removes ambiguity about the layout.

### Example 2 — JSON output

**Context:** You're extracting structured data from unstructured text for use in an application.

```text
Extract the following fields from this job posting: title, company, location,
salary_range, required_skills (as an array), experience_years.

Return as valid JSON with no additional text or explanation.

Job posting:
[paste job posting text here]
```

**Why this works:** The schema is fully specified — field names, types (array for skills), and the instruction to return only JSON ensures clean, parseable output.

### Example 3 — Template-based

**Context:** You want a consistent format for a recurring report.

```text
Write a weekly status update following this exact structure:

## Completed This Week
- [bullet items]

## In Progress
- [bullet items with % complete]

## Blocked
- [bullet items with blocker description]

## Next Week
- [planned items]

Here's what happened this week: shipped the auth module, 60% done with the dashboard
redesign, waiting on API credentials from the vendor, and next week we start load testing.
```

**Why this works:** The exact template is provided, so the model fills in the structure rather than inventing its own — ensuring consistency across weeks.

## Common Pitfalls

:::caution[Format over substance]
**Problem:** Heavy formatting constraints on reasoning-intensive tasks can reduce output quality. Tam et al. (2024) showed this empirically.
**Fix:** For complex analysis, let the model reason freely first, then ask it to reformat in a follow-up prompt. Separate the *thinking* step from the *formatting* step.
:::
:::caution[Underspecified format]
**Problem:** "Give me a table" without specifying columns, rows, or what goes in each cell leaves too much ambiguity.
**Fix:** Define the exact columns, rows, and what information belongs in each cell. The more specific the format spec, the more useful the output.
:::
:::caution[Incompatible formats]
**Problem:** Asking for "a brief paragraph" and "include all details" simultaneously creates a contradiction.
**Fix:** Choose the format that matches your information density needs. If you need comprehensive detail, use a structured format (table, sections) that can hold more information than a paragraph.
:::
:::note[Platform tip]
Claude supports structured output via tool use and JSON mode. OpenAI has a JSON mode and function calling for guaranteed JSON output. For strict schema adherence, use these platform features rather than relying on prompt instructions alone.
:::
## Related Techniques

- [Direct Instruction](../direct-instruction/) — be explicit about what you want the model to do
- [Few-Shot Learning](../few-shot-learning/) — show format by example
- [Summarization and Distillation](../summarization-and-distillation/) — formatting is especially important for summaries
- [Prompt Engineering Overview](../)
- [Data Analysis use case](../../../../use-cases/data-analysis/) — structured output is critical for data workflows

## Further Reading

- Tam et al. 2024 — *Let Me Speak Freely? A Study on the Impact of Format Restrictions on Performance* — [arxiv.org/abs/2408.02442](https://arxiv.org/abs/2408.02442)
- Liu et al. 2024 — *"We Need Structured Output": Towards User-centered Constraints on LLM Output* — [arxiv.org/abs/2404.07362](https://arxiv.org/abs/2404.07362)
