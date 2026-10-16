#!/usr/bin/env python3
"""Run one Deconstruct eval: build its fixture, run the skill, and play the student.

Usage:
  python3 run_eval.py <eval-id> <out-dir> [--plugin DIR] [--max-turns N] [--only-session N]

  --plugin        plugin folder under test (default: this repo's plugins/handsonai)
  --max-turns     cap on AI turns per session (default 60; a baseline run may cap lower)
  --only-session  run one session of a multi-session eval (1-based)

For each session it writes, under <out-dir>/session-<n>/:
  workspace-start/  the fixture as built
  workspace/        the same folder after the run (the skill works here)
  transcript.md     every message, AI and student, in order
Then grade with: python3 grade_eval.py <out-dir>

The skill runs with `claude -p` and only this plugin (`--setting-sources project,local`
drops the account's own plugins). The student is a second `claude -p` that sees only its
script and the conversation so far, and may only read files (decided R10-5).
"""
import argparse
import json
import shutil
import subprocess
import sys
import uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]

STUDENT_RULES = """You are playing a student in a test of an AI interview. Follow the script below exactly.
Reply with only the student's next message: no notes, no quotes around it, no labels.
Answer only what the AI's last message asks. One short reply. Never use framework terms the AI hasn't used.
If the script's stop condition is met, reply exactly END.

SCRIPT:
"""


def claude(args, prompt, cwd):
    # The prompt goes on stdin: --allowedTools takes several values and would swallow it.
    cmd = ["claude", "-p", "--setting-sources", "project,local", "--output-format", "json"] + args
    r = subprocess.run(cmd, cwd=cwd, input=prompt, capture_output=True, text=True, timeout=1800)
    if r.returncode != 0:
        raise RuntimeError(f"claude failed ({r.returncode}): {r.stderr[-2000:]}")
    return json.loads(r.stdout)["result"].strip()


def run_session(ev, s, n, out, plugin, max_turns):
    d = out / f"session-{n}"
    if d.exists():
        sys.exit(f"{d} exists; use a new out-dir")
    d.mkdir(parents=True)
    fixture = s.get("fixture", ev["fixture"])
    subprocess.run([sys.executable, str(HERE / "fixtures" / "make_fixture.py"), fixture, str(d / "workspace-start")],
                   check=True, capture_output=True)
    ws = d / "workspace"
    shutil.copytree(d / "workspace-start", ws)

    script = (HERE / ev["student"]).read_text() if s.get("student") and ev.get("student") else None
    replies = list(s.get("replies", []))
    turns = s.get("max_turns", max_turns)
    sid = str(uuid.uuid4())
    skill_args = ["--plugin-dir", str(plugin), "--dangerously-skip-permissions"]

    transcript = []
    msg = s["prompt"]
    for turn in range(turns):
        transcript.append(f"## Student\n\n{msg}\n")
        first = turn == 0
        ai = claude(skill_args + (["--session-id", sid] if first else ["--resume", sid]), msg, ws)
        transcript.append(f"## AI\n\n{ai}\n")
        (d / "transcript.md").write_text("\n".join(transcript))
        if replies:
            msg = replies.pop(0)
        elif script:
            convo = "\n".join(transcript)
            msg = claude(["--system-prompt", STUDENT_RULES + script, "--allowedTools", "Read"],
                         f"The conversation so far:\n\n{convo}\n\nYour next message as the student:", ws)
            if msg.strip() == "END":
                transcript.append("## Student\n\nEND\n")
                break
        else:
            break
    else:
        transcript.append(f"## Harness\n\nStopped at the turn cap ({turns}).\n")
    (d / "transcript.md").write_text("\n".join(transcript))
    return d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("eval_id")
    ap.add_argument("out_dir")
    ap.add_argument("--plugin", default=str(ROOT / "plugins" / "handsonai"))
    ap.add_argument("--max-turns", type=int, default=60)
    ap.add_argument("--only-session", type=int)
    a = ap.parse_args()

    evals = {e["id"]: e for e in json.loads((HERE / "evals.json").read_text())["evals"]}
    ev = evals[a.eval_id]
    sessions = ev.get("sessions") or [{"prompt": ev["prompt"], "student": True}]
    out = Path(a.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "eval.json").write_text(json.dumps(ev, indent=2, ensure_ascii=False))
    for n, s in enumerate(sessions, 1):
        if a.only_session and n != a.only_session:
            continue
        print(run_session(ev, s, n, out, Path(a.plugin), a.max_turns))


if __name__ == "__main__":
    main()
