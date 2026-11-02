#!/usr/bin/env python3
"""check-line-placement.py — the placement check (rules 2.3; build-task-list T35).

Every approved line in framework-evals/approved-lines.json names, for each skill that says it,
the one file that holds it (`files`: {skill: path inside the skill folder}). This confirms each
line is in that file word for word, so a skill's copy of a scripted line can't drift from the
approved wording without failing CI.

Matching reuses framework-evals/approved_lines.py, the same rules the quote check uses:
- `[...]` is a placeholder and matches anything (here, at most HOLE_MAX characters, so a hole
  can't stretch across half a file to stitch a line together from unrelated text);
- `[Label: '...']` is a clause said only in that case: its own text or nothing;
- `...` and the ellipsis character are elisions and match anything (same bound);
- both sides are compared after approved_lines.norm (quotes, dashes, `**`, backticks and
  whitespace normalised), case-insensitively.
Fragment forms (`"fragment": true`, a platform's substitution inside another line, such as
"in a new session") aren't lines on their own and are skipped, as the quote check skips them.
The skill file is read with Markdown blockquote markers ('> ') stripped at line starts, so a
line quoted across several blockquote lines still matches.

Skills whose rewrite hasn't landed are listed in scripts/line-placement-pending.txt: their
missing lines are reported, not failed. A listed skill that already holds every line fails
the check, so the list has to shrink as the rewrites land.

Usage:
  python3 scripts/check-line-placement.py              # check, honouring the pending list
  python3 scripts/check-line-placement.py --strict     # ignore the pending list
  python3 scripts/check-line-placement.py --quiet      # summaries and failures only
  python3 scripts/check-line-placement.py --corpus F --pending F --skills-dir D

Exit codes: 0 every line in place (pending skills aside), 1 a line missing or drifted,
2 usage error or the corpus can't be read.
"""
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "framework-evals"))
import approved_lines as al  # noqa: E402  (the corpus's own matcher)

HOLE_MAX = 600


def bounded_regex(toks):
    out = []
    for t in toks:
        if t[0] == "lit":
            out.append(al._lit_regex(t[1]))
        elif t[0] == "hole":
            out.append(r".{0,%d}?" % HOLE_MAX)
        else:
            out.append("(?:" + bounded_regex(t[1]) + ")?")
    return "".join(out)


def read_pending(path):
    names = []
    if not path.exists():
        return names
    for raw in path.read_text().splitlines():
        name = raw.split("#", 1)[0].strip()
        if name:
            names.append(name)
    return names


def file_text(path, cache={}):
    if path not in cache:
        if not path.is_file():
            cache[path] = None
        else:
            raw = path.read_text(encoding="utf-8")
            raw = re.sub(r"(?m)^[ \t]*(?:>[ \t]?)+", "", raw)
            cache[path] = al.norm(raw)
    return cache[path]


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--corpus", default=str(ROOT / "framework-evals" / "approved-lines.json"))
    ap.add_argument("--pending", default=str(ROOT / "scripts" / "line-placement-pending.txt"))
    ap.add_argument("--skills-dir", default=str(ROOT / "plugins" / "handsonai" / "skills"))
    ap.add_argument("--strict", action="store_true", help="ignore the pending list")
    ap.add_argument("--quiet", action="store_true", help="print summaries and failures only")
    args = ap.parse_args()

    try:
        corpus = al.Corpus(args.corpus)
    except Exception as e:  # unreadable or malformed corpus: the check can't run
        print(f"Error: can't read the corpus {args.corpus}: {e}", file=sys.stderr)
        return 2

    skills_dir = Path(args.skills_dir)
    pending = set() if args.strict else set(read_pending(Path(args.pending)))
    for name in sorted(pending):
        if not (skills_dir / name).is_dir():
            print(f"  note  pending list names '{name}', which has no skill folder")

    results = {}  # skill -> {"ok": n, "missing": [(label, file, why)]}
    corpus_errors = []
    fragments = 0
    for ln in corpus.lines:
        if not ln.text:
            continue  # a row with no wording (the extraction warnings say which); nothing to place
        if ln.fragment:
            fragments += 1
            continue  # a platform substitution inside another line, not a line: the quote check skips it too
        if getattr(ln, "derived", False):
            continue  # a form the corpus builds from another one (a platform's refuse label): its source form is placed
        for skill in ln.skills:
            if skill != "built-workflow" and skill not in ln.files:
                corpus_errors.append(f"{ln.label()}: used by '{skill}' but names no file for it")
        rx = None
        for skill, rel in sorted(ln.files.items()):
            r = results.setdefault(skill, {"ok": 0, "missing": []})
            text = file_text(skills_dir / skill / rel)
            if text is None:
                r["missing"].append((ln.label(), rel, "file not found"))
                continue
            longest = max((al.norm(x) for x in al.literal_segments(ln.toks)), key=len, default="")
            if longest and longest.lower() not in text.lower():
                r["missing"].append((ln.label(), rel, "not in file"))
                continue
            if rx is None:
                rx = re.compile(bounded_regex(ln.toks), re.S | re.I)
            if rx.search(text):
                r["ok"] += 1
            else:
                r["missing"].append((ln.label(), rel, "not in file"))

    fails = 0
    print("approved-line placement (framework-evals/approved-lines.json)")
    for err in corpus_errors:
        print(f"  FAIL  corpus: {err}")
        fails += 1
    for skill in sorted(results):
        r = results[skill]
        total = r["ok"] + len(r["missing"])
        is_pending = skill in pending
        if not r["missing"]:
            if is_pending:
                print(f"  FAIL  {skill}: all {total} lines in place, but it's still on the pending list "
                      f"(remove it from scripts/line-placement-pending.txt)")
                fails += 1
            else:
                print(f"  ok    {skill}: all {total} lines in place")
            continue
        if is_pending:
            print(f"  pend  {skill}: {r['ok']} of {total} in place, {len(r['missing'])} missing "
                  f"(report only: rewrite not landed)")
        else:
            print(f"  FAIL  {skill}: {r['ok']} of {total} in place, {len(r['missing'])} missing or drifted")
            fails += 1
        if not is_pending or not args.quiet:
            by_file = {}
            for label, rel, why in r["missing"]:
                by_file.setdefault((rel, why), []).append(label)
            for (rel, why), labels in sorted(by_file.items()):
                print(f"        {rel} ({why}): {', '.join(labels)}")
    print(f"  ({fragments} fragment forms skipped: substitutions inside another line, as in the quote check)")
    if pending:
        print(f"  ({len(pending)} skill(s) on the pending list: {', '.join(sorted(pending))})")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
