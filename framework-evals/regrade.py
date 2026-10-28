#!/usr/bin/env python3
"""Re-grade a finished round with today's graders, without re-running any session.

Usage:
  python3 framework-evals/regrade.py <round-dir> [<eval-id>...] --evals FILE
          [--tag v2] [--scripted-only] [--parallel N] [--smoke | --no-smoke] [--yes]

  round-dir      a run_eval.py out-dir (its <eval-id>/run-<k>/ folders)
  eval ids       which evals to re-grade; none means every eval folder in the round
  --evals        the evals.json whose expectations to grade against (today's, so a changed or added
                 check applies). The sessions, fixtures and platform come from each run's own eval.json:
                 what actually ran
  --tag          the suffix of the files written (default v2): scripted-v2.json, grading-v2.json and
                 result-v2.json beside each run's own, and summary-v2.md in the round dir. Nothing the
                 round wrote is ever changed; a tag already used is refused (pick another)
  --scripted-only  re-run the scripted checks only (no model call; no --yes needed). The judged
                 results are carried from the run's grading.json, marked so in result-<tag>.json
  --parallel     runs graded at once (default 4)
  --smoke        verdicts as a smoke round's (SMOKE PASS/FAIL); default: read from the round's summary.md
  --yes          make the grader calls. Without it the cost estimate is printed and nothing is called

Each run's files are rebuilt from what the round kept: a session that began from its fixture rebuilds
it (the fixture builder as it is in this checkout, so a fixture changed since the round shows here as
its new version) and the platform's layout, and its end tree is that start tree with the session's
changes/ laid over and removed.txt taken away; a session carried over from the one before starts from
that session's end tree. The events.jsonl sits beside a rebuilt workspace, as in the round, so checks
and judge context that read the session's tool calls see them. The round keeps no per-turn file lists,
so a check with file_existed_during inside it is carried from the run's scripted.json, marked so.
Only runs whose sessions were kept (status valid or invalid) are re-graded, and only where today's
eval makes the same sessions as the run's own eval.json (RAN_KEYS); the others are listed as skipped,
to re-run. A fixture builder changed since the round under the same fixture name can't be seen from
what the round kept: re-grade a round only against fixtures that haven't changed since it.

The graders run through harness.py exactly as in a round: a control call first, the keychain login,
the init assertions, and the fail-closed check on the real Claude config before and after.
"""
import argparse
import concurrent.futures as cf
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path

import check_scripted as CS
import grade_eval as G
import harness as H
import leader as L
import run_eval as RE

GRADED = ("valid", "invalid")
# what makes the sessions: when today's eval differs from the run's own in any of these, the run
# can't stand for today's eval (its fixture or prompt changed since), so it is re-run, never re-graded
RAN_KEYS = ("fixture", "prompt", "sessions", "student", "platform", "platform_faults", "tools", "stub_tools",
            "max_turns", "leader_runs")


def stale(ev, rdir):
    """The RAN_KEYS where today's eval differs from what the run ran ([] when none)."""
    ran = json.loads((rdir / "eval.json").read_text())
    return [k for k in RAN_KEYS if ran.get(k) != ev.get(k)]


def _uses(check, kind):
    if not isinstance(check, dict):
        return False
    if check.get("type") == kind:
        return True
    subs = list(check.get("checks") or []) + [check.get(k) for k in ("passed", "open") if isinstance(check.get(k), dict)]
    return any(_uses(x, kind) for x in subs)


class StaleFixture(Exception):
    """The fixture rebuilt today isn't the one the session read: re-run the eval, don't re-grade it."""


def _rel(fp):
    return fp.split("/workspace/", 1)[1] if "/workspace/" in fp else None


def fixture_drift(start, events_path):
    """The files the session read (a Read before any write to the file) whose lines aren't in the
    rebuilt start tree, as paths: a fixture changed since the round under the same name."""
    try:
        lines = Path(events_path).read_text(errors="replace").splitlines()
    except OSError:
        return []
    reads, written, bad = {}, set(), []
    for line in lines:
        try:
            e = json.loads(line)
        except ValueError:
            continue
        msg = e.get("message") if isinstance(e, dict) else None
        content = msg.get("content") if isinstance(msg, dict) else None
        for b in content if isinstance(content, list) else []:
            if not isinstance(b, dict):
                continue
            if b.get("type") == "tool_use":
                inp = b.get("input") or {}
                rel = _rel(str(inp.get("file_path") or ""))
                if b.get("name") == "Read" and rel and rel not in written:
                    reads[b.get("id")] = rel
                elif b.get("name") in ("Write", "Edit", "MultiEdit") and rel:
                    written.add(rel)
                elif b.get("name") == "Bash":
                    cmd = str(inp.get("command") or "")
                    written |= {r for r in start if Path(r).name in cmd}
            elif b.get("type") == "tool_result" and b.get("tool_use_id") in reads and not b.get("is_error"):
                rel = reads.pop(b["tool_use_id"])
                c = b.get("content")
                text = c if isinstance(c, str) else "\n".join(x.get("text", "") for x in c or [] if isinstance(x, dict))
                body = text.split("<system-reminder>")[0]  # the reminder Claude Code appends isn't the file
                if rel in written or not body.strip():
                    continue
                have = {ln.rstrip() for ln in (start.get(rel) or "").splitlines()}
                got = [m.group(1).rstrip() for m in re.finditer(r"(?m)^\s*\d+\t(.*)$", body)]
                if rel not in start or any(ln.strip() and ln not in have for ln in got):
                    bad.append(rel)
    return sorted(set(bad))


def overlay(start, sdir):
    """A session's end tree: its start tree, the files in changes/ laid over, removed.txt taken away."""
    end = dict(start)
    ch = sdir / "changes"
    end.update(CS.load_tree(ch))
    rem = sdir / "removed.txt"
    for rel in (rem.read_text().splitlines() if rem.exists() else []):
        end.pop(rel.strip(), None)
    return end


def _write_tree(files, folder):
    folder.mkdir(parents=True, exist_ok=True)
    for rel, body in files.items():
        p = folder / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(body)


def rebuild_run(rdir, evals_dir, data, work):
    """The run dict run_eval.run_once graded, rebuilt from a run folder into `work` (each session's
    end tree at work/session-n/workspace, its events.jsonl beside it). The eval is the run's own
    eval.json (what ran)."""
    ran = json.loads((rdir / "eval.json").read_text())
    sessions = ran.get("sessions") or [{"prompt": ran.get("prompt"), "student": True}]
    run, prev_end = {"sessions": []}, None
    for n, s in enumerate(sessions, 1):
        sdir = rdir / f"session-{n}"
        if not (sdir / "turns.json").exists():
            raise H.HarnessFailure(f"{rdir.name}: session {n} has no turns.json")
        platform = L.platform_for(ran, s)
        fresh = bool(s.get("fixture_from")) or n == 1 or not s.get("from_previous")
        if not fresh:
            start = dict(prev_end)
        else:
            ws = Path(tempfile.mkdtemp(dir=work)) / "workspace"
            if s.get("fixture_from"):
                src = Path(s["fixture_from"])
                shutil.copytree(src if src.is_absolute() else evals_dir / src, ws)
            else:
                RE.build_fixture(s.get("fixture", ran.get("fixture")), ws, evals_dir, data.get("fixture_builder"))
                platform.prepare(ws)
            start = CS.load_tree(ws)
            drift = fixture_drift(start, sdir / "events.jsonl")
            if drift:
                raise StaleFixture(f"session {n}'s fixture changed since the round (the session read other "
                                   f"lines in {', '.join(drift[:3])}): re-run it")
        end = overlay(start, sdir)
        wroot = work / f"session-{n}"
        _write_tree(end, wroot / "workspace")
        if (sdir / "events.jsonl").exists():
            shutil.copy2(sdir / "events.jsonl", wroot / "events.jsonl")
        script = None
        if isinstance(s.get("student"), str):
            script = RE.load_script(evals_dir, s["student"])
        elif s.get("student") and ran.get("student"):
            script = RE.load_script(evals_dir, ran["student"])
        transcript = (sdir / "transcript.md").read_text() if (sdir / "transcript.md").exists() else ""
        run["sessions"].append({"n": n, "turns": json.loads((sdir / "turns.json").read_text()),
                                "files_by_turn": None, "files_start": start, "files_end": end,
                                "cap_hit": "Stopped at the turn cap." in transcript,
                                "root": str(wroot / "workspace"), "platform": platform.key,
                                "script_quotes": CS.script_quotes(script), "fixture": fresh})
        prev_end = end
    return run


def scripted_checks(ev, run, data, old):
    """CS.run_checks, except a check needing the per-turn file lists (not kept) is carried from the
    round's own result for it (failed when there's none: fail closed)."""
    run = {**run, "skill": run.get("skill") or data.get("skill_name")}
    olds = {x["text"]: x for x in old}
    out = []
    for x in ev["expectations"]:
        if x["kind"] != "scripted":
            continue
        keep = {k: x[k] for k in ("must", "gating") if k in x}
        if _uses(x["check"], "file_existed_during"):
            o = olds.get(x["text"])
            out.append({"text": x["text"], "kind": "scripted", "passed": bool(o and o["passed"]),
                        "evidence": "carried from the round (files after each turn aren't kept): "
                        + (o["evidence"] if o else "no result in the round: failed"), "carried": True, **keep})
            continue
        ok, why = CS.check(x["check"], run)
        out.append({"text": x["text"], "kind": "scripted", "passed": bool(ok), "evidence": why, **keep})
    for b in CS.builtins_for(ev, data):
        ok, why = CS.check({"type": b}, run)
        out.append({"text": CS.BUILTIN_TEXT[b], "kind": "scripted", "passed": bool(ok), "evidence": why, "builtin": b})
    if any(s["cap_hit"] for s in run["sessions"]):
        out.append({"text": "The run ends before the turn cap", "kind": "scripted",
                    "passed": False, "evidence": "turn cap hit"})
    return out


def regrade_run(rnd, rdir, ev, data, evals_dir, tag, scripted_only):
    old_res = json.loads((rdir / "result.json").read_text())
    old_scripted = json.loads((rdir / "scripted.json").read_text()) if (rdir / "scripted.json").exists() else []
    old_judged = (json.loads((rdir / "grading.json").read_text()).get("expectations", [])
                  if (rdir / "grading.json").exists() else [])
    root = H.new_run_root()
    calls = []
    try:
        run = rebuild_run(rdir, evals_dir, data, root)
        scripted = scripted_checks(ev, run, data, old_scripted)
        fid = None
        if ev.get("student") or any(isinstance(x.get("student"), str) for x in ev.get("sessions", [])):
            ok, why = CS.fidelity(run)
            fid = {"passed": ok, "evidence": why}
        if scripted_only:
            judged = [dict(j, carried=True) for j in old_judged]
        else:
            judged, grec = G.grade(rnd, root, ev, run, evals_dir)
            calls += [grec] if grec else []
            if data.get("judge_rubric", True) and ev.get("judge_rubric", True):
                rubric, rrec = G.grade_rubric(rnd, root, ev, run)
                judged += rubric
                if rrec:
                    rrec["role"] = "rubric"
                    calls.append(rrec)
    finally:
        shutil.rmtree(root, ignore_errors=True)
    pre = [j for j in judged if j.get("precondition")]
    status, note = "valid", ""
    if fid and not fid["passed"]:
        status, note = "invalid", "fidelity: " + fid["evidence"]
    elif any(not j["passed"] for j in pre):
        status, note = "invalid", "precondition: " + "; ".join(j["text"] for j in pre if not j["passed"])
    exp = scripted + [j for j in judged if not j.get("precondition")]
    res = {**{k: old_res.get(k) for k in ("eval", "run", "tier", "models", "claude_code_version", "leader_actions")},
           "status": status, "note": note, "fidelity": fid, "preconditions": pre, "expectations": exp,
           "passed": sum(1 for e in exp if e["passed"]), "total": len(exp),
           "regrade": {"tag": tag, "scripted_only": scripted_only, "judged_carried": scripted_only,
                       "round_status": old_res.get("status"), "round_passed": old_res.get("passed"),
                       "round_total": old_res.get("total")},
           "usd": round(sum(c.get("total_cost_usd") or 0 for c in calls), 4)}
    (rdir / f"scripted-{tag}.json").write_text(json.dumps(scripted, indent=2, ensure_ascii=False))
    if not scripted_only:
        (rdir / f"grading-{tag}.json").write_text(json.dumps({"expectations": judged}, indent=2, ensure_ascii=False))
        (rdir / f"calls-{tag}.json").write_text(json.dumps(calls, indent=2, ensure_ascii=False))
    (rdir / f"result-{tag}.json").write_text(json.dumps(res, indent=2, ensure_ascii=False))
    hits = H.commit_leak_scan(rdir)
    if hits:
        for f in rdir.glob(f"*-{tag}.json"):
            f.unlink()
        return {"eval": ev["id"], "run": old_res.get("run"), "status": "harness_failure",
                "note": f"leak scan hits: {len(hits)} (re-grade files deleted)"}
    return res


def summary(out, evs, data, tag, results, smoke, skipped=()):
    RE.SMOKE = smoke
    lines = [f"# Re-grade summary ({tag})", "",
             "Each eval's verdict from the round's own results, then from this re-grade, and every expectation "
             "whose pass count changed.", ""]
    if skipped:
        lines += ["Not re-graded (the run no longer stands for today's eval):", ""] + [f"- {x}" for x in skipped] + [""]
    for ev in evs:
        t = RE.tier_of(ev, data)
        olds = [json.loads(f.read_text()) for f in sorted((out / ev["id"]).glob("run-*/result.json"))]
        news = sorted([r for r in results if r["eval"] == ev["id"]], key=lambda r: r.get("run") or 0)
        was, _ = RE.eval_verdict(ev, olds, t)
        now, graded = RE.eval_verdict(ev, news, t)
        lines += [f"### {ev['id']}: {was} -> {now}", "",
                  "Runs: " + ", ".join(f"run-{r.get('run')} {r['status']}"
                                       + (f" {r['passed']}/{r['total']}" if "total" in r else "") for r in news)]
        old_by = {}
        for r in olds:
            for x in r.get("expectations") or []:
                old_by.setdefault(x["text"], []).append(bool(x["passed"]))
        for i, x in enumerate(graded[0]["expectations"] if graded else []):
            got = [r["expectations"][i]["passed"] for r in graded if i < len(r["expectations"])]
            before = old_by.get(x["text"])
            if before is None or sum(before) != sum(got):
                lines.append(f"- {sum(got)}/{len(got)} (round: "
                             + (f"{sum(before)}/{len(before)}" if before is not None else "new") + f") "
                             f"[{x['kind']}{', carried' if x.get('carried') else ''}] {x['text'][:140]}")
        lines.append("")
    (out / f"summary-{tag}.md").write_text("\n".join(lines))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("round_dir")
    ap.add_argument("eval_ids", nargs="*")
    ap.add_argument("--evals", required=True)
    ap.add_argument("--tag", default="v2")
    ap.add_argument("--scripted-only", action="store_true")
    ap.add_argument("--parallel", type=int, default=4)
    sm = ap.add_mutually_exclusive_group()
    sm.add_argument("--smoke", dest="smoke", action="store_true", default=None)
    sm.add_argument("--no-smoke", dest="smoke", action="store_false")
    ap.add_argument("--yes", action="store_true")
    args = ap.parse_args()
    if not args.tag.replace("-", "").isalnum():
        sys.exit("--tag: letters, digits and hyphens only")

    out = Path(args.round_dir).resolve()
    evals_path = Path(args.evals).resolve()
    evals_dir = evals_path.parent
    data = RE.load_evals(evals_path)
    by_id = {e["id"]: e for e in data["evals"]}
    ids = args.eval_ids or sorted(p.name for p in out.iterdir() if p.is_dir() and any(p.glob("run-*/result.json")))
    missing = [i for i in ids if i not in by_id]
    if missing:
        sys.exit(f"not in {evals_path.name}: {missing}")
    jobs, skipped = [], []
    for i in ids:
        for rdir in sorted((out / i).glob("run-*")):
            if not (rdir / "result.json").exists():
                continue
            if any(rdir.glob(f"*-{args.tag}.json")):
                sys.exit(f"{rdir}: already re-graded as {args.tag}; pick another --tag")
            if json.loads((rdir / "result.json").read_text()).get("status") not in GRADED:
                continue
            changed = stale(by_id[i], rdir)
            if changed:
                skipped.append(f"{i} {rdir.name}: the eval's {', '.join(changed)} changed since the round: re-run it")
                continue
            jobs.append((by_id[i], rdir))
    for x in skipped:
        print("SKIPPED", x)
    if not jobs:
        sys.exit("no runs to re-grade")
    smoke = args.smoke if args.smoke is not None else (
        (out / "summary.md").exists() and "SMOKE " in (out / "summary.md").read_text())

    per_run = [sum(c.get("total_cost_usd") or 0 for c in json.loads((rdir / "calls.json").read_text())
                   if c.get("role") in ("grader", "rubric"))
               for _, rdir in jobs if (rdir / "calls.json").exists()]
    if per_run and any(per_run):
        est, basis = sum(per_run) / len(per_run) * len(jobs), "the round's own grader and rubric calls"
    else:
        est, basis = len(jobs) * (RE.EST_USD["grader"] + RE.EST_USD["rubric"]), "rough per-call rates"
    if args.scripted_only:
        print(f"Re-grade of {len(jobs)} runs in {out.name} as {args.tag} (scripted checks only: no model calls)")
    else:
        print(f"Re-grade of {len(jobs)} runs in {out.name} as {args.tag}; estimate "
              f"${est + RE.EST_USD['control']:.2f} API-equivalent ({basis}, plus the control call)")
    rnd = None
    if not args.scripted_only:
        if not args.yes:
            print("Not started: show James this estimate, then re-run with --yes. No model calls were made.")
            sys.exit(3)
        before = H.real_config_snapshot()
        if H.leak_signs():
            sys.exit(f"leak signs before the re-grade: {H.leak_signs()}")
        rnd = H.Round()
        croot = H.new_run_root()
        _, crec = H.call(rnd, "control", croot, "Say OK.", cwd=croot / "grader", tools=[])
        rnd.bundled_skills = crec["init"]["skills"]
        rnd.bundled_plugins = [p["source"] for p in crec["init"]["plugins"] if p.get("path") == "builtin"]
        auth = H.auth_method(rnd, croot)
        shutil.rmtree(croot)
        if auth != "oauth_token":
            sys.exit(f"authMethod is {auth}, expected oauth_token")

    results = []
    with cf.ThreadPoolExecutor(max_workers=args.parallel) as pool:
        futs = {pool.submit(regrade_run, rnd, rdir, ev, data, evals_dir, args.tag, args.scripted_only): (ev, rdir)
                for ev, rdir in jobs}
        for f in cf.as_completed(futs):
            ev, rdir = futs[f]
            try:
                r = f.result()
            except StaleFixture as e:
                r = {"eval": ev["id"], "run": int(rdir.name.split("-")[1]), "status": "stale_fixture", "note": str(e)}
                skipped.append(f"{ev['id']} {rdir.name}: {e}")
            except H.UsageLimit as e:
                r = {"eval": ev["id"], "run": int(rdir.name.split("-")[1]), "status": "usage_pause", "note": str(e)}
            except Exception as e:  # a fixture that no longer builds, a grader failure: never a pass
                r = {"eval": ev["id"], "run": int(rdir.name.split("-")[1]), "status": "harness_failure",
                     "note": H.scrub(repr(e))[:500]}
            results.append(r)
            print(f"{r['eval']} run-{r['run']}: {r['status']}"
                  + (f" {r['passed']}/{r['total']}" if "total" in r else "")
                  + (f" (round {r['regrade']['round_passed']}/{r['regrade']['round_total']})" if "regrade" in r else "")
                  + (f" ({r['note'][:200]})" if r.get("note") else ""), flush=True)
    summary(out, [by_id[i] for i in ids], data, args.tag, results, smoke, skipped)
    usd = sum(r.get("usd") or 0 for r in results)
    if rnd is not None:
        problems = H.compare_snapshots(before, H.real_config_snapshot())
        if problems:
            print("FAIL-CLOSED CHECK FAILED: the re-grade is void:", problems)
            sys.exit(2)
    print(f"re-grade done; reported usage ${usd:.2f}; summary in {out / f'summary-{args.tag}.md'}")


if __name__ == "__main__":
    main()
