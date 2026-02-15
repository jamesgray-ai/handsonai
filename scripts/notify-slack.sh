#!/bin/bash
# Post a cookbook changelog update to Slack via incoming webhooks.
#
# Usage:
#   ./scripts/notify-slack.sh "Entry Title" "One-line summary" "https://handsonai.info/blog/2026/02/14/slug/"
#
# Requires environment variables:
#   SLACK_WEBHOOK_1  — Incoming webhook URL for first workspace
#   SLACK_WEBHOOK_2  — Incoming webhook URL for second workspace
#
# Requires: jq (for safe JSON escaping)

set -euo pipefail

TITLE="${1:?Usage: notify-slack.sh TITLE SUMMARY URL}"
SUMMARY="${2:?Usage: notify-slack.sh TITLE SUMMARY URL}"
URL="${3:?Usage: notify-slack.sh TITLE SUMMARY URL}"

PAYLOAD=$(jq -n \
  --arg title "$TITLE" \
  --arg summary "$SUMMARY" \
  --arg url "$URL" \
  '{blocks: [{type: "section", text: {type: "mrkdwn", text: (":book: *Cookbook Update: <" + $url + "|" + $title + ">*\n" + $summary)}}]}')

post_to_webhook() {
  local webhook_url="$1"
  local name="$2"
  if [ -z "$webhook_url" ]; then
    echo "Skipping ${name} — webhook URL not set"
    return 0
  fi
  curl -s -o /dev/null -w "%{http_code}" -X POST \
    -H "Content-Type: application/json" \
    -d "$PAYLOAD" \
    "$webhook_url"
  echo " — ${name} notified"
}

post_to_webhook "${SLACK_WEBHOOK_1:-}" "Workspace 1"
post_to_webhook "${SLACK_WEBHOOK_2:-}" "Workspace 2"
