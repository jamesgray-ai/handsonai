#!/usr/bin/env python3
"""Build the workspace a Design eval starts from, in this release's formats (T23).

Usage: python3 make_fixture.py <fixture-name> <target-dir>
       python3 make_fixture.py --list

Every fixture is a whole Claude Code workspace (`framework/`, `registry/`, and `.claude/skills/`
once built); the harness's platform simulations move it into a drive or OneDrive for other
platforms. Two sources:

- framework-fixtures/ (the shared routing-state library): most entry and update evals point at a
  variant folder directly (`dir:../../framework-fixtures/...`); the names here are the combinations
  that library doesn't hold (a built earlier-version plan, an edited skill, change requests of each
  kind, a requirements file missing a section, and so on).
- workflows/ (this folder): hand-written requirements in the 10.0 format, one per route and choice
  design.md 14 tests, each added beside Client Follow-Up in the state-4 registry. Every one passes
  tools/requirements-check.js. They stand in for files the finished Deconstruct produced until T45
  and T71 regenerate them from real runs.

Every fixture with a registry ends with its views recomposed (compose-registry.js), so the
registry lints clean and compose --check passes before the eval starts; a node never links a file
the fixture removed.

Built fixtures get real fingerprints (`sha256:` + the hex digest of the installed file), so a
Design that compares what's installed with the build record finds an edit only where a fixture
made one.
"""
import hashlib
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
FF = ROOT / "framework-fixtures"
WF = HERE / "workflows"
CFU = "client-follow-up"
S04 = "states/s04-plan-needed/with-registry"
S11 = "states/s11-live/with-registry"


# ---------- helpers ----------

def ff(t, rel):
    shutil.copytree(FF / rel, t, symlinks=True)


def wf_dir(t, slug):
    return Path(t) / "framework" / slug


def sub(path, old, new, count=1):
    p = Path(path)
    text = p.read_text()
    if old not in text:
        sys.exit(f"{p}: {old!r} not found")
    p.write_text(text.replace(old, new, count))


def add_workflow(t, slug, title, description, trigger, status="under-development", registry=True):
    """Copy workflows/<slug> into the workspace and give it a Workflow node."""
    shutil.copytree(WF / slug, wf_dir(t, slug))
    if not registry or not (Path(t) / "registry").is_dir():
        return
    node = Path(t) / "registry" / "workflows" / f"{slug}.md"
    node.write_text(
        "---\ntype: Workflow\n"
        f'title: "{title}"\n'
        f'description: "{description}"\n'
        "generated: { by: process:deconstruct, at: 2026-10-20T10:00:00Z }\n"
        f"status: {status}\n"
        f'trigger: "{trigger}"\n'
        "---\n"
        f"# {title}\n\n{description}\n\n# Artifacts\n\n"
        f"- [Requirements](framework/{slug}/requirements.md)\n\n# Skills\n\n\n# Agents\n"
    )
    idx = Path(t) / "registry" / "workflows" / "index.md"
    idx.write_text(idx.read_text().rstrip("\n") + f"\n- [{title}](/workflows/{slug}.md)\n")


def add_skill(t, name, description, body, used_by=None):
    """An installed skill the leader already has, optionally linked from another workflow's node."""
    d = Path(t) / ".claude" / "skills" / name
    d.mkdir(parents=True, exist_ok=True)
    (d / "SKILL.md").write_text(f"---\nname: {name}\ndescription: {description}\n---\n\n{body}\n")
    if used_by and (Path(t) / "registry").is_dir():
        slug, title, desc = used_by
        node = Path(t) / "registry" / "workflows" / f"{slug}.md"
        node.write_text(
            "---\ntype: Workflow\n"
            f'title: "{title}"\n'
            f'description: "{desc}"\n'
            "generated: { by: process:build, at: 2026-09-15T10:00:00Z }\n"
            "status: in-production\n"
            'trigger: "You ask for it"\n'
            "---\n"
            f"# {title}\n\n{desc}\n\n# Artifacts\n\n\n# Skills\n\n- [{name}](.claude/skills/{name}/SKILL.md)\n\n# Agents\n"
        )
        idx = Path(t) / "registry" / "workflows" / "index.md"
        idx.write_text(idx.read_text().rstrip("\n") + f"\n- [{title}](/workflows/{slug}.md)\n")
        # an in-production workflow joins a Process (registry-bundle.md rule 5; the lint's error otherwise)
        proc = Path(t) / "registry" / "processes" / "client-relationship-management.md"
        if proc.exists():
            proc.write_text(proc.read_text().rstrip("\n") + f"\n- [{title}](/workflows/{slug}.md)\n")


def drop_links(t, slug, *labels, skills=False):
    """Take a node's links to files a fixture removed off it, as the step that removed them would
    (registry-bundle.md rule 7: no link to a moved file): `labels` from # Artifacts, and with
    skills=True every # Skills entry."""
    node = Path(t) / "registry" / "workflows" / f"{slug}.md"
    if not node.exists():
        return
    text = node.read_text()
    for label in labels:
        text = re.sub(rf"(?m)^- \[{re.escape(label)}\]\([^)]*\)\n", "", text)
    if skills:
        text = re.sub(r"(?ms)(^# Skills\n).*?(?=^# )", r"\1\n\n", text)
        # and the skills inventory compose wrote from them (compose refuses to run past a broken link)
        idx = Path(t) / "registry" / "index.md"
        if idx.exists():
            idx.write_text(re.sub(rf"(?m)^- \[[^\]]+\]\(\.claude/skills/{re.escape(slug)}/SKILL\.md\).*\n", "",
                                  idx.read_text()))
    node.write_text(text)


def compose(t):
    """Regenerate the registry's views (REGISTRY.md, indexes, GENERATED blocks) from the fixture's
    nodes, as a step's maintenance pass leaves them, so lint-registry and compose --check start clean."""
    if not (Path(t) / "registry" / "SCHEMA.md").exists():
        return
    r = subprocess.run(["node", str(ROOT / "plugins" / "handsonai" / "tools" / "compose-registry.js"), "registry"],
                       cwd=t, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"compose-registry failed on the fixture: {r.stdout[-600:]}{r.stderr[-600:]}")


def digest(path):
    return "sha256:" + hashlib.sha256(Path(path).read_bytes()).hexdigest()


def real_fingerprints(t, slug=CFU):
    """Point the build record's fingerprints at the files as installed now."""
    rec = wf_dir(t, slug) / "build-record.md"
    if not rec.exists():
        return
    skill = Path(t) / ".claude" / "skills" / slug / "SKILL.md"
    ctx = Path(t) / ".claude" / "skills" / slug / "references" / "follow-up-style.md"
    text = rec.read_text()
    if skill.exists():
        text = re.sub(rf"(?m)^(  {re.escape(slug)}: )sha256:\S+", lambda m: m.group(1) + digest(skill), text)
    if ctx.exists():
        text = re.sub(r"(?m)^(  follow-up-style\.md: )sha256:\S+", lambda m: m.group(1) + digest(ctx), text)
    rec.write_text(text)


def live(t, rel=S11):
    ff(t, rel)
    real_fingerprints(t)


def bump_requirements(t, slug, lines, by="deconstruct"):
    req = wf_dir(t, slug) / "requirements.md"
    sub(req, "revision: 1\n", "revision: 2\n")
    sub(req, "revisions: []\n", f"revisions:\n  - revision: 2\n    by: {by}\n    lines: [{', '.join(lines)}]\n")


# ---------- the routes (design.md 14 item 2) ----------

def on_s04(slug, title, description, trigger):
    def build(t):
        ff(t, S04)
        add_workflow(t, slug, title, description, trigger)
    return build


fx_regulated_same_way = on_s04(
    "expense-report-approval", "Expense Report Approval",
    "Checks each submitted expense report against the expense policy and recommends approve or return, for the controller to sign off.",
    "An employee submits an expense report")
fx_regulated_some_of_each = on_s04(
    "vendor-onboarding", "Vendor Onboarding",
    "Screens each new vendor and assembles its onboarding file, for the procurement manager to approve.",
    "A project lead submits a new vendor request")
fx_split_part = on_s04(
    "board-update", "Monthly Board Update",
    "Drafts the monthly board update from the finance pack and the team updates, for the CEO to edit and send.",
    "Finance shares the month-end pack")
fx_domains = on_s04(
    "competitor-research-brief", "Competitor Research Brief",
    "Researches a competitor question across public sources and writes a sourced brief, for the product lead to read.",
    "The product team asks a competitor question")
fx_planned_steps = on_s04(
    "invoice-coding", "Invoice Coding",
    "Codes each supplier invoice to the right account and cost centre, for the bookkeeper to check and enter.",
    "A supplier invoice arrives in the accounts inbox")


# ---------- the choices (item 3) ----------

def fx_reuse(t):  # Client Follow-Up beside an installed skill that drafts client emails, shared with Client Check-In
    ff(t, S04)
    add_skill(t, "drafting-client-emails",
              "This skill should be used when the user asks to draft an email to a client from notes. Drafts a plain-text client email in the house style.",
              "# Drafting client emails\n\n1. Read the notes.\n2. Draft a plain-text email in the house style: greeting, three short paragraphs, sign-off.\n3. Put the draft in Gmail Drafts.",
              used_by=("client-check-in", "Client Check-In",
                       "Drafts a quarterly check-in email to each client from your account notes."))


def fx_regime_unchecked(t):
    fx_domains(t)
    sub(wf_dir(t, "competitor-research-brief") / "requirements.md", "Governing regime: None", "Governing regime: Not sure — to check")


def fx_cannot_meet(t):
    fx_regulated_same_way(t)
    sub(wf_dir(t, "expense-report-approval") / "requirements.md",
        "| P1 | Expense reports and receipts stay inside the finance team's systems. | Finance policy FIN-07 |",
        "| P1 | Expense reports and receipts never leave our own servers: no AI service outside the company may read them. | Finance policy FIN-07 |")


def fx_no_connection(t):
    fx_regulated_same_way(t)
    req = wf_dir(t, "expense-report-approval") / "requirements.md"
    sub(req, "- W1 · NetSuite · post the approved expense report · Step 5",
        "- W1 · Acme Ledger (our in-house finance system; it has no connection) · post the approved expense report · Step 5")
    sub(req, "produces a posted expense report in NetSuite", "produces a posted expense report in Acme Ledger")


# open-ended research that runs without the leader and writes to a live system: Autonomous is the least
# that does the job. (Deal Hygiene, the first version, had one input and a stated criterion, so Design
# rightly planned it Guided and asked D5″ in all six core runs, 10-28.) W1, a label in the leader's own
# inbox, can be undone; W2, an entry on a tracker page the team reads, can't.
fx_d5_autonomous = on_s04(
    "competitor-watch", "Competitor Watch",
    "Researches what each tracked competitor changed every night, across public sources and their newsletters, and records each change in the team's competitor tracker.",
    "Every night at 1am")
fx_d5_guided = on_s04(
    "support-triage", "Support Triage",
    "Triages each new support email by your priority rules, flags urgent ones to the escalation channel and drafts a first reply.",
    "A new email arrives in the support inbox")
fx_shared_record = on_s04(
    "meeting-notes-to-crm", "Meeting Notes to CRM",
    "Turns your meeting notes into the deal's next step and updates it in HubSpot once you've checked it.",
    "You finish a sales meeting and paste in your notes")


# ---------- the cap (item 4) ----------

def fx_cap_seven(t):
    ff(t, S04)
    add_workflow(t, "renewal-risk-monitor", "Renewal Risk Monitor",
                 "Works out each week which customers are at risk of not renewing and why, and gives each account owner a task to act on it.",
                 "Every Monday at 6am")
    add_skill(t, "summarizing-support-tickets",
              "This skill should be used when the user asks to summarise a customer's support tickets. Summarises the last 90 days of a customer's Zendesk tickets into themes and open issues.",
              "# Summarising support tickets\n\n1. Read the customer's tickets from the last 90 days.\n2. Group them into themes.\n3. List the open issues with their age.",
              used_by=("weekly-support-report", "Weekly Support Report",
                       "Summarises the week's support tickets for the support lead."))


fx_cap_safety = on_s04(
    "launch-announcer", "Launch Announcer",
    "Announces each release in every channel it belongs in, from the release notes, as soon as the release is marked ready.",
    "A release is marked ready in the release tracker")


def fx_light_cap(t):
    ff(t, S04)
    add_workflow(t, "reading-list-digest", "Reading List Digest",
                 "Summarises the articles you saved this week into a one-page digest, for you to read on Friday.",
                 "You ask for this week's digest")
    add_skill(t, "summarizing-articles",
              "This skill should be used when the user asks to summarise an article from a link. Writes a three-line summary of one article.",
              "# Summarising articles\n\n1. Read the article at the link.\n2. Write three lines: the claim, the evidence, why it matters.")


# ---------- the light track (item 13) and schedules (items 7, 11) ----------

fx_light_switch = on_s04(
    "prospect-snapshot", "Prospect Snapshot",
    "Turns a prospect's website and recent news into a half-page snapshot, for you to read before your first call.",
    "You book a first call and paste in the prospect's website and news")
fx_scheduled = on_s04(
    "weekly-pipeline-post", "Weekly Pipeline Post",
    "Summarises the open pipeline every Monday morning and posts it for the sales team once the sales manager approves it.",
    "Every Monday at 8am")


# ---------- entry (item 1) ----------

def fx_live(t):
    live(t)


def fx_live_no_registry(t):
    live(t, "states/s11-live/no-registry")


def fx_wrong_place(t):  # the live workflow's own place: its skill and context copy, no framework files
    src = FF / S11
    t.mkdir(parents=True)
    shutil.copytree(src / ".claude", t / ".claude")


def fx_missing_section(t):  # requirements with no Rules & Constraints section, nothing built
    ff(t, S04)
    req = wf_dir(t, CFU) / "requirements.md"
    text = req.read_text()
    req.write_text(re.sub(r"## Rules & Constraints\n.*?(?=## Human Gates)", "", text, flags=re.S))


def fx_built_missing_section(t):  # the same, on a live workflow
    live(t)
    req = wf_dir(t, CFU) / "requirements.md"
    text = req.read_text()
    req.write_text(re.sub(r"## Rules & Constraints\n.*?(?=## Human Gates)", "", text, flags=re.S))


def fx_earlier_plan_built(t):  # a live workflow whose plan is a 9.x design-spec.md: Design owns state 1, N-B44 first
    live(t)
    d = wf_dir(t, CFU)
    shutil.copy(FF / "earlier-version/v1-design-spec/with-registry/framework/client-follow-up/design-spec.md", d / "design-spec.md")
    (d / "design-plan.md").unlink()
    node = Path(t) / "registry" / "workflows" / f"{CFU}.md"
    sub(node, "- [Design plan](framework/client-follow-up/design-plan.md)",
        "- [Design spec](framework/client-follow-up/design-spec.md)")
    # an older node (a bare-date stamp) may carry the earlier label (registry-bundle.md rule 2)
    text = node.read_text()
    node.write_text(re.sub(r"(?m)^(generated: \{ by: [^,]+, at: )(\d{4}-\d\d-\d\d)T[^ ]+ \}", r"\1\2 }", text, count=1))


def fx_retired(t):
    ff(t, "states/s00-retired/with-registry")
    real_fingerprints(t)


def fx_retired_no_record(t):  # retired, never built: requirements and an approved plan only (Build is next)
    ff(t, "states/s00-retired/with-registry")
    d = wf_dir(t, CFU)
    for f in ("build-record.md", "test-results.md"):
        (d / f).unlink()
    shutil.rmtree(Path(t) / ".claude", ignore_errors=True)
    drop_links(t, CFU, "Test results", skills=True)


def fx_retired_no_requirements(t):  # retired, its folder empty of framework files: Deconstruct is next
    ff(t, "states/s00-retired/with-registry")
    d = wf_dir(t, CFU)
    for f in ("build-record.md", "test-results.md", "design-plan.md", "requirements.md"):
        (d / f).unlink()
    shutil.rmtree(Path(t) / ".claude", ignore_errors=True)
    drop_links(t, CFU, "Requirements", "Design plan", "Test results", skills=True)


def fx_switched_off_no_registry(t):  # no registry: a workflow the leader switched off still reads as live
    ff(t, "states/s00-retired/no-registry")
    real_fingerprints(t)


def fx_rerun_consequential(t):  # a Deconstruct re-run before anything is built that makes it send the email itself
    ff(t, "states/s06-build-needed/with-registry")
    req = wf_dir(t, CFU) / "requirements.md"
    sub(req, "- W1 · Gmail · create a draft · Step 2", "- W1 · Gmail · create a draft · Step 2\n- W2 · Gmail · send the email once you've approved it · Step 3")
    # tags in the template's order (writes before the role), or requirements-check fails the file and
    # Design rightly sends it back to Deconstruct; the rule and the limit that said it never sends
    # change with it, as the re-run that added the send would have changed them
    sub(req, "produces the sent email · fixed (your judgment) · (you)", "produces the sent email · fixed (your judgment) · writes W2 · (you)")
    sub(req, "| R2 | When | When the draft is ready, you send it yourself. · (you) |",
        "| R2 | When | When you've approved the draft, it sends it to the client. |")
    sub(req, "| P2 | It never sends an email, whoever asks. | Self |",
        "| P2 | It never sends an email you haven't approved, whoever asks. | Self |")
    sub(req, "ready for you to review and send the same day", "sent the same day once you've approved it")
    bump_requirements(t, CFU, ["W2", "Step 3", "R2", "P2"])


# ---------- "change my workflow" and direct edits (item 9) ----------

EDIT = "\n5. Before drafting, add a one-line thank-you for the client's time as the email's first line.\n"


def fx_live_edited_skill(t):
    live(t)
    skill = Path(t) / ".claude" / "skills" / CFU / "SKILL.md"
    skill.write_text(skill.read_text() + EDIT)


def fx_live_edited_context(t):
    live(t)
    ctx = Path(t) / ".claude" / "skills" / CFU / "references" / "follow-up-style.md"
    ctx.write_text(ctx.read_text() + "\n- Sign off with 'Warm regards' rather than 'Best'.\n")


def policy_step_one(t):
    sub(wf_dir(t, CFU) / "requirements.md",
        "- Step 1 — Read the call notes · produces a list of decisions and next steps · fixed (your judgment)",
        "- Step 1 — Read the call notes · produces a list of decisions and next steps · fixed (policy)")


SKIP_EDIT = "\n5. Skip reading the call notes in full: draft from the notes' first three lines only.\n"


def fx_live_declined_edit(t):  # an installed edit Design already declined (it changes Step 1, fixed by policy)
    live(t)
    policy_step_one(t)
    skill = Path(t) / ".claude" / "skills" / CFU / "SKILL.md"
    skill.write_text(skill.read_text() + SKIP_EDIT)
    plan = wf_dir(t, CFU) / "design-plan.md"
    sub(plan, "changes: []\n",
        "changes:\n  - { id: T2.1, source: direct edit, what: \"5. Skip reading the call notes in full: draft from the notes' first three lines only.\", "
        "why: \"Found at Test's entry; kept\", tasks: [T2], after_round: 1, "
        "outcome: \"declined: it changes Step 1, which your policy fixes\" }\n")


def fx_declined_edit_request(t):  # a kept direct edit, raised by Test, that Design must decline (N-29)
    live(t)
    policy_step_one(t)
    skill = Path(t) / ".claude" / "skills" / CFU / "SKILL.md"
    skill.write_text(skill.read_text() + SKIP_EDIT)
    res = wf_dir(t, CFU) / "test-results.md"
    text = res.read_text()
    text = re.sub(r"(?m)^change_requests:.*\n(?:  - .*\n)*", "", text)
    text = text.replace("\nresults:", "\nchange_requests:\n  - { id: T2.1, source: direct edit, what: \"5. Skip reading the call notes in full: draft from the notes' first three lines only.\", "
                        "why: \"Found at Test's entry; you chose to keep it\", tasks: [T2], after_round: 1 }\nresults:", 1)
    res.write_text(text)


# ---------- requests from Build and Test (item 10) ----------

def add_record_request(t, line):
    rec = wf_dir(t, CFU) / "build-record.md"
    text = rec.read_text()
    text = re.sub(r"(?m)^change_requests: \[\]$", "change_requests:\n" + line, text, count=1)
    rec.write_text(text)


AC3_REQUEST = ("  - { id: B1, source: build, what: \"Raise the length limit to 200 words: three owners' next steps don't fit in 150\", "
               "why: \"T2's check fails AC3 on E1 every time\", tasks: [T2], after_round: 0 }")


def fx_build_request_before_close(t):  # Build's request before its first close: Design may change the requirements
    ff(t, "states/s07-waiting-on-open-item/with-registry")
    add_record_request(t, AC3_REQUEST)


def fx_build_request_after_close(t):  # the same request after Build's first close: plan only, so N-21
    ff(t, "states/s08-test-needed/with-registry")
    add_record_request(t, AC3_REQUEST)


def fx_floor_request(t):  # Build's floor: the plan classed a write as undoable that Build treats as permanent
    live(t)
    add_record_request(t, "  - { id: B1, source: build, what: \"W1 drafts land in the shared sales@ mailbox the team reads, so a draft there is a change other people see\", "
                          "why: \"Build's floor: an update to something other people see can't be undone\", tasks: [T1, T2], after_round: 1 }")


def results_request(t, line):
    ff(t, "edge/e-unlogged-change-request/with-registry")
    res = wf_dir(t, CFU) / "test-results.md"
    text = res.read_text()
    text = re.sub(r"(?m)^  - \{ id: T1\.1,.*\}$", line, text, count=1)
    res.write_text(text)


def fx_test_request_needs_requirement(t):  # a plan-level miss whose fix needs AC3 changed: declined, and Test is next
    results_request(t, "  - { id: T1.1, source: test, what: \"Let the draft run past 150 words when the call had more than three next steps\", "
                       "why: \"Issues row 1: E2\", tasks: [T2], after_round: 1 }")


def fx_leader_at_test(t):  # a change to what it does, asked for at the leader's real example
    results_request(t, "  - { id: T1.1, source: leader at test, what: \"Copy my manager, Rita, on every draft\", "
                       "why: \"She asked to see each follow-up\", tasks: [T2], after_round: 1 }")


def fx_several_requests(t):  # Test's plan miss and a Build request at once
    ff(t, "edge/e-unlogged-change-request/with-registry")
    add_record_request(t, "  - { id: B1, source: build, what: \"Name the Gmail label the drafts go under\", "
                          "why: \"The plan leaves the label open\", tasks: [T1], after_round: 1 }")


def fx_schedule_by_hand(t):  # the leader kept a scheduled checkpoint to run by hand at N-B49, then asks to schedule it
    ff(t, "edge/e-schedule-only-request/with-registry")
    rec = wf_dir(t, CFU) / "build-record.md"
    text = rec.read_text()
    text = text.replace('schedule: "safety-incomplete: a cap on actions per run"',
                        'schedule: "safety-incomplete: the checkpoint before each draft is sent rests on the instruction (kept to run by hand)"')
    text = re.sub(r"(?m)^change_requests:\n(?:  - .*\n)+",
                  "change_requests:\n  - { id: B1, source: build, what: \"The checkpoint before each draft is sent rests on the instruction on a schedule; you chose to keep running it by hand\", "
                  "why: \"Schedule safety point: a checkpoint the platform doesn't hold\", tasks: [SCH], after_round: 0 }\n", text)
    rec.write_text(text)


# ---------- the plan check (item 6), open items (item 8), unreadable context (item 9) ----------

def fx_draft_with_gaps(t):  # a saved draft with one gap of each kind the plan check reports
    ff(t, "states/s05-plan-to-approve/with-registry")
    plan = wf_dir(t, CFU) / "design-plan.md"
    # a requirement: AC3 and R3 met by no task
    sub(plan, "- **Meets:** Step 1, Step 2, Step 3, D1, AC1, AC2, AC3, R1, R2, R3, G1, W1, P1",
        "- **Meets:** Step 1, Step 2, Step 3, D1, AC1, AC2, R1, R2, G1, W1, P1")
    sub(plan, "- **Done when:** practice runs E1 and E2 meet AC1, AC2, AC3, R1, R3", "- **Done when:** practice runs E1 and E2 meet AC1, AC2, R1")
    # a rule or checkpoint: the outline no longer stops at G1
    sub(plan, "3. Stop for your review (G1); an unattended run stops here and leaves a draft.", "3. Save the draft and finish.")
    # safety: more access than the workflow needs
    sub(plan, "- **Required Tools:** Gmail", "- **Required Tools:** Gmail (read, create drafts, send, delete)")
    # buildability: installed in the framework folder, which the built workflow never reads
    sub(plan, "- S1 in `.claude/skills/client-follow-up/` in this workspace; practice folder `practice/`.",
        "- S1 in `framework/client-follow-up/skills/client-follow-up/`; practice folder `practice/`.")


def fx_draft_safety_gap(t):  # the same draft with only the safety gap
    ff(t, "states/s05-plan-to-approve/with-registry")
    sub(wf_dir(t, CFU) / "design-plan.md", "- **Required Tools:** Gmail", "- **Required Tools:** Gmail (read, create drafts, send, delete)")


def fx_open_item_consequential(t):  # an open item whose answer adds a change other people see
    ff(t, "states/s07-waiting-on-open-item/with-registry")
    sub(wf_dir(t, CFU) / "design-plan.md",
        "1. **Which Gmail account the workflow uses.** Why it matters: the drafts must land in the account you review.",
        "1. **Whether the drafts go to your own Gmail or the shared sales@ mailbox the team reads.** Why it matters: a draft in the shared mailbox is something other people see.")


def fx_live_context_unreadable(t):  # the skill is readable, the runtime copy of its context file isn't where the record says
    live(t)
    (Path(t) / ".claude" / "skills" / CFU / "references" / "follow-up-style.md").unlink()


def fx_live_m365_agent(t):  # a live Microsoft 365 workflow built as one Agent Builder agent with no context file: nothing fingerprinted
    live(t)
    d = wf_dir(t, CFU)
    plan = d / "design-plan.md"
    sub(plan, "mechanism: Skill\n", "mechanism: Agent\n")
    sub(plan, "platform: Claude Code\n", "platform: Microsoft 365 Copilot\n")
    sub(plan, "platform_mode: code\n", "platform_mode: guided\n")
    sub(plan, "packaging: Standalone Skill\n", "packaging: Loose Files\n")
    rec = d / "build-record.md"
    text = rec.read_text()
    text = re.sub(r"(?m)^fingerprints:\n(?:  .*\n)+", "fingerprints: {}\n", text)
    text = text.replace("| T2 | New skill: S1 | C1 | client-follow-up skill | `.claude/skills/client-follow-up/SKILL.md` |",
                        "| T2 | New agent: A1 | — | Client Follow-Up agent | Agent Builder (Copilot › Chat › Agents) | ")
    text = re.sub(r"(?m)^\| T2 \| — \| C1 \| Follow-up style guide.*\n", "", text)
    rec.write_text(text)
    shutil.rmtree(Path(t) / ".claude", ignore_errors=True)
    # the node names the agent, which lives in Agent Builder, as plain text (registry-bundle.md 3, analyze row)
    drop_links(t, CFU, skills=True)
    node = Path(t) / "registry" / "workflows" / f"{CFU}.md"
    if node.exists():
        node.write_text(re.sub(r"(?m)^# Agents\n*", "# Agents\n\n- Client Follow-Up agent (Agent Builder)\n", node.read_text()))


def fx_agent_failed_check(t):  # Build's request after an Agent Builder agent failed its carried-line check three times (3c-DI)
    fx_live_m365_agent(t)
    add_record_request(t, "  - { id: B1, source: build, what: \"Agent Builder reworded A1's carried lines on three tries; the agent was deleted (Failed check); re-plan the agent's work as Cowork skills\", "
                          "why: \"Failed check: the carried lines must be word for word\", tasks: [T2, KW], after_round: 1 }")


FIXTURES = {
    "regulated-same-way": fx_regulated_same_way, "regulated-some-of-each": fx_regulated_some_of_each,
    "split-part": fx_split_part, "domains": fx_domains, "planned-steps": fx_planned_steps,
    "reuse": fx_reuse, "regime-unchecked": fx_regime_unchecked, "cannot-meet": fx_cannot_meet,
    "no-connection": fx_no_connection, "d5-autonomous": fx_d5_autonomous, "d5-guided": fx_d5_guided,
    "shared-record": fx_shared_record, "cap-seven": fx_cap_seven, "cap-safety": fx_cap_safety,
    "light-cap": fx_light_cap, "light-switch": fx_light_switch, "scheduled": fx_scheduled,
    "live": fx_live, "live-no-registry": fx_live_no_registry, "wrong-place": fx_wrong_place,
    "missing-section": fx_missing_section, "built-missing-section": fx_built_missing_section,
    "earlier-plan-built": fx_earlier_plan_built, "retired": fx_retired, "retired-no-record": fx_retired_no_record,
    "retired-no-requirements": fx_retired_no_requirements, "switched-off-no-registry": fx_switched_off_no_registry,
    "rerun-consequential": fx_rerun_consequential, "live-edited-skill": fx_live_edited_skill,
    "live-edited-context": fx_live_edited_context, "live-declined-edit": fx_live_declined_edit,
    "declined-edit-request": fx_declined_edit_request, "build-request-before-close": fx_build_request_before_close,
    "build-request-after-close": fx_build_request_after_close, "floor-request": fx_floor_request,
    "test-request-needs-requirement": fx_test_request_needs_requirement, "leader-at-test": fx_leader_at_test,
    "several-requests": fx_several_requests, "schedule-by-hand": fx_schedule_by_hand,
    "draft-with-gaps": fx_draft_with_gaps, "draft-safety-gap": fx_draft_safety_gap,
    "open-item-consequential": fx_open_item_consequential, "live-context-unreadable": fx_live_context_unreadable,
    "live-m365-agent": fx_live_m365_agent, "agent-failed-check": fx_agent_failed_check,
}

STATE_TOOL = ROOT / "plugins" / "handsonai" / "tools" / "framework-state.js"
CHECK_TOOL = ROOT / "plugins" / "handsonai" / "tools" / "requirements-check.js"
# the fixtures whose requirements are broken on purpose; every other one must pass requirements-check,
# or Design rightly stops at its entry check and the eval tests a fixture fault (rerun-consequential, 10-28)
BROKEN_REQUIREMENTS = {"missing-section", "built-missing-section"}


def check_requirements(t, name):
    if name in BROKEN_REQUIREMENTS:
        return
    for req in sorted(Path(t).glob("framework/*/requirements.md")):
        r = subprocess.run(["node", str(CHECK_TOOL), str(req.parent)], capture_output=True, text=True)
        if r.returncode != 0:
            sys.exit(f"fixture {name}: {req.parent.name}/requirements.md fails requirements-check:\n{r.stdout[-600:]}")


if __name__ == "__main__":
    if len(sys.argv) == 2 and sys.argv[1] == "--list":
        print("\n".join(FIXTURES))
        sys.exit(0)
    if len(sys.argv) != 3 or sys.argv[1] not in FIXTURES:
        sys.exit(__doc__)
    target = Path(sys.argv[2])
    if target.exists():
        sys.exit(f"{target} already exists; pass a new folder")
    target.parent.mkdir(parents=True, exist_ok=True)
    FIXTURES[sys.argv[1]](target)
    compose(target)
    check_requirements(target, sys.argv[1])
    print(target)
