"""MkDocs hook to inject curated feed teaser into the homepage.

Renders the 6 most recent items as a flat grid with category badges.
"""

import html
import json
from pathlib import Path

PLACEHOLDER = "<!-- curated-feed -->"
TEASER_COUNT = 6


def _load_feed_items(docs_dir):
    """Load feed.json and return the first TEASER_COUNT items."""
    feed_path = Path(docs_dir) / "assets" / "data" / "feed.json"
    if not feed_path.is_file():
        return []

    data = json.loads(feed_path.read_text(encoding="utf-8"))
    return data.get("items", [])[:TEASER_COUNT]


def _time_ago(iso_string):
    """Simple relative time for build-time rendering."""
    from datetime import datetime, timezone

    try:
        published = datetime.fromisoformat(iso_string)
        seconds = (datetime.now(tz=timezone.utc) - published).total_seconds()
        if seconds < 3600:
            return f"{int(seconds // 60)}m ago"
        if seconds < 86400:
            return f"{int(seconds // 3600)}h ago"
        days = int(seconds // 86400)
        return "1 day ago" if days == 1 else f"{days} days ago"
    except (ValueError, TypeError):
        return ""


def on_page_markdown(markdown, page, config, files):
    """Replace the curated-feed placeholder with a flat grid of recent items."""
    if PLACEHOLDER not in markdown:
        return markdown

    items = _load_feed_items(config["docs_dir"])
    if not items:
        return markdown.replace(PLACEHOLDER, "")

    cards = '<div class="feed-teaser__row">\n'
    for item in items:
        title = html.escape(item.get("title", "Untitled"))
        url = html.escape(item.get("url", "#"))
        source = html.escape(item.get("source", ""))
        category = html.escape(item.get("category", ""))
        time_str = _time_ago(item.get("published", ""))

        cards += (
            f'<a href="{url}" target="_blank" rel="noopener" '
            f'class="feed-teaser__card">'
        )
        if category:
            cards += f'<span class="feed-teaser__category">{category}</span>'
        cards += f'<span class="feed-teaser__meta">{source}'
        if time_str:
            cards += f" &middot; {time_str}"
        cards += "</span>"
        cards += f'<span class="feed-teaser__title">{title}</span>'
        cards += "</a>\n"

    cards += "</div>\n"

    teaser_html = (
        '<h2 id="curated-feed">Curated AI Feed</h2>\n'
        '<p style="opacity: 0.7;">I follow dozens of AI sources so you don\'t have to. '
        "Here's what matters most right now.</p>\n"
        + cards
        + '\n<p><a href="/feed/" style="font-weight: 600;">View full feed &rarr;</a></p>\n'
    )

    return markdown.replace(PLACEHOLDER, teaser_html)
