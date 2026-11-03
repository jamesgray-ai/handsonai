#!/usr/bin/env bash
# publish-plugin.sh — copy skills and agents from a source folder into a Claude plugin
# folder and version the release. Needs only Bash and Git: built into macOS, and
# installed on Windows with Git for Windows (run it in Git Bash).
#
# Usage: publish-plugin.sh <command> --plugin-repo <path> [options]
#
#   setup   --source <path> --name <plugin-name> [--description <text>] [--owner <name>]
#           [--skills-dir .claude/skills] [--agents-dir .claude/agents]
#           Saves the settings and creates the plugin's two manifests if they are missing.
#   check   Checks both folders are ready to publish. Exit 2 = something needs attention.
#   copy    Mirrors the source's skills and agents into the plugin, then lists what changed.
#   changes Lists what changed since the last saved release, and the version bump it calls for.
#   bump    <major|minor|patch|first|X.Y.Z>  Sets the new version in both manifests.
#
# Exit codes: 0 ok · 1 usage or error · 2 needs attention · 3 possible secret found.
# Never commits or pushes: the skill does that after the person approves.

set -u

SETTINGS_FILE=".publish-plugin"

die()  { printf 'ERROR: %s\n' "$*" >&2; exit 1; }
note() { printf '%s\n' "$*"; }

cmd="${1:-}"; [ -n "$cmd" ] || die "no command. Use setup, check, copy, changes or bump."
shift

REPO=""; SOURCE=""; NAME=""; DESCRIPTION=""; OWNER=""; SKILLS_DIR=""; AGENTS_DIR=""; BUMP=""
while [ $# -gt 0 ]; do
  case "$1" in
    --plugin-repo) REPO="${2:-}"; shift 2 ;;
    --source)      SOURCE="${2:-}"; shift 2 ;;
    --name)        NAME="${2:-}"; shift 2 ;;
    --description) DESCRIPTION="${2:-}"; shift 2 ;;
    --owner)       OWNER="${2:-}"; shift 2 ;;
    --skills-dir)  SKILLS_DIR="${2:-}"; shift 2 ;;
    --agents-dir)  AGENTS_DIR="${2:-}"; shift 2 ;;
    -*)            die "unknown option $1" ;;
    *)             BUMP="$1"; shift ;;
  esac
done

[ -n "$REPO" ] || REPO="$(pwd)"
[ -d "$REPO" ] || die "plugin folder not found: $REPO"
REPO="$(cd "$REPO" && pwd)"

# ---------- settings ----------
read_setting() { # key -> value (empty if missing)
  [ -f "$REPO/$SETTINGS_FILE" ] || return 0
  sed -n "s/^$1=//p" "$REPO/$SETTINGS_FILE" | head -n 1
}

load_settings() {
  [ -f "$REPO/$SETTINGS_FILE" ] || die "no settings in $REPO. Run setup first."
  SOURCE="$(read_setting source)"; NAME="$(read_setting plugin)"
  SKILLS_DIR="$(read_setting skills_dir)"; AGENTS_DIR="$(read_setting agents_dir)"
  [ -n "$SKILLS_DIR" ] || SKILLS_DIR=".claude/skills"
  [ -n "$AGENTS_DIR" ] || AGENTS_DIR=".claude/agents"
  [ -n "$SOURCE" ] && [ -n "$NAME" ] || die "settings file is missing source or plugin."
  [ -d "$SOURCE" ] || die "source folder not found: $SOURCE"
  PLUGIN_DIR="$REPO/plugins/$NAME"
  PLUGIN_JSON="$PLUGIN_DIR/.claude-plugin/plugin.json"
  MARKET_JSON="$REPO/.claude-plugin/marketplace.json"
}

# ---------- versions ----------
VERSION_RE='"version"[[:space:]]*:[[:space:]]*"[^"]*"'

count_versions() { grep -o "$VERSION_RE" "$1" 2>/dev/null | wc -l | tr -d ' '; }
read_version()   { grep -o "$VERSION_RE" "$1" | head -n 1 | sed 's/.*"\([^"]*\)"$/\1/'; }

write_version() { # file new-version
  local tmp="$1.tmp.$$"
  sed "s/$VERSION_RE/\"version\": \"$2\"/" "$1" > "$tmp" && mv "$tmp" "$1"
}

check_manifest() { # file label
  [ -f "$1" ] || die "$2 not found: $1"
  local n; n="$(count_versions "$1")"
  [ "$n" = "1" ] || die "$2 must hold exactly one \"version\" field (found $n): $1. Edit it by hand."
}

next_version() { # current bump
  local cur="$1" b="$2" major minor patch
  case "$b" in
    first) printf '1.0.0'; return ;;
    [0-9]*.[0-9]*.[0-9]*) printf '%s' "$b"; return ;;
  esac
  printf '%s' "$cur" | grep -Eq '^[0-9]+\.[0-9]+\.[0-9]+$' || die "current version '$cur' is not X.Y.Z"
  major="${cur%%.*}"; minor="${cur#*.}"; minor="${minor%%.*}"; patch="${cur##*.}"
  case "$b" in
    major) printf '%s.0.0' "$((major + 1))" ;;
    minor) printf '%s.%s.0' "$major" "$((minor + 1))" ;;
    patch) printf '%s.%s.%s' "$major" "$minor" "$((patch + 1))" ;;
    *) die "bump must be major, minor, patch, first or X.Y.Z" ;;
  esac
}

# ---------- secrets ----------
# Files that look like passwords or keys never leave the source folder.
find_secrets() { # dir...
  find "$@" -type f \( -name '.env' -o -name '.env.*' -o -name '*.pem' -o -name '*.key' \
    -o -name 'id_rsa*' -o -name 'id_ed25519*' -o -iname '*credentials*' -o -iname '*secret*' \) \
    2>/dev/null
}

# ---------- commands ----------
do_setup() {
  [ -n "$SOURCE" ] && [ -n "$NAME" ] || die "setup needs --source and --name"
  printf '%s' "$NAME" | grep -Eq '^[a-z0-9]+(-[a-z0-9]+)*$' \
    || die "plugin name must be lowercase words joined by hyphens, like my-team-skills"
  [ -d "$SOURCE" ] || die "source folder not found: $SOURCE"
  SOURCE="$(cd "$SOURCE" && pwd)"
  # Default layout: .claude/skills and .claude/agents, where Claude loads them when it works in the
  # folder. A source that keeps them at the top level (skills/, agents/) is picked up instead.
  if [ -z "$SKILLS_DIR" ]; then
    if [ -d "$SOURCE/.claude/skills" ] || [ ! -d "$SOURCE/skills" ]; then SKILLS_DIR=".claude/skills"; else SKILLS_DIR="skills"; fi
  fi
  if [ -z "$AGENTS_DIR" ]; then
    if [ -d "$SOURCE/.claude/agents" ] || [ ! -d "$SOURCE/agents" ]; then AGENTS_DIR=".claude/agents"; else AGENTS_DIR="agents"; fi
  fi
  [ -n "$OWNER" ] || OWNER="$(git -C "$REPO" config user.name 2>/dev/null)"
  [ -n "$OWNER" ] || OWNER="$NAME"
  [ -n "$DESCRIPTION" ] || DESCRIPTION="Skills and agents published from $(basename "$SOURCE")."
  DESCRIPTION="$(printf '%s' "$DESCRIPTION" | sed 's/\\/\\\\/g; s/"/\\"/g')"
  OWNER="$(printf '%s' "$OWNER" | sed 's/\\/\\\\/g; s/"/\\"/g')"

  {
    printf 'source=%s\n' "$SOURCE"
    printf 'plugin=%s\n' "$NAME"
    printf 'skills_dir=%s\n' "$SKILLS_DIR"
    printf 'agents_dir=%s\n' "$AGENTS_DIR"
  } > "$REPO/$SETTINGS_FILE"

  # Settings hold a path on this computer: keep them out of the shared history.
  touch "$REPO/.gitignore"
  grep -qx "$SETTINGS_FILE" "$REPO/.gitignore" || printf '%s\n' "$SETTINGS_FILE" >> "$REPO/.gitignore"
  grep -qx '.DS_Store' "$REPO/.gitignore" || printf '.DS_Store\n' >> "$REPO/.gitignore"

  local pdir="$REPO/plugins/$NAME/.claude-plugin" mdir="$REPO/.claude-plugin"
  mkdir -p "$pdir" "$mdir"
  if [ ! -f "$pdir/plugin.json" ]; then
    cat > "$pdir/plugin.json" <<EOF
{
  "name": "$NAME",
  "description": "$DESCRIPTION",
  "version": "0.0.0",
  "author": {
    "name": "$OWNER"
  }
}
EOF
    note "created plugins/$NAME/.claude-plugin/plugin.json"
  fi
  if [ ! -f "$mdir/marketplace.json" ]; then
    cat > "$mdir/marketplace.json" <<EOF
{
  "name": "$NAME",
  "description": "$DESCRIPTION",
  "owner": {
    "name": "$OWNER"
  },
  "plugins": [
    {
      "name": "$NAME",
      "source": "./plugins/$NAME",
      "description": "$DESCRIPTION",
      "version": "0.0.0"
    }
  ]
}
EOF
    note "created .claude-plugin/marketplace.json"
  fi
  if [ ! -f "$REPO/README.md" ]; then
    cat > "$REPO/README.md" <<EOF
# $NAME

$DESCRIPTION

This repository is a Claude plugin marketplace. It holds only released versions of the skills and
agents in \`plugins/$NAME/\`. They are built and changed in a separate source repository.

## Install

- **Claude (web, desktop app, Cowork):** Customize › Plugins › Add › Add marketplace, enter this
  repository's GitHub address, then install **$NAME**. For a private repository, connect GitHub
  and give the Claude GitHub App access to it when asked.
- **Claude Code:** \`/plugin marketplace add <owner>/<this-repository>\`, then
  \`/plugin install $NAME@$NAME\`.

Updates arrive when a new version is released. Don't edit files here by hand: changes are made in
the source repository and published with the \`publishing-plugins\` skill.
EOF
    note "created README.md"
  fi
  note "saved settings: source=$SOURCE plugin=$NAME skills=$SKILLS_DIR agents=$AGENTS_DIR"
}

do_check() {
  load_settings
  local attention=0
  git -C "$REPO" rev-parse --is-inside-work-tree >/dev/null 2>&1 \
    || die "the plugin folder is not a Git repository: $REPO"
  check_manifest "$PLUGIN_JSON" "plugin.json"
  check_manifest "$MARKET_JSON" "marketplace.json"
  grep -q "\"name\"[[:space:]]*:[[:space:]]*\"$NAME\"" "$PLUGIN_JSON" \
    || die "plugin.json's name doesn't match the plugin name in the settings ($NAME): $PLUGIN_JSON"

  # Secrets first: nothing else matters, and nothing may be offered for saving, until they're gone.
  local secrets; secrets="$(find_secrets "$SOURCE/$SKILLS_DIR" "$SOURCE/$AGENTS_DIR")"
  if [ -n "$secrets" ]; then
    note "SECRET files that look like passwords or keys are in the source. Stop here:"
    printf '%s\n' "$secrets"
    exit 3
  fi

  local pv mv; pv="$(read_version "$PLUGIN_JSON")"; mv="$(read_version "$MARKET_JSON")"
  if [ "$pv" != "$mv" ]; then
    note "ATTENTION versions differ: plugin.json $pv, marketplace.json $mv"; attention=1
  fi
  note "current version: $pv"

  if [ -n "$(git -C "$REPO" status --porcelain)" ]; then
    note "ATTENTION the plugin folder has unsaved changes:"
    git -C "$REPO" status --short
    attention=1
  fi

  [ -d "$SOURCE/$SKILLS_DIR" ] || [ -d "$SOURCE/$AGENTS_DIR" ] \
    || die "source has neither $SKILLS_DIR/ nor $AGENTS_DIR/: $SOURCE"

  if git -C "$SOURCE" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    local dirty
    dirty="$(git -C "$SOURCE" status --porcelain -- "$SKILLS_DIR" "$AGENTS_DIR" 2>/dev/null)"
    if [ -n "$dirty" ]; then
      note "ATTENTION the source has skill or agent changes not yet saved in its history:"
      printf '%s\n' "$dirty"
      attention=1
    fi
    note "source commit: $(git -C "$SOURCE" rev-parse --short HEAD 2>/dev/null || printf 'none yet')"
  else
    note "source is not a Git repository; its history won't be recorded in the release"
  fi

  [ "$attention" = "0" ] && note "ready to publish" || exit 2
}

prune() { # dir — remove files that never ship
  [ -d "$1" ] || return 0
  find "$1" \( -name '.DS_Store' -o -name 'Thumbs.db' -o -name 'desktop.ini' -o -name 'Untitled' \
    -o -name '.git' -o -name 'node_modules' -o -name '__pycache__' -o -name '*.pyc' \
    -o -name 'evals' -o -name '*-workspace' -o -name 'iteration-*' \) -prune -exec rm -rf {} + 2>/dev/null
  return 0
}

do_copy() {
  load_settings
  local secrets; secrets="$(find_secrets "$SOURCE/$SKILLS_DIR" "$SOURCE/$AGENTS_DIR")"
  if [ -n "$secrets" ]; then
    note "SECRET files that look like passwords or keys are in the source. Nothing was copied:"
    printf '%s\n' "$secrets"
    exit 3
  fi

  local n_skills=0 n_agents=0 d f
  rm -rf "$PLUGIN_DIR/skills" "$PLUGIN_DIR/agents"
  mkdir -p "$PLUGIN_DIR/skills" "$PLUGIN_DIR/agents"

  if [ -d "$SOURCE/$SKILLS_DIR" ]; then
    for d in "$SOURCE/$SKILLS_DIR"/*/; do
      [ -f "${d}SKILL.md" ] || continue          # a skill is a folder holding SKILL.md
      cp -R "${d%/}" "$PLUGIN_DIR/skills/"
      n_skills=$((n_skills + 1))
    done
  fi
  if [ -d "$SOURCE/$AGENTS_DIR" ]; then
    for f in "$SOURCE/$AGENTS_DIR"/*.md; do
      [ -f "$f" ] || continue                     # an agent is a top-level .md file
      cp "$f" "$PLUGIN_DIR/agents/"
      n_agents=$((n_agents + 1))
    done
  fi
  prune "$PLUGIN_DIR/skills"; prune "$PLUGIN_DIR/agents"
  rmdir "$PLUGIN_DIR/agents" 2>/dev/null || true
  note "copied $n_skills skill(s) and $n_agents agent(s) into plugins/$NAME"
  do_changes
}

# One line per changed file in the plugin, reduced to one line per skill or agent.
# (A function, not inline: macOS's Bash 3.2 can't parse a case statement inside $( ).)
list_units() {
  local line path rel unit
  git -C "$REPO" -c core.quotepath=off status --porcelain --untracked-files=all \
      -- "plugins/$NAME/skills" "plugins/$NAME/agents" \
    | while IFS= read -r line; do
        path="${line:3}"; path="${path#\"}"; path="${path%\"}"
        rel="${path#plugins/$NAME/}"
        case "$rel" in
          skills/*) unit="${rel#skills/}"; printf 'skill\t%s\n' "${unit%%/*}" ;;
          agents/*) printf 'agent\t%s\n' "${rel#agents/}" ;;
        esac
      done | sort -u
}

do_changes() {
  load_settings
  local has_head=0 units kind unit before now added=0 updated=0 removed=0
  git -C "$REPO" rev-parse --verify HEAD >/dev/null 2>&1 && has_head=1
  units="$(list_units)"

  if [ -z "$units" ]; then
    note "no changes since the last release"
    note "suggested bump: none"
    return 0
  fi

  while IFS="$(printf '\t')" read -r kind unit; do
    [ -n "$kind" ] || continue
    if [ "$kind" = "skill" ]; then
      now=0; [ -d "$PLUGIN_DIR/skills/$unit" ] && now=1
      before=0
      [ "$has_head" = "1" ] && [ -n "$(git -C "$REPO" ls-tree HEAD "plugins/$NAME/skills/$unit")" ] && before=1
    else
      now=0; [ -f "$PLUGIN_DIR/agents/$unit" ] && now=1
      before=0
      [ "$has_head" = "1" ] && [ -n "$(git -C "$REPO" ls-tree HEAD "plugins/$NAME/agents/$unit")" ] && before=1
    fi
    if   [ "$before" = "0" ]; then note "added $kind: $unit";   added=$((added + 1))
    elif [ "$now" = "0" ];    then note "removed $kind: $unit"; removed=$((removed + 1))
    else                           note "updated $kind: $unit"; updated=$((updated + 1))
    fi
  done <<EOF
$units
EOF

  local cur; cur="$(read_version "$PLUGIN_JSON")"
  if   [ "${cur%%.*}" = "0" ]; then note "suggested bump: first"   # 0.x = never released
  elif [ "$removed" -gt 0 ];   then note "suggested bump: major"
  elif [ "$added" -gt 0 ];     then note "suggested bump: minor"
  else                              note "suggested bump: patch"
  fi
}

do_bump() {
  load_settings
  [ -n "$BUMP" ] || die "bump needs major, minor, patch, first or X.Y.Z"
  check_manifest "$PLUGIN_JSON" "plugin.json"
  check_manifest "$MARKET_JSON" "marketplace.json"
  local cur new
  cur="$(read_version "$PLUGIN_JSON")"
  new="$(next_version "$cur" "$BUMP")" || exit 1
  write_version "$PLUGIN_JSON" "$new"
  write_version "$MARKET_JSON" "$new"
  [ "$(read_version "$PLUGIN_JSON")" = "$new" ] && [ "$(read_version "$MARKET_JSON")" = "$new" ] \
    || die "version update failed; check both manifests by hand"
  note "version: $cur -> $new"
}

case "$cmd" in
  setup)   do_setup ;;
  check)   do_check ;;
  copy)    do_copy ;;
  changes) do_changes ;;
  bump)    do_bump ;;
  *)       die "unknown command '$cmd'. Use setup, check, copy, changes or bump." ;;
esac
