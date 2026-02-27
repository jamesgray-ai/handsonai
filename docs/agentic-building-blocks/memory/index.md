---
title: Memory
description: The Memory building block — accumulated knowledge from past interactions that makes AI persistent, personalized, and improving over time
---

# Memory

> **Platforms:** `claude` `openai` `gemini` `m365-copilot`

## What Memory Is

**Memory** is accumulated knowledge from past interactions — preferences, decisions, facts, and patterns that the AI retains and retrieves when relevant. Memory makes AI persistent rather than stateless: instead of starting from scratch every conversation, the AI improves over time.

The key distinction from [Context](../context/index.md): **Context is knowledge you provide; Memory is knowledge the system accumulates.** You curate context by uploading files, pasting examples, or configuring project knowledge. Memory is managed by the AI itself — it decides what to remember based on your interactions.

## Key Characteristics

- **System-managed, not user-curated** — the AI decides what to remember from your interactions
- **Persists across conversations** — survives session boundaries, available in future interactions
- **Grows over time** — more interactions produce richer memory, improving personalization and relevance
- **Two main types** — short-term (within a session) and long-term (across sessions)

## When to Use Memory

Use memory when:

- Repeating context to the AI is friction — preferences, project conventions, communication style
- Personalization improves the experience — the AI should adapt to how you work
- The AI needs to learn from past interactions — building on previous decisions and patterns
- Continuity matters — picking up where you left off without re-explaining

When memory isn't available or appropriate, use [Context](../context/index.md) to provide knowledge explicitly for a single conversation or project.

## Platform Implementations

| Platform | How It Works |
|----------|-------------|
| **Claude** | Claude memory, CLAUDE.md project memory, conversation continuity |
| **OpenAI (ChatGPT)** | ChatGPT Memory, custom instructions persistence |
| **Gemini** | Conversation memory, Gems with learned preferences |
| **M365 Copilot** | Microsoft Graph as implicit memory, organizational knowledge |

## Types of Memory

### Short-term memory (working context)

The current conversation history and documents loaded into the context window. This is what the AI can "see" right now — it's limited by the model's context window size and disappears when the conversation ends.

### Long-term memory (persistent storage)

Information stored outside the context window that persists across conversations. Long-term memory includes:

- **Episodic memory** — Records of specific past interactions ("Last week, you asked me to format reports with bullet points instead of paragraphs")
- **Semantic memory** — General knowledge extracted from interactions ("This user prefers concise responses and works in financial services")
- **Procedural memory** — Learned workflows and procedures ("When writing code for this project, always use TypeScript and follow the existing test patterns")

!!! tip "Implementation deep-dive"
    For details on how agents implement memory systems — retrieval mechanisms, storage architectures, and design patterns — see the [Memory capability pattern](../agents/capability-patterns/memory.md).

## Memory vs. Context

| Dimension | Context | Memory |
|-----------|---------|--------|
| **Who curates** | User provides | System accumulates |
| **Lifecycle** | Attached per conversation or project | Persists and grows over time |
| **Management** | User uploads, pastes, or configures | AI decides what to store and retrieve |
| **Example** | Upload a style guide | AI remembers you prefer bullet points |
| **Scope** | Explicit — you choose what to include | Emergent — grows from interactions |

## Relationship to Other Blocks

- **[Context](../context/index.md)** provides knowledge explicitly; Memory accumulates it implicitly
- **[Projects](../projects/index.md)** organize context persistently; Memory adds learned persistence on top — the AI remembers not just what's in the project, but what it has learned from working with you in it
- **[Agents](../agents/index.md)** use Memory to improve across runs — an agent that remembers past decisions makes better decisions next time
- **[Skills](../skills/index.md)** benefit from Memory — remembered preferences shape skill outputs without you specifying them each time

## Related

- [Memory capability pattern](../agents/capability-patterns/memory.md) — implementation deep-dive: how agents store and retrieve memory (episodic, semantic, procedural)
- [Context](../context/index.md) — the closest sibling building block (user-provided knowledge)
- [Projects](../projects/index.md) — persistent workspaces that organize context and benefit from memory
- [Agent capability patterns](../agents/capability-patterns/index.md) — patterns agents use, including memory
