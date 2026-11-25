"""Round metrics, the same measure for a baseline round and any later round. Read-only, no model call.
usage: round_metrics.py <round-dir> [--detail]

Each run's results are its latest re-grade (highest -vN tag) where one exists, else the round's own.
- pass rate: evals where every expectation passed in every run.
- clean runs: runs with every expectation passed.
- reworded-line rate: runs failing the quote check ("Every scripted line the AI says is the approved line").
- narration rate: runs with an AI message holding a note to itself: the checker's own narration hits
  (check_scripted.narration_hits) or a paragraph opening "Now <verb>…" (not "Now that"), "Write/Edit/Update the
  … node", "State <n>", "Need …" or "Save the edited text to history".
"""
import json, glob, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_scripted as CS

R = sys.argv[1].rstrip("/")
detail = "--detail" in sys.argv
QUOTE = "Every scripted line the AI says is the approved line"
NOTE = re.compile(r"^\W*(Now (?!that\b)[a-z]+|(?:Write|Edit|Update) the (?:[\w']+ ){0,2}node\b|State \d+\b|Need |"
                  r"Save the edited text to history)")


def latest(rdir, stem):
    tagged = sorted(glob.glob(f"{rdir}/{stem}-v*.json"), key=lambda p: int(re.search(r"-v(\d+)\.json$", p).group(1)))
    return tagged[-1] if tagged else f"{rdir}/{stem}.json"


def narrates(rdir):
    hits = []
    for f in sorted(glob.glob(f"{rdir}/session-*/turns.json")):
        for t in json.load(open(f)):
            if t["role"] != "ai":
                continue
            hits += [h[1] for h in CS.narration_hits(t["text"])]
            hits += [p.strip()[:90] for p in re.split(r"\n\s*\n", t["text"]) if NOTE.match(p.strip())]
    return hits


evals, runs, clean, reworded, narr = {}, 0, 0, 0, 0
for d in sorted(glob.glob(R + "/*/")):
    ev = os.path.basename(d.rstrip("/"))
    fails = []
    n_runs = 0
    for rdir in sorted(glob.glob(d + "run-*")):
        if not os.path.exists(rdir + "/result.json"):
            continue
        n_runs += 1; runs += 1
        sc = json.load(open(latest(rdir, "scripted")))
        gr = json.load(open(latest(rdir, "grading")))
        gr = gr["expectations"] if isinstance(gr, dict) else gr
        bad = [("scripted", e) for e in sc if not e["passed"]] + [("judged", e) for e in gr if not e.get("passed")]
        clean += not bad
        reworded += any(e["text"].startswith(QUOTE) for _, e in bad)
        nh = narrates(rdir)
        narr += bool(nh)
        rn = os.path.basename(rdir)
        fails += [(rn, k, e["text"][:110], str(e.get("evidence", ""))[:330]) for k, e in bad]
        if detail and nh:
            fails.append((rn, "narration-metric", nh[0], ""))
    if n_runs:
        evals[ev] = (n_runs, fails)
passed = [e for e, (n, f) in evals.items() if not [x for x in f if x[1] != "narration-metric"]]
pct = lambda a, b: f"{a} of {b} ({100 * a / b:.0f}%)"
print(f"evals passing: {pct(len(passed), len(evals))}")
print(f"clean runs: {pct(clean, runs)}")
print(f"reworded-line rate (quote check): {pct(reworded, runs)} runs")
print(f"narration rate: {pct(narr, runs)} runs")
if detail:
    for ev, (n, f) in evals.items():
        if f:
            print(f"\n## {ev} ({n} run{'s' if n > 1 else ''})")
            for rn, k, text, evd in f:
                print(f"  {rn} [{k}] {text}\n      {evd}")
