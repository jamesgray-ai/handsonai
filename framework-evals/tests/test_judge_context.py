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

    def test_loaded_skill_text_counts_as_a_tool_passage(self):
        skill = {"type": "user", "message": {"content": [{"type": "text", "text":
                 "Base directory for this skill: /x\n\nThe leader runs it once by hand before its schedule goes on."}]}}
        msg = "Build gets the schedule ready; the leader runs it once by hand before its schedule goes on."
        run = run_with([skill], text=msg)
        self.assertIn("runs it once by hand before its schedule goes on", G.shared_lines(run, [msg]))

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


if __name__ == "__main__":
    unittest.main()
