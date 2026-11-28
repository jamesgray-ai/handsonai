#!/usr/bin/env python3
"""Propose the release gate's safety tests, for James to approve (shape release G1). Dev-only.

  python3 framework-evals/tools/list_safety_candidates.py <evals.json>... [--named ID,ID]

Prints a Markdown table per skill of every non-retired core eval: id, name, platform, what it
covers, and Proposed (yes when its id prefix, name, or covers point at something that
protects the leader, or when --named lists it). It proposes only: nothing is tagged until James
approves the list and `"safety": true` is set by hand.
"""
import argparse
import json
import re
from pathlib import Path

PREFIXES = ("LS-", "SEC-", "RA-", "TS-")
WORDS = re.compile(r"send|post|delete|irreversible|can't be undone|confidential|secret|password|"
                   r"fail.closed|schedule|unattended|approv|gate|go.live|live change|outside content|"
                   r"planted|\blaw\b|regulat", re.I)


def _text(ev):
    # the name and what it covers only: nearly every eval's expectations mention an approval or a
    # checkpoint, which proposed 138 of 327 core tests against the 46 of 10.5.0's final rounds
    covers = ev.get("covers") or []
    covers = covers if isinstance(covers, list) else [covers]
    return " ".join([ev.get("name", "")] + [str(c) for c in covers])


def candidates(path, named=frozenset()):
    data = json.loads(Path(path).read_text())
    rows = []
    for ev in data["evals"]:
        if ev.get("retired") or (ev.get("tier") or data.get("default_tier") or "regression") != "core":
            continue
        why = ("named in the release notes" if ev["id"] in named
               else "id prefix" if ev["id"].startswith(PREFIXES)
               else (lambda m: f"mentions '{m.group(0)}'" if m else "")(WORDS.search(_text(ev))))
        plats = {ev.get("platform")} | {s.get("platform") for s in ev.get("sessions") or []}
        rows.append({"id": ev["id"], "name": ev.get("name", ""), "proposed": bool(why), "why": why,
                     "platform": ", ".join(sorted(p for p in plats if p)) or "default",
                     "skill": data.get("skill_name", Path(path).parent.parent.name)})
    return rows


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--named", default="")
    a = ap.parse_args(argv)
    named = {x.strip() for x in a.named.split(",") if x.strip()}
    for p in a.paths:
        rows = candidates(p, named)
        if not rows:
            continue
        yes = sum(r["proposed"] for r in rows)
        print(f"### {rows[0]['skill']}: {yes} proposed of {len(rows)} core tests\n")
        print("| Proposed | Test | Name | Platform | Why |\n|---|---|---|---|---|")
        for r in sorted(rows, key=lambda r: (not r["proposed"], r["id"])):
            print(f"| {'**yes**' if r['proposed'] else 'no'} | {r['id']} | {r['name']} | {r['platform']} | {r['why']} |")
        print()


if __name__ == "__main__":
    main()
