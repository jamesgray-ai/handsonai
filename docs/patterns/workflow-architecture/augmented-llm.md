---
title: Augmented LLM
description: The foundational AI workflow pattern — an LLM enhanced with retrieval, tools, and memory to overcome its inherent limitations
---

# Augmented LLM

An **Augmented LLM** combines the reasoning and generative abilities of an LLM with external tools, data, or systems to overcome its inherent limitations. It is the foundational building block for all other workflow architecture patterns.

Think of it as an intelligent assistant that can access databases, search the web, run calculations, or interact with APIs — providing answers that go beyond what the model knows from training alone.

## Why It Matters

- **Enhanced capabilities** — Augmentation lets the model fetch real-time information, query databases, or use tools for accurate, up-to-date, and customized responses
- **Task specialization** — Augmented LLMs excel at domain-specific tasks (financial analysis, customer service, medical diagnostics) because they pull in relevant data
- **Adaptability** — They integrate into existing workflows and leverage specialized tools, making them flexible across business applications

## Key Components

| Component | Purpose | Example |
|-----------|---------|---------|
| **LLM Core** | Understands input, generates responses, decides which tasks require augmentation | User asks "What were our sales figures last month?" — the model recognizes it needs to retrieve this data |
| **External Data Source** | Provides relevant, up-to-date, or domain-specific information (APIs, databases, cloud storage) | Sales data in a company database queried for the latest figures |
| **Tools (Plugins)** | Specialized tools for calculations, data processing, or third-party interactions | A spreadsheet plugin calculates revenue growth from retrieved data |
| **Orchestrator** | Oversees the process, ensuring seamless interaction between the LLM and external components | Routes the query to the database and sends results back to the LLM |
| **User Input/Output** | The user's request in, and the enriched response out | Input: "What were last month's sales?" → Output: "Sales were $500,000, a 10% increase from the previous month." |

## When to Use It

- **Real-time information needs** — generating reports from live data, stock prices, or current metrics
- **Complex tasks requiring multiple tools** — financial analysis that involves querying a database, running calculations, and formatting results
- **Domain-specific expertise** — a healthcare LLM augmented with medical databases and imaging tools

## Example: Customer Support Chatbot

A company uses an AI-powered chatbot augmented with external systems:

1. The LLM understands the customer's issue
2. It queries the company's knowledge base or CRM for specific information (e.g., order status)
3. If needed, it uses tools like a refund calculator to generate a solution
4. The response — enriched with real-time data — is delivered to the customer

This pattern enables accurate, context-aware responses without requiring the model to have all information in its training data.

## How to Implement

1. **Define the goal** — What task does the augmented LLM need to perform? Real-time data retrieval, calculations, or insight generation?
2. **Integrate external data and tools** — Connect the LLM to relevant APIs, databases, or plugins. Ensure the orchestrator routes tasks properly.
3. **Test iteratively** — Validate with different inputs to ensure seamless, accurate responses

*Based on [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) by Anthropic.*

## Related

- [Workflow Architecture Patterns Overview](index.md)
- [Prompt Chaining](prompt-chaining.md) — the next step up in complexity
- [MCP (Model Context Protocol)](../../agentic-building-blocks/mcp/index.md) — the connector layer for giving models access to external tools
- [Build > Design Your AI Workflow](../../business-first-ai-framework/build/design.md)
