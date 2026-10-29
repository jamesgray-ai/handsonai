#!/usr/bin/env python3
"""What the rubric judge sees beside the messages: the routing script's verdict, the loaded skill
text, and a proper name's line in the leader's files (core round 2026-10-28, Design).

No model is called. Run: python3 -m unittest discover -s framework-evals/tests -v
"""
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import grade_eval as G  # noqa: E402

STATE_OUT = ('client-follow-up: state 10 (Ready to go live), Test: "test the workflow I built". '
             'Because round 1 is ready for plan revision 1, with go_live: pending.\n'
             + json.dumps({"workflow": "client-follow-up", "state": 10,
                           "facts": {"workflow": "client-follow-up",
                                     "files": {"requirements.md": True, "deconstruct-in-progress.md": False,
                                               "test-results.md": True}}}))


def run_with(events, files=None, text="x"):
    t = tempfile.mkdtemp()
    Path(t, "events.jsonl").write_text("".join(json.dumps(e) + "\n" for e in events))
    return {"sessions": [{"root": str(Path(t, "workspace")), "files_start": files or {},
                          "turns": [{"role": "ai", "text": text}]}]}


def tool_result(text):
    return {"type": "user", "message": {"content": [{"type": "tool_result", "content": text}]}}


class JudgeContext(unittest.TestCase):
    def test_routing_verdict_and_files_found(self):
        run = run_with([tool_result(STATE_OUT)])
        out = G.state_lines(run)
        self.assertIn("state 10 (Ready to go live)", out)
        self.assertIn("files found: requirements.md, test-results.md", out)
        self.assertNotIn("deconstruct-in-progress.md", out)

    def test_no_state_lines_without_the_script(self):
        self.assertEqual(G.state_lines(run_with([tool_result("ls: framework")])), "")

    def test_loaded_skill_text_is_shown_as_the_steps_instructions(self):
        skill = {"type": "user", "message": {"content": [{"type": "text", "text":
                 "Base directory for this skill: /x\n\nThe leader runs it once by hand before its schedule goes on."}]}}
        msg = "Build gets the schedule ready; the leader runs it once by hand before its schedule goes on."
        run = run_with([skill], text=msg)
        # the rule is shown, labelled as the step's own instructions, never as tool output
        self.assertIn("runs it once by hand before its schedule goes on", G.skill_passages(run, [msg]))
        self.assertEqual(G.shared_lines(run, [msg]), "")
        _, prompt = G.rubric_prompt(run)
        self.assertIn("The step's own instructions", prompt)
        self.assertIn("never a source for a fact about the leader's work", prompt)
        self.assertNotIn("Lines the AI's own tool calls printed", prompt)

    def test_an_example_figure_in_the_skill_text_is_never_a_tool_line(self):
        # 9620e646b put skill text among the tool results, so its example figures reached the judge
        # as tool output: an echoed "within 48 hours" with no leader source passed "Nothing invented"
        skill = {"type": "user", "message": {"content": [{"type": "text", "text":
                 "Base directory for this skill: /x\n\nExample: the leader sends a follow-up within 48 hours "
                 "of each call (120 min).\nAsk what the leader does after each call."}]}}
        msg = "So you send each client a follow-up within 48 hours of each call, about 120 min each. Is that right?"
        run = run_with([skill], text=msg)
        self.assertEqual(G.tool_lines(run, [msg]), "")
        self.assertEqual(G.shared_lines(run, [msg]), "")
        self.assertEqual(G._tool_results(Path(run["sessions"][0]["root"]).parent / "events.jsonl"), [])
        _, prompt = G.rubric_prompt(run)
        head = prompt.split("## Message 1")[0]
        self.assertNotIn("Lines the AI's own tool calls printed", head)
        # shown only under the label that says it backs nothing about the leader's work
        self.assertIn("never a source for a fact about the leader's work", head)
        self.assertLess(head.index("## The step's own instructions"), head.index("48 hours"))

    def test_the_same_figure_from_a_real_tool_result_still_counts(self):
        msg = "Your notes say you reply within 48 hours of each call, 120 min in all."
        run = run_with([tool_result("C1-call-notes.md: I reply within 48 hours of each call (120 min).")], text=msg)
        self.assertIn("120 min", G.tool_lines(run, [msg]))
        self.assertIn("within 48 hours", G.shared_lines(run, [msg]))

    def test_a_named_thing_said_in_other_words_is_shown(self):
        # the requirements' "from the expense inbox", said as "into the expense inbox": no four-word run
        # is shared, and longer shared lines filled the cap, so the judge never saw the source (RA, SD-n16)
        msg = "It has no email connection, so it never goes into the expense inbox itself."
        filler = [tool_result(f"| P{i} | It has no email connection, so it never goes past rule {i}. |") for i in range(12)]
        src = tool_result("- I1 · the submitted expense report with its receipts · from the expense inbox · Status: available")
        run = run_with(filler + [src], text=msg)
        self.assertIn("from the expense inbox", G.shared_lines(run, [msg]))

    def test_a_noun_run_from_the_skill_text_is_still_never_a_tool_line(self):
        skill = {"type": "user", "message": {"content": [{"type": "text", "text":
                 "Base directory for this skill: /x\n\nExample: reports arrive in the expense inbox."}]}}
        msg = "It never goes into the expense inbox itself."
        self.assertEqual(G.shared_lines(run_with([skill], text=msg), [msg]), "")

    def test_a_name_from_the_leaders_files_is_shown_with_its_path(self):
        files = {"framework/x/inputs/E2-no-next-step.md": "source: deconstruct\n\nCall with Lee Park (Northwind)."}
        msg = "Here's the plan. On the Northwind notes, it asks you for a next step."
        run = run_with([], files=files, text=msg)
        self.assertIn("framework/x/inputs/E2-no-next-step.md: Call with Lee Park (Northwind).", G.name_lines(run, [msg]))

    def test_a_name_the_skill_holds_or_no_file_holds_is_not_shown(self):
        skill = {"type": "user", "message": {"content": [{"type": "text", "text":
                 "Base directory for this skill: /x\n\nIt drafts in Gmail."}]}}
        files = {"framework/x/requirements.md": "W1 · Gmail · create a draft"}
        msg = "It saves a draft in Gmail for Harbour to read."
        self.assertEqual(G.name_lines(run_with([skill], files=files, text=msg), [msg]), "")


REF = "/tmp/handsonai-evals/tmpab12/plugin/skills/design/references/updating-the-plan.md"
WS = "/tmp/handsonai-evals/tmpab12/workspace/framework/x/C1-call-notes.md"


def call_and_result(i, name, inp, text):
    return [{"type": "assistant", "message": {"content": [{"type": "tool_use", "id": f"c{i}", "name": name, "input": inp}]}},
            {"type": "user", "message": {"content": [{"type": "tool_result", "tool_use_id": f"c{i}", "content": text}]}}]


class PluginTextIsInstructions(unittest.TestCase):
    """A plugin reference file the AI reads is the step's own text, as SKILL.md is: its example figures
    never reach the judge as tool output."""
    MSG = "So you send each client a follow-up within 48 hours of each call, about 120 min a week. Right?"
    EXAMPLE = "     1\tExample: the leader sends a follow-up within 48 hours of each call (120 min a week).\n"

    def check_not_credited(self, events):
        run = run_with(events, text=self.MSG)
        self.assertEqual(G.tool_lines(run, [self.MSG]), "")
        self.assertEqual(G.shared_lines(run, [self.MSG]), "")
        self.assertIn("within 48 hours", G.skill_passages(run, [self.MSG]))
        head = G.rubric_prompt(run)[1].split("## Message 1")[0]
        self.assertNotIn("Lines the AI's own tool calls printed", head)
        self.assertLess(head.index("## The step's own instructions"), head.index("48 hours"))

    def test_read_of_a_reference_file(self):
        self.check_not_credited(call_and_result(1, "Read", {"file_path": REF}, self.EXAMPLE))

    def test_cat_or_grep_of_a_reference_file(self):
        self.check_not_credited(call_and_result(1, "Bash", {"command": f"cat {REF} | head -40"}, self.EXAMPLE[7:]))
        self.check_not_credited(call_and_result(1, "Grep", {"pattern": "48", "path": REF}, self.EXAMPLE[7:]))

    def test_the_leaders_file_and_the_routing_script_stay_tool_output(self):
        run = run_with(call_and_result(1, "Read", {"file_path": WS}, self.EXAMPLE), text=self.MSG)
        self.assertIn("within 48 hours", G.shared_lines(run, [self.MSG]))
        script = "python3 /tmp/handsonai-evals/tmpab12/plugin/scripts/framework-state.py framework/client-follow-up"
        run = run_with(call_and_result(1, "Bash", {"command": script}, STATE_OUT))
        self.assertIn("state 10 (Ready to go live)", G.state_lines(run))


class AIWrittenFilesMarked(unittest.TestCase):
    """files_read: a file the AI wrote in an earlier session is shown marked as the AI's, never as the
    leader's (it used to be shown under "the leader's files" like any other)."""

    def run2(self, s1_files, s2_files, fixture2=False):
        t = tempfile.mkdtemp()
        sess = []
        for n, files in ((1, s1_files), (2, s2_files)):
            d = Path(t, f"s{n}")
            d.mkdir()
            res = "\n".join(files.values())
            Path(d, "events.jsonl").write_text(json.dumps(tool_result(res)) + "\n")
            sess.append({"n": n, "root": str(d / "workspace"), "files_start": files, "files_end": files,
                         "fixture": n == 1 or fixture2, "turns": [{"role": "ai", "text": "x"}]})
        return {"sessions": sess}

    BROUGHT = {"framework/x/C1-call-notes.md": "Call with Lee Park of Northwind about the renewal terms.\nThey want the pricing sheet by Friday at noon."}
    AI = {"framework/x/requirements.md": "Baseline: the leader spends 45 minutes on each follow-up email.\nTarget: a draft ready within ten minutes of each call."}

    def test_an_earlier_ai_written_file_is_marked(self):
        out = G.files_read(self.run2(self.BROUGHT, dict(self.BROUGHT, **self.AI)), ["x"])
        head = next(ln for ln in out.splitlines() if "requirements.md" in ln)
        self.assertIn("WRITTEN BY THE AI", head)
        notes = next(ln for ln in out.splitlines() if "C1-call-notes.md" in ln)
        self.assertNotIn("WRITTEN BY THE AI", notes)

    def test_a_file_the_leader_brought_is_not_marked(self):
        out = G.files_read(self.run2(dict(self.BROUGHT, **self.AI), dict(self.BROUGHT, **self.AI)), ["x"])
        self.assertNotIn("WRITTEN BY THE AI", out)
        out = G.files_read(self.run2(self.BROUGHT, dict(self.BROUGHT, **self.AI), fixture2=True), ["x"])
        self.assertNotIn("WRITTEN BY THE AI", out)


class NameLinesLeaderFilesOnly(unittest.TestCase):
    """name_lines reads the files the leader brought, never a later session's start tree, which holds
    what the AI wrote in an earlier session (31b7210dc read every session's)."""

    def two_sessions(self, first, second, marks=True):
        t = tempfile.mkdtemp()
        sess = []
        for n, files in ((1, first), (2, second)):
            d = Path(t, f"s{n}")
            d.mkdir()
            Path(d, "events.jsonl").write_text("")
            s = {"n": n, "root": str(d / "workspace"), "files_start": files,
                 "turns": [{"role": "ai", "text": "x"}]}
            if marks:
                s["fixture"] = n == 1
            sess.append(s)
        return {"sessions": sess}

    def test_a_name_only_the_ai_wrote_in_session_1_is_not_shown(self):
        msg = "On the Northwind notes, it asks you for a next step."
        ai_wrote = {"framework/x/requirements.md": "Example input: call notes from Northwind."}
        for marks in (True, False):  # a run saved before the marks counts its first session only
            run = self.two_sessions({}, ai_wrote, marks)
            self.assertEqual(G.name_lines(run, [msg]), "")

    def test_a_name_the_leader_brought_is_shown(self):
        msg = "On the Northwind notes, it asks you for a next step."
        brought = {"framework/x/inputs/E2.md": "Call with Lee Park (Northwind)."}
        run = self.two_sessions(brought, dict(brought, **{"framework/x/design-plan.md": "Northwind plan"}))
        self.assertEqual(G.name_lines(run, [msg]), "framework/x/inputs/E2.md: Call with Lee Park (Northwind).")

    def test_a_later_session_from_its_own_fixture_counts(self):
        msg = "On the Northwind notes, it asks you for a next step."
        run = self.two_sessions({}, {"framework/x/inputs/E2.md": "Northwind call."})
        run["sessions"][1]["fixture"] = True
        self.assertIn("Northwind call.", G.name_lines(run, [msg]))


if __name__ == "__main__":
    unittest.main()
