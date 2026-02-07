---
title: Contributing to Hands-on AI
description: How to add content — questions, how-to guides, topics, and patterns — to the AI Cookbook
---

# Contributing to Hands-On AI

Thank you for contributing to Hands-On AI! This guide explains how to add new content.

## Site Structure

| Section | Location | Purpose |
|---------|----------|---------|
| Agentic Building Blocks | `agentic-building-blocks/` | The six AI building blocks (Prompts, Context, Projects, Skills, Agents, MCP) |
| Business-First AI Framework | `business-first-ai-framework/` | Three-phase methodology (Discover, Deconstruct, Build) |
| Platforms | `platforms/` | Platform-specific content (Claude, OpenAI, Gemini, M365 Copilot) |
| Builder Setup | `builder-setup/` | Tool setup and installation guides |
| Patterns | `patterns/` | Document reusable approaches |
| Courses | `courses/` | Structured learning paths (course-specific) |

## Content Types and Templates

| Type | Template |
|------|----------|
| Question (AEO) | [question-template.md](./_templates/question-template.md) |
| How-To Guide | [how-to-template.md](./_templates/how-to-template.md) |
| Topic | [topic-template.md](./_templates/topic-template.md) |
| Pattern | Use topic template |
| Troubleshooting | Use how-to template |

## Adding a Question (AEO-Optimized)

Questions are optimized for Answer Engine Optimization (AEO) - making content easily extractable by AI systems like ChatGPT, Perplexity, and Google AI Overviews.

### Why Questions?

- **One question per page** - Each file answers one specific question
- **Lead with the answer** - Short answer appears in the first 100 words
- **Easy AI extraction** - Consistent, predictable format
- **Clear URL structure** - `/questions/how-do-i-handle-rate-limits/`

### How to Add a Question

1. Copy `_templates/question-template.md` to the appropriate subdirectory (e.g., `agentic-building-blocks/prompts/questions/` or `platforms/claude/questions/`)
2. Name the file as a URL-friendly version of the question: `how-do-i-handle-rate-limits.md`
3. Fill in all sections:
   - **YAML frontmatter** - Machine-readable metadata (includes `short_answer` for JSON-LD schema)
   - **Question as H1** - The exact question being answered
   - **Short answer** - 1-2 sentence direct answer (keep identical to frontmatter `short_answer`)
   - **Full answer** - 2-4 paragraphs of detailed explanation
   - **Code example** - Working, practical implementation
   - **Key takeaways** - 3-5 bullet points
   - **Related questions** - Links to related Q&A
4. Add a link to the appropriate category's README.md index

### Question Naming Convention

- Use lowercase with hyphens: `how-do-i-write-system-prompts.md`
- Frame as a question: `what-is-`, `how-do-i-`, `why-does-`, `when-should-i-`
- Be specific: `how-do-i-handle-openai-rate-limits.md` not `rate-limits.md`

### Question Template Structure

```markdown
---
question: "How do I handle rate limits?"
short_answer: "Implement exponential backoff with jitter, and use the retry-after header."
platforms: [openai]
topic: integrations
date: 2026-01-24
author: Your Name
---

# How do I handle rate limits?

**Short answer:** [1-2 sentence direct answer]

## The Full Answer
[2-4 paragraphs]

## Code Example
[Working code]

## Key Takeaways
- Bullet points

## Related Questions
- Links to related Q&A
```

## Adding a How-To Guide

1. Copy `_templates/how-to-template.md` to the appropriate subdirectory under the relevant section
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

## Adding Setup Guides

Setup guides go in `getting-started/` and should:

1. Focus on one tool per guide
2. Include prerequisites
3. Provide platform-specific instructions (macOS/Windows)
4. Link to official documentation
5. Include troubleshooting tips

## Questions?

If you're unsure where something belongs or how to structure it, check existing entries for examples.

## About This Site

Hands-On AI is maintained by [James Gray](https://maven.com/james-gray). It consolidates setup guides, course materials, and AI reference content from multiple repositories into one resource.
