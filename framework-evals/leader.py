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

  claude-code     files in the workspace (the real platform; no preamble)
  codex           files in the workspace; Codex's wording and its read-only bare-run command
  claude-web      Google Drive (./drive/Framework); paste-back from new chats
  claude-desktop  a local folder added to the chat (./Framework); faults: no_folder_added
  chatgpt         Google Drive (./drive/Framework); apps; paste-back from new chats
  microsoft-365   OneDrive (./onedrive/Framework), read from the location with nothing attached;
                  Cowork's folder ./onedrive/Documents/Cowork; Agent Builder from a pasted build
                  prompt. Faults: cowork_cannot_read_onedrive (the attach fallback; with
                  attach_fails, the admin line), agent_builder_missing_context_file,
                  agent_builder_rewords_carried_line, agent_builder_requirements_under_knowledge,
                  agent_builder_ordinary_chat, skill_cannot_read_by_path

The leader-action counter (`count_actions`) reports leader actions per run (each message the leader
sends, plus each action a simulation counts on the leader's screen: opening a chat, pasting, adding
a file under Knowledge, choosing Create) against the spec's journey figures. It never measures time.
"""
import re
import shutil
from pathlib import Path

import approved_lines as AL

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

class Platform:
    key = "claude-code"
    name = "Claude Code"
    files_root = ""           # where the framework folder lives, relative to the workspace
    location = "framework/[workflow-slug]"
    paste_back = False

    def __init__(self, faults=()):
        self.faults = set(faults)
        self.state = {}

    def preamble(self):
        return None

    def leader_notes(self):
        return ""

    def prepare(self, ws):
        """Lay the workspace out the way this platform keeps the leader's files."""

    def on_leader(self, msg, ws):
        """React to what the leader typed (an attach, say). Returns platform actions to count."""
        return 0

    def screen(self, ai_text, ws, run_chat=None):
        """What the leader's screen shows after this AI message: [(observation, actions)]."""
        out = []
        if self.paste_back and run_chat is not None:
            block = handover_block(ai_text)
            if block:
                answer = run_chat(block, self)
                out.append((f"[You opened a new chat and pasted the block. It answered:]\n{answer}", 3))
        return out


def _move_into(ws, sub):
    """Move the workspace's framework files under ws/sub/Framework (a drive or a named folder)."""
    target = Path(ws) / sub / "Framework" if sub else Path(ws) / "Framework"
    target.mkdir(parents=True, exist_ok=True)
    for name in ("framework", "registry"):
        src = Path(ws) / name
        if src.exists():
            dst = target if name == "framework" else target / "registry"
            if name == "framework":
                for child in src.iterdir():
                    shutil.move(str(child), str(dst / child.name))
                src.rmdir()
            else:
                shutil.move(str(src), str(dst))
    for f in ("REGISTRY.md", "backlog.md", "ai-opportunity-report.md", "analyze-in-progress.md"):
        if (Path(ws) / f).exists():
            shutil.move(str(Path(ws) / f), str(target / f))
    return target


class ClaudeCode(Platform):
    pass


class Codex(Platform):
    key, name = "codex", "Codex"

    def preamble(self):
        return ("Simulated platform: you are running as Codex (the CLI) in this workspace, not Claude Code. "
                "Name the platform as Codex wherever you'd name it, use Codex's own steps, and say 'a new session' "
                "for a new chat. The framework folder is framework/ in this workspace.")


class _Drive(Platform):
    files_root = "drive"
    location = "Google Drive, in Framework/[workflow-slug]"
    paste_back = True
    product = ""

    def preamble(self):
        return (f"Simulated platform: {self.product}, in a chat outside any Project. The leader's Google Drive "
                "connection is on and can write; in this simulation the drive's files are the folder ./drive in your "
                "working folder (./drive/Framework is 'Google Drive, in Framework'). Read and save the leader's files "
                "only through it. You have no terminal of your own for the leader's work and no local folder: anything "
                "the leader must run in a new chat, give them to paste, and they paste back what it says.")

    def prepare(self, ws):
        _move_into(ws, "drive")


class ClaudeWeb(_Drive):
    key, name, product = "claude-web", "Claude on the web", "Claude on the web (claude.ai)"


class ChatGPT(_Drive):
    key, name, product = "chatgpt", "ChatGPT", "ChatGPT (Plus), where connections are called apps"


class ClaudeDesktop(Platform):
    key, name = "claude-desktop", "Claude desktop"
    location = "Framework/[workflow-slug]"
    paste_back = True

    def preamble(self):
        return ("Simulated platform: Claude desktop, with the leader's framework folder added to this chat; in this "
                "simulation it is ./Framework in your working folder. If ./Framework isn't there, no folder is added "
                "to this chat. Anything the leader must run in a new chat, give them to paste, and they paste back.")

    def prepare(self, ws):
        target = _move_into(ws, "")
        if "no_folder_added" in self.faults:
            hidden = Path(ws).parent / ".sim-hidden" / "Framework"
            hidden.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(target), str(hidden))
            self.state["hidden"] = hidden

    def on_leader(self, msg, ws):
        if self.state.get("hidden") and re.search(r"\bdone\b", msg, re.I):
            shutil.move(str(self.state.pop("hidden")), str(Path(ws) / "Framework"))
            return 1
        return 0

    def leader_notes(self):
        if "no_folder_added" in self.faults:
            return "\nYour screen: you started this chat without adding your framework folder. When asked, add it and say 'done'."
        return ""


class Microsoft365(Platform):
    key, name = "microsoft-365", "Microsoft 365 Copilot Cowork"
    files_root = "onedrive"
    location = "OneDrive, in Framework/[workflow-slug]"
    paste_back = True

    def preamble(self):
        p = ("Simulated platform: Microsoft 365 Copilot Cowork, in a new Cowork chat. Cowork reads and writes the "
             "leader's OneDrive; in this simulation OneDrive is ./onedrive in your working folder "
             "(./onedrive/Framework is 'OneDrive, in Framework', and Cowork's own folder is "
             "./onedrive/Documents/Cowork). Read the framework files from the location with nothing attached. "
             "Agents are made by the leader in Copilot's Agent Builder, not here. Anything the leader must run in a "
             "new chat, give them to paste, and they paste back what it says.")
        if "skill_cannot_read_by_path" in self.faults:
            p += " In this tenant a Cowork skill can't read a file by its path."
        return p

    def prepare(self, ws):
        target = _move_into(ws, "onedrive")
        (Path(ws) / "onedrive" / "Documents" / "Cowork").mkdir(parents=True, exist_ok=True)
        if "cowork_cannot_read_onedrive" in self.faults:
            hidden = Path(ws).parent / ".sim-hidden" / "Framework"
            hidden.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(target), str(hidden))
            self.state["hidden"] = hidden

    def on_leader(self, msg, ws):
        if self.state.get("hidden") and re.search(r"\bdone\b", msg, re.I) and "attach_fails" not in self.faults:
            shutil.move(str(self.state.pop("hidden")), str(Path(ws) / "onedrive" / "Framework"))
            return 1
        return 0

    def screen(self, ai_text, ws, run_chat=None):
        out = []
        from check_scripted import find_prompt  # late: check_scripted imports nothing from here
        build = find_prompt(ai_text, "build")
        fix = find_prompt(ai_text, "fix")
        if build:
            out.append(self.agent_builder_create(build))
        elif fix:
            out.append(self.agent_builder_fix(fix))
        else:
            out += Platform.screen(self, ai_text, ws, run_chat)
        return out

    # -- Agent Builder
    def agent_builder_create(self, prompt):
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
            knowledge.append("Framework/requirements.md")
        instructions = self._instructions(prompt)
        self.state["instructions"] = instructions
        self.state["knowledge"] = knowledge
        shown = "\n".join(notes + [f"Knowledge lists: {', '.join(Path(k).name for k in knowledge) or 'nothing'}.",
                                   "Work content: nothing switched on.",
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

    def _instructions(self, prompt):
        low = prompt.lower()
        lines = prompt[low.find("word for word:") + len("word for word:"):] if "word for word:" in low else ""
        body = ["You draft this workflow's deliverable from the plan's task. Read only your Knowledge.", lines.strip()]
        text = "\n".join(b for b in body if b)
        if "agent_builder_rewords_carried_line" in self.faults:
            text = text.replace("Practice run: nothing will be sent or changed.",
                                _reworded("Practice run: nothing will be sent or changed."))
        return text


def _reworded(line):
    return line.replace("changed.", "modified.") if line.endswith("changed.") else line + " (paraphrased)"


PLATFORMS = {c.key: c for c in (ClaudeCode, Codex, ClaudeWeb, ClaudeDesktop, ChatGPT, Microsoft365)}


def platform_for(ev, session=None):
    key = (session or {}).get("platform", ev.get("platform", "claude-code"))
    if key not in PLATFORMS:
        raise ValueError(f"unknown platform {key!r}: one of {sorted(PLATFORMS)}")
    return PLATFORMS[key](ev.get("platform_faults", []))


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


def action_report(counts, target):
    """'47 leader actions (the spec's figure: about 50 for the full Deconstruct on a chat platform)'."""
    if not target:
        return f"{counts['actions']} leader actions ({counts['messages']} messages, {counts['screen_actions']} on screen)"
    return (f"{counts['actions']} leader actions ({counts['messages']} messages, {counts['screen_actions']} on screen); "
            f"the spec's figure: about {target['figure']} for {target['journey']}")
