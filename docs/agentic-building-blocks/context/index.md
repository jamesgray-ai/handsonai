---
title: Context
description: The Context building block — background information, reference docs, and examples that ground AI in your specific domain
---

# Context

> **Platforms:** `claude` `openai` `gemini` `m365-copilot`

## What Context Is

**Context** is the unique knowledge — not in the model's training data — that an agentic workflow needs to execute well. This includes documents, databases, markdown files, examples, style guides, and any other information from your specific domain.

Every AI model has broad general knowledge, but it doesn't know your company's style guide, your product specs, your customer data, or your industry's specific terminology. Context bridges that gap.

## Key Characteristics

- **Provides knowledge the model doesn't have** — your data, your docs, your domain
- **Can be inline (pasted), attached as files, or pre-loaded in a project** — flexibility in how you deliver it
- **Improves output quality** by grounding the model in your specific domain rather than relying on generic knowledge
- **Can be ephemeral or persistent** — inline context disappears after the conversation; project-level context persists

## When to Use Context

Use context when:

- The model needs information it wasn't trained on — your company's data, your domain's standards
- You want outputs grounded in specific examples or reference materials
- The task requires accuracy about your particular situation (not just general knowledge)
- You're working with proprietary or specialized information

Context alone (without a project) is sufficient when:

- The task is a one-off — you won't need this context again
- You have 1-2 files to share — small enough to attach or paste inline
- The context changes every time — different documents, different data

When you find yourself re-uploading the same context repeatedly, that's a signal to use a [Project](../projects/index.md) to organize it persistently.

## Platform Implementations

| Platform | How It Works |
|----------|-------------|
| **Claude** | File attachments, project knowledge base, conversation history |
| **OpenAI (ChatGPT)** | File uploads, Custom GPT knowledge files, conversation history |
| **Gemini** | File uploads, Google Drive integration, NotebookLM sources |
| **M365 Copilot** | Microsoft Graph (emails, files, meetings), attached documents |

## Types of Context

| Type | Description | Example |
|------|-------------|---------|
| **Reference material** | Documents the AI reads but doesn't execute | Style guide, product spec, buyer persona |
| **Examples** | Samples of desired output quality or format | Past reports, approved emails, template documents |
| **Data** | Structured information the AI processes | CSV exports, database queries, spreadsheet data |
| **Domain knowledge** | Specialized information about your field | Industry terminology, regulatory requirements, technical standards |

## Common Context Anti-Patterns

**Too much context** — Uploading everything "just in case" dilutes signal. Include only what the task actually needs. A focused set of relevant documents outperforms a large dump of loosely related ones.

**No context when needed** — Asking the model to write in your brand voice without providing your style guide. The model will guess, and it will guess wrong.

**Stale context** — Using last quarter's data for this quarter's report. Context should be current and relevant to the specific task.

**Context without instructions** — Attaching a document and saying "use this" without explaining how. Tell the model what role the context plays: "Use this style guide to match our brand voice" is better than "Here's our style guide."

## Relationship to Other Blocks

Context makes prompts smarter. Projects organize context persistently so you don't re-upload it every time. Skills can package context alongside instructions for reuse. Agents draw on context as they execute multi-step workflows.

## Related

- [Agentic Building Blocks](../index.md) — Context in the context of all six building blocks
- [Prompts](../prompts/index.md) — the instructions that context enhances
- [Projects](../projects/index.md) — where context becomes persistent and organized
