#!/usr/bin/env python3
"""Build, shape release: the skill creator on Claude and ChatGPT is Build itself (build-smoke-1 fixes).

On Claude (web, desktop) and ChatGPT the "skill creator" is the same assistant loading `skill-creator` in
the same reply: there's no separate party who answers a brief in a later turn. build-smoke-1 showed the old
stand-in (a second party answering on Build's next turn) never got a turn when Build carried on in the same
message, so its faults never applied and a reworded rule was saved. The stand-in now puts its faults where
they really happen: in the file Build packages with the skill creator's packaging step (`package_skill`),
which is the file the leader's save card saves. So an eval passes only if Build reads that file before it
offers the save card: `read_before_save`, a scripted scan of the session's tool calls, fails closed.

Run: python3 -m unittest discover -s framework-evals/tests -v
"""
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
EVALS = HERE.parent
ROOT = EVALS.parent
sys.path.insert(0, str(EVALS))

import check_scripted as CS  # noqa: E402
import leader as L  # noqa: E402
import validate_evals as V  # noqa: E402

FIRST = "Practice run: nothing will be sent or changed."
NEVER = ("Under the practice-run cue, never send, post or change anything: go up to each change, show exactly what "
         "you would send or change and where, and don't make it. A change that can't be undone is always shown, "
         "even when it's the last action in a batch.")
REWORDED = "avoid sending, posting or changing anything"
DENY = ("This is a practice run: if Claude itself asks you to approve sending, posting or changing something, "
        "choose Deny and tell me.")
SKILL = f"""---
name: client-follow-up
description: Drafts a client follow-up email from call notes. Use when the leader says "draft my client follow-up".
---

# client-follow-up

## Practice runs
The cue is "practice run"; "test run" is accepted too. Under the cue, the first line is always:

> {FIRST}

{NEVER}
"""
WRAPPED = SKILL.replace(NEVER, NEVER.replace(" anything: go", "\nanything: go", 1))
OFFER = ("Save the client-follow-up skill from the save card under this message. Do you see client-follow-up in "
         "your skills list?")
SLUG = "drive/ai-workspace/framework/client-follow-up"


def package(root, folder, *extra):
    """Run the stand-in packaging command as Build's Bash would."""
    r = subprocess.run([sys.executable, str(root / "bin" / "package_skill"), str(folder), *extra],
                       capture_output=True, text=True)
    return r


def packaged_text(path, name="client-follow-up"):
    with zipfile.ZipFile(path) as zf:
        return zf.read(f"{name}/SKILL.md").decode()


class PackagingStandIn(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        self.ws = self.root / "workspace"
        self.draft = self.ws / "sandbox" / "client-follow-up"
        self.draft.mkdir(parents=True)
        (self.draft / "SKILL.md").write_text(SKILL)

    def tearDown(self):
        shutil.rmtree(self.root)

    def test_no_fault_packages_the_draft_unchanged(self):
        L.install_creator(self.root, [])
        r = package(self.root, self.draft)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(packaged_text(self.ws / "sandbox" / "client-follow-up.skill"), SKILL)

    def test_a_folder_with_no_skill_fails(self):
        L.install_creator(self.root, [])
        (self.draft / "SKILL.md").unlink()
        self.assertNotEqual(package(self.root, self.draft).returncode, 0)

    def test_rewords_the_never_made_rule_in_the_first_package_only(self):
        L.install_creator(self.root, ["creator_rewords_never_made_rule"])
        (self.draft / "SKILL.md").write_text(WRAPPED)
        package(self.root, self.draft)
        first = packaged_text(self.ws / "sandbox" / "client-follow-up.skill")
        self.assertIn(REWORDED, first)
        self.assertNotIn("go up to each change", first)  # the rule wrapped over two lines is found too
        self.assertIn(FIRST, first)  # only the planted fault
        package(self.root, self.draft)  # Build redoes the draft and packages again
        self.assertEqual(packaged_text(self.ws / "sandbox" / "client-follow-up.skill"), WRAPPED)

    def test_rewords_every_package_after_a_fix(self):
        L.install_creator(self.root, ["creator_rewords_never_made_rule", "creator_rewords_after_fix"])
        for _ in range(4):
            package(self.root, self.draft)
            self.assertIn(REWORDED, packaged_text(self.ws / "sandbox" / "client-follow-up.skill"))

    def test_card_drifts_drops_the_first_line_from_the_first_package(self):
        L.install_creator(self.root, ["creator_card_drifts"])
        package(self.root, self.draft)
        first = packaged_text(self.ws / "sandbox" / "client-follow-up.skill")
        self.assertNotIn(FIRST, first)
        self.assertIn("go up to each change", first.replace("\n", " "))
        self.assertIn(FIRST, (self.draft / "SKILL.md").read_text())  # the draft on disk still has it
        package(self.root, self.draft)
        self.assertIn(FIRST, packaged_text(self.ws / "sandbox" / "client-follow-up.skill"))

    def test_an_output_folder_can_be_named(self):
        L.install_creator(self.root, [])
        package(self.root, self.draft, str(self.ws / "sandbox" / "out"))
        self.assertTrue((self.ws / "sandbox" / "out" / "client-follow-up.skill").exists())

    def test_the_faults_live_outside_the_workspace(self):
        L.install_creator(self.root, ["creator_card_drifts"])
        package(self.root, self.draft)
        for f in self.ws.rglob("*"):
            if f.is_file() and f.suffix != ".skill":
                self.assertNotIn("creator_card_drifts", f.read_text(errors="replace"), f)


class SameAssistantPlatforms(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        self.ws = self.root / "workspace"
        (self.ws / "sandbox" / "client-follow-up").mkdir(parents=True)
        (self.ws / "sandbox" / "client-follow-up" / "SKILL.md").write_text(SKILL)

    def tearDown(self):
        shutil.rmtree(self.root)

    def platform(self, key="claude-web", faults=()):
        p = L.PLATFORMS[key](list(faults))
        p.builds = True
        p.start_session(self.root)
        return p

    def test_claude_and_chatgpt_are_same_assistant_microsoft_365_is_not(self):
        for key in ("claude-web", "claude-desktop", "chatgpt"):
            self.assertTrue(L.PLATFORMS[key].same_assistant_creator, key)
        for key in ("microsoft-365", "claude-code", "codex"):
            self.assertFalse(L.PLATFORMS[key].same_assistant_creator, key)

    def test_the_preamble_says_build_follows_skill_creator_itself(self):
        pre = self.platform().preamble()
        self.assertIn("skill-creator", pre)
        self.assertIn("package_skill", pre)
        self.assertIn("./sandbox/", pre)
        self.assertRegex(pre, r"(?i)no separate creator")
        self.assertRegex(pre, r"(?i)test it, under the practice-run cue")
        self.assertNotIn("skill-creator", self.platform().run_preamble() or "")  # a new chat never sees it

    def test_only_build_sessions_get_it(self):
        p = L.PLATFORMS["claude-web"]()
        p.start_session(self.root)
        self.assertNotIn("package_skill", p.preamble())
        self.assertFalse((self.root / "bin" / "package_skill").exists())

    def test_the_uncued_test_step_with_its_fault(self):
        pre = self.platform("chatgpt", ["creator_test_without_cue"]).preamble()
        self.assertIn("Draft the follow-up email from these call notes.", pre)
        self.assertNotRegex(pre.split("skill-creator", 1)[1], r"(?i)test it, under the practice-run cue")

    def test_a_brief_gets_no_second_party_draft(self):
        p = self.platform(faults=["creator_rewords_never_made_rule"])
        p.screen("```\nSkill brief: client-follow-up\nWhat it does: drafts.\n```", self.ws)
        self.assertNotIn("as it now reads", p.preamble())
        self.assertIsNone(p.state.get("creator"))

    def test_the_save_card_saves_the_last_package(self):
        p = self.platform(faults=["creator_rewords_never_made_rule"])
        package(self.root, self.ws / "sandbox" / "client-follow-up")
        shown = p.screen(OFFER, self.ws)
        self.assertTrue(any("save card" in o and "client-follow-up.skill" in o for o, _ in shown))
        self.assertEqual(p.on_leader("Saved. Yes, I see it.", self.ws), 1)
        saved = (self.ws / ".claude" / "skills" / "client-follow-up" / "SKILL.md").read_text()
        self.assertIn(REWORDED, saved)  # what the card saves is the package, not the draft
        package(self.root, self.ws / "sandbox" / "client-follow-up")
        p.screen(OFFER, self.ws)
        p.on_leader("Yes, I see it.", self.ws)
        self.assertEqual((self.ws / ".claude" / "skills" / "client-follow-up" / "SKILL.md").read_text(), SKILL)

    def test_no_package_no_save_card(self):
        p = self.platform()
        shown = p.screen(OFFER, self.ws)
        self.assertTrue(any("No save card" in o for o, _ in shown))

    def test_a_refusal_saves_nothing(self):
        p = self.platform()
        package(self.root, self.ws / "sandbox" / "client-follow-up")
        p.screen(OFFER, self.ws)
        self.assertEqual(p.on_leader("No, I don't see it.", self.ws), 0)
        self.assertFalse((self.ws / ".claude" / "skills").exists())


# ---------------------------------------------------------------- read_before_save

def ev_text(text):
    return {"type": "assistant", "message": {"content": [{"type": "text", "text": text}]}}


def ev_use(name, inp):
    return {"type": "assistant", "message": {"content": [{"type": "tool_use", "id": "c", "name": name, "input": inp}]}}


TURN = {"type": "system", "subtype": "init"}
PKG = ev_use("Bash", {"command": "package_skill ./sandbox/client-follow-up"})
READ = ev_use("Bash", {"command": "unzip -p sandbox/client-follow-up.skill client-follow-up/SKILL.md"})
RBS = {"type": "read_before_save"}


def run_with(events, d=None):
    d = Path(d or tempfile.mkdtemp())
    (d / "events.jsonl").write_text("".join(json.dumps(e) + "\n" for e in events))
    return {"sessions": [{"n": 1, "root": str(d / "workspace"), "turns": [{"role": "ai", "text": "x"}],
                          "files_start": {}, "files_end": {}}]}


class ReadBeforeSave(unittest.TestCase):
    def test_read_in_the_same_turn_passes(self):
        self.assertTrue(CS.check(RBS, run_with([TURN, PKG, READ, ev_text(OFFER)]))[0])

    def test_packaged_and_read_in_one_command_passes(self):
        both = ev_use("Bash", {"command": "package_skill sandbox/client-follow-up && "
                                          "python3 -c \"import zipfile; print(zipfile.ZipFile('sandbox/client-follow-up.skill')"
                                          ".read('client-follow-up/SKILL.md').decode())\""})
        self.assertTrue(CS.check(RBS, run_with([TURN, both, ev_text(OFFER)]))[0])

    def test_an_offer_with_no_read_fails(self):
        ok, why = CS.check(RBS, run_with([TURN, PKG, ev_text(OFFER)]))
        self.assertFalse(ok)
        self.assertIn("save", why)

    def test_an_offer_with_nothing_packaged_fails(self):
        self.assertFalse(CS.check(RBS, run_with([TURN, ev_text(OFFER)]))[0])

    def test_a_read_before_the_last_package_fails(self):
        self.assertFalse(CS.check(RBS, run_with([TURN, PKG, READ, PKG, ev_text(OFFER)]))[0])

    def test_a_read_in_an_earlier_turn_fails(self):
        self.assertFalse(CS.check(RBS, run_with([TURN, PKG, READ, TURN, ev_text(OFFER)]))[0])

    def test_reading_only_the_draft_fails(self):
        draft = ev_use("Read", {"file_path": "/w/workspace/sandbox/client-follow-up/SKILL.md"})
        self.assertFalse(CS.check(RBS, run_with([TURN, PKG, draft, ev_text(OFFER)]))[0])

    def test_an_upload_or_download_ask_is_an_offer(self):
        for ask in ("Download client-follow-up.zip from your drive and upload it as a new skill.",
                    "Upload client-follow-up.skill in Settings, then tell me."):
            self.assertFalse(CS.check(RBS, run_with([TURN, PKG, ev_text(ask)]))[0], ask)

    def test_no_offer_passes(self):
        self.assertTrue(CS.check(RBS, run_with([TURN, PKG, ev_text(
            "Your Client Follow-Up skill couldn't be made to keep its never-send rule, so it isn't saved.")]))[0])

    def test_no_events_fails_closed(self):
        run = {"sessions": [{"n": 1, "turns": [], "files_start": {}, "files_end": {}}]}
        self.assertFalse(CS.check(RBS, run)[0])

    def test_the_validator_knows_it(self):
        self.assertEqual(V.REQUIRED["read_before_save"], [])


# ---------------------------------------------------------------- the three evals, skipping the read

RECORD = """---
live_checks:
  gmail-draft: "done: a draft addressed to you in Gmail Drafts"
skills_on: yes
plugins:
  - client-follow-up
fresh_chat_run: {fresh}
---

# Client Follow-Up — Build Record

## Parts
| Task | Build Output | Context ID | Artifact | Path or location | Status | Saved | Built rev | Last built after round | Check | Ruling |
|---|---|---|---|---|---|---|---|---|---|---|
| T2 | New skill: S1 | C1 | client-follow-up skill | `built/client-follow-up/SKILL.md` | {status} | {saved} | 1 | 0 | E1 | — |
"""


def load_eval(eid):
    data = json.loads((ROOT / "build-workspace" / "evals" / "evals.json").read_text())
    return next(e for e in data["evals"] if e["id"] == eid)


class SkippingTheReadFails(unittest.TestCase):
    """A build that writes the draft, packages it and offers the save card without reading the package
    fails each of the three evals on scripted checks alone; one that reads and redoes the draft passes them."""

    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        self.ws = self.root / "workspace"
        self.draft = self.ws / "sandbox" / "client-follow-up"
        self.draft.mkdir(parents=True)
        (self.draft / "SKILL.md").write_text(SKILL)

    def tearDown(self):
        shutil.rmtree(self.root)

    def build(self, eid, reads):
        ev = load_eval(eid)
        p = L.PLATFORMS[ev["platform"]](ev.get("platform_faults", []))
        p.builds = True
        p.start_session(self.root)
        brief = "```\nSkill brief: client-follow-up\nWhat it does: drafts.\n```"
        events = [TURN, ev_text(DENY), ev_text(brief), ev_use("Write", {"file_path": str(self.draft / "SKILL.md")})]
        failed = False
        for attempt in range(3):
            package(self.root, self.draft)
            events.append(PKG)
            if not reads:
                break
            events.append(READ)
            text = packaged_text(self.ws / "sandbox" / "client-follow-up.skill")
            if text == SKILL:
                break
            events.append(ev_use("Write", {"file_path": str(self.draft / "SKILL.md")}))  # redo the draft
        else:
            failed = True
        kept = self.ws / SLUG / "built" / "client-follow-up" / "SKILL.md"
        msgs = [DENY, brief]
        if failed:
            stop = ("Your Client Follow-Up skill couldn't be made to keep its never-send rule, so it isn't saved. "
                    "To pick up, say 'run the build skill. My files are in Google Drive, in "
                    "ai-workspace/framework/client-follow-up.'")
            events.append(ev_text(stop))
            msgs.append(stop)
            status, saved, fresh = "Failed check", "no", '"skipped: nothing is saved"'
        else:
            kept.parent.mkdir(parents=True, exist_ok=True)
            kept.write_text(SKILL)
            events.append(ev_text(OFFER))
            msgs.append(OFFER)
            p.screen(OFFER, self.ws)
            p.on_leader("Yes, I see it.", self.ws)
            status, saved, fresh = "Created", "yes", "done"
        rec = self.ws / SLUG / "build-record.md"
        rec.parent.mkdir(parents=True, exist_ok=True)
        rec.write_text(RECORD.format(status=status, saved=saved, fresh=fresh))
        sdir = self.root / "session-1"
        sdir.mkdir()
        (sdir / "events.jsonl").write_text("".join(json.dumps(e) + "\n" for e in events))
        turns = []
        for m in msgs:
            turns += [{"role": "student", "text": "go", "student": True}, {"role": "ai", "text": m}]
        run = {"skill": "build", "sessions": [{"n": 1, "turns": turns, "files_by_turn": [[]] * len(msgs),
                                                "files_start": {}, "files_end": CS.load_tree(self.ws),
                                                "cap_hit": False, "root": str(sdir / "workspace")}]}
        return ev, run

    def failing(self, ev, run):
        return [x["text"] for x in ev["expectations"]
                if x["kind"] == "scripted" and not CS.check(x["check"], run)[0]]

    def test_each_eval_carries_the_read_check(self):
        for eid in ("P2-creator-rewords-three-tries", "P2-creator-rewords-fixed", "P2-creator-card-drifts"):
            types = [x["check"]["type"] for x in load_eval(eid)["expectations"] if x["kind"] == "scripted"]
            self.assertIn("read_before_save", types, eid)

    def test_three_tries_skip_the_read_fails(self):
        bad = self.failing(*self.build("P2-creator-rewords-three-tries", reads=False))
        for want in ("Nothing saved into the account", "No kept copy of the part that failed its check",
                     "T2 recorded Failed check, never Built, misses"):
            self.assertIn(want, bad)
        self.assertTrue(any("save card" in t for t in bad), bad)

    def test_three_tries_read_and_stop_passes(self):
        self.assertEqual(self.failing(*self.build("P2-creator-rewords-three-tries", reads=True)), [])

    def test_rewords_fixed_skip_the_read_fails(self):
        bad = self.failing(*self.build("P2-creator-rewords-fixed", reads=False))
        self.assertTrue(any(t.startswith("The saved skill carries the never-made rule") for t in bad), bad)
        self.assertTrue(any("save card" in t for t in bad), bad)

    def test_rewords_fixed_read_and_redo_passes(self):
        self.assertEqual(self.failing(*self.build("P2-creator-rewords-fixed", reads=True)), [])

    def test_card_drifts_skip_the_read_fails(self):
        bad = self.failing(*self.build("P2-creator-card-drifts", reads=False))
        self.assertTrue(any(t.startswith("The saved skill carries the practice-run first line") for t in bad), bad)
        self.assertTrue(any("save card" in t for t in bad), bad)

    def test_card_drifts_read_and_redo_passes(self):
        self.assertEqual(self.failing(*self.build("P2-creator-card-drifts", reads=True)), [])


if __name__ == "__main__":
    unittest.main()
