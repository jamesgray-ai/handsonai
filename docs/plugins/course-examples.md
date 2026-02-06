---
title: Course Examples
description: Working examples of Claude Code agents and skills from the Hands-on AI cohort courses
---

# Course Examples

Working examples of agents and skills built during Hands-on AI cohort courses. This plugin demonstrates how to package domain expertise — writing standards, research processes, editorial criteria — into reusable components that Claude activates automatically. Install it to get a ready-made content creation and research toolkit, or study the components as blueprints for building your own.

## Install

```bash
/plugin install course-examples@handsonai
```

## Components

### Agents

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

    "Prepare talking points about generative AI's impact on enterprise
    operations for a board presentation"
    → Delivers a one-page brief with recommendations first, bullet-point
      findings, and clear next steps

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

    "Does this section on stakeholder capitalism make a strong argument?"
    → Evaluates argument strength, identifies gaps in evidence, suggests
      specific improvements, and provides rewritten passages

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

    "Take this whitepaper and get it ready for our website and also
    make a downloadable PDF"
    → Produces web-ready Markdown with heading structure, meta
      description, and tags, plus a PDF-formatted document

**What you'll get:** Two deliverables: (1) web-ready Markdown with SEO metadata, structured headings, pull quotes, and social media snippets; (2) a PDF-ready document with professional formatting, title page, and citations.

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

    "Has Anthropic released anything new lately?"
    → Focused research on Anthropic announcements, Claude updates,
      API changes, and related coverage

    "Find me some recent videos about Claude Code"
    → Searches AI-focused YouTube channels for tutorials, reviews,
      and demos

**What you'll get:** A categorized news report saved as a Markdown file in `ai-news-reports/`. Sections include: Product Releases & Updates, Research & Papers, Company Updates (with Anthropic/Claude highlighted), YouTube Content, Podcasts, Community Highlights, and Key Takeaways.

---

#### `ai-productivity-researcher`

**What it does:** Finds documented case studies of companies using AI for productivity gains. Prioritizes HBR-caliber sources with quantified outcomes — suitable for articles, presentations, and executive briefings.

**When to use it:** Use this when you need credible, data-backed examples of enterprise AI adoption for business writing, presentations, or research. Especially useful when building the evidence base for thought leadership pieces.

**How it works:** Claude conducts research across a tiered source hierarchy: Tier 1 (HBR, McKinsey, peer-reviewed journals, earnings calls), Tier 2 (WSJ, FT, TechCrunch, company newsrooms), and Tier 3 (conference presentations, verified LinkedIn posts). For each case study, it captures the company profile, specific AI implementation, quantified outcomes with timeframes, source attribution, and a credibility assessment.

**Example prompts:**

    "Find examples of companies using AI agents for customer support"
    → Researches documented implementations with specific metrics,
      company contexts, and credible source citations

    "What are some documented productivity gains from companies
    implementing AI tools?"
    → Compiles quantified results across industries with source
      validation and credibility ratings

**What you'll get:** Structured case study briefs with: company profile, AI implementation details, measurable outcomes, full source citations, credibility assessment, and relevance tags. Output format adapts to your need — executive summary, case study brief, comparative analysis, data table, or annotated bibliography.

---

#### `claude-research-daily`

**What it does:** Produces a daily brief on Anthropic, Claude, Claude Code, and Cowork. Covers official announcements, tech news, video content, tutorials, and community discussions from the last 24 hours.

**When to use it:** Use this as a morning briefing to stay current on the Claude ecosystem. Also useful when you need to check if Anthropic has made any recent announcements or when looking for new Claude-related content.

**How it works:** Claude searches official channels first (anthropic.com, GitHub releases), then news sites (TechCrunch, The Verge, Hacker News), community sources (Reddit, developer forums), video content (YouTube channels like AI Explained, Fireship, Matt Wolfe), and newsletters. It strictly filters for content from the last 24 hours — quiet days are reported as such rather than padded with older content.

**Example prompts:**

    "What's the latest news about Claude and Anthropic?"
    → Produces a structured daily brief covering top headlines,
      product updates, notable videos, tutorials, and community buzz

    "Have there been any new Claude Code features released recently?"
    → Focused search on Claude Code updates, new capabilities, and
      related documentation changes

**What you'll get:** A daily brief saved as `outputs/claude-research-daily-YYYY-MM-DD.md`. Sections include: Top Headlines, Product Updates, Notable Videos, Examples & Tutorials, Research & Technical, Quick Links, and Brief Info (sources checked, coverage window).

---

#### `meeting-prep-researcher`

**What it does:** Researches meeting attendees and companies, then produces a structured prep brief with profiles, talking points, and suggested questions.

**When to use it:** Use this before any meeting where you need context on the people or company — sales calls, partnership discussions, interviews, or client meetings. Especially valuable when meeting someone for the first time.

**How it works:** Claude gathers meeting details (who, what company, meeting type, your goal), then researches attendees (LinkedIn, recent posts, public statements, decision-making authority) and the company (recent news, strategic direction, competitive landscape, leadership changes). Findings are synthesized into a scannable brief designed to be read in under 5 minutes. The agent loads the `meeting-prep-research` skill for the structured research workflow.

**Example prompts:**

    "I have a meeting with Sarah Chen from Acme Corp tomorrow.
    Help me prepare."
    → Researches Sarah's role, recent activity, and conversation
      starters, plus Acme Corp's recent news, strategy, and
      competitive position

    "Put together a prep doc for my 2pm call with the marketing
    team at Rivian"
    → Produces a brief with attendee profiles, company snapshot,
      talking points, questions to ask, and potential watch-outs

**What you'll get:** A Meeting Prep Brief with: attendee profiles (background, recent activity, conversation starters), company snapshot (what they do, size, recent news, strategic priorities), suggested talking points with rationale, questions that demonstrate preparation and advance your goals, and watch-outs (sensitive topics, potential objections).

---

### Skills

---

#### `editing-hbr-articles`

**What it does:** Teaches Claude specific editorial criteria for editing articles to HBR publication quality. Loaded automatically by the `hbr-editor` agent, but can also be invoked directly.

**When to use it:** Use this when you want Claude to make direct, prescriptive edits to an article rather than just providing feedback. The skill focuses on hands-on editing rather than review.

**How it works:**

1. Read the article completely before making any edits
2. Assess against HBR editorial criteria (structure, evidence, voice, length)
3. Make direct edits to the file, prioritizing highest-impact issues first:
    - **Structure** — Does the opening hook? Is the thesis clear by paragraph 3?
    - **Evidence** — Are claims supported with specific data, named companies, credible sources?
    - **Redundancy** — Cut repeated points, excessive examples, conclusions that rehash the intro
    - **Voice** — Remove hedging, jargon, promotional language; strengthen to active voice
    - **Length** — Target 2,500-3,500 words for features, 1,500-2,500 for thought leadership
4. Provide an editorial summary: major changes, tightening metrics (word count before → after), and remaining considerations

**Example prompts:**

    "Edit this article to HBR quality"
    → Makes direct edits to the file following the priority order,
      then provides a summary of changes and word count reduction

**What you'll get:** Your article file edited in place, plus an editorial summary with major changes listed, word count reduction percentage, and optional improvements for the author to consider.

**Platform compatibility:** Claude Code &#10003;

---

#### `meeting-prep-research`

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
      with profiles, company snapshot, talking points, and questions

**What you'll get:** A structured Meeting Prep Brief (same format as the agent output) with attendee profiles, company snapshot, talking points, questions to ask, and watch-outs.

**Platform compatibility:** Claude Code &#10003; | Claude.ai &#10003;
