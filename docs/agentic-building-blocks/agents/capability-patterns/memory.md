---
title: Memory
description: How AI agents store and retrieve information across interactions, enabling them to learn from experience and maintain context over time.
---

# Memory

## What It Is

Memory is a pattern where an agent stores information from past interactions and retrieves it when relevant to current tasks. Without memory, every conversation starts from scratch — the agent has no knowledge of previous interactions, decisions, or user preferences. With memory, the agent builds up context over time, becoming more useful and personalized with each interaction.

Memory in AI agents is inspired by human memory systems, but implemented through a combination of databases, embeddings, and retrieval mechanisms rather than biological processes.

## Why It Matters

A stateless agent is like a colleague with amnesia — you have to re-explain everything every time. Memory transforms agents from one-shot tools into persistent collaborators that accumulate knowledge, learn preferences, and build on past work.

The landmark Generative Agents paper (Park et al. 2023) demonstrated that agents with memory could form relationships, remember past conversations, and coordinate activities over time — emergent behaviors that weren't explicitly programmed but arose naturally from the memory architecture.

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

Claude Code's `CLAUDE.md` files and memory directory are a practical implementation of this pattern — project context and user preferences persist across sessions.

## When to Use It

- Customer-facing systems where personalization improves the experience
- Long-running projects where context accumulates over time
- Agents that need to learn from mistakes (paired with [Reflection](reflection.md))
- Any workflow where repeating context to the agent is a friction point

## Related Patterns

- [Reflection](reflection.md) — Reflection generates insights that can be stored in memory for future use
- [Planning](planning.md) — Memory of past plans helps the agent make better plans in the future
- [Multi-Agent Collaboration](multi-agent-collaboration.md) — Shared memory allows agents to coordinate without direct communication
- [Agent Capability Patterns](index.md)

## Further Reading

- Park et al. 2023 — *Generative Agents: Interactive Simulacra of Human Behavior* — [arxiv.org/abs/2304.03442](https://arxiv.org/abs/2304.03442)
- Zhang et al. 2024 — *A Survey on the Memory Mechanism of Large Language Model Based Agents* — [arxiv.org/abs/2404.13501](https://arxiv.org/abs/2404.13501)
- Andrew Ng — *Agentic Design Patterns Part 6: Memory* — [deeplearning.ai/the-batch](https://www.deeplearning.ai/the-batch/)
- LangChain — *Memory in LLM Applications* — [python.langchain.com/docs/concepts/memory](https://python.langchain.com/docs/concepts/memory/)
