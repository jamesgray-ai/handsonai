---
title: Business First AI
description: The Business-First AI Framework as executable Claude Code skills — discover opportunities, deconstruct workflows, and build with worked examples
---

# Business First AI

This plugin implements the [Business-First AI Framework](../business-first-ai-framework.md) as executable Claude Code skills. It covers all three phases: discover where AI fits in your workflows, deconstruct those workflows into AI building blocks, and build with worked examples across the autonomy spectrum. Install it to get a complete toolkit for going from "where should I use AI?" to working AI workflows.

## Install

```bash
/plugin install business-first-ai@handsonai
```

## Components

---

### Phase 1 — Discover

Find which workflows are candidates for AI.

---

#### `finding-ai-opportunities`

**What it does:** Runs a structured audit of your workflows to discover where AI can help. Produces a prioritized report of opportunities across three categories: Collaborative AI, Deterministic Workflows, and Multi-Agent Systems.

**When to use it:** Use this when you want to figure out where AI fits in your work. Especially useful when you're new to AI and need a starting point, or when you want a systematic review rather than ad-hoc experimentation.

**How it works:**

1. **Memory & history scan** — Claude reviews everything it knows about you from prior conversations, memory, and project files. Presents findings for you to confirm or correct.
2. **Targeted discovery interview** — Claude asks focused questions one at a time about your role, repetitive tasks, information synthesis, multi-step processes, quality issues, communication overhead, and decision-making. Follows up based on your answers.
3. **Opportunity analysis & report** — Produces a summary table and detailed opportunity cards grouped by category, ordered by impact.

**Example prompts:**

    "Help me find where AI can improve my workflows"
    → Runs the full three-step audit and produces a categorized
      opportunity report

    "I want to figure out which parts of my job could benefit from AI"
    → Interactive discovery session followed by a structured report
      with specific, actionable recommendations

**What you'll get:** An opportunity report (`outputs/ai-opportunity-report.md`) with a summary table and detailed cards for each opportunity. Each card includes: why it's a good candidate, the current pain point, how AI helps (specifically), and a practical first step.

**Platform compatibility:** Claude Code &#10003; | Claude.ai &#10003;

---

### Phase 2 — Deconstruct

Break workflows into AI building blocks.

---

#### `workflow-deconstructor`

**What it does:** Orchestrates the full three-step workflow deconstruction process. Runs discovery, analysis, and output generation sequentially, with file-based handoffs between stages so you can also run each step individually in separate conversations.

**When to use it:** Use this when you want to go through the entire deconstruction process in one session. The agent manages the flow between steps, saves intermediate files, and keeps you involved at each stage. If you prefer to work step-by-step across separate conversations, invoke the individual skills instead.

**How it works:** The agent runs three skills in sequence:

1. **Discovery** (`discovering-workflows`) — Interactive conversation where you describe your workflow. The agent probes for missing steps, decision points, data flows, and failure modes. Produces a Workflow Blueprint.
2. **Analysis** (`analyzing-workflows`) — Reads the Blueprint, classifies each step on an autonomy spectrum (Human → AI-Deterministic → AI-Semi-Autonomous → AI-Autonomous), and maps to AI building blocks. Produces a Workflow Analysis Document.
3. **Output Generation** (`generating-workflow-outputs`) — Reads the Analysis Document and generates a ready-to-use prompt plus recommendations for which steps should become dedicated skills. Produces the Baseline Prompt and Skill Recommendations.

Files are saved to `outputs/` using kebab-case workflow names (e.g., `outputs/lead-qualification-blueprint.md`).

**Example prompts:**

    "I want to deconstruct my client onboarding workflow"
    → Walks you through all three steps, asking questions during
      discovery, presenting the analysis for review, and generating
      the final deliverables

    "People keep dropping off during enrollment. Help me build
    a workflow for that."
    → Starts from a problem description, proposes a candidate
      workflow, then deconstructs it into building blocks

    "Help me figure out which parts of my weekly reporting process
    could be automated with AI"
    → Decomposes the reporting process, classifies each step by
      autonomy level, and identifies quick wins vs. complex
      automation opportunities

**What you'll get:** Four files in `outputs/`:

1. **Workflow Blueprint** — `[name]-blueprint.md` — structured decomposition of every step
2. **Workflow Analysis Document** — `[name]-analysis.md` — autonomy classification and AI building block mapping
3. **Baseline Workflow Prompt** — `[name]-prompt.md` — ready-to-use prompt with numbered steps
4. **Skill Build Recommendations** — `[name]-skill-recs.md` — specs for which steps should become dedicated skills

---

#### `discovering-workflows`

**What it does:** Interactively discovers and decomposes a business workflow into a structured Workflow Blueprint. This is Step 1 of 3 in the workflow deconstruction series.

**When to use it:** Use this when you want to thoroughly document a workflow before analyzing it for AI readiness. Also useful standalone when you just need a structured breakdown of a complex process — even without planning to automate it.

**How it works:**

1. **Scenario discovery** — Claude asks about the business scenario, objective, high-level steps, and ownership. One question at a time. If you describe a problem instead of a workflow, Claude proposes a candidate workflow for you to react to.
2. **Scope check** — Claude assesses whether this is one workflow or multiple bundled together. If multiple, it recommends splitting and asks which to start with.
3. **Name the workflow** — Claude presents 2-3 name options (2-4 word noun phrases, Title Case) and confirms name, description, outcome, trigger, and type.
4. **Deep dive** — For each step, Claude probes five dimensions:
    - Discrete steps (is this actually multiple steps?)
    - Decision points (if/then branches, quality gates)
    - Data flows (inputs, outputs, sources, destinations)
    - Context needs (specific documents, files, reference materials)
    - Failure modes (what happens when this step fails)
5. **Propose and react** — From step 4 onward, Claude proposes a hypothesis across all five dimensions and asks "What's right, what's wrong, what am I missing?"
6. **Map sequence** — Claude identifies sequential vs. parallel steps and the critical path
7. **Consolidate context** — Claude presents a rolled-up "context shopping list" of every artifact the workflow needs
8. **Generate Blueprint** — Claude writes the structured Blueprint to the output file

**Example prompts:**

    "Use discovering-workflows to break down my expense reporting process"
    → Interactive discovery session producing
      outputs/expense-reporting-blueprint.md

    "I need to document how our team handles customer escalations"
    → Walks through the discovery process, probing for hidden steps
      and decision points

**What you'll get:** A Workflow Blueprint file (`outputs/[name]-blueprint.md`) containing: scenario metadata, refined steps (with sub-steps, decision points, data flows, context needs, and failure modes for each), step sequence and dependencies, and a context shopping list.

**Platform compatibility:** Claude Code &#10003; | Claude.ai &#10003;

---

#### `analyzing-workflows`

**What it does:** Classifies workflow steps on the autonomy spectrum, maps them to AI building blocks, and produces a Workflow Analysis Document. This is Step 2 of 3 in the workflow deconstruction series.

**When to use it:** Use this when you have a Workflow Blueprint (from Step 1) and want to analyze which steps can be automated, which need human oversight, and what AI tools are required.

**How it works:**

1. **Load Blueprint** — Claude reads the Blueprint file from `outputs/`
2. **Confirm understanding** — Claude summarizes the workflow and asks you to confirm before proceeding
3. **Classify each step** — For every step, Claude determines:
    - **Autonomy level**: Human / AI-Deterministic / AI-Semi-Autonomous / AI-Autonomous
    - **AI building block(s)**: Prompt, Context, Skill, Agent, MCP, Project
    - **Tools and connectors**: External tools, APIs, and integrations needed
    - **Human-in-the-loop gates**: Where human review is recommended
4. **Present mapping** — Claude shows the classification as a table and walks through reasoning for non-obvious decisions. You can adjust classifications.
5. **Generate Analysis Document** — After your confirmation, Claude produces the complete document

**Example prompts:**

    "Use analyzing-workflows on my blueprint"
    → Reads the most recent Blueprint, classifies each step, presents
      the mapping table, and generates the Analysis Document

    "Analyze the lead-qualification blueprint for AI readiness"
    → Reads outputs/lead-qualification-blueprint.md and produces
      the analysis

**What you'll get:** A Workflow Analysis Document (`outputs/[name]-analysis.md`) containing: scenario summary, step-by-step decomposition table (with autonomy level and AI building blocks for each step), autonomy spectrum summary, step sequence and dependencies, prerequisites, context inventory, tools and connectors required, and recommended implementation order (quick wins first).

**Platform compatibility:** Claude Code &#10003; | Claude.ai &#10003;

---

#### `generating-workflow-outputs`

**What it does:** Generates a ready-to-use Baseline Workflow Prompt and Skill Build Recommendations from a Workflow Analysis Document. This is Step 3 of 3 in the workflow deconstruction series.

**When to use it:** Use this when you have a completed Analysis Document (from Step 2) and want the final, actionable deliverables — a prompt you can run immediately and specs for which steps should become dedicated skills.

**How it works:**

1. **Load Analysis Document** — Claude reads the Analysis Document from `outputs/`
2. **Confirm understanding** — Claude summarizes the workflow, step count, AI-eligible steps, and implementation order. You confirm before proceeding.
3. **Generate Baseline Workflow Prompt** — A self-contained, ready-to-use prompt with:
    - Title, purpose, and when to use it
    - Numbered steps, each labeled (AI) or (Human)
    - Input requirements with format specifications
    - Context requirements (what to attach when running the prompt)
    - Output format with structure specifications
4. **Generate Skill Build Recommendations** — For each step that should become a dedicated skill:
    - Skill name, purpose, inputs, outputs
    - Which baseline prompt steps it replaces
    - Integration points (external tools, APIs, MCP servers)
    - Priority level (High / Medium / Low)
    - Quick Start Prompt for invoking the skill

**Example prompts:**

    "Use generating-workflow-outputs on my analysis"
    → Reads the most recent Analysis Document, generates the prompt
      and skill recommendations

    "Generate the deliverables for expense-reporting"
    → Reads outputs/expense-reporting-analysis.md and produces both
      output files

**What you'll get:** Two files:

1. **Baseline Workflow Prompt** (`outputs/[name]-prompt.md`) — A self-contained prompt you can run immediately. Steps are labeled (AI) or (Human), includes all input/context/output requirements.
2. **Skill Build Recommendations** (`outputs/[name]-skill-recs.md`) — Specs for each recommended skill, in priority order, with Quick Start Prompts.

**Platform compatibility:** Claude Code &#10003; | Claude.ai &#10003;

---

### Phase 3 — Build

Turn deconstruction outputs into working AI workflows.

---

#### `tech-executive-writer`

**What it does:** Writes business-focused content about AI and technology, translating complex technical concepts for non-technical audiences. Combines deep technical understanding with executive-level communication skills.

**When to use it:** Use this when you need to write LinkedIn posts, magazine articles, executive briefs, or thought leadership pieces about AI topics. Especially useful when you need to explain technical concepts (like RAG, fine-tuning, or agentic AI) to business leaders.

**How it works:** Claude adopts the persona of a seasoned technology executive with 20+ years of experience and published articles in HBR and MIT Sloan Management Review. It first clarifies your audience, platform, length, and core message, then outlines an approach before drafting. Every piece is optimized for the target format — LinkedIn posts get strong hooks and hashtags, magazine articles get executive summaries and frameworks, executive briefs lead with recommendations.

**Example prompts:**

    "Write a LinkedIn post about how RAG is transforming enterprise search"
    → Drafts a 1,200-1,500 character post with a strong opening hook,
      plain-language explanation of RAG, business implications, and
      engagement prompt

    "Turn this technical documentation about our ML pipeline into an
    article suitable for Harvard Business Review"
    → Produces a 2,000-4,000 word article with executive summary,
      concrete analogies, named case studies, and actionable takeaways

**What you'll get:** Polished content tailored to your target platform and audience — ready to publish or use as a strong first draft. LinkedIn posts include hashtag suggestions. Articles include framework structures. Briefs lead with actionable recommendations.

---

#### `hbr-editor`

**What it does:** Reviews business articles against Harvard Business Review editorial standards. Provides prescriptive feedback — not just what's wrong, but exactly how to fix it.

**When to use it:** Use this when you have a draft article intended for a professional business audience and want publication-quality editorial feedback. Works for thought leadership pieces, feature articles, essays, and book chapters.

**How it works:** Claude adopts the persona of a senior HBR editor with 20+ years of experience. It reads your complete draft, then evaluates it against HBR's specific standards: the "Big Idea" test (is the central argument clear and compelling?), audience alignment, structure and flow, evidence quality, and voice. The agent loads the `editing-hbr-articles` skill for detailed editorial criteria, then provides structured feedback with line-level edits.

**Example prompts:**

    "Review this article for HBR quality"
    → Reads the full piece, provides an overall assessment, evaluates
      the central argument, identifies structural issues, flags weak
      evidence, and delivers line-level edits with before/after examples

**What you'll get:** A structured editorial review with: overall assessment, Big Idea evaluation, structure and flow analysis, evidence gaps, voice and language feedback, line-level edits (original → suggested → rationale), and a prioritized list of the 3-5 most important revisions.

---

#### `hbr-publisher`

**What it does:** Formats finalized articles for web publication and PDF distribution. Handles SEO metadata, social media snippets, and professional layout.

**When to use it:** Use this after your article has been through writing and editing stages and is ready for publication. It's the final step in the content pipeline: write → edit → publish.

**How it works:** Claude validates that the content is complete (title, author, abstract, body, citations), then produces two outputs. For web, it structures content with proper HTML-semantic headings, creates meta descriptions, suggests tags, adds pull quotes, and writes social media snippets for LinkedIn and X. For PDF, it creates a professionally formatted document with HBR-style headers, title page, typography hierarchy, page numbers, and proper citations.

**Example prompts:**

    "The article on leadership trends is edited and ready. Prepare it
    for publication."
    → Validates completeness, formats for web with SEO metadata and
      social snippets, creates PDF-ready document with professional
      layout

**What you'll get:** Two deliverables: (1) web-ready Markdown with SEO metadata, structured headings, pull quotes, and social media snippets; (2) a PDF-ready document with professional formatting, title page, and citations.

---

#### `ai-productivity-researcher`

**What it does:** Finds documented case studies of companies using AI for productivity gains. Prioritizes HBR-caliber sources with quantified outcomes — suitable for articles, presentations, and executive briefings.

**When to use it:** Use this when you need credible, data-backed examples of enterprise AI adoption for business writing, presentations, or research. Especially useful when building the evidence base for thought leadership pieces.

**How it works:** Claude conducts research across a tiered source hierarchy: Tier 1 (HBR, McKinsey, peer-reviewed journals, earnings calls), Tier 2 (WSJ, FT, TechCrunch, company newsrooms), and Tier 3 (conference presentations, verified LinkedIn posts). For each case study, it captures the company profile, specific AI implementation, quantified outcomes with timeframes, source attribution, and a credibility assessment.

**Example prompts:**

    "Find examples of companies using AI agents for customer support"
    → Researches documented implementations with specific metrics,
      company contexts, and credible source citations

**What you'll get:** Structured case study briefs with: company profile, AI implementation details, measurable outcomes, full source citations, credibility assessment, and relevance tags. Output format adapts to your need — executive summary, case study brief, comparative analysis, data table, or annotated bibliography.

---

#### `meeting-prep-researcher`

**What it does:** Researches meeting attendees and companies, then produces a structured prep brief with profiles, talking points, and suggested questions.

**When to use it:** Use this before any meeting where you need context on the people or company — sales calls, partnership discussions, interviews, or client meetings. Especially valuable when meeting someone for the first time.

**How it works:** Claude gathers meeting details (who, what company, meeting type, your goal), then researches attendees (LinkedIn, recent posts, public statements, decision-making authority) and the company (recent news, strategic direction, competitive landscape, leadership changes). Findings are synthesized into a scannable brief designed to be read in under 5 minutes. The agent loads the `preparing-meeting-briefs` skill for the structured research workflow.

**Example prompts:**

    "I have a meeting with Sarah Chen from Acme Corp tomorrow.
    Help me prepare."
    → Researches Sarah's role, recent activity, and conversation
      starters, plus Acme Corp's recent news, strategy, and
      competitive position

**What you'll get:** A Meeting Prep Brief with: attendee profiles (background, recent activity, conversation starters), company snapshot (what they do, size, recent news, strategic priorities), suggested talking points with rationale, questions that demonstrate preparation and advance your goals, and watch-outs (sensitive topics, potential objections).

---

#### `editing-hbr-articles`

**What it does:** Teaches Claude specific editorial criteria for editing articles to HBR publication quality. Loaded automatically by the `hbr-editor` agent, but can also be invoked directly.

**When to use it:** Use this when you want Claude to make direct, prescriptive edits to an article rather than just providing feedback. The skill focuses on hands-on editing rather than review.

**How it works:**

1. Read the article completely before making any edits
2. Assess against HBR editorial criteria (structure, evidence, voice, length)
3. Make direct edits to the file, prioritizing highest-impact issues first
4. Provide an editorial summary: major changes, tightening metrics, and remaining considerations

**Example prompts:**

    "Edit this article to HBR quality"
    → Makes direct edits to the file following the priority order,
      then provides a summary of changes and word count reduction

**What you'll get:** Your article file edited in place, plus an editorial summary with major changes listed, word count reduction percentage, and optional improvements for the author to consider.

**Platform compatibility:** Claude Code &#10003;

---

#### `preparing-meeting-briefs`

**What it does:** Provides a structured research workflow for meeting preparation. Loaded automatically by the `meeting-prep-researcher` agent, but can also be invoked directly.

**When to use it:** Use this when you want the step-by-step meeting research process without the full agent persona — useful when you want more control over the research flow.

**How it works:**

1. Gather meeting details — attendee name(s), company, meeting type, and your goal
2. Research attendees — LinkedIn profiles, recent posts, public activity
3. Research company — recent news (last 90 days), strategic direction, relevant context
4. Synthesize into a formatted Meeting Prep Brief
5. Refine with you — ask if any section needs more depth or adjustment

**Example prompts:**

    "Research John Park from Stripe before my call on Thursday"
    → Walks through the 5-step workflow, producing a scannable brief

**What you'll get:** A structured Meeting Prep Brief with attendee profiles, company snapshot, talking points, questions to ask, and watch-outs.

**Platform compatibility:** Claude Code &#10003; | Claude.ai &#10003;

---

### Utility

Agents for staying current on AI developments.

---

#### `ai-news-researcher`

**What it does:** Scans news outlets, blogs, YouTube channels, podcasts, and communities for the latest AI developments. Categorizes findings by significance and topic.

**When to use it:** Use this when you want to stay current on AI industry news — product releases, research papers, company updates, regulatory changes, and notable community discussions. Works as a daily briefing or for targeted research on specific topics.

**How it works:** Claude systematically searches across multiple source tiers: major tech news outlets (TechCrunch, The Verge, Wired), AI-specific publications (The Decoder, Import AI), official company blogs, social media, newsletters (The Batch, Ben's Bites, TLDR AI), community discussions (Hacker News, Reddit), product aggregators, podcasts (Latent Space, Practical AI), and YouTube channels. Each finding is categorized and rated by significance (Major, Notable, Minor).

**Example prompts:**

    "What's new in AI today?"
    → Produces a categorized news summary covering product releases,
      research papers, company updates, YouTube content, podcasts,
      and community highlights

**What you'll get:** A categorized news report saved as a Markdown file in `ai-news-reports/`. Sections include: Product Releases & Updates, Research & Papers, Company Updates (with Anthropic/Claude highlighted), YouTube Content, Podcasts, Community Highlights, and Key Takeaways.

---

#### `claude-research-daily`

**What it does:** Produces a daily brief on Anthropic, Claude, Claude Code, and Cowork. Covers official announcements, tech news, video content, tutorials, and community discussions from the last 24 hours.

**When to use it:** Use this as a morning briefing to stay current on the Claude ecosystem. Also useful when you need to check if Anthropic has made any recent announcements or when looking for new Claude-related content.

**How it works:** Claude searches official channels first (anthropic.com, GitHub releases), then news sites (TechCrunch, The Verge, Hacker News), community sources (Reddit, developer forums), video content (YouTube channels like AI Explained, Fireship, Matt Wolfe), and newsletters. It strictly filters for content from the last 24 hours — quiet days are reported as such rather than padded with older content.

**Example prompts:**

    "What's the latest news about Claude and Anthropic?"
    → Produces a structured daily brief covering top headlines,
      product updates, notable videos, tutorials, and community buzz

**What you'll get:** A daily brief saved as `outputs/claude-research-daily-YYYY-MM-DD.md`. Sections include: Top Headlines, Product Updates, Notable Videos, Examples & Tutorials, Research & Technical, Quick Links, and Brief Info (sources checked, coverage window).

---

### Prompts

---

#### `linkedin-prospect-research`

**What it does:** A deterministic prospecting prompt that finds and qualifies LinkedIn prospects against a buyer persona. Works with any AI tool — no plugin required.

---

#### `buyer-persona-revenue-leader-rachel`

**What it does:** An example buyer persona used as input to the LinkedIn prospect research workflow. Defines the ideal customer profile for a revenue-focused SaaS leader.

---

#### `meeting-prep-quick`

**What it does:** A portable one-shot meeting prep prompt. Copy and paste into any AI tool for quick meeting preparation without the full agent workflow.

---

## Recommended Workflow

The plugin covers the full Business-First AI Framework. Here's the recommended path:

1. **Discover** — Run `finding-ai-opportunities` to audit your workflows and identify where AI creates the most value
2. **Deconstruct** — Pick your highest-impact opportunity and run it through the `workflow-deconstructor` agent (or use the three skills individually: `discovering-workflows` → `analyzing-workflows` → `generating-workflow-outputs`)
3. **Build** — Use the Baseline Workflow Prompt on a real scenario, then build skills in priority order from the recommendations. Study the Phase 3 agents and skills as working examples.

## FAQ

**Which phase should I start with?**
Start with Phase 1 (Discover) if you're not sure where AI fits in your work. Start with Phase 2 (Deconstruct) if you already know which workflow you want to automate. Start with Phase 3 (Build) if you want to study working examples before deconstructing your own workflows.

**Can I start from a problem instead of a workflow?**
Yes. Tell the `workflow-deconstructor` agent about your problem (e.g., "people keep dropping off during enrollment") and it will propose a candidate workflow for you to refine during discovery.

**What if I lose context mid-conversation?**
The file-based handoffs mean you can continue in a new conversation. Just invoke the next skill and point it at the file from the previous step (e.g., "Use analyzing-workflows on outputs/lead-qualification-blueprint.md").

**What are AI building blocks?**
The categories used during analysis: Prompt (single instruction), Context (reference material), Skill (multi-step workflow), Agent (autonomous personality), MCP (external tool connection), and Project (workspace configuration). Each step gets mapped to one or more of these.

**Do I need Claude Code for all of this?**
No. The Phase 1 skill and Phase 2 skills work in Claude.ai too. The prompts work in any AI tool. The agents require Claude Code for automatic activation, but you can use the skill workflows manually anywhere.
