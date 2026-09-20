---
title: Few-Shot Learning
description: "Few-shot learning — teach an LLM a new pattern by giving it a few worked examples directly in the prompt, with guidance on choosing and formatting examples."
---> **Platforms:** `claude` `openai` `gemini` `m365-copilot`

## What It Is

Few-shot learning means providing the model with a few examples of the task before asking it to perform on new input. The model learns the pattern from your demonstrations — the format, tone, reasoning approach, or classification rules — and applies it to the input you actually care about. This technique is sometimes called "in-context learning."

## Why It Works

LLMs (large language models) perform in-context learning: they recognize patterns in the examples you provide and apply those patterns to new inputs. This works because the model's core training objective is to predict the next token in a sequence, so it naturally continues patterns it sees. Your examples effectively "program" the model's behavior for the current conversation without any fine-tuning.

## When to Use It

- Custom output formats the model wouldn't produce naturally
- Classification tasks with your own categories or taxonomy
- Matching a specific tone or writing style
- Tasks where showing is easier than describing
- When [zero-shot prompting](../zero-shot-prompting/) produces the right idea but the wrong format

## The Pattern

```text
{Task description}

Example 1:
Input: {example input 1}
Output: {example output 1}

Example 2:
Input: {example input 2}
Output: {example output 2}

Example 3:
Input: {example input 3}
Output: {example output 3}

Now:
Input: {actual input}
Output:
```

**Filled-in example:**

```text
Classify each customer review using NPS-style labels: Promoter, Passive, or Detractor.

Example 1:
Input: "Absolutely love this product, already recommended it to three friends!"
Output: Promoter

Example 2:
Input: "It works fine, nothing special."
Output: Passive

Example 3:
Input: "Broke after two weeks. Waste of money."
Output: Detractor

Now:
Input: "Good quality but shipping took forever. Might order again if delivery improves."
Output:
```

## Examples in Practice

### Sentiment classification with custom labels

**Context:** Your team uses NPS-style categories (Promoter, Passive, Detractor) instead of the generic positive/negative/neutral labels most models default to.

```text
Classify each customer review using our NPS labels: Promoter, Passive, or Detractor.

Example 1:
Input: "Best purchase I've made all year. 10/10 would buy again."
Output: Promoter

Example 2:
Input: "Does what it says. Nothing more, nothing less."
Output: Passive

Example 3:
Input: "Customer support was unhelpful and the product is mediocre."
Output: Detractor

Now:
Input: "The interface is confusing but once you learn it, the features are solid."
Output:
```

**Why this works:** The examples define a custom taxonomy the model wouldn't use by default, and they show the boundary between categories through demonstration.

### Data extraction to structured format

**Context:** You receive unstructured emails and need to extract contact details into a consistent JSON format for your CRM.

```text
Extract the contact information from the text and return it as JSON.

Example 1:
Input: "Hey, this is Mike Chen from Acuity Labs. Reach me at mike@acuitylabs.io"
Output: {"name": "Mike Chen", "email": "mike@acuitylabs.io", "company": "Acuity Labs"}

Example 2:
Input: "Sarah Lopez, Director of Ops at Bridgewell Inc — sarah.lopez@bridgewell.com"
Output: {"name": "Sarah Lopez", "email": "sarah.lopez@bridgewell.com", "company": "Bridgewell Inc"}

Example 3:
Input: "Contact: James Rivera (james@deltaforge.co), he's with DeltaForge"
Output: {"name": "James Rivera", "email": "james@deltaforge.co", "company": "DeltaForge"}

Now:
Input: "Got a referral from Priya Patel at Nimbus Health — her email is priya.p@nimbushealth.org"
Output:
```

**Why this works:** The examples define the exact JSON structure, field names, and formatting conventions you need, removing all ambiguity about the output format.

### Tone matching

**Context:** You need to rewrite formal documentation into casual Slack messages for your team.

```text
Rewrite the formal text as a casual Slack message.

Example 1:
Input: "Please be advised that the server maintenance window has been scheduled for Saturday, March 15th, from 02:00 to 06:00 UTC."
Output: "Heads up — servers will be down Saturday 3/15 from 2-6am UTC for maintenance"

Example 2:
Input: "We would like to inform all stakeholders that the Q2 budget review meeting has been rescheduled to Thursday at 14:00."
Output: "Q2 budget review got moved to Thursday at 2pm — see you there"

Example 3:
Input: "It has come to our attention that several team members have not completed the mandatory security training module."
Output: "Friendly nudge: a few folks still need to finish the security training. Please knock it out when you get a chance"

Now:
Input: "We are pleased to announce that the organization has successfully achieved SOC 2 Type II compliance certification."
Output:
```

**Why this works:** Tone and style are notoriously hard to describe in words but easy to demonstrate through examples. The model picks up on the pattern of shortening, de-formalizing, and adding conversational markers.

## Common Pitfalls

:::caution[Too few or too many examples]

**Problem:** One example isn't enough to establish a reliable pattern. Ten or more examples waste tokens and can confuse the model.

**Fix:** Three to five examples is the sweet spot for most tasks. Use the minimum number that consistently produces the output format you want.
:::
:::caution[Example order effects]

**Problem:** Research shows that the order of examples affects output quality. The model pays more attention to examples near the end of the sequence.

**Fix:** Put your most representative example last (closest to the actual input). If results seem biased toward one category, vary the order and check whether outputs change.
:::
:::caution[Inconsistent examples]

**Problem:** Examples that contradict each other or use different formats confuse the model and produce unreliable output.

**Fix:** Ensure all examples follow the exact same format, use the same field names, and apply the same logic. Review your examples as a set before including them.
:::
## Related Techniques

- [Zero-Shot Prompting](../zero-shot-prompting/) — try this first when you don't need examples
- [Chain-of-Thought](../chain-of-thought/) — add reasoning steps to your examples for complex tasks
- [Output Formatting](../output-formatting/) — other ways to control the shape of model output
- [Prompt Engineering Overview](../)
- [Data Analysis use case](../../../../use-cases/data-analysis/)

## Further Reading

- Brown et al. 2020 — *Language Models are Few-Shot Learners* — [arxiv.org/abs/2005.14165](https://arxiv.org/abs/2005.14165)
- Dong et al. 2022 — *A Survey on In-context Learning* — [arxiv.org/abs/2301.00234](https://arxiv.org/abs/2301.00234)
