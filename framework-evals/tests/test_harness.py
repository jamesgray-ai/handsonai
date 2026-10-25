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
                 "files": [], "platform": "gemini",
                 "expectations": [{"text": "q", "kind": "scripted", "check": {"type": "quote", "id": "N-ZZ9"}},
                                  {"text": "y", "kind": "scripted", "check": {"type": "no_yaml", "path": "x"}}]}]}
            Path(t, "evals.json").write_text(json.dumps(bad))
            errs = V.validate_file(Path(t, "evals.json"))
            joined = "\n".join(errs)
            for needle in ("tier 'gold'", "unknown platform 'gemini'", "no approved line N-ZZ9", "no_yaml is retired"):
                self.assertIn(needle, joined)


class Corpus(unittest.TestCase):
    def test_shape(self):
        c = AL.load()
        ids = set(c.by_id)
        for must in ("N-F1", "N-F13", "N-B52", "N-B53", "N-B54", "N-T2", "N-T35", "N-T42", "N-R1", "git-save-point",
                     "D5", "D10", "practice-run-line"):
            self.assertIn(must, ids)
        for e in json.loads(AL.DEFAULT_CORPUS.read_text())["lines"]:
            self.assertEqual(set(e) - {"fragment", "note"}, {"id", "form", "text", "kind", "skills", "files", "source"})
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
    """A Claude Code Build session sees Gmail when the plan uses it; other cases see no connection."""

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
            self.assertIsNone(R.connections_for(L.PLATFORMS["chatgpt"](), ws, tmp, build))
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
