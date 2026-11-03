#!/usr/bin/env bash
# Tests for plugins/handsonai/skills/publishing-plugins/scripts/publish-plugin.sh
# Run: bash scripts/test-publish-plugin.sh
set -u
HERE="$(cd "$(dirname "$0")/.." && pwd)"
SCRIPT="$HERE/plugins/handsonai/skills/publishing-plugins/scripts/publish-plugin.sh"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
pass=0; fail=0
ok()   { pass=$((pass + 1)); }
bad()  { fail=$((fail + 1)); printf 'FAIL: %s\n' "$*"; }
expect_contains() { case "$1" in *"$2"*) ok ;; *) bad "$3 — expected '$2' in: $1" ;; esac; }
expect_absent()   { case "$1" in *"$2"*) bad "$3 — did not expect '$2' in: $1" ;; *) ok ;; esac; }
expect_code()     { [ "$1" = "$2" ] && ok || bad "$3 — expected exit $2, got $1"; }
run() { bash "$SCRIPT" "$@" 2>&1; }
g() { git -C "$1" -c user.name=t -c user.email=t@t "${@:2}" >/dev/null 2>&1; }
release() { g "$PLG" add -A; g "$PLG" commit -m "$1"; }

SRC="$TMP/my source"; PLG="$TMP/team-plugins"
mkdir -p "$SRC/.claude/skills/recap" "$SRC/.claude/skills/proposal/references" "$SRC/.claude/skills/ingest" \
         "$SRC/.claude/skills/notes-only" "$SRC/.claude/agents" "$PLG"
printf -- '---\nname: recap\n---\nA\n' > "$SRC/.claude/skills/recap/SKILL.md"
printf -- '---\nname: proposal\n---\nB\n' > "$SRC/.claude/skills/proposal/SKILL.md"
printf 'ref\n' > "$SRC/.claude/skills/proposal/references/tone.md"
printf 'junk\n' > "$SRC/.claude/skills/proposal/.DS_Store"
mkdir -p "$SRC/.claude/skills/proposal/evals"; printf 'e\n' > "$SRC/.claude/skills/proposal/evals/run.json"
printf -- '---\nname: ingest\n---\nI\n' > "$SRC/.claude/skills/ingest/SKILL.md"
printf 'no skill file\n' > "$SRC/.claude/skills/notes-only/README.md"
printf -- '---\nname: helper\n---\nH\n' > "$SRC/.claude/agents/helper.md"
git init -q "$SRC"; g "$SRC" add -A; g "$SRC" commit -m init
git init -q "$PLG"

# --- setup and plugins ---
out="$(run setup --plugin-repo "$PLG" --source "$SRC" --owner "Pat Lee")"
expect_contains "$out" "skills=.claude/skills agents=.claude/agents" "default .claude layout"
expect_contains "$out" "marketplace=team-plugins" "marketplace named after the folder"
for f in .claude-plugin/marketplace.json release-plan.txt README.md .gitignore; do [ -f "$PLG/$f" ] && ok || bad "setup missing $f"; done
grep -qx '.publish-plugin' "$PLG/.gitignore" && ok || bad "settings not gitignored"
expect_contains "$(run add-plugin --plugin-repo "$PLG" --name "Bad Name")" "lowercase words joined by hyphens" "bad plugin name"
expect_contains "$(run add-plugin --plugin-repo "$PLG" --name sales --description 'For the sales team')" "added plugin sales" "add sales"
expect_contains "$(run add-plugin --plugin-repo "$PLG" --name ops)" "added plugin ops" "add ops"
grep -c '"source": "./plugins/' "$PLG/.claude-plugin/marketplace.json" | grep -qx 2 && ok || bad "marketplace should list 2 plugins"

# --- undecided items block a release until the person decides ---
out="$(run check --plugin-repo "$PLG")"; code=$?
expect_code "$code" 2 "check with undecided items"
expect_contains "$out" "UNDECIDED" "undecided reported"
expect_contains "$out" "skill recap" "recap undecided"
expect_absent  "$out" "notes-only" "folder without SKILL.md is not a skill"
expect_contains "$(run assign --plugin-repo "$PLG" nope skill recap)" "no plugin named nope" "assign to missing plugin"
expect_contains "$(run assign --plugin-repo "$PLG" sales skill nothing)" "no skill named nothing" "assign missing skill"
run assign --plugin-repo "$PLG" sales skill recap >/dev/null
run assign --plugin-repo "$PLG" ops skill recap >/dev/null      # one skill in two plugins
run assign --plugin-repo "$PLG" sales skill proposal >/dev/null
run assign --plugin-repo "$PLG" sales agent helper >/dev/null
expect_contains "$(run assign --plugin-repo "$PLG" none skill ingest)" "recorded: none skill ingest" "keep ingest out"
expect_contains "$(run assign --plugin-repo "$PLG" sales skill ingest)" "marked none" "none and a plugin can't both hold it"
expect_absent "$(run list --plugin-repo "$PLG")" "undecided:" "nothing undecided after assigning"

# --- first release ---
out="$(run copy --plugin-repo "$PLG")"
expect_contains "$out" "plugin sales:" "sales changes listed"
expect_contains "$out" "added skill: proposal" "proposal added to sales"
expect_contains "$out" "added agent: helper" "agent added (no .md in the name)"
expect_contains "$out" "suggested bump: first" "first release"
[ -d "$PLG/plugins/ops/skills/recap" ] && ok || bad "recap not in ops"
[ ! -e "$PLG/plugins/ops/skills/proposal" ] && ok || bad "proposal leaked into ops"
[ ! -e "$PLG/plugins/sales/skills/ingest" ] && ok || bad "ingest (none) was released"
[ ! -e "$PLG/plugins/sales/skills/proposal/.DS_Store" ] && ok || bad ".DS_Store shipped"
[ -f "$PLG/plugins/sales/skills/proposal/evals/run.json" ] && ok || bad "a folder inside the skill (evals) was dropped"
[ -f "$PLG/plugins/sales/skills/proposal/references/tone.md" ] && ok || bad "references not copied"
[ ! -e "$PLG/plugins/ops/agents" ] && ok || bad "empty agents folder left in ops"
expect_contains "$(run bump --plugin-repo "$PLG" sales first)" "sales version: 0.0.0 -> 1.0.0" "bump sales"
expect_contains "$(run bump --plugin-repo "$PLG" ops first)" "ops version: 0.0.0 -> 1.0.0" "bump ops"
c="$(grep -c '"version": "1.0.0"' "$PLG/.claude-plugin/marketplace.json")"; [ "$c" = "2" ] && ok || bad "marketplace versions not rebuilt ($c)"
release v1
out="$(run check --plugin-repo "$PLG")"; expect_code $? 0 "check passes after release: $out"
expect_contains "$(run copy --plugin-repo "$PLG")" "no changes since the last release" "no changes"

# --- patch only touches the plugins that hold the changed skill ---
printf 'A2\n' >> "$SRC/.claude/skills/proposal/SKILL.md"; g "$SRC" commit -am edit
out="$(run copy --plugin-repo "$PLG")"
expect_contains "$out" "updated skill: proposal" "edit detected"
expect_contains "$out" "suggested bump: patch" "patch suggested"
expect_absent  "$out" "plugin ops:" "ops untouched by a sales-only skill"
run bump --plugin-repo "$PLG" sales patch >/dev/null; release v101
grep -q '"version": "1.0.1"' "$PLG/plugins/sales/.claude-plugin/plugin.json" && ok || bad "sales not 1.0.1"
grep -q '"version": "1.0.0"' "$PLG/plugins/ops/.claude-plugin/plugin.json" && ok || bad "ops should stay 1.0.0"

# --- a shared skill changes both plugins ---
printf 'A3\n' >> "$SRC/.claude/skills/recap/SKILL.md"; g "$SRC" commit -am recap
out="$(run copy --plugin-repo "$PLG")"
expect_contains "$out" "plugin sales:" "shared edit hits sales"
expect_contains "$out" "plugin ops:" "shared edit hits ops"
run bump --plugin-repo "$PLG" sales patch >/dev/null; run bump --plugin-repo "$PLG" ops patch >/dev/null; release shared

# --- a new skill is undecided until assigned; then a minor release ---
mkdir -p "$SRC/.claude/skills/pricing"; printf -- '---\nname: pricing\n---\nP\n' > "$SRC/.claude/skills/pricing/SKILL.md"; g "$SRC" add -A; g "$SRC" commit -m add
out="$(run check --plugin-repo "$PLG")"; expect_code $? 2 "new skill needs a decision"
expect_contains "$out" "skill pricing" "pricing undecided"
expect_absent "$(run copy --plugin-repo "$PLG")" "pricing" "undecided skill is not released"
run assign --plugin-repo "$PLG" ops skill pricing >/dev/null
out="$(run check --plugin-repo "$PLG")"; expect_code $? 0 "a release-plan change isn't a hand edit: $out"
printf 'hand edit\n' >> "$PLG/README.md"
out="$(run check --plugin-repo "$PLG")"; expect_code $? 2 "a hand edit is flagged"
expect_contains "$out" "changes made by hand" "hand edit reported"
g "$PLG" checkout -- README.md
out="$(run copy --plugin-repo "$PLG")"
expect_contains "$out" "added skill: pricing" "pricing added to ops"
expect_contains "$out" "suggested bump: minor" "minor suggested"
run bump --plugin-repo "$PLG" ops minor >/dev/null; release add

# --- taking a skill out of a plugin is a major release for that plugin ---
run unassign --plugin-repo "$PLG" sales agent helper >/dev/null
run assign --plugin-repo "$PLG" none agent helper >/dev/null
out="$(run copy --plugin-repo "$PLG")"
expect_contains "$out" "removed agent: helper" "removal detected"
expect_contains "$out" "suggested bump: major" "major suggested"
expect_contains "$(run bump --plugin-repo "$PLG" sales major)" "1.0.2 -> 2.0.0" "major bump"
release remove

# --- deleting a skill from the source that a plan still lists ---
rm -rf "$SRC/.claude/skills/pricing"; g "$SRC" add -A; g "$SRC" commit -m del
out="$(run copy --plugin-repo "$PLG")"
expect_contains "$out" "MISSING skill pricing" "missing source reported"
expect_contains "$out" "removed skill: pricing" "removed from ops"
g "$PLG" checkout -- .; g "$PLG" clean -fd
run unassign --plugin-repo "$PLG" ops skill pricing >/dev/null; g "$PLG" add -A; g "$PLG" commit -m plan

# --- source changes not yet saved ---
printf 'draft\n' >> "$SRC/.claude/skills/recap/SKILL.md"
out="$(run check --plugin-repo "$PLG")"; expect_code $? 2 "unsaved source"
expect_contains "$out" "not yet saved in its history" "unsaved source reported"
g "$SRC" checkout -- .

# --- secrets in a released skill stop everything, before anything else ---
printf 'KEY=1\n' > "$SRC/.claude/skills/recap/.env"
out="$(run check --plugin-repo "$PLG")"; expect_code $? 3 "secret stops check"
expect_absent "$out" "not yet saved" "secret reported before unsaved changes"
out="$(run copy --plugin-repo "$PLG")"; expect_code $? 3 "secret stops copy"
[ ! -e "$PLG/plugins/sales/skills/recap/.env" ] && ok || bad "secret was copied"
rm "$SRC/.claude/skills/recap/.env"
# a secret in a skill that stays out ("none") doesn't block
printf 'KEY=1\n' > "$SRC/.claude/skills/ingest/.env"
out="$(run check --plugin-repo "$PLG")"; expect_absent "$out" "SECRET" "secret in an unreleased skill doesn't block"
rm "$SRC/.claude/skills/ingest/.env"

# --- a plugin someone already started at 0.x is adopted ---
mkdir -p "$PLG/plugins/legacy/.claude-plugin"
printf '{\n  "name": "legacy",\n  "description": "Old",\n  "version": "0.1.0"\n}\n' > "$PLG/plugins/legacy/.claude-plugin/plugin.json"
expect_contains "$(run add-plugin --plugin-repo "$PLG" --name legacy)" "already exists (version 0.1.0)" "existing plugin kept"
run assign --plugin-repo "$PLG" legacy skill recap >/dev/null
expect_contains "$(run copy --plugin-repo "$PLG")" "suggested bump: first" "0.x counts as unreleased"
expect_contains "$(run bump --plugin-repo "$PLG" legacy 3.0.0)" "-> 3.0.0" "explicit version"
g "$PLG" checkout -- .; g "$PLG" clean -fd; rm -rf "$PLG/plugins/legacy"; run unassign --plugin-repo "$PLG" legacy skill recap >/dev/null

# --- guards for the mistakes real people make ---
expect_contains "$(bash "$SCRIPT" check 2>&1)" "--plugin-repo is required" "plugin repo must be named"
expect_contains "$(run setup --plugin-repo "$SRC" --source "$SRC")" "two different folders" "same folder refused"
mkdir -p "$SRC/inner-plugins"
expect_contains "$(run setup --plugin-repo "$SRC/inner-plugins" --source "$SRC")" "inside the source repository" "nested plugin repo refused"
rmdir "$SRC/inner-plugins"
mkdir -p "$TMP/empty-src" "$TMP/empty-plg"; git init -q "$TMP/empty-plg"
expect_contains "$(run setup --plugin-repo "$TMP/empty-plg" --source "$TMP/empty-src")" "no skills or agents found" "empty source refused"
# a skill folder with spaces is reported for renaming, and can't be assigned
mkdir -p "$SRC/.claude/skills/Call Notes"; printf -- '---\nname: call-notes\n---\n' > "$SRC/.claude/skills/Call Notes/SKILL.md"; g "$SRC" add -A; g "$SRC" commit -m sp
out="$(run check --plugin-repo "$PLG")"; expect_contains "$out" "RENAME" "bad folder name reported"
rm -rf "$SRC/.claude/skills/Call Notes"; g "$SRC" add -A; g "$SRC" commit -m unsp
# plugin names must match exactly (case)
expect_contains "$(run assign --plugin-repo "$PLG" Sales skill recap)" "no plugin named Sales" "plugin name case enforced"
# versions only go up, and a re-run never bumps twice
expect_contains "$(run bump --plugin-repo "$PLG" sales 1.0.0)" "must be higher" "backwards version refused"
expect_contains "$(run bump --plugin-repo "$PLG" sales 1.2.3.4)" "bump must be" "malformed version refused"
printf 'A4\n' >> "$SRC/.claude/skills/proposal/SKILL.md"; g "$SRC" commit -am e4
run copy --plugin-repo "$PLG" >/dev/null
a="$(run bump --plugin-repo "$PLG" sales patch)"; b="$(run bump --plugin-repo "$PLG" sales patch)"
expect_contains "$b" "2.0.0 -> 2.0.1" "re-running bump counts from the last release"
out="$(run check --plugin-repo "$PLG")"; expect_absent "$out" "made by hand" "copy output isn't a hand edit"
g "$PLG" checkout -- .; g "$PLG" clean -fd
# a marketplace file in someone else's layout is never rewritten
mkdir -p "$TMP/foreign/.claude-plugin"; git init -q "$TMP/foreign"
printf '{"name":"x","owner":{"name":"y"},"plugins":[]}\n' > "$TMP/foreign/.claude-plugin/marketplace.json"
expect_contains "$(run setup --plugin-repo "$TMP/foreign" --source "$SRC")" "Nothing was changed" "foreign marketplace refused"
grep -q '"owner"' "$TMP/foreign/.claude-plugin/marketplace.json" && ok || bad "foreign marketplace was rewritten"
# a plugin folder that isn't its own Git repository
mkdir -p "$TMP/outer/plugins-here"; git init -q "$TMP/outer"
expect_contains "$(run setup --plugin-repo "$TMP/outer/plugins-here" --source "$SRC")" "inside another Git repository" "nested repo refused at setup"
# a source that isn't a Git repository can't be released from
mkdir -p "$TMP/nogit/.claude/skills/s" "$TMP/nogit-plg"; printf -- '---\nname: s\n---\n' > "$TMP/nogit/.claude/skills/s/SKILL.md"; git init -q "$TMP/nogit-plg"
run setup --plugin-repo "$TMP/nogit-plg" --source "$TMP/nogit" >/dev/null
out="$(run check --plugin-repo "$TMP/nogit-plg")"; expect_code $? 2 "source without Git"
expect_contains "$out" "isn't a Git repository" "source without Git reported"
# README carries the real GitHub name when the plugin repo has one
mkdir -p "$TMP/gh-plg"; git init -q "$TMP/gh-plg"; git -C "$TMP/gh-plg" remote add origin https://github.com/acme/acme-plugins.git
run setup --plugin-repo "$TMP/gh-plg" --source "$SRC" >/dev/null
grep -q 'acme/acme-plugins' "$TMP/gh-plg/README.md" && ok || bad "README not filled from origin"

# --- review fixes: 'first' refused once released; symlinks refused ---
expect_contains "$(run bump --plugin-repo "$PLG" sales first)" "already been released" "first refused after release"
ln -s /etc/hosts "$SRC/.claude/skills/recap/link.txt"
out="$(run check --plugin-repo "$PLG")"; expect_code $? 3 "symlink stops check"
expect_contains "$out" "a shortcut" "symlink reported"
rm "$SRC/.claude/skills/recap/link.txt"

# --- top-level skills/ and agents/ still work when that's what the source has ---
S2="$TMP/flat"; P2="$TMP/flat-plugins"; mkdir -p "$S2/skills/a" "$S2/agents" "$P2"
printf -- '---\nname: a\n---\n' > "$S2/skills/a/SKILL.md"; git init -q "$P2"
expect_contains "$(run setup --plugin-repo "$P2" --source "$S2")" "skills=skills agents=agents" "flat layout detected"

# --- an existing plugin repository with a plugin this skill doesn't manage is never rewritten ---
EX="$TMP/existing-root"; mkdir -p "$EX/.claude-plugin"; git init -q "$EX"
printf '{\n  "name": "team-skills",\n  "version": "0.1.0"\n}\n' > "$EX/.claude-plugin/plugin.json"
printf '{\n  "name": "team",\n  "owner": {"name": "Pat"},\n  "plugins": [{"name": "team-skills", "source": "./"}]\n}\n' > "$EX/.claude-plugin/marketplace.json"
cp "$EX/.claude-plugin/marketplace.json" "$TMP/ex-before.json"
expect_contains "$(run setup --plugin-repo "$EX" --source "$SRC")" "doesn't manage" "root-level plugin refused"
cmp -s "$EX/.claude-plugin/marketplace.json" "$TMP/ex-before.json" && ok || bad "existing marketplace was changed"
EX2="$TMP/existing-remote"; mkdir -p "$EX2/.claude-plugin"; git init -q "$EX2"
printf '{\n  "name": "team",\n  "owner": {"name": "Pat"},\n  "plugins": [\n    {"name": "x", "source": {"source": "github", "repo": "a/b"}}\n  ]\n}\n' > "$EX2/.claude-plugin/marketplace.json"
expect_contains "$(run setup --plugin-repo "$EX2" --source "$SRC")" "doesn't manage" "remote-source plugin refused"

# --- adversarial review fixes ---
R2="$TMP/r2"; mkdir -p "$R2"
mk_src() { # dir: a source repo with skills named like clutter, plus an agents README
  mkdir -p "$1/.claude/skills/evals" "$1/.claude/skills/iteration-planner/references" "$1/.claude/skills/team-workspace" "$1/.claude/agents"
  for k in evals iteration-planner team-workspace; do printf -- "---\nname: $k\n---\n" > "$1/.claude/skills/$k/SKILL.md"; done
  printf 'notes\n' > "$1/.claude/skills/iteration-planner/references/iteration-1-notes.md"
  printf 'junk\n' > "$1/.claude/skills/evals/.DS_Store"
  printf '# About these agents\n' > "$1/.claude/agents/README.md"
  git init -q "$1"; g "$1" add -A; g "$1" commit -m init
}
mk_src "$R2/src"
# a plugin repo named "plugins", with a tracked .gitignore that has no trailing newline
mkdir -p "$R2/plugins"; git init -q "$R2/plugins"; printf 'node_modules' > "$R2/plugins/.gitignore"; g "$R2/plugins" add -A; g "$R2/plugins" commit -m start
run setup --plugin-repo "$R2/plugins" --source "$R2/src" >/dev/null
grep -qx 'node_modules' "$R2/plugins/.gitignore" && grep -qx '.publish-plugin' "$R2/plugins/.gitignore" && ok || bad ".gitignore without trailing newline was merged into one line"
grep -q '"name": "plugins"' "$R2/plugins/.claude-plugin/marketplace.json" && ok || bad "a repo named plugins lost its marketplace name"
run add-plugin --plugin-repo "$R2/plugins" --name team --description $'Line one\nline "two"\tand a \\ backslash' >/dev/null
python3 -m json.tool "$R2/plugins/.claude-plugin/marketplace.json" >/dev/null && python3 -m json.tool "$R2/plugins/plugins/team/.claude-plugin/plugin.json" >/dev/null && ok || bad "newline/tab in a description made invalid JSON"
expect_absent "$(run check --plugin-repo "$R2/plugins")" "agent README" "agents README.md isn't treated as an agent"
for k in evals iteration-planner team-workspace; do run assign --plugin-repo "$R2/plugins" team skill $k >/dev/null; done
expect_contains "$(run copy --plugin-repo "$R2/plugins")" "copied 3 skill(s)" "clutter-like skill names all ship"
[ -f "$R2/plugins/plugins/team/skills/iteration-planner/references/iteration-1-notes.md" ] && ok || bad "a reference file named iteration-* was dropped"
[ ! -e "$R2/plugins/plugins/team/skills/evals/.DS_Store" ] && ok || bad ".DS_Store inside a skill shipped"
out="$(run check --plugin-repo "$R2/plugins")"; expect_absent "$out" "made by hand" "a tracked .gitignore changed by setup isn't a hand edit"
run bump --plugin-repo "$R2/plugins" team first >/dev/null; g "$R2/plugins" add -A; g "$R2/plugins" commit -m v1
# Windows line endings in the release plan
sed 's/$/\r/' "$R2/plugins/release-plan.txt" > "$TMP/crlf" && mv "$TMP/crlf" "$R2/plugins/release-plan.txt"
out="$(run check --plugin-repo "$R2/plugins")"; expect_absent "$out" "MISSING" "CRLF plan isn't read as missing items"; expect_absent "$out" "UNDECIDED" "CRLF plan isn't read as undecided"
expect_contains "$(run copy --plugin-repo "$R2/plugins")" "no changes since the last release" "CRLF plan releases nothing new"
expect_contains "$(run unassign --plugin-repo "$R2/plugins" team skill evals)" "removed" "unassign works on a CRLF plan"
g "$R2/plugins" checkout -- .
# a skill already in the plugin that the plan doesn't name
mkdir -p "$R2/plugins/plugins/team/skills/old-skill"; printf -- '---\nname: old-skill\n---\n' > "$R2/plugins/plugins/team/skills/old-skill/SKILL.md"; g "$R2/plugins" add -A; g "$R2/plugins" commit -m old
expect_contains "$(run check --plugin-repo "$R2/plugins")" "ONLY IN PLUGIN" "plugin-only skill reported before it's removed"
g "$R2/plugins" rm -rq plugins/team/skills/old-skill; g "$R2/plugins" commit -m rmold
# a release saved but not sent to GitHub
git init -q --bare "$R2/gh.git"; g "$R2/plugins" remote add origin "$R2/gh.git"; g "$R2/plugins" push -u origin HEAD
printf 'x\n' >> "$R2/plugins/README.md"; g "$R2/plugins" commit -am local-only
expect_contains "$(run check --plugin-repo "$R2/plugins")" "UNPUSHED" "an unsent release is reported"
expect_contains "$(run list --plugin-repo "$R2/plugins")" "not yet on GitHub" "list marks an unsent release"
g "$R2/plugins" push
# leftovers from an interrupted run are cleaned, not shipped
touch "$R2/plugins/.claude-plugin/marketplace.json.tmp.12345"
run check --plugin-repo "$R2/plugins" >/dev/null; [ ! -e "$R2/plugins/.claude-plugin/marketplace.json.tmp.12345" ] && ok || bad "a leftover temp file survived"
# secrets: names, contents, examples
printf '{"token": "x"}\n' > "$R2/src/.claude/skills/evals/token.json"
expect_code "$(run check --plugin-repo "$R2/plugins" >/dev/null; echo $?)" 3 "a token.json blocks the release"
rm "$R2/src/.claude/skills/evals/token.json"
# placeholders and ordinary names don't block
printf -- '---\nname: evals\n---\nYour Slack token starts with xoxb-your-bot-token-here. AWS docs use AKIAIOSFODNN7EXAMPLE. Anthropic keys look like sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxx. A PEM file starts with -----BEGIN RSA PRIVATE KEY-----.\n' > "$R2/src/.claude/skills/evals/SKILL.md"
printf 'def count_tokens(): pass\n' > "$R2/src/.claude/skills/evals/count_tokens.py"
printf 'checklist\n' > "$R2/src/.claude/skills/evals/credentials-checklist.md"
g "$R2/src" add -A; g "$R2/src" commit -m docs
expect_absent "$(run check --plugin-repo "$R2/plugins")" "SECRET" "placeholders and ordinary names don't block"
# a real-looking key does, with its line number
# Built at run time so no token-shaped text sits in this file (GitHub push protection).
printf 'slack: xox%s-%s-%s\n' 'b' '4815162342' 'ABCDEFghijkl9876' > "$R2/src/.claude/skills/evals/settings.yaml"
out="$(run check --plugin-repo "$R2/plugins")"; expect_contains "$out" "settings.yaml:1" "a real-looking key is reported with its line"
rm "$R2/src/.claude/skills/evals/settings.yaml"
printf 'key: sk-%s-api03-%s\n' 'ant' 'AbCdEfGhIjKlMnOpQrStUvWxYz012345' > "$R2/src/.claude/skills/evals/config.yaml"
expect_code "$(run check --plugin-repo "$R2/plugins" >/dev/null; echo $?)" 3 "a key pasted into a file blocks the release"
rm "$R2/src/.claude/skills/evals/config.yaml"
printf 'API_KEY=\n' > "$R2/src/.claude/skills/evals/.env.example"; g "$R2/src" add -A; g "$R2/src" commit -m example
expect_absent "$(run check --plugin-repo "$R2/plugins")" "SECRET" "an .env.example doesn't block"
# a hand edit to a released plugin.json is an undo, not a new repository
g "$R2/plugins" add -A; g "$R2/plugins" commit -q -m pre-edit
sed 's/"description": "[^"]*"/"description": "edited by hand"/' "$R2/plugins/plugins/team/.claude-plugin/plugin.json" > "$TMP/pj" && mv "$TMP/pj" "$R2/plugins/plugins/team/.claude-plugin/plugin.json"
out="$(run check --plugin-repo "$R2/plugins")"; expect_code $? 2 "hand edit exits 2"; expect_contains "$out" "changes made by hand" "hand edit reported as a hand edit"
g "$R2/plugins" checkout -- .
# author before name in a hand-written plugin.json
mkdir -p "$R2/plugins/plugins/auth/.claude-plugin"
printf '{\n  "author": {\n    "name": "Pat"\n  },\n  "name": "auth",\n  "version": "0.1.0"\n}\n' > "$R2/plugins/plugins/auth/.claude-plugin/plugin.json"
expect_contains "$(run add-plugin --plugin-repo "$R2/plugins" --name auth)" "already exists" "author-before-name plugin.json is read correctly"
# an empty plugin is called out
expect_contains "$(run copy --plugin-repo "$R2/plugins")" "EMPTY PLUGIN auth" "empty plugin warned"
g "$R2/plugins" checkout -- .; g "$R2/plugins" clean -fdq

# a marketplace someone else edited: renamed entry, extra key, mismatched version
M3="$TMP/m3"; mkdir -p "$M3/plugins/sales/.claude-plugin" "$M3/.claude-plugin"; git init -q "$M3"
printf '{\n  "name": "sales",\n  "description": "d",\n  "version": "1.2.0"\n}\n' > "$M3/plugins/sales/.claude-plugin/plugin.json"
printf '{\n  "name": "m3",\n  "owner": {\n    "name": "o"\n  },\n  "plugins": [\n    {\n      "name": "sales-tools",\n      "source": "./plugins/sales",\n      "version": "1.4.0",\n      "category": "x"\n    }\n  ],\n  "metadata": {"version": "3"}\n}\n' > "$M3/.claude-plugin/marketplace.json"
cp "$M3/.claude-plugin/marketplace.json" "$TMP/m3-before"
expect_contains "$(run setup --plugin-repo "$M3" --source "$SRC")" "Nothing was changed" "hand-edited marketplace refused"
cmp -s "$M3/.claude-plugin/marketplace.json" "$TMP/m3-before" && ok || bad "hand-edited marketplace was changed"

# --- 10.1.2: new repositories start on main ---
R4="$TMP/r4"; mk_src "$R4/src"; mkdir -p "$R4/new-plugins"; git -C "$R4/new-plugins" -c init.defaultBranch=master init -q
run setup --plugin-repo "$R4/new-plugins" --source "$R4/src" >/dev/null
[ "$(git -C "$R4/new-plugins" symbolic-ref --short HEAD)" = "main" ] && ok || bad "a new plugin repository didn't start on main"
# a repository that already has releases keeps its branch
b_before="$(git -C "$R2/plugins" symbolic-ref --short HEAD)"; run setup --plugin-repo "$R2/plugins" --source "$R2/src" >/dev/null
[ "$(git -C "$R2/plugins" symbolic-ref --short HEAD)" = "$b_before" ] && ok || bad "setup renamed the branch of a released repository"
g "$R2/plugins" checkout -- .

# --- 10.1.2: the source version a release names must be on GitHub ---
run add-plugin --plugin-repo "$R4/new-plugins" --name team >/dev/null
run assign --plugin-repo "$R4/new-plugins" team skill evals >/dev/null
for k in iteration-planner team-workspace; do run assign --plugin-repo "$R4/new-plugins" none skill $k >/dev/null; done
out="$(run check --plugin-repo "$R4/new-plugins")"; expect_contains "$out" "no GitHub connection" "a source with no GitHub connection is noted"
expect_contains "$out" "ready to publish" "a note alone doesn't block"
git init -q --bare "$R4/src.git"; g "$R4/src" remote add origin "$R4/src.git"; g "$R4/src" push -u origin HEAD
expect_contains "$(run check --plugin-repo "$R4/new-plugins")" "ready to publish" "a pushed source is ready"
printf 'more\n' >> "$R4/src/.claude/skills/evals/SKILL.md"; g "$R4/src" commit -am local
out="$(run check --plugin-repo "$R4/new-plugins")"; code=$?
expect_code "$code" 2 "an unpushed source commit stops the release"
expect_contains "$out" "SOURCE UNPUSHED" "an unpushed source commit is named"
expect_contains "$out" "$(git -C "$R4/src" rev-parse --short HEAD)" "the unpushed commit is identified"
g "$R4/src" push
expect_contains "$(run check --plugin-repo "$R4/new-plugins")" "ready to publish" "pushing the source clears it"
# a source with no upstream branch, but whose commit is on GitHub under another branch, is fine
g "$R4/src" checkout -b side; out="$(run check --plugin-repo "$R4/new-plugins")"; expect_absent "$out" "SOURCE UNPUSHED" "a commit already on GitHub isn't flagged"
g "$R4/src" commit --allow-empty -m side-only; expect_contains "$(run check --plugin-repo "$R4/new-plugins")" "SOURCE UNPUSHED" "a new branch never sent is flagged"
g "$R4/src" checkout main 2>/dev/null || g "$R4/src" checkout master

# --- 10.1.2: describe changes a plugin's description everywhere ---
out="$(run describe --plugin-repo "$R4/new-plugins" team --description 'Meeting and research skills for the sales team.')"
expect_contains "$out" "team description: Meeting and research skills for the sales team." "describe reports the new description"
grep -q '"description": "Meeting and research skills for the sales team."' "$R4/new-plugins/plugins/team/.claude-plugin/plugin.json" && ok || bad "plugin.json description not changed"
grep -q '"description": "Meeting and research skills for the sales team."' "$R4/new-plugins/.claude-plugin/marketplace.json" && ok || bad "marketplace description not rebuilt"
run describe --plugin-repo "$R4/new-plugins" team --description $'Quotes "x", a \\ and & /slash\nnewline' >/dev/null
python3 -m json.tool "$R4/new-plugins/plugins/team/.claude-plugin/plugin.json" >/dev/null && python3 -m json.tool "$R4/new-plugins/.claude-plugin/marketplace.json" >/dev/null && ok || bad "describe with special characters made invalid JSON"
[ "$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["description"])' "$R4/new-plugins/plugins/team/.claude-plugin/plugin.json")" = 'Quotes "x", a \ and & /slash newline' ] && ok || bad "describe didn't keep special characters"
[ "$(grep -c '"version"' "$R4/new-plugins/plugins/team/.claude-plugin/plugin.json")" = "1" ] && grep -q '"name": "team"' "$R4/new-plugins/plugins/team/.claude-plugin/plugin.json" && ok || bad "describe damaged other fields"
expect_contains "$(run list --plugin-repo "$R4/new-plugins")" 'description: Quotes \"x\"' "list shows each plugin's description"
expect_contains "$(run describe --plugin-repo "$R4/new-plugins" nobody --description x)" "no plugin named nobody" "describe an unknown plugin refused"
expect_contains "$(run describe --plugin-repo "$R4/new-plugins" team)" "needs --description" "describe without text refused"

# --- Claude's own validator accepts what the script writes (when Claude Code is installed) ---
if command -v claude >/dev/null 2>&1; then
  out="$(claude plugin validate "$PLG" 2>&1)"; expect_contains "$out" "Validation passed" "marketplace validates"
  out="$(claude plugin validate "$PLG/plugins/sales" 2>&1)"; expect_contains "$out" "Validation passed" "plugin validates"
fi

printf '%d passed, %d failed\n' "$pass" "$fail"
[ "$fail" = "0" ]
