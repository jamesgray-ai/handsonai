---
name: openai-model-naming
description: OpenAI model versioning conventions and naming patterns as observed through mid-2026
metadata:
  type: reference
---

## Model family naming (as of June 2026)

OpenAI has moved to a decimal versioning scheme for GPT-5 variants:
- GPT-5 → GPT-5.1 → GPT-5.2 → GPT-5.3 → GPT-5.4 → GPT-5.5 (current family as of June 2026)
- Each version has sub-variants: `Instant` (fast/default), `Thinking` (reasoning), `Pro` (most capable)
- Retirements follow a pattern: older version deprecated from ChatGPT first, then API deprecation notice, then API removal ~6 months later

## Current state (June 2026)
- **GPT-5.5** is the current generation (released April 23, 2026); GPT-5.5 Instant is the default ChatGPT model
- **GPT-5.2** was removed from ChatGPT on June 12, 2026; conversations migrated automatically to GPT-5.5 equivalents
- **GPT-5.5 and o3 snapshots** notified for API deprecation June 11, 2026; API removal December 11, 2026
- **GPT Image (older)** models: notified June 2, 2026; API removal December 1, 2026

## Specialist models
- **GPT-Rosalind**: life sciences specialist model (enhanced biological reasoning, genomics, medicinal chemistry)
- **Codex**: AI coding agent product (now with 5M+ weekly users as of June 2026)

## Reasoning models
- **o3**, **o4-mini** are the current reasoning series (alongside GPT-5+ with "Thinking" mode)
