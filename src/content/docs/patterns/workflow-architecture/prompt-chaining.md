---
title: Prompt Chaining
description: "The prompt chaining pattern: break a task into ordered steps, each building on the last, with gates between them that stop errors before they spread."
last_reviewed: 2026-10-24
---

**Level:** Deterministic with coded gates; Guided if the AI judges a gate. See [the patterns and their levels](../#the-patterns-and-their-levels).

**Also called:** sequential pipeline.

**Prompt chaining** breaks a complex task into a sequence of smaller steps. Each step builds on the output of the previous one, with intermediate **gates** that validate quality before proceeding. If an output fails validation, the process can exit early to prevent error propagation. The steps can be single LLM calls or separate agents; the pattern is the same either way.

Think of it as an assembly line where each station contributes a specific part to the final product, inspects the result, and passes the workpiece on. No station starts until it receives input from the one before it.

## Why It Matters

- **Increased accuracy** — Each step focuses on a specific goal, reducing errors and improving overall quality
- **Modularity** — You can inspect and debug intermediate steps, making the workflow easier to adapt and refine; when something goes wrong, you can see exactly where
- **Enhanced reliability** — Gates catch errors early, increasing confidence in the final output
- **Efficiency trade-off** — This workflow trades some latency (multiple steps) for more robust, higher-quality outputs

Prompt chaining is the simplest multi-step pattern to build, test, and debug, which makes it the default starting point once a single [Augmented LLM](../augmented-llm/) call isn't enough.

## How It Works

```text
┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐
│ Step 1   │────▸│ Step 2   │────▸│ Step 3   │────▸│  Output  │
│ Research │     │ Analyze  │     │  Write   │     │          │
└─────────┘     └─────────┘     └─────────┘     └─────────┘
     │               │               │
  Gate 1          Gate 2          Gate 3
 (validate)      (validate)      (validate)
```

1. **Step 1** receives the initial input and produces its output.
2. **Gate 1** validates that output. If it fails, the step retries or the chain halts.
3. **Step 2** receives the validated output and produces its own.
4. The pattern repeats until the final step delivers the result.

**Each step sees only what it needs.** A step receives the previous stage's output, not the entire task history. This keeps prompts clean, reduces token costs, and protects each step's context from material it doesn't need — one of the main reasons to split work into steps at all.

How the gates check sets the level. A gate written as code (a length check, a schema check, a required-sections check) is an instruction: Deterministic. A gate where the AI judges the output by your criteria and that judgment decides whether the chain continues is Guided.

## Key Components

| Component | Purpose | Example |
|-----------|---------|---------|
| **Step 1** | Handles the initial step and produces the first output | Generate a document outline based on user input |
| **Gate** | Validates the output of the previous step; continues or exits | Check if the outline contains all necessary sections |
| **Step 2** | Processes the validated output from the previous step | Expand the approved outline into a detailed draft |
| **Step 3** | Finalizes the task by refining or transforming the output | Translate the draft or format it for publication |
| **Exit** | Ends the workflow early if validation fails | Stop if the outline doesn't meet quality standards |
| **Output** | Delivers the final product after all steps complete successfully | A polished, translated document ready for publication |

## When to Use It

- **Multi-step processes** — Tasks that naturally decompose into ordered stages (research → write → edit)
- **Tasks requiring validation** — When intermediate outputs need quality checks before proceeding
- **Different expertise per step** — When different steps benefit from different prompts, models, tools, or configurations
- **Debuggability matters** — When you need to trace where things went wrong

## When Not to Use It

- Stages are independent and could run simultaneously — use [Parallelization](../parallelization/) instead
- The number or order of stages isn't known until runtime — use [Orchestrator-Workers](../orchestrator-workers/) instead
- The task requires iteration between stages (writer ↔ editor back-and-forth) — use [Evaluator-Optimizer](../evaluator-optimizer/) instead
- One step does the job — adding a chain adds complexity without benefit

## Examples

### Generating marketing materials

A company needs product launch copy translated into multiple languages with consistent tone:

1. **Step 1** — Generate initial marketing copy from product details and target audience
2. **Gate** — Validate against tone guide and campaign goals
3. **Step 2** — Translate the validated copy into multiple languages
4. **Gate** — Ensure translations retain tone and key messages
5. **Step 3** — Format translated copy for each platform (email, social media, website)
6. **Output** — Finalized, multilingual marketing materials ready for deployment

### Content production pipeline

A marketing team's content workflow as a chain of agents:

1. **Research Agent** — Receives a topic brief, gathers data from web sources and internal docs, outputs a structured research summary.
2. **Writer Agent** — Receives the research summary, drafts an article following brand guidelines.
3. **Editor Agent** — Receives the draft, checks for clarity, accuracy, and tone. Outputs a revised version.
4. **SEO Agent** — Receives the edited article, optimizes headlines, metadata, and keyword placement. Outputs the final publish-ready piece.

The Writer never sees raw search results — it receives a clean brief from the Research Agent. The SEO Agent never rewrites for tone — that's already handled.

### Support ticket handling

1. **Classify** — Read the incoming ticket, categorize it (billing, technical, returns), and extract key details.
2. **Look up policy** — Find the relevant policy for that category and determine what actions are permitted.
3. **Draft** — Write a customer-facing response within the classification and policy constraints.
4. **Compliance check** — Review the draft for regulatory compliance before it's sent.

Every ticket takes the same four steps, so the path is fixed. If the category instead chose *which* steps ran next, that would be [Routing](../routing/).

## How to Implement

1. **Decompose the task** — Identify the logical subtasks that make up the overall goal
2. **Define validation criteria** — Establish clear checkpoints (gates) to evaluate outputs after each step, and decide whether each is checked by code or judged by the AI
3. **Connect steps programmatically** — Design the workflow so outputs from one step feed into the next, passing only what the next step needs
4. **Test and refine** — Ensure each step performs as intended and adjust based on intermediate results

## Sources

- Anthropic — [Building effective agents](https://www.anthropic.com/research/building-effective-agents) (December 19, 2024) — "Workflow: Prompt chaining", including programmatic checks ("gates") between steps
- Google Cloud — [Choose a design pattern for your agentic AI system](https://docs.cloud.google.com/architecture/choose-design-pattern-agentic-ai-system) (last reviewed May 28, 2026) — the multi-agent sequential pattern
- Microsoft — [AI Agent Orchestration Patterns](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/ai-agent-design-patterns), Azure Architecture Center (accessed 2026-10-24) — "Sequential orchestration"
- Google Developers Blog — [Developer's guide to multi-agent patterns in ADK](https://developers.googleblog.com/developers-guide-to-multi-agent-patterns-in-adk/) (December 16, 2025) — the sequential pipeline pattern
- CrewAI — [Processes](https://docs.crewai.com/v1.15.30/en/concepts/processes) (v1.15.30 docs, accessed 2026-10-24) — the sequential process, "with the output of one task serving as context for the next"

## Related

- [Workflow Architecture Patterns Overview](../)
- [Augmented LLM](../augmented-llm/) — the foundation this pattern builds on
- [Routing](../routing/) — another structured workflow, for branching paths
- [Parallelization](../parallelization/) — run independent stages at the same time instead of in order
- [Evaluator-Optimizer](../evaluator-optimizer/) — iterative refinement with feedback loops
- [Orchestrator-Workers](../orchestrator-workers/) — when the stages aren't fixed
- [Design Your AI Workflow](../../../ai-workflow-framework/design/)
