---
name: drafting-linkedin-posts
description: >
  Draft a LinkedIn post from selected insights, key points, or a topic brief. Use when
  the user wants to create a LinkedIn post optimized for professional engagement. Produces
  a complete post with hook, body, CTA, and suggested hashtags. Works well when chained
  after extracting-article-insights for content repurposing workflows.
user-invocable: true
model: sonnet
effort: medium
---

# Drafting LinkedIn Posts

Transform selected insights or a topic brief into an engaging LinkedIn post optimized for professional engagement. Produces a ready-to-publish post with a clear hook, structured body, and call to action.

## Instructions

1. **Identify the single strongest angle.** If given multiple insights, select the one that is most surprising, actionable, or debate-worthy. The post should have one clear point — not a summary of everything.

2. **Write the hook (first 1-2 lines).** This is the only part visible before "see more." It must stop the scroll. Use one of these patterns:
   - **Bold claim:** "Most AI strategies fail because they start with the technology, not the problem."
   - **Surprising stat:** "87% of AI pilots never make it to production. Here's why."
   - **Contrarian take:** "The best AI teams I've worked with don't hire AI engineers first."
   - **Direct question:** "When was the last time you automated something that actually saved you time?"

3. **Write the body (3-5 short paragraphs).** LinkedIn readers scan — keep paragraphs to 1-3 sentences. Structure options:
   - **Problem → Insight → Implication:** State the problem, share the insight, explain what it means
   - **Story → Lesson → Application:** Brief anecdote, what it taught you, how readers can apply it
   - **List of points:** 3 numbered takeaways with one sentence each

4. **Write the CTA (final 1-2 lines).** Drive engagement with one of:
   - **Opinion prompt:** "What's your take — does this match what you're seeing?"
   - **Experience prompt:** "Have you tried this? What happened?"
   - **Share prompt:** "If this resonates, share it with someone building their first AI workflow."

5. **Formatting rules:**
   - Use line breaks between paragraphs (LinkedIn compresses text without them)
   - Bold sparingly — one or two key phrases per post, not every sentence
   - No more than 3 hashtags
   - Target 150-250 words total
   - Do not use emojis as bullet points or section markers

## Output Format

```
## LinkedIn Post Draft

**Angle:** [One sentence describing the core point]
**Hook pattern:** [bold claim | surprising stat | contrarian take | direct question]

---

[Full post text, formatted exactly as it would appear on LinkedIn — with line breaks between paragraphs]

---

**Hashtags:** #tag1 #tag2 #tag3
**Word count:** [N]
```
