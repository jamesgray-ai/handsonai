#!/usr/bin/env python3
"""The leader's click on Claude Code's settings prompt, for Build and Test sessions in the evals
(stdio MCP, JSON-RPC 2.0; Claude Code's --permission-prompt-tool).

Build writes the block into `.claude/settings.local.json` with its Edit or Write tool, so Claude Code
asks the leader to allow it (claude-code-block.md section 4 step 5). A `claude -p` session can't
show that prompt and refuses the write even with an allow rule, so this tool answers it the way the
leader would: it allows an Edit, Write or MultiEdit whose file_path resolves to the workspace's own
`.claude/settings.local.json`, and denies everything else but one case: an Edit, Write or MultiEdit
inside the workspace's own `.claude/skills/` or `.claude/agents/` (Build installing the parts it built,
and its check agents' files, claude-code-block.md section 6), which Claude Code also asks about and
the leader running Build allows. It also denies the settings file when:
- the leader declined Claude Code's prompt (SETTINGS_PROMPT_DENY=1, the eval's
  `leader_denies_settings_prompt` fault), or
- the gate file (SETTINGS_PROMPT_GATE, rewritten by the runner before every turn) says the leader
  answered no to N-B20. Where N-B20 wasn't asked in this session (a resumed entry using the
  recorded OK, or N-B20 said in the same turn as the write), the gate can't tell: it allows.
Every decision is appended to SETTINGS_PROMPT_LOG (JSON lines), the path relative to the workspace.
"""
import json
import os
import sys
import time

TOOL = "approve"
FILE_TOOLS = ("Edit", "Write", "MultiEdit")
TARGET = os.path.join(".claude", "settings.local.json")
PARTS = (os.path.join(".claude", "skills"), os.path.join(".claude", "agents"))


def _real(p):
    return os.path.realpath(p)


def decide(tool_name, tool_input, workspace, gate=None, leader_declines=False):
    """(allow: bool, reason: str). Pure: the unit tests call it directly."""
    if tool_name not in FILE_TOOLS:
        return False, f"{tool_name} isn't a file edit the leader's settings prompt covers"
    path = (tool_input or {}).get("file_path") or ""
    if not path:
        return False, "no file_path"
    full = path if os.path.isabs(path) else os.path.join(workspace, path)
    for d in PARTS:
        root = _real(os.path.join(workspace, d))
        if _real(full).startswith(root + os.sep):
            return True, f"Build's own write inside the workspace's {d}/"
    if _real(full) != _real(os.path.join(workspace, TARGET)):
        return False, "not the workspace's .claude/settings.local.json"
    if leader_declines:
        return False, "the leader declined Claude Code's prompt (fault leader_denies_settings_prompt)"
    state = (gate or {}).get("n_b20", "unseen")
    if state == "no":
        return False, "the leader said no to N-B20"
    if state == "ok":
        return True, "the leader said OK to N-B20"
    return True, "N-B20 not seen before this turn in this session (allowed: can't tell)"


def _rel(path, workspace):
    full = path if os.path.isabs(path) else os.path.join(workspace, path)
    try:
        return os.path.relpath(_real(full), _real(workspace))
    except ValueError:
        return "(outside the workspace)"


def _gate():
    p = os.environ.get("SETTINGS_PROMPT_GATE")
    try:
        with open(p) as f:
            return json.load(f)
    except (TypeError, OSError, ValueError):
        return {}


def answer(args):
    ws = os.environ.get("SETTINGS_PROMPT_WORKSPACE", os.getcwd())
    name, inp = args.get("tool_name"), args.get("input") or {}
    gate = _gate()
    ok, why = decide(name, inp, ws, gate, os.environ.get("SETTINGS_PROMPT_DENY") == "1")
    log = os.environ.get("SETTINGS_PROMPT_LOG")
    if log:
        with open(log, "a") as f:
            f.write(json.dumps({"t": time.time(), "tool": name,
                                "path": _rel(inp["file_path"], ws) if inp.get("file_path") else None,
                                "n_b20": gate.get("n_b20", "unseen"),
                                "decision": "allow" if ok else "deny", "reason": why}) + "\n")
    if ok:
        return {"behavior": "allow", "updatedInput": inp}
    return {"behavior": "deny", "message": "The leader didn't allow this: " + why}


def reply(rid, result=None, error=None):
    msg = {"jsonrpc": "2.0", "id": rid}
    msg.update({"error": error} if error else {"result": result})
    sys.stdout.write(json.dumps(msg) + "\n")
    sys.stdout.flush()


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
        except ValueError:
            continue
        rid, method, params = req.get("id"), req.get("method"), req.get("params") or {}
        if rid is None:
            continue
        if method == "initialize":
            reply(rid, {"protocolVersion": params.get("protocolVersion", "2025-06-18"),
                        "capabilities": {"tools": {}}, "serverInfo": {"name": "leader_click", "version": "0.1"}})
        elif method == "tools/list":
            reply(rid, {"tools": [{"name": TOOL, "description": "The leader's answer to a permission prompt.",
                                   "inputSchema": {"type": "object", "properties": {
                                       "tool_name": {"type": "string"}, "input": {"type": "object"},
                                       "tool_use_id": {"type": "string"}}, "required": ["tool_name"]}}]})
        elif method == "tools/call":
            if params.get("name") != TOOL:
                reply(rid, error={"code": -32602, "message": f"unknown tool {params.get('name')}"})
                continue
            out = answer(params.get("arguments") or {})
            reply(rid, {"content": [{"type": "text", "text": json.dumps(out)}]})
        elif method == "ping":
            reply(rid, {})
        else:
            reply(rid, error={"code": -32601, "message": f"method not found: {method}"})


if __name__ == "__main__":
    main()
