<!--
  Question template for the Q&A library.

  Where to save:
    src/content/docs/questions/<slug>.md

  The slug becomes the URL: /questions/<slug>/

  The page footer ("← Back to Q&A" + alumni CTA) is rendered automatically
  by src/components/QuestionPageFooter.astro whenever `question:` is in
  the frontmatter — do not add CTA boilerplate to the body.

  The FAQPage JSON-LD schema is emitted automatically by
  src/components/Head.astro from `question` + `short_answer` frontmatter.
-->
---
question: "Your question here?"
short_answer: "Provide a 1-2 sentence direct answer. This is used for JSON-LD schema."
platforms: [openai, claude, gemini]
topic: prompting
date: 2026-01-24
author: Your Name
---

# Your question here?

**Short answer:** Provide a 1-2 sentence direct answer that immediately addresses the question. Keep this identical to the `short_answer` frontmatter field above.

## The Full Answer

Expand on the short answer with 2-4 paragraphs of detailed explanation. Include:

- Context for why this matters
- The underlying concepts
- When this applies (and when it doesn't)

Be thorough but focused. Every paragraph should add value toward answering the question.

## Code Example

```python
# Working code example that demonstrates the answer
# Include all necessary imports
# Add comments explaining key parts

def example_function():
    """Example showing how to implement the answer."""
    pass
```

## Key Takeaways

- First key point the reader should remember
- Second key point
- Third key point (keep to 3-5 bullet points)

## Related Questions

- [Related question 1?](./related-question-1.md)
- [Related question 2?](../other-category/related-question-2.md)
