---
name: openai-sources
description: Canonical OpenAI source URLs that are reliable for news gathering, changelog data, and product announcements
metadata:
  type: reference
---

Primary OpenAI sources (checked in priority order):

- **OpenAI News hub**: https://openai.com/news/ — product and company announcements; often returns HTTP 403 to WebFetch so use WebSearch with `site:openai.com` instead
- **API Changelog**: https://developers.openai.com/api/docs/changelog — fetchable directly via WebFetch; reliably returns structured changelog entries with dates; best source for API/platform changes
- **ChatGPT Release Notes**: https://help.openai.com/en/articles/6825453-chatgpt-release-notes — returns 403 to WebFetch; use WebSearch corroboration
- **Model Release Notes**: https://help.openai.com/en/articles/9624314-model-release-notes — same 403 issue; use WebSearch
- **OpenAI Developer Community**: https://community.openai.com — useful for deprecation notices (e.g., Agent Builder shutdown)
- **OpenAI Official X/Twitter**: corroborated via secondary press search

Reliable secondary sources confirmed in June 2026 research:
- TechCrunch (techcrunch.com) — model releases
- Fortune (fortune.com) — company/IPO news
- CNBC (cnbc.com) — acquisitions
- The Next Web (thenextweb.com) — acquisitions
- Bloomberg (bloomberg.com) — acquisitions, business deals
- Neowin (neowin.net) — product/feature updates
- Releasebot (releasebot.io) — good aggregation of ChatGPT/API release notes by month

**WebFetch note**: openai.com itself returns HTTP 403 for all pages. Use WebSearch for openai.com content, then fetch secondary press URLs for detail.
