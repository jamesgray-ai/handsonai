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
            multiline-frontmatter missing-index-entry missing-dir-index \
            legacy-timestamp; do
  if run_lint "broken/$case"; then bad "$case: lint should exit 1"; else
    out=$(lint_output "broken/$case")
    grep -q "ERROR" <<<"$out" && ok "$case errors" || bad "$case: no ERROR line"
  fi
done
run_lint broken/unassigned-backlog && ok "unassigned backlog is warning-only" || bad "backlog unassigned must not error"
# lint: claims sweep dedupes claimants from the SAME workflow (Finding 4) --
# two links to sops/one-sop.md in one workflow's prose is one claim, not a
# false "claimed by 2 Workflow nodes" double-claim.
WS=$(stage valid-bundle)
node -e '
const fs = require("fs");
const f = process.argv[1];
let t = fs.readFileSync(f, "utf8");
t = t.replace("The complete fixture workflow", "See also [the SOP](sops/one-sop.md). The complete fixture workflow");
fs.writeFileSync(f, t);
' "$WS/registry/workflows/first-workflow.md"
run_lint_at "$WS" && ok "duplicate same-workflow SOP link does not false-positive double-claim" || bad "duplicate same-workflow SOP link should still lint clean: $(run_lint_at "$WS" 2>&1)"
# lint: a stale/hand-edited GENERATED:owns block is a WARNING, not an error
# (Finding A -- the Owns-block deadlock). Phase 4 of scaffolding names Process
# owners before Phase 6's maintenance pass regenerates Owns, so this is an
# expected mid-run state, and lint must never block compose from fixing it.
run_lint broken/hand-edited-generated && ok "hand-edited-generated is warning-only (exit 0)" || bad "stale Owns content must not error"
out=$(lint_output broken/hand-edited-generated)
grep -qi "WARN.*Owns" <<<"$out" && ok "hand-edited-generated warns about stale Owns" || bad "expected stale Owns WARN"

# lint/compose: the deadlock is gone end-to-end -- stage valid-bundle, empty a
# Function's Owns content (simulating post-scaffold staleness before Phase 6's
# maintenance pass), confirm lint warns but exits 0, confirm compose still
# succeeds and refills it, then confirm a fresh lint is clean.
WS=$(stage valid-bundle)
node -e '
const fs = require("fs");
const file = process.argv[1];
let text = fs.readFileSync(file, "utf8");
text = text.replace(/<!-- GENERATED:owns -->[\s\S]*?<!-- \/GENERATED -->/, "<!-- GENERATED:owns -->\n<!-- /GENERATED -->");
fs.writeFileSync(file, text);
' "$WS/registry/functions/operations.md"
run_lint_at "$WS" && ok "deadlock fixture: stale Owns lints clean (exit 0)" || bad "deadlock fixture: stale Owns should not error"
out=$(run_lint_at "$WS" 2>&1)
(cd "$WS" && node "$TOOLS/compose-registry.js" registry >/tmp/deadlock-compose.out 2>&1) && ok "deadlock fixture: compose succeeds against stale Owns" || bad "deadlock fixture: compose failed: $(cat /tmp/deadlock-compose.out)"
grep -q "Client Onboarding" "$WS/registry/functions/operations.md" && ok "deadlock fixture: compose refilled Owns" || bad "deadlock fixture: Owns still empty after compose"
run_lint_at "$WS" && ok "deadlock fixture: post-compose lint is clean" || bad "deadlock fixture: post-compose lint should be clean"
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

# compose: fixtures excluded from capability scan (Finding 1 regression) --
# registry-template/tools/fixtures/** contains its own .claude/skills/ trees
# (orphan-skill, some-skill) used to test lint's orphan-capability warning.
# Composing at the *template repo root* (not just registry/) must not walk
# into tools/fixtures/ and leak those fictional skills into the data island
# or lint's orphan-capabilities warning.
FSWS=$(mktemp -d); cp -R "$REPO_ROOT/registry-template/." "$FSWS/"
(cd "$FSWS" && git init -q . && git add -A >/dev/null 2>&1)
(cd "$FSWS" && node tools/compose-registry.js --island-only registry) > /tmp/fixture-scan-island.json 2>/tmp/fixture-scan-island.err
if grep -q "orphan-skill" /tmp/fixture-scan-island.json; then
  bad "fixture skills leaked into island (orphan-skill present)"
else
  ok "island has no orphan-skill from tools/fixtures"
fi
if grep -q "tools/fixtures" /tmp/fixture-scan-island.json; then
  bad "island contains a tools/fixtures/ path"
else
  ok "island has no tools/fixtures/ path"
fi
fixlint_out=$(cd "$FSWS" && node tools/lint-registry.js registry 2>&1)
if grep -q "tools/fixtures" <<<"$fixlint_out"; then
  bad "lint emitted an orphan-capability warning for a tools/fixtures skill"
else
  ok "lint emits zero orphan-capability warnings for fixture skills"
fi

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

  # dashboard-template: a Workflow with processId:null (Finding 7) is counted
  # in the KPI total (workflows.length) but, before this fix, was rendered
  # nowhere -- it only ever appeared nested under a Process row, which by
  # definition excludes a null processId. Also asserts the unassigned-
  # processes lane no longer rebuilds title-less/owner-less stubs.
  node -e '
const fs = require("fs");
const island = JSON.parse(fs.readFileSync(process.argv[1], "utf8"));
island.workflows = island.workflows.concat([{
  id: "orphan-workflow-test", title: "Orphan Workflow Test",
  description: "No process assigned.", status: "backlog",
  processId: null, lobId: null, state: "Requirements needed", skills: [], agents: [],
  nodePath: "registry/workflows/orphan-workflow-test.md",
}]);
fs.writeFileSync(process.argv[2], JSON.stringify(island));
' "$FIX/golden/data-island.json" /tmp/unassigned-wf-island.json
  node -e '
const fs = require("fs");
const vm = require("vm");
const script = fs.readFileSync(process.argv[1], "utf8");
const islandJson = fs.readFileSync(process.argv[2], "utf8");

function makeEl(id) {
  return {
    id: id, _text: "", _html: "", listeners: {},
    get textContent() { return this._text; }, set textContent(v) { this._text = String(v); },
    get innerHTML() { return this._html; }, set innerHTML(v) { this._html = String(v); },
    classList: { add: function () {}, remove: function () {} },
    setAttribute: function () {}, getAttribute: function () { return null; },
    addEventListener: function (type, fn) { this.listeners[type] = this.listeners[type] || []; this.listeners[type].push(fn); },
  };
}
const ids = ["data", "root", "scrim", "panel", "panel-type", "panel-title", "panel-desc", "panel-meta", "panel-extra", "panel-close"];
const elements = {};
ids.forEach(function (id) { elements[id] = makeEl(id); });
elements["data"].textContent = islandJson;
const doc = {
  getElementById: function (id) { return elements[id]; },
  listeners: {},
  addEventListener: function (type, fn) { this.listeners[type] = this.listeners[type] || []; this.listeners[type].push(fn); },
};
const sandbox = { document: doc, console: console, Date: Date, JSON: JSON, String: String, Array: Array, Object: Object, Boolean: Boolean, Infinity: Infinity };
vm.createContext(sandbox);
vm.runInContext(script, sandbox);

const shownByTitle = elements.root.innerHTML.indexOf("Orphan Workflow Test") !== -1;
console.log(shownByTitle ? "UNASSIGNED_WF_SHOWN" : "UNASSIGNED_WF_MISSING");

const fakeTarget = {
  closest: function () {
    return { getAttribute: function (attr) { return attr === "data-kind" ? "workflow" : (attr === "data-id" ? "orphan-workflow-test" : null); } };
  },
};
(elements.root.listeners.click || []).forEach(function (fn) { fn({ target: fakeTarget }); });
const drillInOk = elements["panel-title"].textContent === "Orphan Workflow Test";
console.log(drillInOk ? "UNASSIGNED_WF_DRILLIN_OK" : "UNASSIGNED_WF_DRILLIN_FAIL");
' /tmp/dashboard-renderer.js /tmp/unassigned-wf-island.json > /tmp/unassigned-wf-exec.out
  grep -q "UNASSIGNED_WF_SHOWN" /tmp/unassigned-wf-exec.out && ok "processId:null workflow rendered by title in an Unassigned lane" || bad "processId:null workflow missing from rendered output"
  grep -q "UNASSIGNED_WF_DRILLIN_OK" /tmp/unassigned-wf-exec.out && ok "processId:null workflow row is a clickable drill-in" || bad "processId:null workflow row did not drill in"
else
  bad "registry-template/tools/dashboard-template.html missing"
fi

# compose-registry.js: registry-dashboard.html injection survives $-shaped and
# </script>-shaped content intact (Finding 2 regression). Uses a private copy
# of valid-bundle so the shared golden fixtures don't need special-case
# content that would churn every golden diff above.
WS=$(stage valid-bundle)
node -e '
const fs = require("fs");
const file = process.argv[1];
let text = fs.readFileSync(file, "utf8");
const hostile = "Has a literal </script> tag, a $& backreference, and a $1 group.";
text = text.replace(/^description: .*$/m, () => "description: " + JSON.stringify(hostile));
fs.writeFileSync(file, text);
' "$WS/registry/workflows/first-workflow.md"
cp "$TOOLS/dashboard-template.html" "$WS/registry-dashboard.html"
(cd "$WS" && node "$TOOLS/compose-registry.js" registry) >/tmp/inject-compose.out 2>&1
node -e '
const fs = require("fs");
const html = fs.readFileSync(process.argv[1], "utf8");
const re = /<script type="application\/json" id="data">([\s\S]*?)<\/script>/;
const m = re.exec(html);
if (!m) { console.log("NO_MATCH"); process.exit(0); }
// Raw injected text must never contain an unescaped </script> -- that would
// prematurely close the tag (or, with the non-greedy regex above, truncate
// the match at the wrong point).
if (m[1].indexOf("</script>") !== -1) { console.log("UNESCAPED_SCRIPT_CLOSE"); process.exit(0); }
let island;
try { island = JSON.parse(m[1]); } catch (e) { console.log("PARSE_FAIL " + e.message); process.exit(0); }
// Round-tripped through JSON.parse, the original content -- including the
// literal </script> and the $-shaped substrings -- must come back intact
// (proves the function-form .replace() did not treat them as replacement
// patterns, and the < escaping did not survive into the parsed value).
const text = JSON.stringify(island);
if (text.indexOf("</script>") === -1) { console.log("SCRIPT_CLOSE_LOST"); process.exit(0); }
if (text.indexOf("$&") === -1 || text.indexOf("$1 group") === -1) { console.log("CONTENT_CORRUPTED"); process.exit(0); }
console.log("OK");
' "$WS/registry-dashboard.html" > /tmp/inject-check.out 2>&1
grep -q "^OK$" /tmp/inject-check.out && ok "dashboard injection survives \$&/\$1/</script> content intact" || bad "dashboard injection check failed: $(cat /tmp/inject-check.out) / compose: $(cat /tmp/inject-compose.out)"

# registry-lib.js replaceGeneratedBlock: derived content containing a literal
# "$&" must survive intact into a GENERATED block (Finding 3 -- the same
# $-substitution hazard as the dashboard inject above, but in the
# Function `# Owns` / Workflow `# Insights` regeneration path, which used the
# string form of .replace() until now).
WS=$(stage valid-bundle)
sed -i '' 's/^title: "Client Onboarding"$/title: "Client Onboarding $\&"/' "$WS/registry/processes/client-onboarding.md"
(cd "$WS" && node "$TOOLS/compose-registry.js" registry) >/tmp/dollar-owns-compose.out 2>&1
grep -qF 'Client Onboarding $&' "$WS/registry/functions/operations.md" && ok "Owns block survives a \$& title intact" || bad "Owns block corrupted by \$& title: $(cat /tmp/dollar-owns-compose.out)"

# lint: a freshly scaffolded bundle with zero workflows (post-v8 scaffold) lints clean
run_lint empty-workflows-bundle && ok "empty-workflows bundle lints clean (exit 0)" || bad "empty-workflows bundle should lint clean"

# No outputs/ layout any more (rules 11.1): lint never reads, warns about or moves an old
# outputs/<slug>/ record; outputs/ is only ever a workflow's own output.
run_lint legacy-outputs-workspace && ok "old outputs/ record: lint exits 0" || bad "old outputs/ record must not error"
out=$(lint_output legacy-outputs-workspace)
grep -qE "pre-9\.0|outputs/first-workflow/:" <<<"$out" && bad "lint still warns about an outputs/ record: $(grep WARN <<<"$out")" || ok "no outputs/ record warning is ever emitted"

out=$(lint_output valid-bundle)
grep -q "folder not claimed" <<<"$out" && bad "valid-bundle: unexpected unclaimed-folder warning" || ok "output-only outputs folder is silent (no unclaimed warning)"

# first-workflow -> client-onboarding -> design-services. Give that LOB a folder: so the check runs.
# Lint warns at most once per workflow (it breaks after the first outside link), so a framework/
# link must not be that first warning; .claude/skills/... is expected to be.
WS=$(stage valid-bundle)
perl -0pi -e 's/^(status: .*)$/$1\nfolder: lob-files\//m' "$WS/registry/lines-of-business/design-services.md"
grep -q "^folder: lob-files/" "$WS/registry/lines-of-business/design-services.md" || bad "LOB test setup: folder: not inserted"
run_lint_at "$WS" 2>&1 | grep -q "artifact link framework/" \
  && bad "LOB folder check exempts framework/: got an outside-LOB warning for a framework/ link" || ok "LOB folder check exempts framework/"

WS=$(stage valid-bundle); mkdir -p "$WS/framework/orphan-workflow"; : > "$WS/framework/orphan-workflow/requirements.md"
run_lint_at "$WS" 2>&1 | grep -q "WARN.*framework/orphan-workflow/: framework folder not claimed by any Workflow node" \
  && ok "unclaimed framework folder warned" || bad "expected unclaimed framework folder WARN"

# staged agents: framework/<slug>/package/agents/*.md count as capabilities (staged skills already do)
WS=$(stage valid-bundle); mkdir -p "$WS/framework/first-workflow/package/agents"; printf -- '---\nname: staged-agent\ndescription: x\n---\n' > "$WS/framework/first-workflow/package/agents/staged-agent.md"
run_lint_at "$WS" 2>&1 | grep -q "orphan.*framework/first-workflow/package/agents/staged-agent.md" \
  && ok "staged agent in a workflow's package/ counted as a capability" || bad "expected staged agent framework/first-workflow/package/agents/staged-agent.md in orphan warning"
# kept copies in history/ are never live capabilities
WS=$(stage valid-bundle); mkdir -p "$WS/framework/first-workflow/history/kept-copy-2026-10-01-0900/skills/kept-skill"; printf -- '---\nname: kept-skill\ndescription: x\n---\n' > "$WS/framework/first-workflow/history/kept-copy-2026-10-01-0900/skills/kept-skill/SKILL.md"
run_lint_at "$WS" 2>&1 | grep -q "kept-skill" && bad "a kept copy in history/ counted as a capability" || ok "skills in history/ are not capabilities"

# capability descriptions: SKILL.md and agent files are not registry nodes and commonly write
# `description: >` (folded), `|` (literal) or a plain value continued on indented lines -- the
# island must carry the text, not an empty description (the dashboard renders that as "—").
WS=$(stage valid-bundle)
printf -- '---\nname: some-skill\ndescription: >\n  Folded line one\n  and line two.\nlicense: MIT\n---\n# some-skill\n' > "$WS/.claude/skills/some-skill/SKILL.md"
printf -- '---\nname: orphan-skill\ndescription: Plain start\n  continued here.\n---\n# orphan-skill\n' > "$WS/.claude/skills/orphan-skill/SKILL.md"
mkdir -p "$WS/.claude/agents"; printf -- '---\nname: lit-agent\ndescription: |\n  Literal one\n  Literal two\ntools: Read\n---\nBody\n' > "$WS/.claude/agents/lit-agent.md"
(cd "$WS" && node "$TOOLS/compose-registry.js" --island-only registry) > "$WS/island.json" 2>/dev/null
desc() { node -e "const d=JSON.parse(require('fs').readFileSync(process.argv[1]));const all=[...(d.skills||[]),...(d.agents||[])];const x=all.find(s=>s.id===process.argv[2]);process.stdout.write(x?x.description:'<missing>')" "$WS/island.json" "$1"; }
[ "$(desc some-skill)" = "Folded line one and line two." ] && ok "folded (>) skill description read" || bad "folded description: got '$(desc some-skill)'"
[ "$(desc orphan-skill)" = "Plain start continued here." ] && ok "plain multi-line skill description read" || bad "plain multi-line description: got '$(desc orphan-skill)'"
[ "$(desc lit-agent)" = "Literal one Literal two" ] && ok "literal (|) agent description read onto one line" || bad "literal description: got '$(desc lit-agent)'"
# markdown views stay intact: a multi-line, blank-line or pipe-bearing description is one table row
mkdir -p "$WS/.claude/agents"; printf -- '---\nname: md-agent\ndescription: |\n  Does A | B\n\n  - not a bullet\n---\nBody\n' > "$WS/.claude/agents/md-agent.md"
(cd "$WS" && node "$TOOLS/compose-registry.js" registry >/dev/null 2>&1)
row=$(grep -n "md-agent" "$WS/REGISTRY.md")
[ "$(grep -c "md-agent" "$WS/REGISTRY.md")" -eq 1 ] && grep -qF 'Does A \| B - not a bullet |' <<<"$row" \
  && ok "REGISTRY.md: multi-line description with a pipe stays one escaped table row" || bad "REGISTRY.md row broken: $(grep -A2 md-agent "$WS/REGISTRY.md")"
grep -q "^- not a bullet" "$WS/registry/index.md" && bad "registry/index.md got a stray bullet from a description" || ok "registry/index.md: no stray bullet from a multi-line description"
# registry nodes stay strict: multi-line frontmatter in a node is still a lint error
out=$(lint_output broken/multiline-frontmatter)
grep -q "ERROR.*multi-line YAML" <<<"$out" && ok "multi-line node frontmatter still errors (strict parser)" || bad "multi-line node frontmatter must still error: $out"

# on GitHub Actions, each lint error is also a workflow annotation, so the run's summary page
# names the file and rule without opening the log; elsewhere the output is unchanged
WS=$(stage broken/bad-enum)
out=$(cd "$WS" && GITHUB_ACTIONS=true node "$TOOLS/lint-registry.js" registry 2>&1 || true)
grep -q "^::error title=Registry check::" <<<"$out" && ok "lint posts errors as GitHub annotations on Actions" || bad "expected ::error annotations under GITHUB_ACTIONS=true"
out=$(cd "$WS" && env -u GITHUB_ACTIONS node "$TOOLS/lint-registry.js" registry 2>&1 || true)
grep -q "^::error" <<<"$out" && bad "lint printed annotations outside GitHub Actions" || ok "no annotations outside GitHub Actions"

# lenient reader edge cases: a byte-order mark, and an indentation indicator (>2)
node -e "
const lib=require(process.argv[1]);
const a=lib.parseCapabilityFrontmatter('\uFEFF---\nname: x\ndescription: With BOM\n---\n');
const b=lib.parseCapabilityFrontmatter('---\nname: x\ndescription: >2\n  Indented text\n---\n');
process.exit(a.description==='With BOM' && b.description==='Indented text' ? 0 : 1);" "$TOOLS/registry-lib.js" \
  && ok "capability frontmatter: BOM and >2 indicator read" || bad "capability frontmatter: BOM or >2 indicator misread"
# compose never crashes on an unreadable or dangling skill/agent file
WS=$(stage valid-bundle); chmod 000 "$WS/.claude/skills/orphan-skill/SKILL.md"; mkdir -p "$WS/.claude/agents"; ln -s "$WS/nope.md" "$WS/.claude/agents/dangling.md"
out=$(cd "$WS" && node "$TOOLS/compose-registry.js" registry 2>&1 || true); chmod 644 "$WS/.claude/skills/orphan-skill/SKILL.md"
! grep -qE '^[[:space:]]+at |EACCES|ENOENT' <<<"$out" && ok "compose skips unreadable or dangling skill/agent files" || bad "compose crashed on an unreadable skill/agent file: $(grep -E 'Error' <<<"$out" | head -1)"

# an outputs/<slug>/ holding a run log or test-runs/ is a workflow's own output: no warning
WS=$(stage valid-bundle)
printf '| Date | Result |\n|---|---|\n| 2026-10-01 | ok |\n' > "$WS/outputs/first-workflow/runs.md"
mkdir -p "$WS/outputs/first-workflow/test-runs"; : > "$WS/outputs/first-workflow/test-runs/round-1.md"
run_lint_at "$WS" 2>&1 | grep -q "outputs/first-workflow/:" && bad "outputs/<slug>/ warned as a record" || ok "outputs/<slug>/ with runs.md or test-runs/ is never warned"

# a missing framework/ link is strict: framework/ is never gitignored, so lint errors
WS=$(stage valid-bundle); rm "$WS/framework/first-workflow/test-results.md"
if run_lint_at "$WS" >/dev/null 2>&1; then bad "missing framework/ link: lint should exit 1"; else
  out=$(run_lint_at "$WS" 2>&1)  # variable capture: lint exits 1 here, so never pipe it under pipefail
  grep -q "ERROR.*repo link framework/first-workflow/test-results.md -- file not found" <<<"$out" \
    && ok "missing framework/ link is a lint ERROR naming the file" || bad "missing framework/ link: no ERROR naming test-results.md"
fi

# robustness: odd entries where lint expects folders never crash it with a JS stack trace
no_trace() { ! grep -qE '^[[:space:]]+at |TypeError|Error:' <<<"$1"; }
WS=$(stage valid-bundle); rm -rf "$WS/framework"; : > "$WS/framework"
out=$(run_lint_at "$WS" 2>&1 || true)
no_trace "$out" && ok "framework/ as a plain file: lint reports, no stack trace" || bad "framework/ as a plain file crashed lint: $(grep -E 'Error' <<<"$out" | head -1)"
WS=$(stage valid-bundle); ln -s "$WS/does-not-exist" "$WS/framework/dangling"
out=$(run_lint_at "$WS" 2>&1 || true)
no_trace "$out" && ok "broken symlink in framework/: lint skips it, no stack trace" || bad "broken symlink in framework/ crashed lint: $(grep -E 'Error' <<<"$out" | head -1)"
WS=$(stage valid-bundle); ln -s "$WS/does-not-exist" "$WS/outputs/dangling"
out=$(run_lint_at "$WS" 2>&1 || true)
no_trace "$out" && ok "broken symlink in outputs/: lint skips it, no stack trace" || bad "broken symlink in outputs/ crashed lint: $(grep -E 'Error' <<<"$out" | head -1)"
WS=$(stage valid-bundle); rm -rf "$WS/outputs"; : > "$WS/outputs"
out=$(run_lint_at "$WS" 2>&1 || true)
no_trace "$out" && ok "outputs/ as a plain file: lint reports, no stack trace" || bad "outputs/ as a plain file crashed lint: $(grep -E 'Error' <<<"$out" | head -1)"
WS=$(stage valid-bundle); rm -rf "$WS/sops"; : > "$WS/sops"
out=$(run_lint_at "$WS" 2>&1 || true)
no_trace "$out" && ok "sops/ as a plain file: lint reports, no stack trace" || bad "sops/ as a plain file crashed lint: $(grep -E 'Error' <<<"$out" | head -1)"
WS=$(stage valid-bundle); ln -s "$WS/does-not-exist.md" "$WS/sops/dangling.md"
out=$(run_lint_at "$WS" 2>&1 || true)
no_trace "$out" && ok "broken symlink in sops/: lint skips it, no stack trace" || bad "broken symlink in sops/ crashed lint: $(grep -E 'Error' <<<"$out" | head -1)"
# (an administrator account can read a mode-000 file, so this test proves nothing when run as root)
WS=$(stage valid-bundle); printf 'x\n' > "$WS/sops/locked.md"; chmod 000 "$WS/sops/locked.md"
out=$(run_lint_at "$WS" 2>&1 || true); chmod 644 "$WS/sops/locked.md"
no_trace "$out" && ok "unreadable file in sops/: lint skips it, no stack trace" || bad "unreadable file in sops/ crashed lint: $(grep -E 'Error' <<<"$out" | head -1)"

# --- this release's views and rules (rules 6.10, 6.11) -------------------------
# views: no step number, no "Review by", no raw autonomy/execution_mode labels
compose_at valid-bundle >/dev/null 2>&1
grep -qE "step [0-9]+/|Review by|Review dates|\| Mode \||\| Autonomy \|" "$WS/REGISTRY.md" && bad "REGISTRY.md carries a step number or an old label" || ok "REGISTRY.md: no step number, no Review by, no Mode/Autonomy columns"
grep -q "| Progress | How it decides | How it runs | Re-check by |" "$WS/REGISTRY.md" && ok "REGISTRY.md: Progress, How it decides, How it runs, Re-check by" || bad "REGISTRY.md: missing the plain-label columns"
grep -q "## Re-check dates" "$WS/REGISTRY.md" && ok "REGISTRY.md: Re-check dates section" || bad "REGISTRY.md: no Re-check dates section"
grep -q "Runs with you" "$WS/REGISTRY.md" && grep -q "Guided: makes bounded decisions with your method" "$WS/REGISTRY.md" && ok "REGISTRY.md: plain labels for execution mode and autonomy" || bad "REGISTRY.md: plain labels missing"
for D in "$TOOLS/dashboard-template.html" "$REPO_ROOT/plugins/handsonai/skills/indexing-registry/references/dashboard-template.html"; do
  grep -qE "Review by|'Autonomy'|'Execution mode'|'Definition type'|wf\.step|a\.step|⚠ overdue" "$D" && bad "$(basename "$(dirname "$D")")/dashboard-template.html carries an old label or step" || ok "$(basename "$(dirname "$D")")/dashboard-template.html: no step, no Review by, no raw labels"
done
grep -q '"step"' "$TOOLS/data-island.schema.json" && bad "data-island schema still has step" || ok "data-island schema has state, no step"
cmp -s "$TOOLS/dashboard-template.html" "$REPO_ROOT/plugins/handsonai/skills/indexing-registry/references/dashboard-template.html" && cmp -s "$TOOLS/data-island.schema.json" "$REPO_ROOT/plugins/handsonai/skills/indexing-registry/references/data-island.schema.json" \
  && ok "dashboard template and island schema byte-identical to the skill copies" || bad "dashboard template or island schema differs from the skill copy"

# state name per routing: compose reads each workflow's folder through framework-state
FF="$REPO_ROOT/framework-fixtures/states"
for pair in "s04-plan-needed:Plan needed" "s06-build-needed:Build needed" "s08-test-needed:Test needed" "s11-live:Live" "s00-running-work:Not a framework workflow, or retired"; do
  fx="${pair%%:*}"; name="${pair#*:}"
  SW=$(mktemp -d); cp -R "$FF/$fx/with-registry/." "$SW/"; (cd "$SW" && git init -q . )
  (cd "$SW" && node "$TOOLS/compose-registry.js" --island-only registry 2>/dev/null) > "$SW/island.json"
  node -e "const d=JSON.parse(require('fs').readFileSync(process.argv[1]));process.exit(d.workflows.some(w=>w.state===process.argv[2])?0:1)" "$SW/island.json" "$name" \
    && ok "state name from the folder: $fx -> $name" || bad "state name: $fx expected '$name', got $(node -e "const d=JSON.parse(require('fs').readFileSync(process.argv[1]));console.log(d.workflows.map(w=>w.id+'='+w.state).join(', '))" "$SW/island.json" 2>&1)"
  rm -rf "$SW"
done

# generated.at: a UTC instant; a bare date on an older node; anything else errors
WS=$(stage valid-bundle)
sed -i '' 's/^generated: { by: process:fixture, at: 2026-08-01 }$/generated: { by: process:fixture, at: 2026-08-01T09:30:00Z }/' "$WS/registry/workflows/second-workflow.md"
run_lint_at "$WS" >/dev/null 2>&1 && ok "generated.at as a UTC instant lints clean" || bad "generated.at instant should lint clean: $(run_lint_at "$WS" 2>&1 | grep ERROR)"
sed -i '' 's/at: 2026-08-01T09:30:00Z }/at: 2026-08-01 09:30 }/' "$WS/registry/workflows/second-workflow.md"
if run_lint_at "$WS" >/dev/null 2>&1; then bad "malformed generated.at should error"; else ok "malformed generated.at errors"; fi

# legacy labels: tolerated on an older node (bare-date stamp), an error on a node that writes them
run_lint valid-bundle && ok "older node with Design spec / Run guide / Improvement plan lints clean" || bad "legacy labels on an older node must lint clean"
WS=$(stage valid-bundle)
sed -i '' 's/^generated: { by: process:fixture, at: 2026-08-01 }$/generated: { by: process:test, at: 2026-10-24T12:00:00Z }/' "$WS/registry/workflows/first-workflow.md"
if run_lint_at "$WS" >/dev/null 2>&1; then bad "a current node writing legacy labels should error"; else
  out=$(run_lint_at "$WS" 2>&1)
  grep -q 'ERROR.*legacy artifact label(s) "Design spec", "Run guide", "Improvement plan" written on a current node' <<<"$out" \
    && ok "a current node writing legacy labels errors, naming them" || bad "legacy-label error text: $(grep ERROR <<<"$out")"
fi

# run log: external or absent "Run log" link is tolerated; a readable one is checked
WS=$(stage broken/runlog-status-contradiction)
sed -i '' 's|- \[Run log\](runs.md)|- [Run log](https://example.com/runs)|' "$WS/registry/workflows/first-workflow.md"
run_lint_at "$WS" >/dev/null 2>&1 && ok "external Run log link tolerated" || bad "external Run log link should lint clean: $(run_lint_at "$WS" 2>&1 | grep ERROR)"
WS=$(stage broken/runlog-status-contradiction)
sed -i '' '/- \[Run log\](runs.md)/d' "$WS/registry/workflows/first-workflow.md"
run_lint_at "$WS" >/dev/null 2>&1 && ok "absent Run log link tolerated (runs.md beside it is not read)" || bad "absent Run log link should lint clean"
out=$(lint_output broken/runlog-status-contradiction)
grep -q 'ERROR.*contradicts run log evidence (runs.md has entries)' <<<"$out" && ok "run log in the workflow's place, linked, contradicting status errors" || bad "run log contradiction text: $out"

# web-shaped bundle: Framework/ holds registry/ beside <slug>/ folders; links are <slug>/...
WEB=$(mktemp -d); cp -R "$FIX/valid-bundle/." "$WEB/"
mv "$WEB/framework/first-workflow" "$WEB/first-workflow"; rmdir "$WEB/framework"
sed -i '' 's|(framework/first-workflow/|(first-workflow/|g' "$WEB/registry/workflows/first-workflow.md"
(cd "$WEB" && git init -q . && git add -A >/dev/null 2>&1)
run_lint_at "$WEB" >/dev/null 2>&1 && ok "web-shaped bundle: <slug>/ links resolve from the registry's parent" || bad "web-shaped bundle should lint clean: $(run_lint_at "$WEB" 2>&1 | grep ERROR)"
mkdir -p "$WEB/orphan-flow"; : > "$WEB/orphan-flow/requirements.md"; mkdir -p "$WEB/history"; : > "$WEB/history/requirements.md"
out=$(run_lint_at "$WEB" 2>&1 || true)
grep -q "WARN.*orphan-flow/: framework folder not claimed" <<<"$out" && ok "web-shaped bundle: unclaimed sibling workflow folder warned" || bad "web-shaped: expected unclaimed warning for orphan-flow/"
grep -qE "WARN.*(history|sops)/: framework folder not claimed" <<<"$out" && bad "web-shaped: history/ or sops/ taken for a workflow folder" || ok "web-shaped: history/ and sops/ are never workflow folders"
(cd "$WEB" && node "$TOOLS/compose-registry.js" --island-only registry 2>/dev/null) > "$WEB/island.json"
node -e "const d=JSON.parse(require('fs').readFileSync(process.argv[1]));process.exit(d.workflows.find(w=>w.id==='first-workflow').state==='Earlier version'?0:1)" "$WEB/island.json" \
  && ok "web-shaped bundle: compose reads <slug>/ beside registry/ for the state" || bad "web-shaped bundle: state not read from <slug>/"
rm -rf "$WEB"

# TOOLS_VERSION: raised, equal to package.json's version, and the plugin ships the same tools
node -e "
const lib=require(process.argv[1]); const pkg=require(process.argv[2]);
process.exit(lib.TOOLS_VERSION && lib.TOOLS_VERSION===pkg.version && pkg.type==='commonjs' ? 0 : 1)" "$TOOLS/registry-lib.js" "$TOOLS/package.json" \
  && ok "TOOLS_VERSION matches tools/package.json's version (commonjs)" || bad "TOOLS_VERSION and package.json disagree"
for f in compose-registry.js lint-registry.js registry-lib.js package.json framework-state.js requirements-check.js; do
  cmp -s "$TOOLS/$f" "$REPO_ROOT/plugins/handsonai/tools/$f" && ok "plugin tools/$f identical to registry-template" || bad "plugin tools/$f differs from registry-template/tools/$f"
done
(cd "$REPO_ROOT" && node plugins/handsonai/tools/framework-state.js --help >/dev/null 2>&1; [ $? -ne 127 ] && node -e "require('./plugins/handsonai/tools/compose-registry.js')") >/dev/null 2>&1 \
  && ok "plugin tools load from the repo root (commonjs)" || bad "plugin tools fail to load from the repo root"

# worked example: examples/weekly-status-report is a committed fixture -- lints with exactly one expected warning and composes to a no-op
EX="$REPO_ROOT/examples/weekly-status-report"
ex_out=$(cd "$EX" && node "$TOOLS/lint-registry.js" registry 2>&1) && ok "worked example lints with exit 0" || bad "worked example lint failed: $(tail -1 <<<"$ex_out")"
grep -q "ERROR" <<<"$ex_out" && bad "worked example has lint errors" || ok "worked example has no lint errors"
ex_warns=$(grep -c "^WARN" <<<"$ex_out" || true)
grep -q "WARN.*stale_after 2026-08-14 is past -- re-check due" <<<"$ex_out" && [ "$ex_warns" -eq 1 ] \
  && ok "worked example: exactly the expected re-check-due warning" || bad "worked example: expected exactly one warning (re-check due), got $ex_warns: $(grep '^WARN' <<<"$ex_out")"
(cd "$EX" && node "$TOOLS/compose-registry.js" --check registry >/dev/null 2>&1) && ok "worked example composes to a no-op (REGISTRY.md, indexes, GENERATED blocks all current)" \
  || bad "worked example has stale derived views: $(cd "$EX" && node "$TOOLS/compose-registry.js" --check registry 2>&1 | grep STALE | tr '\n' ' ')"
[ "$(git -C "$REPO_ROOT" ls-files examples/weekly-status-report/framework | wc -l | tr -d ' ')" -gt 10 ] && ok "worked example framework/ is tracked by git" || bad "worked example framework/ is not tracked (gitignore?)"
[ "$(git -C "$REPO_ROOT" ls-files 'examples/weekly-status-report/outputs/weekly-status-report/status-report-*.md' | wc -l | tr -d ' ')" -eq 5 ] && ok "worked example keeps 5 sample reports in outputs/" || bad "worked example should keep its 5 status reports in outputs/"
ex_island=$(cd "$EX" && node "$TOOLS/compose-registry.js" --island-only registry 2>/dev/null)
grep -q '"nodeUrl"' <<<"$ex_island" && bad "worked example island carries nodeUrl (would be dead links for students)" || ok "worked example island has no nodeUrl"
[ -e "$EX/tools" ] && bad "worked example has a tools/ folder (nothing publishes it; compose no longer writes one)" || ok "worked example has no tools/ folder"

# compose never creates tools/last-data-island.json -- nothing publishes the registry, so
# the only data-island consumer is registry-dashboard.html, which compose updates in place.
compose_at valid-bundle >/dev/null 2>&1
[ -e "$WS/tools/last-data-island.json" ] && bad "compose wrote tools/last-data-island.json" || ok "compose writes no tools/last-data-island.json"
[ -e "$WS/tools" ] && bad "compose created a tools/ folder" || ok "compose creates no tools/ folder"

# nodeUrl links only to files on the remote branch, using the real branch name
# (never a hard-coded main). A throwaway repo with a GitHub remote and a faked
# origin/<branch> ref holding one of the two registry files.
echo
echo "-- nodeUrl: real branch, pushed files only --"
GT=$(mktemp -d)
cp -R "$EX/." "$GT/"
( cd "$GT" && git init -q -b trunk && git config user.email t@t && git config user.name t \
  && git remote add origin https://github.com/acme/reg.git \
  && git add registry/SCHEMA.md registry/businesses && git commit -qm pushed \
  && git update-ref refs/remotes/origin/trunk HEAD \
  && git add -A && git commit -qm local-only ) >/dev/null 2>&1
gt_island=$(cd "$GT" && node "$TOOLS/compose-registry.js" --island-only registry 2>/dev/null)
grep -q 'github.com/acme/reg/blob/trunk/registry/businesses/' <<<"$gt_island" && ok "pushed file links to the real branch (trunk)" || bad "pushed file has no nodeUrl on the real branch"
grep -q 'blob/main/' <<<"$gt_island" && bad "nodeUrl assumes main" || ok "nodeUrl never assumes main"
grep -q 'blob/trunk/registry/processes/' <<<"$gt_island" && bad "unpushed file got a nodeUrl (dead link)" || ok "unpushed files get no nodeUrl"
( cd "$GT" && git update-ref -d refs/remotes/origin/trunk ) >/dev/null 2>&1
gt_island=$(cd "$GT" && node "$TOOLS/compose-registry.js" --island-only registry 2>/dev/null)
grep -q '"nodeUrl"' <<<"$gt_island" && bad "branch never pushed still got nodeUrl" || ok "branch never pushed: no nodeUrl"
rm -rf "$GT"

echo
echo "$PASS ok, $FAIL bad"
[ "$FAIL" -eq 0 ]
