#!/usr/bin/env python3
"""Isolation for every eval call: run roots, login, per-role init checks, the fail-closed
check on the real Claude config, and leak scans.

Every `claude -p` call the runner, the student and the grader make goes through `call()`.
Rules (build1-plan.md, Global Constraints, "Eval safety"; kept by T18 when the harness moved to
framework-evals/: R12-1's keychain-only login and per-role init assertion, R12-3's fail-closed check):
- Each run gets its own run root under one eval parent folder in $TMPDIR, outside every repo
  and outside the home folder. It holds home/ (temp HOME; home/.claude is CLAUDE_CONFIG_DIR),
  workspace/ (the skill's working folder), plugin/ (a copy of the plugin under test),
  student/ and grader/ (empty folders the student and grader run from).
- Login is the setup-token in the macOS keychain (service handsonai-eval-token), passed only
  in CLAUDE_CODE_OAUTH_TOKEN, with CLAUDE_CODE_SUBPROCESS_ENV_SCRUB=1. It is never written
  anywhere; raw output is scanned for its prefix after every call.
- Every call checks its own init message for its role. A failed check raises HarnessFailure:
  the run stops and nothing is copied back.
"""
import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

SKILL_MODEL = "claude-opus-5-5"     # the model the skill session runs on; James can change it
STUDENT_MODEL = "claude-opus-5-5"
GRADER_MODEL = "claude-opus-5-5"

TOKEN_SERVICE = "handsonai-eval-token"
TOKEN_PREFIX = "sk-ant-oat"
HISTORY_MARKER = "HANDSONAI-EVAL-FAKE-HISTORY-7731"

# The skill's tools: passed to both --tools (what exists) and --allowedTools (pre-approved).
SKILL_TOOLS = ["Read", "Write", "Edit", "Bash", "Glob", "Grep", "Skill"]
AGENT_TOOLS = SKILL_TOOLS + ["Agent"]
NO_FILE_TOOLS = ["Read", "Glob", "Grep", "Skill"]   # NF1: no Write, Edit or Bash
WEB_TOOLS = SKILL_TOOLS + ["WebSearch", "WebFetch"]  # running a built workflow that researches (G2)

DENY_SETTINGS = {"permissions": {"deny": [
    "Bash(claude plugin:*)", "Bash(claude plugin *)", "Bash(claude mcp:*)", "Bash(claude mcp *)",
]}}

REAL_HOME = Path.home()
REAL_CLAUDE = REAL_HOME / ".claude"
REAL_CLAUDE_JSON = REAL_HOME / ".claude.json"

USAGE_LIMIT_RE = re.compile(r"usage limit|limit reached|rate.?limit|resets? (at|in)|429", re.I)
TRANSIENT_RE = re.compile(r"overloaded|API Error: 5\d\d|ECONNRESET|socket hang up|timed? ?out|network", re.I)


class HarnessFailure(Exception):
    """An isolation or harness problem: never a skill result."""


class UsageLimit(Exception):
    """The subscription's usage limit was hit: pause the round, never retry as a crash."""


# ---------- paths ----------

def real(p):
    return os.path.realpath(str(p))


def path_forms(p):
    """Both forms macOS temp paths appear in: /private/var/... and /var/..."""
    r = real(p)
    forms = {r}
    if r.startswith("/private/"):
        forms.add(r[len("/private"):])
    return forms


def dashed(p):
    """Claude Code's project-folder name: every non-alphanumeric character becomes '-'."""
    return re.sub(r"[^A-Za-z0-9]", "-", p)


def eval_parent():
    tmp = os.environ.get("TMPDIR") or tempfile.gettempdir()
    p = Path(real(tmp)) / "handsonai-evals"
    p.mkdir(exist_ok=True)
    if real(p).startswith(real(REAL_HOME)):
        raise HarnessFailure(f"eval parent folder is under the home folder: {p}")
    return p


# ---------- version pin ----------

def pin_binary():
    """Copy the versioned claude binary into the eval parent folder and call that copy all round."""
    found = shutil.which("claude")
    if not found:
        raise HarnessFailure("claude not found on PATH")
    src = Path(real(found))
    version = src.name if re.fullmatch(r"\d+\.\d+\.\d+", src.name) else None
    if not version:
        out = subprocess.run([str(src), "--version"], capture_output=True, text=True).stdout
        m = re.search(r"\d+\.\d+\.\d+", out)
        if not m:
            raise HarnessFailure("could not read the claude version")
        version = m.group(0)
    dst = eval_parent() / "bin" / f"claude-{version}"
    if not dst.exists():
        dst.parent.mkdir(exist_ok=True)
        shutil.copy2(src, dst)
    return str(dst), version


# ---------- login ----------

_token = None


def token():
    global _token
    if _token is None:
        r = subprocess.run(["security", "find-generic-password", "-s", TOKEN_SERVICE, "-w"],
                           capture_output=True, text=True)
        t = r.stdout.strip()
        if r.returncode != 0 or not t.startswith(TOKEN_PREFIX) or t.count(TOKEN_PREFIX) != 1:
            raise HarnessFailure(f"no usable token in the keychain under {TOKEN_SERVICE}")
        _token = t
    return _token


def scrub(text):
    t = _token
    return text.replace(t, "<TOKEN>") if t and text else text


# ---------- run roots ----------

GUIDANCE_FILES = ("CLAUDE.md", "CLAUDE.local.md", "AGENTS.md", ".claude/CLAUDE.md")


def assert_no_parent_guidance(root):
    for parent in Path(real(root)).parents:
        for name in GUIDANCE_FILES:
            if (parent / name).exists():
                raise HarnessFailure(f"guidance file in a parent of the run root: {parent / name}")


def new_run_root(plugin_src=None):
    root = Path(tempfile.mkdtemp(dir=eval_parent()))
    assert_no_parent_guidance(root)
    for sub in ("workspace", "student", "grader"):
        (root / sub).mkdir()
    if plugin_src:
        shutil.copytree(plugin_src, root / "plugin", symlinks=False)
    reset_home(root)
    return root


def reset_home(root):
    """Rebuild the temp HOME before each session: no memory carries between sessions."""
    home = root / "home"
    if home.exists():
        shutil.rmtree(home)
    cfg = home / ".claude"
    (cfg / "skills").mkdir(parents=True)
    (cfg / "history.jsonl").write_text(json.dumps({
        "display": f"{HISTORY_MARKER} draft the weekly status report",
        "pastedContents": {}, "timestamp": 1790000000000,
        "project": str(root / "workspace"), "sessionId": "00000000-0000-0000-0000-000000000000",
    }) + "\n")
    (root / "settings-deny.json").write_text(json.dumps(DENY_SETTINGS))


def env_for(root):
    home = root / "home"
    return {
        "PATH": "/usr/bin:/bin:/usr/sbin:/sbin:/opt/homebrew/bin:/usr/local/bin",
        "HOME": str(home),
        "CLAUDE_CONFIG_DIR": str(home / ".claude"),
        "TMPDIR": str(eval_parent()),
        "LANG": os.environ.get("LANG", "en_US.UTF-8"),
        "CLAUDE_CODE_OAUTH_TOKEN": token(),
        "CLAUDE_CODE_SUBPROCESS_ENV_SCRUB": "1",
        "ENABLE_CLAUDEAI_MCP_SERVERS": "false",
        "DISABLE_AUTOUPDATER": "1",
    }


# ---------- one call ----------

class Round:
    """State shared by every call in a round: the pinned binary and the allowed bundled skills."""

    def __init__(self, binary=None, version=None):
        # Tests pass a stub binary; a real round always pins the installed claude.
        self.binary, self.version = (binary, version) if binary else pin_binary()
        self.bundled_skills = None      # recorded by the no-plugin control call
        self.bundled_plugins = None


def parse_stream(stdout):
    init, result, events = None, None, []
    for line in stdout.splitlines():
        try:
            m = json.loads(line)
        except ValueError:
            continue
        events.append(m)
        if m.get("type") == "system" and m.get("subtype") == "init" and init is None:
            init = m
        if m.get("type") == "result":
            result = m
    return init, result, events


INIT_FIELDS = ("cwd", "model", "tools", "mcp_servers", "skills", "plugins", "agents",
               "memory_paths", "apiKeySource", "claude_code_version", "permissionMode")


def check_init(rnd, role, init, root, tools, cwd, plugin):
    """The per-role init assertion. Raises HarnessFailure on any mismatch."""
    if init is None:
        raise HarnessFailure(f"{role}: no init message")
    bad = []
    if real(init.get("cwd", "")) != real(cwd):
        bad.append(f"cwd {init.get('cwd')}")
    if init.get("claude_code_version") != rnd.version:
        bad.append(f"version {init.get('claude_code_version')} != {rnd.version}")
    if init.get("mcp_servers"):
        bad.append(f"mcp_servers {init.get('mcp_servers')}")
    if init.get("apiKeySource") not in ("none", None):
        bad.append(f"apiKeySource {init.get('apiKeySource')}")
    # The pinned CLI reports the subagent tool by its older name, Task, when --tools asks for Agent.
    alias = {"Task": "Agent"}
    if sorted(alias.get(t, t) for t in init.get("tools") or []) != sorted(tools):
        bad.append(f"tools {init.get('tools')} != {tools}")
    home = real(root / "home")
    for k, v in (init.get("memory_paths") or {}).items():
        if v and not real(v).startswith(home):
            bad.append(f"memory_paths.{k} outside run-root/home: {v}")
    # Plugins: the built-in plugins the no-plugin control recorded, plus the plugin under test.
    plugins = init.get("plugins") or []
    allowed_builtin = rnd.bundled_plugins
    for p in plugins:
        if p.get("path") == "builtin":
            if allowed_builtin is not None and p.get("source") not in allowed_builtin:
                bad.append(f"unexpected built-in plugin {p.get('source')}")
        elif not plugin or real(p.get("path", "")) != real(plugin):
            bad.append(f"plugin {p.get('name')} at {p.get('path')}")
    if plugin and not any(p.get("path") != "builtin" and real(p.get("path", "")) == real(plugin) for p in plugins):
        bad.append("plugin under test did not load")
    skills = init.get("skills") or []
    if rnd.bundled_skills is not None:
        # Skills the student built and installed in the workspace's own .claude/skills/ are allowed.
        own = {p.parent.name for p in (Path(cwd) / ".claude" / "skills").glob("*/SKILL.md")}
        extra = [s for s in skills if s not in rnd.bundled_skills and s not in own
                 and not (plugin and s.startswith("handsonai:"))]
        if extra:
            bad.append(f"unexpected skills {extra}")
    if bad:
        raise HarnessFailure(f"{role}: init assertion failed: " + "; ".join(bad))


def check_config_folder(root, plugin):
    cfg = root / "home" / ".claude"
    if (cfg / "plugins" / "synced").exists():
        raise HarnessFailure("account plugin sync ran in the test config folder (plugins/synced exists)")
    ip = cfg / "plugins" / "installed_plugins.json"
    if ip.exists():
        keys = list(json.loads(ip.read_text()).get("plugins", {}))
        if keys:
            raise HarnessFailure(f"plugins installed in the test config folder: {keys}")


def call(rnd, role, root, prompt, *, cwd, tools, plugin=None, resume=None, session_id=None,
         system_prompt=None, append_system_prompt=None, model=None, agent=None, log=None, retries=2):
    """One `claude -p` call. Returns (result_text, record). Raises HarnessFailure or UsageLimit."""
    args = [rnd.binary, "-p", "--setting-sources", "project,local", "--strict-mcp-config",
            "--output-format", "stream-json", "--verbose",
            "--model", model or {"skill": SKILL_MODEL, "student": STUDENT_MODEL}.get(role, GRADER_MODEL),
            "--settings", str(root / "settings-deny.json"),
            "--tools", ",".join(tools)]
    if tools:
        args += ["--allowedTools", ",".join(tools)]
    if plugin:
        args += ["--plugin-dir", str(plugin)]
    if agent:
        args += ["--agent", agent]
    if system_prompt:
        args += ["--system-prompt", system_prompt]
    if append_system_prompt:
        args += ["--append-system-prompt", append_system_prompt]
    if session_id:
        args += ["--session-id", session_id]
    if resume:
        args += ["--resume", resume]

    attempt = 0
    while True:
        attempt += 1
        try:
            r = subprocess.run(args, cwd=cwd, env=env_for(root), input=prompt,
                               capture_output=True, text=True, timeout=3600)
        except subprocess.TimeoutExpired:
            r = None
        raw = (r.stdout + "\n" + r.stderr) if r else ""
        if TOKEN_PREFIX in raw:
            raise HarnessFailure(f"{role}: token prefix appeared in raw output")
        init, result, events = parse_stream(r.stdout if r else "")
        text = (result or {}).get("result") or ""
        if result and result.get("is_error") and USAGE_LIMIT_RE.search(text):
            raise UsageLimit(text[:300])
        crashed = r is None or r.returncode != 0 or result is None
        if crashed and attempt <= retries and (r is None or TRANSIENT_RE.search(text + (r.stderr if r else ""))):
            time.sleep(20 * attempt)
            continue
        break
    if log is not None:
        with open(log, "a") as f:
            for e in events:
                f.write(json.dumps(e, ensure_ascii=False) + "\n")
    if crashed:
        err = text or (r.stderr[-1500:] if r else "timeout")
        raise HarnessFailure(f"{role}: call failed: {err}")
    # Only the first call of a session sends a fresh init worth checking? Every call has one; check all.
    check_init(rnd, role, init, root, tools, cwd, plugin)
    check_config_folder(root, plugin)
    record = {
        "role": role,
        "init": {k: init.get(k) for k in INIT_FIELDS},
        "model_used": list((result.get("modelUsage") or {}).keys()),
        "permission_denials": result.get("permission_denials") or [],
        "usage": result.get("usage"),
        "total_cost_usd": result.get("total_cost_usd"),
        "num_turns": result.get("num_turns"),
        "duration_ms": result.get("duration_ms"),
        "attempts": attempt,
    }
    return text.strip(), record


def auth_method(rnd, root):
    """`claude auth status --json`; keep only authMethod (email and organisation are never saved)."""
    r = subprocess.run([rnd.binary, "auth", "status", "--json"], cwd=root / "grader", env=env_for(root),
                       capture_output=True, text=True, timeout=120)
    if TOKEN_PREFIX in r.stdout + r.stderr:
        raise HarnessFailure("token prefix in auth status output")
    try:
        return json.loads(r.stdout).get("authMethod")
    except ValueError:
        return None


# ---------- fail-closed check on the real config (R12-3) ----------

def _hash_tree(p, skip=()):
    h = hashlib.sha256()
    if not p.exists():
        return "absent"
    if p.is_file():
        h.update(p.read_bytes())
        return h.hexdigest()
    for f in sorted(p.rglob("*")):
        rel = str(f.relative_to(p))
        if any(rel == s or rel.startswith(s + "/") for s in skip):
            continue
        if f.is_symlink():
            h.update(f"L {rel} {os.readlink(f)}\n".encode())
        elif f.is_file():
            h.update(f"F {rel}\n".encode())
            h.update(f.read_bytes())
        elif f.is_dir():
            h.update(f"D {rel}\n".encode())
    return h.hexdigest()


def _account_field(name):
    """Read at run time from ~/.claude.json; never written down."""
    try:
        return json.loads(REAL_CLAUDE_JSON.read_text()).get("oauthAccount", {}).get(name)
    except (OSError, ValueError):
        return None


def _synced_skills():
    """~/.claude/skills/synced/ is the account skill sync that James's own Claude Code sessions
    rewrite on their schedule (its manifest's lastUpdated and .last-complete-round change on
    every sync). Compare what it holds, not its timestamps: the synced folders and, per
    manifest, each skill's id, name, source and updatedAt."""
    root = REAL_CLAUDE / "skills" / "synced"
    if not root.exists():
        return "absent"
    out = {}
    for acct in sorted(p for p in root.iterdir() if p.is_dir()):
        m = acct / "manifest.json"
        try:
            skills = json.loads(m.read_text()).get("skills", []) if m.exists() else []
        except ValueError:
            skills = ["unreadable manifest"]
        out[acct.name] = {
            "folders": sorted(p.name for p in acct.iterdir() if p.is_dir()),
            "skills": sorted(json.dumps({k: x.get(k) for k in ("skillId", "name", "source", "updatedAt")},
                                        sort_keys=True) if isinstance(x, dict) else str(x) for x in skills),
        }
    return hashlib.sha256(json.dumps(out, sort_keys=True).encode()).hexdigest()


def real_config_snapshot():
    """Read-only. Raises HarnessFailure if ~/.claude.json can't be read (stop and ask James)."""
    try:
        cj = json.loads(REAL_CLAUDE_JSON.read_text())
    except (OSError, ValueError) as e:
        raise HarnessFailure(f"cannot read ~/.claude.json for the fail-closed check: {e}")
    ip = REAL_CLAUDE / "plugins" / "installed_plugins.json"
    plugins = json.loads(ip.read_text()).get("plugins", {}) if ip.exists() else {}
    return {
        "settings.json": _hash_tree(REAL_CLAUDE / "settings.json"),
        "skills/": _hash_tree(REAL_CLAUDE / "skills", skip=("synced",)),
        "skills/synced": _synced_skills(),
        "agents/": _hash_tree(REAL_CLAUDE / "agents"),
        "mcpServers": hashlib.sha256(json.dumps(cj.get("mcpServers"), sort_keys=True).encode()).hexdigest(),
        # profileFetchedAt is rewritten whenever any Claude Code session on this machine refetches the
        # profile (2026-10-16: the desktop app did, mid-round); every identity field is still compared.
        "oauthAccount": hashlib.sha256(json.dumps({k: v for k, v in (cj.get("oauthAccount") or {}).items()
                                                   if k != "profileFetchedAt"}, sort_keys=True).encode()).hexdigest(),
        "plugin_keys": sorted(plugins),
        "_projects": list(cj.get("projects", {})),
        "_install_paths": [e.get("installPath", "") for v in plugins.values() for e in v],
    }


def leak_signs():
    """Signs that an eval reached the real config: anything naming the eval parent folder."""
    forms = path_forms(eval_parent())
    dashes = {dashed(f) for f in forms}
    signs = []
    try:
        cj = json.loads(REAL_CLAUDE_JSON.read_text())
    except (OSError, ValueError) as e:
        raise HarnessFailure(f"cannot read ~/.claude.json: {e}")
    signs += [f"~/.claude.json projects: {k}" for k in cj.get("projects", {}) if any(k.startswith(f) for f in forms)]
    hist = REAL_CLAUDE / "history.jsonl"
    if hist.exists():
        with open(hist, errors="replace") as fh:
            for line in fh:
                if "handsonai-evals" not in line:
                    continue
                try:
                    proj = json.loads(line).get("project", "")
                except ValueError:
                    proj = line
                if any(proj.startswith(f) for f in forms):
                    signs.append("history.jsonl line under the eval parent folder")
    ip = REAL_CLAUDE / "plugins" / "installed_plugins.json"
    if ip.exists():
        for k, v in json.loads(ip.read_text()).get("plugins", {}).items():
            for e in v:
                if any(real(e.get("installPath", "")).startswith(f) for f in forms):
                    signs.append(f"installed_plugins.json {k} installPath under the eval parent folder")
    synced = REAL_CLAUDE / "skills" / "synced"
    if synced.exists():
        for f in synced.rglob("*"):
            if f.is_file() and f.stat().st_size < 5_000_000 and "handsonai-evals" in f.read_text(errors="replace"):
                signs.append(f"skills/synced file names the eval parent folder: {f.name}")
    projects = REAL_CLAUDE / "projects"
    if projects.exists():
        for p in projects.rglob("*"):
            n = str(p)
            if any(f in n for f in forms) or any(d in p.name for d in dashes):
                signs.append(f"~/.claude/projects entry {p.name}")
    return signs


def compare_snapshots(before, after):
    bad = []
    for k in ("settings.json", "skills/", "skills/synced", "agents/", "mcpServers", "oauthAccount"):
        if before[k] != after[k]:
            bad.append(f"{k} changed")
    new_plugins = sorted(set(after["plugin_keys"]) - set(before["plugin_keys"]))
    if new_plugins:
        bad.append(f"new plugins installed: {new_plugins}")
    return bad + leak_signs()


# ---------- leak scans before committing ----------

def commit_leak_scan(folder):
    """Grep results for the home path, the account email and ID, and the token prefix."""
    needles = {str(REAL_HOME): "home path", TOKEN_PREFIX: "token prefix"}
    for field, label in (("emailAddress", "account email"), ("accountUuid", "account ID")):
        v = _account_field(field)
        if v:
            needles[v] = label
    hits = []
    for f in Path(folder).rglob("*"):
        if f.is_file():
            try:
                s = f.read_text(errors="replace")
            except OSError:
                continue
            hits += [f"{f}: {label}" for n, label in needles.items() if n in s]
    return hits
