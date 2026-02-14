---
title: Model
description: The Model building block — the AI engine that processes inputs and generates outputs, powering everything the other building blocks do
---

# Model

> **Platforms:** `claude` `openai` `gemini` `m365-copilot`

## What a Model Is

A **model** is the AI engine that powers everything. It's a system trained on data that takes input and produces output through learned patterns — generating text, writing code, analyzing images, or reasoning through complex problems.

Every other building block depends on a model. Prompts steer it. Context informs it. Projects organize work for it. Skills package routines for it. Agents orchestrate it. MCP connects it to external systems. Without a model, the other blocks have nothing to run on.

## Key Characteristics

- **Trained on data** — a model's knowledge comes from its training data, with a cutoff date after which it has no information
- **Come in capability tiers** — from fast, lightweight models for simple tasks to deep reasoning models for complex analysis
- **Have defined context windows** — how much information (measured in tokens) a model can process at once
- **Vary by modality** — some handle only text, others work with code, vision, audio, or multiple modalities together

## Model Capabilities

Different models excel at different things. Here are the key capability dimensions to consider:

| Capability | What It Means | Example Tasks |
|-----------|---------------|---------------|
| **Reasoning** | Complex analysis, multi-step logic, nuanced judgment | Strategy analysis, research synthesis, debugging complex systems |
| **Code generation** | Writing, debugging, and explaining code | Building features, fixing bugs, code review |
| **Multimodal** | Processing or generating images, audio, or video | Analyzing charts, describing photos, transcribing audio |
| **Speed** | Fast response for simple, high-volume tasks | Summarization, formatting, classification, triage |
| **Context window** | How much input the model can handle at once | Processing long documents, large codebases, multi-file analysis |
| **Tool use** | Calling functions, APIs, and external tools | Running code, searching the web, querying databases |

## When to Use It (Model Selection Guidance)

Choosing the right model for the task is one of the highest-leverage decisions you can make:

| Task Type | Recommended Model Tier | Why |
|-----------|----------------------|-----|
| Simple tasks (summarization, formatting, classification) | Fast, lightweight models | Speed and cost matter more than depth |
| Complex analysis (research, strategy, multi-step reasoning) | Reasoning-capable models | Accuracy and depth matter more than speed |
| Visual tasks (image analysis, diagram interpretation) | Multimodal models | The task requires understanding non-text inputs |
| Code-heavy work (building features, debugging, refactoring) | Code-optimized models | Specialized training produces better code output |
| High-volume automation (batch processing, triage) | Fast models with tool use | Throughput and cost-efficiency are priorities |

!!! tip "Cost-quality tradeoff"
    Not every task needs the most powerful model. Using a fast model for simple tasks and reserving reasoning models for complex ones saves cost without sacrificing quality. Many platforms let you route different tasks to different models within the same workflow.

## Foundational Concepts

These concepts help you understand what a model is and how it works:

**Parameters** — The internal weights that define a model's learned patterns. More parameters generally means more capability, but also more computational cost. You don't set parameters — they're determined during training.

**Tokens** — How models measure input and output. A token is roughly 3-4 characters of English text. Models have limits on how many tokens they can process (input) and generate (output) per request.

**Context window** — The total number of tokens a model can handle in a single interaction, including both the input you provide and the output it generates. Larger context windows let you work with longer documents and more complex inputs.

**Temperature** — A setting that controls randomness in outputs. Low temperature (0.0) produces more deterministic, focused responses. High temperature (1.0+) produces more creative, varied responses. Most platforms default to a balanced setting.

**Training data and knowledge cutoff** — Models learn from data up to a specific date. They don't know about events, products, or information published after their cutoff. This is why context (providing current information) is essential for tasks involving recent data.

**Fine-tuning** — Customizing a pre-trained model on your specific data to improve performance for your domain. Most users don't need to fine-tune — prompt engineering and context are usually sufficient — but it's available for specialized use cases.

## Where to Find Models

| Source | What's Available | Best For |
|--------|-----------------|----------|
| **Anthropic (Claude)** | Claude model family across capability tiers | Reasoning, code, analysis, long context |
| **OpenAI** | GPT and reasoning model families | General purpose, reasoning, multimodal |
| **Google** | Gemini model family | Multimodal, Google ecosystem integration |
| **Open-source hubs (Hugging Face)** | Thousands of community and enterprise models | Custom deployment, fine-tuning, specialized tasks |

!!! info "Open-source vs. proprietary"
    Proprietary models (Claude, GPT, Gemini) are accessed via APIs and platforms — you don't host them yourself. Open-source models (Llama, Mistral, and others on Hugging Face) can be downloaded and run on your own infrastructure, offering more control but requiring more technical setup.

## Platform Implementations

| Platform | How It Works |
|----------|-------------|
| **Claude** | Multiple model tiers (fast, balanced, reasoning); select via model picker in conversation or API parameter |
| **OpenAI (ChatGPT)** | Multiple model tiers (fast, balanced, reasoning); select via model picker in conversation or API parameter |
| **Gemini** | Multiple model tiers (fast, balanced); select via model picker in conversation or API parameter |
| **M365 Copilot** | Models managed by Microsoft; limited user selection based on Copilot context |

## Relationship to Other Blocks

Model is the foundation — the engine everything else runs on:

- **Prompts** steer the model — telling it what to do
- **Context** informs the model — giving it knowledge it wasn't trained on
- **Projects** organize work for the model — grouping instructions and context
- **Skills** package routines for the model — reusable workflows it executes
- **Agents** orchestrate the model — directing it through multi-step tasks
- **MCP** connects the model — giving it access to external tools and data

## Related

- [Agentic Building Blocks](../index.md) — Model in the context of all seven building blocks
- [AI Use Cases](../../use-cases/index.md) — what teams build with these blocks, organized by six primitives
- [Prompts](../prompts/index.md) — the instructions that steer the model
- [Context](../context/index.md) — the knowledge that informs the model
- [Projects](../projects/index.md) — workspaces that organize work for the model
- [Skills](../skills/index.md) — reusable routines the model executes
- [Agents](../agents/index.md) — autonomous systems that orchestrate the model
- [MCP](../mcp/index.md) — connectors that extend the model's reach
- [Platforms](../../platforms/index.md) — platform-specific model guides
