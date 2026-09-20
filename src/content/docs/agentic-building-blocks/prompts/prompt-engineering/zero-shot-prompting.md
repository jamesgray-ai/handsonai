---
title: Zero-Shot Prompting
description: "Zero-shot prompting — instruct an LLM with no examples and rely on its training to complete the task, with tips for when it works and when to add examples."
---> **Platforms:** `claude` `openai` `gemini` `m365-copilot`

## What It Is

Zero-shot prompting means giving the model a task with no examples — just an instruction. It is the simplest form of prompting. The model relies entirely on its training data and instruction-tuning to interpret what you want and produce an appropriate response.

## Why It Works

Modern LLMs (large language models) are trained on massive datasets and fine-tuned to follow instructions through a process called RLHF (Reinforcement Learning from Human Feedback). They already know how to perform thousands of tasks — summarization, translation, classification, and more. You just need to describe what you want clearly enough for the model to match your request to patterns it has already learned.

## When to Use It

- Simple, well-understood tasks (summarize, translate, classify)
- When you don't have examples handy
- Quick exploration before investing in more complex prompts
- Tasks where the standard format is acceptable

## The Pattern

```text
{Task description}. {Optional constraints or specifications}.
```

**Filled-in example:**

```text
Summarize the following article in 3 bullet points, focusing on the key findings.
```

## Examples in Practice

### Translation

**Context:** You need a formal French translation of an English paragraph.

```text
Translate the following English text to French, maintaining a formal tone:

"We are pleased to announce that our quarterly results exceeded expectations,
driven by strong performance in the European market."
```

**Why this works:** Translation is a well-defined task the model has seen extensively in training, and specifying "formal tone" constrains the register.

### Classification

**Context:** You need to categorize incoming customer reviews for a dashboard.

```text
Classify the following customer review as positive, negative, or neutral.

Review: "The product arrived on time but the packaging was damaged."

Classification:
```

**Why this works:** The instruction is specific and the output space is constrained to three clear options, leaving no room for ambiguity.

### Content generation

**Context:** You need a quick out-of-office reply before heading on vacation.

```text
Write a professional out-of-office email reply. I'll be away from Feb 15-22
and Jane Smith (jane@company.com) will handle urgent requests.
```

**Why this works:** Out-of-office emails have a well-known format, so the model can produce a polished result without any examples.

## Zero-Shot Chain-of-Thought

A powerful variation of zero-shot prompting is **Zero-Shot CoT** (Chain-of-Thought). Simply appending "Let's think step by step" to a zero-shot prompt can dramatically improve performance on reasoning tasks (Kojima et al. 2022). This bridges zero-shot prompting and [Chain-of-Thought](../chain-of-thought/) prompting without requiring any examples.

```text
A store has 45 apples. They sell 60% in the morning and half of the remainder
in the afternoon. How many are left? Let's think step by step.
```

:::tip[Platform tip]

Claude's extended thinking mode essentially automates Zero-Shot CoT reasoning — the model reasons internally before responding. On OpenAI, the o1/o3 model family does this natively. Enable these features when tackling complex reasoning tasks where zero-shot alone falls short.
:::
## Common Pitfalls

:::caution[Too vague]

**Problem:** "Write something about marketing." gives the model too much freedom, producing generic, unfocused output.

**Fix:** Be specific — "Write a 200-word LinkedIn post about email marketing best practices for small businesses."
:::
:::caution[Assuming model knowledge]

**Problem:** Asking about your specific product, internal processes, or proprietary data without providing details. The model has no access to information it hasn't been trained on.

**Fix:** Include necessary context directly in the prompt, or switch to [Contextual Prompting](../contextual-prompting/) for tasks that require background information.
:::
:::caution[Complex tasks without structure]

**Problem:** Asking for multi-part analysis in a single sentence leads to incomplete or disorganized output.

**Fix:** Break the task into explicit steps or switch to [Chain-of-Thought](../chain-of-thought/) prompting for problems that require multi-step reasoning.
:::
## Related Techniques

- [Few-Shot Learning](../few-shot-learning/) — add examples when zero-shot isn't producing the right format or quality
- [Direct Instruction](../direct-instruction/) — make your zero-shot prompts more explicit with imperative commands
- [Chain-of-Thought](../chain-of-thought/) — add step-by-step reasoning for complex problems
- [Prompt Engineering Overview](../)
- [Content Creation use case](../../../../use-cases/content-creation/)

## Further Reading

- Kojima et al. 2022 — *Large Language Models are Zero-Shot Reasoners* — [arxiv.org/abs/2205.11916](https://arxiv.org/abs/2205.11916)
- Brown et al. 2020 — *Language Models are Few-Shot Learners* — [arxiv.org/abs/2005.14165](https://arxiv.org/abs/2005.14165)
