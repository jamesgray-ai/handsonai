# Hands-on AI Playbook

The source repository for [handsonai.info](https://handsonai.info) — James Gray's playbook for building real things with AI: the AI Workflow Framework, the agentic building blocks, setup guides, patterns, and course companion content.

Almost everything here is markdown. This repository is a working example of a lesson it teaches: version control isn't only for code — the skills, agents, and documents AI works from live here too, moving through branches, pull requests, and reviews like any software project.

## Three ways to use the playbook

| Mode | What it is | Start here |
|------|------------|-----------|
| **Learn** | Read the playbook on the site — framework, building blocks, setup guides, patterns | [handsonai.info](https://handsonai.info) |
| **Build** | Install the plugins — the playbook's skills and agents, packaged for Claude | [Plugin marketplace](https://handsonai.info/use-the-playbook/build/) |
| **Ask** | Connect the MCP server and query the playbook from Claude, ChatGPT, Cursor, or VS Code | [MCP server guide](https://handsonai.info/mcp-server/) |

## What's in this repository

- `src/content/docs/` — the site's content: the [AI Workflow Framework](https://handsonai.info/ai-workflow-framework/), the [agentic building blocks](https://handsonai.info/agentic-building-blocks/), [builder setup guides](https://handsonai.info/builder-setup/), platform guides, use cases, and patterns
- `plugins/handsonai/` — the canonical source of the plugin-packaged skills and agents, distributed via [`handsonai-plugins`](https://github.com/jamesgray-ai/handsonai-plugins)
- `mcp-server/` — the MCP server that serves the playbook to AI tools, deployed on Cloudflare
- `.claude/` — repo-specific skills and agents that maintain the site itself
- `examples/` — worked example artifacts referenced from the playbook

## Running the site locally

```bash
npm install     # Astro/Starlight + plugins
npm run dev     # local dev server at http://localhost:4321
npm run build   # production build
```

## Contributing

Suggestions and fixes are welcome — see the [contributor guidelines](src/content/docs/CONTRIBUTING.md), then open a pull request. Every change to this repository travels the same path the playbook teaches: branch, commit, pull request, review, merge.

---

Built and maintained by [James Gray](https://jamesgray.ai) with AI collaborators — most changes here are co-authored with Claude, reviewed before merge.
