---
title: Router
description: How a classifier agent inspects input and dispatches it to the right specialist agent — enabling efficient handling of varied request types.
---

# Router

## What It Is

The router pattern uses a lightweight classifier agent to inspect incoming input and dispatch it to the most appropriate specialist agent. Instead of one agent handling everything, the router ensures each request reaches the agent best equipped to handle it.

Think of it like a hospital triage desk. A triage nurse doesn't treat patients — they quickly assess each case and direct it to the right department: emergency, orthopedics, or dermatology. The specialists handle the actual treatment.

## Why It Matters

Real-world systems handle diverse inputs that require different handling. A customer support system receives billing questions, technical issues, and return requests — each requiring different tools, policies, and tone. A single agent loaded with instructions for all three categories performs worse than three focused specialists.

Routing separates the *classification* decision from the *execution* — keeping each specialist agent's prompt clean and focused. It also makes the system easy to extend: adding a new category means adding a new specialist, not rewriting the main agent.

## How It Works

```text
              ┌─────────────┐
              │   Router     │
              │ (classify)   │
              └──┬───┬───┬──┘
                 │   │   │
        ┌────────┘   │   └────────┐
        ▼            ▼            ▼
  ┌──────────┐ ┌──────────┐ ┌──────────┐
  │ Billing  │ │ Technical│ │ Returns  │
  │ Agent    │ │ Agent    │ │ Agent    │
  └──────────┘ └──────────┘ └──────────┘
```

1. **Classify** — The router agent examines the input and determines which category it belongs to. This can use an LLM call, keyword matching, or an embedding-based classifier.
2. **Dispatch** — The router sends the input (plus any extracted metadata) to the selected specialist agent.
3. **Execute** — The specialist handles the request with its focused prompt, tools, and context.
4. **Return** — The specialist's output is returned to the caller (or to the router for post-processing).

The router itself should be fast and cheap — it's making a classification decision, not doing substantive work. A smaller, faster model often works well for the routing step.

## Example

### Customer support routing

A support system receives tickets of varying types:

- **Router Agent** — Reads the ticket, classifies it as `billing`, `technical`, `returns`, or `general`, and extracts the customer ID and order number.
- **Billing Agent** — Has access to the payment system. Handles refunds, charges, and invoicing questions.
- **Technical Agent** — Has access to the knowledge base and diagnostic tools. Handles product troubleshooting.
- **Returns Agent** — Has access to the order and logistics systems. Handles exchanges, returns, and shipping issues.

The router routes 85% of tickets to the right agent on the first try. The remaining 15% include an escalation path where the specialist can re-route to a different agent.

### Document processing

An enterprise receives documents in multiple formats:

- **Router** — Identifies the document type: invoice, contract, resume, or support ticket.
- **Invoice Agent** — Extracts line items, totals, and vendor details; validates against PO numbers.
- **Contract Agent** — Identifies key clauses, obligations, and renewal dates.
- **Resume Agent** — Extracts skills, experience, and education; scores against job requirements.

Each agent has a tailored extraction prompt and a different set of output schemas.

## When to Use It

- Inputs naturally fall into distinct categories requiring different handling
- Each category benefits from a specialist with focused instructions and tools
- You want to extend the system by adding new specialists without changing existing ones
- Classification accuracy is high enough to avoid frequent misrouting
- The routing decision is simpler than the downstream task

## When NOT to Use It

- All inputs need the same handling — routing adds unnecessary complexity
- Categories overlap significantly, making accurate classification difficult
- The task requires agents to collaborate on a single input — use [Hierarchical](hierarchical.md) or [Group Chat](group-chat.md) instead
- The routing logic is so complex it needs its own multi-step reasoning — use [Hierarchical](hierarchical.md) instead

## Related Patterns

- [Sequential](sequential.md) — the router can feed into a sequential pipeline per category
- [Hierarchical](hierarchical.md) — when the coordinator does more than just classify (it also decomposes and synthesizes)
- [Handoff](handoff.md) — when the routing decision happens mid-conversation rather than at the start
- [Routing](../../../patterns/workflow-architecture/routing.md) — the workflow architecture equivalent
- [Orchestration Patterns Overview](index.md)

## Further Reading

- Anthropic — [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) — "routing" section
- OpenAI Agents SDK — [Multi-Agent Patterns](https://openai.github.io/openai-agents-python/multi_agent/) — agent-as-tool routing
- Google Cloud — [Choose a Design Pattern for Agentic AI](https://cloud.google.com/architecture/choose-design-pattern-agentic-ai-system) — routing pattern
