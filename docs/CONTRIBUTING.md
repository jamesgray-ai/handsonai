# Contributing to the Cookbook

Thank you for contributing to the Maven AI/ML Cookbook! This guide explains how to add new content.

## Types of Content

| Type | Location | Purpose | Template |
|------|----------|---------|----------|
| How-To Guide | `how-to/` | Solve a specific problem | [how-to-template.md](./_templates/how-to-template.md) |
| Topic | `topics/` | Explain a concept | [topic-template.md](./_templates/topic-template.md) |
| Pattern | `patterns/` | Document reusable approaches | Use topic template |
| Troubleshooting | `troubleshooting/` | Fix common errors | Use how-to template |

## Adding a How-To Guide

1. Copy `_templates/how-to-template.md` to the appropriate subdirectory in `how-to/`
2. Name the file descriptively: `stream-responses.md`, `handle-rate-limits.md`
3. Fill in all sections of the template
4. Add a link to the section's README.md index
5. Add platform tags to help readers find relevant content

### How-To Naming Convention

- Use lowercase with hyphens: `my-guide-name.md`
- Start with a verb when possible: `configure-`, `handle-`, `implement-`
- Be specific: `stream-openai-responses.md` not `streaming.md`

## Adding a Topic

1. Copy `_templates/topic-template.md` to the appropriate subdirectory in `topics/`
2. Name the file after the concept: `function-calling.md`, `context-windows.md`
3. Fill in all sections of the template
4. Add a link to the section's README.md index

### Topic Naming Convention

- Use lowercase with hyphens: `my-topic-name.md`
- Use nouns or noun phrases: `prompt-caching.md`, `tool-use-basics.md`

## Writing Guidelines

### Be Practical

- Include working code examples
- Show real-world use cases
- Mention common pitfalls

### Be Specific

- State which platforms/models apply
- Include version numbers when relevant
- Note any prerequisites

### Be Concise

- Get to the point quickly
- Use bullet points for lists
- Keep code examples minimal but complete

## Platform Tags

Use these tags to indicate which platforms a guide applies to:

- `openai` - OpenAI GPT models and APIs
- `claude` - Anthropic Claude models
- `gemini` - Google Gemini models
- `m365-copilot` - Microsoft 365 Copilot
- `all` - Applies to all platforms

## Updating Indexes

When you add a new file, update the README.md in that section to include a link:

```markdown
## Guides

- [How to Stream Responses](./stream-responses.md) - `openai` `claude`
- [How to Handle Rate Limits](./handle-rate-limits.md) - `all`
```

## Questions?

If you're unsure where something belongs or how to structure it, check existing entries for examples.
