#!/usr/bin/env python3
"""The simulated leader (R10-5) and the platform simulations it works in (rules 14).

A second agent plays a business leader new to evaluation, from a fixed script (students/*.md): it
sees only its script, the conversation and what its screen shows, answers one message at a time,
and never uses a framework term the AI hasn't used first (the fidelity check).

Every eval session runs the skill in Claude Code. For the other five platforms the session runs
with a platform preamble (appended to the skill's system prompt) and a workspace laid out the way
that platform keeps files; what happens *outside* the skill's chat (a new chat the leader opens,
Agent Builder making an agent, Cowork attaching a folder) is simulated here, deterministically, and
shown to the leader as their screen. An eval picks one with `"platform": "<key>"` and seeds the
platform's known failures with `"platform_faults": [...]`:

  claude-code     files in the workspace (the real platform; no preamble); for Build, a
                  stand-in Gmail connection when the plan uses Gmail (run_eval.connections_for).
                  Faults: no_gmail (the leader hasn't connected it)
                  and, for Build and Test, the leader's click on Claude Code's prompt for
                  .claude/settings.local.json (run_eval.settings_prompt_for). Fault:
                  leader_denies_settings_prompt (the leader declines that prompt)
  codex           files in the workspace; Codex's wording and its read-only bare-run command

For Test on Claude Code and Codex, the leader's own runs are simulated too (`simulates_leader_runs`):
a hand-over's block runs in a new session in the workspace itself (the leader's second terminal),
with the built workflow installed there and nothing from the framework chat, and its answer is the
leader's screen, as the chat platforms' new chats are. A session whose script plants the block a run
ends with (a contaminated or injected run, say) opts out with `"leader_runs": "scripted"`, and the
leader pastes the script's block as before. On the chat platforms the same opt-out keeps the new chat's
answer off the leader's screen (`scripted_runs`), so the planted block is the only one they can paste. Build keeps its own behaviour on both platforms.
  claude-web      Google Drive (the working folder ./drive/ai-workspace); paste-back from new chats.
                  Faults (claude-web and chatgpt): service_dropbox (the connected service is Dropbox, so
                  locations read "Dropbox, in ai-workspace"), drive_cannot_save (the connection
                  reads only)
  claude-desktop  the working folder selected in the chat (./ai-workspace); faults: no_folder_added
                  (no folder selected)
  chatgpt         Google Drive (the working folder ./drive/ai-workspace); apps; paste-back from new chats
  microsoft-365   OneDrive (the working folder ./onedrive/ai-workspace), read from the location with nothing attached;
                  Cowork's folder ./onedrive/Documents/Cowork; Agent Builder from a pasted build
                  prompt. Faults: cowork_cannot_read_onedrive (the attach fallback; with
                  attach_fails, the admin line), agent_builder_missing_context_file,
                  agent_builder_rewords_carried_line, agent_builder_requirements_under_knowledge,
                  agent_builder_ordinary_chat, skill_cannot_read_by_path

The leader-action counter (`count_actions`) reports leader actions per run (each message the leader
sends, plus each action a simulation counts on the leader's screen: opening a chat, pasting, adding
a file under Knowledge, choosing Create) against the spec's journey figures. It never measures time.
`replies_by_part` splits the leader's replies at the skill's signposts and reports, at each count Deconstruct
says, the replies still to come (Deconstruct says one: in the line that says how its interview will go).
"""
import json
import re
import shutil
import zipfile
import subprocess
from pathlib import Path

import approved_lines as AL

COMPOSE = Path(__file__).resolve().parents[1] / "plugins" / "handsonai" / "tools" / "compose-registry.js"

LEADER_RULES = """You are playing a business leader in a test of an AI framework step. You see only your script, the conversation, and what your screen shows you.
Reply with only the leader's next message: no notes, no quotes around it, no labels.
Rules:
- Stay the person. Never mention the script, these rules, a test or a "Not sure?" line, and never explain why you
  give an answer ("the script says…"): reply only what that person would type.
- When you don't know, say only that you're not sure, in a few words. Never give a reason, a detail or a fact
  the script doesn't hold.
- Answer only from the script and your screen. If neither covers what the AI asks, say you're not sure, in a few
  words, and add nothing of your own: no guesses, no new names, numbers, tools, people or habits.
- Use plain, everyday words. You are new to evaluation: never use a framework or evaluation term (for example
  acceptance criterion, fixed step, human gate, autonomy, Golden Example, eval, test case, scenario) unless the AI
  used it first.
- Do each provocation the script lists exactly where the script says, and nowhere else.
- Otherwise answer only what the AI's last message asks, the way the person in the script would. Don't volunteer
  a fact the AI hasn't asked for yet unless the script tells you to.
- When the AI asks you to do something on your screen (open a chat, paste text, add a file, choose a button),
  do it as your screen allows, then say what the AI asked for: paste what your screen shows when it asks you to
  paste it. Each thing you do on screen, write first on its own line as [did: what you did].
- If the script's stop condition is met, reply exactly END.

SCRIPT:
"""

DID = re.compile(r"^\s*\[did:[^\]]*\]\s*$", re.M)


def strip_actions(msg):
    """The leader's message as the skill sees it, and the on-screen actions it reported."""
    acts = DID.findall(msg)
    return DID.sub("", msg).strip(), len(acts)


# ---------------------------------------------------------------- platforms

# Build's install line on a platform where the leader saves the skill (N-B12: "Do you see [skill] in your
# skills list?"), and the replace form a fix gives ("Replace its instructions with…", "it replaces the … skill").
INSTALL_LINE = re.compile(r"in your skills list\?|\breplace (?:its|the) (?:instructions|contents|skill)\b|\bit replaces the [\w-]+ skill\b",
                          re.I)


class Platform:
    key = "claude-code"
    name = "Claude Code"
    files_root = ""           # where the working folder lives, relative to the workspace
    location = "framework/[workflow-slug]"
    paste_back = False
    run_in_workspace = False  # a leader's run happens in the workspace itself, not a cold copy
    leader_runs = False       # set per session by simulates_leader_runs: hand-overs run on this platform too
    scripted_runs = False     # set per session by scripted_runs: a planted block; no run chat is simulated
    run_opening = "You opened a new chat and pasted the block"

    def __init__(self, faults=()):
        self.faults = set(faults)
        self.state = {}

    def preamble(self):
        return self.with_planted(None)

    def run_preamble(self):
        """The system-prompt addition for a run the leader starts from a hand-over."""
        return self.preamble()

    def with_planted(self, p):
        """The preamble, plus any content a fixture planted for the platform to supply unasked
        (`.sim-grounding.md`: Cowork's mail and Teams grounding, a connector's results). Analyze sets
        it aside (R5); an eval checks it never becomes evidence."""
        g = self.state.get("grounding")
        if not g:
            return p
        note = ("Simulated platform: content this platform added to the chat on its own, without the leader "
                "or the skill asking for it:\n" + g)
        return f"{p}\n\n{note}" if p else note

    def leader_notes(self):
        return ""

    def prepare(self, ws):
        """Lay the workspace out the way this platform keeps the leader's files."""
        take_planted(self, ws)

    def on_leader(self, msg, ws):
        """React to what the leader typed (an attach, say). Returns platform actions to count."""
        return self.apply_install(msg, ws)

    def apply_install(self, msg, ws):
        """final-test-1a (2026-11-24): on a platform where the leader installs by hand (paste_back), a yes or
        "done" to Build's install line saves what Build staged into the stand-in account (`.claude/skills`,
        what a new chat loads), as the leader's own save would. No install line, nothing saved: a Build
        that never has its fix installed is still caught by the next Test round."""
        if not self.state.pop("install", False) or not re.search(r"\b(yes|done|i do|i see|see it|replaced|saved)\b", msg, re.I):
            return 0
        account = Path(ws) / ".claude" / "skills"
        saved = 0
        for pkg in sorted(Path(ws).glob("**/framework/*/package")):
            for f in sorted(pkg.rglob("SKILL.md")):
                target = account / f.parent.name
                if target.exists():
                    shutil.rmtree(target)
                shutil.copytree(f.parent, target)
                saved += 1
            for z in sorted(pkg.rglob("*.zip")):
                with zipfile.ZipFile(z) as zf:
                    names = [n for n in zf.namelist() if n.endswith("SKILL.md")]
                    for n in names:
                        top = Path(n).parent
                        target = account / (top.name or z.stem)
                        if target.exists():
                            shutil.rmtree(target)
                        prefix = "" if str(top) == "." else str(top) + "/"
                        for m in zf.namelist():
                            if m.startswith(prefix) and not m.endswith("/"):
                                dest = target / m[len(prefix):]
                                dest.parent.mkdir(parents=True, exist_ok=True)
                                dest.write_bytes(zf.read(m))
                        saved += 1
        return 1 if saved else 0

    def screen(self, ai_text, ws, run_chat=None):
        """What the leader's screen shows after this AI message: [(observation, actions)]."""
        out = []
        if self.paste_back and INSTALL_LINE.search(ai_text or ""):
            self.state["install"] = True
        if (self.paste_back or self.leader_runs) and run_chat is not None:
            block = handover_block(ai_text)
            if block and self.scripted_runs:
                # the script plants the run's answer: the leader opens the chat and pastes; no answer shows
                out.append((f"[{self.run_opening}.]", 3))
            elif block:
                answer = run_chat(block, self)
                out.append((f"[{self.run_opening}. It answered:]\n{answer}", 3))
        return out


PLANTED_HISTORY = ".sim-history.jsonl"
PLANTED_GROUNDING = ".sim-grounding.md"


def take_planted(platform, ws):
    """Take the hidden files a fixture plants for the simulation, before the session starts (and
    before the workspace is snapshotted), so the skill never sees them as files:
    - `.sim-history.jsonl`: requests typed into Claude Code (one JSON object per line, as
      ~/.claude/history.jsonl holds them; "WORKSPACE" as the project is this workspace), added to
      the temp HOME's history, which the evidence pass's typed-request clause reads;
    - `.sim-grounding.md`: content the platform supplies unasked, added to the platform preamble
      (with_planted)."""
    ws = Path(ws)
    hist = ws / PLANTED_HISTORY
    if hist.exists():
        home_hist = ws.parent / "home" / ".claude" / "history.jsonl"
        text = hist.read_text().replace('"WORKSPACE"', json.dumps(str(ws)))
        platform.state["typed_history"] = text  # shown to the judges as its own context block (grade_eval)
        if home_hist.parent.is_dir():
            with home_hist.open("a") as f:
                f.write(text if text.endswith("\n") else text + "\n")
        hist.unlink()
    grounding = ws / PLANTED_GROUNDING
    if grounding.exists():
        platform.state["grounding"] = grounding.read_text().strip()
        grounding.unlink()


# The working folder's own folders: the framework's, and the documents Analyze's evidence pass reads
# (knowledge/, sops/, process-guides/; requirements 3.1 R4).
WORKING_FOLDER_DIRS = ("framework", "registry", "knowledge", "sops", "process-guides")


def _move_into(ws, sub):
    """Move the workspace's framework files into a working folder, ws/sub/ai-workspace (on a drive) or
    ws/ai-workspace (the folder selected on Claude desktop), keeping the workspace's layout: framework/,
    registry/, knowledge/, the evidence pass's documents (sops/, process-guides/) and the registry views
    at its root, framework-level files in framework/. The registry's links are relative to its parent
    folder (registry-bundle.md rule 4), the working folder here as in the workspace, so
    `framework/<slug>/...` links carry over unchanged."""
    ws = Path(ws)
    target = ws / sub / "ai-workspace" if sub else ws / "ai-workspace"
    dirs = [d for d in WORKING_FOLDER_DIRS if (ws / d).exists()]
    views = [f for f in ("REGISTRY.md", "registry-dashboard.html") if (ws / f).exists()]
    level = [f for f in ("backlog.md", "ai-opportunity-report.md", "analyze-in-progress.md") if (ws / f).exists()]
    if not (dirs or views or level):
        return target  # nothing to move: no working folder yet, so none is made (Analyze's first run)
    target.mkdir(parents=True, exist_ok=True)
    for d in dirs:
        shutil.move(str(ws / d), str(target / d))
    for f in views:
        shutil.move(str(ws / f), str(target / f))
    if level:
        (target / "framework").mkdir(exist_ok=True)
        for f in level:
            shutil.move(str(ws / f), str(target / "framework" / f))
    md = list((target / "registry").rglob("*.md")) if (target / "registry").exists() else []
    for p in md + [target / "REGISTRY.md"]:
        if p.exists():
            text = p.read_text()
            # a skill installed in the leader's account isn't a file beside the registry: its name, as text
            moved = re.sub(r"\[([^\]]+)\]\(\.(?:claude|agents)/skills/[^)]+\)", r"\1", text)
            if moved != text:
                p.write_text(moved)
    if (target / "registry" / "SCHEMA.md").exists():
        # the views as a maintenance pass on this platform leaves them (the skills inventory scans the
        # folder, which holds no installed skill here), so the registry lints and composes clean
        subprocess.run(["node", str(COMPOSE), "registry"], cwd=target, capture_output=True, text=True)
    return target


# Build's ask to pause an older skill on Claude Code (claude-code-block / setup.md: move the folder out, or add
# `disable-model-invocation: true` to its SKILL.md), then "Say 'done' when it's paused…"
PAUSE_ASK = re.compile(r"(?is)disable-model-invocation.*?\bsay\s+[‘’'\"“”]done[‘’'\"“”]\s+when it[‘’']?s paused")


class ClaudeCode(Platform):
    run_in_workspace = True
    run_opening = ("You opened a second terminal window, went to the folder, started Claude Code and pasted "
                   "the block")

    def run_preamble(self):
        return None  # the real platform: the workspace's .claude/skills load as they would for the leader

    def screen(self, ai_text, ws, run_chat=None):
        # remember which older skills Build asked the leader to pause, for their "done" (on_leader)
        self.state["pause"] = (sorted(set(re.findall(r"\.claude/skills/([A-Za-z0-9_-]+)", ai_text or "")))
                               if PAUSE_ASK.search(ai_text or "") else [])
        return Platform.screen(self, ai_text, ws, run_chat)

    def on_leader(self, msg, ws):
        """build-full-1 (2026-11-21): the leader says "done" to pausing an older skill, as the student script
        says, but a student can't edit files: the leader's edit is made here, as Build asked, by adding
        `disable-model-invocation: true` to that skill's SKILL.md frontmatter (the folder stays put)."""
        names = self.state.pop("pause", [])
        if not names or not re.search(r"\bdone\b", msg, re.I):
            return 0
        acts = 0
        for name in names:
            f = Path(ws) / ".claude" / "skills" / name / "SKILL.md"
            if not f.is_file():
                continue
            text = f.read_text()
            m = re.match(r"---\n(.*?)\n---", text, re.S)
            if not m or re.search(r"(?m)^disable-model-invocation:", m.group(1)):
                continue
            f.write_text(f"---\n{m.group(1)}\ndisable-model-invocation: true\n---" + text[m.end():])
            acts += 1
        return acts


class Codex(Platform):
    key, name = "codex", "Codex"
    run_in_workspace = True
    run_opening = "You opened a new Codex session in the folder and pasted the block"

    def preamble(self):
        return self.with_planted(
            "Simulated platform: you are running as Codex (the CLI) in this workspace, not Claude Code. "
            "Name the platform as Codex wherever you'd name it, use Codex's own steps, and say 'a new session' "
            "for a new chat. The framework folder is framework/ in this workspace.")

    def run_preamble(self):
        return ("Simulated platform: you are running as Codex (the CLI) in this workspace, not Claude Code; say "
                "'a new session' for a new chat. Codex's installed skills are the folders in .agents/skills/ here: "
                "when a message asks you to use one, read its SKILL.md and follow it.")


# Chat platforms keep the leader's history the way the real products do: saved memory, and past chats
# searched on request. The fixtures hold none about the leader's work, so the evidence pass finds
# nothing there (Cowork's memory is never offered: requirements 3.1 R4, fail closed).
CHAT_HISTORY = (" This chat has the platform's saved memory and can search the leader's past chats on request; "
                "in this simulation neither holds anything about the leader's work.")


class _Drive(Platform):
    files_root = "drive"
    location = "Google Drive, in ai-workspace/framework/[workflow-slug]"
    paste_back = True
    product = ""

    def __init__(self, faults=()):
        super().__init__(faults)
        if "service_dropbox" in self.faults:
            self.location = "Dropbox, in ai-workspace/framework/[workflow-slug]"

    def service(self):
        return "Dropbox" if "service_dropbox" in self.faults else "Google Drive"

    def preamble(self):
        svc = self.service()
        if "drive_cannot_save" in self.faults:
            can = (f"connection is on, but it can only read: it has no tool that creates, edits, moves or renames a "
                   f"file, so nothing can be saved under ./drive")
        else:
            can = "connection is on and can write"
        p = (f"Simulated platform: {self.product}, in a chat outside any Project. The leader's {svc} "
             f"{can}; in this simulation the drive's files are the folder ./drive here "
             f"(./drive/ai-workspace is '{svc}, in ai-workspace'). No other storage service is connected. Read and save the leader's files "
             "only through it. You have no terminal of your own for the leader's work and no local folder: anything "
             "the leader must run in a new chat, give them to paste, and they paste back what it says.")
        return self.with_planted(p + CHAT_HISTORY)

    def prepare(self, ws):
        take_planted(self, ws)
        _move_into(ws, "drive")


class ClaudeWeb(_Drive):
    key, name, product = "claude-web", "Claude on the web", "Claude on the web (claude.ai)"


class ChatGPT(_Drive):
    key, name, product = "chatgpt", "ChatGPT", "ChatGPT (Plus), where connections are called apps"


class ClaudeDesktop(Platform):
    key, name = "claude-desktop", "Claude desktop"
    location = "ai-workspace/framework/[workflow-slug]"
    paste_back = True

    def preamble(self):
        return self.with_planted(
            "Simulated platform: Claude desktop, with the leader's working folder selected in this chat; in this "
            "simulation it is the folder ./ai-workspace here. If ./ai-workspace isn't there, no folder is selected "
            "in this chat. Anything the leader must run in a new chat, give them to paste, and they paste back." + CHAT_HISTORY)

    def prepare(self, ws):
        take_planted(self, ws)
        target = _move_into(ws, "")
        if "no_folder_added" in self.faults:
            target.mkdir(parents=True, exist_ok=True)  # the leader's folder exists; it isn't selected in the chat
            hidden = Path(ws).parent / ".sim-hidden" / "ai-workspace"
            hidden.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(target), str(hidden))
            self.state["hidden"] = hidden

    def on_leader(self, msg, ws):
        if self.state.get("hidden") and re.search(r"\bdone\b", msg, re.I):
            shutil.move(str(self.state.pop("hidden")), str(Path(ws) / "ai-workspace"))
            return 1
        return self.apply_install(msg, ws)

    def leader_notes(self):
        if "no_folder_added" in self.faults:
            return "\nYour screen: you started this chat without selecting your working folder. When asked, select it and say 'done'."
        return ""


class Microsoft365(Platform):
    key, name = "microsoft-365", "Microsoft 365 Copilot Cowork"
    files_root = "onedrive"
    location = "OneDrive, in ai-workspace/framework/[workflow-slug]"
    paste_back = True

    def preamble(self):
        p = ("Simulated platform: Microsoft 365 Copilot Cowork, in a new Cowork chat. Cowork reads and writes the "
             "leader's OneDrive; in this simulation OneDrive is the folder ./onedrive here "
             "(./onedrive/ai-workspace is 'OneDrive, in ai-workspace', and Cowork's own folder is "
             "./onedrive/Documents/Cowork). Read the framework files from the location with nothing attached. "
             "Agents are made by the leader in Copilot's Agent Builder, not here. Anything the leader must run in a "
             "new chat, give them to paste, and they paste back what it says." + CHAT_HISTORY)
        if "skill_cannot_read_by_path" in self.faults:
            p += " In this tenant a Cowork skill can't read a file by its path."
        return self.with_planted(p)

    def prepare(self, ws):
        take_planted(self, ws)
        target = _move_into(ws, "onedrive")
        (Path(ws) / "onedrive" / "Documents" / "Cowork").mkdir(parents=True, exist_ok=True)
        if "cowork_cannot_read_onedrive" in self.faults:
            target.mkdir(parents=True, exist_ok=True)
            hidden = Path(ws).parent / ".sim-hidden" / "ai-workspace"
            hidden.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(target), str(hidden))
            self.state["hidden"] = hidden

    def on_leader(self, msg, ws):
        if self.state.get("hidden") and re.search(r"\bdone\b", msg, re.I) and "attach_fails" not in self.faults:
            shutil.move(str(self.state.pop("hidden")), str(Path(ws) / "onedrive" / "ai-workspace"))
            return 1
        return 0

    def screen(self, ai_text, ws, run_chat=None):
        out = []
        from check_scripted import find_prompt  # late: check_scripted imports nothing from here
        build = find_prompt(ai_text, "build")
        fix = find_prompt(ai_text, "fix")
        if build:
            out.append(self.agent_builder_create(build, ws))
        elif fix:
            out.append(self.agent_builder_fix(fix))
        else:
            out += Platform.screen(self, ai_text, ws, run_chat)
        return out

    # -- Agent Builder
    def agent_builder_create(self, prompt, ws=None):
        if "agent_builder_ordinary_chat" in self.faults and not self.state.get("tried_ordinary"):
            self.state["tried_ordinary"] = True
            return ("[You pasted it into Copilot's ordinary chat by mistake. Copilot answered with a description of "
                    "the agent, and there is no Create button.]", 2)
        files = re.findall(r"Documents/Cowork/[^\s,]+?\.md", prompt)
        knowledge = list(files)
        notes = []
        if "agent_builder_missing_context_file" in self.faults and files:
            notes.append(f"Agent Builder says: I couldn't find {Path(files[0]).name} in your OneDrive.")
            knowledge = knowledge[1:]
        if "agent_builder_requirements_under_knowledge" in self.faults:
            knowledge.append("ai-workspace/framework/requirements.md")
        instructions = self._instructions(prompt, ws)
        self.state["created"] = self.state.get("created", 0) + 1
        self.state["instructions"] = instructions
        self.state["knowledge"] = knowledge
        shown = "\n".join(notes + [f"Knowledge lists: {', '.join(Path(k).name for k in knowledge) or 'nothing'}.",
                                   "Work content: nothing switched on; each source has its own switch you can turn on or off.",
                                   "After Create, the agent shows under Agents. Under Edit, its Instructions read:",
                                   instructions])
        return (f"[You opened Copilot > Chat > Agents > New agent and pasted the prompt.]\n{shown}",
                5 + len(files))

    def agent_builder_fix(self, prompt):
        quoted = re.search(r"carries this line word for word: '(.+?)'\.", AL.norm(prompt))
        ins = self.state.get("instructions", "")
        if quoted:
            want = quoted.group(1)
            if "agent_builder_rewords_after_fix" not in self.faults:
                ins = ins.replace(_reworded(want), want) if _reworded(want) in ins else ins + "\n" + want
        self.state["instructions"] = ins
        return (f"[You opened the agent, chose Edit and pasted the fix. Under Edit, its Instructions now read:]\n{ins}", 4)

    def _instructions(self, prompt, ws=None):
        low = prompt.lower()
        lines = prompt[low.find("word for word:") + len("word for word:"):] if "word for word:" in low else ""
        body = ["You draft this workflow's deliverable from the plan's task. Read only your Knowledge.",
                "\n".join(_plan_lines(prompt, ws)), lines.strip()]
        text = "\n".join(b for b in body if b)
        # Rewords the first agent made; a rebuild (a new agent, release check 29's path) rewords it
        # again only with agent_builder_rewords_after_fix, as a fix prompt does.
        if "agent_builder_rewords_carried_line" in self.faults and (
                not self.state.get("created") or "agent_builder_rewords_after_fix" in self.faults):
            text = text.replace("Practice run: nothing will be sent or changed.",
                                _reworded("Practice run: nothing will be sent or changed."))
        return text


def _plan_lines(prompt, ws):
    """What Agent Builder writes from the files the build prompt names (build.md 6.3: it reads the plan
    and the requirements itself): the requirements' steps, their decisions and rules, acceptance criteria,
    rules, checkpoints and constraints, each as one instruction line. Nothing when the files can't be read."""
    m = re.search(r"in ai-workspace/framework/([\w-]+)", prompt or "")
    if not ws or not m:
        return []
    try:
        req = (Path(ws) / "onedrive" / "ai-workspace" / "framework" / m.group(1) / "requirements.md").read_text()
    except OSError:
        return []
    out = [f"Step {n}: {what}, producing {made}." for n, what, made in
           re.findall(r"^- Step (\d+) — (.+?) · produces (.+?)(?: · .*)?$", req, re.M)]
    out += re.findall(r"^- D\d+ \(Step \d+\): (.+?)(?: · .*)?$", req, re.M)
    out += re.findall(r"^\*\*Rule:\*\* (.+)$", req, re.M)
    out += re.findall(r"^\d+\. \*\*AC\d+[^*]*\*\* — (.+)$", req, re.M)
    for row in re.findall(r"^\| ([RGP]\d+) \|(.+)\|\s*$", req, re.M):
        cells = [c.strip() for c in row[1].split("|")]
        out.append(cells[0] if row[0].startswith("P") else cells[-1])
    # The build prompt's carried lines tell the agent never to write requirement IDs, and Agent Builder
    # reads the Context Inventory, so a context item's ID comes out as its name ("Follow C1's tone" ->
    # "Follow the follow-up style guide's tone"): the planted fault stays the only defect.
    names = {i: n.strip()[0].lower() + n.strip()[1:] for i, n in
             re.findall(r"^\| (C\d+) \| ([^|]+) \|", req, re.M)}
    out = [re.sub(r"\b(C\d+)\b", lambda k: f"the {names[k.group(1)]}" if k.group(1) in names else k.group(1), x)
           for x in out]
    return [re.sub(r" · \(you\)$", "", x).strip() for x in out if x.strip()]


def _reworded(line):
    return line.replace("changed.", "modified.") if line.endswith("changed.") else line + " (paraphrased)"


PLATFORMS = {c.key: c for c in (ClaudeCode, Codex, ClaudeWeb, ClaudeDesktop, ChatGPT, Microsoft365)}


def platform_for(ev, session=None):
    key = (session or {}).get("platform", ev.get("platform", "claude-code"))
    if key not in PLATFORMS:
        raise ValueError(f"unknown platform {key!r}: one of {sorted(PLATFORMS)}")
    # a session's own platform_faults win (one session of an eval on print-to-save, say), as run_eval reads them
    return PLATFORMS[key]((session or {}).get("platform_faults", ev.get("platform_faults", [])))


LEADER_RUN_MODES = ("simulated", "scripted")


def simulates_leader_runs(skill, platform, session=None, ev=None):
    """Whether a Test session on Claude Code or Codex runs the leader's hand-overs (run_chat in the
    workspace) instead of the script's "Your runs" blocks. A first round's practice set holds an input
    the AI writes itself, which no scripted block can match, so simulated is the default; a session
    (or eval) whose script plants the run's block says `"leader_runs": "scripted"`. Build never: its
    behaviour on these platforms is unchanged."""
    mode = (session or {}).get("leader_runs", (ev or {}).get("leader_runs", "simulated"))
    return skill == "test" and platform.key in ("claude-code", "codex") and mode != "scripted"


def scripted_runs(session=None, ev=None):
    """`leader_runs: "scripted"` (session or eval) on any platform: the script plants the block a run ends
    with (a contaminated run, a block with no practice-run line), so no run chat is simulated and the
    leader's screen shows no answer for them to paste in its place. On Claude Code and Codex this is
    simulates_leader_runs' opt-out; on the chat platforms it switches paste_back's run chat off too."""
    return (session or {}).get("leader_runs", (ev or {}).get("leader_runs")) == "scripted"


def handover_block(ai_text):
    """The block a hand-over asks the leader to paste into a new chat (Test's N-T8, Build's N-B45)."""
    if not re.search(r"(?i)paste (the block below|this)", ai_text):
        return None
    m = re.findall(r"```[^\n]*\n(.*?)```", ai_text, re.S)
    return m[-1].strip() if m else None


# ---------------------------------------------------------------- the action counter

def count_actions(sessions):
    """Leader actions per run: every message the leader sent (its first prompt included, END not),
    plus the on-screen actions the simulations and the leader reported."""
    msgs = sum(1 for s in sessions for t in s["turns"]
               if t["role"] == "student" and not t.get("end") and t["text"].strip() != "END")
    screen = sum(t.get("actions", 0) for s in sessions for t in s["turns"] if t["role"] == "student")
    return {"messages": msgs, "screen_actions": screen, "actions": msgs + screen}


def _is_reply(t):
    return t["role"] == "student" and not t.get("end") and t["text"].strip() != "END"


def replies_by_part(sessions, skill="deconstruct"):
    """Leader replies per part, on top of count_actions: every reply count_actions counts as a message, split
    at the skill's "Part k of N" signposts (check_scripted.SIGNPOST_IDS; replies before the first signpost are
    "entry"), plus, at each AI message that carries a count, the replies still to come after it: what that
    count's [M] promises. Deconstruct's one count is in the line that says how the interview will go
    (check_scripted.COUNT_CARRIERS); a run that also says "About [M] questions left." gets a count point for it,
    so the stray count shows. A skill with no signposts (Deconstruct, since its single interview) has only
    "entry". Never measures time."""
    import check_scripted as CS  # lazily: check_scripted doesn't import this module, but keep loading cheap
    total = CS.SIGNPOST_IDS.get(skill, (0, []))[0]
    signpost = re.compile(rf"\bPart ([1-9]) of {total}\b") if total else None
    corpus = AL.load()
    carriers = [(f, f"{lid}") for lid, form in CS.COUNT_CARRIERS for f in corpus.get(lid, form) if f.text]
    count_line = [f for f in corpus.get(CS.COUNT_LINE_ID) if f.text]
    flat = [(s.get("n", k), t) for k, s in enumerate(sessions, 1) for t in s["turns"]]
    by_part, part, points, ai_no = {"entry": 0}, "entry", [], {}
    for at, (n, t) in enumerate(flat):
        if t["role"] == "ai":
            ai_no[n] = ai_no.get(n, 0) + 1
            hit = signpost.search(AL.norm(t["text"])) if signpost else None
            if hit:
                part = f"Part {hit.group(1)}"
                by_part.setdefault(part, 0)
            said = [lid for f, lid in carriers if f.matches(t["text"])]
            if any(f.matches(t["text"]) for f in count_line):
                said.append(f"{part} signpost" if hit else "the count line")
            if said:
                still = sum(1 for _, x in flat[at + 1:] if _is_reply(x))
                points.append({"at": said[0], "session": n, "message": ai_no[n], "still_to_come": still})
        elif _is_reply(t):
            by_part[part] += 1
    return {"by_part": by_part, "replies": sum(by_part.values()), "count_points": points}


def action_report(counts, target):
    """'47 leader actions (the spec's figure: about 50 for the full Deconstruct on a chat platform)'."""
    if not target:
        return f"{counts['actions']} leader actions ({counts['messages']} messages, {counts['screen_actions']} on screen)"
    return (f"{counts['actions']} leader actions ({counts['messages']} messages, {counts['screen_actions']} on screen); "
            f"the spec's figure: about {target['figure']} for {target['journey']}")
