#!/usr/bin/env python3
"""Grade a run from run_eval.py against its checklist.

Usage: python3 grade_eval.py <out-dir>

A grader (`claude -p`, read-only) gets the eval's expectations, each session's transcript,
and every file the run added, changed or removed. It marks each expectation passed or not,
with evidence quoted from the transcript or files. Writes <out-dir>/grading.json in the
same shape as analyze-workspace (expectations: text, passed, evidence) and prints a summary.
"""
import filecmp
import json
import re
import subprocess
import sys
from pathlib import Path

GRADER = """You grade a test run of an AI skill against a checklist. Be strict and literal:
an expectation that quotes wording passes only if that wording appears (small punctuation
differences aside). An expectation about a file passes only if the file shows it. If the run
stopped before the point an expectation is about, mark it failed with evidence "not reached".
Return only JSON: {"expectations": [{"text": ..., "passed": true|false, "evidence": ...}]},
one entry per expectation, in the order given."""


def changed_files(start, end):
    out = []
    for p in sorted(end.rglob("*")):
        if p.is_file():
            rel = p.relative_to(end)
            s = start / rel
            if not s.exists():
                out.append(("added", rel, p))
            elif not filecmp.cmp(s, p, shallow=False):
                out.append(("changed", rel, p))
    for p in sorted(start.rglob("*")):
        if p.is_file() and not (end / p.relative_to(start)).exists():
            out.append(("removed", p.relative_to(start), None))
    return out


def main():
    out = Path(sys.argv[1])
    ev = json.loads((out / "eval.json").read_text())
    parts = [f"# Eval {ev['id']} — {ev['name']}\n\nExpected: {ev['expected_output']}\n\n## Expectations\n"]
    parts += [f"{i}. {x}" for i, x in enumerate(ev["expectations"], 1)]
    for d in sorted(out.glob("session-*")):
        parts.append(f"\n# {d.name}\n\n## Transcript\n\n{(d / 'transcript.md').read_text()}\n\n## Files the run touched\n")
        for kind, rel, p in changed_files(d / "workspace-start", d / "workspace"):
            body = p.read_text(errors="replace")[:20000] if p else ""
            parts.append(f"### {kind}: {rel}\n\n```\n{body}\n```\n")
    r = subprocess.run(["claude", "-p", "--setting-sources", "project,local", "--output-format", "json",
                        "--system-prompt", GRADER, "--allowedTools", "Read"],
                       input="\n".join(parts), capture_output=True, text=True, timeout=1800)
    if r.returncode != 0:
        sys.exit(r.stderr[-2000:])
    text = json.loads(r.stdout)["result"]
    m = re.search(r"\{.*\}", text, re.S)
    grading = json.loads(m.group(0))
    (out / "grading.json").write_text(json.dumps(grading, indent=2, ensure_ascii=False))
    passed = sum(1 for e in grading["expectations"] if e["passed"])
    print(f"{ev['id']}: {passed}/{len(grading['expectations'])} passed")
    for e in grading["expectations"]:
        print(("PASS " if e["passed"] else "FAIL ") + e["text"][:110])


if __name__ == "__main__":
    main()
