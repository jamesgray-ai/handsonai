#!/usr/bin/env bash
# Sync plugins/handsonai/ → ~/Code/jamesgray/handsonai-plugins/, bumping versions.
#
# Usage: ./scripts/sync-plugins.sh patch|minor|major
#
# What this does:
#   1. Bumps version in plugins/handsonai/.claude-plugin/plugin.json (semver).
#   2. Rsyncs plugins/handsonai/ → handsonai-plugins/plugins/handsonai/ (--delete).
#   3. Bumps both metadata.version and plugins[0].version in handsonai-plugins/.claude-plugin/marketplace.json.
#
# What this does NOT do:
#   - Commit or push anywhere. You drive both pushes deliberately so the
#     "push handsonai-plugins last" Cowork rule stays intact.

set -euo pipefail

BUMP="${1:-}"
case "$BUMP" in
  patch|minor|major) ;;
  *)
    echo "Usage: $0 patch|minor|major" >&2
    exit 1
    ;;
esac

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC_DIR="$REPO_ROOT/plugins/handsonai"
PLUGIN_JSON="$SRC_DIR/.claude-plugin/plugin.json"

DEST_REPO="$HOME/Code/jamesgray/handsonai-plugins"
DEST_DIR="$DEST_REPO/plugins/handsonai"
MARKETPLACE_JSON="$DEST_REPO/.claude-plugin/marketplace.json"

# Pre-flight
command -v jq >/dev/null || { echo "Error: jq is required (brew install jq)" >&2; exit 1; }
[ -f "$PLUGIN_JSON" ] || { echo "Error: $PLUGIN_JSON not found" >&2; exit 1; }
[ -d "$DEST_DIR" ] || { echo "Error: $DEST_DIR not found — clone handsonai-plugins first" >&2; exit 1; }
[ -f "$MARKETPLACE_JSON" ] || { echo "Error: $MARKETPLACE_JSON not found" >&2; exit 1; }

# Compute new version
CURRENT="$(jq -r .version "$PLUGIN_JSON")"
IFS='.' read -r MAJOR MINOR PATCH <<< "$CURRENT"
case "$BUMP" in
  patch) PATCH=$((PATCH + 1)) ;;
  minor) MINOR=$((MINOR + 1)); PATCH=0 ;;
  major) MAJOR=$((MAJOR + 1)); MINOR=0; PATCH=0 ;;
esac
NEW="${MAJOR}.${MINOR}.${PATCH}"

echo "Bumping ${CURRENT} → ${NEW} (${BUMP})"

# 1. Update plugin.json here
tmp="$(mktemp)"
jq --arg v "$NEW" '.version = $v' "$PLUGIN_JSON" > "$tmp" && mv "$tmp" "$PLUGIN_JSON"

# 2. Rsync to handsonai-plugins (carries bumped plugin.json with it)
rsync -av --delete "$SRC_DIR/" "$DEST_DIR/"

# 3. Update both version fields in marketplace.json
tmp="$(mktemp)"
jq --arg v "$NEW" '.metadata.version = $v | .plugins[0].version = $v' "$MARKETPLACE_JSON" > "$tmp" && mv "$tmp" "$MARKETPLACE_JSON"

cat <<EOF

Synced. New version: ${NEW}

Next steps (in order — do not push handsonai-plugins until last):
  1. Commit and push this repo (handsonai).
  2. cd "$DEST_REPO"
  3. If skills changed: ./scripts/build-skill-zips.sh
  4. gh release create v${NEW} dist/*.zip --title "v${NEW}" --notes "…"
  5. git add -A && git commit -m "release v${NEW}" && git push
EOF
