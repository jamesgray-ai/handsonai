---
title: Evaluation
description: Measuring whether AI systems produce good outputs — approaches, metrics, and practical guidance for building eval suites
---

# Evaluation

> **Platforms:** `claude` `openai` `gemini`

## What Evaluation Is

**Evaluation** (or "evals") is the practice of systematically measuring whether an AI system produces good outputs. It answers the question: *how do you know if your AI is working?*

Every time you change a prompt, swap a model, update instructions, or modify the context an AI sees, you need a way to tell whether the change made things better, worse, or had no effect. Evaluation gives you that signal.

Without evals, you're guessing. With evals, you're engineering.

## Why Evaluation Matters

- **Consistency** — Verify that your AI system performs reliably across different inputs, not just the examples you tested by hand
- **Regression detection** — Catch when a change to one part of your system breaks something elsewhere
- **Comparison** — Make informed decisions when choosing between models, prompts, or architectures
- **Confidence** — Ship changes knowing they've been measured, not just spot-checked
- **Iteration speed** — Tight feedback loops let you improve faster — change something, run evals, see the result

## Types of Evaluation

### Human Evaluation

People review AI outputs and rate them on criteria like accuracy, helpfulness, tone, and completeness. This is the gold standard for quality but expensive and slow.

**Best for:** Establishing ground truth, evaluating subjective qualities (tone, creativity), calibrating automated metrics.

### Automated Evaluation

Code-based checks that run without human involvement. These range from simple (did the output contain the expected keyword?) to sophisticated (does the JSON output match the schema?).

**Best for:** Fast iteration, regression testing, checking structural requirements, CI/CD pipelines.

**Examples:**

- String matching and regex checks
- Schema validation (JSON, XML)
- Code execution tests (does the generated code run?)
- Factual accuracy against known answers

### Model-as-Judge

Using one AI model to evaluate the output of another. The judge model receives the input, the output, and scoring criteria, then rates the result. This scales better than human evaluation while capturing nuance that simple automated checks miss.

**Best for:** Evaluating open-ended outputs at scale, measuring qualities like helpfulness or reasoning quality, comparing model versions.

**Trade-offs:** The judge model has its own biases. Calibrate against human judgments and watch for systematic blind spots.

### Reference-Based Evaluation

Comparing AI output against a known-good reference answer. Metrics like BLEU, ROUGE, and semantic similarity measure how close the output is to the expected result.

**Best for:** Tasks with clear correct answers — summarization, translation, question answering with known answers.

**Trade-offs:** Good outputs that differ from the reference may score poorly. Works best as one signal among many.

## Building an Eval Suite

A practical eval suite doesn't need to be complex. Start small and grow it as your system matures.

### 1. Define what "good" means

Before writing any eval, get specific about what a good output looks like for your use case. Is it accurate? Concise? Properly formatted? Safe? Different tasks have different quality dimensions.

### 2. Collect test cases

Build a set of representative inputs paired with expected behaviors. Include:

- **Happy path cases** — typical inputs that should work well
- **Edge cases** — unusual inputs, empty values, very long text
- **Failure cases** — inputs that should be refused or handled gracefully

Start with 20–50 cases. You can always add more.

### 3. Choose your eval methods

Mix evaluation types based on what matters:

| Quality dimension | Eval method |
|-------------------|-------------|
| Factual accuracy | Automated checks against known answers |
| Format compliance | Schema validation, regex |
| Helpfulness / tone | Model-as-judge with rubric |
| Safety | Automated filters + model-as-judge |
| Overall quality | Human evaluation (periodic) |

### 4. Automate and integrate

Run evals automatically when you change prompts, update instructions, or switch models. Even a simple script that runs your test cases and reports pass/fail rates is a major improvement over manual spot-checking.

### 5. Track over time

Record eval results so you can see trends. A prompt change that improves accuracy by 5% but degrades tone by 15% is a net loss — you need the data to see it.

## The Eval Mindset

Evaluation isn't a one-time activity you do before launch. It's a continuous practice — like testing in software engineering. The teams that build the best AI systems are the ones that eval relentlessly:

- Change a prompt → run evals
- Try a new model → run evals
- Add a tool → run evals
- Get a user complaint → add it as a test case → run evals

The goal isn't perfection. It's *knowing where you stand* and *improving deliberately*.

## Further Reading

- [Demystifying Evals for AI Agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) — Anthropic's practical guide to evaluating agentic systems
- [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents) — Anthropic's guide includes evaluation as a core practice
- [Eval Skills](https://developers.openai.com/blog/eval-skills/) — OpenAI's guide to building evaluation skills
- [OpenAI Evals](https://github.com/openai/evals) — OpenAI's open-source evaluation framework
- [Braintrust](https://www.braintrust.dev/) — evaluation and observability platform for AI applications
- [Promptfoo](https://www.promptfoo.dev/) — open-source tool for testing and evaluating LLM outputs

## Related

- [Product & Engineering](../product-engineering/index.md) — the parent section
- [Context Engineering](context-engineering.md) — designing the context that evals measure
- [Agentic Building Blocks](../agentic-building-blocks/index.md) — the components that evaluation applies to
- [Prompts](../agentic-building-blocks/prompts/index.md) — prompt changes are the most common trigger for re-evaluation
- [Patterns](../patterns/index.md) — reusable approaches including the Evaluator-Optimizer pattern
