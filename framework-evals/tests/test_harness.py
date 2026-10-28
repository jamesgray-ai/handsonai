#!/usr/bin/env python3
"""The harness's own tests (T18's "done when"): each check catches a planted failure; the quote check
fails a transcript with one word of a scripted line changed; a run with an extra plugin or connector
fails its init assertion; the runner reports per tier; an existing Deconstruct eval validates.

No model is ever called and ~/.claude is never read or written: model calls go to a stub binary
(stub_claude.py), the keychain token is a fake, and the real-config paths point at a fake home.

Run: python3 -m unittest discover -s framework-evals/tests -v
"""
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

HERE = Path(__file__).resolve().parent
EVALS = HERE.parent
ROOT = EVALS.parent
sys.path.insert(0, str(EVALS))

import approved_lines as AL  # noqa: E402
import check_quotes as CQ  # noqa: E402
import check_scripted as CS  # noqa: E402
import harness as H  # noqa: E402
import leader as L  # noqa: E402
import structure as ST  # noqa: E402
import validate_evals as V  # noqa: E402

FIX = ROOT / "framework-fixtures" / "states" / "s11-live" / "with-registry" / "framework" / "client-follow-up"
N_D1 = "Do you have anything written down for this: an SOP, a checklist, a past example, or notes?"


def run_of(*ai_messages, files_end=None, files_start=None, root=None):
    turns = []
    for m in ai_messages:
        turns += [{"role": "student", "text": "go", "student": True}, {"role": "ai", "text": m}]
    return {"sessions": [{"n": 1, "turns": turns, "files_by_turn": [[]] * len(ai_messages),
                          "files_start": files_start or {}, "files_end": files_end or {}, "cap_hit": False,
                          "root": root}]}


def ok(c, run):
    return CS.check(c, run)[0]


class QuoteCheck(unittest.TestCase):
    def test_platform_refuse_label_fills_n_f4(self):
        # 3c-DW: Copilot Cowork's refuse button is "Cancel"; N-F4 names it there
        c = AL.Corpus()
        m = ("This is a practice run: if Copilot itself asks you to approve sending, posting or changing something, "
             "choose Cancel and tell me. Answer the workflow's own questions as you would at work.")
        self.assertEqual(c.near_misses(m), [])
        self.assertTrue(any(ln.id == "N-F4" and ln.matches(m) for ln in c.checkable()))

    def test_exact_line_passes_and_one_word_changed_fails(self):
        good = run_of("Thanks. " + N_D1)
        bad = run_of("Thanks. " + N_D1.replace("past example", "past sample"))
        self.assertTrue(ok({"type": "scripted_lines"}, good))
        passed, why = CS.check({"type": "scripted_lines"}, bad)
        self.assertFalse(passed)
        self.assertIn("N-D1", why)

    def test_option_list_said_with_only_the_options_that_apply(self):
        # N-14's options marked "only where…" are left out where they don't apply, commas and "or" with them
        two = ("Your requirements say it should post the entry, but the wiki connection can't do that. You can make "
               "that change yourself, or have the support lead make that change. I recommend making that change "
               "yourself, because the drafts are yours.")
        one = two.replace(", or have the support lead make that change", "")
        self.assertTrue(ok({"type": "quote", "id": "N-14", "form": "main"}, run_of(two)))
        self.assertTrue(ok({"type": "quote", "id": "N-14", "form": "main"}, run_of(one)))
        self.assertFalse(ok({"type": "quote", "id": "N-14", "form": "main"},
                            run_of(two.replace("the wiki connection can't do that", "the wiki has no connection"))))

    def test_placeholders_are_wildcards(self):
        said = ("Start Design in a new chat with: 'run the design skill. "
                "My files are in Google Drive, in Framework/client-follow-up.'")
        self.assertTrue(ok({"type": "quote", "id": "N-F2", "form": "main"}, run_of(said)))
        self.assertTrue(ok({"type": "scripted_lines"}, run_of(said)))
        wrong = said.replace("in a new chat", "in a fresh chat")
        self.assertFalse(ok({"type": "quote", "id": "N-F2", "form": "main"}, run_of(wrong)))

    def test_label_clause_is_optional(self):
        base = ("To see what the AI does with no instructions, open a new chat in your workflow's Project, "
                "so it has nothing it could send or change with. Paste this, and copy back what it says. Then delete that chat.")
        with_clause = base.replace("Project,", "Project, and before typing, switch off connectors and memory under +,")
        self.assertTrue(ok({"type": "quote", "id": "N-B45", "form": "main"}, run_of(base)))
        self.assertTrue(ok({"type": "quote", "id": "N-B45", "form": "main"}, run_of(with_clause)))

    def test_two_label_clauses_in_one_bracket_are_alternatives(self):
        # N-B27's "[Can be undone: '…' Permanent: '…']": either clause alone is word for word
        head = "Done: here it is in your Gmail Drafts: an empty draft with no recipient. "
        self.assertTrue(ok({"type": "quote", "id": "N-B27"},
                           run_of(head + "I'll offer to undo the check changes together at the end.")))
        self.assertTrue(ok({"type": "quote", "id": "N-B27"}, run_of(head + "That one stays.")))

    def test_fix_signpost_counts_the_parts_it_runs(self):
        # build.md 171: a later entry counts only the parts it runs; "Part 1 of 2 in this fix" is the example
        for said in ("**Part 1 of 3 in this fix — your setup**", "Part 2 of 2 in this fix"):
            self.assertTrue(ok({"type": "scripted_lines", "skill": "build"}, run_of(said)), said)
        self.assertFalse(ok({"type": "scripted_lines", "skill": "build"}, run_of("Part 1 of 3 in the fix")))

    def test_a_block_quoted_paste_back_isnt_the_ais_wording(self):
        # microsoft-365-agent.md: an agent's reworded line is block-quoted as the leader pasted it; the
        # same words in the AI's own sentence, or in a prompt to paste, still fail the quote check
        bad = "Practice run: nothing will be sent or modified."
        quoted = f"Agent Builder changed one line:\n\n> {bad}\n\nThat should be the line every practice run must start with."
        self.assertTrue(ok({"type": "scripted_lines", "skill": "build"}, run_of(quoted)))
        self.assertFalse(ok({"type": "scripted_lines", "skill": "build"}, run_of(f"It says {bad}")))
        self.assertFalse(ok({"type": "scripted_lines", "skill": "build"}, run_of(f"Paste this:\n\n```\n{bad}\n```")))

    def test_cli_transcript_mode_fails_on_one_changed_word(self):
        with tempfile.TemporaryDirectory() as t:
            good, bad = Path(t, "good.md"), Path(t, "bad.md")
            good.write_text(f"## Student\n\nhi\n\n## AI\n\n{N_D1}\n")
            bad.write_text(f"## Student\n\nhi\n\n## AI\n\n{N_D1.replace('checklist', 'list')}\n")
            with redirect_stdout(io.StringIO()):
                self.assertEqual(CQ.main(["transcript", str(good)]), 0)
            out = io.StringIO()
            with redirect_stdout(out):
                self.assertEqual(CQ.main(["transcript", str(bad)]), 1)
            self.assertIn("N-D1", out.getvalue())

    def test_bring_in_line_platform_forms_are_whole_lines(self):
        # lines-to-approve: the bring-in line in N-F2's platform forms ("in a new session" on Claude Code
        # and Codex); the whole line each fragment makes is checkable, and a changed word still fails
        cc = {"type": "quote", "id": "bring-in-line", "form": "Claude Code and Codex, whole line"}
        said = "To bring Client Follow-Up into the framework, start Deconstruct in a new session with: 'run the deconstruct skill on Client Follow-Up. My files are in framework.'"
        self.assertTrue(ok(cc, run_of(said)))
        self.assertFalse(ok({"type": "quote", "id": "bring-in-line", "form": "main"}, run_of(said)))
        self.assertFalse(ok(cc, run_of(said.replace("start Deconstruct", "open Deconstruct"))))
        desk = {"type": "quote", "id": "bring-in-line", "form": "Claude desktop, whole line"}
        self.assertTrue(ok(desk, run_of("To bring Client Follow-Up into the framework, start Deconstruct in a new chat with your framework folder added: 'run the deconstruct skill on Client Follow-Up. My files are in Framework.'")))

    def test_n_b4_leaves_out_an_empty_clause_and_nothing_else(self):
        """build SKILL.md: "A clause with nothing in it is left out." No draft to check: the list closes
        up. A changed OK clause still fails."""
        c = AL.Corpus()
        forms = [ln for ln in c.checkable() if ln.id == "N-B4"]
        said = ("Build makes your workflow for Client Follow-Up from your approved plan, task by task, checking each "
                "part as it goes. First I'll need you to connect Gmail and OK 2 quick real checks and setup changes; "
                "then I build and check the rest, and I'll ask you to confirm about 4 things along the way. I'll read "
                "and save your files in `framework/client-follow-up`. Stopping early is safe: progress is saved after "
                "each task. To pick up, say 'run the build skill. My files are in framework/client-follow-up.' "
                "Let's start with your Gmail connection.")
        self.assertTrue(any(f.matches(said) for f in forms))
        self.assertFalse(any(f.matches(said.replace("OK 2 quick real checks and setup changes", "OK 2 quick real check"))
                             for f in forms))
        # 3c-EC: with [L] at 1 the clause's count-one forms are approved, whole lines only
        for one in ("OK 1 quick real check", "OK 1 setup change"):
            self.assertTrue(any(f.matches(said.replace("OK 2 quick real checks and setup changes", one)) for f in forms))
        self.assertFalse(any(f.matches(said.replace("OK 2 quick real checks and setup changes", "OK 1 real check"))
                             for f in forms))
        self.assertFalse(ok({"type": "quote", "id": "N-B4"}, run_of("Please OK 1 quick real check.")))

    def test_quote_absent(self):
        self.assertFalse(ok({"type": "quote_absent", "id": "N-D1"}, run_of(N_D1)))
        self.assertTrue(ok({"type": "quote_absent", "id": "N-D1"}, run_of("Hello.")))

    def test_reads_the_corpus_not_the_skills(self):
        src = (EVALS / "check_quotes.py").read_text() + (EVALS / "approved_lines.py").read_text()
        self.assertNotIn("skills/", src.replace("never the skills", "").replace("never reads the skills", ""))


class WordingChecks(unittest.TestCase):
    def test_vocabulary(self):
        self.assertTrue(ok({"type": "vocabulary"}, run_of("Your plan is ready. Shall I go on?")))
        self.assertFalse(ok({"type": "vocabulary"}, run_of("I'll write the acceptance criteria next. OK?")))
        self.assertFalse(ok({"type": "vocabulary"}, run_of("This edge case needs a test case. Ready?")))
        # an approved line that holds a platform label isn't flagged
        self.assertTrue(ok({"type": "vocabulary"}, run_of(
            "To see what the AI does with no instructions, open a new chat in your workflow's Project, and before typing, "
            "switch off connectors and memory under +, so it has nothing it could send or change with. Paste this, and "
            "copy back what it says. Then delete that chat.")))
        # file names in code aren't wording
        self.assertTrue(ok({"type": "vocabulary"}, run_of("I moved `design-spec.md` aside. Shall I start?")))
        # the leader's work shown back in a block quote isn't the AI's wording
        self.assertTrue(ok({"type": "vocabulary"}, run_of("Here's the input:\n> check-in on Q1 project scope\nKeep it?")))
        self.assertTrue(ok({"type": "no_time_or_step_numbers"}, run_of("Here's the input:\n> renewal, 30 min\nKeep it?")))

    def test_text_checks_read_code_marks_as_plain_words(self):
        # the leader reads `framework` as framework; the quote check's own norm drops the marks too
        c = {"type": "ai_contains", "text": "I'll read and save your files in framework", "turn": "first"}
        self.assertTrue(ok(c, run_of("I'll read and save your files in `framework`. Stopping early is safe.")))
        self.assertFalse(ok(c, run_of("I'll read and save your files in `Google Drive`.")))

    def test_no_time_or_step_numbers(self):
        self.assertTrue(ok({"type": "no_time_or_step_numbers"}, run_of("Part 2 of 4 — the plan. Step 3, your review, stays.")))
        self.assertFalse(ok({"type": "no_time_or_step_numbers"}, run_of("This takes about 20 minutes. Ready?")))
        self.assertFalse(ok({"type": "no_time_or_step_numbers"}, run_of("Next is Step 3 (Design). Say go.")))
        self.assertFalse(ok({"type": "no_time_or_step_numbers"}, run_of("Design is Step 3 of the framework.")))
        # the approved time-saved line is a carried line, not an estimate
        self.assertTrue(ok({"type": "no_time_or_step_numbers"}, run_of("Run 12; about 6 hours saved so far.")))
        # the leader's own sizes, played back, aren't estimates; the framework's own still are
        run = run_of("Noted: about 20 minutes per follow-up today, as your estimate.",
                     "Got it: the 2 hours a day as what the team spends today.")
        run["sessions"][0]["turns"][0]["text"] = "About twenty minutes per follow-up, and two hours a day."
        self.assertTrue(ok({"type": "no_time_or_step_numbers"}, run))
        run = run_of("Noted: about 20 minutes per follow-up. This part takes about 10 minutes.")
        run["sessions"][0]["turns"][0]["text"] = "About 20 minutes per follow-up."
        self.assertFalse(ok({"type": "no_time_or_step_numbers"}, run))
        self.assertFalse(ok({"type": "no_time_or_step_numbers"}, run_of("This conversation takes about 20 minutes.")))
        # the Baseline in the requirements' Value & Measurement is the leader's number too
        req = {"framework/x/requirements.md": "## Value & Measurement\n\n| Baseline | 15 minutes per report · Estimated |\n\n## Metadata\n\n| Effort | 40 minutes |\n"}
        said = "Its log tracks how long each run took against your 15-minute starting point."
        self.assertTrue(ok({"type": "no_time_or_step_numbers"}, run_of(said, files_start=req)))
        self.assertFalse(ok({"type": "no_time_or_step_numbers"}, run_of(said)))
        self.assertFalse(ok({"type": "no_time_or_step_numbers"}, run_of("That takes about 40 minutes.", files_start=req)))
        # a resume plays back what Analyze's progress file noted from an earlier chat: the leader's number
        prog = {"framework/analyze-in-progress.md": "## Noted so far\n- Client Follow-Up: drafting follow-ups after calls takes about 20 minutes each.\n"}
        said = "Last time we covered Client Relationship Management; I noted Client Follow-Up (drafting a follow-up takes about 20 minutes)."
        self.assertTrue(ok({"type": "no_time_or_step_numbers"}, run_of(said, files_start=prog)))
        self.assertFalse(ok({"type": "no_time_or_step_numbers"}, run_of(said)))
        self.assertFalse(ok({"type": "no_time_or_step_numbers"}, run_of(said + " The next process takes about 10 minutes.", files_start=prog)))

    def test_progress_sizes_count_only_as_the_leader_brought_them(self):
        # 03bd1eef1 read every session's start tree: from session 2 on that holds what the AI wrote in
        # session 1, so an estimate the AI wrote into analyze-in-progress.md counted as the leader's
        said = "Last time I noted Client Follow-Up (drafting a follow-up takes about 20 minutes)."
        prog = {"framework/analyze-in-progress.md": "## Noted so far\n- Client Follow-Up: about 20 minutes each.\n"}
        def two(first, second, marks=True):
            run = run_of("Hello. Which process first?")
            run["sessions"].append({**run_of(said)["sessions"][0], "n": 2, "files_start": second})
            run["sessions"][0]["files_start"] = first
            if marks:
                run["sessions"][0]["fixture"], run["sessions"][1]["fixture"] = True, False
            return run
        c = {"type": "no_time_or_step_numbers"}
        for marks in (True, False):  # unmarked (a run saved before the marks): the first session only
            self.assertFalse(ok(c, two({}, prog, marks)), "the AI's own session-1 note isn't the leader's")
            self.assertTrue(ok(c, two(prog, prog, marks)), "the leader brought the note")
        run = two({}, prog)
        run["sessions"][1]["fixture"] = True  # session 2 started from its own fixture
        self.assertTrue(ok(c, run))

    def test_a_baseline_the_ai_wrote_is_not_the_leaders_size(self):
        # 05289ac91 counted every requirements file's Value & Measurement, the AI's own writing too:
        # a Baseline the AI wrote with no size from the leader made its own estimate pass
        req = {"framework/x/requirements.md": "## Value & Measurement\n\n| Baseline | 15 minutes per report · Estimated |\n"}
        said = "Its log tracks how long each run took against your 15-minute starting point."
        c = {"type": "no_time_or_step_numbers"}
        self.assertFalse(ok(c, run_of(said, files_end=req)))
        run = run_of(said, files_end=req)
        run["sessions"][0]["turns"][0]["text"] = "Each report takes me about fifteen minutes."
        self.assertTrue(ok(c, run))  # the leader's own message gave it
        # session 2 carried over: its start tree is the AI's session-1 file, not the leader's
        run = run_of("Done. Shall we start?")
        run["sessions"].append({**run_of(said)["sessions"][0], "n": 2, "files_start": req})
        run["sessions"][0]["files_end"] = req
        run["sessions"][0]["fixture"], run["sessions"][1]["fixture"] = True, False
        self.assertFalse(ok(c, run))
        self.assertTrue(ok(c, run_of(said, files_start=req)))  # the leader brought it

    def test_signposts_per_skill(self):
        dec = ["Part 1 of 5 — what this is worth.", "Part 2 of 5 — where it starts and ends, and a name.", "Part 3 of 5 — the outcome.",
               "Part 4 of 5 — how the work gets done.", "Part 5 of 5 — rules, sources and practice runs."]
        self.assertTrue(ok({"type": "signposts", "skill": "deconstruct"}, run_of(*dec)))
        self.assertFalse(ok({"type": "signposts", "skill": "deconstruct"}, run_of(*(dec[:2] + dec[3:]))))
        des = ["Part 1 of 4 — where it runs", "Part 2 of 4 — the plan", "Part 3 of 4 — a few questions for you",
               "Part 4 of 4 — review and approve"]
        self.assertTrue(ok({"type": "signposts", "skill": "design"}, run_of(*des)))
        self.assertFalse(ok({"type": "signposts", "skill": "design"}, run_of(des[1], des[0], des[2], des[3])))
        tst = ["Part 1 of 4 — open the round", "Part 2 of 4 — run it", "Part 3 of 4 — the verdict", "Part 4 of 4 — go live"]
        self.assertTrue(ok({"type": "signposts", "skill": "test"}, run_of(*tst)))
        self.assertFalse(ok({"type": "signposts", "skill": "test"}, run_of(*tst[:3])))
        bld = ["Part 1 of 3 — your setup", "Part 2 of 3 — building and checking", "Part 3 of 3 — save it and test"]
        self.assertTrue(ok({"type": "signposts", "skill": "build"}, run_of(*bld)))
        self.assertFalse(ok({"type": "signposts", "skill": "build"}, run_of(bld[0], "Part 2 of 3 — building", bld[2])))

    def test_rubric_judge_sees_tool_lines_behind_a_figure(self):
        # a version the AI read with `claude --version` isn't invented: the judge sees that output line
        import grade_eval as G
        with tempfile.TemporaryDirectory() as t:
            ev = {"type": "user", "message": {"content": [{"type": "tool_result", "content": "2.1.309 (Claude Code)\nPython 3.12.1"}]}}
            Path(t, "events.jsonl").write_text(json.dumps(ev) + "\n")
            run = {"sessions": [{"root": str(Path(t, "workspace")), "files_start": {}, "turns": [
                {"role": "ai", "text": "Your Claude Code version (2.1.309) hasn't been confirmed yet."}]}]}
            _, prompt = G.rubric_prompt(run)
        self.assertIn("2.1.309 (Claude Code)", prompt)
        self.assertNotIn("Python 3.12.1", prompt)

    def test_rubric_judge_sees_a_file_date_from_ls(self):
        # a date the AI read off `ls -l` isn't invented: the line naming the file it speaks of comes
        # first, ahead of other lines with the same date
        import grade_eval as G
        other = "\n".join(f"drwxr-xr-x@  3 me  staff   96 Oct 24 15:02 folder{i}" for i in range(40))
        res = other + "\n-rw-r--r--@ 1 me  staff  894 Oct 24 15:02 SKILL.md\n-rw-r--r--@ 1 me  staff  9 Oct 25 02:51 x.md"
        with tempfile.TemporaryDirectory() as t:
            ev = {"type": "user", "message": {"content": [{"type": "tool_result", "content": res}]}}
            Path(t, "events.jsonl").write_text(json.dumps(ev) + "\n")
            run = {"sessions": [{"root": str(Path(t, "workspace")), "files_start": {}, "turns": [
                {"role": "ai", "text": "`SKILL.md` is unchanged: same contents and same date (Oct 24)."}]}]}
            _, prompt = G.rubric_prompt(run)
        self.assertIn("-rw-r--r--@ 1 me staff 894 Oct 24 15:02 SKILL.md", prompt)
        self.assertNotIn("x.md", prompt)

    def test_rubric_judge_sees_an_iso_date_behind_a_spoken_date(self):
        # "from 20 October" read off a results file's `date: 2026-10-20` isn't invented
        import grade_eval as G
        with tempfile.TemporaryDirectory() as t:
            ev = {"type": "user", "message": {"content": [{"type": "tool_result", "content": "round: 1\ndate: 2026-10-20\nworkflow: x"}]}}
            Path(t, "events.jsonl").write_text(json.dumps(ev) + "\n")
            run = {"sessions": [{"root": str(Path(t, "workspace")), "files_start": {}, "turns": [
                {"role": "ai", "text": "Picking up round 1 from 20 October."}]}]}
            _, prompt = G.rubric_prompt(run)
        self.assertIn("date: 2026-10-20", prompt)
        self.assertNotIn("workflow: x", prompt)

    def test_rubric_judge_sees_tool_passages_sharing_four_words(self):
        # a plan list the AI read in the plugin's platform registry (one long JSON line) isn't invented:
        # the judge sees that sentence, cut from the line; passages sharing fewer than four words in a row
        # don't show, nor do passages matched only through an approved line
        import grade_eval as G
        reg = json.dumps({"notes": "Skills: sidebar Plugins > Skills > Create. The skills article lists Business, "
                                   "Enterprise, Healthcare and Edu, so skills on Plus and Pro are unverified. "
                                   "Memory: Settings > Personalization > Memory."})
        res = f"     1\t{reg}\n     2\tThe plan is short.\n     3\tHere's the plan in brief, as approved."
        with tempfile.TemporaryDirectory() as t:
            ev = {"type": "user", "message": {"content": [{"type": "tool_result", "content": res}]}}
            Path(t, "events.jsonl").write_text(json.dumps(ev) + "\n")
            run = {"sessions": [{"root": str(Path(t, "workspace")), "files_start": {}, "turns": [
                {"role": "ai", "text": "Here's the plan in brief. The full plan is in `framework/x/design-plan.md`.\n\n"
                                       "OpenAI documents skills for its Business, Enterprise, Healthcare and Edu plans."}]}]}
            _, prompt = G.rubric_prompt(run)
        self.assertIn("The skills article lists Business, Enterprise, Healthcare and Edu, so skills on Plus", prompt)
        self.assertNotIn("Personalization", prompt)
        self.assertNotIn("The plan is short.", prompt)
        self.assertNotIn("as approved", prompt)

    def test_rubric_judge_sees_a_path_pattern_the_message_fills_in(self):
        # Documents/Cowork/[workflow-slug]/ in the registry backs Documents/Cowork/competitor-research-brief/
        import grade_eval as G
        reg = json.dumps({"knowledge": "The leader adds each context file from its runtime copy in "
                                       "Documents/Cowork/[workflow-slug]/, and checks Knowledge lists only those files.",
                          "skills": "Cowork saves it to OneDrive, in Documents/Cowork/skills/<skill>/."}, indent=1)
        with tempfile.TemporaryDirectory() as t:
            ev = {"type": "user", "message": {"content": [{"type": "tool_result", "content": reg}]}}
            Path(t, "events.jsonl").write_text(json.dumps(ev) + "\n")
            run = {"sessions": [{"root": str(Path(t, "workspace")), "files_start": {}, "turns": [
                {"role": "ai", "text": "Your list's copy lives in `Documents/Cowork/competitor-research-brief/`."}]}]}
            _, prompt = G.rubric_prompt(run)
        self.assertIn("Documents/Cowork/[workflow-slug]/", prompt)
        self.assertNotIn("Documents/Cowork/skills/<skill>/", prompt)

    def test_rubric_judge_sees_the_changed_lines_of_a_cut_file(self):
        # a long saved draft the AI read and fixed: past the cut, the judge still sees the line it fixed
        import grade_eval as G
        filler = "\n".join(f"- **Filler {i}:** a line that the session leaves exactly as it was, number {i}." for i in range(60))
        start = f"# Plan\n\n{filler}\n- **Required Tools:** Gmail (read, create drafts, send, delete)\n- **Model:** default tier, unchanged by the session here.\n"
        end = start.replace("Gmail (read, create drafts, send, delete)", "Gmail (create drafts)")
        with tempfile.TemporaryDirectory() as t:
            ev = {"type": "user", "message": {"content": [{"type": "tool_result", "content": start}]}}
            Path(t, "events.jsonl").write_text(json.dumps(ev) + "\n")
            run = {"sessions": [{"root": str(Path(t, "workspace")), "turns": [
                {"role": "ai", "text": "The draft gave the skill permission to send and delete email; now it only creates drafts."}],
                "files_start": {"framework/x/design-plan.md": start}, "files_end": {"framework/x/design-plan.md": end}}]}
            _, prompt = G.rubric_prompt(run)
        self.assertIn("Gmail (read, create drafts, send, delete)", prompt)
        self.assertNotIn("unchanged by the session here", prompt)
        self.assertIn("[the session changed this file; its changed lines as the session left them:]\n"
                      "- **Required Tools:** Gmail (create drafts)", prompt)

    def test_rubric_judge_sees_the_after_state_of_a_changed_line(self):
        # a short plan the plan check fixed in-session: the before line and, labelled, the line as left
        import grade_eval as G
        start = ("# Plan\n\n- **Required Tools:** Gmail (read, create drafts, send, delete)\n"
                 "- **Model:** default tier, a line the session leaves exactly as it was.\n")
        end = start.replace("Gmail (read, create drafts, send, delete)", "Gmail (read, create drafts); send and delete denied")
        with tempfile.TemporaryDirectory() as t:
            ev = {"type": "user", "message": {"content": [{"type": "tool_result", "content": start}]}}
            Path(t, "events.jsonl").write_text(json.dumps(ev) + "\n")
            run = {"sessions": [{"root": str(Path(t, "workspace")), "turns": [
                {"role": "ai", "text": "Gmail: it can only create drafts."}],
                "files_start": {"framework/x/design-plan.md": start}, "files_end": {"framework/x/design-plan.md": end}}]}
            _, prompt = G.rubric_prompt(run)
            run["sessions"][0]["files_end"] = {"framework/x/design-plan.md": start}
            _, unchanged = G.rubric_prompt(run)
        self.assertIn("Gmail (read, create drafts, send, delete)", prompt)
        self.assertIn("as the session left them:]\n- **Required Tools:** Gmail (read, create drafts); send and delete denied",
                      prompt)
        self.assertEqual(prompt.count("default tier"), 1)
        self.assertNotIn("the session changed this file", unchanged)

    def test_rubric_judge_sees_a_profile_line_past_the_cut(self):
        # a send tool the AI read in the record's profile, past the cut, is shown: the line shares two words
        import grade_eval as G
        filler = "\n".join(f"- **Filler {i}:** a line about nothing the messages speak of, number {i}." for i in range(60))
        start = f"# Build record\n\n{filler}\ntool gmail write mcp__gmail__send_message | Sends a message\nheadless_writes practice only here\n"
        with tempfile.TemporaryDirectory() as t:
            ev = {"type": "user", "message": {"content": [{"type": "tool_result", "content": start}]}}
            Path(t, "events.jsonl").write_text(json.dumps(ev) + "\n")
            run = {"sessions": [{"root": str(Path(t, "workspace")), "turns": [
                {"role": "ai", "text": "Its Gmail connection also includes a way to send email."}],
                "files_start": {"framework/x/build-record.md": start}, "files_end": {"framework/x/build-record.md": start}}]}
            _, prompt = G.rubric_prompt(run)
        self.assertIn("mcp__gmail__send_message", prompt)
        self.assertNotIn("headless_writes", prompt)

    def test_rubric_judge_sees_each_sessions_own_version_of_a_file(self):
        # two sessions from different fixtures: the second's plan (approved: false) is shown for it,
        # and each message carries its session
        import grade_eval as G
        one = "---\napproved: true\n---\n# Plan\nThe plan drafts a follow-up email after each client call.\nIt never sends anything at all, ever.\n"
        two = one.replace("approved: true", "approved: false")
        with tempfile.TemporaryDirectory() as t:
            sessions = []
            for k, text in ((1, one), (2, two)):
                d = Path(t, f"s{k}")
                d.mkdir()
                ev = {"type": "user", "message": {"content": [{"type": "tool_result", "content": text}]}}
                Path(d, "events.jsonl").write_text(json.dumps(ev) + "\n")
                sessions.append({"root": str(d / "workspace"), "files_start": {"framework/x/design-plan.md": text},
                                 "turns": [{"role": "ai", "text": f"Message from session {k}."}]})
            _, prompt = G.rubric_prompt({"sessions": sessions})
        self.assertIn("design-plan.md (session 2: its lines that differ from session 1's)", prompt)
        self.assertIn("approved: false", prompt)
        self.assertIn("## Message 2 (session 2)", prompt)


def events_run(*tool_uses, events=True):
    """A one-session run whose events.jsonl holds these assistant tool calls, in order."""
    t = tempfile.mkdtemp()
    if events:
        Path(t, "events.jsonl").write_text("".join(json.dumps(
            {"type": "assistant", "message": {"content": [{"type": "tool_use", "id": f"t{i}", "name": n, "input": inp}]}}) + "\n"
            for i, (n, inp) in enumerate(tool_uses)))
    return run_of("Do you approve the plan?", root=str(Path(t, "workspace")))


PLAN = "/tmp/x/workspace/framework/client-follow-up/design-plan.md"
RESET = {"type": "tool_write", "path": "framework/client-follow-up/design-plan.md",
         "pattern": "(?m)^approved: false[ \\t]*$", "before": "approved: true"}


class ToolWrite(unittest.TestCase):
    """EN-rerun-consequential: the plan is set back to approved: false before it's approved again
    (cc11ff3a7 left the reset to the judge, who sees only the end state)."""

    def test_reset_then_reapproval_passes(self):
        run = events_run(("Write", {"file_path": PLAN, "content": "---\nworkflow: x\napproved: false\n---\n"}),
                         ("Bash", {"command": f"sed -i '' 's/^approved: false$/approved: true/' {PLAN}"}))
        self.assertTrue(ok(RESET, run))
        run = events_run(("Edit", {"file_path": PLAN, "old_string": "approved: true", "new_string": "approved: false"}),
                         ("Edit", {"file_path": PLAN, "old_string": "approved: false", "new_string": "approved: true"}))
        self.assertTrue(ok(RESET, run))

    def test_no_reset_fails(self):
        # approved straight on the earlier yes: only the end state, approved: true
        run = events_run(("Bash", {"command": f"sed -i '' 's/^approved: false$/approved: true/' {PLAN}"}),
                         ("Edit", {"file_path": PLAN, "old_string": "requirements_revision: 1",
                                   "new_string": "requirements_revision: 2"}))
        self.assertFalse(ok(RESET, run))
        # a Bash command that names approved: false isn't a reset: only Write and Edit count
        run = events_run(("Bash", {"command": f"grep -n 'approved: false' {PLAN}"}),
                         ("Edit", {"file_path": PLAN, "old_string": "approved: false", "new_string": "approved: true"}))
        self.assertFalse(ok(RESET, run))

    def test_reset_after_approval_or_never_reapproved_fails(self):
        run = events_run(("Edit", {"file_path": PLAN, "old_string": "approved: false", "new_string": "approved: true"}),
                         ("Edit", {"file_path": PLAN, "old_string": "approved: true", "new_string": "approved: false"}))
        self.assertFalse(ok(RESET, run))
        run = events_run(("Edit", {"file_path": PLAN, "old_string": "approved: true", "new_string": "approved: false"}))
        self.assertFalse(ok(RESET, run))

    def test_another_files_reset_or_no_events_fails(self):
        other = PLAN.replace("design-plan.md", "requirements.md")
        run = events_run(("Edit", {"file_path": other, "old_string": "approved: true", "new_string": "approved: false"}),
                         ("Edit", {"file_path": PLAN, "old_string": "approved: false", "new_string": "approved: true"}))
        self.assertFalse(ok(RESET, run))
        self.assertFalse(ok(RESET, events_run(events=False)))
        self.assertFalse(ok(RESET, run_of("Do you approve the plan?")))  # no root at all

    def test_the_eval_uses_it(self):
        ev = next(e for e in json.loads((ROOT / "design-workspace" / "evals" / "evals.json").read_text())["evals"]
                  if e["id"] == "EN-rerun-consequential")
        checks = json.dumps([x.get("check") for x in ev["expectations"] if x["kind"] == "scripted"])
        self.assertIn('"tool_write"', checks)


class FileChecks(unittest.TestCase):
    def setUp(self):
        self.req = (FIX / "requirements.md").read_text()
        self.plan = (FIX / "design-plan.md").read_text()
        self.record = (FIX / "build-record.md").read_text()
        self.results = (FIX / "test-results.md").read_text()

    def test_yaml_keys(self):
        files = {"framework/x/design-plan.md": self.plan}
        c = {"type": "yaml_keys", "path": "framework/*/design-plan.md", "keys": ST.PLAN_KEYS}
        self.assertTrue(ok(c, run_of("x", files_end=files)))
        planted = {"framework/x/design-plan.md": self.plan.replace("changes: []", "counts: 3\nchanges: []")}
        self.assertFalse(ok(c, run_of("x", files_end=planted)))
        self.assertFalse(ok(c, run_of("x", files_end={"framework/x/design-plan.md": "# no frontmatter\n"})))

    def test_no_yaml_is_retired(self):
        with self.assertRaises(ValueError):
            CS.check({"type": "no_yaml", "path": "x"}, run_of("x", files_end={"x": "a"}))

    def structure(self, kind, text):
        return ok({"type": "structure", "kind": kind, "path": "f.md"}, run_of("x", files_end={"f.md": text}))

    def test_plan_structure(self):
        self.assertTrue(self.structure("plan", self.plan))
        self.assertFalse(self.structure("plan", self.plan.replace("autonomy: Guided", "autonomy: guided")))
        self.assertFalse(self.structure("plan", self.plan.replace("### KW — Keeping it working", "### X9 — Keeping it working")))
        self.assertFalse(self.structure("plan", self.plan.replace("## Self-Test Summary", "## Coverage\n\n## Self-Test Summary")))
        self.assertFalse(self.structure("plan", self.plan.replace("| Handled by orchestrator |", "| Orchestrator does it |")))

    def test_build_record_structure(self):
        self.assertTrue(self.structure("build_record", self.record))
        self.assertFalse(self.structure("build_record", self.record.replace("| Ruling |\n", "|\n", 1)))
        self.assertFalse(self.structure("build_record", self.record.replace("schedule: none", "schedule: on")))
        self.assertFalse(self.structure("build_record", self.record.replace("## What it can access", "## Access")))

    def test_results_structure(self):
        self.assertTrue(self.structure("results", self.results))
        self.assertFalse(self.structure("results", self.results.replace("round_kind: first", "round_kind: initial")))
        self.assertFalse(self.structure("results", self.results.replace("go_live: done", "go_live: done\ncriteria_met: 13")))
        self.assertFalse(self.structure("results", self.results.replace("## Not run", "## Scenarios not run")))
        self.assertFalse(self.structure("results", self.results.replace("R3: met }", "R3: passed }", 1)))

    def test_requirements_structure_through_t14(self):
        with tempfile.TemporaryDirectory() as t:
            t = str(Path(t) / "wf")
            shutil.copytree(FIX, t)  # the whole workflow folder: the script checks inputs/ too
            run = run_of("x", files_end={"requirements.md": self.req}, root=t)
            c = {"type": "structure", "kind": "requirements", "path": "requirements.md", "registry": False}
            self.assertTrue(ok(c, run), CS.check(c, run)[1])
            broken = re.sub(r"^## Acceptance Criteria\n", "## Things it must get right\n", self.req, flags=re.M)
            Path(t, "requirements.md").write_text(broken)
            self.assertFalse(ok(c, run_of("x", files_end={"requirements.md": broken}, root=t)))


PLAN_WITH_AGENT = """---
workflow: client-follow-up
requirements_revision: 1
approved: true
autonomy: Guided
decomposition: steps
mechanism: Agent
involvement: Augmented
platform: Microsoft 365
platform_mode: guided
packaging: Loose Files
changes: []
---

# Client Follow-Up — Design Plan

## Data Readiness
| Context | Status | AI can reach it | Read at runtime from | Provided by |
|---|---|---|---|---|
| C1 | Exists | Yes | Documents/Cowork/client-follow-up/C1-follow-up-style.md | T1 |

## Component Blueprints

### A1 — client-follow-up
- **Tools:** Outlook

## Tasks

### T1 — Copy the style guide
- **Builds:** setup: the runtime copy of C1
- **Uses / hands on:** C1
- **Meets:** C1
- **Done when:** read-back
- **Depends on:** —
- **rev:** 1

### T2 — Client Follow-Up agent
- **Builds:** New agent: A1 (`client-follow-up`)
- **Uses / hands on:** I1; C1
- **Meets:** AC1
- **Done when:** practice run E1 meets AC1
- **Depends on:** T1
- **rev:** 1
"""
CARRIED = ["Practice run: nothing will be sent or changed.", "All results"]


def build_prompt(task="T2", folder="client-follow-up", files="Documents/Cowork/client-follow-up/C1-follow-up-style.md",
                 conns="Outlook", lines="Practice run: nothing will be sent or changed. End with a block headed All results."):
    return (f"Build the agent described in task {task} of design-plan.md, using the requirements in requirements.md. "
            f"Both files are in my OneDrive, in Framework/{folder}. Everything you need is in those files, so don't ask "
            f"me anything they already answer. The agent reads only {files}, and connects to {conns}. Its instructions "
            f"must also include these lines, word for word: {lines}")


class FillCheck(unittest.TestCase):
    def check(self, prompt, kind="build"):
        msg = f"[Agent] is made in Copilot's Agent Builder:\n\n```\n{prompt}\n```\n"
        run = run_of(msg, files_end={"framework/client-follow-up/design-plan.md": PLAN_WITH_AGENT})
        return CS.check({"type": "fill_check", "kind": kind, "carried": CARRIED}, run)

    def test_good_build_prompt_passes(self):
        passed, why = self.check(build_prompt())
        self.assertTrue(passed, why)

    def test_planted_failures(self):
        self.assertFalse(self.check(build_prompt(task="T1"))[0])                     # wrong task
        self.assertFalse(self.check(build_prompt(folder="other"))[0])                 # wrong folder
        self.assertFalse(self.check(build_prompt(
            files="Documents/Cowork/client-follow-up/C1-follow-up-style.md and Framework/client-follow-up/requirements.md"))[0])
        self.assertFalse(self.check(build_prompt(files="Framework/client-follow-up/context/C1-follow-up-style.md"))[0])
        self.assertFalse(self.check(build_prompt(conns="Outlook and Teams"))[0])      # an extra connection
        self.assertFalse(self.check(build_prompt(
            lines="Practice run: nothing will be sent or modified. End with a block headed All results."))[0])
        self.assertFalse(self.check(build_prompt().replace("so don't ask me", "so never ask me"))[0])  # fixed words

    def test_fix_prompt(self):
        good = ("In this agent, put back the line every practice run must start with, so it carries this line word for "
                "word: 'Practice run: nothing will be sent or changed.'. Change nothing else.")
        self.assertTrue(self.check(good, "fix")[0], self.check(good, "fix")[1])
        self.assertFalse(self.check(good.replace("or changed.'", "or modified.'"), "fix")[0])
        self.assertFalse(self.check(good.replace(" Change nothing else.", ""), "fix")[0])


class PlatformSimulations(unittest.TestCase):
    def ws(self):
        t = Path(tempfile.mkdtemp())
        ws = t / "workspace"
        (ws / "framework" / "client-follow-up").mkdir(parents=True)
        (ws / "framework" / "client-follow-up" / "requirements.md").write_text("x")
        (ws / "registry").mkdir()
        return t, ws

    def test_six_platforms(self):
        self.assertEqual(sorted(L.PLATFORMS), sorted(["claude-code", "codex", "claude-web", "claude-desktop",
                                                      "chatgpt", "microsoft-365"]))

    def test_drive_layout(self):
        t, ws = self.ws()
        L.PLATFORMS["chatgpt"]().prepare(ws)
        self.assertTrue((ws / "drive" / "Framework" / "client-follow-up" / "requirements.md").exists())
        self.assertTrue((ws / "drive" / "Framework" / "registry").exists())
        shutil.rmtree(t)

    def test_m365_attach_fallback(self):
        t, ws = self.ws()
        p = L.PLATFORMS["microsoft-365"](["cowork_cannot_read_onedrive"])
        p.prepare(ws)
        self.assertFalse((ws / "onedrive" / "Framework").exists())
        self.assertEqual(p.on_leader("done", ws), 1)
        self.assertTrue((ws / "onedrive" / "Framework" / "client-follow-up" / "requirements.md").exists())
        t2, ws2 = self.ws()
        q = L.PLATFORMS["microsoft-365"](["cowork_cannot_read_onedrive", "attach_fails"])
        q.prepare(ws2)
        q.on_leader("done", ws2)
        self.assertFalse((ws2 / "onedrive" / "Framework").exists())
        shutil.rmtree(t)
        shutil.rmtree(t2)

    def test_agent_builder_faults(self):
        msg = f"```\n{build_prompt()}\n```"
        clean = L.PLATFORMS["microsoft-365"]().screen(msg, Path("."))[0][0]
        self.assertIn("Practice run: nothing will be sent or changed.", clean)
        reworded = L.PLATFORMS["microsoft-365"](["agent_builder_rewords_carried_line"]).screen(msg, Path("."))[0][0]
        self.assertIn("nothing will be sent or modified.", reworded)
        missing = L.PLATFORMS["microsoft-365"](["agent_builder_missing_context_file"]).screen(msg, Path("."))[0][0]
        self.assertIn("couldn't find C1-follow-up-style.md", missing)
        knowledge = L.PLATFORMS["microsoft-365"](["agent_builder_requirements_under_knowledge"]).screen(msg, Path("."))[0][0]
        self.assertIn("requirements.md", knowledge.split("Knowledge lists:")[1].split("\n")[0])
        ordinary = L.PLATFORMS["microsoft-365"](["agent_builder_ordinary_chat"])
        self.assertIn("ordinary chat", ordinary.screen(msg, Path("."))[0][0])
        self.assertIn("Instructions", ordinary.screen(msg, Path("."))[0][0])  # the second try makes it
        # the reworded line is what the paste-back check (N-B53's carried-line fill) must catch
        self.assertNotIn("Practice run: nothing will be sent or changed.", reworded)
        # a rebuild (a second agent made) keeps the line, unless the fault persists after a fix
        once = L.PLATFORMS["microsoft-365"](["agent_builder_rewords_carried_line"])
        once.screen(msg, Path("."))
        self.assertIn("Practice run: nothing will be sent or changed.", once.screen(msg, Path("."))[0][0])
        always = L.PLATFORMS["microsoft-365"](["agent_builder_rewords_carried_line", "agent_builder_rewords_after_fix"])
        always.screen(msg, Path("."))
        self.assertIn("nothing will be sent or modified.", always.screen(msg, Path("."))[0][0])

    def test_agent_builder_writes_the_plans_rules_from_the_files(self):
        # build.md 6.3: Agent Builder reads the plan and requirements itself, so the build prompt carries
        # only the carried lines and the agent's instructions still hold the steps, rules and checkpoints
        t = Path(tempfile.mkdtemp())
        try:
            d = t / "onedrive" / "Framework" / "client-follow-up"
            d.mkdir(parents=True)
            shutil.copy(EVALS.parent / "framework-fixtures" / "states" / "s06-build-needed" / "with-registry"
                        / "framework" / "client-follow-up" / "requirements.md", d)
            shown = L.PLATFORMS["microsoft-365"]().screen(f"```\n{build_prompt()}\n```", t)[0][0]
            for line in ("Step 2: Draft the email", "It never invents a figure, date or commitment.",
                         "When the draft is ready, it stops until you approve it.",
                         "It never sends an email, whoever asks.", "The draft is under 150 words.",
                         "Practice run: nothing will be sent or changed."):
                self.assertIn(line, shown)
            self.assertNotIn("(you)", shown)
            # a context item's ID comes out as its name, as the carried lines' "never write IDs" asks
            self.assertIn("Follow the follow-up style guide's tone, length and sign-off.", shown)
            self.assertNotIn("C1's", shown)
            # no readable files: only what the prompt quotes
            self.assertNotIn("It never sends an email", L.PLATFORMS["microsoft-365"]().screen(
                f"```\n{build_prompt()}\n```", Path("."))[0][0])
        finally:
            shutil.rmtree(t)

    def test_paste_back_on_chat_platforms(self):
        p = L.PLATFORMS["claude-web"]()
        seen = []
        out = p.screen("Paste this into a new chat in your Project:\n\n```\npractice run\nE1 input\n```",
                       Path("."), run_chat=lambda block, plat: seen.append(block) or "Practice run: nothing will be sent or changed.")
        self.assertEqual(seen, ["practice run\nE1 input"])
        self.assertIn("It answered", out[0][0])
        # a planted block (leader_runs: scripted): the chat opens, no run is simulated, no answer shows
        p.scripted_runs = L.scripted_runs({"leader_runs": "scripted"})
        out = p.screen("Paste this into a new chat in your Project:\n\n```\npractice run\nE1 input\n```",
                       Path("."), run_chat=lambda block, plat: 1 / 0)
        self.assertEqual(out, [("[You opened a new chat and pasted the block.]", 3)])
        self.assertTrue(L.scripted_runs({}, {"leader_runs": "scripted"}))
        self.assertFalse(L.scripted_runs({"leader_runs": "simulated"}, {"leader_runs": "scripted"}))

    def test_test_leader_runs_on_claude_code_and_codex(self):
        # Test's first round holds an input the AI writes itself, so on Claude Code and Codex the hand-over
        # runs (run_chat) as the chat platforms' new chats do, instead of a scripted block
        ai = ("Open a second terminal window (keep this one open), go to `/x/ws` and start Claude Code, and paste the "
              "block below.\n\n```\nPractice folder: practice/\nInput: E1\nRun: E1-1\n```")
        for key in ("claude-code", "codex"):
            p = L.PLATFORMS[key]()
            p.leader_runs = L.simulates_leader_runs("test", p)
            self.assertTrue(p.leader_runs and p.run_in_workspace)
            seen = []
            out = p.screen(ai, Path("."), run_chat=lambda b, plat: seen.append(b) or "Practice run: nothing will be sent or changed.")
            self.assertEqual(seen, ["Practice folder: practice/\nInput: E1\nRun: E1-1"])
            self.assertIn("It answered:]\nPractice run", out[0][0])
        cc = L.PLATFORMS["claude-code"]()
        self.assertFalse(L.simulates_leader_runs("build", cc))  # Build keeps its behaviour
        self.assertFalse(L.simulates_leader_runs("test", cc, {"leader_runs": "scripted"}))  # a planted block
        self.assertFalse(L.simulates_leader_runs("test", cc, {}, {"leader_runs": "scripted"}))
        self.assertTrue(L.simulates_leader_runs("test", cc, {}, {"leader_runs": "simulated"}))
        self.assertFalse(L.simulates_leader_runs("test", L.PLATFORMS["claude-web"]()))  # chat platforms: paste_back
        self.assertEqual(cc.screen(ai, Path("."), run_chat=lambda b, plat: 1 / 0), [])  # not switched on: no run
        # Codex's run is told where Codex keeps its skills; Claude Code's load from the workspace natively
        self.assertIn(".agents/skills/", L.PLATFORMS["codex"]().run_preamble())
        self.assertIsNone(cc.run_preamble())
        web = L.PLATFORMS["claude-web"]()
        self.assertEqual(web.run_preamble(), web.preamble())

    def test_run_chat_runs_in_the_workspace_on_claude_code_and_codex(self):
        import types
        import run_eval as R
        t = Path(tempfile.mkdtemp())
        saved = H.call
        try:
            ws = t / "workspace"
            (ws / ".claude" / "skills" / "wf").mkdir(parents=True)
            seen = []
            H.call = lambda rnd, role, root, prompt, **kw: (seen.append(kw) or ("ok", {}))
            calls = []
            rc = R.make_run_chat(None, t, ws, types.SimpleNamespace(skill_model="m"), calls)
            for key in ("claude-code", "codex", "claude-web"):
                rc("block", L.PLATFORMS[key]())
            self.assertEqual([kw["cwd"] for kw in seen[:2]], [ws, ws])  # the leader's second terminal
            self.assertNotEqual(seen[2]["cwd"], ws)  # a cold chat with only the built workflow
            self.assertTrue((seen[2]["cwd"] / ".claude" / "skills" / "wf").is_dir())
            self.assertIn(".agents/skills/", seen[1]["append_system_prompt"])
            self.assertEqual([c["role"] for c in calls], ["run_chat"] * 3)
        finally:
            H.call = saved
            shutil.rmtree(t)

    def test_chat_platform_layout_keeps_the_registry_linting_clean(self):
        # rule 4: in a framework folder the registry's repo links drop the `framework/` prefix; a skill in
        # the leader's account is named as text; on a case-insensitive disk ws/framework is ws/Framework
        for key, sub in (("claude-desktop", ""), ("microsoft-365", "onedrive"), ("chatgpt", "drive")):
            t = Path(tempfile.mkdtemp())
            try:
                shutil.copytree(ROOT / "framework-fixtures" / "states" / "s11-live" / "with-registry", t, dirs_exist_ok=True)
                L.PLATFORMS[key]().prepare(t)
                fw = t / sub / "Framework"
                node = (fw / "registry" / "workflows" / "client-follow-up.md").read_text()
                self.assertIn("](client-follow-up/requirements.md)", node)
                self.assertNotIn("](framework/", node)
                self.assertNotIn(".claude/skills/", node)
                self.assertTrue((fw / "client-follow-up" / "requirements.md").exists())
                self.assertFalse((t / ".framework-moving").exists())
                lint = subprocess.run(["node", str(ROOT / "plugins/handsonai/tools/lint-registry.js"), "registry"],
                                      cwd=fw, capture_output=True, text=True)
                self.assertIn("0 error(s)", lint.stdout + lint.stderr, key)
            finally:
                shutil.rmtree(t)

    def test_no_framework_folder_yet_makes_none(self):
        # Analyze's first run on a chat platform: nothing to move, so no Framework folder appears
        for key, sub in (("claude-web", "drive"), ("microsoft-365", "onedrive"), ("claude-desktop", "")):
            t = Path(tempfile.mkdtemp())
            try:
                L.PLATFORMS[key]().prepare(t)
                self.assertFalse((t / sub / "Framework").exists(), key)
            finally:
                shutil.rmtree(t)
        t = Path(tempfile.mkdtemp())
        try:  # a folder not added to the chat still exists for the leader to add
            p = L.PLATFORMS["claude-desktop"](["no_folder_added"])
            p.prepare(t)
            self.assertFalse((t / "Framework").exists())
            self.assertEqual(p.on_leader("done", t), 1)
            self.assertTrue((t / "Framework").is_dir())
        finally:
            shutil.rmtree(t)
            shutil.rmtree(t.parent / ".sim-hidden", ignore_errors=True)

    def test_action_counter(self):
        sessions = [{"turns": [{"role": "student", "text": "run the build skill", "prompt": True, "actions": 0},
                               {"role": "ai", "text": "…"},
                               {"role": "student", "text": "done", "actions": 6},
                               {"role": "ai", "text": "…"},
                               {"role": "student", "text": "END", "end": True, "actions": 0}]}]
        c = L.count_actions(sessions)
        self.assertEqual(c, {"messages": 2, "screen_actions": 6, "actions": 8})
        self.assertIn("about 70", L.action_report(c, {"figure": 70, "journey": "light path with an agent on Microsoft 365"}))
        self.assertNotRegex(L.action_report(c, None), r"(?i)minute|hour|second")
        msg, n = L.strip_actions("[did: opened a new chat]\n[did: pasted the block]\nIt says hello.")
        self.assertEqual((msg, n), ("It says hello.", 2))


class ReleaseItemsAndFidelity(unittest.TestCase):
    def test_judged_items_and_preconditions_follow_the_release_checks(self):
        saved = CS.release_checks_passed
        try:
            for passed in (True, False):
                CS.release_checks_passed = lambda ids, p=passed: p
                ev = {"expectations": [
                    {"text": "AI runs", "kind": "judged", "release_check": {"ids": [6], "passed": "AI runs", "open": "Leader runs"}},
                    {"text": "only with AI runs", "kind": "judged", "release_check": {"ids": [6], "passed": "only with AI runs", "open": None}},
                    {"text": "always", "kind": "judged"}],
                      "preconditions": [{"release_check": {"ids": [6], "passed": "wrapper starts", "open": None}}, "plain"]}
                CS.resolve_release_items(ev)
                self.assertEqual([x["text"] for x in ev["expectations"]],
                                 ["AI runs", "only with AI runs", "always"] if passed else ["Leader runs", "always"])
                self.assertTrue(all("release_check" not in x for x in ev["expectations"]))
                self.assertEqual(ev["preconditions"], ["wrapper starts", "plain"] if passed else ["plain"])
        finally:
            CS.release_checks_passed = saved
        # today release check 6 is open: Test's AI-run evals read the leader-runs path
        import run_eval as R
        evs = {e["id"]: e for e in R.load_evals(ROOT / "test-workspace" / "evals" / "evals.json")["evals"]}
        self.assertFalse(CS.release_checks_passed([6]))
        self.assertTrue(any("N-T42" in x["text"] for x in evs["TS-cc-ai-runs"]["expectations"] if x["kind"] == "judged"))
        self.assertFalse(any("check 6" in p for e in evs.values() for p in e.get("preconditions", [])
                             if "can start a headless session" in p))

    def test_validator_checks_release_items(self):
        with tempfile.TemporaryDirectory() as t:
            bad = {"skill_name": "x", "how_to_run": "t", "evals": [
                {"id": "A", "name": "a", "tier": "core", "prompt": "go", "fixture": "empty", "expected_output": "",
                 "files": [], "preconditions": [{"release_check": {"ids": [999], "passed": "x", "open": None}}],
                 "expectations": [{"text": "q", "kind": "judged", "release_check": {"ids": [6], "passed": 3}}]}]}
            Path(t, "evals.json").write_text(json.dumps(bad))
            joined = "\n".join(V.validate_file(Path(t, "evals.json")))
            for needle in ("release check 999 isn't in the platform registry", "release_check 'passed' must be",
                           "release_check 'open' must be"):
                self.assertIn(needle, joined)

    def test_fidelity_counts_the_screen_and_the_scripts_quoted_blocks_as_seen(self):
        def run(turns, quotes=""):
            return {"sessions": [{"n": 1, "turns": turns, "script_quotes": quotes}]}
        pasted = "Practice run: nothing will be sent or changed. What I did: read requirements.md"
        turns = [{"role": "student", "text": "go", "prompt": True}, {"role": "ai", "text": "Paste its block here."},
                 {"role": "student", "text": pasted, "student": True}]
        self.assertFalse(CS.fidelity(run(turns))[0])  # the leader's own words: a term first
        self.assertTrue(CS.fidelity(run(turns, CS.script_quotes(f'- Your real example\'s block: "{pasted}"')))[0])
        turns[2]["screen"] = "[You opened a new chat and pasted the block. It answered:]\n" + pasted
        self.assertTrue(CS.fidelity(run(turns))[0])  # what the screen showed


class CoreRuns(unittest.TestCase):
    """`core_runs: 1` (the Microsoft 365 and Codex evals): the core round runs them once and one valid run counts."""

    def test_core_runs_once_where_the_eval_says_so(self):
        import types
        import run_eval as R
        data = {"default_tier": "regression"}
        args = types.SimpleNamespace(runs=None, smoke=False)
        once = {"id": "M", "tier": "core", "core_runs": 1}
        three = {"id": "C", "tier": "core"}
        legacy = {"id": "D", "tier": "core", "runs": 2}  # an eval's own runs never takes a core eval below three
        reg = {"id": "R", "tier": "regression", "runs": 5}
        self.assertEqual([R.runs_for(e, args, data) for e in (once, three, legacy, reg)], [1, 3, 3, 5])
        args.runs = 3  # an explicit --runs still applies
        self.assertEqual(R.runs_for(once, args, data), 3)
        args.runs, args.smoke = None, True
        self.assertEqual(R.runs_for(three, args, data), 1)
        args.smoke = False
        rows, _ = R.estimate([once, three], types.SimpleNamespace(runs=None, smoke=False, cost_from=None), data)
        self.assertEqual([r[2] for r in rows], [1, 3])

    def test_one_valid_run_counts_only_where_core_runs_is_one(self):
        import run_eval as R
        run = [{"status": "valid", "expectations": [{"passed": True}]}]
        x = [{"text": "t", "kind": "scripted", "passed": True}]
        for r in run:
            r["expectations"] = x
        self.assertFalse(R.SMOKE)
        self.assertEqual(R.eval_verdict({"id": "M", "core_runs": 1}, run, "core")[0], "PASS")
        self.assertEqual(R.eval_verdict({"id": "C"}, run, "core")[0], "NOT COUNTED")

    def test_validator_takes_core_runs_only_on_a_core_eval(self):
        with tempfile.TemporaryDirectory() as t:
            evs = [{"id": i, "name": i, "tier": tier, "prompt": "go", "fixture": "empty", "expected_output": "",
                    "files": [], "core_runs": n, "expectations": [{"text": "q", "kind": "judged"}]}
                   for i, tier, n in (("A", "core", 1), ("B", "regression", 1), ("C", "core", 0), ("D", "core", True))]
            Path(t, "evals.json").write_text(json.dumps({"skill_name": "x", "how_to_run": "t", "evals": evs}))
            errs = [e for e in V.validate_file(Path(t, "evals.json")) if "core_runs" in e]
            self.assertEqual(sorted(e.split(":")[1] for e in errs), ["B", "C", "D"])


class MailStub(unittest.TestCase):
    """The stand-in Gmail/Outlook connection's optional delete_draft tool (N-B33's undo form)."""

    def talk(self, env, calls):
        import subprocess
        reqs = [{"jsonrpc": "2.0", "id": 0, "method": "initialize", "params": {}},
                {"jsonrpc": "2.0", "id": 1, "method": "tools/list"}]
        reqs += [{"jsonrpc": "2.0", "id": i + 2, "method": "tools/call", "params": {"name": n, "arguments": a}}
                 for i, (n, a) in enumerate(calls)]
        out = subprocess.run([sys.executable, "-I", str(H.GMAIL_STUB)], input="\n".join(json.dumps(r) for r in reqs),
                             capture_output=True, text=True, env={**os.environ, **env}).stdout
        return [json.loads(x) for x in out.splitlines()]

    def test_delete_draft_offered_only_on_request_and_only_for_its_own_drafts(self):
        with tempfile.TemporaryDirectory() as t:
            log = str(Path(t) / "gmail-calls.jsonl")
            plain = self.talk({"GMAIL_STUB_LOG": log}, [("delete_draft", {"draftId": "draft-1"})])
            self.assertNotIn("delete_draft", [x["name"] for x in plain[1]["result"]["tools"]])
            self.assertIn("error", plain[2])
            env = {"GMAIL_STUB_LOG": log, "GMAIL_STUB_EXTRA": "delete_draft"}
            made = self.talk(env, [("create_draft", {"body": "hi"})])
            self.assertIn("delete_draft", [x["name"] for x in made[1]["result"]["tools"]])
            did = json.loads(made[2]["result"]["content"][0]["text"])["draftId"]
            # a later session (a new server) deletes it once, from the log; never a draft it didn't make
            res = self.talk(env, [("delete_draft", {"draftId": did}), ("delete_draft", {"draftId": did}),
                                  ("delete_draft", {"draftId": "draft-x"})])
            got = [json.loads(r["result"]["content"][0]["text"])["deleted"] for r in res[2:]]
            self.assertEqual(got, [True, False, False])
        root = Path(tempfile.mkdtemp())
        try:
            self.assertIn("mcp__outlook__delete_draft",
                          H.gmail_mcp(root, server="outlook", service="Outlook", extra=["delete_draft"])["allow"])
            self.assertNotIn("mcp__gmail__delete_draft", H.gmail_mcp(root)["allow"])
            with self.assertRaises(H.HarnessFailure):
                H.gmail_mcp(root, extra=["send_everything"])
        finally:
            shutil.rmtree(root)


class SheetsStub(unittest.TestCase):
    """The stand-in Google Sheets a Build session on Claude Code sees when the plan uses it (P1-floor)."""
    talk = MailStub.talk

    def test_sheets_kind_and_the_plans_connections(self):
        with tempfile.TemporaryDirectory() as t:
            env = {"GMAIL_STUB_LOG": str(Path(t) / "log.jsonl"), "GMAIL_STUB_KIND": "sheets",
                   "GMAIL_STUB_SERVICE": "Google Sheets"}
            out = self.talk(env, [("create_spreadsheet", {"title": "Build check, delete me"}),
                                  ("send_message", {"to": "x", "body": "y"})])
            names = [x["name"] for x in out[1]["result"]["tools"]]
            self.assertEqual(names, ["get_profile", "list_spreadsheets", "read_range", "create_spreadsheet", "update_range"])
            self.assertEqual(json.loads(out[2]["result"]["content"][0]["text"])["sharedWith"], "no one")
            self.assertIn("error", out[3])  # no mail tools on a sheet
        import run_eval as R
        root = Path(tempfile.mkdtemp())
        try:
            ws = root / "workspace"
            plan_dir = ws / "framework" / "client-follow-up"
            plan_dir.mkdir(parents=True)
            plan = plan_dir / "design-plan.md"
            plan.write_text("Gmail: the Claude Code connector (use). Google Sheets: the connector, to update the team's Client Tracker (use).\n")
            data = {"skill_name": "build"}
            m = R.connections_for(L.PLATFORMS["claude-code"](), ws, root, data)
            self.assertEqual(m["servers"], ["gmail", "google_sheets"])
            self.assertIn("mcp__google_sheets__update_range", m["allow"])
            cfg = json.loads(Path(m["config"]).read_text())["mcpServers"]
            self.assertEqual(cfg["google_sheets"]["env"]["GMAIL_STUB_KIND"], "sheets")
            plan.write_text("Gmail: the Claude Code connector (use).\n")
            self.assertEqual(R.connections_for(L.PLATFORMS["claude-code"](), ws, root, data)["servers"], ["gmail"])
            self.assertIsNone(R.connections_for(L.PLATFORMS["claude-code"](), ws, root, {"skill_name": "test"}))
        finally:
            shutil.rmtree(root)


class ChatPlatformConnections(unittest.TestCase):
    """On Claude on the web, ChatGPT and Claude desktop the leader connects Gmail in the platform's
    settings when Build asks: the stand-in is there from the next turn, never before."""

    def test_connect_now_needs_the_ask_and_the_done(self):
        import run_eval as R
        ask = "Gmail isn't connected yet.\n\n1. In Claude, open **Settings**...\n\nSay 'done' when it's connected."
        self.assertTrue(R.connect_now(ask, "done"))
        self.assertFalse(R.connect_now(ask, "Not sure."))
        self.assertFalse(R.connect_now("Can you check that skills are turned on?", "done"))
        self.assertEqual(set(R.CHAT_CONNECT), {"claude-web", "chatgpt", "claude-desktop"})

    def test_chat_platforms_get_the_plan_s_gmail_from_the_drive(self):
        import run_eval as R
        root = Path(tempfile.mkdtemp())
        try:
            ws = root / "workspace"
            (ws / "drive" / "Framework" / "client-follow-up").mkdir(parents=True)
            (ws / "drive" / "Framework" / "client-follow-up" / "design-plan.md").write_text("Gmail: the Claude connector (use).\n")
            m = R.connections_for(L.PLATFORMS["claude-web"](), ws, root, {"skill_name": "build"})
            self.assertEqual(m["servers"], ["gmail"])
            self.assertIsNone(R.connections_for(L.PLATFORMS["claude-web"](), ws, root, {"skill_name": "test"}))
        finally:
            shutil.rmtree(root)


class RestartContinues(unittest.TestCase):
    """Build's restart before Part 2 on Claude Code: a one-session eval gets the leader's second
    session with the pick-up phrase, once; never on another platform, step or listed sessions."""

    def test_restart_session(self):
        import run_eval as R
        cc, web = L.ClaudeCode(), L.PLATFORMS["claude-web"]()
        last = ("That's your setup done. Before I build anything, please restart Claude Code once: close this "
                "session and open a new one. To pick up, say 'run the build skill. My files are in framework/client-follow-up.'")
        turns = [{"role": "student", "text": "Run the build skill."}, {"role": "ai", "text": last},
                 {"role": "student", "text": "END", "end": True}]
        ev, build = {"prompt": "x"}, {"skill_name": "build"}
        s = R.restart_session(ev, build, cc, turns, [{}])
        self.assertEqual(s["prompt"], "Run the build skill. My files are in framework/client-follow-up.")
        self.assertTrue(s["from_previous"])
        self.assertIsNone(R.restart_session(ev, build, cc, turns, [{}, s]))  # once
        self.assertIsNone(R.restart_session(ev, build, web, turns, [{}]))
        self.assertIsNone(R.restart_session(ev, {"skill_name": "test"}, cc, turns, [{}]))
        self.assertIsNone(R.restart_session({"sessions": [{}, {}]}, build, cc, turns, [{}]))
        self.assertIsNone(R.restart_session({"restart_continues": False}, build, cc, turns, [{}]))
        stop = turns[:1] + [{"role": "ai", "text": "To pick up, say 'run the build skill. My files are in framework/x.'"},
                            turns[2]]
        self.assertIsNone(R.restart_session(ev, build, cc, stop, [{}]))  # a pause, not a restart


class NoPython3(unittest.TestCase):
    def test_the_fault_takes_python3_off_path_and_nothing_else(self):
        import subprocess
        root = Path(tempfile.mkdtemp())
        try:
            path = H._system_path(root)
            self.assertEqual(path, H.SYSTEM_PATH)
            (root / H.NO_PYTHON3).write_text("")
            path = H._system_path(root)
            env = {"PATH": path}
            self.assertNotEqual(subprocess.run(["/bin/sh", "-c", "command -v python3"], env=env,
                                               capture_output=True).returncode, 0)
            self.assertEqual(subprocess.run(["/bin/sh", "-c", "command -v ls && command -v git"], env=env,
                                            capture_output=True).returncode, 0)
        finally:
            shutil.rmtree(root)


class StubbedHarness(unittest.TestCase):
    """Init assertions and a whole round, against the stub binary and a fake home."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="fe-test-"))
        self.saved = {k: getattr(H, k) for k in ("REAL_HOME", "REAL_CLAUDE", "REAL_CLAUDE_JSON", "token", "pin_binary")}
        self.env = os.environ.get("TMPDIR")
        os.environ["TMPDIR"] = str(self.tmp / "t")
        (self.tmp / "t").mkdir()
        home = self.tmp / "fakehome"
        (home / ".claude").mkdir(parents=True)
        (home / ".claude.json").write_text(json.dumps({"projects": {}, "oauthAccount": {"emailAddress": "x@example.com"}}))
        H.REAL_HOME, H.REAL_CLAUDE, H.REAL_CLAUDE_JSON = home, home / ".claude", home / ".claude.json"
        H.token = lambda: "sk-ant-oat-STUB"  # never the keychain in tests
        self.stub_dir = self.tmp / "stub"
        self.stub_dir.mkdir()
        shutil.copy2(HERE / "stub_claude.py", self.stub_dir / "claude")
        os.chmod(self.stub_dir / "claude", 0o755)
        H.pin_binary = lambda: (str(self.stub_dir / "claude"), "9.9.9")
        self.plugin = self.tmp / "plugin"
        (self.plugin / "skills" / "deconstruct").mkdir(parents=True)
        (self.plugin / "skills" / "deconstruct" / "SKILL.md").write_text("---\nname: deconstruct\n---\n")
        self.mode({})

    def tearDown(self):
        for k, v in self.saved.items():
            setattr(H, k, v)
        if self.env is None:
            os.environ.pop("TMPDIR", None)
        else:
            os.environ["TMPDIR"] = self.env
        shutil.rmtree(self.tmp, ignore_errors=True)

    def mode(self, m):
        (self.stub_dir / "stub-mode.json").write_text(json.dumps(m))

    def skill_call(self):
        rnd = H.Round(binary=str(self.stub_dir / "claude"), version="9.9.9")
        rnd.bundled_skills, rnd.bundled_plugins = [], []
        root = H.new_run_root(str(self.plugin))
        return H.call(rnd, "skill", root, "run the deconstruct skill", cwd=root / "workspace",
                      tools=H.SKILL_TOOLS, plugin=root / "plugin")

    def test_clean_init_passes(self):
        text, rec = self.skill_call()
        self.assertEqual(rec["init"]["plugins"][0]["name"], "handsonai")

    def test_extra_plugin_fails_the_init_assertion(self):
        self.mode({"extra_plugin": True})
        with self.assertRaisesRegex(H.HarnessFailure, "init assertion failed: .*someone-elses-plugin"):
            self.skill_call()

    def test_extra_connector_fails_the_init_assertion(self):
        self.mode({"mcp_servers": [{"name": "gmail", "status": "connected"}]})
        with self.assertRaisesRegex(H.HarnessFailure, "init assertion failed: mcp_servers"):
            self.skill_call()

    def test_the_stand_in_gmail_passes_only_when_given(self):
        self.mode({"mcp_servers": [{"name": "gmail", "status": "connected"}]})
        rnd = H.Round(binary=str(self.stub_dir / "claude"), version="9.9.9")
        rnd.bundled_skills, rnd.bundled_plugins = [], []
        root = H.new_run_root(str(self.plugin))
        H.call(rnd, "skill", root, "run the build skill", cwd=root / "workspace",
               tools=H.SKILL_TOOLS, plugin=root / "plugin", mcp=H.gmail_mcp(root))
        self.mode({"mcp_servers": [{"name": "slack", "status": "connected"}]})
        with self.assertRaisesRegex(H.HarnessFailure, "init assertion failed: mcp_servers"):
            H.call(rnd, "skill", root, "run the build skill", cwd=root / "workspace",
                   tools=H.SKILL_TOOLS, plugin=root / "plugin", mcp=H.gmail_mcp(root))

    def test_the_settings_prompt_server_passes_only_when_given(self):
        self.mode({"mcp_servers": [{"name": "leader_click", "status": "connected"}]})
        rnd = H.Round(binary=str(self.stub_dir / "claude"), version="9.9.9")
        rnd.bundled_skills, rnd.bundled_plugins = [], []
        root = H.new_run_root(str(self.plugin))
        H.call(rnd, "skill", root, "run the build skill", cwd=root / "workspace", tools=H.SKILL_TOOLS,
               plugin=root / "plugin", prompt_tool=H.settings_prompt(root, root / "workspace"))
        with self.assertRaisesRegex(H.HarnessFailure, "init assertion failed: mcp_servers"):
            H.call(rnd, "skill", root, "run the build skill", cwd=root / "workspace",
                   tools=H.SKILL_TOOLS, plugin=root / "plugin")

    def test_wrong_version_fails_the_init_assertion(self):
        self.mode({"version": "9.9.8"})
        with self.assertRaisesRegex(H.HarnessFailure, "version"):
            self.skill_call()

    def test_a_workspace_skill_moved_during_the_call_is_still_its_own(self):
        """The init lists the skills there when the call starts; a call that moves one (P1-older's
        kept copy) is no stop. A skill found anywhere else still is, and the stop says where."""
        rnd = H.Round(binary=str(self.stub_dir / "claude"), version="9.9.9")
        rnd.bundled_skills, rnd.bundled_plugins = [], []
        root = H.new_run_root(str(self.plugin))
        ws = root / "workspace"
        (ws / ".claude" / "skills" / "client-follow-up").mkdir(parents=True)
        (ws / ".claude" / "skills" / "client-follow-up" / "SKILL.md").write_text("---\nname: client-follow-up\n---\n")
        self.mode({"extra_skills": ["client-follow-up"], "move_during": ".claude/skills/client-follow-up"})
        H.call(rnd, "skill", root, "run the build skill", cwd=ws, tools=H.SKILL_TOOLS, plugin=root / "plugin")
        # the next call starts with it gone, but the init still names it: a stop, with where it was found
        with self.assertRaisesRegex(H.HarnessFailure,
                                    r"unexpected skills \['client-follow-up'\] \(found: client-follow-up at "
                                    r"workspace/client-follow-up-moved/SKILL.md\)"):
            H.call(rnd, "skill", root, "run the build skill", cwd=ws, tools=H.SKILL_TOOLS, plugin=root / "plugin")
        # one the temp HOME holds (user scope) is never allowed
        shutil.rmtree(ws / ".claude" / "skills")
        (root / "home" / ".claude" / "skills" / "client-follow-up").mkdir(parents=True)
        (root / "home" / ".claude" / "skills" / "client-follow-up" / "SKILL.md").write_text("x")
        with self.assertRaisesRegex(H.HarnessFailure, r"found: client-follow-up at .*home/.claude/skills/client-follow-up/SKILL.md"):
            H.call(rnd, "skill", root, "run the build skill", cwd=ws, tools=H.SKILL_TOOLS, plugin=root / "plugin")

    def test_each_run_has_its_own_tmpdir(self):
        a, b = H.new_run_root(str(self.plugin)), H.new_run_root(str(self.plugin))
        ta, tb = H.env_for(a)["TMPDIR"], H.env_for(b)["TMPDIR"]
        self.assertNotEqual(ta, tb)
        self.assertTrue(ta.startswith(str(a)) and Path(ta).is_dir())

    def test_tool_links_never_point_under_the_home_folder(self):
        """A run root's bin/ links to binaries outside the home folder: one under it is copied to the
        eval parent folder first (ls -l bin, readlink, a program's own path would print it)."""
        fake = H.REAL_HOME / ".local" / "bin"
        fake.mkdir(parents=True)
        (fake / "node").write_text("#!/bin/sh\necho stub-node\n")
        os.chmod(fake / "node", 0o755)
        root = H.new_run_root(str(self.plugin))
        saved = shutil.which
        try:
            H.shutil.which = lambda t, *a, **k: str(fake / "node") if t == "node" else saved(t, *a, **k)
            H._tool_bin(root)
        finally:
            H.shutil.which = saved
        target = os.path.realpath(root / "bin" / "node")
        self.assertFalse(target.startswith(os.path.realpath(H.REAL_HOME)), target)
        self.assertTrue(target.startswith(os.path.realpath(H.eval_parent())), target)
        self.assertEqual((root / "bin" / "node").read_text(), "#!/bin/sh\necho stub-node\n")

    def test_leak_scan_says_what_followed_the_home_path_without_it(self):
        out = self.tmp / "out"
        out.mkdir()
        (out / "events.jsonl").write_text(f'{{"x": "lrwxr-xr-x node -> {H.REAL_HOME}/.local/share/fnm/node"}}\n')
        hits = H.commit_leak_scan(out)
        self.assertEqual(len(hits), 1)
        self.assertIn("home path (near: ", hits[0])
        self.assertIn("node -> ~/.local/share/fnm/node", hits[0])
        self.assertNotIn(str(H.REAL_HOME), hits[0].split(": home path", 1)[1])

    def test_fake_home_only(self):
        self.assertTrue(str(H.REAL_CLAUDE).startswith(str(self.tmp)))
        before = H.real_config_snapshot()
        self.skill_call()
        self.assertEqual(H.compare_snapshots(before, H.real_config_snapshot()), [])

    def test_round_reports_per_tier(self):
        import run_eval as R
        self.mode({"skill_replies": [N_D1]})
        evdir = self.tmp / "evals"
        (evdir / "students").mkdir(parents=True)
        (evdir / "students" / "s.md").write_text("# Leader\n\n## What you know\n- nothing\n\n## When to stop\nReply END.\n")
        exp = [{"text": "Asks N-D1", "kind": "scripted", "check": {"type": "quote", "id": "N-D1"}},
               {"text": "Asks one question", "kind": "judged"}]
        data = {"skill_name": "deconstruct", "how_to_run": "test", "evals": [
            {"id": "C1", "name": "core case", "tier": "core", "prompt": "run the deconstruct skill", "student": "students/s.md",
             "fixture": "empty", "expected_output": "N-D1", "files": [], "expectations": exp,
             "action_target": {"figure": 50, "journey": "the full Deconstruct on a chat platform"}},
            {"id": "R1", "name": "regression case", "tier": "regression", "runs": 1, "prompt": "run the deconstruct skill",
             "student": "students/s.md", "fixture": "empty", "expected_output": "N-D1", "files": [], "expectations": exp}]}
        (evdir / "evals.json").write_text(json.dumps(data))
        out = self.tmp / "out"
        argv = sys.argv
        sys.argv = ["run_eval.py", str(out), "--evals", str(evdir / "evals.json"), "--plugin", str(self.plugin),
                    "--yes", "--parallel", "1"]
        buf = io.StringIO()
        try:
            with redirect_stdout(buf):
                R.main()
        finally:
            sys.argv = argv
        printed = buf.getvalue()
        summary = (out / "summary.md").read_text()
        self.assertIn("Cost estimate", printed)
        self.assertIn("## Tier: core", summary)
        self.assertIn("## Tier: regression", summary)
        self.assertIn("### C1 — core case: PASS", summary)
        self.assertEqual(len(list((out / "C1").glob("run-*"))), 3)  # core runs three times
        self.assertEqual(len(list((out / "R1").glob("run-*"))), 1)
        self.assertIn("tier core: 1 pass", printed)
        rj = json.loads((out / "round.json").read_text())
        self.assertEqual(rj["tiers"], {"core": {"C1": "PASS"}, "regression": {"R1": "PASS"}})
        self.assertEqual(rj["fail_closed_check"], "pass")
        res = json.loads((out / "C1" / "run-1" / "result.json").read_text())
        self.assertIn("the spec's figure: about 50", res["leader_actions"]["report"])
        # the fixture session's start-tree hashes, so a re-grade can tell a fixture changed since
        self.assertEqual(json.loads((out / "C1" / "run-1" / "session-1" / "start-tree.json").read_text()), {})
        self.assertTrue(any(e.get("builtin") == "scripted_lines" and e["passed"] for e in res["expectations"]))
        self.assertTrue(any(e.get("rubric") for e in res["expectations"]))

    def test_core_fails_when_a_scripted_line_is_misquoted(self):
        import run_eval as R
        self.mode({"skill_replies": [N_D1.replace("checklist", "list")]})
        evdir = self.tmp / "evals"
        evdir.mkdir()
        data = {"skill_name": "x", "how_to_run": "t", "evals": [
            {"id": "C1", "name": "core", "tier": "core", "prompt": "go", "fixture": "empty", "expected_output": "",
             "files": [], "expectations": [{"text": "Asks N-D1", "kind": "scripted", "check": {"type": "quote", "id": "N-D1"}}]}]}
        (evdir / "evals.json").write_text(json.dumps(data))
        out = self.tmp / "out"
        argv = sys.argv
        sys.argv = ["run_eval.py", str(out), "--evals", str(evdir / "evals.json"), "--plugin", str(self.plugin), "--yes"]
        try:
            with redirect_stdout(io.StringIO()):
                R.main()
        finally:
            sys.argv = argv
        self.assertIn("### C1 — core: FAIL", (out / "summary.md").read_text())

    def test_no_yes_means_no_calls(self):
        import run_eval as R
        argv = sys.argv
        sys.argv = ["run_eval.py", str(self.tmp / "o"), "I16", "--evals",
                    str(ROOT / "deconstruct-workspace" / "evals" / "evals.json")]
        H.pin_binary = lambda: self.fail("a model call was set up without --yes")
        try:
            with redirect_stdout(io.StringIO()), self.assertRaises(SystemExit) as e:
                R.main()
        finally:
            sys.argv = argv
        self.assertEqual(e.exception.code, 3)


class ExistingEvals(unittest.TestCase):
    def test_a_deconstruct_eval_validates(self):
        errs = V.validate_file(ROOT / "deconstruct-workspace" / "evals" / "evals.json", build=True, only={"NF1", "I16"})
        self.assertEqual(errs, [])

    def test_validator_catches_planted_problems(self):
        with tempfile.TemporaryDirectory() as t:
            bad = {"skill_name": "x", "how_to_run": "t", "evals": [
                {"id": "A", "name": "a", "tier": "gold", "prompt": "go", "fixture": "empty", "expected_output": "",
                 "files": [], "platform": "gemini", "leader_runs": "live",
                 "expectations": [{"text": "q", "kind": "scripted", "check": {"type": "quote", "id": "N-ZZ9"}},
                                  {"text": "y", "kind": "scripted", "check": {"type": "no_yaml", "path": "x"}}]}]}
            Path(t, "evals.json").write_text(json.dumps(bad))
            errs = V.validate_file(Path(t, "evals.json"))
            joined = "\n".join(errs)
            for needle in ("tier 'gold'", "unknown platform 'gemini'", "no approved line N-ZZ9", "no_yaml is retired",
                           "leader_runs 'live'"):
                self.assertIn(needle, joined)


class Corpus(unittest.TestCase):
    def test_shape(self):
        c = AL.load()
        ids = set(c.by_id)
        for must in ("N-F1", "N-F13", "N-B52", "N-B53", "N-B54", "N-T2", "N-T35", "N-T42", "N-R1", "git-save-point",
                     "D5", "D10", "practice-run-line"):
            self.assertIn(must, ids)
        for e in json.loads(AL.DEFAULT_CORPUS.read_text())["lines"]:
            self.assertEqual(set(e) - {"fragment", "note", "clause"}, {"id", "form", "text", "kind", "skills", "files", "source"})
            self.assertIn(e["kind"], ["question", "safety or promise", "teaching", "carried", "structure"])
        self.assertEqual(c.get("N-F13")[0].files["build"], "references/routing.md")
        self.assertEqual(c.get("N-T20")[0].files, {"build": "references/carried-lines.md"})
        self.assertEqual(c.get("N-T20")[0].skills, ["built-workflow"])
        self.assertIn("3c-DI", c.get("N-B54")[0].__dict__.get("source", "") or
                      json.dumps([e for e in json.loads(AL.DEFAULT_CORPUS.read_text())["lines"] if e["id"] == "N-B54"]))



RUNNING_WORK = ("This workflow already runs outside the framework. To bring it in, say 'run the deconstruct skill "
                "on client follow-up. My files are in framework.' Deconstruct pins down what it must produce and how "
                "it should go; until the new version is built and installed, keep running it as it is.")
N_T25 = ("Testing waits for your plan to be approved: say 'run the design skill. "
         "My files are in framework/client-follow-up.'")


class ClauseMarks(unittest.TestCase):
    """A semicolon and a full stop between clauses match each other; a colon stays strict."""

    def test_full_stop_for_semicolon_matches(self):
        said = RUNNING_WORK.replace("should go; until", "should go. Until")
        self.assertTrue(ok({"type": "quote", "id": "running-work"}, run_of(RUNNING_WORK)))
        self.assertTrue(ok({"type": "quote", "id": "running-work"}, run_of(said)))
        self.assertTrue(ok({"type": "scripted_lines"}, run_of(said)))

    def test_semicolon_for_full_stop_matches(self):
        said = RUNNING_WORK.replace("outside the framework. To bring", "outside the framework; to bring")
        self.assertTrue(ok({"type": "quote", "id": "running-work"}, run_of(said)))

    def test_colon_stays_strict(self):
        self.assertTrue(ok({"type": "quote", "id": "N-T25"}, run_of(N_T25)))
        stuffed = N_T25.replace("approved: say", "approved. Say")
        self.assertFalse(ok({"type": "quote", "id": "N-T25"}, run_of(stuffed)))
        second = N_T25.replace("approved: say", "approved: nothing is built yet. Say")
        self.assertFalse(ok({"type": "quote", "id": "N-T25"}, run_of(second)))

    def test_other_marks_stay_strict(self):
        self.assertFalse(ok({"type": "quote", "id": "running-work"},
                            run_of(RUNNING_WORK.replace("should go; until", "should go, until"))))


class ScriptedMarks(unittest.TestCase):
    """The rubric judge's ⟦…⟧ marks: one marker per approved line, its fills inside it."""

    PROMPT = ("Build the agent described in task T2 of design-plan.md, using the requirements in requirements.md. "
              "Both files are in my OneDrive, in Framework/client-follow-up. Everything you need is in those files, "
              "so don't ask me anything they already answer. The agent reads only "
              "Documents/Cowork/client-follow-up/C1-follow-up-style.md, and connects to Outlook (create drafts). "
              "Its instructions must also include these lines, word for word:\n\n- a carried line.")

    def setUp(self):
        import grade_eval as G
        self.mark = G.mark_scripted

    def test_build_prompt_fill_inside_its_marker(self):
        msg = "2. Paste this into the Message Agent Builder box:\n\n```\n" + self.PROMPT + "\n```\n\nSay 'done' when it's made."
        out = self.mark(msg)
        own = re.sub(r"⟦[^⟧]*⟧", " ", out)
        self.assertNotIn("T2", own)  # the task ID is the line's own fill, inside its marker
        self.assertNotIn("⟦⟦", out)  # the shorter "Build the agent described in task" form never nests
        self.assertIn("⟦Build the agent described in task T2 of design-plan.md", out)
        self.assertIn("```", out)  # the code block stays fenced for the judge

    def test_leading_fill_stays_in_its_sentence(self):
        out = self.mark("Now update the record. client-follow-up is made in Copilot's Agent Builder, not here in "
                        "Cowork: 1. Open Copilot, choose Chat, then Agents, then New agent. 2. Paste this into the "
                        "Message Agent Builder box:")
        self.assertTrue(out.startswith("Now update the record. ⟦"), out)

    def test_model_wording_id_stays_outside(self):
        out = self.mark("I'll redo T2 now. " + self.PROMPT)
        self.assertIn("T2", re.sub(r"⟦[^⟧]*⟧", " ", out))


class NearMissScope(unittest.TestCase):
    """Near misses count only the skill under test's lines, and skip edge-word changes on short runs."""

    def test_only_the_skill_under_tests_lines(self):
        msg = "Thanks. " + N_D1.replace("past example", "past sample")  # N-D1 is Deconstruct's
        c = AL.load()
        self.assertTrue(c.near_misses(msg))
        self.assertTrue(c.near_misses(msg, skill="deconstruct"))
        self.assertFalse(c.near_misses(msg, skill="test"))
        run = run_of(msg)
        self.assertTrue(ok({"type": "scripted_lines"}, {**run, "skill": "test"}))
        self.assertFalse(ok({"type": "scripted_lines"}, run))
        out = CS.run_checks({"expectations": []}, run, {"skill_name": "test", "builtin_checks": ["scripted_lines"]})
        self.assertTrue(out[0]["passed"], out[0]["evidence"])
        out = CS.run_checks({"expectations": []}, run, {"skill_name": "deconstruct",
                                                         "builtin_checks": ["scripted_lines"]})
        self.assertFalse(out[0]["passed"])

    def test_edge_word_on_a_short_run_is_skipped(self):
        c = AL.load()
        # N-D16 (main-2) is "It keeps running as it is." (six words)
        first = "The live version keeps running as it is until the new one is built and installed."
        self.assertFalse([x for x in c.near_misses(first) if x[0].id == "N-D16"])
        last = "For now it keeps running as it was before."
        self.assertFalse([x for x in c.near_misses(last) if x[0].id == "N-D16"])
        middle = "For now it keeps working as it is."
        self.assertTrue([x for x in c.near_misses(middle) if x[0].id == "N-D16"])

    def test_shared_start_phrase_alone_is_not_a_near_miss(self):
        c = AL.load()
        own = ("Its plan hasn't been approved. To review and approve it, say 'run the design skill. "
               "My files are in framework/client-follow-up.'")
        self.assertFalse([x for x in c.near_misses(own, skill="build") if x[0].id == "open-item-line"])
        wrong = ("Sending waits for the price. To answer them, say 'run the design skill. "
                 "My files are in framework/client-follow-up.'")
        self.assertTrue([x for x in c.near_misses(wrong, skill="build") if x[0].id == "open-item-line"])

    def test_edge_word_on_a_long_run_still_counts(self):
        c = AL.load()
        msg = N_D1.replace("Do you have", "Did you have")  # first word changed, a run of eight or more
        self.assertTrue(c.near_misses(msg))


class StandInGmail(unittest.TestCase):
    """A Claude Code Build session sees Gmail when the plan uses it (a chat platform's, once the leader
    connects it: ChatPlatformConnections); other cases see no connection."""

    def test_only_build_on_claude_code_with_gmail_in_the_plan(self):
        import run_eval as R
        tmp = Path(tempfile.mkdtemp())
        try:
            ws = tmp / "workspace"
            (ws / "framework" / "cfu").mkdir(parents=True)
            plan = ws / "framework" / "cfu" / "design-plan.md"
            plan.write_text("## Connections\nGmail: the Claude Code connector (use).\n")
            build = {"skill_name": "build"}
            mcp = R.connections_for(L.ClaudeCode(), ws, tmp, build)
            self.assertEqual(mcp["servers"], ["gmail"])
            self.assertNotIn("mcp__gmail__send_message", mcp["allow"])
            self.assertIsNone(R.connections_for(L.ClaudeCode(), ws, tmp, {"skill_name": "test"}))
            # a chat platform's stand-in exists too; run_eval holds it back until the leader connects it
            self.assertEqual(R.connections_for(L.PLATFORMS["chatgpt"](), ws, tmp, build)["servers"], ["gmail"])
            plan.write_text("## Connections\nNone: the draft is shown in the chat.\n")
            self.assertIsNone(R.connections_for(L.ClaudeCode(), ws, tmp, build))
            m365 = ws / "onedrive" / "Framework" / "cfu"
            m365.mkdir(parents=True)
            (m365 / "design-plan.md").write_text("## Connections\nOutlook: the agent's Outlook work content (use).\n")
            mcp = R.connections_for(L.PLATFORMS["microsoft-365"](), ws, tmp, build)
            self.assertEqual(mcp["servers"], ["outlook"])
            self.assertIn("mcp__outlook__create_draft", mcp["allow"])
            self.assertNotIn("mcp__outlook__send_message", mcp["allow"])
        finally:
            shutil.rmtree(tmp, ignore_errors=True)


class SettingsPrompt(unittest.TestCase):
    """The leader's click on Claude Code's settings prompt allows only the workspace's own
    .claude/settings.local.json, and only when the leader hasn't said no (tools/settings_prompt_mcp.py)."""

    def setUp(self):
        sys.path.insert(0, str(EVALS / "tools"))
        import settings_prompt_mcp as SP
        self.SP = SP
        self.tmp = Path(tempfile.mkdtemp())
        self.ws = self.tmp / "workspace"
        (self.ws / ".claude").mkdir(parents=True)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def d(self, tool, path, gate=None, declines=False):
        return self.SP.decide(tool, {"file_path": path}, str(self.ws), gate, declines)[0]

    def test_only_the_settings_file(self):
        target = str(self.ws / ".claude" / "settings.local.json")
        for tool in ("Edit", "Write", "MultiEdit"):
            self.assertTrue(self.d(tool, target))
        self.assertTrue(self.d("Edit", ".claude/settings.local.json"))   # relative to the workspace
        self.assertTrue(self.d("Edit", str(self.ws / ".claude" / ".." / ".claude" / "settings.local.json")))
        self.assertFalse(self.d("Bash", target))
        self.assertFalse(self.SP.decide("Bash", {"command": "python3 -c 'write settings'"}, str(self.ws))[0])
        self.assertFalse(self.d("Write", str(self.ws / ".claude" / "settings.json")))
        self.assertFalse(self.d("Write", str(self.ws / "framework" / ".bin" / "test-run.sh")))
        self.assertFalse(self.d("Write", str(self.tmp / "other" / ".claude" / "settings.local.json")))
        self.assertFalse(self.d("Write", ""))

    def test_builds_own_parts_and_check_agents_are_allowed(self):
        # Build installs into .claude/skills/ and writes check agents into .claude/agents/; Claude Code
        # asks about both and the leader allows them. Bash, the folders themselves and anything
        # outside the workspace stay refused.
        self.assertTrue(self.d("Write", str(self.ws / ".claude" / "skills" / "x" / "SKILL.md")))
        self.assertTrue(self.d("Edit", ".claude/agents/framework-check-x-t2.md"))
        self.assertTrue(self.d("Write", str(self.ws / ".claude" / "skills" / "x" / "SKILL.md"), {"n_b20": "no"}))
        self.assertFalse(self.d("Bash", str(self.ws / ".claude" / "skills" / "x" / "SKILL.md")))
        self.assertFalse(self.d("Write", str(self.ws / ".claude" / "skills")))
        self.assertFalse(self.d("Write", str(self.ws / ".claude" / "skills-x" / "SKILL.md")))
        self.assertFalse(self.d("Write", str(self.ws / ".claude" / "skills" / ".." / "settings.json")))
        self.assertFalse(self.d("Write", str(self.tmp / "other" / ".claude" / "skills" / "x" / "SKILL.md")))

    def test_a_symlink_out_of_the_workspace_is_refused(self):
        (self.tmp / "elsewhere").mkdir()
        (self.ws / "link").symlink_to(self.tmp / "elsewhere")
        self.assertFalse(self.d("Write", str(self.ws / "link" / "settings.local.json")))

    def test_the_leaders_no_and_the_decline_fault_deny(self):
        target = str(self.ws / ".claude" / "settings.local.json")
        self.assertTrue(self.d("Edit", target, {"n_b20": "ok"}))
        self.assertTrue(self.d("Edit", target, {"n_b20": "unseen"}))
        self.assertFalse(self.d("Edit", target, {"n_b20": "no"}))
        self.assertFalse(self.d("Edit", target, {"n_b20": "ok"}, declines=True))

    def test_answer_logs_each_decision_relative_to_the_workspace(self):
        log = self.tmp / "log.jsonl"
        env = {"SETTINGS_PROMPT_WORKSPACE": str(self.ws), "SETTINGS_PROMPT_LOG": str(log),
               "SETTINGS_PROMPT_GATE": str(self.tmp / "missing.json")}
        saved = {k: os.environ.get(k) for k in env}
        os.environ.update(env)
        try:
            a = self.SP.answer({"tool_name": "Write", "input": {"file_path": str(self.ws / ".claude" / "settings.local.json")}})
            b = self.SP.answer({"tool_name": "Write", "input": {"file_path": str(self.ws / "x.txt")}})
        finally:
            for k, v in saved.items():
                os.environ.pop(k, None) if v is None else os.environ.__setitem__(k, v)
        self.assertEqual(a["behavior"], "allow")
        self.assertEqual(b["behavior"], "deny")
        rows = [json.loads(x) for x in log.read_text().splitlines()]
        self.assertEqual([r["decision"] for r in rows], ["allow", "deny"])
        self.assertEqual(rows[0]["path"], os.path.join(".claude", "settings.local.json"))
        self.assertNotIn(str(self.tmp), log.read_text())

    def test_n_b20_state_from_the_conversation(self):
        ask = ("To set this up I need to block Gmail's send from making changes while I check them, in your "
               "Claude Code settings for this project. Shall I go ahead?")
        conv = [{"role": "student", "text": "run the build skill"}, {"role": "ai", "text": ask}]
        self.assertEqual(H.n_b20_state(conv[:1]), "unseen")
        self.assertEqual(H.n_b20_state(conv + [{"role": "student", "text": "Yes, go ahead."}]), "ok")
        self.assertEqual(H.n_b20_state(conv + [{"role": "student", "text": "No, not now."}]), "no")
        other = [{"role": "ai", "text": "To set this up I need to connect Gmail in Claude. Shall I go ahead?"},
                 {"role": "student", "text": "no"}]
        self.assertEqual(H.n_b20_state(other), "unseen")  # N-B20 about something other than the settings

    def test_only_build_and_test_on_claude_code(self):
        import run_eval as R
        root = self.tmp / "root"
        root.mkdir()
        pt = R.settings_prompt_for(L.ClaudeCode(), self.ws, root, {"skill_name": "build"})
        self.assertEqual(pt["tool"], "mcp__leader_click__approve")
        cfg = json.loads(Path(pt["config"]).read_text())["mcpServers"]["leader_click"]
        self.assertNotIn("SETTINGS_PROMPT_DENY", cfg["env"])
        self.assertIsNotNone(R.settings_prompt_for(L.ClaudeCode(), self.ws, root, {"skill_name": "test"}))
        self.assertIsNone(R.settings_prompt_for(L.ClaudeCode(), self.ws, root, {"skill_name": "design"}))
        self.assertIsNone(R.settings_prompt_for(L.PLATFORMS["codex"](), self.ws, root, {"skill_name": "build"}))
        pt = R.settings_prompt_for(L.ClaudeCode(), self.ws, root, {"skill_name": "build"},
                                   ev={"platform_faults": ["leader_denies_settings_prompt"]})
        cfg = json.loads(Path(pt["config"]).read_text())["mcpServers"]["leader_click"]
        self.assertEqual(cfg["env"]["SETTINGS_PROMPT_DENY"], "1")
        self.assertIn("leader_denies_settings_prompt", V.FAULTS)


class NoAddedFiles(unittest.TestCase):
    """no_added_files compares the end tree with the session's start tree (the fixture's own files)."""

    def test_fixture_files_dont_count(self):
        start = {"framework/client-follow-up/test-results.md": "round: 1",
                 "framework/client-follow-up/history/set-aside-1/test-results.md": "old"}
        run = run_of("hi", files_start=start, files_end=dict(start))
        self.assertTrue(ok({"type": "no_added_files", "session": 1}, run))
        # the old check this replaced reads fixture files as written ones
        self.assertFalse(ok({"type": "file_absent", "path": "framework/*/test-results.md", "session": 1}, run))

    def test_an_added_file_fails(self):
        start = {"framework/client-follow-up/requirements.md": "x"}
        end = {**start, "framework/client-follow-up/test-results.md": "round: 1"}
        passed, why = CS.check({"type": "no_added_files", "session": 1}, run_of("hi", files_start=start, files_end=end))
        self.assertFalse(passed)
        self.assertIn("test-results.md", why)
        self.assertTrue(ok({"type": "no_added_files", "except": ["*/test-results.md"], "session": 1},
                           run_of("hi", files_start=start, files_end=end)))


if __name__ == "__main__":
    unittest.main()
