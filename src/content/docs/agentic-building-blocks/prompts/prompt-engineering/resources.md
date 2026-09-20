---
title: Prompt Engineering Resources
description: "Academic papers, platform documentation, and practitioner references for prompt engineering techniques — zero-shot, few-shot, chain-of-thought, and more."
---Academic papers, platform guides, and practitioner references organized by technique. Each pattern page links to its most relevant papers; this page collects them all in one place.

## Platform Documentation

These official guides are maintained by the AI platform teams and reflect current best practices.

| Platform | Guide | Notes |
|----------|-------|-------|
| Anthropic (Claude) | [Prompt Engineering Guide](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview) | Comprehensive guide covering all major techniques |
| OpenAI (ChatGPT) | [Prompt Engineering Best Practices](https://platform.openai.com/docs/guides/prompt-engineering) | Strategies and tactics for better results |
| OpenAI (GPT-5.4) | [Prompt Guidance for GPT-5.4](https://developers.openai.com/api/docs/guides/prompt-guidance) | Model-specific guidance for long-running tasks, tool use, and reliable execution |
| Google Cloud | [Prompt Engineering Overview and Guide](https://cloud.google.com/discover/what-is-prompt-engineering#prompt-engineering-overview-and-guide) | Overview of prompt engineering concepts and techniques |

## Courses and Learning Resources

| Resource | Provider | Notes |
|----------|----------|-------|
| [Prompt Engineering Courses](https://www.edx.org/search?q=Prompt%20Engineering) | edX | University-backed courses on prompt engineering |
| [Prompt Engineering Courses](https://www.coursera.org/search?query=prompt%20engineering) | Coursera | Courses from industry and academic partners |
| [Prompting Guide](https://www.promptingguide.ai/) | DAIR.AI | Open-source guide covering techniques, applications, and research |

## Academic Papers by Technique

### Zero-Shot Prompting

- Brown et al. 2020 — *Language Models are Few-Shot Learners* — [arxiv.org/abs/2005.14165](https://arxiv.org/abs/2005.14165) — The GPT-3 paper that established the zero-shot paradigm, demonstrating that large language models can perform tasks from instructions alone
- Kojima et al. 2022 — *Large Language Models are Zero-Shot Reasoners* — [arxiv.org/abs/2205.11916](https://arxiv.org/abs/2205.11916) — Showed that adding "Let's think step by step" enables zero-shot chain-of-thought reasoning

### Few-Shot Learning

- Brown et al. 2020 — *Language Models are Few-Shot Learners* — [arxiv.org/abs/2005.14165](https://arxiv.org/abs/2005.14165) — Seminal paper demonstrating few-shot learning via text demonstrations
- Dong et al. 2022 — *A Survey on In-context Learning* — [arxiv.org/abs/2301.00234](https://arxiv.org/abs/2301.00234) — Comprehensive survey on why few-shot demonstrations work and how models learn in context

### Chain-of-Thought

- Wei et al. 2022 — *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models* — [arxiv.org/abs/2201.11903](https://arxiv.org/abs/2201.11903) — The seminal chain-of-thought paper showing step-by-step reasoning improves performance on math, logic, and commonsense tasks
- Kojima et al. 2022 — *Large Language Models are Zero-Shot Reasoners* — [arxiv.org/abs/2205.11916](https://arxiv.org/abs/2205.11916) — Zero-shot CoT: "Let's think step by step"
- Yao et al. 2023 — *Tree of Thoughts: Deliberate Problem Solving with Large Language Models* — [arxiv.org/abs/2305.10601](https://arxiv.org/abs/2305.10601) — Generalizes chain-of-thought into tree-structured reasoning with backtracking

### Direct Instruction

- Wei et al. 2021 — *Finetuned Language Models Are Zero-Shot Learners (FLAN)* — [arxiv.org/abs/2109.01652](https://arxiv.org/abs/2109.01652) — Foundation paper on instruction tuning
- Ouyang et al. 2022 — *Training Language Models to Follow Instructions with Human Feedback* — [arxiv.org/abs/2203.02155](https://arxiv.org/abs/2203.02155) — InstructGPT paper establishing RLHF for instruction following
- Zhang et al. 2023 — *Instruction Tuning for Large Language Models: A Survey* — [arxiv.org/abs/2308.10792](https://arxiv.org/abs/2308.10792) — Survey covering instruction tuning methods and their impact

### Contextual Prompting

- Dong et al. 2022 — *A Survey on In-context Learning* — [arxiv.org/abs/2301.00234](https://arxiv.org/abs/2301.00234) — Defines the in-context learning paradigm
- Lewis et al. 2020 — *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks* — [arxiv.org/abs/2005.11401](https://arxiv.org/abs/2005.11401) — RAG framework for augmenting prompts with retrieved context

### Role Prompting

- Kong et al. 2023 — *Better Zero-Shot Reasoning with Role-Play Prompting* — [arxiv.org/abs/2308.07702](https://arxiv.org/abs/2308.07702) — Role-play improved ChatGPT accuracy on AQuA from 53.5% to 63.8%
- Zheng et al. 2023 — *When "A Helpful Assistant" Is Not Really Helpful* — [arxiv.org/abs/2311.10054](https://arxiv.org/abs/2311.10054) — Important counterpoint: persona prompts don't reliably improve performance across all tasks

### Output Formatting

- Tam et al. 2024 — *Let Me Speak Freely? A Study on the Impact of Format Restrictions on Performance* — [arxiv.org/abs/2408.02442](https://arxiv.org/abs/2408.02442) — Shows format restrictions can degrade reasoning performance
- Liu et al. 2024 — *"We Need Structured Output": Towards User-centered Constraints on LLM Output* — [arxiv.org/abs/2404.07362](https://arxiv.org/abs/2404.07362) — User-centered perspective on structured output constraints

### Multi-Turn Conversation

- Yi et al. 2024 — *A Survey on Recent Advances in LLM-Based Multi-turn Dialogue Systems* — [arxiv.org/abs/2402.18013](https://arxiv.org/abs/2402.18013) — Survey covering dialogue management, context tracking, and coherence
- Zheng et al. 2025 — *LLMs Get Lost In Multi-Turn Conversation* — [arxiv.org/abs/2505.06120](https://arxiv.org/abs/2505.06120) — Documents a 39% average performance drop in multi-turn vs. single-turn interactions

### Self-Consistency and Reflection

- Wang et al. 2022 — *Self-Consistency Improves Chain of Thought Reasoning in Language Models* — [arxiv.org/abs/2203.11171](https://arxiv.org/abs/2203.11171) — Sampling diverse reasoning paths and selecting the most consistent answer
- Shinn et al. 2023 — *Reflexion: Language Agents with Verbal Reinforcement Learning* — [arxiv.org/abs/2303.11366](https://arxiv.org/abs/2303.11366) — Verbal self-reflection for iterative improvement
- Madaan et al. 2023 — *Self-Refine: Iterative Refinement with Self-Feedback* — [arxiv.org/abs/2303.17651](https://arxiv.org/abs/2303.17651) — Generate-critique-refine loop without external feedback

### Emotional Prompting

- Li et al. 2023 — *EmotionPrompt: Leveraging Psychology for Large Language Models Enhancement via Emotional Stimulus* — [arxiv.org/abs/2307.11760](https://arxiv.org/abs/2307.11760) — Showed 10%+ improvement on benchmarks using emotional stimuli, though effects vary by model and task

### Reframing Prompts

- Ma et al. 2023 — *Query Rewriting for Retrieval-Augmented Large Language Models* — [arxiv.org/abs/2305.14283](https://arxiv.org/abs/2305.14283) — Rewrite-Retrieve-Read framework for query reformulation

### Style Unbundling

- Lenny Rachitsky — *Five proven prompt engineering techniques* — [lennysnewsletter.com](https://www.lennysnewsletter.com/p/five-proven-prompt-engineering-techniques) — Practitioner origin of the style unbundling technique
- Liu et al. 2023 — *Learning to Generate Text in Arbitrary Writing Styles* — [arxiv.org/abs/2312.17242](https://arxiv.org/abs/2312.17242) — Academic research on style decomposition and reproduction

### Summarization and Distillation

- Adams et al. 2023 — *From Sparse to Dense: GPT-4 Summarization with Chain of Density Prompting* — [arxiv.org/abs/2309.04269](https://arxiv.org/abs/2309.04269) — Iterative increasing-density summarization technique
- Jin et al. 2024 — *A Comprehensive Survey on Process-Oriented Automatic Text Summarization* — [arxiv.org/abs/2403.02901](https://arxiv.org/abs/2403.02901) — Broad survey of summarization approaches

### Real-World Constraints

This is primarily a practitioner pattern. The academic literature on constrained generation focuses on technical format constraints rather than business constraints in prompts. See the platform documentation above for practical guidance.

## General References

These foundational papers cover topics relevant to multiple techniques.

- Schulhoff et al. 2024 — *The Prompt Report: A Systematic Survey of Prompting Techniques* — [arxiv.org/abs/2406.06608](https://arxiv.org/abs/2406.06608) — Comprehensive taxonomy of 58 prompting techniques with a unified terminology
- Zhou et al. 2022 — *Large Language Models Are Human-Level Prompt Engineers* — [arxiv.org/abs/2211.01910](https://arxiv.org/abs/2211.01910) — Automatic prompt optimization (APE)
- White et al. 2023 — *A Prompt Pattern Catalog to Enhance Prompt Engineering with ChatGPT* — [arxiv.org/abs/2302.11382](https://arxiv.org/abs/2302.11382) — Pattern-based approach to prompt engineering, similar to software design patterns

## Related

- [Prompt Engineering Overview](../)
- [Prompts Building Block](../)
