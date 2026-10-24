#!/usr/bin/env python3
"""The quote check on scripted lines (rules 2.3, 14: core). It reads approved-lines.json only, never
the skills, with placeholders as wildcards.

  python3 check_quotes.py transcript <transcript.md | turns.json | run folder>...
      Every scripted line in the AI's messages is the approved line, word for word: a run of six
      or more fixed words from an approved line said with a word or two changed fails, naming the
      line, the approved words and what was said.

  python3 check_quotes.py evals <evals.json>...
      The evals are in step with the corpus: every `quote` check names a line and form that exist;
      every `ai_contains` marked with `line` matches that line's wording; and no `ai_contains` text
      quotes an approved line with a word changed (a stale quote).

  --corpus FILE   another approved-lines.json (tests)

Exit 1 when anything fails. Run it after every skill change and before any paid eval round; the
runner also applies it to every run as a built-in check.
"""
import argparse
import json
import re
import sys
from pathlib import Path

import approved_lines as AL


def ai_messages(path):
    p = Path(path)
    if p.is_dir():
        out = []
        for f in sorted(p.rglob("turns.json")):
            out += ai_messages(f)
        return out
    if p.suffix == ".json":
        return [t["text"] for t in json.loads(p.read_text()) if t.get("role") == "ai"]
    # transcript.md: "## AI" sections
    parts = re.split(r"^## (AI|Student|Leader|Harness)\s*$", p.read_text(), flags=re.M)
    return [parts[i + 1].strip() for i in range(1, len(parts) - 1, 2) if parts[i] == "AI"]


def check_transcripts(corpus, paths):
    bad = 0
    for path in paths:
        for i, m in enumerate(ai_messages(path), 1):
            for ln, exp, got in corpus.near_misses(m):
                bad += 1
                print(f"{path} AI message {i}: {ln.label()} said with words changed:\n"
                      f"    approved: {exp}\n    said:     {got}")
    return bad


def _walk(node, out):
    if isinstance(node, dict):
        if node.get("type") in ("ai_contains", "quote", "quote_absent"):
            out.append(node)
        for v in node.values():
            _walk(v, out)
    elif isinstance(node, list):
        for v in node:
            _walk(v, out)
    return out


def check_evals(corpus, files):
    bad = 0
    for f in files:
        for ev in json.loads(Path(f).read_text())["evals"]:
            for c in _walk(ev.get("expectations", []), []):
                where = f"{Path(f).name} {ev['id']}"
                if c["type"] in ("quote", "quote_absent"):
                    if not [x for x in corpus.get(c["id"], c.get("form")) if x.text]:
                        bad += 1
                        print(f"{where}: no approved line {c['id']} ({c.get('form', 'any form')})")
                    continue
                text = c["text"]
                if c.get("line"):
                    forms = [x for x in corpus.get(c["line"]) if x.text]
                    if not forms:
                        bad += 1
                        print(f"{where}: ai_contains names unknown line {c['line']}")
                    elif not any(re.search(AL.to_regex(x.toks), AL.norm(text), re.I | re.S) or
                                 AL.norm(text).lower() in AL.norm(x.text).lower() for x in forms):
                        bad += 1
                        print(f"{where}: ai_contains doesn't match {c['line']}'s approved wording: {text[:100]!r}")
                for ln, exp, got in corpus.near_misses(text):
                    if exp.startswith(got) or exp.endswith(got):
                        continue  # an eval may quote part of a line
                    bad += 1
                    print(f"{where}: ai_contains quotes {ln.label()} with words changed:\n"
                          f"    approved: {exp}\n    eval has: {got}")
    return bad


def main(argv=None):
    ap = argparse.ArgumentParser(description="The quote check, against approved-lines.json only.")
    ap.add_argument("mode", choices=["transcript", "evals"])
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--corpus", default=str(AL.DEFAULT_CORPUS))
    a = ap.parse_args(argv)
    corpus = AL.Corpus(a.corpus)
    bad = (check_transcripts if a.mode == "transcript" else check_evals)(corpus, a.paths)
    print(f"{bad} problem(s)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
