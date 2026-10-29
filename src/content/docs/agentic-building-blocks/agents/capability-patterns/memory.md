---
title: Memory
description: How AI agents store and retrieve information across interactions, enabling them to learn from experience and maintain context over time.
last_reviewed: 2026-10-24
---

:::tip[Memory as a building block]
This page covers Memory as an **agent capability pattern** — the specific mechanisms agents use to store and retrieve information. For the broader concept of Memory as a platform-level building block, see [Memory](../../../memory/).
:::
## What It Is

Memory is a pattern where an agent stores information from past interactions and retrieves it when relevant to current tasks. Without memory, every conversation starts from scratch — the agent has no knowledge of previous interactions, decisions, or user preferences. With memory, the agent builds up context over time, becoming more useful and personalized with each interaction.

Memory isn't one of Andrew Ng's four agentic design patterns; the playbook adds it because any agent that works across sessions depends on it. Memory in AI agents borrows its terms from human memory, but it's implemented through a combination of databases, embeddings, and retrieval mechanisms.

## Why It Matters

A stateless agent is like a colleague with amnesia — you have to re-explain everything every time. Memory transforms agents from one-shot tools into persistent collaborators that accumulate knowledge, learn preferences, and build on past work.

The Generative Agents paper (Park et al., 2023) gave 25 simulated characters a memory: a record of everything they experienced, summarized over time into reflections and retrieved when they planned. Told only that one character wanted to throw a Valentine's Day party, the characters spread the invitations over two days, made new acquaintances, asked each other to the party, and turned up together at the right time. The authors' tests showed that observation, planning and reflection each contributed critically to how believable the characters were.

## How It Works

Agent memory systems typically implement multiple types of memory:

### Short-term memory (working context)

The current conversation history and any documents loaded into the context window. This is what the agent can "see" right now. It's limited by the model's context window size.

### Long-term memory (persistent storage)

Information stored outside the context window in a database or file system, retrieved when relevant. This includes:

- **Episodic memory** — Records of specific past interactions ("Last Tuesday, the user asked about exchange policies and preferred email communication").
- **Semantic memory** — General knowledge extracted from interactions ("This user prefers concise responses" or "This customer is a VIP account").
- **Procedural memory** — Learned workflows and procedures ("When processing exchanges for this company, always check the VIP discount table first").

### Retrieval

When the agent starts a new task, it queries long-term memory for relevant context. Common retrieval methods include:

- **Keyword/semantic search** — Finding memories related to the current topic using embeddings
- **Recency weighting** — Prioritizing recent memories over older ones
- **Importance scoring** — Surfacing memories that were flagged as significant

```text
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Current     │────▸│  Retrieval    │────▸│  Enriched    │
│  Task        │     │  (search      │     │  Context     │
│              │     │   memory)     │     │              │
└─────────────┘     └──────┬───────┘     └─────────────┘
                           │
                    ┌──────▼───────┐
                    │  Long-term    │
                    │  Memory Store │
                    └──────────────┘
```

## Example

### Customer exchange scenario

A customer contacts support about an exchange. The agent retrieves from memory:

- **Episodic:** "This customer contacted us 3 weeks ago about a defective Blue Widget. We sent a replacement. They mentioned they prefer phone updates over email."
- **Semantic:** "This customer has been with us for 4 years and has a lifetime value of $2,400. They're in the VIP tier."
- **Procedural:** "VIP customers get free expedited shipping on exchanges and a courtesy discount on the replacement item."

Armed with this context, the agent provides personalized service without the customer having to repeat their history.

### Development workflow

A coding agent with memory:

- Remembers the project's architecture decisions from previous sessions
- Recalls that the user prefers TypeScript over JavaScript and tabs over spaces
- Knows which test framework the project uses without being told each time
- Stores debugging insights ("The authentication module has a known issue with token refresh timing")

Claude Code's `CLAUDE.md` files and auto memory are a practical implementation of this pattern: instructions you write, and notes Claude writes itself, are loaded at the start of every session ([How Claude remembers your project](https://code.claude.com/docs/en/memory), accessed 2026-10-24).

## When to Use It

- Customer-facing systems where personalization improves the experience
- Long-running projects where context accumulates over time
- Agents that need to learn from mistakes (paired with [Reflection](../reflection/))
- Any workflow where repeating context to the agent is a friction point

## Related Patterns

- [Reflection](../reflection/) — Reflection generates insights that can be stored in memory for future use
- [Planning](../planning/) — Memory of past plans helps the agent make better plans in the future
- [Multi-Agent Collaboration](../multi-agent-collaboration/) — Shared memory allows agents to coordinate without direct communication
- [Agent Capability Patterns](../)

## Further Reading

- Park et al. — [Generative Agents: Interactive Simulacra of Human Behavior](https://arxiv.org/abs/2304.03442) (arXiv, April 7, 2023)
- Zhang et al. — [A Survey on the Memory Mechanism of Large Language Model based Agents](https://arxiv.org/abs/2404.13501) (arXiv, April 21, 2024)
- LangChain — [Memory overview](https://docs.langchain.com/oss/python/concepts/memory) (accessed 2026-10-24) — short-term and long-term memory, and semantic, episodic and procedural memory
- Anthropic — [How Claude remembers your project](https://code.claude.com/docs/en/memory) (Claude Code docs, accessed 2026-10-24) — `CLAUDE.md` files and auto memory
