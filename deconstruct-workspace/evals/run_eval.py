#!/usr/bin/env python3
"""Run framework evals in isolation: build each fixture, run the skill, play the student, grade.

Usage:
  python3 run_eval.py <out-dir> <eval-id>... [--evals FILE] [--runs N] [--plugin DIR]
                      [--max-turns N] [--parallel N] [--skill-model MODEL] [--max-usd N]

  --evals        the evals.json to read (default: this folder's)
  --runs         repeats per eval (default: the eval's `runs`, else 3)
  --plugin       plugin folder under test (default: this repo's plugins/handsonai)
  --max-turns    cap on AI turns per session (default 80); hitting it fails the run
  --parallel     runs at once (default 2; see how_to_run for the cap)
  --skill-model  the skill session's model for this round (default harness.SKILL_MODEL);
                 used for the information-only claude-sonnet-5-5 subset
  --max-usd      stop starting new runs once the round's reported usage passes this
                 (the API-equivalent cost Claude Code reports; a subscription is not billed it)

Every call runs through harness.py (isolation, login, init checks). The round runs the
fail-closed check on the real Claude config before and after (R12-3).

Output, per eval and run, under <out-dir>/<eval-id>/run-<k>/:
  eval.json, result.json (status and every expectation's result), grading.json (judged),
  scripted.json, calls.json (init records, models, denials, usage per call), and per session:
  session-<n>/transcript.md, turns.json, events.jsonl (tool calls with their results),
  changes/ (files the session added or changed) and removed.txt; plus session-<n>/workspace
  for evals marked `keep_workspace` (writers read by other evals: I1, I2, I8, C1, ...).
Then <out-dir>/round.json and <out-dir>/summary.md.

Session sources, in an eval's `sessions` list: `fixture_from` wins in any session, the first
session included; otherwise the first session builds the eval's `fixture`; a later session rebuilds its `fixture` (or the eval's) unless it says `from_previous: true`
(keep the workspace as it is) or `fixture_from: <path>` (copy a copied-back session snapshot;
relative paths resolve from the evals.json folder). Fixture names: see build_fixture. `agent: true` (eval or session) starts the
session on the plugin's framework-agent. `student: true` plays the eval's script; `student: "<path>"`
plays that session's own script (the chain eval C1). `tools: "no_file"` turns off Write, Edit and Bash (NF1); `tools: "web"` adds WebSearch and WebFetch
(running a built workflow that researches, G2).
"""
import argparse
import concurrent.futures as cf
import json
import shutil
import subprocess
import sys
import threading
import uuid
from datetime import datetime, timezone
from pathlib import Path

import check_scripted as CS
import grade_eval as G
import harness as H

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]

STUDENT_RULES = """You are playing a student in a test of an AI interview. You see only your script and the conversation.
Reply with only the student's next message: no notes, no quotes around it, no labels.
Rules:
- Answer only from the script. If the script doesn't cover what the AI asks, say you're not sure, in a few words,
  and add nothing of your own: no guesses, no "I think...", no new names, numbers, tools, people or habits.
- Use plain, everyday words. Never use a framework term (for example acceptance criterion, fixed step, human gate,
  autonomy, Golden Example) unless the AI used it first.
- Do each provocation the script lists (rambling, answering two questions at once, asking a question back,
  contradicting yourself) exactly where the script says, and nowhere else.
- Otherwise answer only what the AI's last message asks, the way the person in the script would. Don't volunteer
  a fact the AI hasn't asked for yet unless the script tells you to volunteer it; save it for when it's asked.
- If the script's stop condition is met, reply exactly END.

SCRIPT:
"""

lock = threading.Lock()


def load_evals(path):
    data = json.loads(Path(path).read_text())
    for ev in data["evals"]:
        ev["expectations"] = [x if isinstance(x, dict) else {"text": x, "kind": "judged"} for x in ev["expectations"]]
    return data


def build_fixture(fixture, target, evals_dir, builder=None):
    """`empty` makes an empty workspace; `dir:<path>` copies a committed folder (relative to the
    evals.json folder); anything else is a name passed to the evals file's `fixture_builder`
    (default fixtures/make_fixture.py beside it, else this folder's)."""
    if target.exists():
        shutil.rmtree(target)
    if fixture in (None, "empty"):
        target.mkdir(parents=True)
        return
    if fixture.startswith("dir:"):
        src = (evals_dir / fixture[4:]).resolve()
        if not src.is_dir():
            raise H.HarnessFailure(f"fixture folder missing: {fixture}")
        shutil.copytree(src, target)
        return
    maker = evals_dir / (builder or "fixtures/make_fixture.py")
    if not maker.exists():
        maker = HERE / "fixtures" / "make_fixture.py"
    r = subprocess.run([sys.executable, str(maker), fixture, str(target)], capture_output=True, text=True)
    if r.returncode != 0:
        raise H.HarnessFailure(f"fixture {fixture}: {r.stderr[-800:]}")


def tools_for(ev, s):
    kind = s.get("tools", ev.get("tools"))
    if kind == "no_file":
        return H.NO_FILE_TOOLS
    if kind == "web":
        return H.WEB_TOOLS
    if kind == "agent" or s.get("agent", ev.get("agent")):
        return H.AGENT_TOOLS
    return H.SKILL_TOOLS


def file_list(ws):
    return sorted(str(p.relative_to(ws)) for p in ws.rglob("*") if p.is_file())


def run_once(rnd, ev, k, out, args, evals_dir):
    """One run of one eval in its own run root. Returns the result dict."""
    rdir = out / ev["id"] / f"run-{k}"
    if rdir.exists():
        shutil.rmtree(rdir)
    rdir.mkdir(parents=True)
    (rdir / "eval.json").write_text(json.dumps(ev, indent=2, ensure_ascii=False))
    root = H.new_run_root(args.plugin)
    plugin = root / "plugin"
    ws = root / "workspace"
    calls, run = [], {"sessions": []}
    status, note = "valid", ""
    judged, scripted, fid = [], [], None
    sessions = ev.get("sessions") or [{"prompt": ev["prompt"], "student": True}]
    try:
        for n, s in enumerate(sessions, 1):
            # Fresh temp HOME per session; kept across this session's --resume turns.
            H.reset_home(root)
            if s.get("fixture_from"):
                src = Path(s["fixture_from"])
                src = src if src.is_absolute() else (evals_dir / src)
                if ws.exists():
                    shutil.rmtree(ws)
                shutil.copytree(src, ws)
            elif n == 1 or not s.get("from_previous"):
                build_fixture(s.get("fixture", ev.get("fixture")), ws, evals_dir, args.fixture_builder)
            sdir = root / f"session-{n}"
            shutil.copytree(ws, sdir / "workspace-start")
            # `student: true` uses the eval's script; `student: "<path>"` names this session's own.
            script = None
            if isinstance(s.get("student"), str):
                script = (evals_dir / s["student"]).read_text()
            elif s.get("student") and ev.get("student"):
                script = (evals_dir / ev["student"]).read_text()
            replies = list(s.get("replies", []))
            cap = s.get("max_turns", ev.get("max_turns", args.max_turns))
            tools = tools_for(ev, s)
            agent = "handsonai:framework-agent" if s.get("agent", ev.get("agent")) else None
            sid = str(uuid.uuid4())
            turns, files_by_turn, cap_hit = [], [], False
            msg, msg_kind = s["prompt"], "prompt"
            for turn in range(cap):
                turns.append({"role": "student", "text": msg, msg_kind: True})
                kw = {"session_id": sid} if turn == 0 else {"resume": sid}
                ai, rec = H.call(rnd, "skill", root, msg, cwd=ws, tools=tools, plugin=plugin, agent=agent,
                                 model=args.skill_model, log=sdir / "events.jsonl", **kw)
                rec.update(session=n, turn=turn + 1)
                calls.append(rec)
                turns.append({"role": "ai", "text": ai})
                files_by_turn.append(file_list(ws))
                if replies:
                    msg, msg_kind = replies.pop(0), "scripted_reply"
                elif script:
                    convo = "\n\n".join(f"## {'AI' if t['role'] == 'ai' else 'Student'}\n\n{t['text']}" for t in turns)
                    msg, srec = H.call(rnd, "student", root,
                                       f"The conversation so far:\n\n{convo}\n\nYour next message as the student:",
                                       cwd=root / "student", tools=[], system_prompt=STUDENT_RULES + script)
                    srec.update(session=n, turn=turn + 1)
                    calls.append(srec)
                    msg_kind = "student"
                    if msg.strip() == "END":
                        turns.append({"role": "student", "text": "END", "end": True})
                        break
                else:
                    break
            else:
                cap_hit = True
            shutil.copytree(ws, sdir / "workspace")
            start, end = CS.load_tree(sdir / "workspace-start"), CS.load_tree(sdir / "workspace")
            run["sessions"].append({"n": n, "turns": turns, "files_by_turn": files_by_turn,
                                    "files_start": start, "files_end": end, "cap_hit": cap_hit})
        # Grade inside the run root's lifetime (the grader runs from run-root/grader).
        scripted = CS.run_checks(ev, run)
        if any(s["cap_hit"] for s in run["sessions"]):
            scripted.append({"text": "The run ends before the turn cap", "kind": "scripted",
                             "passed": False, "evidence": "turn cap hit"})
        if ev.get("student") or any(isinstance(x.get("student"), str) for x in sessions):
            ok, why = CS.fidelity(run)
            fid = {"passed": ok, "evidence": why}
        judged, grec = G.grade(rnd, root, ev, run, evals_dir)
        if grec:
            calls.append(grec)
    except H.UsageLimit as e:
        status, note = "usage_pause", str(e)
    except H.HarnessFailure as e:
        status, note = "harness_failure", str(e)
    if status != "valid":
        shutil.rmtree(root, ignore_errors=True)
        # Nothing is copied back from a failed run except the failure itself.
        for p in rdir.iterdir():
            if p.name != "eval.json":
                shutil.rmtree(p) if p.is_dir() else p.unlink()
        res = {"eval": ev["id"], "run": k, "status": status, "note": H.scrub(note)}
        (rdir / "result.json").write_text(json.dumps(res, indent=2))
        return res

    pre = [j for j in judged if j.get("precondition")]
    if fid and not fid["passed"]:
        status, note = "invalid", "fidelity: " + fid["evidence"]
    elif any(not j["passed"] for j in pre):
        status, note = "invalid", "precondition: " + "; ".join(j["text"] for j in pre if not j["passed"])
    exp = scripted + [j for j in judged if not j.get("precondition")]
    res = {"eval": ev["id"], "run": k, "status": status, "note": note,
           "models": sorted({m for c in calls for m in c["model_used"]}),
           "claude_code_version": rnd.version, "fidelity": fid, "preconditions": pre,
           "expectations": exp,
           "passed": sum(1 for e in exp if e["passed"]), "total": len(exp),
           "denials": [d for c in calls for d in c["permission_denials"]],
           "usd": round(sum(c.get("total_cost_usd") or 0 for c in calls), 4)}
    # Copy back named outputs only.
    for sess in run["sessions"]:
        n = sess["n"]
        out_s = rdir / f"session-{n}"
        out_s.mkdir()
        if (root / f"session-{n}" / "events.jsonl").exists():
            shutil.copy2(root / f"session-{n}" / "events.jsonl", out_s / "events.jsonl")
        (out_s / "turns.json").write_text(json.dumps(sess["turns"], indent=2, ensure_ascii=False))
        (out_s / "transcript.md").write_text("\n".join(
            f"## {'AI' if t['role'] == 'ai' else 'Student'}\n\n{t['text']}\n" for t in sess["turns"])
            + ("\n## Harness\n\nStopped at the turn cap.\n" if sess["cap_hit"] else ""))
        ch = out_s / "changes"
        for rel, body in sess["files_end"].items():
            if sess["files_start"].get(rel) != body:
                (ch / rel).parent.mkdir(parents=True, exist_ok=True)
                (ch / rel).write_text(body)
        removed = [r for r in sess["files_start"] if r not in sess["files_end"]]
        if removed:
            (out_s / "removed.txt").write_text("\n".join(removed) + "\n")
        if ev.get("keep_workspace"):
            shutil.copytree(root / f"session-{n}" / "workspace", out_s / "workspace")
    (rdir / "scripted.json").write_text(json.dumps(scripted, indent=2, ensure_ascii=False))
    (rdir / "grading.json").write_text(json.dumps({"expectations": judged}, indent=2, ensure_ascii=False))
    (rdir / "calls.json").write_text(json.dumps(calls, indent=2, ensure_ascii=False))
    (rdir / "result.json").write_text(json.dumps(res, indent=2, ensure_ascii=False))
    shutil.rmtree(root, ignore_errors=True)
    hits = H.commit_leak_scan(rdir)
    if hits:
        shutil.rmtree(rdir)
        rdir.mkdir(parents=True)
        res = {"eval": ev["id"], "run": k, "status": "harness_failure",
               "note": f"leak scan hits: {len(hits)} (results deleted)"}
        (rdir / "result.json").write_text(json.dumps(res, indent=2))
    return res


def run_slot(rnd, ev, k, out, args, evals_dir, budget):
    """A run slot: re-run an invalid run up to twice; a third invalid counts as a failure."""
    for attempt in range(3):
        with lock:
            if budget["usd"] >= args.max_usd or budget["paused"]:
                return {"eval": ev["id"], "run": k, "status": "skipped", "note": "budget or usage pause"}
        res = run_once(rnd, ev, k, out, args, evals_dir)
        with lock:
            budget["usd"] += res.get("usd", 0)
            if res["status"] == "usage_pause":
                budget["paused"] = True
        if res["status"] != "invalid":
            return res
        res["invalid_attempts"] = attempt + 1
    res["status"] = "failed_invalid_cap"
    (out / ev["id"] / f"run-{k}" / "result.json").write_text(json.dumps(res, indent=2, ensure_ascii=False))
    return res


def pass_bar(x, n):
    """Global Constraints pass rules: scripted and must-level judged pass every run; other
    judged pass 2 of 3 (final round: 7 of 10, 4 of 5). `gating: false` expectations are reported
    as info and never fail a round."""
    if x["kind"] == "scripted" or x.get("must"):
        return n
    return {1: 1, 2: 2, 3: 2, 5: 4, 10: 7}.get(n, -(-n * 2 // 3))


def summarize(out, evs, results):
    lines = ["# Round summary", ""]
    for ev in evs:
        rs = sorted([r for r in results if r["eval"] == ev["id"]], key=lambda r: r["run"])
        graded = [r for r in rs if r["status"] in ("valid", "failed_invalid_cap") and r.get("expectations")]
        lines += [f"## {ev['id']} — {ev.get('name', '')}", ""]
        lines.append("Runs: " + ", ".join(
            f"run-{r['run']} {r['status']}" + (f" {r['passed']}/{r['total']}" if "total" in r else "") for r in rs))
        if graded:
            lines.append("")
            for i, x in enumerate(graded[0]["expectations"]):
                got = [r["expectations"][i]["passed"] for r in graded if i < len(r["expectations"])]
                need = pass_bar(x, len(got))
                verdict = ("info" if x.get("gating") is False else "PASS" if sum(got) >= need else "FAIL")
                lines.append(f"- {verdict} {sum(got)}/{len(got)} (needs {need}) [{x['kind']}"
                             + (", must" if x.get("must") else "") + f"] {x['text'][:140]}")
        lines.append("")
    (out / "summary.md").write_text("\n".join(lines))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out_dir")
    ap.add_argument("eval_ids", nargs="+")
    ap.add_argument("--evals", default=str(HERE / "evals.json"))
    ap.add_argument("--runs", type=int)
    ap.add_argument("--plugin", default=str(ROOT / "plugins" / "handsonai"))
    ap.add_argument("--max-turns", type=int, default=80)
    ap.add_argument("--parallel", type=int, default=2)
    ap.add_argument("--skill-model", default=H.SKILL_MODEL)
    ap.add_argument("--max-usd", type=float, default=float("inf"))
    args = ap.parse_args()

    evals_path = Path(args.evals).resolve()
    evals_dir = evals_path.parent
    data = load_evals(evals_path)
    args.fixture_builder = data.get("fixture_builder")
    by_id = {e["id"]: e for e in data["evals"]}
    missing = [i for i in args.eval_ids if i not in by_id]
    if missing:
        sys.exit(f"unknown eval ids: {missing}")
    evs = [by_id[i] for i in args.eval_ids]
    out = Path(args.out_dir).resolve()
    out.mkdir(parents=True, exist_ok=True)

    before = H.real_config_snapshot()
    if H.leak_signs():
        sys.exit(f"leak signs before the round: {H.leak_signs()}")
    rnd = H.Round()
    # Record the allowed bundled skills and built-in plugins from a no-plugin control call.
    croot = H.new_run_root()
    _, crec = H.call(rnd, "control", croot, "Say OK.", cwd=croot / "grader", tools=[])
    rnd.bundled_skills = crec["init"]["skills"]
    rnd.bundled_plugins = [p["source"] for p in crec["init"]["plugins"] if p.get("path") == "builtin"]
    auth = H.auth_method(rnd, croot)
    shutil.rmtree(croot)
    if auth != "oauth_token":
        sys.exit(f"authMethod is {auth}, expected oauth_token")

    budget = {"usd": 0.0, "paused": False}
    jobs = [(ev, k) for ev in evs for k in range(1, (args.runs or ev.get("runs", 3)) + 1)]
    results = []
    with cf.ThreadPoolExecutor(max_workers=args.parallel) as pool:
        futs = {pool.submit(run_slot, rnd, ev, k, out, args, evals_dir, budget): (ev["id"], k) for ev, k in jobs}
        for f in cf.as_completed(futs):
            try:
                r = f.result()
            except Exception as e:  # a bug in the runner: record it as a harness failure
                eid, k = futs[f]
                r = {"eval": eid, "run": k, "status": "harness_failure", "note": H.scrub(repr(e))[:500]}
            results.append(r)
            print(f"{r['eval']} run-{r['run']}: {r['status']}"
                  + (f" {r['passed']}/{r['total']}" if "total" in r else "")
                  + (f" ({r['note'][:200]})" if r.get("note") else ""), flush=True)

    after = H.real_config_snapshot()
    problems = H.compare_snapshots(before, after)
    round_info = {"finished": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                  "claude_code_version": rnd.version, "auth_method": auth,
                  "skill_model": args.skill_model, "student_model": H.STUDENT_MODEL,
                  "grader_model": H.GRADER_MODEL,
                  "evals_file": str(evals_path.relative_to(ROOT)), "usd_reported": round(budget["usd"], 4),
                  "fail_closed_check": "pass" if not problems else problems,
                  "results": [{k: r.get(k) for k in ("eval", "run", "status", "passed", "total", "note")}
                              for r in results]}
    (out / "round.json").write_text(json.dumps(round_info, indent=2))
    summarize(out, evs, results)
    if problems:
        print("FAIL-CLOSED CHECK FAILED: the round is void:", problems)
        sys.exit(2)
    print(f"round done; reported usage ${budget['usd']:.2f}; summary in {out / 'summary.md'}")


if __name__ == "__main__":
    main()
