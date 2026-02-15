"""MkDocs hook to inject curated feed teaser into the homepage.

Renders a row per Inoreader folder, each showing up to 4 items as horizontal cards.
"""

import html
import json
from collections import OrderedDict
from pathlib import Path

PLACEHOLDER = "<!-- curated-feed -->"
ITEMS_PER_FOLDER = 4


def _load_feed_data(docs_dir):
    """Load feed.json and return (categories, items) grouped by folder."""
    feed_path = Path(docs_dir) / "assets" / "data" / "feed.json"
    if not feed_path.is_file():
        return {}

    data = json.loads(feed_path.read_text(encoding="utf-8"))
    items = data.get("items", [])

    # Group items by category, preserving order from JSON (newest first)
    grouped = OrderedDict()
    for item in items:
        cat = item.get("category", "Other")
        if cat not in grouped:
            grouped[cat] = []
        if len(grouped[cat]) < ITEMS_PER_FOLDER:
            grouped[cat].append(item)

    return grouped


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
    """Replace the curated-feed placeholder with a row-per-folder layout."""
    if PLACEHOLDER not in markdown:
        return markdown

    grouped = _load_feed_data(config["docs_dir"])
    if not grouped:
        return markdown.replace(PLACEHOLDER, "")

    sections = []
    for category, items in grouped.items():
        cat_escaped = html.escape(category)

        # Folder header with "View all" link
        section = (
            f'<div style="display: flex; align-items: baseline; justify-content: space-between;">'
            f'<h3 class="feed-teaser__heading">{cat_escaped}</h3>'
            f'<a href="/feed/?category={cat_escaped}" '
            f'style="font-size: 0.82em; opacity: 0.6; white-space: nowrap;">View all &rarr;</a>'
            f'</div>\n'
        )
        section += '<div class="feed-teaser__row">\n'

        for item in items:
            title = html.escape(item.get("title", "Untitled"))
            url = html.escape(item.get("url", "#"))
            source = html.escape(item.get("source", ""))
            time_str = _time_ago(item.get("published", ""))

            section += (
                f'<a href="{url}" target="_blank" rel="noopener" '
                f'class="feed-teaser__card">'
                f'<span class="feed-teaser__meta">{source}'
            )
            if time_str:
                section += f" &middot; {time_str}"
            section += "</span>"
            section += f'<span class="feed-teaser__title">{title}</span>'
            section += "</a>\n"

        section += "</div>\n"
        sections.append(section)

    teaser_html = (
        '<h2 id="curated-feed">Curated AI Feed</h2>\n'
        '<p style="opacity: 0.7;">I follow dozens of AI sources so you don\'t have to. '
        "Here's what matters most right now.</p>\n"
        + "\n".join(sections)
        + '\n<p><a href="/feed/" style="font-weight: 600;">View full feed &rarr;</a></p>\n'
    )

    return markdown.replace(PLACEHOLDER, teaser_html)
