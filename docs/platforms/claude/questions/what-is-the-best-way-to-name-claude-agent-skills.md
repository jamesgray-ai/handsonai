---
question: "What is the best way to name Claude agent skills?"
short_answer: "Name skills using a gerund verb-noun pattern that describes the action and its context, like 'writing-workflow-sops' or 'registering-building-blocks', so the name alone tells you what the skill does."
platforms: [claude]
topic: agents
date: 2026-02-02
author: James Gray
---

# What is the best way to name Claude agent skills?

**Short answer:** Name skills using a verb-noun pattern that describes the action and its context, like 'writing-workflow-sops' or 'registering-building-blocks', so the name alone tells you what the skill does.

## The Full Answer

Anthropic's official best practices recommend using **gerund form** (verb + -ing) as the primary naming pattern for agent skills. This clearly describes the activity or capability the skill provides. For example, `processing-pdfs` immediately tells you the skill handles PDF processing, and `writing-documentation` tells you it writes docs.

The `name` field in a skill's YAML frontmatter has specific technical constraints: maximum 64 characters, lowercase letters, numbers, and hyphens only. You cannot use XML tags or reserved words like "anthropic" or "claude" in the name. These constraints keep names clean, URL-friendly, and consistent across the platform.

Beyond the gerund convention, the most important principle is **consistency within your skill collection**. If you name one skill `writing-workflow-sops`, don't name the next one `sop-writer` or `create-sops`. Pick a pattern and stick with it. Consistent naming makes skills easier to reference in documentation, understand at a glance, search through, and maintain as your library grows.

Noun phrases like `pdf-processing` and action-oriented names like `process-pdfs` are acceptable alternatives, but mixing patterns within the same collection creates confusion.

## Naming Examples

**Gerund form (recommended):**

| Skill Name | What It Does |
|-----------|--------------|
| `processing-pdfs` | Handles PDF text extraction and manipulation |
| `analyzing-spreadsheets` | Analyzes tabular data in spreadsheets |
| `writing-documentation` | Generates documentation content |
| `managing-databases` | Manages database operations |
| `testing-code` | Runs and manages code tests |

**Acceptable alternatives:**

| Pattern | Example |
|---------|---------|
| Noun phrase | `pdf-processing`, `spreadsheet-analysis` |
| Action-oriented | `process-pdfs`, `analyze-spreadsheets` |

**Avoid these patterns:**

| Pattern | Examples | Why |
|---------|----------|-----|
| Vague names | `helper`, `utils`, `tools` | Tells you nothing about what the skill does |
| Overly generic | `documents`, `data`, `files` | Too broad to be useful |
| Reserved words | `anthropic-helper`, `claude-tools` | Blocked by the platform |
| Inconsistent patterns | Mixing `writing-docs` with `pdf-processor` | Creates confusion in your library |

## Key Takeaways

- Use **gerund form** (verb + -ing) as the default naming pattern: `writing-`, `processing-`, `analyzing-`
- Keep names under 64 characters using only lowercase letters, numbers, and hyphens
- Be consistent across your entire skill collection — don't mix naming patterns
- The name should tell you what the skill does without reading the description
- Avoid reserved words (`anthropic`, `claude`) and vague names (`helper`, `utils`)

## Related Questions

- [Official Anthropic skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices#naming-conventions)
