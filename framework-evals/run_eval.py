#!/usr/bin/env python3
"""Run framework evals in isolation: build each fixture, run the skill, play the leader, grade.

The shared runner for every step's eval set (build-task-list T18). Dev-only: never shipped.

Usage:
  python3 framework-evals/run_eval.py <out-dir> [<eval-id>...] --evals FILE
          [--tier core|regression|all] [--runs N] [--plugin DIR] [--max-turns N] [--parallel N]
          [--skill-model MODEL] [--max-usd N] [--cost-from ROUND-DIR] [--dry-run] [--yes]

  --evals        the evals.json to read (required; each step keeps its own in <step>-workspace/evals/)
  eval ids       which evals to run; none means every eval in the chosen tier
  --tier         core, regression or all (default all). Each eval is tagged `tier: core|regression`
                 (the evals file's `default_tier` otherwise). Core cases run three times before they
                 count, and pass only when every expectation passes in every run (rules 14)
  --runs         repeats per eval (default: the eval's `runs`, else 3; never fewer than 3 for core)
  --plugin       plugin folder under test (default: this repo's plugins/handsonai)
  --max-turns    cap on AI turns per session (default 80); hitting it fails the run
  --parallel     runs at once (default 2)
  --skill-model  the skill session's model for this round (default harness.SKILL_MODEL)
  --max-usd      stop starting new runs once the round's reported usage passes this
  --cost-from    a previous round's out-dir: estimate each eval's cost from its measured usage
  --dry-run      build every fixture, load every script, check every expectation and the corpus,
                 print the cost estimate, and stop: no model calls
  --yes          start the round. Without it the runner prints the cost estimate and stops, so James
                 approves each round's cost before any paid call (build-task-list T18)

Every call runs through harness.py (isolation, keychain login, init assertions). The round runs the
fail-closed check on the real Claude config before and after (R12-3).

Output, per eval and run, under <out-dir>/<eval-id>/run-<k>/: eval.json, result.json, grading.json,
scripted.json, calls.json, and per session transcript.md, turns.json, events.jsonl, changes/,
removed.txt (and the workspace for evals marked `keep_workspace`). Then <out-dir>/round.json and
<out-dir>/summary.md, both reported per tier, with each run's leader-action count.

Sessions: an eval's `sessions` list, or one session from `prompt`. `fixture_from` wins in any
session; otherwise the first session builds the eval's `fixture`; a later session rebuilds its
`fixture` (or the eval's) unless it says `from_previous: true`. Fixture names: see build_fixture.
`student: true` plays the eval's leader script; `student: "<path>"` plays that session's own.
`tools: "no_file"` turns off Write, Edit and Bash; `tools: "web"` adds WebSearch and WebFetch. `platform` and `platform_faults` pick a
platform simulation (leader.py). `action_target: {figure, journey}` names the spec's action figure.
A session's own `max_turns` is a deliberate stop (the eval grades only what comes before it), so
reaching it isn't the turn cap. `run_writes: [{when, path, text}]` stands in for a leader's run in the
shared workspace (Claude Code, Codex): when a leader message matches the regex `when`, `path` is written there.
For Test on Claude Code and Codex the leader's hand-overs run for real in the workspace (leader.py,
simulates_leader_runs); `leader_runs: "scripted"` (session or eval) keeps a planted script's blocks instead.
"""
import argparse
import concurrent.futures as cf
import json
import re
import shutil
import subprocess
import sys
import threading
import uuid
from datetime import datetime, timezone
from pathlib import Path

import approved_lines as AL
import check_scripted as CS
import grade_eval as G
import harness as H
import leader as L

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

INCLUDE_FACTS = re.compile(r"^<!-- include-facts: (\S+) -->$", re.M)
TIERS = ("core", "regression")
CORE_RUNS = 3
SMOKE = False  # --smoke: one run each, verdicts marked SMOKE and never counted as a core pass

# Rough API-equivalent cost per call (USD), for the estimate printed before each round. A subscription
# isn't billed it; --cost-from replaces it with a previous round's measured usage.
EST_USD = {"skill_turn": 0.30, "leader_turn": 0.04, "grader": 0.50, "rubric": 0.40, "control": 0.05, "run_chat": 0.30}
EST_TURNS_WITH_LEADER = 25


def load_script(evals_dir, rel):
    """A leader script, with each `<!-- include-facts: students/X.md -->` line replaced by X's
    "What you know" section, so a script that says "the same facts as I1" carries I1's facts."""
    def facts(m):
        other = (evals_dir / m.group(1)).read_text()
        sec = re.search(r"^## What you know\n(.*?)(?=^## |\Z)", other, re.M | re.S)
        if not sec:
            raise ValueError(f"{m.group(1)} has no '## What you know' section")
        return f"## {Path(m.group(1)).stem}: the facts referred to above\n{sec.group(1).rstrip()}\n"
    return INCLUDE_FACTS.sub(facts, (evals_dir / rel).read_text())


lock = threading.Lock()


def load_evals(path):
    data = json.loads(Path(path).read_text())
    for ev in data["evals"]:
        ev["expectations"] = [x if isinstance(x, dict) else {"text": x, "kind": "judged"} for x in ev["expectations"]]
        CS.resolve_release_items(ev)  # judged items and preconditions that read the release checks
    return data


def tier_of(ev, data):
    return ev.get("tier") or data.get("default_tier") or "regression"


def build_fixture(fixture, target, evals_dir, builder=None):
    """`empty` makes an empty workspace; `dir:<path>` copies a committed folder (relative to the
    evals.json folder); anything else is a name passed to the evals file's `fixture_builder`
    (default fixtures/make_fixture.py beside it)."""
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
        raise H.HarnessFailure(f"no fixture builder for {fixture!r}: {maker}")
    r = subprocess.run([sys.executable, str(maker), fixture, str(target)], capture_output=True, text=True)
    if r.returncode != 0:
        raise H.HarnessFailure(f"fixture {fixture}: {r.stderr[-800:]}")


def tools_for(ev, s):
    kind = s.get("tools", ev.get("tools"))
    if kind == "no_file":
        return H.NO_FILE_TOOLS
    if kind == "web":
        return H.WEB_TOOLS
    if kind == "agent":
        return H.AGENT_TOOLS
    return H.SKILL_TOOLS


def file_list(ws):
    return sorted(str(p.relative_to(ws)) for p in ws.rglob("*") if p.is_file())


def leader_prompt(turns, screens):
    convo = "\n\n".join(f"## {'AI' if t['role'] == 'ai' else 'You'}\n\n{t['text']}" for t in turns)
    screen = ("\n\n## Your screen now\n\n" + "\n\n".join(screens)) if screens else ""
    return f"The conversation so far:\n\n{convo}{screen}\n\nYour next message as the leader:"


def connections_for(platform, ws, root, data):
    """The stand-in connections a Claude Code (or Codex) session of Build sees: Gmail, when the
    workflow's plan uses it, as a leader who connected it would have (harness.gmail_mcp); on
    Microsoft 365, the Outlook the Cowork chat reaches, when the plan uses Outlook. Test's
    evals don't get it yet: its waiting-on-access cases need a way to show Gmail not connected first."""
    if data.get("skill_name") != "build":
        return None
    if platform.key == "microsoft-365":  # the Outlook a Cowork chat reaches, for its quick real check
        plans = list(Path(ws).glob("onedrive/Framework/*/design-plan.md"))
        if any(re.search(r"(?m)^Outlook: ", p.read_text()) for p in plans):
            return H.gmail_mcp(root, server="outlook", service="Outlook")
        return None
    if platform.key not in ("claude-code", "codex"):
        return None
    plans = [p for p in Path(ws).glob("framework/*/design-plan.md")]
    if not any(re.search(r"(?m)^Gmail: ", p.read_text()) for p in plans):
        return None
    return H.gmail_mcp(root)


def settings_prompt_for(platform, ws, root, data, s=None, ev=None):
    """The leader's click on Claude Code's prompt for `.claude/settings.local.json`
    (harness.settings_prompt): Build writes the block there and lifts it, and Test adds the wrapper's
    rules and lifts a block it took over, each with the Edit or Write tool. Claude Code only.
    Fault leader_denies_settings_prompt: the leader declines that prompt."""
    if data.get("skill_name") not in ("build", "test") or platform.key != "claude-code":
        return None
    faults = (s or {}).get("platform_faults") or (ev or {}).get("platform_faults") or []
    return H.settings_prompt(root, ws, leader_declines="leader_denies_settings_prompt" in faults)


def make_run_chat(rnd, root, ws, args, calls):
    """A new chat the leader opens on a chat platform: a cold session with only the built workflow,
    nothing from the framework (rules 3.5), that answers the pasted block once. On Claude Code and
    Codex (Test's leader runs, leader.simulates_leader_runs) it is a new session in the workspace
    itself, as the leader's second terminal is: the installed workflow loads from there, and whatever
    the run saves lands in the workspace for Test to find and check."""
    def run_chat(block, platform):
        if platform.run_in_workspace:
            cold = ws
        else:
            cold = root / f"run-chat-{uuid.uuid4().hex[:8]}"
            cold.mkdir()
            skills = ws / ".claude" / "skills"
            if skills.exists():
                shutil.copytree(skills, cold / ".claude" / "skills")
        text, rec = H.call(rnd, "skill", root, block, cwd=cold, tools=H.SKILL_TOOLS, plugin=None,
                           model=args.skill_model, append_system_prompt=platform.run_preamble())
        rec["role"] = "run_chat"
        calls.append(rec)
        return text
    return run_chat


def run_once(rnd, ev, k, out, args, evals_dir, data):
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
            H.reset_home(root)  # fresh temp HOME per session; kept across this session's --resume turns
            platform = L.platform_for(ev, s)
            platform.leader_runs = L.simulates_leader_runs(data.get("skill_name"), platform, s, ev)
            if s.get("fixture_from"):
                src = Path(s["fixture_from"])
                src = src if src.is_absolute() else (evals_dir / src)
                if ws.exists():
                    shutil.rmtree(ws)
                shutil.copytree(src, ws)
            elif n == 1 or not s.get("from_previous"):
                build_fixture(s.get("fixture", ev.get("fixture")), ws, evals_dir, data.get("fixture_builder"))
                platform.prepare(ws)
            sdir = root / f"session-{n}"
            shutil.copytree(ws, sdir / "workspace-start")
            script = None
            if isinstance(s.get("student"), str):
                script = load_script(evals_dir, s["student"])
            elif s.get("student") and ev.get("student"):
                script = load_script(evals_dir, ev["student"])
            replies = list(s.get("replies", []))
            cap = s.get("max_turns", ev.get("max_turns", args.max_turns))
            tools = tools_for(ev, s)
            if "no_gmail" in (s.get("platform_faults") or ev.get("platform_faults") or []):
                mcp = None  # a leader who hasn't connected Gmail
            else:
                mcp = connections_for(platform, ws, root, data)
            prompt_tool = settings_prompt_for(platform, ws, root, data, s, ev)
            run_chat = make_run_chat(rnd, root, ws, args, calls)
            sid = str(uuid.uuid4())
            turns, files_by_turn, cap_hit = [], [], False
            msg, msg_kind, acts, shown = s["prompt"], "prompt", 0, ""
            for turn in range(cap):
                turns.append({"role": "student", "text": msg, msg_kind: True, "actions": acts,
                              **({"screen": shown} if shown else {})})
                kw = {"session_id": sid} if turn == 0 else {"resume": sid}
                H.write_settings_gate(prompt_tool, turns)
                ai, rec = H.call(rnd, "skill", root, msg, cwd=ws, tools=tools, plugin=plugin,
                                 model=args.skill_model, append_system_prompt=platform.preamble(),
                                 log=sdir / "events.jsonl", mcp=mcp, prompt_tool=prompt_tool, **kw)
                rec.update(session=n, turn=turn + 1)
                calls.append(rec)
                turns.append({"role": "ai", "text": ai})
                files_by_turn.append(file_list(ws))
                screens = platform.screen(ai, ws, run_chat)
                shown = "\n\n".join(o for o, _ in screens)
                if replies:
                    msg, msg_kind, acts = replies.pop(0), "scripted_reply", sum(a for _, a in screens)
                elif script:
                    raw, srec = H.call(rnd, "student", root, leader_prompt(turns, [o for o, _ in screens]),
                                       cwd=root / "student", tools=[],
                                       system_prompt=L.LEADER_RULES + script + platform.leader_notes())
                    srec.update(session=n, turn=turn + 1)
                    calls.append(srec)
                    msg, reported = L.strip_actions(raw)
                    acts = sum(a for _, a in screens) + reported + platform.on_leader(msg, ws)
                    msg_kind = "student"
                    for w in s.get("run_writes", []):
                        target = ws / w["path"]
                        if re.search(w["when"], msg, re.M) and not target.exists():
                            target.parent.mkdir(parents=True, exist_ok=True)
                            target.write_text(w["text"])
                    if msg.strip().splitlines() and msg.strip().splitlines()[-1].strip() == "END":
                        # END closes the run even after a stray line of the leader's own reasoning
                        turns.append({"role": "student", "text": "END", "end": True, "actions": acts,
                                      **({"screen": shown} if shown else {})})
                        break
                else:
                    break
            else:
                cap_hit = "max_turns" not in s  # a session's own max_turns is a deliberate stop
            shutil.copytree(ws, sdir / "workspace")
            start, end = CS.load_tree(sdir / "workspace-start"), CS.load_tree(sdir / "workspace")
            run["sessions"].append({"n": n, "turns": turns, "files_by_turn": files_by_turn,
                                    "files_start": start, "files_end": end, "cap_hit": cap_hit,
                                    "root": str(sdir / "workspace"), "platform": platform.key,
                                    "script_quotes": CS.script_quotes(script)})
        # Grade inside the run root's lifetime (the graders run from run-root/grader).
        scripted = CS.run_checks(ev, run, data)
        if any(s["cap_hit"] for s in run["sessions"]):
            scripted.append({"text": "The run ends before the turn cap", "kind": "scripted",
                             "passed": False, "evidence": "turn cap hit"})
        if ev.get("student") or any(isinstance(x.get("student"), str) for x in sessions):
            ok, why = CS.fidelity(run)
            fid = {"passed": ok, "evidence": why}
        judged, grec = G.grade(rnd, root, ev, run, evals_dir)
        if grec:
            calls.append(grec)
        if data.get("judge_rubric", True) and ev.get("judge_rubric", True):
            rubric, rrec = G.grade_rubric(rnd, root, ev, run)
            judged += rubric
            if rrec:
                rrec["role"] = "rubric"
                calls.append(rrec)
    except H.UsageLimit as e:
        status, note = "usage_pause", str(e)
    except H.HarnessFailure as e:
        status, note = "harness_failure", str(e)
    if status != "valid":
        shutil.rmtree(root, ignore_errors=True)
        for p in rdir.iterdir():  # nothing is copied back from a failed run except the failure itself
            if p.name != "eval.json":
                shutil.rmtree(p) if p.is_dir() else p.unlink()
        res = {"eval": ev["id"], "run": k, "tier": tier_of(ev, data), "status": status, "note": H.scrub(note)}
        (rdir / "result.json").write_text(json.dumps(res, indent=2))
        return res

    pre = [j for j in judged if j.get("precondition")]
    if fid and not fid["passed"]:
        status, note = "invalid", "fidelity: " + fid["evidence"]
    elif any(not j["passed"] for j in pre):
        status, note = "invalid", "precondition: " + "; ".join(j["text"] for j in pre if not j["passed"])
    exp = scripted + [j for j in judged if not j.get("precondition")]
    counts = L.count_actions(run["sessions"])
    res = {"eval": ev["id"], "run": k, "tier": tier_of(ev, data), "status": status, "note": note,
           "models": sorted({m for c in calls for m in c["model_used"]}),
           "claude_code_version": rnd.version, "fidelity": fid, "preconditions": pre,
           "expectations": exp,
           "passed": sum(1 for e in exp if e["passed"]), "total": len(exp),
           "leader_actions": {**counts, "report": L.action_report(counts, ev.get("action_target")),
                              "target": ev.get("action_target")},
           "denials": [d for c in calls for d in c["permission_denials"]],
           "usd": round(sum(c.get("total_cost_usd") or 0 for c in calls), 4)}
    for sess in run["sessions"]:  # copy back named outputs only
        n = sess["n"]
        out_s = rdir / f"session-{n}"
        out_s.mkdir()
        if (root / f"session-{n}" / "events.jsonl").exists():
            shutil.copy2(root / f"session-{n}" / "events.jsonl", out_s / "events.jsonl")
        (out_s / "turns.json").write_text(json.dumps(sess["turns"], indent=2, ensure_ascii=False))
        (out_s / "transcript.md").write_text("\n".join(
            f"## {'AI' if t['role'] == 'ai' else 'Leader'}\n\n{t['text']}\n" for t in sess["turns"])
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
    if (root / "settings-prompt.jsonl").exists():  # the leader's clicks on the settings prompt
        shutil.copy2(root / "settings-prompt.jsonl", rdir / "settings-prompt.jsonl")
    shutil.rmtree(root, ignore_errors=True)
    hits = H.commit_leak_scan(rdir)
    if hits:
        shutil.rmtree(rdir)
        rdir.mkdir(parents=True)
        res = {"eval": ev["id"], "run": k, "tier": tier_of(ev, data), "status": "harness_failure",
               "note": f"leak scan hits: {len(hits)} (results deleted): "
                       + "; ".join(h.replace(str(rdir) + "/", "") for h in hits)}
        (rdir / "result.json").write_text(json.dumps(res, indent=2))
    return res


def run_slot(rnd, ev, k, out, args, evals_dir, data, budget):
    """A run slot: re-run an invalid run up to twice; a third invalid counts as a failure."""
    for attempt in range(3):
        with lock:
            if budget["usd"] >= args.max_usd or budget["paused"]:
                return {"eval": ev["id"], "run": k, "tier": tier_of(ev, data), "status": "skipped",
                        "note": "budget or usage pause"}
        res = run_once(rnd, ev, k, out, args, evals_dir, data)
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


def pass_bar(x, n, tier="regression"):
    """Core: every expectation passes in every run. Regression: scripted and must-level judged pass
    every run; other judged pass 2 of 3 (7 of 10, 4 of 5). `gating: false` is info only."""
    if tier == "core" or x["kind"] == "scripted" or x.get("must"):
        return n
    return {1: 1, 2: 2, 3: 2, 5: 4, 10: 7}.get(n, -(-n * 2 // 3))


def eval_verdict(ev, rs, tier):
    """PASS, FAIL or NOT COUNTED (core with fewer than three valid runs) for one eval."""
    graded = [r for r in rs if r["status"] in ("valid", "failed_invalid_cap") and r.get("expectations")]
    if tier == "core" and not SMOKE and len([r for r in graded if r["status"] == "valid"]) < CORE_RUNS:
        return "NOT COUNTED", graded
    if not graded:
        return "NO RESULT", graded
    for i, x in enumerate(graded[0]["expectations"]):
        if x.get("gating") is False:
            continue
        got = [r["expectations"][i]["passed"] for r in graded if i < len(r["expectations"])]
        if sum(got) < pass_bar(x, len(got), tier):
            return ("SMOKE FAIL" if SMOKE else "FAIL"), graded
    return ("SMOKE PASS" if SMOKE else "PASS"), graded


def summarize(out, evs, results, data):
    lines = ["# Round summary", ""]
    tiers = {}
    for t in TIERS:
        tevs = [ev for ev in evs if tier_of(ev, data) == t]
        if not tevs:
            continue
        verdicts = {ev["id"]: eval_verdict(ev, [r for r in results if r["eval"] == ev["id"]], t)[0] for ev in tevs}
        tiers[t] = verdicts
        counts = {v: list(verdicts.values()).count(v) for v in sorted(set(verdicts.values()))}
        lines += [f"## Tier: {t} ({len(tevs)} evals)", "",
                  "Core cases run three times and count only when every expectation passes every run."
                  if t == "core" else "Regression: scripted and must-level checks every run; other judged 2 of 3.", "",
                  "Verdicts: " + ", ".join(f"{k} {v}" for k, v in counts.items()), ""]
        for ev in tevs:
            rs = sorted([r for r in results if r["eval"] == ev["id"]], key=lambda r: r["run"])
            verdict, graded = eval_verdict(ev, rs, t)
            lines += [f"### {ev['id']} — {ev.get('name', '')}: {verdict}", ""]
            lines.append("Runs: " + ", ".join(
                f"run-{r['run']} {r['status']}" + (f" {r['passed']}/{r['total']}" if "total" in r else "") for r in rs))
            acts = [r["leader_actions"]["report"] for r in rs if r.get("leader_actions")]
            if acts:
                lines.append("Leader actions: " + " | ".join(acts))
            if graded:
                lines.append("")
                for i, x in enumerate(graded[0]["expectations"]):
                    got = [r["expectations"][i]["passed"] for r in graded if i < len(r["expectations"])]
                    need = pass_bar(x, len(got), t)
                    v = "info" if x.get("gating") is False else "PASS" if sum(got) >= need else "FAIL"
                    lines.append(f"- {v} {sum(got)}/{len(got)} (needs {need}) [{x['kind']}"
                                 + (", must" if x.get("must") else "") + f"] {x['text'][:140]}")
            lines.append("")
    (out / "summary.md").write_text("\n".join(lines))
    return tiers


def runs_for(ev, args, data):
    if getattr(args, "smoke", False):
        return 1
    n = args.runs or ev.get("runs", 3)
    return max(n, CORE_RUNS) if tier_of(ev, data) == "core" else n


def estimate(evs, args, data):
    """Per-eval and total cost estimates, printed before every round."""
    measured = {}
    if args.cost_from:
        for f in Path(args.cost_from).glob("*/run-*/result.json"):
            r = json.loads(f.read_text())
            if r.get("usd"):
                measured.setdefault(r["eval"], []).append(r["usd"])
    rows, total = [], 0.0
    for ev in evs:
        runs = runs_for(ev, args, data)
        if ev["id"] in measured:
            per = sum(measured[ev["id"]]) / len(measured[ev["id"]])
            basis = f"measured, {len(measured[ev['id']])} runs"
        else:
            sessions = ev.get("sessions") or [{"student": True}]
            per = 0.0
            for s in sessions:
                leads = bool(s.get("student")) or bool(s.get("replies"))
                turns = ev.get("est_turns") or (EST_TURNS_WITH_LEADER if leads else 1)
                per += turns * EST_USD["skill_turn"] + (turns * EST_USD["leader_turn"] if s.get("student") else 0)
            per += EST_USD["grader"] + (EST_USD["rubric"] if data.get("judge_rubric", True) and ev.get("judge_rubric", True) else 0)
            basis = "rough, per-call rates"
        cost = per * runs
        total += cost
        rows.append((ev["id"], tier_of(ev, data), runs, per, cost, basis))
    return rows, total + EST_USD["control"]


def print_estimate(rows, total):
    print("Cost estimate for this round (API-equivalent USD; a subscription isn't billed it):")
    print(f"  {'eval':<22} {'tier':<11} {'runs':>4} {'per run':>9} {'cost':>9}  basis")
    for eid, tier, runs, per, cost, basis in rows:
        print(f"  {eid:<22} {tier:<11} {runs:>4} {per:>9.2f} {cost:>9.2f}  {basis}")
    print(f"  {'total (with the control call)':<48} {total:>9.2f}")


def dry_run(evs, evals_path, data):
    """Everything a round does before its first model call."""
    import validate_evals as V
    errs = V.validate_file(evals_path, build=True, only={ev["id"] for ev in evs})
    evals_dir = evals_path.parent
    for ev in evs:
        for s in ev.get("sessions") or [{"student": True}]:
            for p in [s["student"]] if isinstance(s.get("student"), str) else ([ev["student"]] if ev.get("student") and s.get("student") else []):
                try:
                    load_script(evals_dir, p)
                except (OSError, ValueError) as e:
                    errs.append(f"{ev['id']}: script {p}: {e}")
            L.platform_for(ev, s)
    corpus = AL.load()
    for ln in corpus.checkable():
        ln.regex  # every approved line compiles
    return errs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out_dir")
    ap.add_argument("eval_ids", nargs="*")
    ap.add_argument("--evals", required=True)
    ap.add_argument("--tier", choices=["core", "regression", "all"], default="all")
    ap.add_argument("--runs", type=int)
    ap.add_argument("--plugin", default=str(ROOT / "plugins" / "handsonai"))
    ap.add_argument("--max-turns", type=int, default=80)
    ap.add_argument("--parallel", type=int, default=2)
    ap.add_argument("--skill-model", default=H.SKILL_MODEL)
    ap.add_argument("--max-usd", type=float, default=float("inf"))
    ap.add_argument("--cost-from")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--smoke", action="store_true",
                    help="smoke round: every selected eval runs once; verdicts are SMOKE PASS/FAIL and never count as a core pass")
    ap.add_argument("--yes", action="store_true")
    args = ap.parse_args()
    global SMOKE
    SMOKE = args.smoke

    evals_path = Path(args.evals).resolve()
    evals_dir = evals_path.parent
    data = load_evals(evals_path)
    by_id = {e["id"]: e for e in data["evals"]}
    missing = [i for i in args.eval_ids if i not in by_id]
    if missing:
        sys.exit(f"unknown eval ids: {missing}")
    retired = [i for i in args.eval_ids if by_id[i].get("retired")]
    if retired:
        sys.exit(f"retired evals can't run: {retired}")
    evs = [by_id[i] for i in args.eval_ids] if args.eval_ids else [e for e in data["evals"] if not e.get("retired")]
    if args.tier != "all":
        evs = [ev for ev in evs if tier_of(ev, data) == args.tier]
    if not evs:
        sys.exit("no evals to run")

    rows, total = estimate(evs, args, data)
    print_estimate(rows, total)
    if args.dry_run:
        errs = dry_run(evs, evals_path, data)
        for e in errs:
            print("ERROR", e)
        print(f"dry run: {len(evs)} evals, fixtures built, scripts loaded, checks valid; no model calls"
              if not errs else f"dry run: {len(errs)} errors")
        sys.exit(1 if errs else 0)
    if not args.yes:
        print("Not started: show James this estimate, then re-run with --yes. No model calls were made.")
        sys.exit(3)

    out = Path(args.out_dir).resolve()
    out.mkdir(parents=True, exist_ok=True)
    before = H.real_config_snapshot()
    if H.leak_signs():
        sys.exit(f"leak signs before the round: {H.leak_signs()}")
    rnd = H.Round()
    croot = H.new_run_root()  # the allowed bundled skills and built-in plugins, from a no-plugin control call
    _, crec = H.call(rnd, "control", croot, "Say OK.", cwd=croot / "grader", tools=[])
    rnd.bundled_skills = crec["init"]["skills"]
    rnd.bundled_plugins = [p["source"] for p in crec["init"]["plugins"] if p.get("path") == "builtin"]
    auth = H.auth_method(rnd, croot)
    shutil.rmtree(croot)
    if auth != "oauth_token":
        sys.exit(f"authMethod is {auth}, expected oauth_token")

    budget = {"usd": 0.0, "paused": False}
    jobs = [(ev, k) for ev in evs for k in range(1, runs_for(ev, args, data) + 1)]
    results = []
    with cf.ThreadPoolExecutor(max_workers=args.parallel) as pool:
        futs = {pool.submit(run_slot, rnd, ev, k, out, args, evals_dir, data, budget): (ev, k) for ev, k in jobs}
        for f in cf.as_completed(futs):
            try:
                r = f.result()
            except Exception as e:  # a bug in the runner: record it as a harness failure
                ev, k = futs[f]
                r = {"eval": ev["id"], "run": k, "tier": tier_of(ev, data), "status": "harness_failure",
                     "note": H.scrub(repr(e))[:500]}
            results.append(r)
            print(f"[{r.get('tier')}] {r['eval']} run-{r['run']}: {r['status']}"
                  + (f" {r['passed']}/{r['total']}" if "total" in r else "")
                  + (f" ({r['note'][:200]})" if r.get("note") else ""), flush=True)

    after = H.real_config_snapshot()
    problems = H.compare_snapshots(before, after)
    tiers = summarize(out, evs, results, data)
    try:
        evals_rel = str(evals_path.relative_to(ROOT))
    except ValueError:
        evals_rel = str(evals_path)
    round_info = {"finished": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                  "claude_code_version": rnd.version, "auth_method": auth,
                  "skill_model": args.skill_model, "student_model": H.STUDENT_MODEL,
                  "grader_model": H.GRADER_MODEL, "evals_file": evals_rel,
                  "estimate_usd": round(total, 2), "usd_reported": round(budget["usd"], 4),
                  "fail_closed_check": "pass" if not problems else problems,
                  "tiers": tiers,
                  "results": [{k: r.get(k) for k in ("eval", "run", "tier", "status", "passed", "total", "note")}
                              for r in results]}
    (out / "round.json").write_text(json.dumps(round_info, indent=2))
    for t, verdicts in tiers.items():
        vs = list(verdicts.values())
        print(f"tier {t}: {vs.count('PASS')} pass, {vs.count('FAIL')} fail, "
              f"{len(vs) - vs.count('PASS') - vs.count('FAIL')} not counted, of {len(vs)}")
    if problems:
        print("FAIL-CLOSED CHECK FAILED: the round is void:", problems)
        sys.exit(2)
    print(f"round done; reported usage ${budget['usd']:.2f}; summary in {out / 'summary.md'}")


if __name__ == "__main__":
    main()
