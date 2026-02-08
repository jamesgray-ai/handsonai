#!/usr/bin/env python3
"""Generate docs/whats-new.md from GitHub Releases.

Fetches published (non-draft) releases from the GitHub API and writes a
Markdown page suitable for MkDocs.  Uses only Python stdlib — no pip
installs required.

For local preview:
    python scripts/generate_whats_new.py && mkdocs serve

Set GITHUB_TOKEN for a higher API rate limit (automatic in GitHub Actions).
"""

import json
import os
import ssl
import urllib.request
from datetime import datetime
from pathlib import Path

REPO = "jamesgray-ai/handsonai"
API_URL = f"https://api.github.com/repos/{REPO}/releases"
OUTPUT = Path(__file__).resolve().parent.parent / "docs" / "whats-new.md"

FRONTMATTER = """\
---
title: "What's New"
description: Recent updates to the Hands-on AI Cookbook — new guides, updated content, and new Q&As.
---
"""

INTRO = """\
# What's New

Recent updates to the Hands-on AI Cookbook. This page is generated
automatically from [GitHub Releases](https://github.com/{repo}/releases)
— subscribe to the repo or check back here to stay current.

---

""".format(repo=REPO)

PLACEHOLDER = """\
No updates published yet — check back soon!
"""


def _ssl_context():
    """Build an SSL context, trying certifi first for macOS compatibility."""
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ssl.create_default_context()


def fetch_releases():
    """Return a list of published (non-draft, non-prerelease) releases."""
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    req = urllib.request.Request(API_URL, headers=headers)
    ctx = _ssl_context()
    with urllib.request.urlopen(req, context=ctx) as resp:
        data = json.loads(resp.read().decode())

    return [
        r for r in data
        if not r.get("draft") and not r.get("prerelease")
    ]


def format_release(release):
    """Format a single release as a Markdown section."""
    name = release.get("name") or release.get("tag_name", "Untitled")
    published = release.get("published_at", "")
    body = (release.get("body") or "").strip()

    date_str = ""
    if published:
        dt = datetime.strptime(published, "%Y-%m-%dT%H:%M:%SZ")
        date_str = f"{dt.strftime('%B')} {dt.day}, {dt.year}"

    lines = [f"## {name}"]
    if date_str:
        lines.append(f"\n*{date_str}*")
    if body:
        lines.append(f"\n{body}")
    lines.append("")  # trailing newline
    return "\n".join(lines)


def main():
    releases = fetch_releases()

    parts = [FRONTMATTER, INTRO]
    if releases:
        parts.extend(format_release(r) for r in releases)
    else:
        parts.append(PLACEHOLDER)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text("\n".join(parts))
    print(f"Wrote {OUTPUT} ({len(releases)} release(s))")


if __name__ == "__main__":
    main()
