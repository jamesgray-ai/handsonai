#!/usr/bin/env python3
"""leader.py's platform simulation for Analyze 3.1's evidence pass: the working folder's documents move
with the framework files, and the files a fixture plants (typed requests, unasked platform content) are
taken before the session starts and never left in the workspace.

No model is called. Run: python3 -m unittest discover -s framework-evals/tests -v
"""
import json
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))
import leader as L  # noqa: E402


def run_root():
    root = Path(tempfile.mkdtemp())
    ws = root / "workspace"
    (ws / "registry").mkdir(parents=True)
    (ws / "registry" / "SCHEMA.md").write_text("# schema\n")
    (ws / "knowledge").mkdir()
    (ws / "knowledge" / "note.md").write_text("# a note\n")
    (ws / "sops" / "client-work").mkdir(parents=True)
    (ws / "sops" / "client-work" / "sop.md").write_text("# an SOP\n")
    (ws / "process-guides").mkdir()
    (ws / "process-guides" / "guide.md").write_text("# a guide\n")
    home = root / "home" / ".claude"
    home.mkdir(parents=True)
    (home / "history.jsonl").write_text(json.dumps({"display": "marker", "project": "x", "timestamp": 1}) + "\n")
    return root, ws


class Planted(unittest.TestCase):
    def test_drive_moves_the_evidence_documents_into_the_working_folder(self):
        root, ws = run_root()
        L.PLATFORMS["claude-web"]().prepare(ws)
        wf = ws / "drive" / "ai-workspace"
        for rel in ("knowledge/note.md", "sops/client-work/sop.md", "process-guides/guide.md", "registry/SCHEMA.md"):
            self.assertTrue((wf / rel).exists(), rel)
        for d in ("knowledge", "sops", "process-guides"):
            self.assertFalse((ws / d).exists(), d)

    def test_typed_requests_join_the_temp_home_history(self):
        root, ws = run_root()
        (ws / L.PLANTED_HISTORY).write_text(json.dumps({"display": "draft the renewal email", "project": "WORKSPACE",
                                                        "timestamp": 2}) + "\n")
        L.PLATFORMS["claude-code"]().prepare(ws)
        lines = [json.loads(x) for x in (root / "home" / ".claude" / "history.jsonl").read_text().splitlines()]
        self.assertEqual([x["display"] for x in lines], ["marker", "draft the renewal email"])
        self.assertEqual(lines[1]["project"], str(ws))
        self.assertFalse((ws / L.PLANTED_HISTORY).exists())

    def test_grounding_reaches_the_preamble_never_the_workspace(self):
        root, ws = run_root()
        (ws / L.PLANTED_GROUNDING).write_text("Email from a client: send the pricing.\n")
        p = L.PLATFORMS["microsoft-365"]()
        p.prepare(ws)
        self.assertIn("Email from a client: send the pricing.", p.preamble())
        self.assertIn("without the leader or the skill asking", p.preamble())
        self.assertFalse(any(x.name == L.PLANTED_GROUNDING for x in ws.rglob("*")))

    def test_no_planted_files_leaves_the_preamble_as_it_was(self):
        root, ws = run_root()
        p = L.PLATFORMS["claude-code"]()
        p.prepare(ws)
        self.assertIsNone(p.preamble())
        self.assertNotIn("without the leader", L.PLATFORMS["codex"]().preamble())


if __name__ == "__main__":
    unittest.main()
