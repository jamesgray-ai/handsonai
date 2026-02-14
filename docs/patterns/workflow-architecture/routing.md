---
title: Routing
description: Classify input and direct it to specialized follow-up processes for optimized handling of diverse task types
---

# Routing

The **routing** pattern classifies input and directs it to a specialized follow-up task. By separating tasks into distinct categories and routing them to appropriate processes, this pattern enables **separation of concerns** and highly optimized handling for each input type.

Without routing, optimizing a system for one type of input (e.g., simple queries) can degrade performance for other types (e.g., complex or edge-case queries).

## Why It Matters

- **Specialization improves performance** — Each task type is handled by a tailored process, ensuring higher accuracy
- **Efficiency** — Tasks go to the most appropriate system, optimizing resource use and reducing computational costs
- **Scalability** — Varied input types are handled effectively by directing them to the right models or systems
- **Reduced bottlenecks** — No single model becomes overwhelmed by diverse inputs it isn't optimized for

## Key Components

| Component | Purpose | Example |
|-----------|---------|---------|
| **Router (LLM Call)** | Classifies incoming tasks and directs them to the appropriate follow-up | Determines if a customer query is general, refund-related, or technical |
| **Specialized Process 1** | Handles one specific task category | Responds to general inquiries (store hours, product info) |
| **Specialized Process 2** | Handles a different task category | Processes refund requests (checking order history, issuing refunds) |
| **Specialized Process 3** | Handles complex or specialized tasks | Resolves technical support issues with troubleshooting steps |
| **Output** | Consolidates results into the final response | Delivers the resolved answer to the customer |

## When to Use It

- **Diverse input types** — When the system handles inputs that differ in complexity or nature
- **High-performance requirements** — When optimizing for one input type risks degrading performance for others
- **Resource optimization** — When simple tasks can use smaller models while reserving powerful models for complex cases

## Example: Customer Service Automation

A company automates customer service across varied query types:

1. **Router** classifies each query:
    - General questions ("What are your store hours?")
    - Refund requests ("I want a refund for my last order.")
    - Technical issues ("My device isn't turning on.")
2. **Process 1** handles general inquiries with predefined responses
3. **Process 2** processes refunds by accessing order history, validating claims, and initiating refunds
4. **Process 3** resolves technical issues with product-specific troubleshooting
5. **Output** delivers the final response to the customer

## How to Implement

1. **Define categories** — Identify the distinct task or input types your system will handle
2. **Train or configure the router** — Implement a classification mechanism (LLM or traditional classifier) to route inputs correctly
3. **Develop specialized workflows** — Create tailored workflows or prompts for each category
4. **Test and refine** — Evaluate routing accuracy and each specialized workflow's effectiveness

*Based on [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) by Anthropic.*

## Related

- [Workflow Architecture Patterns Overview](index.md)
- [Prompt Chaining](prompt-chaining.md) — sequential processing within a single path
- [Parallelization](parallelization.md) — running multiple paths simultaneously
- [Build > Design Your AI Workflow](../../business-first-ai-framework/build/design.md)
