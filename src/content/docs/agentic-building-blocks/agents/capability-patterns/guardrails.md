---
title: Guardrails
description: How automated rules and constraints keep AI agents safe, on-topic, and within policy — without requiring human intervention at every step.
last_reviewed: 2026-10-24
---

## What It Is

Guardrails are automated rules and constraints that govern what an agent can and cannot do. They operate continuously during agent execution, checking inputs, outputs, and actions against defined policies — and blocking or modifying anything that violates those policies.

Unlike [human-in-the-loop](../human-in-the-loop/) controls, guardrails are automated. They don't require a human to review every action — they enforce rules programmatically, allowing the agent to operate autonomously within defined boundaries.

## Why It Matters

As agents gain more autonomy — making decisions, calling tools, taking actions — the potential for harm increases. An agent without guardrails can hallucinate confidently, leak sensitive data, make unauthorized purchases, or provide advice it shouldn't.

Guardrails are the difference between a useful autonomous system and a liability. They let you grant agents more autonomy (which makes them more useful) while maintaining safety (which makes them trustworthy). Production agent systems always need guardrails — the question is not *whether* to add them, but *which ones* and *where*.

## How It Works

Guardrails can be applied at multiple points in the agent pipeline:

```text
┌────────┐   ┌──────────┐   ┌────────┐   ┌──────────┐   ┌────────┐
│ Input  │──▸│  Input    │──▸│ Agent  │──▸│  Output   │──▸│ Output │
│        │   │  Guards   │   │ (LLM)  │   │  Guards   │   │        │
└────────┘   └──────────┘   └────────┘   └──────────┘   └────────┘
```

### Types of guardrails

**Input guardrails** — Filter or reject problematic inputs before they reach the agent:

- Block prompt injection attempts
- Reject off-topic requests ("I can help with order management, but I can't help with medical advice")
- Sanitize sensitive data (redact credit card numbers before processing)

**Output guardrails** — Check agent responses before they reach the user:

- Block responses containing personally identifiable information (PII)
- Ensure responses stay within the agent's approved topic area
- Verify factual claims against a knowledge base
- Enforce tone and brand voice guidelines

**Action guardrails** — Restrict what tools the agent can call and with what parameters:

- Limit refund amounts ("agent can issue refunds up to $100; anything higher requires approval")
- Restrict database access to read-only queries
- Block destructive operations (delete, overwrite)
- Enforce rate limits on API calls

**Constitutional guardrails** — Baked into the model's behavior through system prompts or fine-tuning:

- Anthropic's Constitutional AI trains a model to follow a written set of principles; in Anthropic's words, "the only human oversight is provided through a list of rules or principles"
- System prompts that define the agent's role and boundaries
- Instructions like "Never provide medical, legal, or financial advice"

## Example

### Customer exchange scenario

An exchange-processing agent has these guardrails:

| Guardrail | Type | Rule |
|-----------|------|------|
| Refund cap | Action | Cannot issue refunds over $200 without escalation |
| Final sale block | Action | Cannot process returns on items marked "final sale" |
| PII filter | Output | Redacts credit card numbers and SSNs from responses |
| Scope limit | Input | Rejects requests unrelated to order management |
| Policy compliance | Output | Verifies that the response cites the correct return policy |

A customer asks: "Can I return this final-sale item?" The action guardrail blocks the return process, and the agent responds: "I'm sorry, final-sale items are not eligible for return or exchange per our policy. I can help you find an alternative product if you'd like."

### Code generation agent

A coding agent has guardrails to prevent generating insecure code:

- **Block** — SQL queries built with string concatenation (SQL injection risk)
- **Warn** — API keys or secrets hardcoded in source code
- **Enforce** — All file writes must go through a sandbox directory

## When to Use It

- Any production agent system — guardrails are not optional for deployed agents
- Agents with access to tools that can take real-world actions (payments, emails, database writes)
- Customer-facing agents where brand safety matters
- Regulated industries (healthcare, finance, legal) with compliance requirements
- Multi-agent systems where individual agents need scoped permissions

## Related Patterns

- [Human Checkpoint](../human-in-the-loop/) — Guardrails handle routine constraints automatically; HITL handles exceptions and edge cases
- [Tool Use](../tool-use/) — Action guardrails govern which tools the agent can access
- [Reflection](../reflection/) — Self-reflection is a soft guardrail; automated guardrails are hard constraints
- [Agent Capability Patterns](../)

## Further Reading

- Anthropic — [Constitutional AI: Harmlessness from AI Feedback](https://www.anthropic.com/research/constitutional-ai-harmlessness-from-ai-feedback) (December 15, 2022)
- Anthropic — [Building effective agents](https://www.anthropic.com/research/building-effective-agents) (December 19, 2024) — guardrails "where one model instance processes user queries while another screens them for inappropriate content or requests"
- OpenAI — [A practical guide to building agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf) (PDF, April 2025) — layered guardrails
- OWASP Gen AI Security Project — [2025 Top 10 Risk & Mitigations for LLMs and Gen AI Apps](https://genai.owasp.org/llm-top-10/) (accessed 2026-10-24) — including prompt injection and excessive agency
- Guardrails AI — [guardrailsai.com](https://guardrailsai.com/) (accessed 2026-10-24) — a framework for adding guardrails to LLM applications
