# Agent Gallery

Example agents, skills, and prompts that previously shipped in the Hands-on AI plugin marketplace. These are preserved here as **study material** rather than installable tools — they're useful as templates to copy and customize for your own workflows, but they were too narrowly scoped to bundle into the production `handsonai` plugin.

The companion docs page at [handsonai.info/use-cases/example-gallery/](https://handsonai.info/use-cases/example-gallery/) describes each one and when you'd adapt it.

## Contents

### `agents/`
Seven research and writing agents. Use these as templates for building agents that match a specific persona, source list, or output format.

- `tech-executive-writer.md` — translates technical AI/data topics for business audiences
- `hbr-editor.md` — edits business writing to HBR publication standards
- `hbr-publisher.md` — formats finalized articles for web + PDF distribution
- `ai-news-researcher.md` — daily AI industry news scan across major vendors and outlets
- `ai-productivity-researcher.md` — gathers HBR-tier case studies of enterprise AI adoption
- `claude-research-daily.md` — vendor-specific researcher (Anthropic / Claude / Cowork)
- `meeting-prep-researcher.md` — researches attendees and companies before a meeting

### `skills/`
Five skills paired with the agents above (or independently useful). Each skill is a self-contained folder you can drop into any Claude Code plugin or upload to Claude.ai / Cowork.

- `editing-hbr-articles/` — editorial criteria for HBR-grade business writing
- `preparing-meeting-briefs/` — structured meeting prep brief format
- `drafting-linkedin-posts/` — LinkedIn post structure with hook, body, CTA, hashtags
- `extracting-article-insights/` — pulls key insights and quotable points from source articles
- `syncing-skills-to-github/` — Notion → GitHub sync for an AI skill registry

### `prompts/`
Three portable prompts that work in any AI tool (ChatGPT, Gemini, M365 Copilot, Claude.ai). Copy the prompt, fill in the blanks, and run.

- `buyer-persona-revenue-leader-rachel.md` — example buyer persona for a SaaS revenue leader
- `linkedin-prospect-research.md` — workflow that takes a buyer persona and identifies 5 LinkedIn prospects
- `meeting-prep-quick.md` — single-shot meeting prep prompt

## How to Adapt These

1. **Pick the agent or skill closest to your need.** Don't start from scratch — examples are 80% of the way there.
2. **Replace persona-specific framing.** "HBR senior editor" becomes "the lead editor at our internal blog." "Anthropic / Claude / Cowork" becomes "OpenAI / GPT / your tool."
3. **Update source lists.** Researchers fail when their source list is wrong for your domain. Replace it with sources you actually trust.
4. **Test on a real example.** Run the adapted agent or skill against a representative input before committing to it.

## License

MIT — same as the main repo. Copy, modify, and ship freely.
