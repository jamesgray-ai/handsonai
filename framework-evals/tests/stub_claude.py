#!/usr/bin/env python3
"""A stub `claude` binary for the harness's own tests: never a live model, never ~/.claude.

It answers `claude -p … --output-format stream-json` with an init message and a result, the way
the pinned CLI does, and `claude auth status --json` with an oauth_token login. What it says is
set by stub-mode.json beside it:
  {"version": "9.9.9", "extra_plugin": false, "mcp_servers": [], "skill_replies": ["…", …]}
The skill's replies are taken in turn (a counter file beside it); the leader always says END;
graders pass everything.
"""
import json
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
MODE = json.loads((HERE / "stub-mode.json").read_text()) if (HERE / "stub-mode.json").exists() else {}


def arg(name):
    a = sys.argv
    return a[a.index(name) + 1] if name in a else None


def main():
    if sys.argv[1:3] == ["auth", "status"]:
        print(json.dumps({"authMethod": "oauth_token", "loggedIn": True}))
        return
    if "--version" in sys.argv:
        print(f"{MODE.get('version', '9.9.9')} (Claude Code)")
        return
    prompt = sys.stdin.read()
    system = arg("--system-prompt") or ""
    plugin = arg("--plugin-dir")
    tools = [t for t in (arg("--tools") or "").split(",") if t]
    plugins = [{"name": "handsonai", "path": plugin, "source": "handsonai@inline"}] if plugin else []
    if MODE.get("extra_plugin"):
        plugins.append({"name": "someone-elses-plugin", "path": "/Users/someone/.claude/plugins/x", "source": "x@market"})
    init = {"type": "system", "subtype": "init", "cwd": os.getcwd(), "model": arg("--model"), "tools": tools,
            "mcp_servers": MODE.get("mcp_servers", []), "skills": ["handsonai:deconstruct"] if plugin else [],
            "plugins": plugins, "agents": [], "memory_paths": {}, "apiKeySource": "none",
            "claude_code_version": MODE.get("version", "9.9.9"), "permissionMode": "default"}
    if "You grade a test run" in system:
        n = len(re.findall(r"^\d+\. ", prompt.split("## Items to grade", 1)[-1].split("\n# Session", 1)[0], re.M))
        text = json.dumps({"results": [{"n": i, "passed": True, "evidence": "stub"} for i in range(1, n + 1)]})
    elif "fixed rubric" in system:
        n = len(re.findall(r"^## Message \d+", prompt, re.M))
        text = json.dumps({"messages": [{"n": i, "fail": [], "evidence": ""} for i in range(1, n + 1)]})
    elif "playing a business leader" in system:
        text = "END"
    elif prompt.strip() == "Say OK.":
        text = "OK"
    else:
        counter = HERE / ".stub-counter"
        k = int(counter.read_text()) if counter.exists() else 0
        replies = MODE.get("skill_replies") or ["OK."]
        text = replies[k % len(replies)]
        counter.write_text(str(k + 1))
    print(json.dumps(init))
    print(json.dumps({"type": "result", "subtype": "success", "is_error": False, "result": text,
                      "modelUsage": {arg("--model") or "stub": {}}, "permission_denials": [],
                      "usage": {"input_tokens": 0}, "total_cost_usd": 0.0, "num_turns": 1, "duration_ms": 1}))


if __name__ == "__main__":
    main()
