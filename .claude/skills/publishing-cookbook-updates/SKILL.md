---
name: publishing-cookbook-updates
description: >
  Draft and publish curated changelog entries for the Hands-on AI Cookbook. Scans
  git history for meaningful changes, drafts a short blog post, presents it for
  review, writes the file, and notifies Slack. Use when: (1) James wants to post
  a cookbook update, (2) user says "publish update" or "changelog entry", or
  (3) user runs /publishing-cookbook-updates.
---

# Publishing Cookbook Updates

Draft a curated changelog entry from recent git history, get approval, publish it, and notify Slack.

## Workflow

1. **Find the last changelog entry date**

   Look at the most recent file in `docs/blog/posts/` to determine the date range. Use the date from the filename (format: `YYYY-MM-DD-slug.md`).

2. **Scan recent changes**

   Run:
   ```bash
   git log --oneline --since="YYYY-MM-DD" -- docs/ plugins/ .claude/
   git diff --stat HEAD~30 -- docs/ plugins/ .claude/
   ```

   Group changes by category:
   - **New Content** — New pages added to `docs/`
   - **Plugins** — Changes to `plugins/` or `.claude/skills/` or `.claude/agents/`
   - **Platform Updates** — Changes to `docs/platforms/`
   - **Builder Setup** — Changes to `docs/builder-setup/`
   - **Courses** — Changes to `docs/courses/`

3. **Filter for signal**

   Ignore:
   - Typo fixes, formatting tweaks, whitespace changes
   - Nav-only changes in `mkdocs.yml`
   - CI/CD config changes (`.github/`)
   - Script changes (`scripts/`)
   - CSS-only changes
   - Changes to `docs/overrides/`

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
   categories:
     - <category>
   description: "<one-line summary of the update>"
   ---

   # <Headline summarizing the theme>

   <2-3 sentence overview of what changed and why it matters.>

   <!-- more -->

   <Details for each notable change — 2-4 sentences each with links to the new/changed pages.>
   ```

   Rules:
   - Filename format: `docs/blog/posts/YYYY-MM-DD-<slug>.md`
   - Use today's date
   - Keep it short and scannable — this is a changelog, not a blog post
   - Link to the actual cookbook pages using relative paths (e.g., `../../agentic-building-blocks/agents/index.md`)
   - If a related Substack article was published, cross-reference it
   - Categories: `New Content`, `Plugins`, `Platform Updates`, `Builder Setup`, `Courses`, `Announcements`
   - Multiple categories can be listed if the update spans areas

5. **Present for review**

   Show the full draft to James. Ask:
   > "Here's the draft changelog entry. Want to adjust anything before I publish it?"

   Wait for approval. James may:
   - Approve as-is
   - Edit the content (make the changes he requests)
   - Add context ("this was built because a student asked...")
   - Reject (stop here)

6. **Create the file**

   Write the approved entry to `docs/blog/posts/YYYY-MM-DD-<slug>.md`.

7. **Commit and push**

   Commit the new changelog entry and push to `main`. The site deploys automatically via CI, and the RSS feed updates with the new entry.

8. **Notify Slack**

   After the commit is pushed (so the link is live), run the Slack notification script:
   ```bash
   source .env
   ./scripts/notify-slack.sh "<title>" "<one-line summary>" "https://handsonai.info/blog/YYYY/MM/DD/<slug>/"
   ```

   If the webhook environment variables are not set, remind James to configure `SLACK_WEBHOOK_1` and `SLACK_WEBHOOK_2` in the `.env` file at the project root.

## Important Notes

- This skill is for James only — it is not published to the plugin marketplace
- The changelog is the single source of truth for updates — homepage, RSS, and Slack all derive from it
- Long-form content goes on Substack, not the changelog
- Always wait for explicit approval before writing the file
