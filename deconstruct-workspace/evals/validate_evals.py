#!/usr/bin/env python3
"""Check evals.json files without running anything (no model calls).

Usage: python3 validate_evals.py <evals.json>... [--build-fixtures]

Checks: required keys; ids unique; every expectation is {text, kind} with kind scripted or
judged; every scripted expectation has a `check` of a known type with its required fields
(and its regexes compile); `must` is a boolean if present; student and `files` paths exist;
fixture names are known to the file's fixture builder (`dir:` fixtures exist); `fixture_from`
paths are either present or name a run folder (produced at run time). With --build-fixtures,
every fixture is built into a temp folder.
"""
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent

REQUIRED = {
    "ai_contains": ["text"], "ai_not_contains": ["text"], "ai_regex": ["pattern"], "ai_not_regex": ["pattern"],
    "signposts": [], "file_exists": ["path"], "file_absent": ["path"], "file_existed_during": ["path"],
    "file_contains": ["path", "text"], "file_not_contains": ["path", "text"], "file_regex": ["path", "pattern"],
    "file_not_regex": ["path", "pattern"], "sections_in_order": ["path", "headings"], "no_yaml": ["path"],
    "file_unchanged": ["path"], "no_added_files": [], "file_line": ["path", "line", "pattern"], "all": ["checks"], "any": ["checks"],
}


def check_check(c, where, errs, nsessions):
    t = c.get("type")
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
    if "session" in c and not (isinstance(c["session"], int) and 1 <= c["session"] <= nsessions):
        errs.append(f"{where}: session {c['session']} out of range 1..{nsessions}")
    for i, sub in enumerate(c.get("checks", [])):
        check_check(sub, f"{where}.checks[{i}]", errs, nsessions)


def fixture_names(evals_dir, builder):
    maker = evals_dir / (builder or "fixtures/make_fixture.py")
    if not maker.exists():
        maker = HERE / "fixtures" / "make_fixture.py"
    r = subprocess.run([sys.executable, str(maker), "--list"], capture_output=True, text=True)
    return maker, set(r.stdout.split())


def main():
    files = [a for a in sys.argv[1:] if not a.startswith("--")]
    build = "--build-fixtures" in sys.argv
    errs = []
    for f in files:
        path = Path(f).resolve()
        d = path.parent
        data = json.loads(path.read_text())
        for k in ("skill_name", "how_to_run", "evals"):
            if k not in data:
                errs.append(f"{f}: missing {k}")
        maker, names = fixture_names(d, data.get("fixture_builder"))
        seen = set()
        used = set()
        for ev in data.get("evals", []):
            eid = ev.get("id", "?")
            w = f"{path.name}:{eid}"
            if eid in seen:
                errs.append(f"{w}: duplicate id")
            seen.add(eid)
            for k in ("id", "name", "expected_output", "expectations", "files"):
                if k not in ev:
                    errs.append(f"{w}: missing {k}")
            if "prompt" not in ev and "sessions" not in ev:
                errs.append(f"{w}: needs prompt or sessions")
            sessions = ev.get("sessions") or [{}]
            if ev.get("student") and not (d / ev["student"]).exists():
                errs.append(f"{w}: student script missing {ev['student']}")
            for p in ev.get("files", []):
                if not (d / p).exists():
                    errs.append(f"{w}: files entry missing {p}")
            fx = [ev.get("fixture")] + [s.get("fixture") for s in sessions]
            for x in fx:
                if not x or x == "empty":
                    continue
                used.add(x)
                if x.startswith("dir:"):
                    if not (d / x[4:]).is_dir():
                        errs.append(f"{w}: fixture folder missing {x}")
                elif x not in names:
                    errs.append(f"{w}: fixture {x!r} unknown to {maker.name}")
            for i, s in enumerate(sessions, 1):
                if isinstance(s.get("student"), str) and not (d / s["student"]).exists():
                    errs.append(f"{w}: session {i} student script missing {s['student']}")
                if ev.get("sessions") and "prompt" not in s:
                    errs.append(f"{w}: session {i} has no prompt")
                ff = s.get("fixture_from")
                if ff and not (d / ff).exists() and "iteration-" not in ff and "run-" not in ff:
                    errs.append(f"{w}: session {i} fixture_from {ff} not found")
            if not ev.get("expectations"):
                errs.append(f"{w}: no expectations")
            for i, x in enumerate(ev.get("expectations", []), 1):
                xw = f"{w} expectation {i}"
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
                        check_check(x["check"], xw, errs, len(sessions))
                elif "check" in x:
                    errs.append(f"{xw}: judged expectation carries a check")
            for p in ev.get("preconditions", []):
                if not isinstance(p, str):
                    errs.append(f"{w}: precondition must be a string")
        if build:
            for x in sorted(used):
                with tempfile.TemporaryDirectory() as t:
                    if x.startswith("dir:"):
                        continue
                    r = subprocess.run([sys.executable, str(maker), x, str(Path(t) / "ws")],
                                       capture_output=True, text=True)
                    if r.returncode != 0:
                        errs.append(f"{path.name}: fixture {x} failed to build: {r.stderr[-300:]}")
        print(f"{f}: {len(data.get('evals', []))} evals checked")
    for e in errs:
        print("ERROR", e)
    print("OK" if not errs else f"{len(errs)} errors")
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
