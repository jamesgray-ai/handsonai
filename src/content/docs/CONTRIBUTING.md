---
title: Contributing to Hands-on AI
description: How to add content — questions, how-to guides, topics, and patterns — to the AI Playbook
---Thank you for contributing to Hands-On AI! This guide explains how to add new content.

## Site Structure

| Section | Location | Purpose |
|---------|----------|---------|
| Agentic Building Blocks | `agentic-building-blocks/` | The AI building blocks (Model, Prompts, Context, Projects, Memory, Skills, Agents, MCP, API, SDK, CLI) |
| AI Workflow Framework | `ai-workflow-framework/` | Seven-step methodology (Analyze, Deconstruct, Design, Build, Test, Run, Improve) |
| Use Cases | `use-cases/` | Six use case primitives (Content Creation, Research, Coding, Data Analysis, Ideation & Strategy, Automation) |
| Platforms | `platforms/` | Platform-specific content (Claude, OpenAI, Gemini, M365 Copilot) |
| Builder Setup | `builder-setup/` | Tool setup and installation guides |
| Patterns | `patterns/` | Document reusable approaches |
| Courses | `courses/` | Structured learning paths (course-specific) |

## Content Types and Templates

| Type | Template |
|------|----------|
| Question (AEO) | [question-template.md](https://github.com/jamesgray-ai/handsonai/blob/main/src/_templates/question-template.md) |
| How-To Guide | [how-to-template.md](https://github.com/jamesgray-ai/handsonai/blob/main/src/_templates/how-to-template.md) |
| Topic | [topic-template.md](https://github.com/jamesgray-ai/handsonai/blob/main/src/_templates/topic-template.md) |
| Use Case | [use-case.mdx](https://github.com/jamesgray-ai/handsonai/blob/main/src/_templates/use-case.mdx) |
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

## Adding a Worked Use Case

Worked use cases live as flat files at `src/content/docs/use-cases/<slug>.mdx` and are surfaced automatically on the [Use Cases hub](/use-cases/) and the per-primitive landing pages via the `<UseCaseList />` component.

### How to add a use case

1. Copy `_templates/use-case.mdx` to `src/content/docs/use-cases/<slug>.mdx`
2. Name the file as a short, job-oriented slug: `draft-brand-voice-social-posts.mdx`, not `social-posts.mdx`
3. Fill in the frontmatter — every field documented in the template:
   - **Required**: `title`, `description`, `jtbd`, `primitives`, `building_blocks`, `question`, `short_answer`, `status`, `published`, `last_updated`
   - **Optional**: `department` (renders as a chip), `maven_video_url`, `maven_course`
4. Set `primitives` to one or two of: `content-creation`, `research`, `coding`, `data-analysis`, `ideation-and-strategy`, `automation`. These power the chips and the per-primitive auto-lists.
5. Write the body following the template sections: *The job*, *Who it's for*, *What you'll get*, *What you'll need*, *The walkthrough*, *The building blocks*, *Variations & extensions*, *Troubleshooting*, *Related*.
6. Aim for ~1,500 words. A reader should be able to skim in 5 minutes and execute in 15.
7. No sidebar update needed — `<UseCaseList />` auto-discovers `status: published` use cases. Drafts (`status: draft`) are excluded.

### Use case naming convention

- Lowercase with hyphens: `draft-brand-voice-social-posts.mdx`
- Lead with a verb that matches the JTBD: `draft-`, `summarize-`, `monitor-`, `extract-`
- Be specific: `summarize-zoom-meeting-with-action-items.mdx` not `meeting-summary.mdx`

### AEO frontmatter on use cases

Use cases include `question` and `short_answer` frontmatter for Answer Engine Optimization — same convention as the [Questions](/questions/) pages. The `question` should be phrased the way someone would actually search, and `short_answer` should be 1–2 sentences that lead with the verb.

**Repeat the short answer visibly on the page.** Right after the frontmatter and any imports, write `**Short answer:** ...` and paste the `short_answer` text verbatim. This is what Google's AI Overviews and similar engines extract from the page body — the JSON-LD `FAQPage` schema agrees with the visible text, which is what gets cited. The template includes this line in the right position.

Use cases are also indexed in `llms.txt` and `llms-full.txt` (built automatically at deploy time) so LLM crawlers can ingest them alongside the Q&A library.

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

- [How to Stream Responses](./stream-responses/) - `openai` `claude`
- [How to Handle Rate Limits](./handle-rate-limits/) - `all`
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
