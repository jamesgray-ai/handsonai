---
title: Context Graphs
description: Structured systems that capture reasoning, decisions, and relational context for agentic AI workflows
---

# Context Graphs

> **Platforms:** `claude` `openai` `gemini` `m365-copilot`

## What Context Graphs Are

A **context graph** is a structured system that captures not just *what* information an AI agent uses, but *why* decisions were made and how facts relate to each other.

Think of it this way: a document gives an AI agent information. A context graph gives it *understanding* — the connections between entities, the reasoning behind decisions, and the temporal sequence of events that led to the current state.

Context graphs build on the concept of a **knowledge graph** (a network of entities connected by labeled relationships) but go further by encoding decision logic, confidence levels, and causal chains. In a knowledge graph, you might store that "Customer A bought Product B." In a context graph, you also capture *why* — the sales signal that triggered outreach, the objection that was overcome, and the precedent from a similar deal that informed the approach.

## How Context Graphs Differ

| Approach | What It Does | What It Misses |
|----------|-------------|----------------|
| **Context window** | Holds the text (measured in **tokens** — chunks of text the model processes) visible to the model in a single conversation | No structure, no persistence, limited size |
| **RAG** | **Retrieval-Augmented Generation** — retrieves relevant documents from a database and injects them into the prompt | Finds *related* content but doesn't capture *relationships* between concepts |
| **Knowledge graph** | Maps entities and their relationships in a structured network of **nodes** (things) and **edges** (connections) | Static structure, no decision reasoning or temporal context |
| **Context graph** | Captures entities, relationships, decisions, reasoning chains, and temporal context in a queryable structure | Emerging technology, more complex to build and maintain |

Each approach in this table builds on the ones above it. **RAG** helps an AI find relevant documents. A **knowledge graph** helps it understand how entities relate. A **context graph** helps it understand *why things happened* and *what led to decisions* — which is what agents need for multi-step reasoning.

## Key Concepts

### Nodes

Nodes are the things in a context graph. Unlike a traditional knowledge graph where nodes are mostly entities (people, companies, products), context graph nodes include:

| Node Type | What It Represents | Example |
|-----------|--------------------|---------|
| **Entity** | A person, organization, product, or concept | "Acme Corp", "Q4 Revenue Report" |
| **Decision** | A choice that was made, with reasoning | "Chose vendor B because of compliance requirements" |
| **Signal** | An event or data point that triggered action | "Customer satisfaction dropped below 80%" |
| **State** | A snapshot of conditions at a point in time | "Pipeline status as of January 2026" |

### Edges

**Edges** are the connections between nodes — they describe *how* things relate. Context graphs use richer edge types than traditional knowledge graphs:

| Edge Type | What It Captures | Example |
|-----------|-----------------|---------|
| **Causation** | One thing led to another | Signal "churn risk detected" → Decision "escalate to account manager" |
| **Dependency** | One thing requires another | Task "generate report" depends on State "data refresh complete" |
| **Precedent** | A past decision that informs a current one | Decision "pricing for Enterprise tier" references Decision "pricing for Mid-Market tier" |
| **Temporal** | Sequence and timing of events | Signal A occurred before Signal B, 3 days apart |
| **Confidence** | How certain a relationship is | Entity "likely competitor" connected with 0.7 confidence |

### Relationships

The combination of nodes and edges creates relationship patterns that agents can traverse:

- **Temporal chains** — "What sequence of events led to this outcome?"
- **Conditional logic** — "Under what conditions was this decision made?"
- **Confidence-weighted paths** — "What's the most reliable chain of reasoning?"

## Why They Matter for Agentic AI

Context graphs address specific limitations that surface when AI agents handle multi-step, real-world workflows:

- **Multi-step reasoning** — Agents can trace chains of causation and dependency rather than relying on whatever fits in the context window
- **Structured memory** — Decisions and their rationale persist across conversations and sessions, giving agents institutional knowledge
- **Auditability** — Every recommendation can be traced back through the graph to the signals and precedents that informed it
- **Compounding organizational knowledge** — Each interaction adds to the graph, making the system more capable over time rather than starting fresh each session

## The Context Engineering Shift

The AI industry is undergoing a shift from **prompt engineering** (optimizing *how you ask*) to **context engineering** (optimizing *what information the model sees*).

The core insight: a well-structured, relevant context makes even a simple prompt produce excellent results. A perfectly crafted prompt with poor context still produces poor results.

This shift has practical implications:

- **Where you invest time changes** — less on prompt syntax, more on building and curating the information your AI workflows consume
- **What you build changes** — systems that assemble, filter, and structure context become more valuable than prompt template libraries
- **How you measure quality changes** — success depends on whether the right context reached the model, not just whether the prompt was well-written

Context graphs represent the most structured end of this spectrum — purpose-built systems for assembling exactly the right context for each agent action.

## Tools and Frameworks

| Tool | What It Does | Best For |
|------|-------------|----------|
| [TrustGraph](https://trustgraph.ai) | Extracts knowledge graphs from documents with AI, supports context graph queries | Document-heavy workflows needing structured extraction |
| [Graphiti](https://github.com/getzep/graphiti) | Temporal knowledge graph library for building agent memory | Agents that need persistent, evolving memory across sessions |
| [LangGraph](https://www.langchain.com/langgraph) | Framework for building stateful, multi-agent workflows with graph-based orchestration | Complex agent orchestration with branching logic |
| [Neo4j](https://neo4j.com) | Graph database for storing and querying relationship-rich data | Enterprise-scale knowledge and context graph storage |
| [MCP](../mcp/index.md) | **Model Context Protocol** — a standard for connecting AI models to external data sources and tools | Connecting agents to live context from APIs, databases, and services |

## Relationship to Other Blocks

Context graphs intersect with every other building block:

- **[Prompts](../prompts/index.md)** — Context graphs provide the structured background that makes prompts effective. Instead of cramming context into a prompt, agents query the graph for exactly what's relevant.
- **[Projects](../projects/index.md)** — Projects organize persistent context. Context graphs add structure *within* that context — not just "here are the files" but "here's how they relate."
- **[Skills](../skills/index.md)** — Skills can use context graphs to make decisions based on precedent and historical patterns rather than just the instructions they contain.
- **[Agents](../agents/index.md)** — Agents are the primary consumers of context graphs. Multi-step workflows benefit most from structured reasoning and memory.
- **[MCP](../mcp/index.md)** — MCP servers can expose context graph data as tools and resources, giving agents structured access to organizational knowledge.

## Further Reading

- [AI's Trillion-Dollar Opportunity: Context Graphs](https://foundationcapital.com/context-graphs-ais-trillion-dollar-opportunity/) — Foundation Capital
- [Context is the Next Data Platform](https://www.glean.com/blog/context-data-platform) — Glean
- [What are Context Graphs](https://medium.com/modelmind/what-are-context-graphs-building-the-ai-that-trulyunderstands-e7e5db39138d) — Neural Notions
- [Context Engineering for Agents](https://blog.langchain.com/context-engineering-for-agents/) — LangChain
- [Context Graphs: A Practical Guide](https://medium.com/@adnanmasood/context-graphs-a-practical-guide-to-governed-context-for-llms-agents-and-knowledge-systems-c49610c8ff27) — Adnan Masood, PhD
- [Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) — Anthropic
- [Context Graphs: AI-Optimized Knowledge Graphs](https://trustgraph.ai/guides/key-concepts/context-graphs/) — TrustGraph
- [Graphiti](https://github.com/getzep/graphiti) — Temporal knowledge graph library for agent memory

## Related

- [Context Engineering](../../ai-engineering/context-engineering.md) — the broader discipline; context graphs are an advanced technique within it
- [Context](index.md) — the Context building block overview
- [Agentic Building Blocks](../index.md) — Context Graphs in the context of all seven building blocks
- [AI Use Cases](../../use-cases/index.md) — what teams build with context, organized by six primitives
- [Agents](../agents/index.md) — autonomous workflows that benefit most from structured context
- [MCP](../mcp/index.md) — the protocol for connecting agents to external context sources
- [Prompts](../prompts/index.md) — the instructions that context enhances
