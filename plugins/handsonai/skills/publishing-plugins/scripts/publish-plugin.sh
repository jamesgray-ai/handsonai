#!/usr/bin/env bash
# publish-plugin.sh — release skills and agents from a source repository into one or more
# Claude plugins in a separate plugin repository, with a version number per plugin.
# Needs only Bash and Git: built into macOS; on Windows, run it in Git Bash (Git for Windows).
#
# Usage: publish-plugin.sh <command> --plugin-repo <path> [options] [arguments]
#
#   setup       --source <path> [--marketplace <name>] [--owner <name>] [--description <text>]
#               [--skills-dir .claude/skills] [--agents-dir .claude/agents]
#               Saves the settings, and creates the marketplace file, README and release plan
#               if they are missing. A plugin repository with no history yet starts on "main".
#   add-plugin  --name <plugin-name> [--description <text>] [--owner <name>]
#               Adds a plugin to the plugin repository (keeps an existing plugin.json).
#   describe    <plugin> --description <text>   Changes a plugin's description (shown in Claude).
#   list        Shows each plugin with its version and description, the release plan, and anything
#               undecided.
#   assign      <plugin|none> <skill|agent> <name>   Records where a skill or agent is released.
#               "none" means it stays in the source repository.
#   unassign    <plugin|none> <skill|agent> <name>   Removes that line from the release plan.
#   check       Checks everything is ready to publish. Exit 2 = something needs attention.
#   copy        Copies each plugin's skills and agents from the source, then lists what changed.
#   changes     Lists what changed per plugin since the last saved release, with the version
#               change each one calls for.
#   bump        <plugin> <major|minor|patch|first|X.Y.Z>   Sets that plugin's new version.
#
# Files in the plugin repository:
#   .publish-plugin    settings (a path on this computer; kept out of Git)
#   release-plan.txt   one line per skill or agent: <plugin|none> <skill|agent> <name>
#   .claude-plugin/marketplace.json   rebuilt from the plugins on every change
#   plugins/<name>/.claude-plugin/plugin.json, skills/, agents/
#
# Exit codes: 0 ok · 1 usage or error · 2 needs attention · 3 possible secret found.
# Never commits or pushes: the skill does that after the person approves.

set -u

SETTINGS_FILE=".publish-plugin"
PLAN_FILE="release-plan.txt"
NAME_RE='^[a-z0-9]+(-[a-z0-9]+)*$'

die()  { printf 'ERROR: %s\n' "$*" >&2; exit 1; }
note() { printf '%s\n' "$*"; }
json_escape() { printf '%s' "$1" | tr '\n\r\t' '   ' | sed 's/\\/\\\\/g; s/"/\\"/g'; }

cmd="${1:-}"; [ -n "$cmd" ] || die "no command. Run with no arguments to see usage in the file header."
shift

REPO=""; SOURCE=""; NAME=""; MARKET=""; DESCRIPTION=""; OWNER=""; SKILLS_DIR=""; AGENTS_DIR=""
ARGS=""
while [ $# -gt 0 ]; do
  case "$1" in
    --plugin-repo) REPO="${2:-}"; shift 2 ;;
    --source)      SOURCE="${2:-}"; shift 2 ;;
    --name)        NAME="${2:-}"; shift 2 ;;
    --marketplace) MARKET="${2:-}"; shift 2 ;;
    --description) DESCRIPTION="${2:-}"; shift 2 ;;
    --owner)       OWNER="${2:-}"; shift 2 ;;
    --skills-dir)  SKILLS_DIR="${2:-}"; shift 2 ;;
    --agents-dir)  AGENTS_DIR="${2:-}"; shift 2 ;;
    -*)            die "unknown option $1" ;;
    *)             ARGS="$ARGS $1"; shift ;;
  esac
done
set -- $ARGS  # names never contain spaces

[ -n "$REPO" ] || die "--plugin-repo is required: the folder of your plugin repository"
[ -d "$REPO" ] || die "plugin repository folder not found: $REPO"
REPO="$(cd "$REPO" && pwd -P)"
MARKET_JSON="$REPO/.claude-plugin/marketplace.json"
PLAN="$REPO/$PLAN_FILE"

# ---------- settings ----------
read_setting() { [ -f "$REPO/$SETTINGS_FILE" ] && sed -n "s/^$1=//p" "$REPO/$SETTINGS_FILE" | head -n 1; }

load_settings() {
  [ -f "$REPO/$SETTINGS_FILE" ] || die "no settings in $REPO. Run setup first."
  SOURCE="$(read_setting source)"
  SKILLS_DIR="$(read_setting skills_dir)"; AGENTS_DIR="$(read_setting agents_dir)"
  [ -n "$SKILLS_DIR" ] || SKILLS_DIR=".claude/skills"
  [ -n "$AGENTS_DIR" ] || AGENTS_DIR=".claude/agents"
  [ -n "$SOURCE" ] || die "settings file is missing the source repository."
  [ -d "$SOURCE" ] || die "source repository not found: $SOURCE"
}

# ---------- JSON fields (files this script writes: one key per line) ----------
json_field() { # file key -> raw (still-escaped) string value of the first occurrence
  grep -Eo "\"$2\"[[:space:]]*:[[:space:]]*\"([^\"\\\\]|\\\\.)*\"" "$1" 2>/dev/null | head -n 1 \
    | sed -E "s/^\"$2\"[[:space:]]*:[[:space:]]*\"//; s/\"\$//"
}
json_top() { # file key -> first value of key at the top level of the object (one key per line)
  local v
  v="$(tr -d '\r' < "$1" 2>/dev/null | awk -v k="$2" '
    { if (depth == 1 && match($0, "\"" k "\"[ \t]*:[ \t]*\"([^\"\\\\]|\\\\.)*\"")) {
        t = substr($0, RSTART, RLENGTH); sub("^\"" k "\"[ \t]*:[ \t]*\"", "", t); sub("\"$", "", t); print t; exit }
      o = gsub(/\{/, "{"); c = gsub(/\}/, "}"); depth += o - c }')"
  [ -n "$v" ] && printf '%s' "$v" || json_field "$1" "$2"
}
VERSION_RE='"version"[[:space:]]*:[[:space:]]*"[^"]*"'
count_versions() { grep -o "$VERSION_RE" "$1" 2>/dev/null | wc -l | tr -d ' '; }

plugin_json() { printf '%s/plugins/%s/.claude-plugin/plugin.json' "$REPO" "$1"; }
released_version() { # plugin -> version in the last saved release, or empty if never saved
  git -C "$REPO" show "HEAD:plugins/$1/.claude-plugin/plugin.json" 2>/dev/null \
    | grep -Eo '"version"[[:space:]]*:[[:space:]]*"[^"]*"' | head -n 1 | sed -E 's/.*"([^"]*)"$/\1/'
}
base_version() { # the version a new release counts up from
  local v; v="$(released_version "$1")"
  [ -n "$v" ] || v="$(json_field "$(plugin_json "$1")" version)"
  printf '%s' "$v"
}
plugin_names() { # every plugin folder that has a plugin.json, sorted
  local d
  for d in "$REPO"/plugins/*/; do
    [ -f "${d}.claude-plugin/plugin.json" ] && basename "$d"
  done | sort
}
plugin_exists() { [ -f "$(plugin_json "$1")" ]; }

PLUGINS_KEY_RE='^[[:space:]]*"plugins"[[:space:]]*:'
strip_cr() { tr -d '\r' < "$1"; }

# Print the marketplace file this script would write for the given plugin names, keeping everything
# above the "plugins" key exactly as it is.
gen_marketplace() { # names...
  local p pj first=1
  strip_cr "$MARKET_JSON" | awk -v re="$PLUGINS_KEY_RE" '$0 ~ re { exit } { print }'
  printf '  "plugins": ['
  for p in "$@"; do
    pj="$(plugin_json "$p")"
    [ "$first" = "1" ] && printf '\n' || printf ',\n'
    first=0
    printf '    {\n'
    printf '      "name": "%s",\n' "$p"
    printf '      "source": "./plugins/%s",\n' "$p"
    printf '      "description": "%s",\n' "$(json_field "$pj" description)"
    printf '      "version": "%s"\n' "$(json_field "$pj" version)"
    printf '    }'
  done
  [ "$first" = "1" ] && printf ']\n}\n' || printf '\n  ]\n}\n'
}

# Refuse to touch a marketplace file this script didn't write, or one changed by hand since: it must
# be exactly what this script would write for the plugins it lists. Anything else (a plugin at the
# top of the repository, one fetched from elsewhere, extra settings, a renamed entry, a version that
# differs from the plugin's own) belongs to another setup, and rewriting it could uninstall or
# downgrade a plugin people already use. Called before any command changes anything.
assert_managed() {
  [ -f "$MARKET_JSON" ] || return 0
  strip_cr "$MARKET_JSON" | grep -Eq "$PLUGINS_KEY_RE" \
    || die "$MARKET_JSON has no \"plugins\" list this skill can manage. Nothing was changed. Use a new, empty plugin repository instead."
  local src listed="" foreign=""
  for src in $(strip_cr "$MARKET_JSON" | grep -Eo '"source"[[:space:]]*:[[:space:]]*"[^"]*"' | sed -E 's/.*"([^"]*)"$/\1/'); do
    case "$src" in
      ./plugins/*) if [ -f "$REPO/${src#./}/.claude-plugin/plugin.json" ]; then listed="$listed ${src#./plugins/}"; else foreign="$foreign $src"; fi ;;
      *) foreign="$foreign $src" ;;
    esac
  done
  strip_cr "$MARKET_JSON" | grep -Eq '"source"[[:space:]]*:[[:space:]]*\{' && foreign="$foreign (a plugin from another location)"
  [ -z "$foreign" ] || die "this plugin repository already lists a plugin this skill doesn't manage:$foreign. Nothing was changed. Use a new, empty plugin repository instead."
  # shellcheck disable=SC2086
  if [ "$(gen_marketplace $(printf '%s\n' $listed | sort))" != "$(strip_cr "$MARKET_JSON")" ]; then
    # Committed by a release, then edited by hand: that's an undo, not a new repository.
    local edited
    edited="$(git -C "$REPO" rev-parse --verify HEAD >/dev/null 2>&1 \
      && git -C "$REPO" diff --name-only HEAD -- .claude-plugin/marketplace.json 'plugins/*/.claude-plugin/plugin.json' 2>/dev/null)"
    if [ -n "$edited" ]; then
      note "ATTENTION the plugin repository has changes made by hand:"
      printf ' M %s\n' $edited
      exit 2
    fi
    die "the marketplace file in this plugin repository isn't one this skill wrote. Nothing was changed. Use a new, empty plugin repository instead, or ask whoever set it up."
  fi
}

# Rebuild the plugins list in marketplace.json from each plugin's plugin.json, so the two can
# never disagree. Only ever called after assert_managed has passed.
regen_marketplace() {
  [ -f "$MARKET_JSON" ] || die "marketplace file not found: $MARKET_JSON. Run setup first."
  local tmp="$MARKET_JSON.tmp.$$"
  # shellcheck disable=SC2046
  gen_marketplace $(plugin_names) > "$tmp" && mv "$tmp" "$MARKET_JSON"
}

# Leftovers from a run that was interrupted never ship.
clean_tmp() { rm -f "$MARKET_JSON".tmp.* "$PLAN".tmp.* "$REPO"/plugins/*/.claude-plugin/plugin.json.tmp.* 2>/dev/null; return 0; }

# ---------- source items ----------
source_items() { # "skill <name>" / "agent <name>" for everything in the source, sorted
  local d f
  if [ -d "$SOURCE/$SKILLS_DIR" ]; then
    for d in "$SOURCE/$SKILLS_DIR"/*/; do [ -f "${d}SKILL.md" ] && printf 'skill %s\n' "$(basename "$d")"; done
  fi
  if [ -d "$SOURCE/$AGENTS_DIR" ]; then
    for f in "$SOURCE/$AGENTS_DIR"/*.md; do
      [ -f "$f" ] && grep -Eq '^name:[[:space:]]*[^[:space:]]' "$f" && printf 'agent %s\n' "$(basename "$f" .md)"
    done
  fi
}
bad_names() { # skills/agents whose names aren't lowercase-with-hyphens
  local kind name
  source_items | while read -r kind name; do
    printf '%s' "$name" | grep -Eq "$NAME_RE" || printf '%s "%s"\n' "$kind" "$name"
  done
}
empty_skills() { # skills whose SKILL.md has no name: line
  local kind name
  source_items | while read -r kind name; do
    [ "$kind" = "skill" ] || continue
    grep -Eq '^name:[[:space:]]*[^[:space:]]' "$SOURCE/$SKILLS_DIR/$name/SKILL.md" 2>/dev/null || printf 'skill %s\n' "$name"
  done
}
source_path() { # kind name -> path in the source
  [ "$1" = "skill" ] && printf '%s/%s/%s' "$SOURCE" "$SKILLS_DIR" "$2" || printf '%s/%s/%s.md' "$SOURCE" "$AGENTS_DIR" "$2"
}

# ---------- release plan ----------
plan_lines() { [ -f "$PLAN" ] && tr -d '\r' < "$PLAN" | sed 's/[[:space:]]*$//' | grep -v '^[[:space:]]*#' | grep -v '^[[:space:]]*$'; return 0; }
plan_decided() { plan_lines | awk -v k="$1" -v n="$2" '$2==k && $3==n { found=1 } END { exit !found }'; }
undecided_items() {
  local kind name
  source_items | while read -r kind name; do
    printf '%s' "$name" | grep -Eq "$NAME_RE" || continue   # reported as RENAME instead
    plan_decided "$kind" "$name" || printf '%s %s\n' "$kind" "$name"
  done
}
missing_items() { # plan lines whose skill or agent is no longer in the source
  local plugin kind name
  plan_lines | while read -r plugin kind name; do
    [ -e "$(source_path "$kind" "$name")" ] || printf '%s %s %s\n' "$plugin" "$kind" "$name"
  done
}
shipped_items() { plan_lines | awk '$1 != "none"'; } # "<plugin> <kind> <name>"

# ---------- secrets ----------
find_secrets_in() { # paths... -> one line per file (name) or file:line (contents) that looks like a secret
  local p
  for p in "$@"; do
    [ -e "$p" ] || continue
    # Files whose names mean credentials.
    find "$p" -type f \( -name '.env' -o -name '.env.*' -o -name '*.pem' -o -name '*.key' -o -name '*.p12' \
      -o -name '*.pfx' -o -name 'id_rsa' -o -name 'id_rsa.*' -o -name 'id_ed25519' -o -name 'id_ed25519.*' \
      -o -name '.npmrc' -o -name '.netrc' -o -name 'credentials' -o -name 'credentials.json' \
      -o -name 'client_secret*.json' -o -name '*service-account*.json' -o -name 'token.json' \) \
      ! -name '*.example' ! -name '*.sample' 2>/dev/null
    # Keys pasted into any file. Placeholders ("your-", "xxxx", "EXAMPLE", "<...>", "...") are ignored,
    # and a real key mixes letters and digits.
    grep -rnoE -e '-----BEGIN [A-Z ]*PRIVATE KEY-----' -e 'sk-ant-[A-Za-z0-9_-]{20,}' -e 'AKIA[0-9A-Z]{16}' \
        -e 'gh[pousr]_[A-Za-z0-9]{30,}' -e 'github_pat_[A-Za-z0-9_]{30,}' -e 'xox[abpr]-[A-Za-z0-9-]{10,}' "$p" 2>/dev/null \
      | awk -F: '{
          m = $0; sub(/^[^:]*:[^:]*:/, "", m)
          if (m ~ /PRIVATE KEY/) { if ($1 !~ /\.(md|txt)$/) print $1 ":" $2 " (a private key)"; next }
          if (m ~ /(EXAMPLE|[Xx]{6,}|[Yy][Oo][Uu][Rr]|<|\.\.\.)/) next
          d = gsub(/[0-9]/, "&", m); l = gsub(/[A-Za-z]/, "&", m)
          if (d >= 4 && l >= 4) print $1 ":" $2 " (looks like a key)"
        }'
  done
}
shipped_secrets() {
  local plugin kind name src
  shipped_items | while read -r plugin kind name; do
    src="$(source_path "$kind" "$name")"
    find_secrets_in "$src"
    # A shortcut (symlink) could point at a secret outside the skill: never release one.
    [ -e "$src" ] && find "$src" -type l 2>/dev/null | sed 's/$/ (a shortcut; replace it with the real file)/'
  done | sort -u
}

# ---------- commands ----------
do_setup() {
  [ -n "$SOURCE" ] || die "setup needs --source"
  [ -d "$SOURCE" ] || die "source repository not found: $SOURCE"
  SOURCE="$(cd "$SOURCE" && pwd -P)"
  [ "$SOURCE" != "$REPO" ] || die "the source repository and the plugin repository must be two different folders"
  case "$REPO/" in "$SOURCE/"*) die "the plugin repository is inside the source repository; make it a separate folder next to it" ;; esac
  case "$SOURCE/" in "$REPO/"*) die "the source repository is inside the plugin repository; they must be two separate folders" ;; esac
  if git -C "$REPO" rev-parse --is-inside-work-tree >/dev/null 2>&1 && [ -n "$(git -C "$REPO" rev-parse --show-prefix 2>/dev/null)" ]; then
    die "the plugin repository folder is inside another Git repository ($(git -C "$REPO" rev-parse --show-toplevel)); it must be its own repository"
  fi
  # Default layout: .claude/skills and .claude/agents, where Claude loads them when it works in
  # the folder. A source that keeps them at the top level (skills/, agents/) is picked up instead.
  if [ -z "$SKILLS_DIR" ]; then
    if [ -d "$SOURCE/.claude/skills" ] || [ ! -d "$SOURCE/skills" ]; then SKILLS_DIR=".claude/skills"; else SKILLS_DIR="skills"; fi
  fi
  if [ -z "$AGENTS_DIR" ]; then
    if [ -d "$SOURCE/.claude/agents" ] || [ ! -d "$SOURCE/agents" ]; then AGENTS_DIR=".claude/agents"; else AGENTS_DIR="agents"; fi
  fi
  if [ -z "$(SKILLS_DIR="$SKILLS_DIR" AGENTS_DIR="$AGENTS_DIR" source_items)" ]; then
    die "no skills or agents found in $SOURCE (looked in $SKILLS_DIR and $AGENTS_DIR)"
  fi
  assert_managed
  clean_tmp
  # A brand-new plugin repository starts on "main", the same name GitHub and the source use, so
  # nobody sees two names for the same idea. Only before the first release: never rename history.
  if git -C "$REPO" rev-parse --is-inside-work-tree >/dev/null 2>&1 \
     && ! git -C "$REPO" rev-parse --verify HEAD >/dev/null 2>&1; then
    git -C "$REPO" symbolic-ref HEAD refs/heads/main
  fi
  if [ -f "$MARKET_JSON" ]; then
    [ -z "$MARKET" ] || [ "$MARKET" = "$(json_field "$MARKET_JSON" name)" ] \
      || note "NOTE the marketplace is already named $(json_field "$MARKET_JSON" name); kept that name"
    MARKET="$(json_field "$MARKET_JSON" name)"
  else
    [ -n "$MARKET" ] || MARKET="$(basename "$REPO" | tr 'A-Z_ .' 'a-z---')"
    printf '%s' "$MARKET" | grep -Eq "$NAME_RE" || die "marketplace name must be lowercase words joined by hyphens: $MARKET"
  fi
  [ -n "$OWNER" ] || OWNER="$(git -C "$REPO" config user.name 2>/dev/null)"
  [ -n "$OWNER" ] || OWNER="$MARKET"
  [ -n "$DESCRIPTION" ] || DESCRIPTION="Skills and agents released from $(basename "$SOURCE")."

  {
    printf 'source=%s\n' "$SOURCE"
    printf 'skills_dir=%s\n' "$SKILLS_DIR"
    printf 'agents_dir=%s\n' "$AGENTS_DIR"
  } > "$REPO/$SETTINGS_FILE"

  add_line() { # file line: append a line, starting a new line first if the file doesn't end with one
    touch "$1"
    tr -d '\r' < "$1" | grep -qx "$2" && return 0
    [ -s "$1" ] && [ -n "$(tail -c 1 "$1")" ] && printf '\n' >> "$1"
    printf '%s\n' "$2" >> "$1"
  }
  add_line "$REPO/.gitignore" "$SETTINGS_FILE"
  add_line "$REPO/.gitignore" ".DS_Store"
  # Keep line endings the same on every computer, so a Windows checkout can't change the plan.
  add_line "$REPO/.gitattributes" "* text=auto eol=lf"

  mkdir -p "$REPO/.claude-plugin"
  if [ ! -f "$MARKET_JSON" ]; then
    {
      printf '{\n'
      printf '  "name": "%s",\n' "$MARKET"
      printf '  "description": "%s",\n' "$(json_escape "$DESCRIPTION")"
      printf '  "owner": {\n    "name": "%s"\n  },\n' "$(json_escape "$OWNER")"
      printf '  "plugins": []\n}\n'
    } > "$MARKET_JSON"
    note "created .claude-plugin/marketplace.json"
  fi
  if [ ! -f "$PLAN" ]; then
    cat > "$PLAN" <<'EOF'
# Release plan: which plugin each skill and agent is released in.
# One line each: <plugin> <skill|agent> <name>. A skill can be in more than one plugin.
# "none" as the plugin means it stays in the source repository and is never released.
EOF
    note "created $PLAN_FILE"
  fi
  local slug
  slug="$(git -C "$REPO" remote get-url origin 2>/dev/null | sed -nE 's#^.*github\.com[:/]([^/]+/[^/]+)$#\1#p' | sed 's/\.git$//')"
  [ -n "$slug" ] || slug="<owner>/<this-repository>"
  if [ ! -f "$REPO/README.md" ]; then
    cat > "$REPO/README.md" <<EOF
# $MARKET

$DESCRIPTION

This repository is a Claude plugin marketplace. It holds only released versions of skills and
agents, in \`plugins/\`. They are built and changed in a separate source repository, and
\`$PLAN_FILE\` records which plugin each one is released in.

## Install

- **Claude (web, desktop app):** Customize › Plugins › Add › Add marketplace, enter
  \`$slug\`, then install the plugin your team uses. For a private repository, connect
  GitHub when asked and give the Claude GitHub App access to this repository only.
- **Claude Code:** \`/plugin marketplace add $slug\`, then
  \`/plugin install <plugin>@$MARKET\`.

Updates arrive when a new version is released. Don't edit files here by hand: changes are made in
the source repository and published with the \`publishing-plugins\` skill.
EOF
    note "created README.md"
  fi
  regen_marketplace
  note "saved settings: source=$SOURCE skills=$SKILLS_DIR agents=$AGENTS_DIR marketplace=$(json_field "$MARKET_JSON" name)"
}

do_add_plugin() {
  load_settings
  [ -n "$NAME" ] || die "add-plugin needs --name"
  printf '%s' "$NAME" | grep -Eq "$NAME_RE" || die "plugin name must be lowercase words joined by hyphens, like sales-team-skills"
  [ "$NAME" != "none" ] || die "\"none\" is reserved in the release plan"
  assert_managed
  clean_tmp
  local pj; pj="$(plugin_json "$NAME")"
  if [ -f "$pj" ]; then
    [ "$(json_top "$pj" name)" = "$NAME" ] || die "$pj names a different plugin; fix it by hand"
    note "plugin $NAME already exists (version $(json_field "$pj" version)); kept it"
  else
    [ -n "$OWNER" ] || OWNER="$(git -C "$REPO" config user.name 2>/dev/null)"
    [ -n "$OWNER" ] || OWNER="$NAME"
    [ -n "$DESCRIPTION" ] || DESCRIPTION="Skills and agents for the $NAME plugin."
    mkdir -p "$(dirname "$pj")"
    {
      printf '{\n'
      printf '  "name": "%s",\n' "$NAME"
      printf '  "description": "%s",\n' "$(json_escape "$DESCRIPTION")"
      printf '  "version": "0.0.0",\n'
      printf '  "author": {\n    "name": "%s"\n  }\n}\n' "$(json_escape "$OWNER")"
    } > "$pj"
    note "added plugin $NAME"
  fi
  regen_marketplace
}

do_describe() {
  load_settings
  [ $# -eq 1 ] || die "describe needs: <plugin> --description <text>"
  [ -n "$DESCRIPTION" ] || die "describe needs --description"
  plugin_exists "$1" || die "no plugin named $1"
  assert_managed
  clean_tmp
  local pj tmp
  pj="$(plugin_json "$1")"
  [ "$(grep -Ec '^[[:space:]]*"description"[[:space:]]*:' "$pj")" = "1" ] \
    || die "$pj must hold exactly one \"description\" line; fix it by hand"
  tmp="$pj.tmp.$$"
  NEWDESC="$(json_escape "$DESCRIPTION")" awk '
    /^[[:space:]]*"description"[[:space:]]*:/ && !done {
      match($0, /^[[:space:]]*/); ind = substr($0, 1, RLENGTH)
      comma = ($0 ~ /,[[:space:]]*$/) ? "," : ""
      print ind "\"description\": \"" ENVIRON["NEWDESC"] "\"" comma; done = 1; next }
    { print }' "$pj" > "$tmp" && mv "$tmp" "$pj"
  regen_marketplace
  note "$1 description: $(json_field "$pj" description)"
}

do_list() {
  load_settings
  local p any=0
  note "source repository: $SOURCE"
  note "plugins:"
  local pending=""
  if git -C "$REPO" rev-parse --verify HEAD >/dev/null 2>&1 && git -C "$REPO" remote get-url origin >/dev/null 2>&1; then
    if git -C "$REPO" rev-parse --abbrev-ref '@{u}' >/dev/null 2>&1; then
      [ "$(git -C "$REPO" rev-list --count '@{u}..HEAD' 2>/dev/null)" = "0" ] || pending=" (not yet on GitHub)"
    else
      pending=" (not yet on GitHub)"
    fi
  fi
  for p in $(plugin_names); do
    if [ -n "$(released_version "$p")" ]; then note "  $p $(released_version "$p")$pending"; else note "  $p not released yet"; fi
    note "    description: $(json_field "$(plugin_json "$p")" description)"
    any=1
  done
  [ "$any" = "1" ] || note "  (none yet)"
  note "release plan:"
  plan_lines | sed 's/^/  /'
  local u; u="$(undecided_items)"
  if [ -n "$u" ]; then note "undecided:"; printf '%s\n' "$u" | sed 's/^/  /'; fi
  return 0
}

do_assign() {
  load_settings
  [ $# -eq 3 ] || die "assign needs: <plugin|none> <skill|agent> <name>"
  local p="$1" k="$2" n="$3"
  [ "$k" = "skill" ] || [ "$k" = "agent" ] || die "kind must be skill or agent"
  [ "$p" = "none" ] || plugin_names | grep -qx "$p" || die "no plugin named $p. Plugins: $(plugin_names | tr '\n' ' ')"
  printf '%s' "$n" | grep -Eq "$NAME_RE" || die "$k \"$n\" needs a lowercase-with-hyphens name before it can be released"
  [ -e "$(source_path "$k" "$n")" ] || die "no $k named $n in the source repository"
  if [ "$p" = "none" ]; then
    plan_lines | awk -v k="$k" -v n="$n" '$1!="none" && $2==k && $3==n { f=1 } END { exit !f }' \
      && die "$k $n is released in a plugin; unassign it there first"
  else
    plan_lines | awk -v k="$k" -v n="$n" '$1=="none" && $2==k && $3==n { f=1 } END { exit !f }' \
      && die "$k $n is marked none; unassign it from none first"
  fi
  plan_lines | grep -qx "$p $k $n" && { note "already recorded: $p $k $n"; return 0; }
  printf '%s %s %s\n' "$p" "$k" "$n" >> "$PLAN"
  note "recorded: $p $k $n"
}

do_unassign() {
  load_settings
  [ $# -eq 3 ] || die "unassign needs: <plugin|none> <skill|agent> <name>"
  plan_lines | grep -qx "$1 $2 $3" || die "not in the release plan: $1 $2 $3"
  local tmp="$PLAN.tmp.$$"
  tr -d '\r' < "$PLAN" | sed 's/[[:space:]]*$//' | grep -vx "$1 $2 $3" > "$tmp"; mv "$tmp" "$PLAN"
  note "removed: $1 $2 $3"
}

do_check() {
  load_settings
  local attention=0 p pj
  git -C "$REPO" rev-parse --is-inside-work-tree >/dev/null 2>&1 \
    || die "the plugin repository folder is not a Git repository: $REPO"
  [ -z "$(git -C "$REPO" rev-parse --show-prefix 2>/dev/null)" ] \
    || die "the plugin repository folder is inside another Git repository ($(git -C "$REPO" rev-parse --show-toplevel)); it must be its own repository"
  [ -f "$MARKET_JSON" ] || die "marketplace file not found. Run setup first."
  assert_managed
  clean_tmp

  # Secrets first: nothing else matters, and nothing may be offered for saving, until they're gone.
  local secrets; secrets="$(shipped_secrets)"
  if [ -n "$secrets" ]; then
    note "SECRET files that look like passwords or keys would be released. Stop here:"
    printf '%s\n' "$secrets"
    exit 3
  fi

  for p in $(plugin_names); do
    pj="$(plugin_json "$p")"
    [ "$(count_versions "$pj")" = "1" ] || die "$pj must hold exactly one \"version\" field; fix it by hand"
    [ "$(json_top "$pj" name)" = "$p" ] || die "$pj's name doesn't match its folder ($p)"
    note "plugin $p: version $(json_field "$pj" version)"
  done
  [ -n "$(plugin_names)" ] || { note "ATTENTION no plugins yet: add one with add-plugin"; attention=1; }

  local bad; bad="$(shipped_items | while read -r p k n; do plugin_exists "$p" || printf '%s\n' "$p"; done | sort -u)"
  if [ -n "$bad" ]; then note "ATTENTION the release plan names plugins that don't exist:"; printf '%s\n' "$bad"; attention=1; fi

  local r; r="$(bad_names)"
  if [ -n "$r" ]; then note "RENAME these need a lowercase-with-hyphens name before they can be released:"; printf '%s\n' "$r"; attention=1; fi
  local e; e="$(empty_skills)"
  if [ -n "$e" ]; then note "EMPTY these skills have no name in their SKILL.md:"; printf '%s\n' "$e"; attention=1; fi
  local m; m="$(missing_items)"
  if [ -n "$m" ]; then note "MISSING the release plan lists these, but they're no longer in the source:"; printf '%s\n' "$m"; attention=1; fi
  local u; u="$(undecided_items)"
  if [ -n "$u" ]; then
    note "UNDECIDED not yet in the release plan (choose a plugin, or none):"
    printf '%s\n' "$u"
    attention=1
  fi

  # Changes this script makes (the release plan, the descriptor files, and the files setup creates)
  # are part of the release. Anything else changed in the plugin repository was done by hand.
  local stray
  stray="$(git -C "$REPO" -c core.quotepath=off status --porcelain --untracked-files=all | awk '{
      path = substr($0, 4); gsub(/^"|"$/, "", path)
      if (path == "release-plan.txt" || path == ".gitignore" || path == ".gitattributes" || path ~ /^\.claude-plugin\// \
          || path ~ /^plugins\/[^\/]+\/(\.claude-plugin|skills|agents)(\/|$)/ \
          || (substr($0, 1, 2) == "??" && path == "README.md")) next
      print
    }')"
  if [ -n "$stray" ]; then
    note "ATTENTION the plugin repository has changes made by hand:"
    printf '%s\n' "$stray"
    attention=1
  fi

  # Skills and agents already in a plugin that the release plan doesn't name would be removed by
  # the next copy: say so before anything changes.
  local only; only="$(for p in $(plugin_names); do
      for d in "$REPO/plugins/$p/skills"/*/; do [ -d "$d" ] && n="$(basename "$d")" && ! plan_lines | grep -qx "$p skill $n" && printf '%s skill %s\n' "$p" "$n"; done
      for f in "$REPO/plugins/$p/agents"/*.md; do [ -f "$f" ] && n="$(basename "$f" .md)" && ! plan_lines | grep -qx "$p agent $n" && printf '%s agent %s\n' "$p" "$n"; done
    done)"
  if [ -n "$only" ]; then
    note "ONLY IN PLUGIN these are in a plugin but not in the release plan, so publishing would remove them:"
    printf '%s\n' "$only"
    attention=1
  fi

  # A release saved on this computer but never sent to GitHub (a push that failed earlier).
  if git -C "$REPO" rev-parse --verify HEAD >/dev/null 2>&1 && git -C "$REPO" remote get-url origin >/dev/null 2>&1; then
    local ahead
    if git -C "$REPO" rev-parse --abbrev-ref '@{u}' >/dev/null 2>&1; then
      ahead="$(git -C "$REPO" rev-list --count '@{u}..HEAD' 2>/dev/null)"
    else
      ahead="$(git -C "$REPO" rev-list --count HEAD 2>/dev/null)"
    fi
    if [ "${ahead:-0}" != "0" ]; then
      note "UNPUSHED a release is saved on this computer but hasn't been sent to GitHub yet"
      attention=1
    fi
  fi

  if git -C "$SOURCE" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    local dirty
    dirty="$(git -C "$SOURCE" status --porcelain -- "$SKILLS_DIR" "$AGENTS_DIR" 2>/dev/null)"
    if [ -n "$dirty" ]; then
      note "ATTENTION the source has skill or agent changes not yet saved in its history:"
      printf '%s\n' "$dirty"
      attention=1
    fi
    # Every release names the source version it came from, so that version must be on GitHub too:
    # a release pointing at a commit nobody else can see can't be traced.
    if git -C "$SOURCE" rev-parse --verify HEAD >/dev/null 2>&1; then
      if git -C "$SOURCE" remote get-url origin >/dev/null 2>&1; then
        git -C "$SOURCE" fetch -q origin 2>/dev/null || true  # fresh view of GitHub; offline falls back to the last one
        if [ -z "$(git -C "$SOURCE" branch -r --contains HEAD 2>/dev/null)" ]; then
          note "SOURCE UNPUSHED the source version $(git -C "$SOURCE" rev-parse --short HEAD) is saved on this computer but isn't on GitHub yet"
          attention=1
        fi
      else
        note "NOTE the source repository has no GitHub connection, so others can't see the version a release names"
      fi
    fi
    note "source commit: $(git -C "$SOURCE" rev-parse --short HEAD 2>/dev/null || printf 'none yet')"
  else
    note "ATTENTION the source repository isn't a Git repository, so a release can't record what it came from"
    attention=1
  fi

  [ "$attention" = "0" ] && note "ready to publish" || exit 2
}

prune() { # dir: remove operating-system and tool clutter inside it. Never touches the folder's
          # own name or anything a skill might mean to ship.
  [ -d "$1" ] || return 0
  find "$1" -mindepth 1 \( -name '.DS_Store' -o -name 'Thumbs.db' -o -name 'desktop.ini' \
    -o -name '.git' -o -name 'node_modules' -o -name '__pycache__' -o -name '*.pyc' \) -prune -exec rm -rf {} + 2>/dev/null
  return 0
}

do_copy() {
  load_settings
  local secrets; secrets="$(shipped_secrets)"
  if [ -n "$secrets" ]; then
    note "SECRET files that look like passwords or keys would be released. Nothing was copied:"
    printf '%s\n' "$secrets"
    exit 3
  fi
  assert_managed
  clean_tmp
  local p dest kind name src n
  for p in $(plugin_names); do
    dest="$REPO/plugins/$p"
    rm -rf "$dest/skills" "$dest/agents"
    mkdir -p "$dest/skills" "$dest/agents"
    n=0
    while read -r pl kind name; do
      [ "$pl" = "$p" ] || continue
      src="$(source_path "$kind" "$name")"
      if [ ! -e "$src" ]; then note "MISSING $kind $name is in $p's plan but not in the source (it will be removed)"; continue; fi
      if [ "$kind" = "skill" ]; then
        cp -R "$src" "$dest/skills/" || die "couldn't copy skill $name into $p"
        prune "$dest/skills/$name"
      else
        cp "$src" "$dest/agents/" || die "couldn't copy agent $name into $p"
      fi
      n=$((n + 1))
    done <<EOF
$(shipped_items)
EOF
    rmdir "$dest/skills" "$dest/agents" 2>/dev/null || true
    note "copied $n skill(s) and agent(s) into $p"
    [ "$n" -gt 0 ] || note "EMPTY PLUGIN $p has no skills or agents in the release plan, so it would be released empty"
  done
  regen_marketplace
  do_changes
}

# One line per changed file under a plugin, reduced to one line per skill or agent.
# (A function, not inline: macOS's Bash 3.2 can't parse a case statement inside $( ).)
list_units() { # plugin
  local line path rel unit
  git -C "$REPO" -c core.quotepath=off status --porcelain --untracked-files=all \
      -- "plugins/$1/skills" "plugins/$1/agents" \
    | while IFS= read -r line; do
        path="${line:3}"; path="${path#\"}"; path="${path%\"}"
        rel="${path#plugins/$1/}"
        case "$rel" in
          skills/*) unit="${rel#skills/}"; printf 'skill\t%s\n' "${unit%%/*}" ;;
          agents/*) unit="${rel#agents/}"; printf 'agent\t%s\n' "${unit%.md}" ;;
        esac
      done | sort -u
}

do_changes() {
  load_settings
  local has_head=0 p units kind unit before now added removed updated cur any=0 path
  git -C "$REPO" rev-parse --verify HEAD >/dev/null 2>&1 && has_head=1
  for p in $(plugin_names); do
    units="$(list_units "$p")"
    [ -n "$units" ] || continue
    any=1; added=0; removed=0; updated=0
    note "plugin $p:"
    while IFS="$(printf '\t')" read -r kind unit; do
      [ -n "$kind" ] || continue
      if [ "$kind" = "skill" ]; then path="plugins/$p/skills/$unit"; now=0; [ -d "$REPO/$path" ] && now=1
      else path="plugins/$p/agents/$unit.md"; now=0; [ -f "$REPO/$path" ] && now=1; fi
      before=0
      [ "$has_head" = "1" ] && [ -n "$(git -C "$REPO" ls-tree HEAD "$path")" ] && before=1
      if   [ "$before" = "0" ]; then note "  added $kind: $unit";   added=$((added + 1))
      elif [ "$now" = "0" ];    then note "  removed $kind: $unit"; removed=$((removed + 1))
      else                           note "  updated $kind: $unit"; updated=$((updated + 1))
      fi
    done <<EOF
$units
EOF
    cur="$(released_version "$p")"
    if   [ -z "$cur" ] || [ "${cur%%.*}" = "0" ]; then note "  suggested bump: first"   # never released
    elif [ "$removed" -gt 0 ];   then note "  suggested bump: major"
    elif [ "$added" -gt 0 ];     then note "  suggested bump: minor"
    else                              note "  suggested bump: patch"
    fi
  done
  [ "$any" = "1" ] || note "no changes since the last release"
}

next_version() { # current bump
  local cur="$1" b="$2" major minor patch
  printf '%s' "$cur" | grep -Eq '^[0-9]+\.[0-9]+\.[0-9]+$' || die "current version '$cur' is not X.Y.Z"
  case "$b" in
    first) printf '1.0.0'; return ;;
  esac
  if printf '%s' "$b" | grep -Eq '^[0-9]+\.[0-9]+\.[0-9]+$'; then
    version_gt "$b" "$cur" || die "version $b must be higher than $cur, or teammates won't get the update"
    printf '%s' "$b"; return
  fi
  major="${cur%%.*}"; minor="${cur#*.}"; minor="${minor%%.*}"; patch="${cur##*.}"
  case "$b" in
    major) printf '%s.0.0' "$((major + 1))" ;;
    minor) printf '%s.%s.0' "$major" "$((minor + 1))" ;;
    patch) printf '%s.%s.%s' "$major" "$minor" "$((patch + 1))" ;;
    *) die "bump must be major, minor, patch, first or X.Y.Z" ;;
  esac
}

version_gt() { # a b -> true if a > b (X.Y.Z)
  local a1 a2 a3 b1 b2 b3
  IFS=. read -r a1 a2 a3 <<EOF
$1
EOF
  IFS=. read -r b1 b2 b3 <<EOF
$2
EOF
  [ "$a1" -gt "$b1" ] && return 0; [ "$a1" -lt "$b1" ] && return 1
  [ "$a2" -gt "$b2" ] && return 0; [ "$a2" -lt "$b2" ] && return 1
  [ "$a3" -gt "$b3" ]
}

do_bump() {
  load_settings
  [ $# -eq 2 ] || die "bump needs: <plugin> <major|minor|patch|first|X.Y.Z>"
  plugin_exists "$1" || die "no plugin named $1"
  assert_managed
  clean_tmp
  local pj cur new tmp
  pj="$(plugin_json "$1")"
  [ "$(count_versions "$pj")" = "1" ] || die "$pj must hold exactly one \"version\" field; fix it by hand"
  if [ "$2" = "first" ] && [ -n "$(released_version "$1")" ] && [ "$(released_version "$1" | cut -d. -f1)" != "0" ]; then
    die "$1 has already been released (version $(released_version "$1")); use major, minor or patch"
  fi
  cur="$(base_version "$1")"   # count up from the last saved release, so a re-run never bumps twice
  new="$(next_version "$cur" "$2")" || exit 1
  tmp="$pj.tmp.$$"
  sed "s/$VERSION_RE/\"version\": \"$new\"/" "$pj" > "$tmp" && mv "$tmp" "$pj"
  regen_marketplace
  [ "$(json_field "$pj" version)" = "$new" ] || die "version update failed; check $pj by hand"
  note "$1 version: $cur -> $new"
}

case "$cmd" in
  setup)      do_setup ;;
  add-plugin) do_add_plugin ;;
  describe)   do_describe ${1+"$@"} ;;
  list)       do_list ;;
  assign)     do_assign ${1+"$@"} ;;
  unassign)   do_unassign ${1+"$@"} ;;
  check)      do_check ;;
  copy)       do_copy ;;
  changes)    do_changes ;;
  bump)       do_bump ${1+"$@"} ;;
  *)          die "unknown command '$cmd'" ;;
esac
