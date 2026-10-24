#!/usr/bin/env bash
# test-run.sh: the AI Workflow Framework's wrapper for headless Claude Code sessions.
#
# Canonical copy: scripts/framework/test-run.sh in the handsonai repo. The sync script
# copies it byte for byte into skills/build/scripts/ and skills/test/scripts/, and Build
# copies it byte for byte into the workspace at framework/.bin/test-run.sh. The model
# never writes or edits it. Rules 8.4, 8.5, 8.6, 8.7 and 8.11 of the framework spec.
#
# Every headless session (Build's checks, the bare run, Test's AI runs) starts here:
#
#   test-run.sh check|bare|test <workflow-slug> --plugin-copy <path> --prompt-file <file>
#               [--input <framework/<slug>/inputs/file>]
#   test-run.sh check|bare|test <workflow-slug> --plugin-copy <path> --prompt-file <file>
#               --resume <session-id> --run-folder <dir>
#
# The settings and the connection config are built from the build record's profile block
# and checked against the plan, never from anything the caller passes. The caller passes
# no Claude Code flags at all: any flag outside the grammar above is refused, and the
# bypass and permission-mode flags are refused by name.
#
# Helpers Build and Test use around the sessions (no session starts; nothing is written
# except where named):
#
#   block-rules     <slug> --plugin-copy <p>   the block's deny rules, read floor applied
#   lift-rules      <slug> --plugin-copy <p>   which of this workflow's rules may be removed
#   allow-rules     <slug> --plugin-copy <p> [--lift]   the wrapper's own allow and denies
#   settings-check  <slug> --plugin-copy <p>   read back the project settings and modes
#   practice-create <slug> --plugin-copy <p> --round <n>     makes the marked practice folder
#   practice-clear  <slug> --plugin-copy <p> --path <dir>    clears it, marked folders only
#   runs-clear      <slug> --plugin-copy <p> --path <dir>    clears one of the wrapper's run folders
#
# Exit codes: 0 done; 1 the session itself failed; 2 refused (a bypass or mode flag, or
# anything outside the grammar); 3 the start-up check failed; 4 the fingerprint doesn't
# match the record and the plugin's copy; 5 the record, plan or profile can't be used
# safely; 6 a prerequisite is missing (python3, claude); 7 a connection can't be passed
# without copying a secret. Every non-zero exit is fail closed: Build uses check agents
# only and skips the bare run; Test hands the inputs to the leader (N-T42).
#
# The binding fingerprint check is the skill's own, before each use (shasum against the
# record and the plugin's copy, claude-code-block.md). The self-check below catches drift
# (a stale copy, an edited record), not tampering: a tampered script could skip it.
#
# RELEASE CHECK markers below name the rules 13.2 row (platform registry `release_checks`
# id) each assumption rests on. Until a row passes on the running version, the skills
# take its fallback, so nothing here is relied on unverified.

set -euo pipefail

refuse() { printf 'test-run.sh: refused: %s\n' "$1" >&2; exit 2; }

# 1. Refuse bypass and permission-mode flags by name, anywhere in the arguments, before
#    anything else runs. Tokens are checked whole and inside values (a value smuggling a
#    flag is refused too).
for arg in ${1+"$@"}; do
  case "$arg" in
    *dangerously-skip-permissions*|*allow-dangerously*)
      refuse "--dangerously-skip-permissions is never passed to a framework session" ;;
    *--permission-mode*|*--permission-prompts*|*bypassPermissions*|*acceptEdits*)
      refuse "the permission mode is fixed by the profile; no permission-mode flag is accepted" ;;
  esac
done

# 2. Prerequisites. python3 does the JSON work; without it there is no start-up check.
PY="$(command -v python3 || true)"
if [ -z "$PY" ] || ! "$PY" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)' >/dev/null 2>&1; then
  printf 'test-run.sh: python3 (3.8 or later) is needed for the start-up check; failing closed.\n' >&2
  exit 6
fi

SELF_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
SELF="$SELF_DIR/$(basename "${BASH_SOURCE[0]}")"

exec "$PY" -I -S - "$SELF" ${1+"$@"} <<'PYTHON'
import datetime
import hashlib
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import tempfile

EXIT_SESSION, EXIT_REFUSED, EXIT_STARTUP, EXIT_FINGERPRINT = 1, 2, 3, 4
EXIT_RECORD, EXIT_PREREQ, EXIT_CONNECTION = 5, 6, 7

PROFILES = ("check", "bare", "test")
HELPERS = ("block-rules", "lift-rules", "allow-rules", "settings-check",
           "practice-create", "practice-clear", "runs-clear")
PRACTICE_MARKER = ".framework-practice"
RUN_MARKER = ".framework-run"
PROFILE_FENCE = "```framework-profile"
SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")
UUID_RE = re.compile(r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$")
TOOL_RE = re.compile(r"^mcp__[A-Za-z0-9_-]+__[A-Za-z0-9_-]+$")
NAME_RE = re.compile(r"^[A-Za-z0-9_-]{1,64}$")
ENV_RE = re.compile(r"^[A-Z_][A-Z0-9_]{0,63}$")
RELPATH_RE = re.compile(r"^[A-Za-z0-9._][A-Za-z0-9._/-]*$")
PROBE_PROMPT = "Reply with the single word READY. Use no tools."

# Built-in tools a profile can allow, and every other built-in denied by name. A tool the
# session lists that is on neither list fails the start-up check (rules 8.5).
# RELEASE CHECK 6: the built-in names and that `--tools` accepts them.
KNOWN_BUILTINS = [
    "Agent", "AskUserQuestion", "Bash", "BashOutput", "CronCreate", "CronDelete",
    "CronList", "Edit", "EnterPlanMode", "EnterWorktree", "ExitPlanMode", "ExitWorktree",
    "Glob", "Grep", "KillBash", "KillShell", "LSP", "ListMcpResourcesTool", "Monitor",
    "MultiEdit", "NotebookEdit", "NotebookRead", "PowerShell", "Read",
    "ReadMcpResourceTool", "SendUserMessage", "Skill", "SlashCommand", "Task",
    "TaskCreate", "TaskGet", "TaskList", "TaskOutput", "TaskStop", "TaskUpdate",
    "TodoWrite", "ToolSearch", "WebFetch", "WebSearch", "Write",
]

# Child environment: only these pass through, plus the env-var names the profile's
# connections name. Nothing else the caller set reaches the session.
ENV_PASS = ["HOME", "USER", "LOGNAME", "PATH", "SHELL", "TERM", "LANG", "LC_ALL",
            "LC_CTYPE", "TMPDIR", "CLAUDE_CONFIG_DIR", "HTTPS_PROXY", "HTTP_PROXY",
            "NO_PROXY", "https_proxy", "http_proxy", "no_proxy", "NODE_EXTRA_CA_CERTS",
            "SSL_CERT_FILE"]

# The read floor (rules 8.4). A tool is a read only when its name and description show
# it can't change anything. These only ever turn a declared read into a write.
WRITE_WORDS = {
    "add", "append", "apply", "approve", "archive", "assign", "attach", "book", "call",
    "cancel", "charge", "clear", "clone", "close", "comment", "commit", "complete",
    "copy", "create", "delete", "deploy", "detach", "disable", "draft", "duplicate",
    "edit", "enable", "execute", "exec", "forward", "generate", "grant", "import",
    "insert", "invite", "invoke", "kill", "label", "link", "mark", "merge", "modify",
    "move", "mutate", "mutation", "open", "overwrite", "patch", "pay", "pin", "post",
    "publish", "purge", "push", "put", "react", "refund", "reject", "remove", "rename",
    "reply", "replace", "reset", "resolve", "restart", "restore", "revoke", "run",
    "save", "schedule", "send", "set", "share", "start", "stop", "store", "submit",
    "subscribe", "sync", "terminate", "transfer", "trash", "trigger", "unlink",
    "unsubscribe", "update", "upload", "upsert", "write",
}
# A tool that can do both counts as a write, whatever the plan says.
MIXED_WORDS = {"fetch", "request", "manage", "http", "api", "graphql", "sql", "batch",
               "command", "raw", "proxy", "webhook", "admin"}
READ_WORDS = {"get", "list", "search", "read", "find", "lookup", "describe", "show",
              "view", "count", "query", "retrieve", "check", "inspect", "preview",
              "browse", "download", "info", "status", "summarize", "summary"}
DESC_WRITE_RE = re.compile(
    r"\b(creat(e|es|ed|ing)|updat(e|es|ed|ing)|delet(e|es|ed|ing)|remov(e|es|ed|ing)|"
    r"modif(y|ies|ied|ying)|writ(e|es|ing)|edit(s|ed|ing)?|send(s|ing)?|sent|"
    r"publish(es|ed|ing)?|upload(s|ed|ing)?|insert(s|ed|ing)?|upsert(s)?|patch(es|ed)?|"
    r"archiv(e|es|ed|ing)|trash(es|ed)?|mov(e|es|ed|ing)|renam(e|es|ed|ing)|"
    r"shar(e|es|ed|ing)|invit(e|es|ed|ing)|cancel(s|led|ling)?|execut(e|es|ed|ing)|"
    r"trigger(s|ed|ing)?|mutat(e|es|ion|ions)|overwrit(e|es|ing)|replac(e|es|ed|ing)|"
    r"puts?|post(s|ed|ing)? (a|an|the|to|message|messages|comment|comments)|"
    r"any http|arbitrary)\b",
    re.IGNORECASE)
NEGATION_RE = re.compile(r"(\bnot\b|\bnever\b|\bno\b|\bwithout\b|n't\b|\bcannot\b)", re.IGNORECASE)
# Commands never allowed by a profile, whatever the plan names (rules 8.4, 8.5).
COMMAND_FLOOR = {"rm", "rmdir", "mv", "cp", "dd", "tee", "chmod", "chown", "ln", "mkdir",
                 "touch", "truncate", "curl", "wget", "ssh", "scp", "rsync", "sudo", "su",
                 "kill", "pkill", "claude", "npm", "npx", "pip", "pip3", "python",
                 "python3", "node", "bash", "sh", "zsh", "eval", "exec", "xargs", "env",
                 "osascript", "open", "perl", "ruby", "sed", "awk", "find", "gh", "codex"}
GIT_READS = {"log", "status", "diff", "show", "rev-parse", "ls-files", "blame", "branch"}
# Secret shapes the kit refuses to pass on. The value is never printed.
SECRET_RES = [re.compile(p) for p in (
    r"sk-[A-Za-z0-9_-]{12,}", r"xox[abprs]-[A-Za-z0-9-]{8,}", r"gh[pousr]_[A-Za-z0-9]{20,}",
    r"github_pat_[A-Za-z0-9_]{20,}", r"AKIA[0-9A-Z]{16}", r"-----BEGIN [A-Z ]*PRIVATE KEY",
    r"(?i)bearer\s+(?!\$\{)[A-Za-z0-9._~+/=-]{8,}",
    r"(?i)(api[_-]?key|token|secret|password)\s*[=:]\s*['\"]?(?!\$\{)[A-Za-z0-9._~+/-]{12,}",
    # a long run of key-like characters, with a letter and a digit (paths and tool names
    # break on / . - and _, so they don't match)
    r"(?<![A-Za-z0-9+=])(?=[A-Za-z0-9+=]*[0-9])(?=[A-Za-z0-9+=]*[A-Za-z])[A-Za-z0-9+=]{32,}",
)]


def say(msg):
    sys.stderr.write("test-run.sh: " + msg + "\n")


def fail(code, msg):
    say(msg)
    sys.exit(code)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def real(path):
    return os.path.realpath(path)


def inside(path, root):
    path, root = real(path), real(root)
    return path == root or path.startswith(root.rstrip(os.sep) + os.sep)


def now_stamp():
    return datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")


# --------------------------------------------------------------------------- arguments

def parse_args(argv):
    if not argv:
        fail(EXIT_REFUSED, "refused: no command. Usage is in the script's header.")
    cmd = argv[0]
    if cmd not in PROFILES and cmd not in HELPERS:
        fail(EXIT_REFUSED, "refused: unknown command %r" % cmd)
    if len(argv) < 2 or not SLUG_RE.match(argv[1]):
        fail(EXIT_REFUSED, "refused: the second argument must be the workflow's slug")
    opts = {"cmd": cmd, "slug": argv[1]}
    allowed = {"--plugin-copy"}
    if cmd in PROFILES:
        allowed |= {"--prompt-file", "--input", "--resume", "--run-folder"}
    elif cmd == "allow-rules":
        allowed |= {"--lift"}
    elif cmd == "practice-create":
        allowed |= {"--round"}
    elif cmd in ("practice-clear", "runs-clear"):
        allowed |= {"--path"}
    i = 2
    while i < len(argv):
        a = argv[i]
        if a not in allowed:
            fail(EXIT_REFUSED, "refused: %r isn't accepted here; the profile sets every Claude Code flag" % a)
        if a in opts:
            fail(EXIT_REFUSED, "refused: %s given twice" % a)
        if a == "--lift":
            opts[a] = True
            i += 1
            continue
        if i + 1 >= len(argv) or argv[i + 1].startswith("-"):
            fail(EXIT_REFUSED, "refused: %s needs a value" % a)
        opts[a] = argv[i + 1]
        i += 2
    if "--plugin-copy" not in opts:
        fail(EXIT_REFUSED, "refused: --plugin-copy (the plugin's own test-run.sh) is required for the fingerprint check")
    if cmd in PROFILES:
        if "--prompt-file" not in opts:
            fail(EXIT_REFUSED, "refused: --prompt-file is required")
        if ("--resume" in opts) != ("--run-folder" in opts):
            fail(EXIT_REFUSED, "refused: a resume needs both --resume and --run-folder")
        if "--resume" in opts and not UUID_RE.match(opts["--resume"]):
            fail(EXIT_REFUSED, "refused: --resume takes a session id")
        if "--resume" in opts and "--input" in opts:
            fail(EXIT_REFUSED, "refused: a resume reuses its run folder; no new input")
    if cmd == "practice-create" and not re.match(r"^[1-9][0-9]{0,3}$", opts.get("--round", "")):
        fail(EXIT_REFUSED, "refused: --round takes the round's number")
    if cmd in ("practice-clear", "runs-clear") and "--path" not in opts:
        fail(EXIT_REFUSED, "refused: --path is required")
    return opts


# --------------------------------------------------------------------------- the record

def frontmatter(text):
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return lines[1:i]
    return None


def unquote(s):
    s = s.strip()
    if len(s) >= 2 and s[0] == s[-1] and s[0] in "\"'":
        return s[1:-1]
    return s


def block_lines(fm, key):
    """The value of a top-level key: (inline text, [indented child lines])."""
    for i, line in enumerate(fm):
        m = re.match(r"^%s:\s*(.*?)\s*(#.*)?$" % re.escape(key), line)
        if m:
            children = []
            for nxt in fm[i + 1:]:
                if nxt.strip() == "" or nxt.startswith((" ", "\t")):
                    children.append(nxt)
                else:
                    break
            return m.group(1), children
    return None, None


def parse_list(children, key):
    """A list under `  key:` (block style or flow style). None when unparseable."""
    out, found, collecting = [], False, False
    for line in children:
        if not line.strip() or line.strip().startswith("#"):
            continue
        m = re.match(r"^  (\w+):\s*(.*?)\s*$", line)
        if m:
            collecting = False
            if m.group(1) == key:
                found = True
                rest = m.group(2)
                if rest.startswith("["):
                    if not rest.endswith("]"):
                        return None
                    inner = rest[1:-1].strip()
                    out = [unquote(x) for x in inner.split(",") if x.strip()] if inner else []
                elif rest in ("", "[]"):
                    collecting = rest == ""
                else:
                    return None
            continue
        m = re.match(r"^    - (.+?)\s*$", line)
        if m and collecting:
            out.append(unquote(m.group(1)))
            continue
        if collecting:
            return None
    return out if found else []


def write_block_of(text):
    """{'state': 'on'|'off', 'on': [...], 'leader_rules': [...], 'leader_allow': [...]},
    or None when the record's write_block can't be read (callers fail closed)."""
    fm = frontmatter(text)
    if fm is None:
        return None
    inline, children = block_lines(fm, "write_block")
    if inline is None:
        return {"state": "off", "on": [], "leader_rules": [], "leader_allow": []}
    inline = unquote(inline)
    if inline == "off":
        return {"state": "off", "on": [], "leader_rules": [], "leader_allow": []}
    if inline != "":
        return None
    result = {"state": "on"}
    for key in ("on", "leader_rules", "leader_allow"):
        val = parse_list(children, key)
        if val is None:
            return None
        result[key] = val
    if not any(re.match(r"^  on:", c) for c in children):
        return None
    return result


def wrapper_fingerprint(text):
    fm = frontmatter(text)
    if fm is None:
        return None
    _, children = block_lines(fm, "fingerprints")
    if children is None:
        return None
    found = []
    for line in children:
        m = re.match(r"^\s+[\"']?(wrapper|framework/\.bin/test-run\.sh)[\"']?:\s*[\"']?(sha256:)?([0-9a-f]{64})[\"']?\s*$", line)
        if m:
            found.append(m.group(3))
    return found[0] if len(found) == 1 else None


def scan_secrets(text):
    for rx in SECRET_RES:
        for m in rx.finditer(text):
            if re.fullmatch(r"[0-9a-f]{64}", m.group(0)):
                continue  # a sha256 fingerprint, not a secret
            return True
    return False


def parse_profile(record_text, slug):
    blocks = record_text.split(PROFILE_FENCE)
    if len(blocks) != 2:
        fail(EXIT_RECORD, "the build record needs exactly one ```framework-profile block (claude-code-block.md)")
    body = blocks[1].split("```", 1)
    if len(body) != 2:
        fail(EXIT_RECORD, "the profile block isn't closed")
    body = body[0]
    if scan_secrets(body):
        fail(EXIT_RECORD, "the profile block seems to hold a secret's value; it is never passed on or repeated. "
             "Name an environment variable instead, and tell the leader to change that secret (N-F14).")
    prof = {"version": None, "workflow": None, "connections": {}, "tools": [], "skills": [],
            "agents": [], "context": [], "commands": [], "deny_commands": [], "webfetch": [],
            "headless_writes": "none"}
    for n, raw in enumerate(body.splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        head, _, rest = line.partition(" ")
        rest = rest.strip()
        bad = lambda why: fail(EXIT_RECORD, "profile line %d: %s" % (n, why))
        if head == "version":
            if rest != "1":
                bad("only version 1 is understood")
            prof["version"] = 1
        elif head == "workflow":
            prof["workflow"] = rest
        elif head == "connection":
            parts = rest.split()
            if len(parts) < 2 or not NAME_RE.match(parts[0]):
                bad("connection <name> stdio|http|sse|claude-ai ...")
            name, kind = parts[0], parts[1]
            if name in prof["connections"]:
                bad("connection %s listed twice" % name)
            conn = {"name": name, "kind": kind, "env": [], "headers": []}
            if kind == "stdio":
                if len(parts) < 3:
                    bad("a stdio connection names its command")
                for tok in parts[2:]:
                    if not re.match(r"^[A-Za-z0-9@._/:=+,-]+$", tok):
                        bad("a command argument holds a character the profile doesn't allow")
                conn["command"], conn["args"] = parts[2], parts[3:]
            elif kind in ("http", "sse"):
                if len(parts) != 3 or not re.match(r"^(https://[A-Za-z0-9.-]+(:[0-9]+)?(/[A-Za-z0-9._~/%-]*)?|http://(localhost|127\.0\.0\.1)(:[0-9]+)?(/[A-Za-z0-9._~/%-]*)?)$", parts[2]):
                    bad("an http or sse connection names one https URL with no query string")
                conn["url"] = parts[2]
            elif kind == "claude-ai":
                if len(parts) != 2:
                    bad("a claude-ai connection takes no other value")
            else:
                bad("unknown connection kind %r" % kind)
            prof["connections"][name] = conn
        elif head == "connection_env":
            parts = rest.split()
            if len(parts) != 2 or parts[0] not in prof["connections"] or not ENV_RE.match(parts[1]):
                bad("connection_env <connection> <ENV_VAR_NAME> (a name, never a value)")
            prof["connections"][parts[0]]["env"].append(parts[1])
        elif head == "connection_header":
            parts = rest.split(None, 2)
            if len(parts) != 3 or parts[0] not in prof["connections"] or not re.match(r"^[A-Za-z0-9-]{1,64}$", parts[1]):
                bad("connection_header <connection> <Header-Name> <value naming ${ENV_VAR}>")
            if not re.match(r"^((Bearer|Basic|Token) )?\$\{[A-Z_][A-Z0-9_]*\}$", parts[2]):
                bad("a header value must name an environment variable as ${NAME}, never hold a value")
            prof["connections"][parts[0]]["headers"].append((parts[1], parts[2]))
        elif head == "tool":
            spec, _, desc = rest.partition("|")
            parts = spec.split()
            if len(parts) != 3 or parts[0] not in prof["connections"] or parts[1] not in ("read", "write") or not TOOL_RE.match(parts[2]):
                bad("tool <connection> read|write <mcp__server__tool> | <description from the live tool list>")
            prof["tools"].append({"connection": parts[0], "declared": parts[1], "name": parts[2], "desc": desc.strip()})
        elif head in ("skill", "agent", "context"):
            if not RELPATH_RE.match(rest) or ".." in rest.split("/"):
                bad("%s takes a path relative to the workspace" % head)
            prof[{"skill": "skills", "agent": "agents", "context": "context"}[head]].append(rest.rstrip("/"))
        elif head in ("command", "deny_command"):
            if not re.match(r"^[A-Za-z0-9._/-]+( [A-Za-z0-9._/=:*-]+)*$", rest):
                bad("%s takes plain words, no shell characters" % head)
            prof["commands" if head == "command" else "deny_commands"].append(rest)
        elif head == "webfetch":
            if not re.match(r"^[a-z0-9.-]+\.[a-z]{2,}$", rest):
                bad("webfetch takes one domain")
            prof["webfetch"].append(rest)
        elif head == "headless_writes":
            # RELEASE CHECK 3: `practice` only once a headless session's writes are shown to
            # stay inside its own practice/; until then Build records `none` (the default).
            if rest not in ("practice", "none"):
                bad("headless_writes is practice or none")
            prof["headless_writes"] = rest
        else:
            bad("unknown directive %r" % head)
    if prof["version"] != 1:
        fail(EXIT_RECORD, "the profile block needs `version 1`")
    if prof["workflow"] != slug:
        fail(EXIT_RECORD, "the profile block belongs to %r, not %r" % (prof["workflow"], slug))
    for t in prof["tools"]:
        conn = prof["connections"][t["connection"]]
        if conn["kind"] != "claude-ai" and not t["name"].startswith("mcp__%s__" % conn["name"]):
            fail(EXIT_RECORD, "tool %s doesn't belong to connection %s" % (t["name"], conn["name"]))
    return prof


# --------------------------------------------------------------------------- read floor

def name_tokens(tool_name):
    short = tool_name.split("__", 2)[-1]
    short = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", short)
    return [t for t in re.split(r"[_\-]+", short.lower()) if t]


def classify(tool):
    """('read'|'write', reason). Only ever moves a declared read to a write."""
    if tool["declared"] == "write":
        return "write", "declared a write"
    toks = name_tokens(tool["name"])
    hit = [t for t in toks if t in WRITE_WORDS]
    if hit:
        return "write", "its name says it can change something (%s)" % hit[0]
    mixed = [t for t in toks if t in MIXED_WORDS]
    if mixed:
        return "write", "it can both read and change (%s): a mixed tool counts as a write" % mixed[0]
    if not any(t in READ_WORDS for t in toks):
        return "write", "its name doesn't show it only reads"
    desc = tool["desc"]
    if not desc:
        return "write", "no description from the live tool list shows it only reads"
    for m in DESC_WRITE_RE.finditer(desc):
        before = desc[max(0, m.start() - 40):m.start()]
        if not NEGATION_RE.search(" ".join(before.split()[-3:])):
            return "write", "its description says it can change something (%s)" % m.group(0).strip()
    return "read", "name and description show it only reads"


def classified(prof):
    reads, writes, demoted = [], [], []
    for t in prof["tools"]:
        cls, why = classify(t)
        if cls == "read":
            reads.append(t["name"])
        else:
            writes.append(t["name"])
            if t["declared"] == "read":
                demoted.append({"tool": t["name"], "why": why})
    overlap = set(reads) & set(writes)
    if overlap:
        fail(EXIT_RECORD, "tool listed as both a read and a write: %s" % sorted(overlap)[0])
    return sorted(set(reads)), sorted(set(writes)), demoted


def bash_rules(prefix):
    return ["Bash(%s:*)" % prefix, "Bash(%s *)" % prefix]


# --------------------------------------------------------------------------- locations

class Place(object):
    pass


def locate(self_path, slug):
    p = Place()
    p.self = self_path
    p.bin = os.path.dirname(self_path)
    if os.path.basename(p.bin) != ".bin" or os.path.basename(os.path.dirname(p.bin)) != "framework":
        fail(EXIT_FINGERPRINT, "the wrapper runs only from framework/.bin/test-run.sh in the workspace")
    p.framework = os.path.dirname(p.bin)
    p.workspace = os.path.dirname(p.framework)
    p.wf = os.path.join(p.framework, slug)
    p.record = os.path.join(p.wf, "build-record.md")
    p.plan = os.path.join(p.wf, "design-plan.md")
    p.slug = slug
    if not os.path.isfile(p.record):
        fail(EXIT_RECORD, "no build record at framework/%s/build-record.md" % slug)
    return p


def check_fingerprint(place, plugin_copy):
    """Rules 8.7: this file must match the record's fingerprint and the plugin's own copy."""
    mine = sha256_file(place.self)
    with open(place.record, encoding="utf-8") as f:
        recorded = wrapper_fingerprint(f.read())
    if not os.path.isfile(plugin_copy):
        fail(EXIT_FINGERPRINT, "fingerprint check failed closed: the plugin's copy isn't at the path given")
    if inside(plugin_copy, place.workspace):
        fail(EXIT_FINGERPRINT, "fingerprint check failed closed: the plugin's copy must be the installed plugin's, outside the workspace")
    theirs = sha256_file(plugin_copy)
    problems = []
    if recorded is None:
        problems.append("the build record has no single wrapper fingerprint")
    elif recorded != mine:
        problems.append("it doesn't match the build record's fingerprint")
    if theirs != mine:
        problems.append("it doesn't match the plugin's own copy")
    if problems:
        fail(EXIT_FINGERPRINT, "fingerprint check failed closed: " + "; ".join(problems) +
             ". Build: check agents only, and no bare run. Test: the leader runs the inputs (N-T42).")
    return mine


def runs_root(slug):
    base = os.environ.get("TMPDIR") or "/tmp"
    root = os.path.join(real(base), "handsonai-framework-runs", slug)
    return root


def outside_repository(path, workspace):
    if inside(path, workspace):
        return False
    cur = real(path)
    while True:
        if os.path.exists(os.path.join(cur, ".git")):
            return False
        parent = os.path.dirname(cur)
        if parent == cur:
            return True
        cur = parent


def read_text(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def all_records(place):
    out = {}
    for name in sorted(os.listdir(place.framework)):
        rec = os.path.join(place.framework, name, "build-record.md")
        if SLUG_RE.match(name) and os.path.isfile(rec):
            out[name] = read_text(rec)
    return out


def load_json(path):
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def settings_paths(place):
    cfg = os.environ.get("CLAUDE_CONFIG_DIR") or os.path.join(os.environ.get("HOME", "~"), ".claude")
    return {
        "local": os.path.join(place.workspace, ".claude", "settings.local.json"),
        "project": os.path.join(place.workspace, ".claude", "settings.json"),
        "user": os.path.join(cfg, "settings.json"),
    }


def perms(settings, key):
    v = (settings.get("permissions") or {}).get(key) or []
    return [x for x in v if isinstance(x, str)]


# --------------------------------------------------------------------------- helpers

def cmd_block_rules(place, prof):
    reads, writes, demoted = classified(prof)
    deny = ["%s" % w for w in writes] + bash_rules("claude")
    records = all_records(place)
    others = {}
    for slug, text in records.items():
        if slug == place.slug:
            continue
        wb = write_block_of(text)
        if wb is None:
            fail(EXIT_RECORD, "framework/%s/build-record.md: its write_block can't be read; failing closed" % slug)
        if wb["state"] == "on":
            for r in wb["on"]:
                others.setdefault(r, []).append(slug)
    own_wb = write_block_of(records[place.slug])
    if own_wb is None:
        fail(EXIT_RECORD, "this workflow's write_block can't be read; failing closed")
    local = load_json(settings_paths(place)["local"])
    present_deny = set(perms(local, "deny"))
    leader_rules = sorted(r for r in present_deny if r in deny and r not in others
                          and r not in own_wb.get("on", []))
    if own_wb["state"] == "on":
        leader_rules = sorted(set(leader_rules) | set(own_wb.get("leader_rules", [])))
    out = {
        "workflow": place.slug,
        "deny": deny,
        "add": [r for r in deny if r not in present_deny],
        "shared_with": {r: others[r] for r in deny if r in others},
        "leader_rules": leader_rules,
        "leader_allow": sorted(set(perms(local, "allow")) - set(allow_rule_set(place)["allow"])),
        "check_agent_tools": reads,
        "reads": reads,
        "writes": writes,
        "demoted_to_write": demoted,
        "record_write_block": {"on": [r for r in deny if r not in leader_rules],
                               "leader_rules": leader_rules},
    }
    print(json.dumps(out, indent=2))


def cmd_lift_rules(place):
    records = all_records(place)
    own = write_block_of(records[place.slug])
    if own is None:
        fail(EXIT_RECORD, "this workflow's write_block can't be read; nothing lifted (failing closed)")
    shared, leader = {}, set()
    for slug, text in records.items():
        wb = write_block_of(text)
        if wb is None:
            fail(EXIT_RECORD, "framework/%s/build-record.md: its write_block can't be read; nothing lifted (failing closed)" % slug)
        leader |= set(wb.get("leader_rules", []))
        if slug != place.slug and wb["state"] == "on":
            for r in wb["on"]:
                shared.setdefault(r, []).append(slug)
    remove, kept_shared, kept_leader = [], {}, []
    for r in own.get("on", []):
        if r in leader:
            kept_leader.append(r)
        elif r in shared:
            kept_shared[r] = shared[r]
        else:
            remove.append(r)
    print(json.dumps({"workflow": place.slug, "state": own["state"], "remove": remove,
                      "kept_shared": kept_shared, "kept_leader": kept_leader}, indent=2))


def allow_rule_set(place):
    bin_abs = "/" + place.bin.lstrip("/")  # `//abs/path` form: absolute in permission rules
    return {
        "allow": ["Bash(framework/.bin/test-run.sh *)", "Bash(./framework/.bin/test-run.sh *)",
                  "Bash(framework/.bin/test-run.sh:*)", "Bash(./framework/.bin/test-run.sh:*)"],
        # RELEASE CHECK 6: path forms. `//abs` is absolute; `./` is from the session's folder.
        "deny": ["Write(/%s/**)" % bin_abs, "Edit(/%s/**)" % bin_abs,
                 "Write(./framework/.bin/**)", "Edit(./framework/.bin/**)"],
    }


def results_frontmatter(place, slug):
    path = os.path.join(place.framework, slug, "test-results.md")
    if not os.path.isfile(path):
        return {}
    fm = frontmatter(read_text(path)) or []
    out = {}
    for line in fm:
        m = re.match(r"^(go_live|round_status):\s*(\S+)", line)
        if m:
            out[m.group(1)] = unquote(m.group(2))
    return out


def cmd_allow_rules(place, lift):
    rules = allow_rule_set(place)
    out = {"workflow": place.slug, "allow": rules["allow"], "deny": rules["deny"]}
    if lift:
        needed_by = []
        for slug in all_records(place):
            if slug == place.slug:
                continue
            fm = results_frontmatter(place, slug)
            if fm.get("go_live") != "done" or fm.get("round_status") == "in-progress":
                needed_by.append(slug)
        out["remove"] = [] if needed_by else rules["allow"] + rules["deny"]
        out["kept_for"] = needed_by
    print(json.dumps(out, indent=2))


def cmd_settings_check(place, prof):
    paths = settings_paths(place)
    loaded = {}
    for k, p in paths.items():
        try:
            loaded[k] = load_json(p)
        except ValueError:
            fail(EXIT_RECORD, "%s settings can't be read as JSON; failing closed" % k)
    local = loaded["local"]
    deny, allow = set(perms(local, "deny")), set(perms(local, "allow"))
    wb = write_block_of(read_text(place.record))
    if wb is None:
        fail(EXIT_RECORD, "this workflow's write_block can't be read; failing closed")
    reads, writes, _ = classified(prof)
    missing = [r for r in wb.get("on", []) if r not in deny] if wb["state"] == "on" else []
    wrapper = allow_rule_set(place)
    allowed_writes = sorted(r for r in allow if any(r == w or r.startswith(w + "(") for w in writes))
    out = {
        "workflow": place.slug,
        "write_block": wb["state"],
        "block_rules_missing": missing,
        "bash_claude_denied": all(r in deny for r in bash_rules("claude")),
        "wrapper_allowed": any(r in allow for r in wrapper["allow"]),
        "wrapper_folder_protected": all(r in deny for r in wrapper["deny"][:2]),
        "allow_rules_added_since_block": sorted(allow - set(wb.get("leader_allow", [])) - set(wrapper["allow"])),
        "allow_rules_on_write_tools": allowed_writes,
        # Build's own session: the mode its settings start it in. The mode the session is in
        # now (a flag at launch, or switched during the session) is read from the session
        # itself, as claude-code-block.md says. RELEASE CHECK 4.
        "default_modes": {k: (v.get("permissions") or {}).get("defaultMode") for k, v in loaded.items()},
    }
    out["ok"] = (not missing) and (wb["state"] != "on" or out["bash_claude_denied"])
    print(json.dumps(out, indent=2))


def practice_target(place):
    """practice/, or practice-<slug>/ where practice/ isn't ours or the workspace is shared."""
    workflows = [n for n in os.listdir(place.framework)
                 if SLUG_RE.match(n) and os.path.isfile(os.path.join(place.framework, n, "design-plan.md"))]
    plain = os.path.join(place.workspace, "practice")
    own = os.path.join(place.workspace, "practice-" + place.slug)
    if len(workflows) > 1:
        return own
    if os.path.lexists(plain):
        mk = read_marker(plain)
        # practice/ marked as this workflow's: left from an earlier round (create refuses
        # until it's cleared). Unmarked, or another workflow's: practice-<slug>/ instead.
        return plain if mk is not None and mk.get("workflow") == place.slug else own
    return plain


def read_marker(folder):
    path = os.path.join(folder, PRACTICE_MARKER)
    if os.path.islink(folder) or not os.path.isdir(folder) or not os.path.isfile(path) or os.path.islink(path):
        return None
    out = {}
    for line in read_text(path).splitlines():
        k, _, v = line.partition(" ")
        out[k] = v.strip()
    return out


def cmd_practice_create(place, rnd):
    target = practice_target(place)
    if os.path.lexists(target):
        mk = read_marker(target)
        if mk is None:
            fail(EXIT_RECORD, "%s exists without the framework's marker; it is never used or cleared. "
                 "Ask the leader to rename it, then try again." % os.path.relpath(target, place.workspace))
        fail(EXIT_RECORD, "%s is still there from round %s; clear it with practice-clear first, at the path that round recorded"
             % (os.path.relpath(target, place.workspace), mk.get("round", "?")))
    os.makedirs(target)
    with open(os.path.join(target, PRACTICE_MARKER), "w", encoding="utf-8") as f:
        f.write("workflow %s\nround %s\ncreated %s\n" % (place.slug, rnd, now_stamp()))
    print(json.dumps({"practice_folder": os.path.relpath(target, place.workspace) + "/",
                      "marker": PRACTICE_MARKER}, indent=2))


def cmd_practice_clear(place, path):
    full = path if os.path.isabs(path) else os.path.join(place.workspace, path)
    full = os.path.normpath(full)
    allowed = {os.path.join(place.workspace, "practice"), os.path.join(place.workspace, "practice-" + place.slug)}
    if full not in allowed:
        fail(EXIT_RECORD, "refused to clear %r: only practice/ or practice-%s/ in the workspace" % (path, place.slug))
    mk = read_marker(full)
    if mk is None:
        fail(EXIT_RECORD, "refused to clear %r: no framework marker, so it isn't the framework's. Never cleared." % path)
    if mk.get("workflow") != place.slug:
        fail(EXIT_RECORD, "refused to clear %r: its marker belongs to %r" % (path, mk.get("workflow")))
    shutil.rmtree(full)
    print(json.dumps({"cleared": os.path.relpath(full, place.workspace) + "/"}, indent=2))


def run_marker(folder):
    path = os.path.join(folder, RUN_MARKER)
    if os.path.islink(folder) or not os.path.isfile(path) or os.path.islink(path):
        return None
    try:
        return json.loads(read_text(path))
    except ValueError:
        return None


def cmd_runs_clear(place, path):
    full = real(path)
    root = runs_root(place.slug)
    mk = run_marker(full)
    if not inside(full, root) or full == real(root) or mk is None or mk.get("workflow") != place.slug:
        fail(EXIT_RECORD, "refused to clear %r: not one of this workflow's run folders (no marker)" % path)
    cfg = mk.get("config_dir")
    shutil.rmtree(full)
    if cfg and inside(cfg, root) and os.path.isdir(cfg):
        shutil.rmtree(cfg)
    print(json.dumps({"cleared": full}, indent=2))


# --------------------------------------------------------------------------- sessions

def plan_cross_check(place, prof):
    if not os.path.isfile(place.plan):
        fail(EXIT_RECORD, "no plan at framework/%s/design-plan.md" % place.slug)
    plan = read_text(place.plan).lower()
    for name in prof["connections"]:
        if name.lower() not in plan and name.lower().replace("_", " ") not in plan:
            fail(EXIT_RECORD, "connection %r isn't in the plan; a profile carries only the plan's connections" % name)
    for c in prof["commands"] + prof["webfetch"]:
        if c.lower() not in plan:
            fail(EXIT_RECORD, "%r isn't named in the plan; Bash and WebFetch stay denied unless the plan names them" % c)


def floor_commands(prof):
    for c in prof["commands"]:
        words = c.split()
        if words[0] in COMMAND_FLOOR:
            fail(EXIT_RECORD, "command %r can change things; only read-only commands are allowed" % c)
        if words[0] == "git" and (len(words) < 2 or words[1] not in GIT_READS):
            fail(EXIT_RECORD, "command %r: only git's read commands are allowed" % c)


def served_by(tool, connections):
    return any(tool.startswith("mcp__%s__" % c) for c in connections)


def build_session_config(place, prof, profile, run_folder):
    """Settings and connection config for one session, from the record only."""
    reads, writes, _ = classified(prof)
    floor_commands(prof)
    connections = {} if profile == "bare" else prof["connections"]
    for c in connections.values():
        if c["kind"] == "claude-ai":
            # RELEASE CHECK 6: whether --strict-mcp-config can carry a claude.ai connector
            # through its stored sign-in. Until then it can't be passed: fail closed.
            fail(EXIT_CONNECTION, "connection %r is a claude.ai connector, which can't be passed to a headless "
                 "session yet; the leader runs the inputs that need it" % c["name"])
    builtin_allow = {"Read", "Glob", "Grep"}
    allow, deny = [], []
    run_abs = "/" + real(run_folder).lstrip("/")
    allow += ["Read(./**)", "Read(/%s/**)" % run_abs, "Glob", "Grep"]
    if profile in ("check", "test"):
        builtin_allow.add("Skill")
        allow.append("Skill")
        if prof["agents"]:
            builtin_allow |= {"Agent", "Task"}
            allow += ["Agent", "Task"]
        if connections:
            builtin_allow.add("ToolSearch")
            allow.append("ToolSearch")
        allow += [r for r in reads if served_by(r, connections)]
        if prof["headless_writes"] == "practice":
            builtin_allow |= {"Write", "Edit"}
            allow += ["Write(./practice/**)", "Edit(./practice/**)",
                      "Write(/%s/practice/**)" % run_abs, "Edit(/%s/practice/**)" % run_abs]
    if profile == "test" and prof["commands"]:
        builtin_allow.add("Bash")
        for c in prof["commands"]:
            allow += bash_rules(c)
    if profile == "test" and prof["webfetch"]:
        builtin_allow.add("WebFetch")
        allow += ["WebFetch(domain:%s)" % d for d in prof["webfetch"]]
    deny += [w for w in writes]
    deny += bash_rules("claude")
    for c in prof["deny_commands"]:
        deny += bash_rules(c)
    for b in KNOWN_BUILTINS:
        if b not in builtin_allow:
            deny.append(b)
    ws_abs = "/" + real(place.workspace).lstrip("/")
    cfg_home = os.environ.get("CLAUDE_CONFIG_DIR") or os.path.join(os.environ.get("HOME", "/nonexistent"), ".claude")
    deny += ["Read(/%s/**)" % ws_abs, "Read(/%s/**)" % ("/" + real(cfg_home).lstrip("/")),
             "Write(./.claude/**)", "Edit(./.claude/**)"]
    settings = {
        "permissions": {"allow": allow, "deny": deny, "defaultMode": "dontAsk"},
        "disableAllHooks": True,
    }
    servers, env_names = {}, []
    for c in connections.values():
        if c["kind"] == "stdio":
            s = {"type": "stdio", "command": c["command"], "args": c["args"]}
            if c["env"]:
                s["env"] = {n: "${%s}" % n for n in c["env"]}
        else:
            s = {"type": c["kind"], "url": c["url"]}
            if c["headers"]:
                s["headers"] = {h: v for h, v in c["headers"]}
        env_names += c["env"] + re.findall(r"\$\{([A-Z_][A-Z0-9_]*)\}", " ".join(v for _, v in c["headers"]))
        servers[c["name"]] = s
    mcp = {"mcpServers": servers}
    # RELEASE CHECK 6: the sub-agent tool's built-in name (Agent in current versions; Task
    # before). Both are allowed by rule; --tools names only Agent, so a version that still
    # calls it Task runs with no sub-agents (a functional failure, never a safety one).
    builtins = sorted(builtin_allow - {"Task"})
    expected = {
        "allowed": set(builtins) | set(r for r in reads if served_by(r, connections)),
        "denied": set(d for d in deny if "(" not in d),
        "servers": set(connections),
        "skills": [os.path.basename(s) for s in prof["skills"]] if profile != "bare" else [],
        "agents": [os.path.splitext(os.path.basename(a))[0] for a in prof["agents"]] if profile != "bare" else [],
        "run_folder": real(run_folder),
        "writes": set(writes),
    }
    return settings, mcp, builtins, env_names, expected


def verify_written(settings_path, settings, expected):
    """The settings read back from disk, checked before the session starts (rules 8.5)."""
    back = load_json(settings_path)
    if back != settings:
        fail(EXIT_STARTUP, "start-up check failed: the settings read back differ from what the profile built")
    p = back["permissions"]
    if p.get("defaultMode") != "dontAsk":
        fail(EXIT_STARTUP, "start-up check failed: the settings' permission mode isn't the profile's")
    for rule in p["allow"]:
        base = rule.split("(", 1)[0]
        if base in expected["writes"] or rule in expected["writes"]:
            fail(EXIT_STARTUP, "start-up check failed: a write tool is on the allow list")
        if base in ("Write", "Edit") and "/practice/**" not in rule:
            fail(EXIT_STARTUP, "start-up check failed: Write or Edit allowed outside practice/")
    for w in expected["writes"]:
        if w not in p["deny"]:
            fail(EXIT_STARTUP, "start-up check failed: a write tool isn't denied")


def child_env(env_names):
    env = {k: os.environ[k] for k in ENV_PASS if k in os.environ}
    for n in env_names:
        if n in os.environ:
            env[n] = os.environ[n]  # passed by name; the value is never written or printed
    return env


def is_hook_event(msg):
    t, st = str(msg.get("type", "")), str(msg.get("subtype", ""))
    return "hook" in t.lower() or "hook" in st.lower()


def check_init(init, expected):
    """The start-up check (rules 8.5, 8.7). Returns a list of problems; empty means pass.
    RELEASE CHECK 6: the init message's field names (tools, mcp_servers, permissionMode,
    cwd, plugins, skills, slash_commands, agents)."""
    problems = []
    if init.get("permissionMode") != "dontAsk":
        problems.append("the session's permission mode is %r, not the profile's" % init.get("permissionMode"))
    cwd = init.get("cwd")
    if not cwd or real(cwd) != expected["run_folder"]:
        problems.append("the session isn't running in its own run folder")
    tools = init.get("tools")
    if not isinstance(tools, list):
        problems.append("the session's start-up tool list can't be read")
        tools = []
    for t in tools:
        if t in expected["allowed"] or t in expected["denied"]:
            continue
        problems.append("tool %r is neither on the allow list nor denied" % t)
    servers = init.get("mcp_servers")
    if not isinstance(servers, list):
        problems.append("the session's connections can't be read")
        servers = []
    names = set()
    for s in servers:
        name = s.get("name") if isinstance(s, dict) else None
        names.add(name)
        if name not in expected["servers"]:
            problems.append("connection %r loaded, which the profile doesn't hold" % name)
        elif s.get("status") != "connected":
            problems.append("connection %r didn't connect" % name)
    for missing in sorted(expected["servers"] - names):
        problems.append("connection %r didn't load" % missing)
    plugins = init.get("plugins")
    if plugins:
        problems.append("a plugin loaded (%s); no plugin may load in a framework session" %
                        ", ".join(str(p.get("name", p) if isinstance(p, dict) else p) for p in plugins))
    if expected["skills"]:
        listed = init.get("skills")
        if not isinstance(listed, list):
            listed = init.get("slash_commands")
        if not isinstance(listed, list):
            problems.append("the session's skills can't be read")
        else:
            have = set(str(x).lstrip("/").split(":")[-1] for x in listed)
            for s in expected["skills"]:
                if s not in have:
                    problems.append("the workflow's skill %r didn't load" % s)
    if expected["agents"]:
        listed = init.get("agents")
        if not isinstance(listed, list):
            problems.append("the session's agents can't be read")
        else:
            have = set(str(x.get("name", "") if isinstance(x, dict) else x) for x in listed)
            for a in expected["agents"]:
                if a not in have:
                    problems.append("the workflow's agent %r didn't load" % a)
    return problems


def run_claude(cmd, cwd, env, prompt, log_path, expected):
    """Starts claude, checks the start-up message before anything else, and kills the
    session (its whole process group) the moment a check fails or a hook runs."""
    err_path = log_path + ".stderr"
    with open(log_path, "ab") as log, open(err_path, "ab") as err:
        proc = subprocess.Popen(cmd, cwd=cwd, env=env, stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE, stderr=err, start_new_session=True)

        def kill(why):
            try:
                os.killpg(proc.pid, signal.SIGKILL)
            except OSError:
                pass
            proc.wait()
            fail(EXIT_STARTUP, "start-up check failed, session stopped: " + why +
                 ". Build: check agents only, and no bare run. Test: the leader runs the inputs (N-T42).")

        try:
            proc.stdin.write(prompt.encode("utf-8"))
            proc.stdin.close()
        except BrokenPipeError:
            pass
        init, result = None, None
        for raw in proc.stdout:
            log.write(raw)
            log.flush()
            try:
                msg = json.loads(raw.decode("utf-8"))
            except ValueError:
                if init is None:
                    kill("output before the start-up message can't be read")
                continue
            if not isinstance(msg, dict):
                continue
            if is_hook_event(msg):
                kill("a hook ran in the session (%s); no hook may load" % (msg.get("hook_name") or msg.get("subtype") or "hook"))
            if init is None:
                if msg.get("type") == "system" and msg.get("subtype") == "init":
                    problems = check_init(msg, expected)
                    if problems:
                        kill("; ".join(problems))
                    init = msg
                elif msg.get("type") in ("assistant", "user", "result"):
                    kill("the session acted before its start-up message")
                continue
            if msg.get("type") == "result":
                result = msg
        rc = proc.wait()
    if init is None:
        fail(EXIT_STARTUP, "start-up check failed: the session never reported its start-up tool list (exit %d)" % rc)
    return init, result, rc


def copy_into(src, dst):
    if os.path.islink(src):
        fail(EXIT_RECORD, "%s is a link; the profile copies real files only" % src)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if os.path.isdir(src):
        shutil.copytree(src, dst, symlinks=False)
    else:
        shutil.copy2(src, dst)


def strip_input_header(text):
    lines = text.splitlines(True)
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                lines = lines[i + 1:]
                break
    while lines and (re.match(r"^(source|tests):", lines[0]) or not lines[0].strip()):
        lines = lines[1:]
    return "".join(lines)


def prepare_run_folder(place, prof, profile, input_path):
    root = runs_root(place.slug)
    os.makedirs(root, exist_ok=True)
    os.chmod(root, 0o700)
    stamp = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    run = tempfile.mkdtemp(prefix="%s-%s-" % (profile, stamp), dir=root)
    cfg = run + ".config"
    os.makedirs(cfg)
    try:
        return fill_run_folder(place, prof, profile, input_path, run, cfg)
    except SystemExit:
        shutil.rmtree(run, ignore_errors=True)
        shutil.rmtree(cfg, ignore_errors=True)
        raise


def fill_run_folder(place, prof, profile, input_path, run, cfg):
    if not outside_repository(run, place.workspace):
        fail(EXIT_RECORD, "the run folder would sit inside a repository; failing closed")
    if profile != "bare":
        for s in prof["skills"]:
            src = os.path.join(place.workspace, s)
            ok = inside(src, os.path.join(place.workspace, ".claude", "skills")) or \
                inside(src, os.path.join(place.wf, "package"))
            if not ok or not os.path.isfile(os.path.join(src, "SKILL.md")):
                fail(EXIT_RECORD, "skill %r isn't a skill folder in .claude/skills/ or this workflow's package/" % s)
            copy_into(src, os.path.join(run, ".claude", "skills", os.path.basename(s)))
        for a in prof["agents"]:
            src = os.path.join(place.workspace, a)
            ok = inside(src, os.path.join(place.workspace, ".claude", "agents")) or \
                inside(src, os.path.join(place.wf, "package"))
            if not ok or not os.path.isfile(src):
                fail(EXIT_RECORD, "agent %r isn't an agent file in .claude/agents/ or this workflow's package/" % a)
            copy_into(src, os.path.join(run, ".claude", "agents", os.path.basename(a)))
    for c in prof["context"]:
        src = os.path.join(place.workspace, c)
        if inside(src, place.framework) or not inside(src, place.workspace) or not os.path.isfile(src):
            fail(EXIT_RECORD, "context %r must be a runtime copy in the workflow's place, never in framework/" % c)
        copy_into(src, os.path.join(run, c))
    if input_path:
        src = input_path if os.path.isabs(input_path) else os.path.join(place.workspace, input_path)
        if os.path.islink(src) or not inside(src, os.path.join(place.wf, "inputs")) or not os.path.isfile(src):
            fail(EXIT_REFUSED, "refused: --input must be a file in framework/%s/inputs/" % place.slug)
        os.makedirs(os.path.join(run, "input"))
        with open(os.path.join(run, "input", os.path.basename(src)), "w", encoding="utf-8") as f:
            f.write(strip_input_header(read_text(src)))  # the steps' header never reaches a run
    os.makedirs(os.path.join(run, "practice"))
    with open(os.path.join(run, RUN_MARKER), "w", encoding="utf-8") as f:
        json.dump({"workflow": place.slug, "profile": profile, "created": now_stamp(),
                   "workspace": place.workspace, "config_dir": cfg}, f)
    return run, cfg


def claude_version(env):
    exe = shutil.which("claude", path=env.get("PATH"))
    if not exe:
        fail(EXIT_PREREQ, "claude isn't on PATH; failing closed")
    try:
        out = subprocess.run([exe, "--version"], env=env, stdout=subprocess.PIPE,
                             stderr=subprocess.DEVNULL, timeout=60).stdout.decode("utf-8", "replace")
    except (OSError, subprocess.TimeoutExpired):
        fail(EXIT_PREREQ, "claude --version didn't answer; failing closed")
    m = re.search(r"(\d+\.\d+\.\d+)", out)
    if not m:
        fail(EXIT_PREREQ, "claude --version can't be read; failing closed")
    return exe, m.group(1)


def print_practice(run):
    base = os.path.join(run, "practice")
    budget = 1000000
    for dirpath, _, files in os.walk(base):
        for name in sorted(files):
            path = os.path.join(dirpath, name)
            rel = os.path.relpath(path, run)
            if os.path.islink(path):
                print("--- %s: a link, not read ---" % rel)
                continue
            data = open(path, "rb").read(200001)
            if b"\0" in data:
                print("--- %s: not text, not shown ---" % rel)
                continue
            if len(data) > budget:
                print("--- %s: not shown, output limit reached ---" % rel)
                continue
            budget -= len(data)
            print("--- %s ---" % rel)
            print(data[:200000].decode("utf-8", "replace"))


def cmd_session(place, prof, opts):
    profile = opts["cmd"]
    wb = write_block_of(read_text(place.record))
    if wb is None:
        fail(EXIT_RECORD, "this workflow's write_block can't be read; failing closed")
    if profile == "check" and wb["state"] != "on":
        fail(EXIT_RECORD, "a check session runs only under the block, and the record's write_block is off")
    plan_cross_check(place, prof)
    prompt_file = opts["--prompt-file"]
    if not os.path.isfile(prompt_file):
        fail(EXIT_REFUSED, "refused: the prompt file isn't there")
    prompt = read_text(prompt_file)
    resume = opts.get("--resume")
    if not resume and "practice run" not in prompt.lower():
        fail(EXIT_REFUSED, "refused: every framework session's prompt carries the practice-run cue")
    if resume:
        run = real(opts["--run-folder"])
        mk = run_marker(run)
        if not inside(run, runs_root(place.slug)) or mk is None:
            fail(EXIT_REFUSED, "refused: --run-folder isn't one of this workflow's run folders")
        if mk.get("workflow") != place.slug or mk.get("profile") != profile or mk.get("workspace") != place.workspace:
            fail(EXIT_REFUSED, "refused: a session resumes only through the profile it started in (%s)" % mk.get("profile"))
        cfg = mk["config_dir"]
    else:
        run, cfg = prepare_run_folder(place, prof, profile, opts.get("--input"))
    print("run_folder: %s" % run)  # recorded in run_folders or the round's Environment
    sys.stdout.flush()
    settings, mcp, builtins, env_names, expected = build_session_config(place, prof, profile, run)
    settings_path, mcp_path = os.path.join(cfg, "settings.json"), os.path.join(cfg, "mcp.json")
    for path, data in ((settings_path, settings), (mcp_path, mcp)):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    verify_written(settings_path, settings, expected)
    env = child_env(env_names)
    exe, version = claude_version(env)
    # RELEASE CHECK 6 rests on every flag here: --restricted ignores the leader's user,
    # project and local settings (so their allow rules and hooks don't load), --tools
    # limits the built-in tools, --strict-mcp-config holds the connections to the profile's,
    # dontAsk with --permission-prompts none refuses every tool not allowed. A version that
    # lacks a flag errors out, which fails closed. --bare isn't used: it drops the
    # subscription login the runs must use.
    base = [exe, "-p", "--output-format", "stream-json", "--verbose", "--include-hook-events",
            "--restricted", "--strict-mcp-config", "--mcp-config", mcp_path,
            "--settings", settings_path, "--permission-mode", "dontAsk",
            "--permission-prompts", "none", "--tools", ",".join(builtins)]
    base += ["--disallowedTools"] + [d for d in settings["permissions"]["deny"] if " " not in d]
    base += ["--allowedTools"] + [a for a in settings["permissions"]["allow"] if " " not in a]
    if profile == "bare":
        base.append("--disable-slash-commands")  # no skill instructions in the bare run (rules 8.6)
    # The probe: the same session settings, a prompt that does nothing, checked before the
    # real prompt is sent anywhere. Then the real session is checked again on its own start.
    probe_log = os.path.join(cfg, "probe-%s.jsonl" % datetime.datetime.utcnow().strftime("%H%M%S%f"))
    run_claude(base + ["--no-session-persistence"], run, env, PROBE_PROMPT, probe_log, expected)
    real_cmd = base + (["--resume", resume] if resume else [])
    log = os.path.join(cfg, "session-%s.jsonl" % datetime.datetime.utcnow().strftime("%H%M%S%f"))
    init, result, rc = run_claude(real_cmd, run, env, prompt, log, expected)
    print("session_id: %s" % (init.get("session_id") or ""))
    print("profile: %s" % profile)
    print("claude_version: %s" % version)
    print("startup_check: passed")
    print("--- result ---")
    if result is not None:
        print(result.get("result") or "")
    if profile != "bare":
        print_practice(run)
    if rc != 0 or result is None or result.get("is_error"):
        say("the session ended with an error (exit %d); its log is in %s" % (rc, cfg))
        sys.exit(EXIT_SESSION)


def main():
    self_path = sys.argv[1]
    opts = parse_args(sys.argv[2:])
    place = locate(self_path, opts["slug"])
    check_fingerprint(place, opts["--plugin-copy"])
    cmd = opts["cmd"]
    needs_profile = cmd in PROFILES or cmd in ("block-rules", "settings-check")
    prof = parse_profile(read_text(place.record), place.slug) if needs_profile else None
    if cmd in PROFILES:
        cmd_session(place, prof, opts)
    elif cmd == "block-rules":
        cmd_block_rules(place, prof)
    elif cmd == "lift-rules":
        cmd_lift_rules(place)
    elif cmd == "allow-rules":
        cmd_allow_rules(place, opts.get("--lift", False))
    elif cmd == "settings-check":
        cmd_settings_check(place, prof)
    elif cmd == "practice-create":
        cmd_practice_create(place, opts["--round"])
    elif cmd == "practice-clear":
        cmd_practice_clear(place, opts["--path"])
    elif cmd == "runs-clear":
        cmd_runs_clear(place, opts["--path"])


main()
PYTHON
