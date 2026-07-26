---
name: publishing-playbook-updates
description: >
  Draft and publish curated changelog entries for the Hands-on AI Playbook. Scans
  git history for meaningful changes, drafts a short blog post, presents it for
  review, writes the file, and notifies Slack. Use when: (1) James wants to post
  a playbook update, (2) user says "publish update" or "changelog entry", or
  (3) user runs /publishing-playbook-updates.
---

# Publishing Playbook Updates

Draft a curated changelog entry from recent git history, get approval, publish it, and notify Slack.

## Workflow

1. **Find the last changelog entry date**

   Look at the most recent file in `src/content/docs/blog/` to determine the date range. Use the date from the filename (format: `YYYY-MM-DD-slug.md`).

2. **Scan recent changes**

   Run:
   ```bash
   git log --oneline --since="YYYY-MM-DD" -- src/content/docs/ plugins/ .claude/
   git diff --stat HEAD~30 -- src/content/docs/ plugins/ .claude/
   ```

   > **Use `src/content/docs/`, not `docs/`.** There is no top-level `docs/` directory in
   > this repo — CLAUDE.md uses `docs/…` as shorthand when describing sections, but the real
   > path is `src/content/docs/…`. Passing `docs/` to `git log` matches nothing and returns
   > **zero commits**, which reads as "no changes to publish" rather than as an error. If the
   > scan comes back empty, check this first.

   Group changes by category:
   - **New Content** — New pages added to `src/content/docs/`
   - **Plugins** — Changes to `plugins/` or `.claude/skills/` or `.claude/agents/`
   - **Platform Updates** — Changes to `src/content/docs/platforms/`
   - **Builder Setup** — Changes to `src/content/docs/builder-setup/`
   - **Courses** — Changes to `src/content/docs/courses/`

3. **Filter for signal**

   Ignore:
   - Typo fixes, formatting tweaks, whitespace changes
   - Sidebar-only changes in `astro.config.mjs`
   - CI/CD config changes (`.github/`)
   - Script changes (`scripts/`)
   - CSS-only changes
   - Changes to `src/components/` (layout-only)

   Surface:
   - New documentation pages
   - New or updated plugins, agents, skills
   - Significant content rewrites (not minor edits)
   - New questions answered
   - New resources added

4. **Draft a changelog entry**

   Create a draft with this structure:

   ```markdown
   ---
   date: YYYY-MM-DD
   authors:
     - jamesgray
   tags:
     - <tag>
   description: "<one-line summary of the update>"
   title: "<Headline summarizing the theme>"
   ---

   <2-3 sentence overview of what changed and why it matters.>

   <!-- more -->

   <Details for each notable change — 2-4 sentences each with links to the new/changed pages.>
   ```

   > **The headline goes in `title:` frontmatter, not an `# H1`.** Starlight renders the
   > frontmatter title as the page heading, so an H1 in the body produces a duplicate
   > heading. All existing posts follow this — verified 2026-07-26: 24 of 24 use `title:`
   > and none contain a body H1.

   Rules:
   - Filename format: `src/content/docs/blog/YYYY-MM-DD-<slug>.md`
   - Use today's date
   - Keep it short and scannable — this is a changelog, not a blog post
   - Link to playbook pages with site-root paths (e.g., `/agentic-building-blocks/agents/`), matching every existing post
   - If a related Substack article was published, cross-reference it
   - Tags: `New Content`, `Plugins`, `Platform Updates`, `Framework`, `Announcements`
   - Multiple tags can be listed if the update spans areas

5. **Present for review**

   Show the full draft to James. Ask:
   > "Here's the draft changelog entry. Want to adjust anything before I publish it?"

   Wait for approval. James may:
   - Approve as-is
   - Edit the content (make the changes he requests)
   - Add context ("this was built because a student asked...")
   - Reject (stop here)

6. **Create the file**

   Write the approved entry to `src/content/docs/blog/YYYY-MM-DD-<slug>.md`.

7. **Build, then commit and push**

   Run `npm run build` and `node scripts/check-links.js` before pushing. The build confirms
   the post renders and appears in the homepage What's New section and `rss.xml`; the link
   checker catches any dead link in the new entry. Then commit and push to `main` — the site
   deploys automatically via CI.

8. **Notify Slack**

   After the commit is pushed **and the deploy has finished**, confirm the post URL returns
   HTTP 200, then run the notification script:
   ```bash
   curl -s -o /dev/null -w "%{http_code}\n" "https://handsonai.info/blog/YYYY-MM-DD-<slug>/"
   ./scripts/notify-slack.sh "<title>" "<one-line summary>" "https://handsonai.info/blog/YYYY-MM-DD-<slug>/"
   ```

   > **The blog URL is `/blog/YYYY-MM-DD-<slug>/`** — the same dated slug as the filename,
   > with no directory nesting. It is **not** `/blog/YYYY/MM/DD/<slug>/`; that form 404s.
   > This blog is hand-rolled via `BlogList.astro` over the `docs` collection rather than
   > driven by starlight-blog's own routes, so the URL is just the page's path. Verified
   > 2026-07-26. Check the 200 before notifying — the Slack post cannot be unsent, and a bad
   > link goes to two channels at once.

   Slack reaches other people. Show James the exact title, summary, and URL and get an
   explicit go-ahead before running the script — publishing the entry and broadcasting it
   are separate decisions.

   The script loads `.env` automatically. If the webhooks are not configured, it will skip with a message — remind James to set `SLACK_WEBHOOK_1` and `SLACK_WEBHOOK_2` in `.env` at the project root.

## Important Notes

- This skill is for James only — it is not published to the plugin marketplace
- The changelog is the single source of truth for updates — homepage, RSS, and Slack all derive from it
- Long-form content goes on Substack, not the changelog
- Always wait for explicit approval before writing the file
