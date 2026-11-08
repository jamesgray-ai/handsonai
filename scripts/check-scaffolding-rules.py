#!/usr/bin/env python3
"""Rule-text checks for scaffolding-registry and indexing-registry, which have no eval workspace.

Each check asserts that a rule a leader's run depends on is written in the skill (or that a known
wrong pattern isn't). These are fixture-level checks of the text, not of a model's behaviour: they
catch a rule being dropped or contradicted by an edit. Exit 1 on any failure. 3c-EL (2026-11-08).
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SK = ROOT / "plugins" / "handsonai" / "skills"
SR = (SK / "scaffolding-registry" / "SKILL.md").read_text()
IG = (SK / "scaffolding-registry" / "references" / "interview-guide.md").read_text()
IX = (SK / "indexing-registry" / "SKILL.md").read_text()
EX = (SK / "scaffolding-registry" / "references" / "example-registry.md").read_text()

checks = []
def must(name, text, needle):
    checks.append((name, needle in text))
def must_not(name, text, pattern):
    checks.append((name, re.search(pattern, text) is None))

# Order: nothing before the storage question; N-F16 gated to Claude and ChatGPT on the web
must("storage question comes first, nothing before it", SR, "**Nothing comes before it:** no greeting, no opening, no question about who the registry is for")
must("N-F16 gated to Claude and ChatGPT on the web", SR, "On Claude or ChatGPT on the web, in any tab or mode, ChatGPT's Work tab included (never Claude desktop, Microsoft 365 Cowork, Claude Code or Codex: any chat not working in a folder on the leader's computer counts as the web, and a sandbox or workspace the AI runs in online is not the leader's computer)")
must("N-F16 said exactly", SR, "I can't see a drive I can save to in this chat. Add your cloud drive to this chat from the prompt box")
must("print-to-save only for Gemini or after 'continue'", SR, "Gemini, or on the web after the leader says 'continue' to N-F16")
must_not("no old 'web chat with no storage connection' print-to-save trigger", SR, r"a web chat with no storage connection on")
# Folder not found, existing registry
must("N-F17 offers to create a missing folder", SR, "I can't find [folder] in your [storage service]. Shall I create it there?")
must("N-SR2 for a registry already there", SR, "You already have a registry here, so I'll check it for gaps instead of starting over.")
must("no gaps: one line, then the close", SR, "With no gaps, say so in one line, then the close's check, the dashboard and N-A7.")
must("the opening yields to N-SR2", IG, "with a registry already there, N-SR2 comes first")
# The storage question: by situation, not platform name (ChatGPT Work-tab test, 2026-11-08)
must("first message settles where the files go (top of skill)", SR, "**Your first message settles where the files go.**")
must("any tab or mode counts as the web", SR, "in any tab or mode, ChatGPT's Work tab included")
must("an online sandbox is not the leader's computer", SR, "a sandbox or workspace the AI runs in online is not")
must("uploads are never the working folder", SR, "Files uploaded to the chat are never the working folder.")
must("the AI's library is never picked or searched in place of asking", SR, "Never pick the AI's own file library (such as ChatGPT's Library) yourself")
must("a library folder the leader names is a working folder", SR, "a folder there that the leader names or chooses is a working folder like any other")
must("the library offered in the storage question", SR, "name it in the storage question's [storage service] beside any drive")
must("go ahead with two places: ask which", SR, "Where [storage service] names more than one place and the leader says \"go ahead\", ask which one in one line.")
# Gap-filling mode as ordered steps (ChatGPT test, 2026-11-08: found folder used unconfirmed, check skipped)
must("gap mode: every step, in order", SR, "Then these steps, in this order, every one of them, with nothing said before the first:")
must("gap mode: a found folder is confirmed", SR, "**Confirm a folder you found.**")
must("gap mode: the close's check runs every time", SR, "**The close's check, every time, gaps or not**")
must("gap mode: present is not checked", SR, "Finding the pages present is not the check")
must("gap mode: N-A7 as text", SR, "ending with N-A7: Analyze's start phrase and the location, as text the leader can copy")
must("Owns: the earlier form is moved out of the markers", IX, "move it above the opening marker; that is the only change made outside them")
# Goals are never invented
must("never invent goals (guide)", IG, "**Never invent goals,**")
must("N-SR3 when no goals are given", IG, "Your goals for this year aren't recorded yet; tell me them any time.")
must("goals only as the leader gives them (skill)", SR, "only as the leader gives them (never invented or drafted")
# Formatted examples, never code blocks, for anything played back
must("processes draft shown as formatted text", IG, "Show it as a formatted list in\nthe chat, never in a code block")
block = IG[IG.index("Here are my suggested processes"):IG.index("**Ask:** \"What would you add, remove, rename, or move?")]
checks.append(("processes draft isn't inside a code fence", "```" not in block))
# Plain words
must("never name a skill or a hand-off (rules for every message)", SR, "**Never name a skill, or a hand-off between skills.**")
must("never name a skill (indexing-registry)", IX, "Never name a skill or a hand-off between skills")
must_not("no 'every page against all its rules' sample to copy", IX, r"I checked every page of your registry against all its rules")
must_not("N-A7 asks nothing", IG, r"Want to run it now\?")
# Owns blocks
must("Owns form shown, heading outside the markers", IX, "# Owns\n\n<!-- GENERATED:owns -->\n- [")
must("close's check covers the Owns block", IX, "each Function's `# Owns` block lists exactly the Processes it owns")
must("print-to-save gives Function pages with Owns filled", IG, "each Function page with its `# Owns` filled")
checks.append(("example registry keeps the heading outside the markers", "# Owns\n\n<!-- GENERATED:owns -->" in EX))
# Cloud sessions and unreachable sources
must("cloud: name the repository, never a path", SR, "name the repository, never a path on the machine")
must("cloud: commit and push after the close's check and after the Artifact line", SR, "commit `registry/`, `REGISTRY.md` and `registry-dashboard.html` and push them to the session's branch yourself, and again after the Artifact's log line")
must("cloud: N-F18", SR, "Your work is saved on GitHub, on the branch [branch].")
must("cloud: the dashboard is in the repository, inside the close template", IG, "in a cloud session, it's in your repository on GitHub to download")
must("an unreachable link is pasted, never an environment change", IG, "never propose changing the environment, network, permissions or credentials")
# Start phrases
must("start phrases word for word", IG, "never \"Run Analyze\"")
must("N-A7's Claude Code and Codex form has no location", IG, "When you're ready, say 'run the analyze skill.' (in Claude Code")

bad = [n for n, ok in checks if not ok]
for n, ok in checks:
    print(("  ok    " if ok else "  FAIL  ") + n)
print(f"\n{len(checks) - len(bad)} passed, {len(bad)} failed")
sys.exit(1 if bad else 0)
