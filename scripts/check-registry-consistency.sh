#!/usr/bin/env bash
#
# check-registry-consistency.sh — the release gate for the AI Registry redesign. The
# registry system is held together by strings that never import each other: a schema
# template copied into two skill packages, an enum vocabulary repeated across a schema
# file and a bundle reference, a set of retired fields that must never reappear, and a
# lint rule list that must say the same thing in prose (registry-bundle.md) and in code
# (lint-registry.js). One drift and a skill writes a field the lint pass doesn't know to
# flag, or a template diverges from the copy a student actually downloads.
#
# This asserts that agreement. Run before shipping via sync-plugins.sh's preflight, or
# directly with --full once the doc migration (Batch E) lands.
#
# Usage:
#   ./scripts/check-registry-consistency.sh          # skip doc-dependent classes
#   ./scripts/check-registry-consistency.sh --full    # also check migrated docs

set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

FULL=0
[ "${1:-}" = "--full" ] && FULL=1

PASS=0
FAIL=0
SKIP=0

ok()   { echo "  ok    $1"; PASS=$((PASS + 1)); }
bad()  { echo "  FAIL  $1"; FAIL=$((FAIL + 1)); }
skip() { echo "  skip  $1 (needs --full)"; SKIP=$((SKIP + 1)); }

# $1 = description, $2 = file, $3 = literal string that must appear
must_contain() {
  if grep -qF -- "$3" "$2" 2>/dev/null; then ok "$1"; else bad "$1 — '$3' not found in $2"; fi
}

# $1 = description, $2 = file, $3 = literal string that must NOT appear
# A negative assertion has to prove the file exists first. Otherwise `2>/dev/null` turns
# "this file was renamed or deleted" into a pass — the check reports the property holds
# when there is nothing left to hold it.
must_not_contain() {
  [ -f "$2" ] || { bad "$1 — $2 does not exist"; return; }
  if grep -qF -- "$3" "$2"; then bad "$1 — '$3' should not be in $2"; else ok "$1"; fi
}

# Case-insensitive variants — used only where a heading/prose capitalization legitimately
# differs from the lowercase spelling used elsewhere (e.g. "Run log" vs "run log").
must_contain_i() {
  if grep -qFi -- "$3" "$2" 2>/dev/null; then ok "$1"; else bad "$1 — '$3' not found in $2 (case-insensitive)"; fi
}

echo "registry consistency"
[ "$FULL" -eq 1 ] && echo "(--full: doc-dependent classes included)" || echo "(doc-dependent classes skipped — pass --full once Batch E docs land)"
echo

# ---------------------------------------------------------------------------
echo "-- 1. byte-identity: canonical templates match their plugin-packaged copies --"
SCHEMA_CANON=registry-template/registry/SCHEMA.md
SCHEMA_COPY=plugins/handsonai/skills/scaffolding-registry/references/schema-template.md
ISLAND_CANON=registry-template/tools/data-island.schema.json
ISLAND_COPY=plugins/handsonai/skills/indexing-registry/references/data-island.schema.json
DASH_CANON=registry-template/tools/dashboard-template.html
DASH_COPY=plugins/handsonai/skills/indexing-registry/references/dashboard-template.html

if [ -f "$SCHEMA_CANON" ] && [ -f "$SCHEMA_COPY" ]; then
  cmp -s "$SCHEMA_CANON" "$SCHEMA_COPY" && ok "SCHEMA.md byte-identical to schema-template.md" \
    || bad "SCHEMA.md and schema-template.md have diverged — copy one over the other"
else
  bad "SCHEMA.md / schema-template.md — one of the two files is missing"
fi

if [ -f "$ISLAND_CANON" ] && [ -f "$ISLAND_COPY" ]; then
  cmp -s "$ISLAND_CANON" "$ISLAND_COPY" && ok "data-island.schema.json byte-identical across tools/ and the skill copy" \
    || bad "data-island.schema.json has diverged between tools/ and the skill copy"
else
  bad "data-island.schema.json — one of the two files is missing"
fi

if [ -f "$DASH_CANON" ] && [ -f "$DASH_COPY" ]; then
  cmp -s "$DASH_CANON" "$DASH_COPY" && ok "dashboard-template.html byte-identical across tools/ and the skill copy" \
    || bad "dashboard-template.html has diverged between tools/ and the skill copy"
else
  bad "dashboard-template.html — one of the two files is missing"
fi

# ---------------------------------------------------------------------------
echo
echo "-- 2. string agreement: enum vocabulary and frontmatter keys --"
BUNDLE=plugins/handsonai/skills/indexing-registry/references/registry-bundle.md
SETUP_PAGE=src/content/docs/builder-setup/ai-registry-setup.md

# Full vocabulary — enums plus generic frontmatter keys — must appear in schema-template.md,
# the single source of the schema.
declare -a VOCAB_FULL=(
  backlog under-development in-production retired
  step-driven goal-driven step-decomposed outcome-driven
  manual augmented automated
  deterministic guided autonomous
  stale_after okf_version "type:" "title:" "description:" "generated: {"
)
for s in "${VOCAB_FULL[@]}"; do
  must_contain "schema-template carries '$s'" "$SCHEMA_COPY" "$s"
done

# registry-bundle.md documents write rules and enums, not the generic schema field list —
# so it carries the enum/status vocabulary but not the bare frontmatter keys.
declare -a VOCAB_ENUMS=(
  backlog under-development in-production retired
  step-driven goal-driven step-decomposed outcome-driven
  manual augmented automated
  deterministic guided autonomous
  stale_after okf_version "generated: {"
)
for s in "${VOCAB_ENUMS[@]}"; do
  must_contain "registry-bundle.md carries '$s'" "$BUNDLE" "$s"
done

if [ "$FULL" -eq 1 ]; then
  for s in "${VOCAB_FULL[@]}"; do
    must_contain "setup page carries '$s'" "$SETUP_PAGE" "$s"
  done
else
  skip "setup page carries the full enum vocabulary"
fi

# ---------------------------------------------------------------------------
echo
echo "-- 3. retired-field discipline: banned fields stay out of every skill --"
declare -a TEN_SKILLS=(
  analyze deconstruct design build test run improve
  naming-workflows scaffolding-registry indexing-registry
)
declare -a RETIRED_FIELDS=(health last_run current_step next_review notion_url)

for skill in "${TEN_SKILLS[@]}"; do
  f="plugins/handsonai/skills/$skill/SKILL.md"
  for field in "${RETIRED_FIELDS[@]}"; do
    must_not_contain "$skill/SKILL.md has no '$field'" "$f" "$field"
  done
done
for field in "${RETIRED_FIELDS[@]}"; do
  must_not_contain "framework-agent.md has no '$field'" plugins/handsonai/agents/framework-agent.md "$field"
done

# registry-bundle.md is the one file allowed to mention these — it bans/maps them. It must
# not, however, write the retired `timestamp:` field outside its own ban line(s): every
# line naming `timestamp:` must also say it's banned/legacy, never present it as live.
if [ -f "$BUNDLE" ]; then
  TS_LINES="$(grep -F 'timestamp:' "$BUNDLE" 2>/dev/null || true)"
  if [ -z "$TS_LINES" ]; then
    bad "registry-bundle.md — expected a 'timestamp:' ban line, found none"
  elif echo "$TS_LINES" | grep -qviE 'legacy|banned'; then
    bad "registry-bundle.md — 'timestamp:' appears outside a banned/legacy context:"
    echo "$TS_LINES" | sed 's/^/         /'
  else
    ok "registry-bundle.md's 'timestamp:' mentions are all in a banned/legacy line"
  fi
else
  bad "registry-bundle.md does not exist"
fi

# ---------------------------------------------------------------------------
echo
echo "-- 4. docs invariants (retired terminology must not reappear in prose) --"
ALLOWLIST=(blog/ use-cases/example-gallery.md)

if [ "$FULL" -eq 1 ]; then
  RETIRED_TERMS_RE='workflow\.yaml|next_review|notion_url|manifest-resolution|notion-mirror|notion_workflow_url|notion_process_url|current_step'
  HITS="$(grep -rlE "$RETIRED_TERMS_RE" src/content/docs --include='*.md' --include='*.mdx' 2>/dev/null || true)"
  BAD_HITS=""
  while IFS= read -r hit; do
    [ -z "$hit" ] && continue
    rel="${hit#src/content/docs/}"
    allowed=0
    for a in "${ALLOWLIST[@]}"; do
      case "$rel" in
        "$a"*) allowed=1 ;;
      esac
    done
    [ "$allowed" -eq 0 ] && BAD_HITS="$BAD_HITS$hit"$'\n'
  done <<< "$HITS"
  if [ -z "$BAD_HITS" ]; then
    ok "no retired-terminology hits outside the allowlist"
  else
    bad "retired terminology found outside the allowlist:"
    echo "$BAD_HITS" | sed 's/^/         /'
  fi

  FRAMEWORK_SURFACE=(
    src/content/docs/ai-workflow-framework
    src/content/docs/builder-setup/ai-registry-setup.md
    src/content/docs/use-the-playbook/build
  )
  NOTION_HITS="$(grep -rl "Notion" "${FRAMEWORK_SURFACE[@]}" 2>/dev/null || true)"
  if [ -z "$NOTION_HITS" ]; then
    ok "no bare 'Notion' mentions on the framework surface"
  else
    bad "bare 'Notion' mentions found on the framework surface:"
    echo "$NOTION_HITS" | sed 's/^/         /'
  fi
else
  skip "docs invariants — retired terminology sweep"
  skip "docs invariants — bare 'Notion' sweep on the framework surface"
fi

# ---------------------------------------------------------------------------
echo
echo "-- 5. ownership rows: each skill's registry write matches its role --"
must_contain     "run: writes in-production"                  plugins/handsonai/skills/run/SKILL.md "in-production"
must_contain     "run: writes stale_after"                    plugins/handsonai/skills/run/SKILL.md "stale_after"
must_contain     "deconstruct: writes under-development"      plugins/handsonai/skills/deconstruct/SKILL.md "under-development"
must_contain     "deconstruct: writes definition_type"        plugins/handsonai/skills/deconstruct/SKILL.md "definition_type"
must_contain     "naming-workflows: writes backlog"           plugins/handsonai/skills/naming-workflows/SKILL.md "backlog"
must_contain     "naming-workflows: owns this process"        plugins/handsonai/skills/naming-workflows/SKILL.md "owns this process"
must_contain     "improve: writes stale_after"                plugins/handsonai/skills/improve/SKILL.md "stale_after"
must_contain     "improve: writes a Note"                     plugins/handsonai/skills/improve/SKILL.md "Note"
must_contain     "design: writes execution_mode"              plugins/handsonai/skills/design/SKILL.md "execution_mode"
must_contain     "design: writes autonomy"                    plugins/handsonai/skills/design/SKILL.md "autonomy"
must_not_contain "test: does not write a registry health field" plugins/handsonai/skills/test/SKILL.md "set the registry field \`health\`"
must_contain     "writing-process-guides: writes guide:"      plugins/handsonai/skills/writing-process-guides/SKILL.md "guide:"
must_contain     "writing-workflow-sops: resolves owning Function" plugins/handsonai/skills/writing-workflow-sops/SKILL.md "owning Function"

# ---------------------------------------------------------------------------
echo
echo "-- 6. skill integrity: every registry-writing skill defers to the bundle --"
# "The ten": the seven canonical framework-step skills plus the three registry-support
# skills that write into it directly. indexing-registry is checked separately in class 9
# (it IS registry-bundle.md's home skill); scaffolding-registry seeds the whole bundle
# from schema-template.md and never references write rules for existing nodes.
declare -a BUNDLE_REFERENCERS=(
  analyze deconstruct design build improve run test
  naming-workflows writing-process-guides writing-workflow-sops
)
for skill in "${BUNDLE_REFERENCERS[@]}"; do
  must_contain "$skill/SKILL.md defers to registry-bundle.md" "plugins/handsonai/skills/$skill/SKILL.md" "registry-bundle.md"
done
must_contain "framework-agent.md defers to registry-bundle.md" plugins/handsonai/agents/framework-agent.md "registry-bundle.md"

# The seven skills that actually write a Workflow node end-to-end must hand off to a
# maintenance pass afterward. Analyze precedes registry existence (nothing to name yet),
# so naming-workflows — the true first write — fills its slot.
declare -a MAINTENANCE_PASS_SKILLS=(deconstruct design build test run improve naming-workflows)
for skill in "${MAINTENANCE_PASS_SKILLS[@]}"; do
  must_contain "$skill/SKILL.md invokes a maintenance pass" "plugins/handsonai/skills/$skill/SKILL.md" "maintenance pass"
done

must_not_contain "deconstruct no longer references a workflow manifest" plugins/handsonai/skills/deconstruct/SKILL.md "### Workflow manifest"

# ---------------------------------------------------------------------------
echo
echo "-- 7. one-node-shape: every worked example carries the same Workflow node fields --"
if [ "$FULL" -eq 1 ]; then
  declare -a SHAPE_DOCS=(
    "$SETUP_PAGE"
    src/content/docs/ai-workflow-framework/examples/worked-example.md
    src/content/docs/courses/framework-end-to-end.md
  )
  for doc in "${SHAPE_DOCS[@]}"; do
    must_contain "$(basename "$doc") carries definition_type" "$doc" "definition_type"
    must_contain "$(basename "$doc") carries execution_mode"  "$doc" "execution_mode"
    must_contain "$(basename "$doc") carries stale_after"     "$doc" "stale_after"
    must_contain "$(basename "$doc") carries a generated: { line" "$doc" "generated: {"
  done
else
  skip "one-node-shape — setup page / worked-example / framework-end-to-end"
fi
# example-registry.md exists from Batch A — runs unconditionally.
EXAMPLE_REGISTRY=plugins/handsonai/skills/scaffolding-registry/references/example-registry.md
must_contain "example-registry.md carries definition_type"     "$EXAMPLE_REGISTRY" "definition_type"
must_contain "example-registry.md carries execution_mode"      "$EXAMPLE_REGISTRY" "execution_mode"
must_contain "example-registry.md carries stale_after"         "$EXAMPLE_REGISTRY" "stale_after"
must_contain "example-registry.md carries a generated: { line" "$EXAMPLE_REGISTRY" "generated: {"

# ---------------------------------------------------------------------------
echo
echo "-- 8. action integrity: the publish workflow runs the real compose step --"
WORKFLOW_YML=registry-template/.github/workflows/registry.yml
must_contain "registry.yml runs compose-registry.js" "$WORKFLOW_YML" "tools/compose-registry.js"
must_contain "registry.yml watches registry/**"       "$WORKFLOW_YML" "registry/**"
must_contain "registry.yml uploads the Pages artifact" "$WORKFLOW_YML" "upload-pages-artifact"

# ---------------------------------------------------------------------------
echo
echo "-- 9. lint-list agreement: registry-bundle.md and lint-registry.js name the same rules --"
LINT_JS=registry-template/tools/lint-registry.js
declare -a LINT_KEYWORDS=(banned claims back-pointer "run log" "index coverage" Owns stale_after orphan actor)
for kw in "${LINT_KEYWORDS[@]}"; do
  must_contain_i "registry-bundle.md names the '$kw' rule" "$BUNDLE" "$kw"
  must_contain_i "lint-registry.js implements the '$kw' rule" "$LINT_JS" "$kw"
done
must_contain "indexing-registry/SKILL.md defers to the single rule list" plugins/handsonai/skills/indexing-registry/SKILL.md "registry-bundle.md"

# ---------------------------------------------------------------------------
echo
echo "-- 10. the leaders checklist generator points at the registry, not Notion --"
if [ "$FULL" -eq 1 ]; then
  PDF_SCRIPT=scripts/generate-leaders-checklist-pdf.py
  must_contain     "leaders-checklist generator references registry/" "$PDF_SCRIPT" "registry/"
  must_not_contain "leaders-checklist generator drops the Notion AI Registry mention" "$PDF_SCRIPT" "Notion AI Registry"
else
  skip "leaders checklist generator — registry/ reference and Notion AI Registry removal"
fi

# ---------------------------------------------------------------------------
echo
echo "$PASS passed, $FAIL failed, $SKIP skipped"
[ "$FAIL" -eq 0 ]
