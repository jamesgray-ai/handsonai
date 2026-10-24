#!/usr/bin/env python3
"""Structure checks on the files later steps and scripts parse (rules 2.3: frontmatter keys,
headings and table columns are scripted).

  plan          design-plan.md      design.md 11 and 14 item 11; rules 6.3, 6.6
  build_record  build-record.md     build.md 11 and 13; rules 6.4, 6.6
  results       test-results.md     test.md 9; rules 6.5, 6.6
  requirements  requirements.md     through T14's requirements-check script (tools/requirements-check.js)

Each check returns a list of problems (empty when the file is well formed).

Usage: python3 structure.py <plan|build_record|results|requirements> <file>... [--no-registry]
"""
import re
import shutil
import subprocess
import sys
from pathlib import Path

try:
    import yaml  # PyYAML, when present: full value checks
except ImportError:  # pragma: no cover
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
REQUIREMENTS_CHECK = ROOT / "plugins" / "handsonai" / "tools" / "requirements-check.js"


# ---------------------------------------------------------------- helpers

def split_frontmatter(text):
    t = text.lstrip("﻿")
    if not t.startswith("---\n"):
        return None, t
    end = t.find("\n---", 4)
    if end < 0:
        return None, t
    return t[4:end], t[end + 4:]


def top_keys(fm):
    return [m.group(1) for m in re.finditer(r"^([A-Za-z_][\w-]*):", fm, re.M)]


def load_fm(fm):
    if yaml is None:
        return None
    try:
        return yaml.safe_load(fm) or {}
    except yaml.YAMLError as e:
        return {"__error__": str(e)}


def h2(body):
    return [l[3:].strip() for l in body.split("\n") if l.startswith("## ")]


def h3_under(body, section):
    out, inside = [], False
    for l in body.split("\n"):
        if l.startswith("## "):
            inside = l[3:].strip() == section
        elif inside and l.startswith("### "):
            out.append(l[4:].strip())
    return out


def section(body, name):
    out, inside = [], False
    for l in body.split("\n"):
        if l.startswith("## "):
            if inside:
                break
            inside = l[3:].strip() == name
            continue
        if inside:
            out.append(l)
    return "\n".join(out)


def tables(text):
    ts, cur = [], None
    for l in text.split("\n"):
        if l.strip().startswith("|"):
            if cur is None:
                cur = []
                ts.append(cur)
            if re.match(r"^\s*\|[\s\-|:]+\|\s*$", l):
                continue
            cur.append([c.strip() for c in re.split(r"(?<!\\)\|", l.strip())[1:-1]])
        else:
            cur = None
    return ts


def in_order(have, want, label):
    """Every heading of want appears in have, in this order."""
    pos, probs = 0, []
    for w in want:
        try:
            pos = have.index(w, pos) + 1
        except ValueError:
            probs.append(f"{label}: '{w}' missing or out of order (have {have})")
    return probs


REQUEST_SOURCES = {"change my workflow", "build", "test", "direct edit", "leader at test"}
REQUEST_KEYS = {"id", "source", "what", "why", "tasks", "after_round"}


def check_requests(reqs, where, with_outcome=False):
    """rules 6.6: the one change-request shape."""
    probs = []
    if reqs in (None, []):
        return probs
    if not isinstance(reqs, list):
        return [f"{where}: not a list"]
    for r in reqs:
        if not isinstance(r, dict):
            probs.append(f"{where}: entry is not a mapping: {r!r}")
            continue
        want = REQUEST_KEYS | ({"outcome"} if with_outcome else set())
        keys = set(r)
        if keys != want:
            probs.append(f"{where} {r.get('id')}: keys {sorted(keys)} != {sorted(want)}")
        if r.get("source") not in REQUEST_SOURCES:
            probs.append(f"{where} {r.get('id')}: source {r.get('source')!r} not one of {sorted(REQUEST_SOURCES)}")
        if not re.match(r"^(B\d+|T\d+\.\d+|C\d+)$", str(r.get("id", ""))):
            probs.append(f"{where}: id {r.get('id')!r} isn't B[n], T[round].[n] or C[n]")
        if with_outcome:
            o = str(r.get("outcome", ""))
            if not (o == "handled" or re.match(r"^declined: cannot-meet: [A-Z]+\d+: .+", o)
                    or (o.startswith("declined: ") and "cannot-meet" not in o)):
                probs.append(f"{where} {r.get('id')}: outcome {o!r} isn't handled, declined: cannot-meet: [line]: [reason], or declined: [reason]")
        if not isinstance(r.get("after_round"), int):
            probs.append(f"{where} {r.get('id')}: after_round isn't a number")
    return probs


# ---------------------------------------------------------------- the plan

PLAN_KEYS = ["workflow", "requirements_revision", "approved", "autonomy", "decomposition", "mechanism",
             "involvement", "platform", "platform_mode", "packaging", "changes"]
PLAN_VALUES = {"approved": {True, False}, "autonomy": {"Deterministic", "Guided", "Autonomous"},
               "decomposition": {"steps", "domains"}, "mechanism": {"Skill", "Agent"},
               "involvement": {"Augmented", "Automated"}, "platform_mode": {"code", "guided"},
               "packaging": {"Plugin", "Standalone Skill", "Workspace Agent", "Loose Files"}}
PLAN_SECTIONS = ["Source", "Architecture", "Decomposition", "Data Readiness", "Component Blueprints",
                 "Prerequisites", "Deployment Plan", "Deferred to Build", "Stakeholders", "Open items",
                 "Tasks", "Self-Test Summary"]
PLAN_OPTIONAL = {"Multi-Agent Configuration"}
PLAN_NEVER = {"Global Constraints", "Coverage", "Evaluation Inputs", "Recommended Implementation Order",
              "Value & Measurement", "Run logging", "Review focus"}
ARCH_SUBS = ["Execution Pattern", "Architecture Decisions", "Autonomy Summary", "Safety & Permissions",
             "Integration Options", "Model Recommendation"]
ARCH_DECISIONS = ["Lens", "Platform", "Platform Mode", "Orchestration", "Involvement", "Packaging", "Trigger"]
DECOMP_COLS = ["Step", "Autonomy", "Orchestration", "Integration", "Intelligence", "Build Output", "Checkpoint", "Role"]
BUILD_OUTPUT = re.compile(r"^(New skill: S\d+|Use existing: .+|Extend existing: .+ \(also used by: .+\)|"
                          r"New agent: A\d+|Inline prompt → Step \S+|Handled by orchestrator|MCP server: .+|"
                          r"Human \(no artifact\)|—)$")
TASK_FIELDS = ["Builds", "Uses / hands on", "Meets", "Done when", "Depends on", "rev"]


def check_plan(text, requirements_text=None):
    probs = []
    fm, body = split_frontmatter(text)
    if fm is None:
        return ["no frontmatter"]
    keys = top_keys(fm)
    if keys != PLAN_KEYS:
        probs.append(f"frontmatter keys {keys} != {PLAN_KEYS} (11.1: these keys, in order, and no others)")
    data = load_fm(fm)
    if data and "__error__" not in data:
        for k, allowed in PLAN_VALUES.items():
            if k in data and data[k] not in allowed:
                probs.append(f"{k}: {data[k]!r} not one of {sorted(map(str, allowed))}")
        if not isinstance(data.get("requirements_revision"), int):
            probs.append("requirements_revision isn't a number")
        probs += check_requests(data.get("changes"), "changes", with_outcome=True)
    elif data:
        probs.append(f"frontmatter doesn't parse: {data['__error__']}")
    heads = h2(body)
    probs += in_order(heads, PLAN_SECTIONS, "sections")
    extra = [h for h in heads if h not in PLAN_SECTIONS and h not in PLAN_OPTIONAL]
    if extra:
        probs.append(f"sections not in 11.2: {extra}")
    never = [h for h in heads + h3_under(body, "Architecture") if h in PLAN_NEVER]
    if never:
        probs.append(f"sections the plan never holds (11.4): {never}")
    probs += in_order(h3_under(body, "Architecture"), ARCH_SUBS, "Architecture")
    arch = section(body, "Architecture")
    dec = next((t for t in tables(arch) if t and t[0][:1] == ["Decision"]), None)
    if not dec:
        probs.append("Architecture Decisions: no table headed Decision")
    else:
        rows = [r[0] for r in dec[1:]]
        if rows != ARCH_DECISIONS:
            probs.append(f"Architecture Decisions rows {rows} != {ARCH_DECISIONS}")
    decomp = section(body, "Decomposition")
    dt = tables(decomp)
    domains = data and data.get("decomposition") == "domains" if isinstance(data, dict) else False
    if not domains:
        if not dt or dt[0][0] != DECOMP_COLS:
            probs.append(f"Decomposition columns {dt[0][0] if dt else None} != {DECOMP_COLS}")
        else:
            for r in dt[0][1:]:
                bo = r[5] if len(r) > 5 else ""
                if not BUILD_OUTPUT.match(bo):
                    probs.append(f"Decomposition {r[0]}: Build Output {bo!r} isn't a canonical value")
    # tasks
    tasks_text = section(body, "Tasks")
    blocks = re.split(r"^### ", tasks_text, flags=re.M)[1:]
    ids = []
    for b in blocks:
        head = b.split("\n", 1)[0]
        m = re.match(r"^(T\d+|KW|SCH) — .+", head)
        if not m:
            probs.append(f"task heading {head!r} isn't 'T[n] — [name]', 'KW — …' or 'SCH — …'")
            continue
        tid = m.group(1)
        ids.append(tid)
        fields = re.findall(r"^- \*\*([^*]+?):\*\*", b, re.M)
        if fields[:6] != TASK_FIELDS:
            probs.append(f"{tid}: fields {fields} != {TASK_FIELDS} (adopted: true may follow)")
        rev = re.search(r"^- \*\*rev:\*\* *(\S+)", b, re.M)
        if not rev or not rev.group(1).isdigit():
            probs.append(f"{tid}: rev isn't a number")
    if "KW" not in ids:
        probs.append("no KW task (11.5: in every plan)")
    nums = [int(t[1:]) for t in ids if t.startswith("T")]
    if nums != list(range(1, len(nums) + 1)):
        probs.append(f"tasks not numbered T1, T2… in order: {ids}")
    tail = [t for t in ids if not t.startswith("T")]
    if ids[len(nums):] != tail or (tail and tail not in (["KW"], ["KW", "SCH"])):
        probs.append(f"KW then SCH come after the numbered tasks: {ids}")
    # self-test summary
    sts = [l for l in section(body, "Self-Test Summary").split("\n") if l.startswith("- ")]
    if not sts or any(not re.match(r"^- [✓⚠]", l) for l in sts):
        probs.append("Self-Test Summary: one line per item, each ✓ or ⚠")
    # no copied requirement wording
    if requirements_text:
        for line in re.findall(r"^- (?:AC|R|G)\d+[^:]*: (.+)$", requirements_text, re.M):
            w = line.strip()
            if len(w.split()) >= 8 and w in text:
                probs.append(f"requirement wording copied into the plan: {w[:80]!r}")
    return probs


# ---------------------------------------------------------------- the build record

RECORD_KEYS = ["plan_revision", "last_close_after_round", "live_checks", "skills_on", "write_block", "schedule",
               "fingerprints", "bare_run", "run_folders", "change_requests"]
RECORD_COLS = ["Task", "Build Output", "Context ID", "Artifact", "Path or location", "Status", "Saved",
               "Built rev", "Last built after round", "Check", "Ruling"]
RECORD_STATUS = re.compile(r"^(Created|Reused|Extended|Installed by you|Built, misses .+|Waiting on .+|"
                           r"Waiting on change request \S+|Failed check|Not built yet|Removed from the plan)$")
SCHEDULE = re.compile(r"^(none|not-on|paused|safety-incomplete: .+)$")
OLDER = re.compile(r"^(- )?An older version: (none that you know of\.|.+(Switch it off for good when this one goes live\.|"
                   r"this one replaced it when it was installed on .+|you switched it off on .+))", re.M)


def check_build_record(text):
    probs = []
    fm, body = split_frontmatter(text)
    if fm is None:
        return ["no frontmatter"]
    keys = top_keys(fm)
    extra = [k for k in keys if k not in RECORD_KEYS]
    if extra:
        probs.append(f"frontmatter keys not in rules 6.4: {extra}")
    data = load_fm(fm)
    if isinstance(data, dict) and "__error__" not in data:
        if "schedule" in data and not SCHEDULE.match(str(data["schedule"])):
            probs.append(f"schedule: {data['schedule']!r} isn't none, not-on, paused or safety-incomplete: [points]")
        if "skills_on" in data and data["skills_on"] not in ("yes", True):
            probs.append(f"skills_on: {data['skills_on']!r} (only 'yes' once checked)")
        wb = data.get("write_block")
        if wb is not None and not (wb == "off" or str(wb).startswith("on")):
            probs.append(f"write_block: {wb!r} isn't off or on: [tools]")
        for k in ("plan_revision", "last_close_after_round"):
            if k in data and not isinstance(data[k], int):
                probs.append(f"{k} isn't a number")
        for k, v in (data.get("live_checks") or {}).items():
            if not re.match(r"^(done(: .+)?|declined|skipped|not yet)$", str(v)):
                probs.append(f"live_checks.{k}: {v!r} isn't done, declined, skipped or not yet")
        for k, v in (data.get("bare_run") or {}).items():
            if not re.match(r"^(done|skipped: .+)$", str(v)):
                probs.append(f"bare_run.{k}: {v!r} isn't done or skipped: [why]")
        probs += check_requests(data.get("change_requests"), "change_requests")
    heads = h2(body)
    if heads[:2] != ["What was built", "What it can access"]:
        probs.append(f"the record opens with 'What was built' then 'What it can access' (have {heads[:2]})")
    table = next((t for t in tables(body) if t and t[0][:1] == ["Task"]), None)
    if not table:
        probs.append("no parts table headed Task")
    else:
        if table[0] != RECORD_COLS:
            probs.append(f"table columns {table[0]} != {RECORD_COLS}")
        for r in table[1:]:
            if len(r) != len(RECORD_COLS):
                probs.append(f"row {r[:2]} has {len(r)} cells")
                continue
            if not RECORD_STATUS.match(r[5]):
                probs.append(f"row {r[0]} {r[3]!r}: Status {r[5]!r} isn't one of build 11's values")
            if r[6] not in ("yes", "no", "—", ""):
                probs.append(f"row {r[0]} {r[3]!r}: Saved {r[6]!r} isn't yes or no")
    built = section(body, "What was built")
    if "An older version:" in built and not OLDER.search(built):
        probs.append("the older-version line isn't in one of rules 6.4's forms")
    for banned in ("changed:",):
        if re.search(rf"^\s*{banned}", text, re.M):
            probs.append(f"'{banned}' markers are never in the record (rules 6.4)")
    return probs


# ---------------------------------------------------------------- the results file

RESULTS_KEYS = ["workflow", "round", "plan_revision", "date", "environment", "round_status", "round_kind",
                "readiness", "go_live", "direct_edit", "change_requests", "results"]
RESULTS_REQUIRED = ["workflow", "round", "plan_revision", "date", "environment", "round_status", "round_kind"]
RESULTS_VALUES = {"round_status": {"in-progress", "complete", "abandoned"},
                  "round_kind": {"first", "after-fix", "after-change", "regression"},
                  "readiness": {"ready", "not-ready", "waiting-on-access"},
                  "go_live": {"pending", "done"}, "direct_edit": {"undo"}}
RESULTS_SECTIONS = ["Check list", "Coverage", "Inputs", "Report card", "Not run", "Environment",
                    "Issues identified", "Accepted misses", "Requirement changes", "Verdict"]
ISSUES_COLS = ["Input", "Line", "Level", "Cause", "Task", "What to change"]


def check_results(text):
    probs = []
    fm, body = split_frontmatter(text)
    if fm is None:
        return ["no frontmatter"]
    keys = top_keys(fm)
    extra = [k for k in keys if k not in RESULTS_KEYS]
    if extra:
        probs.append(f"frontmatter keys not in rules 6.5: {extra} (counts are worked out, never stored)")
    missing = [k for k in RESULTS_REQUIRED if k not in keys]
    if missing:
        probs.append(f"frontmatter keys missing: {missing}")
    data = load_fm(fm)
    if isinstance(data, dict) and "__error__" not in data:
        for k, allowed in RESULTS_VALUES.items():
            if k in data and data[k] not in allowed:
                probs.append(f"{k}: {data[k]!r} not one of {sorted(allowed)}")
        for k in ("round", "plan_revision"):
            if k in data and not isinstance(data[k], int):
                probs.append(f"{k} isn't a number")
        for name, r in (data.get("results") or {}).items():
            if not (re.match(r"^E\d+$", str(name)) or name == "new"):
                probs.append(f"results key {name!r} isn't an E number or 'new'")
            if not isinstance(r, dict) or r.get("runs") not in (1, 2):
                probs.append(f"results.{name}: runs isn't 1 or 2")
                continue
            for run in [k for k in r if k.startswith("run") and k != "runs"]:
                for line, v in (r[run] or {}).items():
                    if v not in ("met", "not-met", "not-run"):
                        probs.append(f"results.{name}.{run}.{line}: {v!r} isn't met, not-met or not-run")
            if r.get("runs") == 2 and "run2" not in r:
                probs.append(f"results.{name}: runs 2 with no run2")
            if "edits" in r and r["edits"] not in ("none", "minor", "major"):
                probs.append(f"results.{name}.edits: {r['edits']!r}")
            extra_keys = set(r) - {"runs", "run1", "run2", "edits", "carried"}
            if extra_keys:
                probs.append(f"results.{name}: keys {sorted(extra_keys)} not in rules 6.5")
        probs += check_requests(data.get("change_requests"), "change_requests")
    heads = h2(body)
    if heads != RESULTS_SECTIONS:
        probs.append(f"sections {heads} != {RESULTS_SECTIONS} (test 9: in order, and no others)")
    for t in tables(section(body, "Issues identified")):
        if t[0] != ISSUES_COLS:
            probs.append(f"Issues identified columns {t[0]} != {ISSUES_COLS}")
        for r in t[1:]:
            if len(r) > 2 and r[2] not in ("build", "plan", "requirement"):
                probs.append(f"Issues row {r[:2]}: Level {r[2]!r} isn't build, plan or requirement")
    verdict = section(body, "Verdict").strip()
    if isinstance(data, dict) and data.get("round_status") == "in-progress":
        return probs  # the verdict is written in Part 3
    if not re.match(r"^(Ready|Not ready|Waiting on access)\b", verdict):
        probs.append(f"Verdict doesn't open with Ready, Not ready or Waiting on access: {verdict[:60]!r}")
    if verdict and not re.search(r"\b\d+ of \d+ lines met across \d+ inputs?\b", verdict):
        probs.append("Verdict has no '[n] of [m] lines met across [k] inputs'")
    return probs


# ---------------------------------------------------------------- the requirements file (T14)

def check_requirements(path, registry=None):
    """T14's requirements-check script; exit 0 valid, 1 invalid, 2 usage error."""
    if not REQUIREMENTS_CHECK.exists():
        return [f"requirements-check script missing: {REQUIREMENTS_CHECK}"]
    # The repo's package.json says "type": "module", so node would load the CommonJS script as an ES
    # module from here; run a .cjs copy instead (the script itself is T14's, unchanged).
    import tempfile
    tmp = Path(tempfile.mkdtemp()) / "requirements-check.cjs"
    tmp.write_text(REQUIREMENTS_CHECK.read_text())
    args = ["node", str(tmp), str(path)]
    if registry is not None:
        args.append("--registry" if registry else "--no-registry")
    r = subprocess.run(args, capture_output=True, text=True)
    shutil.rmtree(tmp.parent, ignore_errors=True)
    if r.returncode == 0:
        return []
    out = (r.stdout + r.stderr).strip().splitlines()
    return out or [f"requirements-check exited {r.returncode}"]


CHECKS = {"plan": check_plan, "build_record": check_build_record, "results": check_results}


def check_text(kind, text, **kw):
    if kind == "requirements":
        raise ValueError("requirements is checked from a path: use check_requirements")
    return CHECKS[kind](text, **kw) if kind == "plan" else CHECKS[kind](text)


def main(argv):
    if len(argv) < 2 or argv[0] not in list(CHECKS) + ["requirements"]:
        sys.exit(__doc__)
    kind, files = argv[0], [a for a in argv[1:] if not a.startswith("--")]
    bad = 0
    for f in files:
        probs = (check_requirements(f, False if "--no-registry" in argv else None) if kind == "requirements"
                 else check_text(kind, Path(f).read_text()))
        print(f"{f}: {'OK' if not probs else str(len(probs)) + ' problem(s)'}")
        for p in probs:
            print("   ", p)
        bad += bool(probs)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main(sys.argv[1:])
