---
name: extracting-article-insights
description: >
  Extract key insights, themes, and quotable points from a source article for content
  repurposing. Use when the user wants to analyze an article, blog post, newsletter, or
  report to identify the most compelling points for reuse across channels. Produces a
  structured list of numbered insights with summaries, source quotes, and relevance tags.
user-invocable: true
---

# Extracting Article Insights

Analyze a source article and extract the most compelling insights for content repurposing. Produces a structured, numbered list of insights ready to be used by downstream content creation workflows.

## Instructions

1. **Read the full article** before extracting anything. Understand the overall argument, structure, and audience before identifying individual insights.

2. **Extract 5-7 key insights.** Look for:
   - Central arguments or thesis statements
   - Surprising data points, statistics, or research findings
   - Counterintuitive or contrarian claims
   - Actionable advice or frameworks
   - Memorable phrases or quotable language
   - Emerging trends or predictions

3. **Evaluate each insight for standalone value.** Each insight should make sense without reading the full article. If it requires too much context to understand, it's not a good candidate for repurposing.

4. **Capture a direct source quote for each insight.** Pull the exact language from the article that supports or expresses the insight. This preserves attribution and gives downstream content the option to quote directly.

5. **Tag each insight for relevance.** Use one of these tags:
   - `data` — Backed by numbers, research, or evidence
   - `opinion` — Author's perspective, argument, or prediction
   - `framework` — A model, process, or mental model readers can apply
   - `trend` — An emerging pattern or shift in the landscape
   - `story` — A narrative, anecdote, or case study

## Output Format

Present insights in this exact structure:

```
## Article Analysis: [Article Title]

**Source:** [Article URL or reference]
**Core theme:** [One-sentence summary of the article's main argument]

---

### Insight 1: [One-sentence summary]
**Source quote:** "[Exact quote from the article]"
**Relevance tag:** [data | opinion | framework | trend | story]
**Why it matters:** [One sentence explaining why this insight is compelling for repurposing]

### Insight 2: [One-sentence summary]
...

[Continue for all insights]

---

**Total insights extracted:** [N]
**Tag distribution:** [e.g., 2 data, 2 opinion, 1 framework, 1 trend, 1 story]
```
