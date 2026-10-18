#!/usr/bin/env python3
"""Quote check: every line an eval quotes word for word must still exist in the skill.

Run after every skill change and before any paid eval round:

    python3 check_quotes.py [evals.json ...]

Each `ai_contains` text (the word-for-word checks) is looked up in the Deconstruct skill's
SKILL.md and references/, with the same quote and dash normalisation the scripted checks use.
A few evals quote another source on purpose; QUOTE_SOURCES names those extra places per eval.
Exit 1 when any quote is missing, listing each one: the eval is out of date, or the skill
changed a line it shouldn't have. `ai_not_contains` texts are retired wording and are not
looked up.
"""
import json
import sys
from pathlib import Path

from check_scripted import qnorm

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SKILLS = ROOT / "plugins" / "handsonai" / "skills"

# Evals that quote something other than Deconstruct: the Analyze skill, or names in the fixtures.
QUOTE_SOURCES = {
    "NF1-analyze": [SKILLS / "analyze"],
    "R6": [HERE / "fixtures"],
    "R12": [HERE / "fixtures"],
}


def corpus(paths):
    text = []
    for p in paths:
        files = [p] if p.is_file() else sorted(f for f in p.rglob("*") if f.is_file())
        for f in files:
            try:
                text.append(f.read_text(errors="replace"))
            except OSError:
                pass
    return qnorm("\n".join(text))


def quotes(node, out):
    if isinstance(node, dict):
        if node.get("type") == "ai_contains":
            out.append(node["text"])
        for v in node.values():
            quotes(v, out)
    elif isinstance(node, list):
        for v in node:
            quotes(v, out)
    return out


def main(files):
    base = corpus([SKILLS / "deconstruct"])
    extra = {}
    missing = []
    for f in files:
        for ev in json.load(open(f))["evals"]:
            text = base
            if ev["id"] in QUOTE_SOURCES:
                extra.setdefault(ev["id"], corpus(QUOTE_SOURCES[ev["id"]]))
                text = base + "\n" + extra[ev["id"]]
            for q in quotes(ev, []):
                if qnorm(q) not in text:
                    missing.append((Path(f).name, ev["id"], q))
    for f, eid, q in missing:
        print(f"{f} {eid}: not in the skill: {q[:120]!r}")
    print(f"{len(missing)} quote(s) missing")
    return 1 if missing else 0


if __name__ == "__main__":
    args = sys.argv[1:] or [str(HERE / "evals.json"), str(HERE / "evals-local.json")]
    sys.exit(main([a for a in args if Path(a).exists()]))
