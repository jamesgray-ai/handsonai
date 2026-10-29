---
title: Routing
description: "The routing pattern — classify each input and direct it to a specialized follow-up process, so diverse task types get handled by the right prompt or agent."
last_reviewed: 2026-10-24
---

**Level:** Guided if the AI classifies each input; Deterministic if fixed rules route it. See [the patterns and their levels](../#the-patterns-and-their-levels).

**Also called:** router, dispatcher, triage.

The **routing** pattern classifies input and directs it to a specialized follow-up task. By separating tasks into distinct categories and routing them to appropriate processes, this pattern enables **separation of concerns** and highly optimized handling for each input type.

Think of it like a hospital triage desk. A triage nurse doesn't treat patients — they quickly assess each case and direct it to the right department: emergency, orthopedics, or dermatology. The specialists handle the actual treatment.

Without routing, optimizing a system for one type of input (e.g., simple queries) can degrade performance for other types (e.g., complex or edge-case queries). The specialists can be single LLM calls or full agents; the pattern is the same either way.

## Why It Matters

- **Specialization improves performance** — Each task type is handled by a tailored process, ensuring higher accuracy
- **Efficiency** — Tasks go to the most appropriate system, optimizing resource use and reducing computational costs
- **Easy to extend** — Adding a new category means adding a new specialist, not rewriting the existing ones
- **Reduced bottlenecks** — No single model becomes overwhelmed by diverse inputs it isn't optimized for

Routing separates the *classification* decision from the *execution*, which keeps each specialist's prompt clean and focused.

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
  │ handler  │ │ handler  │ │ handler  │
  └──────────┘ └──────────┘ └──────────┘
```

1. **Classify** — The router examines the input and decides which category it belongs to. This can be an LLM call, keyword matching, or an embedding-based classifier.
2. **Dispatch** — The router sends the input (plus any extracted details) to the selected specialist.
3. **Execute** — The specialist handles the request with its focused prompt, tools, and context.
4. **Return** — The specialist's output goes back to the caller (or to the router for post-processing).

How the router classifies sets the level. When an LLM judges the category by your criteria, the AI's judgment decides the next step: Guided. When keywords, a form field, or another fixed rule picks the path, your instructions decide it: Deterministic.

The router should be fast and cheap — it's making a classification decision, not doing substantive work, so a smaller, faster model can make it. Routing can also save cost downstream: Anthropic's example sends easy, common questions to a smaller, cheaper model and hard ones to a more capable one.

## Key Components

| Component | Purpose | Example |
|-----------|---------|---------|
| **Router** | Classifies incoming tasks and directs them to the appropriate follow-up | Determines if a customer query is general, refund-related, or technical |
| **Specialized Process 1** | Handles one specific task category | Responds to general inquiries (store hours, product info) |
| **Specialized Process 2** | Handles a different task category | Processes refund requests (checking order history, issuing refunds) |
| **Specialized Process 3** | Handles complex or specialized tasks | Resolves technical support issues with troubleshooting steps |
| **Output** | Consolidates results into the final response | Delivers the resolved answer to the customer |

## When to Use It

- **Diverse input types** — When the system handles inputs that differ in complexity or nature
- **Distinct handling** — When each category benefits from a specialist with focused instructions and tools
- **High-performance requirements** — When optimizing for one input type risks degrading performance for others
- **Resource optimization** — When simple tasks can use smaller models while reserving powerful models for complex cases
- **A simpler decision** — When the routing decision is simpler than the downstream task, and classification is accurate enough to avoid frequent misrouting

## When Not to Use It

- All inputs need the same handling — routing adds unnecessary complexity
- Categories overlap significantly, making accurate classification difficult
- Several specialists need to work together on a single input — use [Orchestrator-Workers](../orchestrator-workers/) or [Group Chat](../group-chat/) instead
- The routing logic is so complex it needs its own multi-step reasoning — use [Orchestrator-Workers](../orchestrator-workers/) instead
- The right specialist only becomes clear partway through a conversation — use [Handoff](../handoff/) instead

## Examples

### Customer service automation

A company automates customer service across varied query types:

1. **Router** classifies each query:
    - General questions ("What are your store hours?")
    - Refund requests ("I want a refund for my last order.")
    - Technical issues ("My device isn't turning on.")
2. **Process 1** handles general inquiries with predefined responses
3. **Process 2** processes refunds by accessing order history, validating claims, and initiating refunds
4. **Process 3** resolves technical issues with product-specific troubleshooting
5. **Output** delivers the final response to the customer

Plan for misrouted queries: give each specialist an escalation path that sends a query back to the router, or on to a person.

### Document processing

An enterprise receives documents in multiple formats:

- **Router** — Identifies the document type: invoice, contract, resume, or support ticket.
- **Invoice handler** — Extracts line items, totals, and vendor details; validates against PO numbers.
- **Contract handler** — Identifies key clauses, obligations, and renewal dates.
- **Resume handler** — Extracts skills, experience, and education; scores against job requirements.

Each handler has a tailored extraction prompt and a different output schema.

## How to Implement

1. **Define categories** — Identify the distinct task or input types your system will handle
2. **Choose the classifier** — An LLM call, keywords, or embeddings. This choice also sets the level (Guided or Deterministic)
3. **Develop specialized workflows** — Create tailored workflows, prompts, or agents for each category
4. **Test and refine** — Evaluate routing accuracy and each specialized workflow's effectiveness

## Sources

- Anthropic — [Building effective agents](https://www.anthropic.com/research/building-effective-agents) (December 19, 2024) — "Workflow: Routing", which "works well for complex tasks where there are distinct categories that are better handled separately"
- OpenAI Agents SDK — [Agent orchestration](https://openai.github.io/openai-agents-python/multi_agent/) (accessed 2026-10-24) — a triage agent that "routes the conversation to a specialist"
- Google Cloud — [Choose a design pattern for your agentic AI system](https://docs.cloud.google.com/architecture/choose-design-pattern-agentic-ai-system) (last reviewed May 28, 2026) — the coordinator pattern, which uses an AI model to "dynamically route tasks" (Google has no pattern named routing)
- Google Developers Blog — [Developer's guide to multi-agent patterns in ADK](https://developers.googleblog.com/developers-guide-to-multi-agent-patterns-in-adk/) (December 16, 2025) — the coordinator/dispatcher pattern

## Related

- [Workflow Architecture Patterns Overview](../)
- [Prompt Chaining](../prompt-chaining/) — a router can feed a fixed chain of steps for each category
- [Parallelization](../parallelization/) — running multiple paths at once instead of choosing one
- [Orchestrator-Workers](../orchestrator-workers/) — when the lead does more than classify (it also splits the work and combines the results)
- [Handoff](../handoff/) — when the routing decision happens mid-conversation rather than at the start
- [Design Your AI Workflow](../../../ai-workflow-framework/design/)
