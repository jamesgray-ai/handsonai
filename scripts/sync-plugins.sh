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

DEST_REPO="${HANDSONAI_PLUGINS_DIR:-$HOME/Code/jamesgray/handsonai-plugins}"
DEST_DIR="$DEST_REPO/plugins/$PLUGIN"
MARKETPLACE_JSON="$DEST_REPO/.claude-plugin/marketplace.json"

# Pre-flight
command -v jq >/dev/null || { echo "Error: jq is required (brew install jq)" >&2; exit 1; }
[ -d "$SRC_DIR" ] || { echo "Error: $SRC_DIR not found" >&2; exit 1; }
[ -f "$PLUGIN_JSON" ] || { echo "Error: $PLUGIN_JSON not found" >&2; exit 1; }
[ -d "$DEST_REPO" ] || { echo "Error: $DEST_REPO not found — clone handsonai-plugins first" >&2; exit 1; }
[ -f "$MARKETPLACE_JSON" ] || { echo "Error: $MARKETPLACE_JSON not found" >&2; exit 1; }

# The AI Registry redesign is held together by string agreement across files that never
# import each other (schema copies, enum vocabulary, lint rule lists, banned fields).
# --full also checks the docs migration, so this stays a hard block until Batch E lands —
# intended: it stops a release shipping before the docs and the registry system agree.
./scripts/check-registry-consistency.sh --full || { echo "Error: registry consistency failed" >&2; exit 1; }

# The multi-agent-example pipeline is mirrored under .claude/ so it runs in this repo.
# Refuse to ship a plugin whose copies have drifted from what we demo.
#
# Test with -f, not -x. The script is run below as `bash <path>`, so its executable bit
# is irrelevant to running it — but using -x as the guard means a chmod, a checkout on a
# filesystem that drops the mode bit, or a CI container that normalises permissions
# silently skips the drift check and ships a plugin that has diverged from what we demo.
if [ "$PLUGIN" = "multi-agent-example" ]; then
  if [ ! -f "$REPO_ROOT/scripts/check-plugin-sync.sh" ]; then
    echo "Error: scripts/check-plugin-sync.sh is missing — refusing to ship this plugin unverified." >&2
    exit 1
  fi
  if ! bash "$REPO_ROOT/scripts/check-plugin-sync.sh"; then
    echo >&2
    echo "Error: repo and plugin copies have drifted. Reconcile them before syncing." >&2
    exit 1
  fi
else
  # Every other plugin's second copy is the distributed repo itself, so at sync time
  # drift is usually the release payload — a hard fail here would block every release.
  # What must not happen is shipping (or deleting) it UNNOTICED: show the full report
  # and make a human acknowledge it, interactively or via SYNC_ACK_DRIFT=1.
  if [ ! -f "$REPO_ROOT/scripts/check-plugin-sync.sh" ]; then
    echo "Error: scripts/check-plugin-sync.sh is missing — refusing to ship this plugin unverified." >&2
    exit 1
  fi
  # `|| CHECK_RC=$?` keeps set -e from aborting before the code is inspected.
  CHECK_RC=0
  bash "$REPO_ROOT/scripts/check-plugin-sync.sh" "$PLUGIN" || CHECK_RC=$?
  if [ "$CHECK_RC" -ge 2 ]; then
    echo "Error: drift check could not run (exit $CHECK_RC). Fix that before syncing." >&2
    exit 1
  fi
  if [ "$CHECK_RC" -eq 1 ]; then
    echo
    echo "The drift above is what this sync will overwrite in the distributed copy"
    echo "(and any 'MISSING in canonical' files will be deleted from it)."
    if [ "${SYNC_ACK_DRIFT:-}" = "1" ]; then
      echo "SYNC_ACK_DRIFT=1 — drift acknowledged, proceeding."
    elif [ -t 0 ]; then
      read -r -p "Ship these changes? [y/N] " REPLY
      case "$REPLY" in
        y|Y|yes|YES) ;;
        *) echo "Error: drift not acknowledged — sync aborted." >&2; exit 1 ;;
      esac
    else
      echo "Error: unacknowledged drift and no terminal to confirm on." >&2
      echo "Review the report above, then re-run with SYNC_ACK_DRIFT=1 to ship it." >&2
      exit 1
    fi
  fi
fi

# Compute new version.
#
# Validate before doing arithmetic on it. `jq -r` yields the string "null" for a missing
# .version; `read` then leaves MINOR and PATCH empty, arithmetic treats empty as 0, and
# the result is the literal version string "null..1" — written into plugin.json, rsynced,
# and published to the marketplace, where Cowork compares it against real semver.
CURRENT="$(jq -r '.version // empty' "$PLUGIN_JSON")"
if ! [[ "$CURRENT" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  echo "Error: $PLUGIN_JSON has no usable version (found: '${CURRENT:-<missing>}'). Expected MAJOR.MINOR.PATCH." >&2
  exit 1
fi
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
# Same reasoning as the version check: an absent description would otherwise publish the
# literal string "null" as the plugin's marketplace listing.
DESCRIPTION="$(jq -r '.description // empty' "$PLUGIN_JSON")"
if [ -z "$DESCRIPTION" ]; then
  echo "Error: $PLUGIN_JSON has no description — it would be listed as \"null\" in the marketplace." >&2
  exit 1
fi

MKT_CURRENT="$(jq -r '.version // empty' "$MARKETPLACE_JSON")"
if ! [[ "$MKT_CURRENT" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
  echo "Error: $MARKETPLACE_JSON has no usable version (found: '${MKT_CURRENT:-<missing>}')." >&2
  exit 1
fi
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
