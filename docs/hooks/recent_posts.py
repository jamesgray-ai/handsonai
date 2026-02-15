"""MkDocs hook to inject recent changelog entries into the homepage."""

import re
from datetime import datetime
from pathlib import Path


PLACEHOLDER = "<!-- latest-updates -->"
MAX_ENTRIES = 5
BRAND_COLOR = "#DDF222"


def _parse_blog_posts(docs_dir):
    """Scan blog/posts/ for markdown files and extract date, title, description, and URL."""
    posts_dir = Path(docs_dir) / "blog" / "posts"
    if not posts_dir.is_dir():
        return []

    entries = []
    for md_file in posts_dir.glob("*.md"):
        text = md_file.read_text(encoding="utf-8")

        # Extract date from frontmatter
        date_match = re.search(r"^date:\s*(\d{4}-\d{2}-\d{2})", text, re.MULTILINE)
        if not date_match:
            continue
        date = datetime.strptime(date_match.group(1), "%Y-%m-%d")

        # Extract description from frontmatter
        desc_match = re.search(r'^description:\s*["\'](.+?)["\']', text, re.MULTILINE)
        description = desc_match.group(1) if desc_match else ""

        # Extract title from first H1
        title_match = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
        title = title_match.group(1).strip() if title_match else md_file.stem

        # MkDocs Material blog generates: blog/<yyyy>/<mm>/<dd>/<slug>/
        slug = md_file.stem
        slug = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", slug)
        url = f"/blog/{date.strftime('%Y/%m/%d')}/{slug}/"

        entries.append((date, title, description, url))

    entries.sort(key=lambda e: e[0], reverse=True)
    return entries[:MAX_ENTRIES]


def on_page_markdown(markdown, page, config, files):
    """Replace the latest-updates placeholder with recent changelog entries."""
    if PLACEHOLDER not in markdown:
        return markdown

    entries = _parse_blog_posts(config["docs_dir"])
    if not entries:
        return markdown.replace(PLACEHOLDER, "")

    items = []
    for date, title, description, url in entries:
        date_str = date.strftime("%b %d")
        desc_html = f'<span style="opacity: 0.75;">{description}</span>' if description else ""
        items.append(
            f'<div style="border-left: 3px solid {BRAND_COLOR}; padding: 0.4em 0 0.4em 1em; margin-bottom: 0.75em;">'
            f'<strong style="opacity: 0.5; font-size: 0.85em;">{date_str}</strong><br>'
            f'<a href="{url}" style="font-weight: 600;">{title}</a><br>'
            f'{desc_html}'
            f'</div>'
        )

    updates_html = (
        '<h2 id="latest-updates">Latest Updates</h2>\n'
        + "\n".join(items)
        + '\n<p><small><a href="/blog/">View full changelog &rarr;</a></small></p>\n'
    )

    return markdown.replace(PLACEHOLDER, updates_html)
