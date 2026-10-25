#!/usr/bin/env python3
"""Check evals.json files without running anything (no model calls).

Usage: python3 framework-evals/validate_evals.py <evals.json>... [--build-fixtures] [--strict-tiers] [--only ID,...]

Checks: required keys; ids unique; `tier` is core or regression (missing: a warning, taken as the
file's `default_tier` or regression; --strict-tiers makes it an error); every expectation is
{text, kind} with kind scripted or judged; every scripted expectation has a `check` of a known type
with its required fields (regexes compile; `quote` ids exist in approved-lines.json; `no_yaml` is
retired); `must`/`gating` are booleans; leader scripts and `files` paths exist; fixture names are
known to the file's fixture builder (`dir:` fixtures exist); `fixture_from` paths are present or name
a run folder; `platform`, `platform_faults` and `leader_runs` are known; `action_target` is {figure, journey}. An
eval marked `"retired"` is skipped (kept in place with its note). With --build-fixtures, every
fixture is built into a temp folder.
"""
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import approved_lines as AL
import check_scripted as CS
import harness as H
import leader as L

REQUIRED = {
    "ai_contains": ["text"], "ai_not_contains": ["text"], "ai_regex": ["pattern"], "ai_not_regex": ["pattern"], "leader_regex": ["pattern"],
    "quote": ["id"], "quote_absent": ["id"], "scripted_lines": [], "vocabulary": [], "no_time_or_step_numbers": [],
    "signposts": [], "file_exists": ["path"], "file_absent": ["path"], "file_existed_during": ["path"],
    "file_contains": ["path", "text"], "file_not_contains": ["path", "text"], "file_regex": ["path", "pattern"],
    "file_not_regex": ["path", "pattern"], "sections_in_order": ["path", "headings"], "yaml_keys": ["path", "keys"],
    "structure": ["path", "kind"], "fill_check": ["kind"],
    "file_unchanged": ["path"], "no_added_files": [], "file_line": ["path", "line", "pattern"],
    "section_regex": ["path", "section", "pattern"], "all": ["checks"], "any": ["checks"],
    "release_check": ["ids", "passed", "open"],
}
RETIRED = {"no_yaml": "retired: use yaml_keys (every framework file has frontmatter now)"}
FAULTS = {"no_folder_added", "cowork_cannot_read_onedrive", "attach_fails", "agent_builder_missing_context_file",
          "agent_builder_rewords_carried_line", "agent_builder_rewords_after_fix",
          "agent_builder_requirements_under_knowledge", "agent_builder_ordinary_chat", "skill_cannot_read_by_path",
          "no_gmail", "leader_denies_settings_prompt"}


def check_check(c, where, errs, nsessions, corpus):
    t = c.get("type")
    if t in RETIRED:
        errs.append(f"{where}: {t} is {RETIRED[t]}")
        return
    if t not in REQUIRED:
        errs.append(f"{where}: unknown check type {t!r}")
        return
    for k in REQUIRED[t]:
        if k not in c:
            errs.append(f"{where}: {t} needs {k!r}")
    if "pattern" in c:
        try:
            re.compile(c["pattern"])
        except re.error as e:
            errs.append(f"{where}: bad regex {c['pattern']!r}: {e}")
    if t in ("quote", "quote_absent") and "id" in c and not [x for x in corpus.get(c["id"], c.get("form")) if x.text]:
        errs.append(f"{where}: no approved line {c['id']} ({c.get('form', 'any form')})")
    if t == "quote" and c.get("ending") and not [x for x in corpus.get(c["id"], c["ending"]) if x.text and x.fragment]:
        errs.append(f"{where}: no fragment form {c['ending']!r} of {c['id']}")
    if t == "ai_contains" and c.get("line") and not corpus.get(c["line"]):
        errs.append(f"{where}: ai_contains names unknown line {c['line']}")
    if t == "structure" and c.get("kind") not in ("plan", "build_record", "results", "requirements"):
        errs.append(f"{where}: structure kind {c.get('kind')!r}")
    if t == "fill_check" and c.get("kind") not in ("build", "fix"):
        errs.append(f"{where}: fill_check kind {c.get('kind')!r}")
    if t == "signposts" and c.get("skill", "deconstruct") not in ("deconstruct", "design", "test", "build"):
        errs.append(f"{where}: signposts skill {c.get('skill')!r}")
    if "session" in c and not (isinstance(c["session"], int) and 1 <= c["session"] <= nsessions):
        errs.append(f"{where}: session {c['session']} out of range 1..{nsessions}")
    for i, sub in enumerate(c.get("checks", [])):
        check_check(sub, f"{where}.checks[{i}]", errs, nsessions, corpus)
    for k in ("passed", "open"):
        if t == "release_check" and isinstance(c.get(k), dict):
            check_check(c[k], f"{where}.{k}", errs, nsessions, corpus)


def check_release_item(rc, where, errs):
    """A judged expectation's or precondition's `release_check: {ids, passed, open}` (text or null each)."""
    if not (isinstance(rc, dict) and isinstance(rc.get("ids"), list) and rc["ids"]
            and all(isinstance(i, int) for i in rc["ids"])):
        errs.append(f"{where}: release_check needs ids, a list of release check numbers")
        return
    for k in ("passed", "open"):
        if k not in rc or not (rc[k] is None or isinstance(rc[k], str)):
            errs.append(f"{where}: release_check {k!r} must be a text or null")
    known = {r["id"] for r in json.loads(CS.REGISTRY.read_text()).get("release_checks", [])}
    for i in rc["ids"]:
        if i not in known:
            errs.append(f"{where}: release check {i} isn't in the platform registry")


def fixture_names(evals_dir, builder):
    maker = evals_dir / (builder or "fixtures/make_fixture.py")
    if not maker.exists():
        return maker, None
    r = subprocess.run([sys.executable, str(maker), "--list"], capture_output=True, text=True)
    return maker, set(r.stdout.split())


def validate_file(path, build=False, strict_tiers=False, only=None, warnings=None):
    """The problems in one evals.json (and warnings, appended to `warnings`)."""
    errs = []
    warnings = warnings if warnings is not None else []
    corpus = AL.load()
    path = Path(path).resolve()
    d = path.parent
    data = json.loads(path.read_text())
    for k in ("skill_name", "how_to_run", "evals"):
        if k not in data:
            errs.append(f"{path.name}: missing {k}")
    if data.get("default_tier") not in (None, "core", "regression"):
        errs.append(f"{path.name}: default_tier {data['default_tier']!r}")
    maker, names = fixture_names(d, data.get("fixture_builder"))
    seen, used = set(), set()
    for ev in data.get("evals", []):
        eid = ev.get("id", "?")
        w = f"{path.name}:{eid}"
        if eid in seen:
            errs.append(f"{w}: duplicate id")
        seen.add(eid)
        if ev.get("retired"):
            continue
        if only and eid not in only:
            continue
        tier = ev.get("tier")
        if tier is None:
            msg = f"{w}: no tier (taken as {data.get('default_tier') or 'regression'})"
            (errs if strict_tiers and not data.get("default_tier") else warnings).append(msg)
        elif tier not in ("core", "regression"):
            errs.append(f"{w}: tier {tier!r} isn't core or regression")
        for k in ("id", "name", "expected_output", "expectations", "files"):
            if k not in ev:
                errs.append(f"{w}: missing {k}")
        if "prompt" not in ev and "sessions" not in ev:
            errs.append(f"{w}: needs prompt or sessions")
        sessions = ev.get("sessions") or [{}]
        if ev.get("student") and not (d / ev["student"]).exists():
            errs.append(f"{w}: leader script missing {ev['student']}")
        for p in ev.get("files", []):
            if not (d / p).exists():
                errs.append(f"{w}: files entry missing {p}")
        for x in [ev.get("platform")] + [s.get("platform") for s in sessions]:
            if x and x not in L.PLATFORMS:
                errs.append(f"{w}: unknown platform {x!r} (one of {sorted(L.PLATFORMS)})")
        for x in [ev] + sessions:
            if "leader_runs" in x and x["leader_runs"] not in L.LEADER_RUN_MODES:
                errs.append(f"{w}: leader_runs {x['leader_runs']!r} (one of {list(L.LEADER_RUN_MODES)})")
        for x in [ev] + sessions:
            for tool in x.get("stub_tools", []):
                if tool not in H.STUB_EXTRA_TOOLS:
                    errs.append(f"{w}: unknown stub_tools entry {tool!r} (one of {sorted(H.STUB_EXTRA_TOOLS)})")
        for f in ev.get("platform_faults", []):
            if f not in FAULTS:
                errs.append(f"{w}: unknown platform fault {f!r}")
        at = ev.get("action_target")
        if at is not None and not (isinstance(at, dict) and isinstance(at.get("figure"), (int, float)) and at.get("journey")):
            errs.append(f"{w}: action_target must be {{figure: number, journey: text}}")
        for x in [ev.get("fixture")] + [s.get("fixture") for s in sessions]:
            if not x or x == "empty":
                continue
            used.add(x)
            if x.startswith("dir:"):
                if not (d / x[4:]).is_dir():
                    errs.append(f"{w}: fixture folder missing {x}")
            elif names is None:
                errs.append(f"{w}: fixture {x!r} needs a fixture builder, and {maker} doesn't exist")
            elif x not in names:
                errs.append(f"{w}: fixture {x!r} unknown to {maker.name}")
        for i, s in enumerate(sessions, 1):
            if isinstance(s.get("student"), str) and not (d / s["student"]).exists():
                errs.append(f"{w}: session {i} leader script missing {s['student']}")
            if ev.get("sessions") and "prompt" not in s:
                errs.append(f"{w}: session {i} has no prompt")
            ff = s.get("fixture_from")
            if ff and not (d / ff).exists() and "iteration-" not in ff and "run-" not in ff:
                errs.append(f"{w}: session {i} fixture_from {ff} not found")
        if not ev.get("expectations"):
            errs.append(f"{w}: no expectations")
        for i, x in enumerate(ev.get("expectations", []), 1):
            xw = f"{w} expectation {i}"
            if isinstance(x, str):
                continue  # a plain string is a judged expectation
            if not isinstance(x, dict) or "text" not in x or x.get("kind") not in ("scripted", "judged"):
                errs.append(f"{xw}: must be {{text, kind: scripted|judged}}")
                continue
            for flag in ("must", "gating"):
                if flag in x and not isinstance(x[flag], bool):
                    errs.append(f"{xw}: {flag} is not a boolean")
            if x["kind"] == "scripted":
                if "check" not in x:
                    errs.append(f"{xw}: scripted with no check")
                else:
                    check_check(x["check"], xw, errs, len(sessions), corpus)
            elif "check" in x:
                errs.append(f"{xw}: judged expectation carries a check")
            if "release_check" in x:
                if x["kind"] != "judged":
                    errs.append(f"{xw}: a release_check item is judged (a scripted one uses the release_check check)")
                check_release_item(x["release_check"], xw, errs)
        for p in ev.get("preconditions", []):
            if isinstance(p, dict) and set(p) == {"release_check"}:
                check_release_item(p["release_check"], f"{w} precondition", errs)
            elif not isinstance(p, str):
                errs.append(f"{w}: precondition must be a string or {{release_check: {{ids, passed, open}}}}")
    if build and names is not None:
        for x in sorted(used):
            if x.startswith("dir:"):
                continue
            with tempfile.TemporaryDirectory() as t:
                r = subprocess.run([sys.executable, str(maker), x, str(Path(t) / "ws")], capture_output=True, text=True)
                if r.returncode != 0:
                    errs.append(f"{path.name}: fixture {x} failed to build: {r.stderr[-300:]}")
    return errs


def main():
    files = [a for a in sys.argv[1:] if not a.startswith("--") and not a.startswith("ID=")]
    only = None
    if "--only" in sys.argv:
        only = set(sys.argv[sys.argv.index("--only") + 1].split(","))
        files = [f for f in files if f != sys.argv[sys.argv.index("--only") + 1]]
    errs, warns = [], []
    for f in files:
        e = validate_file(f, "--build-fixtures" in sys.argv, "--strict-tiers" in sys.argv, only, warns)
        errs += e
        n = len(json.loads(Path(f).read_text()).get("evals", []))
        print(f"{f}: {n if not only else len(only)} evals checked, {len(e)} errors")
    for w in warns:
        print("warning", w)
    for e in errs:
        print("ERROR", e)
    print("OK" if not errs else f"{len(errs)} errors")
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
