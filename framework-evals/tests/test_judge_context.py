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


class PickedCard(unittest.TestCase):
    """smoke-1 fix: a cut Analyze report still shows the picked workflow's card and summary row."""
    REPORT = ("# AI Opportunity Report\n\n" + "Filler line that pads the report head out past the cut.\n" * 60
              + "\n### Detailed Opportunity Cards\n\n---\n\n**1 Client Follow-Up**\n\n**Goal:** Keep renewals on time\n\n---\n\n"
              "**2 Weekly Pipeline Summary**\n\n**Goal:** Win two clients\n\n---\n\n## Workflow Candidate Summary\n\n"
              "| Field | Content |\n|-------|---------|\n| **Workflow** | Client Follow-Up |\n| **Frequency** | Daily |\n\n"
              "| Field | Content |\n|-------|---------|\n| **Workflow** | Weekly Pipeline Summary |\n| **Frequency** | Weekly |\n")

    def test_picked_slugs_and_blocks(self):
        run = {"sessions": [{"files_start": {"framework/ai-opportunity-report.md": self.REPORT},
                             "files_end": {"framework/ai-opportunity-report.md": self.REPORT,
                                           "framework/client-follow-up/deconstruct-in-progress.md": "x"}}]}
        slugs = G.picked_slugs(run)
        self.assertEqual(slugs, {"client-follow-up"})
        out = G.picked_blocks(self.REPORT, slugs, self.REPORT[:G.READ_FILE_CAP])
        self.assertIn("**1 Client Follow-Up**", out)
        self.assertIn("| **Frequency** | Daily |", out)
        self.assertNotIn("Weekly", out)
        self.assertEqual(G.picked_blocks(self.REPORT, set(), ""), "")

    def test_summary_row_first_and_after_a_changed_node(self):
        # smoke-2 fix (M-light-scheduled): "Ends with: A one-page priorities note" was judged invented. The card's
        # prose filled the cap ahead of its summary table, and a changed Workflow node (ranked before the report)
        # overwrote the picked workflows, so no card was shown past the cut at all
        prose = "**1 Client Follow-Up**\n\n" + "**Note:** A long line of card prose about the follow-up work.\n" * 23
        report = self.REPORT.replace("**1 Client Follow-Up**\n\n**Goal:** Keep renewals on time\n", prose)
        report = report.replace("| **Frequency** | Daily |", "| **Deliverable** | A one-page follow-up email |\n| **Frequency** | Daily |")
        self.assertIn("A one-page follow-up email", G.picked_blocks(report, {"client-follow-up"}, report[:G.READ_FILE_CAP]))
        node = "registry/workflows/client-follow-up.md"
        before = "---\ntitle: Client Follow-Up\nstatus: backlog\ndescription: Drafts the follow-up email after each client call.\n---\n"
        after = before.replace("status: backlog", "status: under-development")
        run = run_with([tool_result(report + "\n" + before)],
                       {"framework/ai-opportunity-report.md": report, node: before})
        run["sessions"][0]["files_end"] = {"framework/ai-opportunity-report.md": report, node: after}
        self.assertIn("A one-page follow-up email", G.files_read(run, ["x"]))


class BuildRoundContext(unittest.TestCase):
    """Build rounds 2026-11-18: about 44% of the rubric-6 flags were backed by what the judge wasn't
    shown: the session's tool list, the practice inputs, platform-docs.json, and tool results cut short."""

    INIT = {"type": "system", "subtype": "init", "tools": [
        "Read", "Bash", "Task", "mcp__gmail__get_profile", "mcp__gmail__list_messages",
        "mcp__gmail__create_draft", "mcp__gmail__send_message"]}

    def test_the_session_tool_list_names_each_connection_action(self):
        msg = "This Gmail connection also offers a send action, and it can't delete drafts."
        run = run_with([self.INIT], text=msg)
        offered = G.session_tools(run)
        self.assertIn("mcp__gmail__send_message", offered)
        self.assertNotIn("delete_draft", offered)
        self.assertIn("other tools: Read, Bash, Task", offered)
        head = G.rubric_prompt(run)[1].split("## Message 1")[0]
        self.assertIn("## The tools the session was offered", head)
        self.assertIn("mcp__gmail__create_draft", head)

    def test_a_connection_added_partway_is_in_the_tool_list(self):
        # Re-grade 2026-11-19: Gmail is connected mid-session, so only a later init lists its tools.
        first = {"type": "system", "subtype": "init", "tools": ["Read", "Bash"]}
        run = run_with([first, self.INIT], text="This Gmail connection also offers a send action.")
        offered = G.session_tools(run)
        self.assertIn("mcp__gmail__send_message", offered)
        self.assertEqual(offered.count("Read"), 1)

    def test_the_practice_inputs_are_shown_whole(self):
        files = {"framework/client-follow-up/inputs/E1-acme-renewal-call.md":
                 "source: deconstruct\ntests: AC1\n\nCall with Dana Ortiz (Acme). Lee was happy with the reporting.",
                 "framework/client-follow-up/requirements.md": "W1 · Gmail · create a draft"}
        msg = "Dana Ortiz said Lee was happy with the reporting."
        run = run_with([], files=files, text=msg)
        out = G.practice_inputs(run)
        self.assertIn("inputs/E1-acme-renewal-call.md", out)
        self.assertIn("Lee was happy with the reporting", out)
        self.assertNotIn("requirements.md", out)
        self.assertIn("## The workflow's practice inputs the leader brought", G.rubric_prompt(run)[1])

    def test_the_platform_docs_entry_of_the_sessions_platform(self):
        msg = "OpenAI's page \"Skills in ChatGPT\" (help.openai.com/en/articles/20001066-skills-in-chatgpt) shows it."
        run = run_with([], text=msg)
        run["sessions"][0]["platform"] = "chatgpt"
        out = G.platform_docs(run, [msg])
        self.assertIn("ChatGPT:", out)
        self.assertIn("help.openai.com", out)
        self.assertNotIn("Claude Code:", out)
        # another platform's entry only when a message names one of its pages
        run["sessions"][0]["platform"] = "claude-code"
        self.assertIn("ChatGPT:", G.platform_docs(run, [msg]))
        self.assertNotIn("ChatGPT:", G.platform_docs(run, ["nothing linked"]))
        self.assertIn("## The platform's official pages", G.rubric_prompt(run)[1])

    def test_a_short_check_result_is_shown_with_its_command(self):
        # LV-staged runs: "Nothing is scheduled on this computer" rested on crontab -l and a LaunchAgents look
        big = "x" * 5000
        events = (call_and_result(1, "Bash", {"command": "cat framework/x/build-record.md"}, big)
                  + call_and_result(2, "Bash", {"command": "crontab -l 2>&1; ls ~/Library/LaunchAgents 2>&1"},
                                    "crontab: no crontab for leader\nls: /x/home/Library/LaunchAgents: No such file or directory")
                  + call_and_result(3, "mcp__gmail__create_draft", {"to": "alex@brightline.example", "subject": "Build check, delete me"},
                                    "Draft created: r-123")
                  + call_and_result(4, "Bash", {"command": f"cat {REF}"}, "Example: within 48 hours"))
        run = run_with(events, text="Nothing is scheduled on this computer.")
        out = G.tool_calls(run)
        self.assertIn("$ crontab -l 2>&1; ls ~/Library/LaunchAgents 2>&1\ncrontab: no crontab for leader", out)
        self.assertIn('mcp__gmail__create_draft {"to": "alex@brightline.example"', out)
        self.assertLess(out.index("crontab -l"), out.index("cat framework/x/build-record.md"))  # short results first
        self.assertIn("[…cut]", out)
        self.assertNotIn("within 48 hours", out)  # a read of the step's own text is never a tool result
        self.assertIn("## The AI's own commands and connection calls", G.rubric_prompt(run)[1])

    def test_platform_skill_calls_and_edits_outside_the_plugin_are_shown(self):
        # build-full-1 (2026-11-21): Skill("schedule", "list") answered in a synthetic message, and an Edit
        # that paused the older skill, were invisible to the judge
        synth = {"type": "user", "isSynthetic": True, "message": {"role": "user", "content": [
            {"type": "text", "text": "We're having trouble connecting with your remote claude.ai account."}]}}
        events = (call_and_result(1, "Skill", {"skill": "schedule", "args": "list"}, "Launching skill: schedule")
                  + [synth]
                  + call_and_result(2, "Skill", {"skill": "handsonai:build"}, "Launching skill: handsonai:build")
                  + call_and_result(3, "Edit", {"file_path": "/tmp/x/workspace/.claude/skills/client-follow-up/SKILL.md",
                                                "old_string": "description: x", "new_string":
                                                "description: x\ndisable-model-invocation: true"}, "updated")
                  + call_and_result(4, "Write", {"file_path": "/tmp/x/plugin/skills/build/SKILL.md", "content": "nope"},
                                    "written"))
        out = G.tool_calls(run_with(events))
        self.assertIn('Skill schedule "list"\nLaunching skill: schedule\nWe\'re having trouble connecting', out)
        self.assertNotIn("handsonai:build", out)
        self.assertIn("Edit /tmp/x/workspace/.claude/skills/client-follow-up/SKILL.md: description: x "
                      "disable-model-invocation: true", out)
        self.assertNotIn("/tmp/x/plugin/", out)

    def test_tool_lines_keep_more_of_each_line(self):
        line = "commit 1a2b3c " + "word " * 50 + "my skill 2026-10-20"
        msg = "Your Git history has the commit from 2026-10-20 called my skill."
        self.assertIn("my skill 2026-10-20", G.tool_lines(run_with([tool_result(line)], text=msg), [msg]))

    def test_a_short_count_is_matched_with_the_word_after_it(self):
        # trial 2026-11-19: "71 words" was backed by the check agent's "Word count: 71", but facts
        # under 3 characters were dropped, so the judge flagged it as invented
        msg = "The draft came to 71 words, under your limit."
        results = [tool_result("Word count: 71"), tool_result("Found 71 rows")]
        out = G.tool_lines(run_with(results, text=msg), [msg])
        self.assertIn("Word count: 71", out)
        self.assertNotIn("Found 71 rows", out)  # the number alone, without its word, isn't enough

    def test_the_settings_a_session_wrote_are_shown(self):
        # trial 3: "the four test-run.sh lines under allow" was true but flagged; .claude/ was never shown
        settings = '{"permissions": {"allow": ["Bash(framework/.bin/test-run.sh *)"]}}'
        run = {"sessions": [{"files_start": {}, "files_end": {".claude/settings.local.json": settings}}]}
        self.assertIn("test-run.sh", G.settings_files(run))
        same = {"sessions": [{"files_start": {".claude/settings.local.json": settings},
                              "files_end": {".claude/settings.local.json": settings}}]}
        self.assertEqual(G.settings_files(same), "")

    def test_a_file_staged_then_cleared_is_listed(self):
        # trial 4: the staging in package/ was removed after the install, so the judge never saw it
        write = {"type": "assistant", "message": {"content": [{"type": "tool_use", "name": "Write", "input": {
            "file_path": "/tmp/x/workspace/framework/w/package/skills/s/SKILL.md", "content": "x"}}]}}
        run = run_with([write])
        s = run["sessions"][0]
        s["files_end"] = {}
        self.assertEqual(G.written_then_gone(s), ["framework/w/package/skills/s/SKILL.md"])
        s["files_end"] = {"framework/w/package/skills/s/SKILL.md": "x"}
        self.assertEqual(G.written_then_gone(s), [])

    def test_a_file_staged_by_a_heredoc_then_cleared_is_listed(self):
        # trial 6: the shared skill was staged with `cat > ... <<'EOF'`, which only Write/Edit tracking missed
        cmd = ("cd /tmp/x/workspace/framework/w; mkdir -p package/skills/d; cat > package/skills/d/SKILL.md <<'EOF'\n"
               "text\nEOF\nls -R package 2>/dev/null >&2")
        bash = {"type": "assistant", "message": {"content": [{"type": "tool_use", "name": "Bash",
                                                              "input": {"command": cmd}}]}}
        run = run_with([bash])
        s = run["sessions"][0]
        s["files_end"] = {}
        self.assertEqual(G.written_then_gone(s), ["framework/w/package/skills/d/SKILL.md"])

if __name__ == "__main__":
    unittest.main()


class SkillPlatformFacts(unittest.TestCase):
    """F4 (shape release): the judge reads the skill's own references/platform-facts.md, so a statement
    those rules back isn't flagged as invented."""

    def plugin_run(self, with_facts):
        t = Path(tempfile.mkdtemp())
        ref = t / "plugin" / "skills" / "build" / "references"
        ref.mkdir(parents=True)
        if with_facts:
            (ref / "platform-facts.md").write_text("MARKER-PF: never make up a menu path.\n")
        ws = t / "run" / "workspace"
        ws.mkdir(parents=True)
        (ws.parent / "events.jsonl").write_text("")
        return {"skill": "build", "sessions": [{"root": str(ws), "files_start": {},
                                                 "turns": [{"role": "ai", "text": "x"}]}]}

    def test_platform_facts_in_judge_context(self):
        run = self.plugin_run(True)
        self.assertIn("MARKER-PF", G.skill_platform_facts(run, "build"))
        _, prompt = G.rubric_prompt(run)
        self.assertIn("## The skill's platform rules", prompt)
        self.assertIn("MARKER-PF", prompt)

    def test_platform_facts_missing_is_empty(self):
        run = self.plugin_run(False)
        self.assertEqual(G.skill_platform_facts(run, "build"), "")
        _, prompt = G.rubric_prompt(run)
        self.assertNotIn("## The skill's platform rules", prompt)
