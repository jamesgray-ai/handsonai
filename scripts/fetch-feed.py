#!/usr/bin/env python3
"""Fetch curated feed items from Inoreader and write to feed.json."""

import html
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

import requests

BASE_URL = "https://www.inoreader.com/reader/api/0"
MAX_ITEMS_PER_FOLDER = 100
MAX_TOTAL_ITEMS = 100
MAX_AGE_DAYS = 7
EXCERPT_LENGTH = 150

# Output path relative to repo root
OUTPUT_PATH = Path(__file__).resolve().parent.parent / "docs" / "assets" / "data" / "feed.json"


def get_env(name):
    value = os.environ.get(name)
    if not value:
        print(f"Error: {name} environment variable is required", file=sys.stderr)
        sys.exit(1)
    return value


def refresh_access_token(app_id, app_key, refresh_token):
    """Use refresh token to get a fresh access token."""
    resp = requests.post(
        "https://www.inoreader.com/oauth2/token",
        headers={"Content-type": "application/x-www-form-urlencoded"},
        data={
            "client_id": app_id,
            "client_secret": app_key,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        },
    )
    resp.raise_for_status()
    data = resp.json()
    return data["access_token"]


def get_headers(access_token, app_id, app_key):
    return {
        "Authorization": f"Bearer {access_token}",
        "AppId": app_id,
        "AppKey": app_key,
    }


def fetch_folders(headers):
    """Fetch user's folder (label) list, excluding system tags."""
    resp = requests.get(f"{BASE_URL}/tag/list?output=json", headers=headers)
    resp.raise_for_status()
    folders = []
    for tag in resp.json().get("tags", []):
        tag_id = tag["id"]
        if "/label/" in tag_id:
            name = tag_id.split("/label/", 1)[1]
            folders.append({"id": tag_id, "name": name})
    return folders


def strip_html(text):
    """Remove HTML tags and decode entities."""
    text = re.sub(r"<[^>]+>", "", text)
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def fetch_folder_items(headers, folder):
    """Fetch items from a single folder."""
    stream_id = quote(folder["id"], safe="")
    url = f"{BASE_URL}/stream/contents/{stream_id}?n={MAX_ITEMS_PER_FOLDER}&output=json"
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()

    items = []
    for item in resp.json().get("items", []):
        canonical = item.get("canonical", [{}])
        article_url = canonical[0].get("href", "") if canonical else ""
        if not article_url:
            continue

        summary_html = item.get("summary", {}).get("content", "")
        excerpt = strip_html(summary_html)[:EXCERPT_LENGTH]
        if len(strip_html(summary_html)) > EXCERPT_LENGTH:
            excerpt += "..."

        published = item.get("published", 0)

        items.append({
            "title": item.get("title", "Untitled"),
            "url": article_url,
            "source": item.get("origin", {}).get("title", "Unknown"),
            "published": datetime.fromtimestamp(published, tz=timezone.utc).isoformat(),
            "category": folder["name"],
            "excerpt": excerpt,
        })

    return items


def main():
    app_id = get_env("INOREADER_APP_ID")
    app_key = get_env("INOREADER_APP_KEY")
    refresh_token = get_env("INOREADER_AUTH_TOKEN")

    print("Refreshing access token...")
    access_token = refresh_access_token(app_id, app_key, refresh_token)

    headers = get_headers(access_token, app_id, app_key)

    print("Fetching folders...")
    folders = fetch_folders(headers)
    print(f"Found {len(folders)} folders: {', '.join(f['name'] for f in folders)}")

    all_items = []
    seen_urls = set()

    for folder in folders:
        print(f"Fetching items from '{folder['name']}'...")
        items = fetch_folder_items(headers, folder)
        new_count = 0
        for item in items:
            if item["url"] not in seen_urls:
                seen_urls.add(item["url"])
                all_items.append(item)
                new_count += 1
        print(f"  {len(items)} items fetched, {new_count} new")

    # Filter to last N days
    cutoff = datetime.now(tz=timezone.utc).timestamp() - (MAX_AGE_DAYS * 86400)
    all_items = [
        item for item in all_items
        if datetime.fromisoformat(item["published"]).timestamp() > cutoff
    ]

    # Sort newest first
    all_items.sort(key=lambda x: x["published"], reverse=True)

    # Trim to max
    all_items = all_items[:MAX_TOTAL_ITEMS]

    # Build output
    categories = sorted(set(item["category"] for item in all_items))
    feed_data = {
        "updated": datetime.now(tz=timezone.utc).isoformat(),
        "categories": categories,
        "items": all_items,
    }

    # Ensure output directory exists
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(feed_data, indent=2), encoding="utf-8")
    print(f"\nWrote {len(all_items)} items across {len(categories)} categories to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
