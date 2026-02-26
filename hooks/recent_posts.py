"""MkDocs hook to inject recent changelog entries into the homepage."""

import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path


PLACEHOLDER = "<!-- latest-updates -->"


def _slugify(title):
    """Convert a post title to a URL slug matching MkDocs Material blog behavior."""
    slug = title.lower()
    slug = re.sub(r"[^\w\s-]", "", slug)  # Remove punctuation
    slug = re.sub(r"[\s_]+", "-", slug)   # Spaces/underscores to hyphens
    slug = re.sub(r"-+", "-", slug)       # Collapse multiple hyphens
    return slug.strip("-")


def _git_commit_datetime(file_path):
    """Get the first (oldest) commit datetime for a file, as local time."""
    try:
        result = subprocess.run(
            ["git", "log", "--diff-filter=A", "--follow", "--format=%aI", "--", str(file_path)],
            capture_output=True, text=True, timeout=5,
        )
        lines = result.stdout.strip().splitlines()
        if lines:
            # Last line is the first commit (oldest); use it as the publish time
            return datetime.fromisoformat(lines[-1])
    except (subprocess.TimeoutExpired, OSError):
        pass
    return None


MAX_ENTRIES = 5
BRAND_COLOR = "#DDF222"

# Category styling: (border_color, chip_label, chip_bg, chip_text)
CATEGORY_STYLES = {
    "AI News": ("#BBBDC7", "AI News", "#BBBDC7", "#202621"),
}
DEFAULT_STYLE = (BRAND_COLOR, "Cookbook", BRAND_COLOR, "#202621")


def _parse_blog_posts(docs_dir):
    """Scan blog/posts/ for markdown files and extract date, title, description, and URL."""
    posts_dir = Path(docs_dir) / "blog" / "posts"
    if not posts_dir.is_dir():
        return []

    entries = []
    for md_file in posts_dir.glob("*.md"):
        text = md_file.read_text(encoding="utf-8")

        # Extract date from frontmatter (used for URL path and as fallback)
        date_match = re.search(r"^date:\s*(\d{4}-\d{2}-\d{2})", text, re.MULTILINE)
        if not date_match:
            continue
        frontmatter_date = datetime.strptime(date_match.group(1), "%Y-%m-%d")

        # Use git commit timestamp converted to UTC for precise ordering and display
        git_dt = _git_commit_datetime(md_file)
        if git_dt:
            utc_dt = git_dt.astimezone(timezone.utc).replace(tzinfo=None)
            display_date = utc_dt
        else:
            display_date = frontmatter_date

        # Extract description from frontmatter
        desc_match = re.search(r'^description:\s*["\'](.+?)["\']', text, re.MULTILINE)
        description = desc_match.group(1) if desc_match else ""

        # Extract first category from frontmatter
        cat_match = re.search(r'^categories:\s*\n\s*-\s*(.+)', text, re.MULTILINE)
        category = cat_match.group(1).strip().strip('"\'') if cat_match else ""

        # Extract title from first H1
        title_match = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
        title = title_match.group(1).strip() if title_match else md_file.stem

        # MkDocs Material blog generates URL from frontmatter date + title slug
        slug = _slugify(title)
        url = f"/blog/{frontmatter_date.strftime('%Y/%m/%d')}/{slug}/"

        entries.append((display_date, title, description, url, category))

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
    for date, title, description, url, category in entries:
        if date.hour or date.minute:
            date_str = date.strftime("%b %d, %-I:%M %p") + " UTC"
        else:
            date_str = date.strftime("%b %d")
        border_color, chip_label, chip_bg, chip_text = CATEGORY_STYLES.get(category, DEFAULT_STYLE)
        chip_html = (
            f'<span style="display: inline-block; font-size: 0.7em; font-weight: 600;'
            f' padding: 1px 8px; border-radius: 9999px; margin-left: 0.5em;'
            f' background: {chip_bg}; color: {chip_text}; vertical-align: middle;'
            f' opacity: 0.85;">{chip_label}</span>'
        )
        desc_html = f'<span style="opacity: 0.75;">{description}</span>' if description else ""
        items.append(
            f'<div style="border-left: 3px solid {border_color}; padding: 0.4em 0 0.4em 1em; margin-bottom: 0.75em;">'
            f'<strong style="opacity: 0.5; font-size: 0.85em;">{date_str}</strong>{chip_html}<br>'
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
