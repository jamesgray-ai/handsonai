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
[ ! -e "$PLG/plugins/sales/skills/proposal/evals" ] && ok || bad "evals shipped"
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
expect_contains "$(run setup --plugin-repo "$TMP/foreign" --source "$SRC")" "isn't in the layout" "foreign marketplace refused"
grep -q '"owner"' "$TMP/foreign/.claude-plugin/marketplace.json" && ok || bad "foreign marketplace was rewritten"
# a plugin folder that isn't its own Git repository
mkdir -p "$TMP/outer/plugins-here"; git init -q "$TMP/outer"
run setup --plugin-repo "$TMP/outer/plugins-here" --source "$SRC" >/dev/null 2>&1
expect_contains "$(run check --plugin-repo "$TMP/outer/plugins-here")" "inside another Git repository" "nested repo detected"
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

# --- Claude's own validator accepts what the script writes (when Claude Code is installed) ---
if command -v claude >/dev/null 2>&1; then
  out="$(claude plugin validate "$PLG" 2>&1)"; expect_contains "$out" "Validation passed" "marketplace validates"
  out="$(claude plugin validate "$PLG/plugins/sales" 2>&1)"; expect_contains "$out" "Validation passed" "plugin validates"
fi

printf '%d passed, %d failed\n' "$pass" "$fail"
[ "$fail" = "0" ]
