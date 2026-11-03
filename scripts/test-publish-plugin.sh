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
run() { bash "$SCRIPT" "$@" 2>&1; }

g() { git -C "$1" -c user.name=t -c user.email=t@t "${@:2}" >/dev/null 2>&1; }

SRC="$TMP/my skills"; PLG="$TMP/plugin"
mkdir -p "$SRC/skills/alpha" "$SRC/skills/beta/references" "$SRC/skills/notes-only" "$SRC/agents" "$PLG"
printf -- '---\nname: alpha\n---\nA\n' > "$SRC/skills/alpha/SKILL.md"
printf -- '---\nname: beta\n---\nB\n' > "$SRC/skills/beta/SKILL.md"
printf 'ref\n' > "$SRC/skills/beta/references/r.md"
printf 'junk\n' > "$SRC/skills/beta/.DS_Store"
mkdir -p "$SRC/skills/beta/evals"; printf 'e\n' > "$SRC/skills/beta/evals/run.json"
printf 'no skill file\n' > "$SRC/skills/notes-only/README.md"
printf 'loose\n' > "$SRC/skills/README.md"
printf -- '---\nname: helper\n---\nH\n' > "$SRC/agents/helper.md"
git init -q "$SRC"; g "$SRC" add -A; g "$SRC" commit -m init
git init -q "$PLG"

# setup
out="$(run setup --plugin-repo "$PLG" --source "$SRC" --name my-team-skills --owner "Pat Lee")"
expect_contains "$out" "created .claude-plugin/marketplace.json" "setup creates marketplace"
[ -f "$PLG/plugins/my-team-skills/.claude-plugin/plugin.json" ] && ok || bad "plugin.json missing"
grep -qx '.publish-plugin' "$PLG/.gitignore" && ok || bad "settings not gitignored"
out="$(run setup --plugin-repo "$PLG" --source "$SRC" --name "Bad Name")"
expect_contains "$out" "lowercase words joined by hyphens" "setup rejects bad name"

# check before first release: plugin folder has unsaved files -> attention
out="$(run check --plugin-repo "$PLG")"; code=$?
[ "$code" = "2" ] && ok || bad "check should exit 2 on unsaved plugin changes (got $code)"
expect_contains "$out" "source commit:" "check reports source commit"

# first copy
out="$(run copy --plugin-repo "$PLG")"
expect_contains "$out" "copied 2 skill(s) and 1 agent(s)" "copies only folders with SKILL.md"
expect_contains "$out" "added skill: alpha" "alpha added"
expect_contains "$out" "added skill: beta" "beta added"
expect_contains "$out" "added agent: helper.md" "agent added"
expect_contains "$out" "suggested bump: first" "first release"
expect_absent  "$out" "notes-only" "folder without SKILL.md skipped"
[ ! -e "$PLG/plugins/my-team-skills/skills/beta/.DS_Store" ] && ok || bad ".DS_Store shipped"
[ ! -e "$PLG/plugins/my-team-skills/skills/beta/evals" ] && ok || bad "evals shipped"
[ -f "$PLG/plugins/my-team-skills/skills/beta/references/r.md" ] && ok || bad "references not copied"

out="$(run bump --plugin-repo "$PLG" first)"
expect_contains "$out" "0.0.0 -> 1.0.0" "first bump"
grep -q '"version": "1.0.0"' "$PLG/.claude-plugin/marketplace.json" && ok || bad "marketplace version"
g "$PLG" add -A; g "$PLG" commit -m v1
out="$(run check --plugin-repo "$PLG")"; code=$?
[ "$code" = "0" ] && ok || bad "check should pass after release (got $code): $out"
out="$(run copy --plugin-repo "$PLG")"
expect_contains "$out" "no changes since the last release" "re-copy with no changes"

# patch: edit only
printf 'A2\n' >> "$SRC/skills/alpha/SKILL.md"; g "$SRC" commit -am edit
out="$(run copy --plugin-repo "$PLG")"
expect_contains "$out" "updated skill: alpha" "edit detected"
expect_contains "$out" "suggested bump: patch" "patch suggested"
expect_contains "$(run bump --plugin-repo "$PLG" patch)" "1.0.0 -> 1.0.1" "patch bump"
g "$PLG" add -A; g "$PLG" commit -m v101

# minor: add
mkdir -p "$SRC/skills/gamma"; printf -- '---\nname: gamma\n---\n' > "$SRC/skills/gamma/SKILL.md"
g "$SRC" add -A; g "$SRC" commit -m add
out="$(run copy --plugin-repo "$PLG")"
expect_contains "$out" "added skill: gamma" "add detected"
expect_contains "$out" "suggested bump: minor" "minor suggested"
expect_contains "$(run bump --plugin-repo "$PLG" minor)" "1.0.1 -> 1.1.0" "minor bump"
g "$PLG" add -A; g "$PLG" commit -m v110

# major: remove (and an add in the same release)
rm -rf "$SRC/skills/beta"; mkdir -p "$SRC/skills/delta"; printf 'x\n' > "$SRC/skills/delta/SKILL.md"
g "$SRC" add -A; g "$SRC" commit -m remove
out="$(run copy --plugin-repo "$PLG")"
expect_contains "$out" "removed skill: beta" "removal detected"
expect_contains "$out" "added skill: delta" "add alongside removal"
expect_contains "$out" "suggested bump: major" "major wins"
expect_contains "$(run bump --plugin-repo "$PLG" major)" "1.1.0 -> 2.0.0" "major bump"
g "$PLG" add -A; g "$PLG" commit -m v200

# source with unsaved changes -> check exits 2
printf 'draft\n' >> "$SRC/skills/alpha/SKILL.md"
out="$(run check --plugin-repo "$PLG")"; code=$?
[ "$code" = "2" ] && ok || bad "unsaved source should exit 2 (got $code)"
expect_contains "$out" "not yet saved in its history" "unsaved source reported"
g "$SRC" checkout -- .

# secret in source -> check reports SECRET (exit 3) and never offers it as an unsaved change
printf 'KEY=1\n' > "$SRC/skills/alpha/.env"
out="$(run check --plugin-repo "$PLG")"; code=$?
[ "$code" = "3" ] && ok || bad "check with secret should exit 3 (got $code)"
expect_absent "$out" "not yet saved" "secret reported before unsaved changes"
rm "$SRC/skills/alpha/.env"

# secret in source -> copy refuses, nothing copied
printf 'KEY=1\n' > "$SRC/skills/alpha/.env"
out="$(run copy --plugin-repo "$PLG")"; code=$?
[ "$code" = "3" ] && ok || bad "secret should exit 3 (got $code)"
[ ! -e "$PLG/plugins/my-team-skills/skills/alpha/.env" ] && ok || bad "secret was copied"
rm "$SRC/skills/alpha/.env"

# version drift -> check flags it
sed 's/"version": "2.0.0"/"version": "9.9.9"/' "$PLG/.claude-plugin/marketplace.json" > "$TMP/m" \
  && mv "$TMP/m" "$PLG/.claude-plugin/marketplace.json"
out="$(run check --plugin-repo "$PLG")"
expect_contains "$out" "versions differ" "drift flagged"

[ -f "$PLG/README.md" ] && grep -q '/plugin install my-team-skills@my-team-skills' "$PLG/README.md" && ok || bad "README not created"
grep -q '"description"' "$PLG/.claude-plugin/marketplace.json" && ok || bad "marketplace description missing"

# a plugin someone already scaffolded (Plugin Dev, Claude's plugin creator) at 0.1.0 -> first release
P2="$TMP/scaffolded"; mkdir -p "$P2/plugins/acme/.claude-plugin"; git init -q "$P2"
printf '{\n  "name": "acme",\n  "version": "0.1.0"\n}\n' > "$P2/plugins/acme/.claude-plugin/plugin.json"
run setup --plugin-repo "$P2" --source "$SRC" --name acme >/dev/null
grep -q '"version": "0.1.0"' "$P2/plugins/acme/.claude-plugin/plugin.json" && ok || bad "setup overwrote existing plugin.json"
expect_contains "$(run copy --plugin-repo "$P2")" "suggested bump: first" "0.x treated as unreleased"

# plugin.json name that doesn't match the settings -> check refuses
sed 's/"name": "acme"/"name": "other"/' "$P2/plugins/acme/.claude-plugin/plugin.json" > "$TMP/pj" \
  && mv "$TMP/pj" "$P2/plugins/acme/.claude-plugin/plugin.json"
expect_contains "$(run check --plugin-repo "$P2")" "doesn't match the plugin name" "name mismatch caught"

# default layout: .claude/skills and .claude/agents are picked up without options
S3="$TMP/dotclaude"; P3="$TMP/dotclaude-plugin"
mkdir -p "$S3/.claude/skills/recap" "$S3/.claude/agents" "$P3"
printf -- '---\nname: recap\n---\n' > "$S3/.claude/skills/recap/SKILL.md"
printf -- '---\nname: helper\n---\n' > "$S3/.claude/agents/helper.md"
git init -q "$S3"; g "$S3" add -A; g "$S3" commit -m init; git init -q "$P3"
expect_contains "$(run setup --plugin-repo "$P3" --source "$S3" --name dot-skills)" "skills=.claude/skills agents=.claude/agents" ".claude layout detected"
out="$(run copy --plugin-repo "$P3")"
expect_contains "$out" "added skill: recap" ".claude skill copied"
expect_contains "$out" "added agent: helper.md" ".claude agent copied"

# explicit version
expect_contains "$(run bump --plugin-repo "$PLG" 3.0.0)" "-> 3.0.0" "explicit version"

printf '%d passed, %d failed\n' "$pass" "$fail"
[ "$fail" = "0" ]
