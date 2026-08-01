#!/usr/bin/env bash
#
# check-plugin-sync.sh — every plugin exists in more than one place, and the copies
# must stay identical or students quietly receive something other than what we maintain.
#
# Two modes, selected by the plugin name:
#
#   bash scripts/check-plugin-sync.sh                       # multi-agent-example (default)
#   bash scripts/check-plugin-sync.sh multi-agent-example   # same thing
#
#     The pipeline is mirrored inside THIS repo — .claude/{agents,skills,commands,hooks}/
#     and scripts/ (what runs here) vs plugins/multi-agent-example/ (what students
#     install). Compares those two trees.
#
#   bash scripts/check-plugin-sync.sh handsonai             # or any other plugin name
#
#     Compares the canonical plugins/<name>/ against its distributed copy in the
#     jamesgray-ai/handsonai-plugins clone (default ~/Code/jamesgray/handsonai-plugins,
#     override with HANDSONAI_PLUGINS_DIR). This is the drift that bit issue #225:
#     canonical moved six commits while the distributed copy — the one students
#     install — sat stale, missing a reference file entirely.
#
# Exit codes: 0 in sync (or skipped — distributed clone absent / plugin never synced),
#             1 drift, 2 usage error.

set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DIST_REPO="${HANDSONAI_PLUGINS_DIR:-$HOME/Code/jamesgray/handsonai-plugins}"
NAME="${1:-multi-agent-example}"
DRIFT=0
CHECKED=0

if [ ! -d "$ROOT/plugins/$NAME" ]; then
  echo "Error: no such plugin 'plugins/$NAME' in this repo." >&2
  echo "Usage: $0 [plugin-name]   (default: multi-agent-example)" >&2
  exit 2
fi

# ---------------------------------------------------------------------------
# Distributed mode: plugins/<name>/ vs the handsonai-plugins clone.
# ---------------------------------------------------------------------------
if [ "$NAME" != "multi-agent-example" ]; then
  command -v jq >/dev/null || { echo "Error: jq is required (brew install jq)" >&2; exit 2; }

  CANON="$ROOT/plugins/$NAME"
  DIST="$DIST_REPO/plugins/$NAME"

  if [ ! -d "$DIST_REPO" ]; then
    echo "SKIPPED: distributed repo not found at $DIST_REPO."
    echo "Clone jamesgray-ai/handsonai-plugins (or set HANDSONAI_PLUGINS_DIR) to enable this check."
    exit 0
  fi
  if [ ! -d "$DIST" ]; then
    echo "SKIPPED: '$NAME' has never been synced to $DIST_REPO — nothing to compare."
    echo "(sync-plugins.sh creates it on first sync.)"
    exit 0
  fi

  echo "$NAME: canonical (plugins/$NAME) vs distributed ($DIST_REPO)"

  list_files() {
    (cd "$1" && find . -type f \
       -not -path '*/node_modules/*' -not -name '.DS_Store' | sed 's|^\./||')
  }

  # Union of both trees, so a file present in only one of them is reported in
  # both directions — enumerating a single side is how the last rewrite of this
  # check managed to pass while proving nothing.
  while IFS= read -r rel; do
    CHECKED=$((CHECKED + 1))
    a="$CANON/$rel" b="$DIST/$rel"
    if [ ! -f "$b" ]; then
      echo "  MISSING in distributed: $rel"
      DRIFT=$((DRIFT + 1))
      continue
    fi
    if [ ! -f "$a" ]; then
      echo "  MISSING in canonical:   $rel  (sync-plugins.sh will DELETE it from the distributed copy)"
      DRIFT=$((DRIFT + 1))
      continue
    fi
    if [ "$rel" = ".claude-plugin/plugin.json" ]; then
      # The version is bumped in one place first during a release cycle, so it
      # legitimately differs; only the rest of the manifest counts as drift.
      if ! diff -q <(jq -S 'del(.version)' "$a") <(jq -S 'del(.version)' "$b") > /dev/null; then
        echo "  DRIFTED:                $rel  (beyond the version field)"
        DRIFT=$((DRIFT + 1))
      else
        va="$(jq -r '.version' "$a")" vb="$(jq -r '.version' "$b")"
        if [ "$va" != "$vb" ]; then
          echo "  NOTE: plugin.json version differs (canonical $va vs distributed $vb) — expected mid-release, not counted as drift"
        fi
      fi
      continue
    fi
    if ! diff -q "$a" "$b" > /dev/null; then
      echo "  DRIFTED:                $rel"
      DRIFT=$((DRIFT + 1))
    fi
  done < <({ list_files "$CANON"; list_files "$DIST"; } | sort -u)

  echo
  if [ "$DRIFT" -eq 0 ]; then
    echo "$CHECKED files checked — all in sync"
  else
    echo "$CHECKED files checked — $DRIFT out of sync"
    echo
    echo "plugins/$NAME/ is canonical. Run ./scripts/sync-plugins.sh $NAME patch|minor|major to reconcile."
  fi
  exit $([ "$DRIFT" -eq 0 ] && echo 0 || echo 1)
fi

# ---------------------------------------------------------------------------
# Mirror mode: the multi-agent-example pipeline inside this repo.
# ---------------------------------------------------------------------------
PLUGIN="$ROOT/plugins/multi-agent-example"

compare() {
  # $1 = repo-relative path, $2 = plugin-relative path
  local a="$ROOT/$1" b="$PLUGIN/$2"
  CHECKED=$((CHECKED + 1))
  if [ ! -f "$a" ]; then
    echo "  MISSING in repo:   $1"; DRIFT=$((DRIFT + 1)); return
  fi
  if [ ! -f "$b" ]; then
    echo "  MISSING in plugin: $2"; DRIFT=$((DRIFT + 1)); return
  fi
  if ! diff -q "$a" "$b" > /dev/null; then
    echo "  DRIFTED:           $1  vs  plugins/multi-agent-example/$2"
    DRIFT=$((DRIFT + 1))
  fi
}

# Where a plugin-relative path lives in this repo. `scripts/` maps to the repo's own
# scripts/ directory; everything else sits under .claude/.
repo_path_for() {
  case "$1" in
    scripts/*) echo "$1" ;;
    *)         echo ".claude/$1" ;;
  esac
}

echo "multi-agent-example: repo vs plugin"

# Enumerate from the plugin tree rather than a hardcoded list.
#
# A literal list only guards the files someone remembered to add to it. Adding a fifth
# agent, a second skill, or a new script to the plugin without editing this script would
# print "all in sync" while the two trees genuinely differed — and sync-plugins.sh treats
# a pass here as permission to ship.
#
# .claude-plugin/ is excluded deliberately: plugin.json exists only in the plugin, and
# node_modules/ is build output, not source.
while IFS= read -r rel; do
  # hooks/hooks.json has no repo twin ON PURPOSE. A plugin registers its hooks through
  # hooks/hooks.json; this repo registers the same two scripts through .claude/settings.json.
  # Different files, different formats, same wiring — check-pipeline-consistency.sh is what
  # verifies the two registrations agree.
  [ "$rel" = "hooks/hooks.json" ] && continue
  compare "$(repo_path_for "$rel")" "$rel"
done < <(cd "$PLUGIN" && find agents commands hooks scripts skills -type f \
           -not -path '*/node_modules/*' -not -name '.DS_Store' 2>/dev/null | sort)

# And the other direction, for the directories this pipeline owns outright. A repo-side
# file with no plugin counterpart is drift too — the demo would use something students
# never receive. Limited to exclusive paths: .claude/agents/ and scripts/ are shared with
# unrelated repo content, so they cannot be swept this way.
while IFS= read -r path; do
  rel="${path#$ROOT/.claude/}"
  [ -f "$PLUGIN/$rel" ] || { echo "  MISSING in plugin: $rel (exists in repo)"; DRIFT=$((DRIFT + 1)); }
done < <(find "$ROOT/.claude/hooks" "$ROOT/.claude/skills/editing-hbr-articles" -type f \
           -not -name '.DS_Store' 2>/dev/null | sort)

while IFS= read -r path; do
  name="$(basename "$path")"
  [ -f "$PLUGIN/commands/$name" ] || { echo "  MISSING in plugin: commands/$name (exists in repo)"; DRIFT=$((DRIFT + 1)); }
done < <(find "$ROOT/.claude/commands" -type f -name 'hbr-*' 2>/dev/null | sort)

echo
if [ "$DRIFT" -eq 0 ]; then
  echo "$CHECKED files checked — all in sync"
else
  echo "$CHECKED files checked — $DRIFT out of sync"
  echo
  echo "plugins/multi-agent-example/ is canonical. Copy from there to .claude/, then re-run."
fi

[ "$DRIFT" -eq 0 ]
