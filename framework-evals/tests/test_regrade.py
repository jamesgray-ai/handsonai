#!/usr/bin/env python3
"""regrade.py: a finished round re-graded from what it kept, without re-running any session.

No model is called (--scripted-only). Run: python3 -m unittest discover -s framework-evals/tests -v
"""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
import regrade as R  # noqa: E402

PLAN_ABS = "/tmp/run/workspace/framework/x/design-plan.md"
EV = {"id": "E1", "prompt": "Run the design skill.", "fixture": "empty",
      "expectations": [
          {"text": "plan approved", "kind": "scripted",
           "check": {"type": "file_regex", "path": "framework/x/design-plan.md", "pattern": "^approved: true$"}},
          {"text": "reset first", "kind": "scripted",
           "check": {"type": "tool_write", "path": "framework/x/design-plan.md",
                     "pattern": "^approved: false$", "before": "approved: true"}},
          {"text": "a file during", "kind": "scripted",
           "check": {"type": "file_existed_during", "path": "framework/x/*"}},
          {"text": "judged thing", "kind": "judged"}]}


def tool_use(i, name, inp):
    return {"type": "assistant", "message": {"content": [{"type": "tool_use", "id": f"t{i}", "name": name, "input": inp}]}}


def make_round(events, plan="approved: true\n"):
    t = Path(tempfile.mkdtemp())
    (t / "evals.json").write_text(json.dumps({"skill_name": "design", "builtin_checks": [], "judge_rubric": False,
                                              "evals": [EV]}))
    rd = t / "round" / "E1" / "run-1"
    s1 = rd / "session-1"
    (s1 / "changes" / "framework" / "x").mkdir(parents=True)
    (s1 / "changes" / "framework" / "x" / "design-plan.md").write_text(plan)
    (s1 / "turns.json").write_text(json.dumps([{"role": "student", "text": "go", "prompt": True},
                                               {"role": "ai", "text": "Approved."}]))
    (s1 / "transcript.md").write_text("## AI\n\nApproved.\n")
    (s1 / "events.jsonl").write_text("".join(json.dumps(e) + "\n" for e in events))
    (rd / "eval.json").write_text(json.dumps(EV))
    old_s = [{"text": "plan approved", "kind": "scripted", "passed": True, "evidence": "x"},
             {"text": "a file during", "kind": "scripted", "passed": True, "evidence": "after AI turn 1"}]
    (rd / "scripted.json").write_text(json.dumps(old_s))
    (rd / "grading.json").write_text(json.dumps({"expectations": [
        {"text": "judged thing", "kind": "judged", "passed": True, "evidence": "y"}]}))
    (rd / "result.json").write_text(json.dumps({"eval": "E1", "run": 1, "tier": "regression", "status": "valid",
                                                "passed": 3, "total": 3, "expectations": old_s}))
    return t


def regrade(t, *extra):
    return subprocess.run([sys.executable, str(HERE / "regrade.py"), str(t / "round"), "--evals",
                           str(t / "evals.json"), "--scripted-only", *extra], capture_output=True, text=True)


class Regrade(unittest.TestCase):
    def test_writes_beside_the_old_and_never_over_it(self):
        t = make_round([tool_use(1, "Edit", {"file_path": PLAN_ABS, "old_string": "approved: true", "new_string": "approved: false"}),
                        tool_use(2, "Edit", {"file_path": PLAN_ABS, "old_string": "approved: false", "new_string": "approved: true"})])
        rd = t / "round" / "E1" / "run-1"
        before = {p.name: p.read_text() for p in rd.glob("*.json")}
        r = regrade(t)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual({p.name: p.read_text() for p in rd.glob("*.json") if p.name in before}, before)
        new = {x["text"]: x for x in json.loads((rd / "scripted-v2.json").read_text())}
        self.assertTrue(new["plan approved"]["passed"])     # end tree = start tree + changes/
        self.assertTrue(new["reset first"]["passed"])       # the session's events.jsonl is read
        self.assertTrue(new["a file during"]["carried"])    # per-turn file lists aren't kept
        res = json.loads((rd / "result-v2.json").read_text())
        self.assertTrue(res["regrade"]["judged_carried"])
        self.assertTrue((t / "round" / "summary-v2.md").exists())
        self.assertNotEqual(regrade(t).returncode, 0)        # a used tag is refused
        self.assertEqual(regrade(t, "--tag", "v3").returncode, 0)

    def test_no_reset_fails_on_regrade(self):
        t = make_round([tool_use(1, "Bash", {"command": f"sed -i '' 's/^approved: false$/approved: true/' {PLAN_ABS}"})])
        self.assertEqual(regrade(t).returncode, 0)
        new = {x["text"]: x for x in json.loads((t / "round" / "E1" / "run-1" / "scripted-v2.json").read_text())}
        self.assertFalse(new["reset first"]["passed"])

    def test_a_changed_eval_is_skipped_not_regraded(self):
        t = make_round([])
        data = json.loads((t / "evals.json").read_text())
        data["evals"][0]["prompt"] = "Run the design skill. My files are in framework/x."
        (t / "evals.json").write_text(json.dumps(data))
        r = regrade(t)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("prompt changed since the round", r.stdout)
        self.assertFalse((t / "round" / "E1" / "run-1" / "scripted-v2.json").exists())

    def test_a_fixture_that_changed_under_its_name_is_caught(self):
        start = {"framework/x/requirements.md": "# Req\nStep 1 · draft\n"}
        events = [tool_use(1, "Read", {"file_path": "/r/workspace/framework/x/requirements.md"}),
                  {"type": "user", "message": {"content": [{"type": "tool_result", "tool_use_id": "t1",
                                                            "content": "     1\t# Req\n     2\tStep 1 · send\n"}]}}]
        p = Path(tempfile.mkdtemp(), "events.jsonl")
        p.write_text("".join(json.dumps(e) + "\n" for e in events))
        self.assertEqual(R.fixture_drift(start, p), ["framework/x/requirements.md"])
        self.assertEqual(R.fixture_drift({"framework/x/requirements.md": "# Req\nStep 1 · send\n"}, p), [])

    def test_a_fixture_read_with_cat_is_caught_too(self):
        start = {"framework/x/requirements.md": "# Req\nStep 1 · draft\n"}
        events = [tool_use(1, "Bash", {"command": "cd /r/workspace/framework/x && cat requirements.md"}),
                  {"type": "user", "message": {"content": [{"type": "tool_result", "tool_use_id": "t1",
                                                            "content": "# Req\nStep 1 · send\n"}]}}]
        p = Path(tempfile.mkdtemp(), "events.jsonl")
        p.write_text("".join(json.dumps(e) + "\n" for e in events))
        self.assertEqual(R.fixture_drift(start, p), ["framework/x/requirements.md"])
        self.assertEqual(R.fixture_drift({"framework/x/requirements.md": "# Req\nStep 1 · send\n"}, p), [])

    def test_recorded_start_hashes_are_exact(self):
        start = {"framework/x/requirements.md": "a\n", "framework/x/notes.md": "never read\n"}
        rec = R.start_hashes(start)
        nowhere = Path(tempfile.mkdtemp(), "events.jsonl")  # no events: only the hashes can tell
        self.assertEqual(R.fixture_drift(start, nowhere, rec), [])
        self.assertEqual(R.fixture_drift(dict(start, **{"framework/x/notes.md": "changed\n"}), nowhere, rec),
                         ["framework/x/notes.md"])
        self.assertEqual(R.fixture_drift(dict(start, **{"framework/x/new.md": "x"}), nowhere, rec), ["framework/x/new.md"])


if __name__ == "__main__":
    unittest.main()
