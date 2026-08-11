#!/usr/bin/env bash
# Tests for registry-template/tools/lint-registry.js (Task 5) and, once it
# exists, tools/compose-registry.js (Task 6). Follows the ok/bad/skip +
# summary house style from scripts/test-check-plugin-sync.sh.
#
# Every fixture stages into an isolated mktemp git repo (see stage() below) so
# `git check-ignore` inside lint sees only the fixture's own .gitignore, never
# this repo's unanchored `outputs/` rule -- that's also why
# `registry-template/tools/fixtures/**` is un-ignored in the root .gitignore.
#
# Run: bash scripts/test-compose-registry.sh

set -uo pipefail

PASS=0
FAIL=0
ok()   { echo "  ok    $1"; PASS=$((PASS + 1)); }
bad()  { echo "  FAIL  $1"; FAIL=$((FAIL + 1)); }
skip() { echo "  skip  $1"; }

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TOOLS="$REPO_ROOT/registry-template/tools"
FIX="$TOOLS/fixtures"
stage() {  # copy a fixture workspace to an isolated temp git repo; echoes the path
  local ws; ws=$(mktemp -d)
  cp -R "$FIX/$1/." "$ws/"
  (cd "$ws" && git init -q . && git add -A >/dev/null 2>&1)
  echo "$ws"
}
run_lint()    { local ws; ws=$(stage "$1"); (cd "$ws" && node "$TOOLS/lint-registry.js" registry >/dev/null 2>&1); }
lint_output() { local ws; ws=$(stage "$1"); (cd "$ws" && node "$TOOLS/lint-registry.js" registry 2>&1); }
run_lint_at() { (cd "$1" && node "$TOOLS/lint-registry.js" registry); }
compose_at()  { WS=$(stage "$1"); (cd "$WS" && node "$TOOLS/compose-registry.js" registry); }  # sets $WS for assertions

# lint: valid bundle passes
run_lint valid-bundle && ok "valid bundle lints clean (exit 0)" || bad "valid bundle should lint clean"
# lint: warnings present but exit 0
# (variable-capture pattern throughout -- lint_output legitimately exits 1 on
# error fixtures, and with `pipefail` active that must never sit on the left
# of a pipeline whose only job is to grep the captured text.)
out=$(lint_output valid-bundle)
grep -q "WARN.*stale_after" <<<"$out" && ok "overdue stale_after warned" || bad "expected overdue warning"
grep -q "WARN.*orphan-skill" <<<"$out" && ok "orphan capability warned" || bad "expected orphan-capability warning"
# lint: each broken fixture fails with a message naming the file
grep -q "WARN" <<<"$out" || bad "expected warnings on valid bundle"
out=$(lint_output broken/warn-bad-actor)
grep -q "WARN.*generated.by" <<<"$out" && ok "actor-string warned" || bad "expected actor warning"
out=$(lint_output broken/warn-misfiled-note)
grep -q "WARN.*[Nn]ote" <<<"$out" && ok "misfiled note warned" || bad "expected note warning"
for case in bad-enum dir-type-mismatch missing-owner missing-frontmatter broken-link banned-field \
            unclaimed-sop double-claim sop-backpointer-mismatch runlog-status-contradiction \
            double-parent-list unassigned-inproduction missing-owns-block unterminated-generated \
            multiline-frontmatter hand-edited-generated missing-index-entry missing-dir-index \
            legacy-timestamp; do
  if run_lint "broken/$case"; then bad "$case: lint should exit 1"; else
    out=$(lint_output "broken/$case")
    grep -q "ERROR" <<<"$out" && ok "$case errors" || bad "$case: no ERROR line"
  fi
done
run_lint broken/unassigned-backlog && ok "unassigned backlog is warning-only" || bad "backlog unassigned must not error"
# lint: legacy definition_type spelling ("step-decomposed") is tolerated as a
# warning, never an error -- the legacy-workspace migration path relies on
# this so a mid-migration bundle still lints clean.
run_lint legacy-enum-bundle && ok "legacy-enum-bundle lints clean (exit 0)" || bad "legacy-enum-bundle should lint clean"
out=$(lint_output legacy-enum-bundle)
grep -q "WARN.*step-decomposed" <<<"$out" && ok "legacy definition_type spelling warned, not errored" || bad "expected WARN for step-decomposed"
# lint: gitignore tolerance -- valid bundle with outputs/ deleted still lints clean
tmp=$(mktemp -d); cp -R "$FIX/valid-bundle/." "$tmp/"; rm -rf "$tmp/outputs"
printf 'outputs/\n' > "$tmp/.gitignore"; (cd "$tmp" && git init -q . && git add -A >/dev/null)
run_lint_at "$tmp" && ok "gitignored artifact links tolerated" || bad "gitignore tolerance failed"

# compose: refuses while lint errors
(cd "$FIX/broken/bad-enum" && ! node "$TOOLS/compose-registry.js" registry) && ok "compose refuses on lint errors" || bad "compose must refuse"
# compose: valid bundle → golden REGISTRY.md
compose_at valid-bundle
diff -u "$FIX/golden/REGISTRY.md" "$WS/REGISTRY.md" && ok "REGISTRY.md matches golden" || bad "REGISTRY.md drift"
# compose: fills Workflow `# Insights` GENERATED block (reverse view of the Note's link)
grep -q "/notes/first-workflow-insight.md" "$WS/registry/workflows/second-workflow.md" && ok "compose fills Workflow Insights GENERATED block" || bad "Insights block not filled"
# compose: deterministic — two runs byte-identical
cp "$WS/REGISTRY.md" /tmp/r1; (cd "$WS" && node "$TOOLS/compose-registry.js" registry)
cmp -s /tmp/r1 "$WS/REGISTRY.md" && ok "deterministic" || bad "output differs across runs"
# compose: data island valid + golden
(cd "$WS" && node "$TOOLS/compose-registry.js" --island-only registry) > /tmp/island.json
node -e "JSON.parse(require('fs').readFileSync('/tmp/island.json'))" && ok "island parses" || bad "island invalid JSON"
diff -u "$FIX/golden/data-island.json" /tmp/island.json && ok "island matches golden" || bad "island drift"
# compose: empty skeleton bundle (student's first Action run)
WS=$(mktemp -d); cp -R "$REPO_ROOT/registry-template/registry" "$WS/registry"
(cd "$WS" && git init -q . && node "$TOOLS/compose-registry.js" registry) && ok "empty bundle composes" || bad "empty bundle crashed"
grep -q "No workflows yet" "$WS/REGISTRY.md" && ok "empty dashboard has guidance line" || bad "missing empty-state line"
# compose: self-healing rename — stale GENERATED links must not deadlock
WS=$(stage valid-bundle)
mv "$WS/registry/workflows/first-workflow.md" "$WS/registry/workflows/first-workflow-weekly.md"
sed -i '' 's/^title: .*/title: "First Workflow Weekly"/' "$WS/registry/workflows/first-workflow-weekly.md"
sed -i '' 's|/workflows/first-workflow.md|/workflows/first-workflow-weekly.md|' "$WS/registry/processes/"*.md
# root index's GENERATED block deliberately still holds the stale old link
(cd "$WS" && node "$TOOLS/compose-registry.js" registry) && ok "rename does not deadlock compose" || bad "rename deadlocked"
run_lint_at "$WS" && ok "post-rename lint clean" || bad "post-rename lint dirty"

# compose: data island validates against its JSON Schema (zero-dep recursive
# checker -- ajv is not available; walks required/type/enum only).
node -e '
const fs = require("fs");
const schema = JSON.parse(fs.readFileSync(process.argv[1], "utf8"));
const data = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));
const errors = [];
function validate(node, sch, path) {
  if (sch.type === "array") {
    if (!Array.isArray(node)) { errors.push(path + ": expected array"); return; }
    if (sch.items) node.forEach((item, i) => validate(item, sch.items, path + "[" + i + "]"));
    return;
  }
  if (sch.type === "object" || sch.properties) {
    if (node === null) {
      if (sch.type && sch.type.includes && sch.type.includes("null")) return;
      if (Array.isArray(sch.type) && sch.type.includes("null")) return;
      errors.push(path + ": null not allowed");
      return;
    }
    if (typeof node !== "object") { errors.push(path + ": expected object"); return; }
    for (const req of (sch.required || [])) {
      if (!(req in node)) errors.push(path + ": missing required \"" + req + "\"");
    }
    for (const key of Object.keys(sch.properties || {})) {
      if (key in node) validate(node[key], sch.properties[key], path + "." + key);
    }
    return;
  }
  if (sch.type) {
    const types = Array.isArray(sch.type) ? sch.type : [sch.type];
    const jsType = node === null ? "null" : typeof node === "number" ? "number" : typeof node === "boolean" ? "boolean" : typeof node === "string" ? "string" : typeof node;
    if (!types.includes(jsType)) {
      errors.push(path + ": expected type " + JSON.stringify(sch.type) + ", got " + jsType);
      return;
    }
  }
  if (sch.enum && !sch.enum.includes(node)) {
    errors.push(path + ": " + JSON.stringify(node) + " not in enum " + JSON.stringify(sch.enum));
  }
}
for (const key of Object.keys(schema.properties || {})) {
  if (key in data) validate(data[key], schema.properties[key], key);
}
for (const req of (schema.required || [])) {
  if (!(req in data)) errors.push("(root): missing required \"" + req + "\"");
}
if (errors.length) { console.error(errors.join("\n")); process.exit(1); }
' "$TOOLS/data-island.schema.json" "$FIX/golden/data-island.json" \
  && ok "island validates against data-island.schema.json" \
  || bad "island failed schema validation"

# dashboard-template: self-contained Tier 2 dashboard renders the golden
# island. Injects with a replacer FUNCTION (never a $-substitution string --
# JSON content can contain literal "$1"-shaped text) and escapes any
# "</script"-like substrings so an embedded string can never early-terminate
# the data island element.
DASH="$TOOLS/dashboard-template.html"
if [ -f "$DASH" ]; then
  node -e '
const fs = require("fs");
const template = fs.readFileSync(process.argv[1], "utf8");
const island = fs.readFileSync(process.argv[2], "utf8");
const escaped = island.replace(/<\/script/gi, "<\\/script");
const re = /(<script type="application\/json" id="data">)[\s\S]*?(<\/script>)/;
const out = template.replace(re, function (_m, open, close) { return open + escaped + close; });
fs.writeFileSync(process.argv[3], out);
' "$DASH" "$FIX/golden/data-island.json" /tmp/dashboard-rendered.html
  grep -q "Kestrel Studio" /tmp/dashboard-rendered.html && ok "dashboard renders business name from golden island" || bad "dashboard missing Kestrel Studio"
  ext=$(grep -cE '(src|href)="https?://' /tmp/dashboard-rendered.html || true)
  [ "${ext:-0}" -eq 0 ] && ok "dashboard makes zero external requests (no http(s) src/href)" || bad "dashboard references an external URL"
  # Extract the renderer <script> -- the one WITHOUT type="application/json" --
  # never the data island itself, then check it's syntactically valid JS.
  node -e '
const fs = require("fs");
const html = fs.readFileSync(process.argv[1], "utf8");
const re = /<script(?![^>]*type="application\/json")[^>]*>([\s\S]*?)<\/script>/g;
let m, script = "";
while ((m = re.exec(html))) { script += m[1] + "\n"; }
fs.writeFileSync(process.argv[2], script);
' /tmp/dashboard-rendered.html /tmp/dashboard-renderer.js
  node --check /tmp/dashboard-renderer.js && ok "dashboard renderer script is syntactically valid" || bad "dashboard renderer script has a syntax error"

  # Actually execute the renderer against a minimal zero-dependency DOM stub
  # (no jsdom -- same "roll a ~30-line checker" philosophy as the schema
  # validator above) so these two checks assert real rendered behavior, not
  # just string presence in the raw (unexecuted) file:
  #   - the Business header link prefers business.url (Important finding #2)
  #   - a workflow drill-in renders a matching Note as an Insight, sourced
  #     from data.notes via `links` (Critical finding #1)
  node -e '
const fs = require("fs");
const vm = require("vm");
const script = fs.readFileSync(process.argv[1], "utf8");
const islandJson = fs.readFileSync(process.argv[2], "utf8");

function makeEl(id) {
  return {
    id: id,
    _text: "",
    _html: "",
    listeners: {},
    get textContent() { return this._text; },
    set textContent(v) { this._text = String(v); },
    get innerHTML() { return this._html; },
    set innerHTML(v) { this._html = String(v); },
    classList: { add: function () {}, remove: function () {} },
    setAttribute: function () {},
    getAttribute: function () { return null; },
    addEventListener: function (type, fn) {
      this.listeners[type] = this.listeners[type] || [];
      this.listeners[type].push(fn);
    },
  };
}

const ids = ["data", "root", "scrim", "panel", "panel-type", "panel-title", "panel-desc", "panel-meta", "panel-extra", "panel-close"];
const elements = {};
ids.forEach(function (id) { elements[id] = makeEl(id); });
elements["data"].textContent = islandJson;

const doc = {
  getElementById: function (id) { return elements[id]; },
  listeners: {},
  addEventListener: function (type, fn) {
    this.listeners[type] = this.listeners[type] || [];
    this.listeners[type].push(fn);
  },
};

const sandbox = { document: doc, console: console, Date: Date, JSON: JSON, String: String, Array: Array, Object: Object, Boolean: Boolean, Infinity: Infinity };
vm.createContext(sandbox);
vm.runInContext(script, sandbox);

const bizUrlOk = elements.root.innerHTML.indexOf("href=\"https://kestrelstudio.example\"") !== -1;
console.log(bizUrlOk ? "BIZ_URL_OK" : "BIZ_URL_MISSING");

const fakeTarget = {
  closest: function () {
    return { getAttribute: function (attr) { return attr === "data-kind" ? "workflow" : (attr === "data-id" ? "second-workflow" : null); } };
  },
};
(elements.root.listeners.click || []).forEach(function (fn) { fn({ target: fakeTarget }); });

const insightOk = elements["panel-extra"].innerHTML.indexOf("First Workflow Insight") !== -1;
console.log(insightOk ? "INSIGHT_OK" : "INSIGHT_MISSING");
' /tmp/dashboard-renderer.js "$FIX/golden/data-island.json" > /tmp/dashboard-exec.out
  grep -q "BIZ_URL_OK" /tmp/dashboard-exec.out && ok "dashboard header link prefers business.url" || bad "dashboard header does not use business.url for its href"
  grep -q "INSIGHT_OK" /tmp/dashboard-exec.out && ok "workflow drill-in renders a matching Note as an Insight (data.notes via links)" || bad "workflow drill-in missing Insights section from data.notes"
else
  bad "registry-template/tools/dashboard-template.html missing"
fi

echo
echo "$PASS ok, $FAIL bad"
[ "$FAIL" -eq 0 ]
