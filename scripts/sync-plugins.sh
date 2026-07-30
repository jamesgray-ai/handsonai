#!/usr/bin/env bash
# Sync a plugin from plugins/<name>/ → ~/Code/jamesgray/handsonai-plugins/, bumping versions.
#
# Usage: ./scripts/sync-plugins.sh [plugin] patch|minor|major
#
#   ./scripts/sync-plugins.sh handsonai patch
#   ./scripts/sync-plugins.sh multi-agent-example minor
#   ./scripts/sync-plugins.sh patch                  # plugin defaults to handsonai
#
# What this does:
#   1. Bumps version in plugins/<plugin>/.claude-plugin/plugin.json (semver).
#   2. Rsyncs plugins/<plugin>/ → handsonai-plugins/plugins/<plugin>/ (--delete).
#   3. Updates that plugin's entry in handsonai-plugins/.claude-plugin/marketplace.json,
#      adding the entry if it does not exist yet, and patch-bumps the marketplace's own
#      top-level version so Cowork sees a change.
#
# What this does NOT do:
#   - Commit or push anywhere. You drive both pushes deliberately so the
#     "push handsonai-plugins last" Cowork rule stays intact.

set -euo pipefail

# Accept either "<plugin> <bump>" or just "<bump>" (plugin defaults to handsonai).
case "${1:-}" in
  patch|minor|major)
    PLUGIN="handsonai"
    BUMP="$1"
    ;;
  '')
    echo "Usage: $0 [plugin] patch|minor|major" >&2
    exit 1
    ;;
  *)
    PLUGIN="$1"
    BUMP="${2:-}"
    ;;
esac

case "$BUMP" in
  patch|minor|major) ;;
  *)
    echo "Usage: $0 [plugin] patch|minor|major" >&2
    exit 1
    ;;
esac

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC_DIR="$REPO_ROOT/plugins/$PLUGIN"
PLUGIN_JSON="$SRC_DIR/.claude-plugin/plugin.json"

DEST_REPO="$HOME/Code/jamesgray/handsonai-plugins"
DEST_DIR="$DEST_REPO/plugins/$PLUGIN"
MARKETPLACE_JSON="$DEST_REPO/.claude-plugin/marketplace.json"

# Pre-flight
command -v jq >/dev/null || { echo "Error: jq is required (brew install jq)" >&2; exit 1; }
[ -d "$SRC_DIR" ] || { echo "Error: $SRC_DIR not found" >&2; exit 1; }
[ -f "$PLUGIN_JSON" ] || { echo "Error: $PLUGIN_JSON not found" >&2; exit 1; }
[ -d "$DEST_REPO" ] || { echo "Error: $DEST_REPO not found — clone handsonai-plugins first" >&2; exit 1; }
[ -f "$MARKETPLACE_JSON" ] || { echo "Error: $MARKETPLACE_JSON not found" >&2; exit 1; }

# The multi-agent-example pipeline is mirrored under .claude/ so it runs in this repo.
# Refuse to ship a plugin whose copies have drifted from what we demo.
if [ "$PLUGIN" = "multi-agent-example" ] && [ -x "$REPO_ROOT/scripts/check-plugin-sync.sh" ]; then
  if ! bash "$REPO_ROOT/scripts/check-plugin-sync.sh"; then
    echo >&2
    echo "Error: repo and plugin copies have drifted. Reconcile them before syncing." >&2
    exit 1
  fi
fi

# Compute new version
CURRENT="$(jq -r .version "$PLUGIN_JSON")"
IFS='.' read -r MAJOR MINOR PATCH <<< "$CURRENT"
case "$BUMP" in
  patch) PATCH=$((PATCH + 1)) ;;
  minor) MINOR=$((MINOR + 1)); PATCH=0 ;;
  major) MAJOR=$((MAJOR + 1)); MINOR=0; PATCH=0 ;;
esac
NEW="${MAJOR}.${MINOR}.${PATCH}"

echo "Syncing plugin '$PLUGIN': ${CURRENT} → ${NEW} (${BUMP})"

# 1. Update plugin.json here
tmp="$(mktemp)"
jq --arg v "$NEW" '.version = $v' "$PLUGIN_JSON" > "$tmp" && mv "$tmp" "$PLUGIN_JSON"

# 2. Rsync to handsonai-plugins (carries bumped plugin.json with it)
mkdir -p "$DEST_DIR"
rsync -av --delete "$SRC_DIR/" "$DEST_DIR/"

# 3. Update this plugin's marketplace entry, adding it if absent, and bump the
#    marketplace's own version so Cowork detects the change.
DESCRIPTION="$(jq -r '.description' "$PLUGIN_JSON")"
MKT_CURRENT="$(jq -r .version "$MARKETPLACE_JSON")"
IFS='.' read -r MK_MAJ MK_MIN MK_PAT <<< "$MKT_CURRENT"
MKT_NEW="${MK_MAJ}.${MK_MIN}.$((MK_PAT + 1))"

tmp="$(mktemp)"
jq --arg name "$PLUGIN" \
   --arg v "$NEW" \
   --arg mv "$MKT_NEW" \
   --arg desc "$DESCRIPTION" \
   --arg src "./plugins/$PLUGIN" '
     .version = $mv
     | if ([.plugins[] | select(.name == $name)] | length) > 0
       then .plugins = [ .plugins[] |
              if .name == $name
              then .version = $v | .description = $desc | .source = $src
              else . end ]
       else .plugins += [{name: $name, source: $src, description: $desc, version: $v}]
       end
   ' "$MARKETPLACE_JSON" > "$tmp" && mv "$tmp" "$MARKETPLACE_JSON"

echo "marketplace.json: ${MKT_CURRENT} → ${MKT_NEW}, plugin '$PLUGIN' at ${NEW}"

cat <<EOF

Synced. Plugin '${PLUGIN}' is now v${NEW}.

Next steps (in order — do not push handsonai-plugins until last):
  1. Commit and push this repo (handsonai).
  2. cd "$DEST_REPO"
  3. If skills changed: ./scripts/build-skill-zips.sh
  4. gh release create v${MKT_NEW} dist/*.zip --title "v${MKT_NEW}" --notes "…"
  5. git add -A && git commit -m "release v${MKT_NEW}" && git push
EOF
