#!/usr/bin/env python3
"""Generate course syllabus pages from Notion databases.

Queries the Notion API to fetch the full course hierarchy
(Course → Week → Session → Module → Lesson) and writes Markdown
syllabus files for each published course.

For local preview:
    NOTION_TOKEN=secret_xxx python scripts/generate_syllabi.py && mkdocs serve

Set NOTION_TOKEN to your Notion integration token.  All course databases
must be shared with the integration.
"""

import os
import re
import sys
from pathlib import Path

try:
    from notion_client import Client
except ImportError:
    print(
        "Error: notion-client package required. "
        "Install with: pip install 'notion-client>=2.0'"
    )
    sys.exit(1)

# ---------------------------------------------------------------------------
# Database IDs
# ---------------------------------------------------------------------------

COURSES_DB = "b362adda-e8cc-4639-b042-6b7a6739f336"
COURSE_WEEKS_DB = "2e5edcfd-b924-8071-b2f5-000bcbfc3c32"
SESSIONS_DB = "6170ce99-97d1-4285-967d-dffd2162d4b7"
MODULES_DB = "24aedcfd-b924-8096-bc04-000b547b69f4"
LESSONS_DB = "c5865fa3-d44f-4b44-b0fd-a8ff83cb7177"

# Course name → output directory slug and Maven enrollment URL
COURSE_CONFIG = {
    "Claude and Claude Code for Builders": {
        "slug": "builders",
        "url": "https://maven.com/james-gray/claude",
    },
    "Hands-on Agentic AI for Leaders": {
        "slug": "leaders",
        "url": "https://maven.com/james-gray/hands-on-ai-for-leaders",
    },
}

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "docs" / "courses"

LESSON_TYPE_ICONS = {
    "Live": ":material-video-outline:",
    "Self-Paced": ":material-book-open-variant:",
    "Live-Prerequisite": ":material-clipboard-check-outline:",
}


# ---------------------------------------------------------------------------
# Text helpers
# ---------------------------------------------------------------------------


def slugify(text):
    """Generate URL-safe slug from text."""
    slug = text.lower().strip()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[\s]+", "-", slug)
    return slug


# ---------------------------------------------------------------------------
# Notion property helpers
# ---------------------------------------------------------------------------


def rich_text(prop):
    """Extract plain text from a rich_text or title property value."""
    if not prop:
        return ""
    items = prop.get("title") or prop.get("rich_text") or []
    return "".join(item.get("plain_text", "") for item in items)


def number_val(prop):
    """Extract number value."""
    if not prop:
        return None
    return prop.get("number")


def select_val(prop):
    """Extract select value name."""
    if not prop:
        return None
    s = prop.get("select")
    return s["name"] if s else None


def relation_ids(prop):
    """Extract page IDs from a relation property."""
    if not prop:
        return []
    return [r["id"] for r in prop.get("relation", [])]


def url_val(prop):
    """Extract URL from a url property."""
    if not prop:
        return None
    return prop.get("url")


# ---------------------------------------------------------------------------
# Notion query helpers
# ---------------------------------------------------------------------------


def query_all(notion, data_source_id, filter_obj=None):
    """Query all pages from a data source, handling pagination."""
    pages = []
    kwargs = {"data_source_id": data_source_id, "page_size": 100}
    if filter_obj:
        kwargs["filter"] = filter_obj
    while True:
        response = notion.data_sources.query(**kwargs)
        pages.extend(response["results"])
        if not response.get("has_more"):
            break
        kwargs["start_cursor"] = response["next_cursor"]
    return pages


def build_url_lookup_from_pages(notion, page_ids, label):
    """Build a page_id → URL lookup by fetching individual pages.

    The Slides/Videos databases may not be shared with the integration,
    but individual pages within them are accessible.  Each page has a
    ``_external_object_url`` property containing the Google Slides/Drive URL.
    """
    lookup = {}
    for pid in page_ids:
        try:
            page = notion.pages.retrieve(page_id=pid)
            url = url_val(page["properties"].get("_external_object_url", {}))
            if url:
                lookup[pid] = url
        except Exception:
            pass  # page not accessible — skip silently
    if lookup:
        print(f"  Resolved {len(lookup)}/{len(page_ids)} {label} URL(s)")
    else:
        print(f"  No {label} URLs resolved ({len(page_ids)} page(s) checked)")
    return lookup


# ---------------------------------------------------------------------------
# Data fetching
# ---------------------------------------------------------------------------


def fetch_courses(notion):
    """Fetch published courses."""
    pages = query_all(
        notion,
        COURSES_DB,
        filter_obj={"property": "Status", "select": {"equals": "Published"}},
    )
    courses = {}
    for page in pages:
        props = page["properties"]
        name = rich_text(props.get("Course Name", {}))
        if name not in COURSE_CONFIG:
            continue
        courses[page["id"]] = {
            "name": name,
            "description": rich_text(props.get("Description", {})),
            "url": url_val(props.get("Course URL", {}))
            or COURSE_CONFIG[name]["url"],
            "slug": COURSE_CONFIG[name]["slug"],
        }
    return courses


def fetch_weeks(notion):
    """Fetch all course weeks."""
    pages = query_all(notion, COURSE_WEEKS_DB)
    weeks = {}
    for page in pages:
        props = page["properties"]
        weeks[page["id"]] = {
            "name": rich_text(props.get("Name", {})),
            "outcome": rich_text(props.get("Week Outcome", {})),
            "course_ids": relation_ids(props.get("Course", {})),
        }
    return weeks


def fetch_sessions(notion):
    """Fetch all sessions."""
    pages = query_all(notion, SESSIONS_DB)
    sessions = {}
    for page in pages:
        props = page["properties"]
        sessions[page["id"]] = {
            "name": rich_text(props.get("Session Name", {})),
            "number": number_val(props.get("Session #", {})),
            "description": rich_text(props.get("Description", {})),
            "overview": rich_text(props.get("Session Overview", {})),
            "outcomes": rich_text(props.get("Session Outcomes", {})),
            "prerequisites": rich_text(props.get("Prerequisites", {})),
            "duration": number_val(props.get("Target Duration (min)", {})),
            "week_ids": relation_ids(props.get("Week #", {})),
            "module_ids": relation_ids(props.get("Module", {})),
            "course_ids": relation_ids(props.get("Course", {})),
        }
    return sessions


def fetch_modules(notion):
    """Fetch all modules."""
    pages = query_all(notion, MODULES_DB)
    modules = {}
    for page in pages:
        props = page["properties"]
        modules[page["id"]] = {
            "name": rich_text(props.get("Module Name", {})),
            "description": rich_text(props.get("Module Description", {})),
            "number": number_val(props.get("Module # in Week", {})),
            "week_number": number_val(props.get("Week #", {})),
            "status": select_val(props.get("Status", {})),
            "lesson_ids": relation_ids(props.get("Lessons", {})),
            "session_ids": relation_ids(props.get("Sessions", {})),
            "course_ids": relation_ids(props.get("Course", {})),
        }
    return modules


def fetch_lessons(notion):
    """Fetch all lessons."""
    pages = query_all(notion, LESSONS_DB)
    lessons = {}
    for page in pages:
        props = page["properties"]
        lessons[page["id"]] = {
            "name": rich_text(props.get("Lesson Name", {})),
            "number": number_val(props.get("Lesson Number", {})),
            "description": rich_text(props.get("Lesson Description", {})),
            "type": select_val(props.get("Lesson Type", {})),
            "duration": number_val(props.get("Duration (min)", {})),
            "objectives": rich_text(props.get("Lesson Objectives", {})),
            "module_ids": relation_ids(props.get("Module", {})),
            "slide_ids": relation_ids(props.get("Lesson Slides", {})),
            "video_ids": relation_ids(props.get("Video", {})),
        }
    return lessons


# ---------------------------------------------------------------------------
# Assembly
# ---------------------------------------------------------------------------


def assemble_course(
    course_id, weeks, sessions, modules, lessons, slides_lookup, videos_lookup
):
    """Assemble the full hierarchy for a single course."""
    # Find weeks for this course
    course_weeks = [
        (wid, w)
        for wid, w in weeks.items()
        if course_id in w["course_ids"]
    ]
    course_weeks.sort(key=lambda w: w[1]["name"])

    assembled_weeks = []
    for wid, week in course_weeks:
        # Find sessions for this week that belong to this course
        week_sessions = [
            (sid, s)
            for sid, s in sessions.items()
            if wid in s["week_ids"] and course_id in s["course_ids"]
        ]
        week_sessions.sort(key=lambda s: s[1]["number"] or 0)

        assembled_sessions = []
        for sid, session in week_sessions:
            # Find modules for this session
            session_modules = [
                (mid, modules[mid])
                for mid in session["module_ids"]
                if mid in modules
            ]
            session_modules.sort(key=lambda m: m[1]["number"] or 0)

            assembled_modules = []
            for mid, module in session_modules:
                # Find lessons for this module
                module_lessons = []
                for lid in module["lesson_ids"]:
                    if lid not in lessons:
                        continue
                    lesson = lessons[lid]
                    slide_urls = [
                        slides_lookup[s]
                        for s in lesson["slide_ids"]
                        if s in slides_lookup
                    ]
                    video_urls = [
                        videos_lookup[v]
                        for v in lesson["video_ids"]
                        if v in videos_lookup
                    ]
                    module_lessons.append(
                        {
                            **lesson,
                            "slide_url": slide_urls[0] if slide_urls else None,
                            "video_url": video_urls[0] if video_urls else None,
                        }
                    )
                module_lessons.sort(key=lambda l: l["number"] or 0)

                assembled_modules.append({**module, "lessons": module_lessons})

            assembled_sessions.append({**session, "modules": assembled_modules})

        assembled_weeks.append({**week, "sessions": assembled_sessions})

    return assembled_weeks


# ---------------------------------------------------------------------------
# Markdown generation
# ---------------------------------------------------------------------------


def _split_list_items(text):
    """Split text into individual list items.

    Handles newline-separated items (with or without bullet/number prefixes)
    and single-line text with inline numbering like '1. First 2. Second'.
    Returns a list of clean text strings with prefixes stripped.
    """
    raw_lines = text.strip().splitlines()
    items = []
    for line in raw_lines:
        stripped = line.strip()
        if not stripped:
            continue
        # Strip leading bullet/number prefix
        cleaned = re.sub(r"^(\d+\.\s*|[-•*]\s*)", "", stripped)
        if cleaned:
            items.append(cleaned)

    # If we got only one item but it contains inline numbering, split on that
    if len(items) == 1 and re.search(r"\d+\.\s", items[0]):
        parts = re.split(r"\s*\d+\.\s+", items[0])
        items = [p.strip() for p in parts if p.strip()]

    return items


def format_resources(lesson):
    """Format resource links for a lesson."""
    parts = []
    if lesson.get("slide_url"):
        parts.append(
            f'[:material-presentation: Slides]({lesson["slide_url"]}){{:target="_blank"}}'
        )
    if lesson.get("video_url"):
        parts.append(
            f'[:material-video: Video]({lesson["video_url"]}){{:target="_blank"}}'
        )
    return " · ".join(parts)


def format_lesson_type(lesson_type):
    """Format lesson type with Material icon."""
    icon = LESSON_TYPE_ICONS.get(lesson_type, "")
    return f"{icon} {lesson_type}" if icon else (lesson_type or "")


def generate_lesson_page(lesson, course, session_name, module_name):
    """Generate Markdown content for a single lesson detail page."""
    lesson_name = lesson.get("name", "Untitled Lesson")
    course_name = course["name"]
    description = lesson.get("description", "")
    meta_desc = description[:155] if description else lesson_name

    # Escape double quotes in frontmatter values
    safe_title = f"{lesson_name} — {course_name}".replace('"', '\\"')
    safe_desc = meta_desc.replace('"', '\\"')

    lines = [
        "---",
        f'title: "{safe_title}"',
        f'description: "{safe_desc}"',
        "---",
        "",
        f"# {lesson_name}",
        "",
        "| | |",
        "|---|---|",
        f'| **Course** | [{course_name}](../index.md) |',
        f"| **Session** | {session_name} |",
        f"| **Module** | {module_name} |",
        f"| **Type** | {format_lesson_type(lesson.get('type'))} |",
    ]

    if lesson.get("duration"):
        lines.append(f'| **Duration** | {int(lesson["duration"])} min |')

    lines.append("")

    if description:
        lines.append(description)
        lines.append("")

    objectives = lesson.get("objectives", "")
    if objectives:
        lines.append("## Objectives")
        lines.append("")
        for item in _split_list_items(objectives):
            lines.append(f"- {item}")
        lines.append("")

    resources = format_resources(lesson)
    if resources:
        lines.append("## Resources")
        lines.append("")
        # Split resources and put each on its own line
        for part in resources.split(" · "):
            lines.append(f"- {part}")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append(
        "[Back to syllabus :material-arrow-left:](../syllabus.md){ .md-button }"
    )
    lines.append("")

    return "\n".join(lines)


def write_lesson_pages(course, assembled_weeks):
    """Write individual lesson pages and return a lesson-ID → slug mapping."""
    slug_map = {}
    used_slugs = set()
    lessons_dir = OUTPUT_DIR / course["slug"] / "lessons"
    lessons_dir.mkdir(parents=True, exist_ok=True)

    page_count = 0
    for week in assembled_weeks:
        for session in week.get("sessions", []):
            session_num = (
                int(session["number"]) if session.get("number") else ""
            )
            session_label = re.sub(
                r"^Session\s+\d+:\s*", "", session["name"]
            )
            session_name = f"Session {session_num}: {session_label}"

            for module in session.get("modules", []):
                module_name = module.get("name", "")

                for lesson in module.get("lessons", []):
                    name = lesson.get("name", "")
                    if not name:
                        continue

                    # Generate unique slug
                    base_slug = slugify(name)
                    slug = base_slug
                    counter = 2
                    while slug in used_slugs:
                        slug = f"{base_slug}-{counter}"
                        counter += 1
                    used_slugs.add(slug)

                    # Track by lesson name for lookup during syllabus generation
                    # Use a composite key since lessons don't carry IDs through assembly
                    slug_map[(name, module_name)] = slug

                    content = generate_lesson_page(
                        lesson, course, session_name, module_name
                    )
                    (lessons_dir / f"{slug}.md").write_text(content)
                    page_count += 1

    print(f"  Wrote {page_count} lesson page(s) to {lessons_dir}")
    return slug_map


def generate_markdown(course, assembled_weeks, lesson_slug_map=None):
    """Generate the full syllabus Markdown for a course."""
    lesson_slug_map = lesson_slug_map or {}
    lines = [
        "---",
        f'title: "Course Syllabus — {course["name"]}"',
        'description: "Full syllabus including weekly sessions, modules, lessons, and resources."',
        "---",
        "",
        "# Course Syllabus",
        "",
        f'Full syllabus for **{course["name"]}**.',
        "",
        f'[Enroll on Maven :material-arrow-right:]({course["url"]}){{ .md-button .md-button--primary }}',
        "",
    ]

    if not assembled_weeks:
        lines.append("Syllabus coming soon — check back shortly!")
        lines.append("")
        return "\n".join(lines)

    for week in assembled_weeks:
        lines.append("---")
        lines.append("")
        lines.append(f'## {week["name"]}')
        lines.append("")
        if week.get("outcome"):
            items = _split_list_items(week["outcome"])
            if len(items) > 1:
                for item in items:
                    lines.append(f"- {item}")
            else:
                lines.append(f'*{week["outcome"]}*')
            lines.append("")

        for session in week.get("sessions", []):
            session_num = (
                int(session["number"]) if session.get("number") else ""
            )
            # Strip "Session N: " prefix from name if present to avoid duplication
            session_name = re.sub(
                r"^Session\s+\d+:\s*", "", session["name"]
            )
            lines.append(f"### Session {session_num}: {session_name}")
            lines.append("")

            desc = session.get("overview") or session.get("description") or ""
            if desc:
                lines.append(f"*{desc}*")
                lines.append("")

            if session.get("outcomes"):
                lines.append("**Outcomes:**")
                lines.append("")
                for item in _split_list_items(session["outcomes"]):
                    lines.append(f"- {item}")
                lines.append("")

            if session.get("prerequisites"):
                lines.append(f'**Prerequisites:** {session["prerequisites"]}')
                lines.append("")

            for module in session.get("modules", []):
                mod_num = (
                    int(module["number"]) if module.get("number") else ""
                )
                lines.append(
                    f'???+ note "Module {mod_num}: {module["name"]}"'
                )
                lines.append("")

                if module.get("description"):
                    lines.append(f'    *{module["description"]}*')
                    lines.append("")

                if module.get("lessons"):
                    lines.append(
                        "    | # | Lesson | Type | Duration | Resources |"
                    )
                    lines.append(
                        "    |---|--------|------|----------|-----------|"
                    )
                    for lesson in module["lessons"]:
                        num = (
                            int(lesson["number"])
                            if lesson.get("number")
                            else ""
                        )
                        name = lesson.get("name", "")
                        lesson_slug = lesson_slug_map.get(
                            (name, module.get("name", ""))
                        )
                        if lesson_slug:
                            name = f"[{name}](lessons/{lesson_slug}.md)"
                        ltype = format_lesson_type(lesson.get("type"))
                        dur = (
                            f'{int(lesson["duration"])} min'
                            if lesson.get("duration")
                            else ""
                        )
                        resources = format_resources(lesson)
                        lines.append(
                            f"    | {num} | {name} | {ltype} | {dur} | {resources} |"
                        )
                    lines.append("")

                    # Inline lesson details as collapsible blocks
                    for lesson in module["lessons"]:
                        desc = lesson.get("description", "")
                        objectives = lesson.get("objectives", "")
                        if not desc and not objectives:
                            continue

                        lesson_name = lesson.get("name", "")
                        lines.append(
                            f'    ??? info "{lesson_name}"'
                        )
                        lines.append("")

                        if desc:
                            lines.append(f"        {desc}")
                            lines.append("")

                        if objectives:
                            lines.append("        **Objectives:**")
                            lines.append("")
                            for item in _split_list_items(objectives):
                                lines.append(f"        - {item}")
                            lines.append("")

    lines.append("---")
    lines.append("")
    lines.append(
        "*This syllabus is generated from the course database "
        "and may be updated between cohorts.*"
    )
    lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

PLACEHOLDER = """\
---
title: "Course Syllabus"
description: "Syllabus coming soon."
---

# Course Syllabus

Syllabus coming soon — check back shortly!
"""


def main():
    token = os.environ.get("NOTION_TOKEN")
    if not token:
        print("Error: NOTION_TOKEN environment variable is required.")
        print("Get your token at https://www.notion.so/my-integrations")
        sys.exit(1)

    notion = Client(auth=token)

    print("Fetching courses...")
    courses = fetch_courses(notion)
    if not courses:
        print("No published courses found. Writing placeholder pages.")
        for config in COURSE_CONFIG.values():
            output = OUTPUT_DIR / config["slug"] / "syllabus.md"
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(PLACEHOLDER)
            print(f"  Wrote {output}")
        return

    print(
        f"  Found {len(courses)} course(s): "
        f"{', '.join(c['name'] for c in courses.values())}"
    )

    print("Fetching course weeks...")
    weeks = fetch_weeks(notion)
    print(f"  Found {len(weeks)} week(s)")

    print("Fetching sessions...")
    sessions = fetch_sessions(notion)
    print(f"  Found {len(sessions)} session(s)")

    print("Fetching modules...")
    modules = fetch_modules(notion)
    print(f"  Found {len(modules)} module(s)")

    print("Fetching lessons...")
    lessons = fetch_lessons(notion)
    print(f"  Found {len(lessons)} lesson(s)")

    # Collect all unique slide/video page IDs from lessons
    all_slide_ids = set()
    all_video_ids = set()
    for lesson in lessons.values():
        all_slide_ids.update(lesson["slide_ids"])
        all_video_ids.update(lesson["video_ids"])

    print("Fetching slide deck URLs...")
    slides_lookup = (
        build_url_lookup_from_pages(notion, all_slide_ids, "Slides")
        if all_slide_ids
        else {}
    )

    print("Fetching video URLs...")
    videos_lookup = (
        build_url_lookup_from_pages(notion, all_video_ids, "Videos")
        if all_video_ids
        else {}
    )

    for course_id, course in courses.items():
        print(f"\nAssembling {course['name']}...")
        assembled = assemble_course(
            course_id,
            weeks,
            sessions,
            modules,
            lessons,
            slides_lookup,
            videos_lookup,
        )

        print("  Generating lesson pages...")
        lesson_slug_map = write_lesson_pages(course, assembled)

        markdown = generate_markdown(course, assembled, lesson_slug_map)

        output = OUTPUT_DIR / course["slug"] / "syllabus.md"
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(markdown)

        total_sessions = sum(len(w.get("sessions", [])) for w in assembled)
        total_modules = sum(
            len(s.get("modules", []))
            for w in assembled
            for s in w.get("sessions", [])
        )
        total_lessons = sum(
            len(m.get("lessons", []))
            for w in assembled
            for s in w.get("sessions", [])
            for m in s.get("modules", [])
        )
        print(
            f"  Wrote {output} "
            f"({len(assembled)} weeks, {total_sessions} sessions, "
            f"{total_modules} modules, {total_lessons} lessons)"
        )

    # Write placeholder for configured courses not found in Notion
    found_slugs = {c["slug"] for c in courses.values()}
    for name, config in COURSE_CONFIG.items():
        if config["slug"] not in found_slugs:
            output = OUTPUT_DIR / config["slug"] / "syllabus.md"
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(PLACEHOLDER)
            print(f"\n  {name} not found — wrote placeholder to {output}")


if __name__ == "__main__":
    main()
