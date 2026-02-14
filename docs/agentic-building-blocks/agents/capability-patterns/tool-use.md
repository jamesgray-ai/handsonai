---
title: Tool Use
description: How AI agents extend their capabilities by calling external tools, APIs, and data sources to interact with the real world.
---

# Tool Use

## What It Is

Tool use is a pattern where an agent calls external tools — APIs, databases, calculators, code interpreters, web browsers, file systems — to perform actions that go beyond text generation. Instead of relying solely on its training data, the agent selects the right tool, formats the input, executes the call, and interprets the result.

This is arguably the most fundamental capability pattern. Without tool use, an agent is limited to generating text. With tool use, it can check inventory, send emails, query databases, run code, and interact with any system that exposes an API.

## Why It Matters

LLMs have inherent limitations: they can't access real-time data, perform reliable arithmetic, interact with external systems, or take actions in the world. Tool use bridges these gaps by giving the agent access to specialized capabilities on demand.

The MRKL (Modular Reasoning, Knowledge and Language) architecture (Karpas et al. 2022) formalized this idea: combine a language model with a set of expert modules (calculators, search engines, databases) and let the model route queries to the right module. Every major AI platform — Claude, ChatGPT, Gemini, Copilot — now implements some form of this pattern.

## How It Works

```text
┌──────────┐     ┌──────────────┐     ┌──────────┐
│  Agent    │────▸│ Tool Router   │────▸│  Tool    │
│  (LLM)   │◂────│ (select tool) │◂────│  Result  │
└──────────┘     └──────────────┘     └──────────┘
```

1. **Observe** — The agent receives a task or question that requires external information or action.
2. **Select** — The agent decides which tool to call based on the task requirements and available tool descriptions.
3. **Format** — The agent structures the input according to the tool's expected parameters (function calling).
4. **Execute** — The tool runs and returns a result.
5. **Interpret** — The agent incorporates the tool result into its reasoning and either responds or calls another tool.

Modern implementations use **function calling** (also called tool calling) — the model outputs structured JSON specifying which function to call and with what arguments, rather than generating free-form text that needs parsing.

## Example

### Customer exchange scenario

A customer asks to exchange a product. The agent uses multiple tools in sequence:

1. **Order lookup tool** — `get_order(customer_id="C-1234")` → Returns order details, items, and dates
2. **Policy checker tool** — `check_return_eligibility(order_id="ORD-5678", reason="exchange")` → Returns "eligible, 14-day window"
3. **Inventory tool** — `check_stock(sku="WIDGET-RED", warehouse="US-EAST")` → Returns "in stock, 47 units"
4. **Payment tool** — `process_exchange(original_order="ORD-5678", new_sku="WIDGET-RED")` → Returns confirmation number

Without tool use, the agent could only say "I'd be happy to help with your exchange" — it couldn't actually *do* anything.

### Data analysis

A user asks: "What were our top 5 products by revenue last quarter?"

The agent calls a SQL query tool: `execute_query("SELECT product_name, SUM(revenue) as total FROM sales WHERE quarter='Q4-2025' GROUP BY product_name ORDER BY total DESC LIMIT 5")` — then formats the results into a readable table.

## When to Use It

- Any task requiring real-time or external data (current prices, weather, stock levels)
- Tasks involving calculations or precise data manipulation
- Workflows that require taking actions (sending emails, updating records, creating files)
- Integration with existing business systems (CRM, ERP, order management)
- Code execution and testing

## Related Patterns

- [Planning](planning.md) — Planning determines *which* tools to call and in what order
- [Reflection](reflection.md) — The agent can reflect on tool results to decide if it needs to call additional tools
- [Multi-Agent Collaboration](multi-agent-collaboration.md) — Different agents may have access to different tool sets
- [Guardrails](guardrails.md) — Guardrails can restrict which tools an agent is allowed to call
- [Agent Capability Patterns](index.md)

## Further Reading

- Karpas et al. 2022 — *MRKL Systems: A modular, neuro-symbolic architecture that combines large language models, external knowledge sources and discrete reasoning* — [arxiv.org/abs/2205.00445](https://arxiv.org/abs/2205.00445)
- Yao et al. 2022 — *ReAct: Synergizing Reasoning and Acting in Language Models* — [arxiv.org/abs/2210.03629](https://arxiv.org/abs/2210.03629)
- Anthropic — *Tool Use with Claude* — [docs.anthropic.com/en/docs/build-with-claude/tool-use](https://docs.anthropic.com/en/docs/build-with-claude/tool-use)
- Andrew Ng — *Agentic Design Patterns Part 3: Tool Use* — [deeplearning.ai/the-batch](https://www.deeplearning.ai/the-batch/agentic-design-patterns-part-3-tool-use/)
- OpenAI — *Function Calling Guide* — [platform.openai.com/docs/guides/function-calling](https://platform.openai.com/docs/guides/function-calling)
