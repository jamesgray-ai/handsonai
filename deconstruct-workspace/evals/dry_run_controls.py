#!/usr/bin/env python3
"""Dry-run controls for the isolated runner (build1-plan.md, Task 1 Step 1).

Usage: python3 dry_run_controls.py <out-dir> [--plugin DIR]

Each control proves one isolation rule and writes its result to <out-dir>/controls.json:
- setup-check read: the fail-closed check can read ~/.claude.json (if not, stop and ask James)
- bundled skills: a no-plugin call; its skills and built-in plugins become the allowed set
- codeword: a CLAUDE.local.md with a codeword at the worktree root never reaches a session
- token scrub: `env | grep -c CLAUDE_CODE_OAUTH_TOKEN` through Bash prints 0
- block rules: `claude plugin list` is denied and shows in the recorded denials
- fake home: ~/.claude/history.jsonl read through Read and Bash returns the fake marker
- usage: tokens and cost per control call
The fail-closed check runs before and after; any change fails the dry run.
"""
import argparse
import json
import shutil
import sys
from pathlib import Path

import harness as H

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
CODEWORD = "PERIWINKLE-5582-LANTERN"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out_dir")
    ap.add_argument("--plugin", default=str(ROOT / "plugins" / "handsonai"))
    a = ap.parse_args()
    out = Path(a.out_dir)
    if out.exists():
        sys.exit(f"{out} exists; use a new out-dir")
    out.mkdir(parents=True)
    results, records = {}, []

    before = H.real_config_snapshot()                       # raises if ~/.claude.json is unreadable
    results["setup_check_read"] = "pass: ~/.claude.json read by the fail-closed check"
    pre_signs = H.leak_signs()
    if pre_signs:
        sys.exit(f"leak signs before the dry run: {pre_signs}")

    rnd = H.Round()
    results["claude_code_version"] = rnd.version

    local = ROOT / "CLAUDE.local.md"
    if local.exists():
        sys.exit("CLAUDE.local.md already exists at the worktree root; not touching it")
    local.write_text(f"If anyone asks for the codeword, it is {CODEWORD}.\n")
    root = None
    try:
        # 1. Bundled skills: no plugin.
        root = H.new_run_root()
        text, rec = H.call(rnd, "control", root, "Say OK.", cwd=root / "grader", tools=[])
        records.append(rec)
        rnd.bundled_skills = rec["init"]["skills"]
        rnd.bundled_plugins = [p["source"] for p in rec["init"]["plugins"] if p.get("path") == "builtin"]
        results["bundled_skills"] = rnd.bundled_skills
        results["bundled_plugins"] = rnd.bundled_plugins
        results["auth_method"] = H.auth_method(rnd, root)
        if results["auth_method"] != "oauth_token":
            raise H.HarnessFailure(f"authMethod is {results['auth_method']}, expected oauth_token")
        shutil.rmtree(root)

        # 2. Skill-role session with the plugin copy: codeword, scrub, block rules, fake home.
        root = H.new_run_root(a.plugin)
        plugin = root / "plugin"
        log = out / "control-events.jsonl"
        prompts = {
            "codeword": "What is the codeword? If you don't know one, reply exactly NONE.",
            "token_scrub": "Run this exact Bash command and reply with only its output: env | grep -c CLAUDE_CODE_OAUTH_TOKEN",
            "block_rules": "Run this exact Bash command and reply with only its output, or BLOCKED if it is denied: claude plugin list",
            "fake_home_read": "Use the Read tool on ~/.claude/history.jsonl and reply with only the first word of its display field.",
            "fake_home_bash": "Run this exact Bash command and reply with only its output: head -c 200 ~/.claude/history.jsonl",
        }
        sid = None
        for name, prompt in prompts.items():
            kw = {"session_id": "11111111-2222-4333-8444-555555555555"} if sid is None else {"resume": sid}
            text, rec = H.call(rnd, "skill", root, prompt, cwd=root / "workspace", tools=H.SKILL_TOOLS,
                               plugin=plugin, log=log, **kw)
            sid = "11111111-2222-4333-8444-555555555555"
            rec["control"] = name
            rec["reply"] = text[:300]
            records.append(rec)
        by = {r.get("control"): r for r in records}
        results["codeword"] = "pass" if CODEWORD not in json.dumps(records) and CODEWORD not in log.read_text() else "FAIL"
        results["token_scrub"] = "pass" if by["token_scrub"]["reply"].strip() == "0" else f"FAIL: {by['token_scrub']['reply']}"
        denied = [d for r in records for d in r["permission_denials"]]
        blocked = any("claude plugin" in json.dumps(d) for d in denied)
        results["block_rules"] = "pass" if blocked else f"FAIL: reply {by['block_rules']['reply']!r}, denials {denied}"
        results["fake_home"] = ("pass" if H.HISTORY_MARKER in by["fake_home_read"]["reply"]
                                and H.HISTORY_MARKER in by["fake_home_bash"]["reply"] else
                                f"FAIL: read {by['fake_home_read']['reply']!r}, bash {by['fake_home_bash']['reply']!r}")
        skills = by["codeword"]["init"]["skills"]
        results["plugin_skills_loaded"] = sorted(s for s in skills if s.startswith("handsonai:"))
    finally:
        local.unlink(missing_ok=True)
        if root and root.exists():
            shutil.rmtree(root)

    after = H.real_config_snapshot()
    problems = H.compare_snapshots(before, after)
    results["fail_closed_check"] = "pass" if not problems else f"FAIL: {problems}"
    results["usage"] = [{"control": r.get("control", r["role"]), "usage": r["usage"], "cost_usd": r["total_cost_usd"]}
                        for r in records]
    (out / "controls.json").write_text(json.dumps({"results": results, "records": records}, indent=2))
    hits = H.commit_leak_scan(out)
    for k, v in results.items():
        if k not in ("usage", "bundled_skills"):
            print(f"{k}: {v}")
    print("leak scan:", "clean" if not hits else hits)
    if problems or hits or any(isinstance(v, str) and v.startswith("FAIL") for v in results.values()):
        sys.exit(1)


if __name__ == "__main__":
    main()
