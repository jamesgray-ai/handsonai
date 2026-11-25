#!/usr/bin/env python3
"""Build the workspace a Deconstruct eval starts from, in this release's formats.

Usage: python3 make_fixture.py <fixture-name> <target-dir>
       python3 make_fixture.py --list

Two kinds of fixture:
- Interview fixtures (sales, expenses, meals, winstory): a fresh registry from
  registry-template/registry with one backlog Workflow node, for the I-evals.
- Fixtures built on framework-fixtures/ (T15), the shared library of routing-state workspaces:
  most evals point at a variant folder directly (`dir:../../framework-fixtures/...`); the names here
  are the combinations that library doesn't hold (two interviews partway, the wrong place, a
  newsletter candidate with no risk, standing rules, a Git repository, and so on).

`R1` and `R10` are kept for the Design and Test eval sets that still name them (T23, T25): R1 is a
workflow built and waiting for Test (state 8); R10 an earlier-version requirements file (state 1).
"""
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FF = ROOT / "framework-fixtures"
TEMPLATE = ROOT / "registry-template" / "registry"
CFU = "client-follow-up"
WPS = "weekly-pipeline-summary"
NEWS = "weekly-newsletter-draft"


# ---------- helpers: a fresh registry (interview fixtures) ----------

def fresh_registry(t, business, log_entry):
    t.mkdir(parents=True, exist_ok=True)
    shutil.copytree(TEMPLATE, t / "registry")
    log = t / "registry" / "log.md"
    log.write_text(log.read_text() + f"\n## 2026-09-01 — Registry scaffolded\n\n{log_entry}\n")
    biz = t / "registry" / "businesses" / "business.md"
    biz.write_text(
        "---\ntype: Business\n"
        f'title: "{business}"\n'
        f'description: "{business}."\n'
        "generated: { by: process:scaffolding-registry, at: 2026-09-01T09:00:00Z }\n---\n"
        f"# {business}\n"
    )
    idx = t / "registry" / "businesses" / "index.md"
    if idx.exists():
        body = "\n".join(l for l in idx.read_text().splitlines() if not l.startswith("_No entries yet"))
        idx.write_text(body.rstrip("\n") + f"\n- [{business}](/businesses/business.md)\n")


def node_path(t, slug):
    return t / "registry" / "workflows" / f"{slug}.md"


def add_node(t, slug, title, description, trigger, status="backlog", body_extra="", artifacts=""):
    node_path(t, slug).write_text(
        "---\ntype: Workflow\n"
        f'title: "{title}"\n'
        f'description: "{description}"\n'
        "generated: { by: process:analyze, at: 2026-09-01T09:00:00Z }\n"
        f"status: {status}\n"
        f'trigger: "{trigger}"\n---\n'
        f"# {title}\n\n{description}\n{body_extra}\n"
        f"# Artifacts\n\n{artifacts}\n# Skills\n\n# Agents\n"
    )
    idx = t / "registry" / "workflows" / "index.md"
    kept = [l for l in idx.read_text().splitlines() if not l.startswith("_No entries yet")]
    idx.write_text("\n".join(kept).rstrip("\n") + f"\n- [{title}](/workflows/{slug}.md)\n")


def add_process(t, slug, title, description, owner, workflows=()):
    lines = "".join(f"- [{wt}](/workflows/{ws}.md)\n" for ws, wt in workflows)
    (t / "registry" / "processes" / f"{slug}.md").write_text(
        "---\ntype: Process\n"
        f'title: "{title}"\n'
        f'description: "{description}"\n'
        "generated: { by: process:scaffolding-registry, at: 2026-09-01T09:00:00Z }\n"
        f"owner: {owner}\n---\n"
        f"# {title}\n\n{description}\n\n# Workflows\n{lines}"
    )
    idx = t / "registry" / "processes" / "index.md"
    kept = [l for l in idx.read_text().splitlines() if not l.startswith("_No entries yet")]
    idx.write_text("\n".join(kept).rstrip("\n") + f"\n- [{title}](/processes/{slug}.md)\n")
    # a Process joins its line of business's # Processes list (the lint's error otherwise)
    lobs = sorted(p for p in (t / "registry" / "lines-of-business").glob("*.md") if p.name != "index.md")
    if lobs:
        lobs[0].write_text(lobs[0].read_text().rstrip("\n") + f"\n- [{title}](/processes/{slug}.md)\n")


def progress_file(t, slug, node, next_part, track, notes, root="framework", said=None):
    """A progress file. With `said`, this release's four-line form (`Said:` on line 4); without it, the form the
    earlier two-track interview saved (`Next: Part N — …` or `Next: Light — …`, no `Said:` line)."""
    d = t / root / slug
    d.mkdir(parents=True, exist_ok=True)
    head = f"Next: {next_part}\nWorkflow node: {node}\nTrack: {track}\n" + (f"Said: {said}\n" if said else "")
    (d / "deconstruct-in-progress.md").write_text(f"{head}\n{notes}\n")


# ---------- interview fixtures ----------

def fx_sales(t):
    fresh_registry(t, "Rivera Advisory", "Set up by `scaffolding-registry` for Rivera Advisory, a two-person B2B consulting practice.")
    add_node(t, "sales-pre-call-brief", "Sales Pre-Call Brief",
             "Prepares a one-page brief before each booked scoping call. A brief the consultant reads the day before.",
             "A scoping call is booked")


def fx_expenses(t):
    fresh_registry(t, "Northbank Financial — Finance Operations",
                   "Set up by `scaffolding-registry` for the Finance Operations team at Northbank Financial, a regional bank.")
    add_node(t, "expense-report-approval", "Expense Report Approval",
             "Checks each submitted expense report against policy and routes it for approval. An approved or returned report.",
             "An employee submits an expense report")


def fx_meals(t):
    fresh_registry(t, "The Okafor Household",
                   "Set up by `scaffolding-registry` for a personal-life registry: The Okafor Household, a household of four.")
    add_node(t, "weekly-meal-planning", "Weekly Meal Planning",
             "Plans the week's dinners and the shopping list. A meal plan and a list for Saturday's shop.",
             "Sunday afternoon")


def fx_winstory(t):
    fresh_registry(t, "Lumen Software — Marketing", "Set up by `scaffolding-registry` for the marketing team at Lumen Software.")
    add_node(t, "customer-win-story", "Customer Win Story",
             "Turns a closed deal into a short customer story for the website. A draft story the customer approves.",
             "A deal closes and the customer agrees to a story")


# ---------- fixtures on framework-fixtures/ ----------

def ff(t, rel):
    shutil.copytree(FF / rel, t)


def fx_r1(t):  # kept for test-workspace: built, waiting for Test (state 8)
    ff(t, "states/s08-test-needed/with-registry")


def fx_r10(t):  # kept for design-workspace: an earlier-version requirements file (state 1, Deconstruct)
    ff(t, "earlier-version/old-format/step-driven-norow")


# the single interview's progress notes: plain words under each item's name (one interview for every workflow, 2026-11-15)
CFU_NOTES = ("## The name and description\nClient Follow-Up: drafts a follow-up email after each client call from your call notes, "
             "for you to review and send. Starts: you, after each call.\n\n"
             "## The safety questions\nIt saves the draft in your Outlook Drafts folder; you send it yourself. Runs with you: you read "
             "every draft before it goes. Law or regulation: no. Governing regime: None.")
WPS_NOTES = ("## The name and description\nWeekly Pipeline Summary: summarises your open deals every Friday from HubSpot, "
             "for you to review before the Monday sales meeting. Starts: schedule: every Friday at 3pm.\n\n"
             "## The safety questions\nIt sends and changes nothing: it gives you the summary. Runs with you: you read every summary. "
             "Law or regulation: no. Governing regime: None.\n\n"
             "## The goal\nEach Friday, a one-page summary of every open deal and its next step, ready for you to read before "
             "Monday's sales meeting.")


def fx_one_unfinished(t):  # one interview partway (Client Follow-Up), Weekly Pipeline Summary still in the backlog
    ff(t, "continue/c-only-backlog/with-registry")
    progress_file(t, CFU, f"registry/workflows/{CFU}.md", "the goal", "light", CFU_NOTES, said="folder line")


def fx_two_unfinished(t):  # two interviews partway, no workflow named: deconstruct 3.3's list question
    fx_one_unfinished(t)
    progress_file(t, WPS, f"registry/workflows/{WPS}.md", "what it must get right", "light", WPS_NOTES,
                  said="privacy line · folder line")


def fx_analyze_unfinished(t):  # an unfinished Analyze session beside the backlog: deconstruct 3.3 item 2
    ff(t, "continue/c-only-backlog/with-registry")
    shutil.copy(FF / "continue/c-analyze-unfinished-alone/with-registry/framework/analyze-in-progress.md",
                t / "framework" / "analyze-in-progress.md")


def fx_wrong_place(t):  # the live workflow's own place: its context files, and no framework files
    src = FF / "states/s02-redo-pending/with-registry"
    t.mkdir(parents=True)
    shutil.copytree(src / ".claude", t / ".claude")


def fx_backlog_filter(t):  # 5.1: a backlog node whose slug already has a folder, and running work, are left out
    ff(t, "continue/c-only-backlog/with-registry")
    shutil.copytree(FF / f"states/s04-plan-needed/with-registry/framework/{CFU}", t / "framework" / CFU)
    add_node(t, "stakeholder-meeting-prep", "Stakeholder Meeting Prep",
             "Prepares a one-page brief before each stakeholder meeting, for you to read beforehand.",
             "A stakeholder meeting is booked", status="in-production",
             body_extra="\nRuns today as a prompt you paste before each stakeholder meeting.\n")
    proc = t / "registry" / "processes" / "client-relationship-management.md"  # running work joins a Process
    proc.write_text(proc.read_text().rstrip("\n") + "\n- [Stakeholder Meeting Prep](/workflows/stakeholder-meeting-prep.md)\n")
    add_node(t, NEWS, "Weekly Newsletter Draft",
             "Drafts the weekly client newsletter from your notes, for you to edit and send yourself.",
             "Friday morning, you paste in the week's notes")


def add_newsletter(t):
    add_process(t, "client-newsletter", "Client Newsletter", "Keeping clients up to date between projects.",
                "account-management", [(NEWS, "Weekly Newsletter Draft")])
    report = (t / "framework" / "ai-opportunity-report.md").exists()  # linked only where Analyze left it
    add_node(t, NEWS, "Weekly Newsletter Draft",
             "Drafts the weekly client newsletter from your notes, for you to edit and send yourself.",
             "Friday morning, you paste in the week's notes",
             artifacts="- [Opportunity report](framework/ai-opportunity-report.md)\n" if report else "")


def fx_newsletter(t):  # a first-time leader's backlog with a plain candidate that shows no risk
    ff(t, "continue/c-only-backlog/with-registry")
    add_newsletter(t)


def fx_newsletter_git(t):  # the same, inside a Git repository (the Git offer)
    fx_newsletter(t)
    env = ["-c", "user.name=Leader", "-c", "user.email=leader@example.com", "-c", "commit.gpgsign=false"]
    subprocess.run(["git", "init", "-q", str(t)], check=True)
    subprocess.run(["git", *env, "-C", str(t), "add", "-A"], check=True)
    subprocess.run(["git", *env, "-C", str(t), "commit", "-q", "-m", "My framework files"], check=True)


def fx_newsletter_second(t):  # a second workflow: Client Follow-Up's requirements exist (state 4), the newsletter is next
    ff(t, "states/s04-plan-needed/with-registry")
    add_newsletter(t)


STANDING = """# Standing rules

Rules you keep for every workflow. Deconstruct suggests the ones that fit each new workflow, and each workflow's requirements keep their own copy.

- It never sends an email; it only saves drafts for you to send. · rule · from client-follow-up, 2026-10-01
- It never names one client to another. · rule · from client-follow-up, 2026-10-01
"""


def fx_newsletter_standing(t):  # the same, with standing-rules.md kept from the first workflow
    fx_newsletter_second(t)
    (t / "framework" / "standing-rules.md").write_text(STANDING)


def fx_cold_registry(t):  # a registry whose processes fit the workflow the leader names, and no node for it
    ff(t, "continue/c-only-backlog/with-registry")
    for slug in (CFU, WPS):
        node_path(t, slug).unlink()
    (t / "registry" / "workflows" / "index.md").write_text("# Workflows\n\n_No entries yet._\n")
    for p in (t / "registry" / "processes").glob("*.md"):
        if p.name != "index.md":
            p.write_text(re.sub(r"(?s)# Workflows\n.*", "# Workflows\n", p.read_text()))


def fx_cold_registry_no_fit(t):  # the same, with only a finance process: no process fits a newsletter
    fx_cold_registry(t)
    for p in (t / "registry" / "processes").glob("*.md"):
        if p.name != "index.md":
            p.unlink()
    (t / "registry" / "processes" / "index.md").write_text("# Processes\n")
    for p in list((t / "registry" / "lines-of-business").glob("*.md")) + list((t / "registry" / "functions").glob("*.md")):
        if p.name != "index.md":  # no link to the processes taken out
            p.write_text(re.sub(r"(?m)^- \[[^\]]+\]\(/processes/[^)]+\)\n", "", p.read_text()))
    add_process(t, "month-end-close", "Month-End Close", "Closing the books each month.", "account-management")



# ---------- fidelity check 2026-10-24 ----------

def fx_redo_with_rounds(t):  # S1: a big change whose set-aside holds a finished round beside test-results.md
    ff(t, "states/s02-redo-pending/with-registry")
    sa = t / "framework" / CFU / "history" / "set-aside-2026-10-20-0930"
    text = (sa / "test-results.md").read_text()
    (sa / "test-results-round-1.md").write_text(re.sub(r"(?m)^round: \d+", "round: 1", text, count=1))
    (sa / "test-results.md").write_text(re.sub(r"(?m)^round: \d+", "round: 2", text, count=1))


def fx_redo_no_set_aside(t):  # S2: Design wrote big_change, then stopped before making the set-aside folder
    ff(t, "states/s02-redo-pending/with-registry")
    wf = t / "framework" / CFU
    sa = wf / "history" / "set-aside-2026-10-20-0930"
    for f in sa.iterdir():
        shutil.move(str(f), str(wf / f.name))
    sa.rmdir()
    node = node_path(t, CFU)
    body = node.read_text()
    arts = "- [Design plan](framework/client-follow-up/design-plan.md)\n- [Test results](framework/client-follow-up/test-results.md)\n"
    if "[Design plan]" not in body:
        body = body.replace("# Artifacts\n\n", "# Artifacts\n\n" + arts, 1)
    node.write_text(body)


def fx_backlog_md_beside_registry(t):  # Analyze S3: a registry with no backlog node, and a backlog.md left from before it
    fx_cold_registry(t)
    (t / "framework").mkdir(exist_ok=True)
    (t / "framework" / "backlog.md").write_text(
        "# Backlog\n\n## Client work\n\n1. **Weekly Newsletter Draft.** Every Friday, drafts the client newsletter "
        "from your notes, for you to edit and send yourself.\n")


def fx_backlog_plus_retired(t):  # S8: the backlog, and a retired workflow the leader names at the backlog choice
    ff(t, "continue/c-only-backlog/with-registry")
    add_node(t, "renewal-reminders", "Renewal Reminders",
             "Two months before each contract renews, drafts a reminder for you to send the client.",
             "Two months before a renewal date", status="retired")


# ---------- Deconstruct 3.3: backlogs whose Analyze report has this release's detailed cards ----------
# Every card here is in Analyze's current format (report-format.md): a Goal on every card, "What changes for
# the business", and a Candidate Summary row per candidate with its Trigger, Deliverable and Frequency, so
# N-D23 (R-A1), Part 1's card form (R-P1) and the light defaults read them. Made-up business; the systems
# are the leader's own, varied on purpose (F-M12).

OBJECTIVES = "## Objectives\n\n- Keep every client renewal on time\n- Win two new clients a quarter\n\n"
CARD_CFU = {
    "name": "Client Follow-Up", "process": "Client Relationship Management", "goal": "Keep every client renewal on time",
    "description": "Drafts a follow-up email after each client call from your call notes, for you to review and send.",
    "trigger": "You finish a client call and paste in your notes", "deliverable": "A follow-up email draft",
    "frequency": "Daily", "lever": "Accelerate", "pain": "Follow-ups often go out a day late.",
    "how": "Drafts the follow-up email from the call notes for you to review and send.",
    "changes": "Clients hear back the same day, and the time saved goes to preparing renewals.",
    "objective": "Keep every client renewal on time", "stakeholders": "Account lead; the client's main contact",
    "metrics": "Follow-ups sent within a day of the call",
}
CARD_WPS = {
    "name": "Weekly Pipeline Summary", "process": "Sales Pipeline Management", "goal": "Win two new clients a quarter",
    "description": "Summarises your open deals every Friday from HubSpot, for you to review before the Monday sales meeting.",
    "trigger": "Every Friday afternoon, you ask for this week's summary", "deliverable": "A one-page summary of open deals",
    "frequency": "Weekly", "lever": "Streamline", "pain": "Pulling the deals together by hand takes the Friday afternoon.",
    "how": "Reads the open deals and writes a one-page summary with each deal's next step.",
    "changes": "The Monday meeting starts from the same page, with every stalled deal visible.",
    "objective": "Win two new clients a quarter", "stakeholders": "Sales lead; the partners",
    "metrics": "Open deals with an agreed next step",
}
CARD_MONTHLY = {
    "name": "Monthly Supplier Spend Review", "process": "Finance and Reporting", "goal": "Keep every client renewal on time",
    "description": "On the first working day of each month, checks last month's supplier bills in Xero against the budget and posts the variances to the finance tracker in SharePoint, for the finance lead.",
    "trigger": "The first working day of each month", "deliverable": "Last month's spend variances, posted to the finance tracker",
    "frequency": "Monthly", "lever": "Automate", "pain": "The month's spend check slips to the second week.",
    "how": "Compares last month's supplier bills with the budget lines and writes each variance with its reason.",
    "changes": "Overspends are caught in the first days of the month instead of the second week.",
    "objective": "None of the stated objectives — protects the firm's margins", "stakeholders": "Finance lead; the partners",
    "metrics": "Variances reported by the third working day",
}


def card_report(cards, lens="Organizational"):
    """framework/ai-opportunity-report.md in Analyze's current format, one detailed card and one Candidate
    Summary row per card."""
    head = ("# AI Opportunity Report\n\n| | |\n|---|---|\n| **Role** | Owner, Brightline Advisory |\n"
            f"| **Date** | 2026-10-01 |\n| **Lens** | {lens} |\n| **Opportunities identified** | {len(cards)} |\n\n"
            "### Summary Table\n\n| # | Opportunity | Process | Value lever |\n|---|---|---|---|\n")
    head += "".join(f"| {i} | {c['name']} | {c['process']} | {c['lever']} |\n" for i, c in enumerate(cards, 1))
    body = "\n### Detailed Opportunity Cards\n"
    for i, c in enumerate(cards, 1):
        status = f"**Status:** {c['status_card']}\n\n" if c.get("status_card") else ""
        body += (f"\n#### {c['process']}\n\n---\n\n**{i} {c['name']}**\n\n{status}**Goal:** {c['goal']}\n\n"
                 f"**Why it's a good candidate:** The same piece of work, from the same kind of material, every time.\n\n"
                 f"**Current pain point:** {c['pain']}\n\n**How AI helps:** {c['how']}\n\n"
                 f"**Value lever:** {c['lever']} — {c['changes'].split(',')[0].rstrip('.')}.\n\n"
                 f"**What changes for the business:** {c['changes']}\n\n"
                 f"**Business Objective:** {c['objective']}\n**Stakeholders:** {c['stakeholders']}\n"
                 f"**Success Metrics:** {c['metrics']}\n\n---\n")
    summary = "\n## Workflow Candidate Summary\n"
    for c in cards:
        status = f"| **Status** | {c['status_row']} |\n" if c.get("status_row") else ""
        summary += ("\n| Field | Content |\n|-------|---------|\n"
                    f"| **Workflow** | {c['name']} |\n| **Process** | {c['process']} |\n| **Goal** | {c['goal']} |\n{status}"
                    f"| **Description** | {c['description']} |\n| **Trigger** | {c['trigger']} |\n"
                    f"| **Deliverable** | {c['deliverable']} |\n| **Value lever** | {c['lever']} |\n"
                    f"| **Pain point** | {c['pain']} |\n| **AI opportunity** | {c['how']} |\n"
                    f"| **Frequency** | {c['frequency']} |\n| **Lens** | {lens} |\n"
                    f"| **Business Objective** | {c['objective']} |\n| **Stakeholders** | {c['stakeholders']} |\n"
                    f"| **Success Metrics** | {c['metrics']} |\n")
    return head + body + summary


def with_objectives(t):
    biz = t / "registry" / "businesses" / "brightline-advisory.md"
    text = biz.read_text()
    if "## Objectives" not in text:
        biz.write_text(text.replace("# Lines of Business", OBJECTIVES + "# Lines of Business", 1))


def set_node(t, slug, **fields):
    p = node_path(t, slug)
    text = p.read_text()
    for k, v in fields.items():
        text = re.sub(rf'(?m)^{k}: ".*"$', f'{k}: "{v}"', text)
        if k == "description":
            text = re.sub(r"(?m)^(# [^\n]+\n\n)[^\n]+\n", rf"\g<1>{v}\n", text, count=1)
    p.write_text(text)


def fx_card_backlog(t):  # Client Follow-Up (client details, a saved draft) and Weekly Pipeline Summary (no risk, a time), full cards
    ff(t, "continue/c-only-backlog/with-registry")
    with_objectives(t)
    (t / "framework" / "ai-opportunity-report.md").write_text(card_report([CARD_CFU, CARD_WPS]))


def fx_card_not_clear(t):  # T6: Client Follow-Up's trigger and deliverable left "Not clear yet" by Analyze
    ff(t, "continue/c-only-backlog/with-registry")
    with_objectives(t)
    nc = "Not clear yet — Deconstruct settles it"
    desc = "Helps you follow up with each client after a call, for you to review and send."
    card = {**CARD_CFU, "trigger": nc, "deliverable": nc, "description": desc}
    (t / "framework" / "ai-opportunity-report.md").write_text(card_report([card, CARD_WPS]))
    set_node(t, CFU, description=desc, trigger=nc)


def fx_card_no_goal(t):  # R-P1's fallback: Goal "None named", with the Business node's objectives (q1 in its own message)
    ff(t, "continue/c-only-backlog/with-registry")
    with_objectives(t)
    card = {**CARD_CFU, "goal": "None named", "objective": "None of the stated objectives — protects client goodwill"}
    (t / "framework" / "ai-opportunity-report.md").write_text(card_report([card, CARD_WPS]))


def fx_card_running(t):  # running work Analyze recorded: a card with a Status line (N-D22's Status form, M2)
    ff(t, "states/s00-running-work/with-registry")
    with_objectives(t)
    card = {**CARD_CFU, "status_card": "Already runs with the follow-up-drafter skill, in Claude Code. Could be better: it misses next steps the client agreed to.",
            "status_row": "already runs with the follow-up-drafter skill",
            "pain": "None stated — could be better: it misses next steps the client agreed to.",
            "how": "The follow-up-drafter skill drafts the email from the call notes today."}
    (t / "framework" / "ai-opportunity-report.md").write_text(card_report([card]))


def fx_card_monthly(t):  # F-M12: a monthly workflow on Xero, SharePoint and Microsoft Teams (no Gmail, no Slack)
    ff(t, "continue/c-only-backlog/with-registry")
    with_objectives(t)
    slug = "monthly-supplier-spend-review"
    add_process(t, "finance-and-reporting", "Finance and Reporting", "Keeping spend and reporting on track.",
                "account-management", [(slug, CARD_MONTHLY["name"])])
    add_node(t, slug, CARD_MONTHLY["name"], CARD_MONTHLY["description"], CARD_MONTHLY["trigger"],
             artifacts="- [Opportunity report](framework/ai-opportunity-report.md)\n")
    (t / "framework" / "ai-opportunity-report.md").write_text(card_report([CARD_CFU, CARD_WPS, CARD_MONTHLY]))


def fx_light_progress_old(t):  # a progress file the earlier light interview saved, past item 1, with no safety answers
    fx_newsletter(t)
    progress_file(t, NEWS, f"registry/workflows/{NEWS}.md", "Light — what it must get right", "light",
                  "## Name and description\nWeekly Newsletter Draft: Drafts the weekly client newsletter from your notes, "
                  "for you to edit and send yourself.\n\n## The goal\nEach Friday, a newsletter draft of the week's news "
                  "and one tip, ready for you to edit and send.\n")


def fx_light_progress_rules_old(t):  # a progress file the earlier light interview saved at its rules, safety answers captured
    fx_newsletter(t)
    progress_file(t, NEWS, f"registry/workflows/{NEWS}.md", "Light — the rules", "light",
                  "## Name and description\nWeekly Newsletter Draft: Drafts the weekly client newsletter from your notes, "
                  "for you to edit and send yourself.\n\n"
                  "## Safety questions\nIt sends and changes nothing: it gives you the draft here, and you copy it into your email "
                  "tool and send it yourself. Runs with you: you read and edit every draft. Law or regulation: no.\n\n"
                  "## The goal\nEach Friday, a short, friendly newsletter draft of the week's news and one tip to the firm's "
                  "clients, ready for you to edit and send by noon. No real example was kept.\n\n"
                  "## What it must get right\n1. Every item from your notes is in it. 2. Nothing that isn't in your notes "
                  "(must-have). 3. Under 200 words. 4. It ends with your sign-off.\n\n"
                  "## What it works from\nYour notes for the week, four or five short ones, pasted in each Friday; your past "
                  "newsletters, for the tone.\n")


# ---------- the measurement backlogs (section 7 item 6; the M- leader scripts) ----------
# Fresh registries for the businesses the measurement scripts name, each with a current-format report. The
# switch backlog's cards show no sign of risk: the risk shows in an answer to the safety questions (or the law question).

def card(name, process, goal, description, trigger, deliverable, frequency, lever="Streamline", **kw):
    nc = "Not clear yet — Deconstruct settles it"
    return {"name": name, "process": process, "goal": goal, "description": description,
            "trigger": trigger or nc, "deliverable": deliverable or nc, "frequency": frequency, "lever": lever,
            "pain": kw.get("pain", "It takes longer than it should, and it slips when the week is busy."),
            "how": kw.get("how", "Drafts it from the material the leader already has, for the leader to use."),
            "changes": kw.get("changes", "It's ready when it's needed, and the time saved goes to client work."),
            "objective": kw.get("objective", goal), "stakeholders": kw.get("stakeholders", "The owner of the process"),
            "metrics": kw.get("metrics", "Done on time each period"), **{k: v for k, v in kw.items() if k.startswith("status")}}


def m_backlog(t, business, about, objectives, cards, lens="Organizational", status="backlog"):
    fresh_registry(t, business, f"Set up by `scaffolding-registry` for {business}, {about}.")
    biz = t / "registry" / "businesses" / "business.md"
    biz.write_text(biz.read_text().rstrip("\n") + "\n\n## Objectives\n\n" + "".join(f"- {o}\n" for o in objectives))
    for c in cards:
        slug = re.sub(r"[^a-z0-9]+", "-", c["name"].lower()).strip("-")
        add_node(t, slug, c["name"], c["description"],
                 c["trigger"] if not c["trigger"].startswith("Not clear yet") else c["trigger"],
                 status="in-production" if c.get("status_row") else status,
                 artifacts="- [Opportunity report](framework/ai-opportunity-report.md)\n")
        if c.get("status_row"):  # running work sits in its Process's # Workflows list (the lint requires it)
            reg = t / "registry"
            stamp = "generated: { by: process:scaffolding-registry, at: 2026-09-01T09:00:00Z }\n"
            (reg / "functions" / "operations.md").write_text(
                f'---\ntype: Function\ntitle: "Operations"\ndescription: "Runs the studio day to day."\n{stamp}---\n'
                "# Operations\n\nRuns the studio day to day.\n\n<!-- GENERATED:owns -->\n<!-- /GENERATED -->\n")
            biz.write_text(biz.read_text().rstrip("\n") + "\n\n# Lines of Business\n\n- [Studio](/lines-of-business/studio.md)\n")
            (reg / "functions" / "index.md").write_text("# Functions\n\n- [Operations](/functions/operations.md)\n")
            (reg / "lines-of-business" / "studio.md").write_text(
                f'---\ntype: LineOfBusiness\ntitle: "Studio"\ndescription: "The studio\'s client work."\n{stamp}status: active\n---\n'
                "# Studio\n\nThe studio's client work.\n\n# Processes\n")
            (reg / "lines-of-business" / "index.md").write_text("# Lines of Business\n\n- [Studio](/lines-of-business/studio.md)\n")
            pslug = re.sub(r"[^a-z0-9]+", "-", c["process"].lower()).strip("-")
            add_process(t, pslug, c["process"], f"{c['process']} at {business}.", "operations", [(slug, c["name"])])
    (t / "framework").mkdir(parents=True, exist_ok=True)
    (t / "framework" / "ai-opportunity-report.md").write_text(card_report(cards, lens))


def fx_m_backlog_full(t):
    goals = ["Grow revenue from existing clients by 15% this year", "Win four new enterprise clients"]
    m_backlog(t, "Fernhill Partners", "a 40-person B2B services firm", goals, [
        card("Pipeline Hygiene Review", "Sales Pipeline Management", goals[0],
             "Every Monday before the pipeline call, checks each open deal in the CRM against the pipeline checklist.",
             "Every Monday morning before the pipeline call", None, "Weekly", lever="Streamline",
             metrics="Open deals with a missing or stale field", changes="Forecasts the partners can trust on Monday."),
        card("Competitor Pricing Brief", "Marketing", goals[1],
             "Once a month, writes a brief on competitors' published pricing and offers, for the head of marketing.",
             "The first week of each month", "A two-page competitor pricing brief", "Monthly", lever="Create value"),
        card("Client Onboarding Checks", "Client Onboarding", goals[0],
             "When a new client signs, checks their onboarding documents against the finance onboarding checklist and builds the onboarding file, for the finance director.",
             "A new client signs", "A completed onboarding file in the client folder", "Ad-hoc", lever="Streamline"),
    ])


def fx_m_backlog_light(t):
    goals = ["Keep every client deadline", "Free a day a month for advisory work"]
    m_backlog(t, "Whitfield & Lowe", "a small accounting practice", goals, [
        card("Partner Meeting Agenda", "Practice Management", goals[1],
             "The day before each partners' meeting, drafts the agenda from the partners' notes, for the managing partner to paste into the invite.",
             "You ask for it the day before the partners' meeting", "A one-page meeting agenda", "Weekly"),
        card("Monthly Priorities Note", "Practice Management", goals[0],
             "On the first working day of each month, drafts a note of the month's deadlines, overdue client work and anything stuck, for the managing partner.",
             "The first working day of each month", "A one-page priorities note", "Monthly"),
        card("Client Thank-You Notes", "Client Care", goals[1],
             "When the practice signs a new client, drafts a short thank-you note for the managing partner.",
             "The practice signs a new client", "A thank-you note draft", "Ad-hoc", lever="Accelerate"),
    ], lens="Individual")


def fx_m_backlog_switch(t):
    goals = ["Deliver every order on the promised day", "Cut overtime by a fifth"]
    m_backlog(t, "Kestrel Print", "a 25-person print shop", goals, [
        card("Weekly Website Traffic Note", "Marketing", goals[0],
             "Each week, writes a short note on the website's visits and enquiries from the analytics export, for the operations manager.",
             "You download the week's analytics export", "A short traffic note", "Weekly"),
        # M-switch-law's pick (smoke-1 fix, 2026-11-14): it reads only the presses' own checklist sheets (no staff
        # or client details), so its one sign of risk is the law question answered "yes" partway through light
        card("Press Safety Inspection Log", "Operations", goals[0],
             "Each Monday, drafts the week's press safety inspection log from the presses' checklist sheets, for the operations manager to check and sign.",
             "You scan the presses' checklist sheets on Monday morning", "A draft weekly inspection log", "Weekly"),
        card("Friday Timesheet Gaps List", "Operations", goals[1],
             "Every Friday afternoon, lists the timesheet days still missing, for the operations manager.",
             "Every Friday afternoon", "A list of missing timesheet days", "Weekly"),
    ], lens="Individual")


def fx_m_running_light(t):
    m_backlog(t, "Marsh Studio", "a two-person design studio", ["Win three new retainer clients this year"], [
        card("Weekly Reading List", "Studio Learning", "Win three new retainer clients this year",
             "Every Monday, turns the links saved last week into a short reading list with a line on each, for the founder.",
             "Monday morning, you paste in last week's saved links", "A short reading list", "Weekly",
             status_card="Already runs with a saved prompt, in Claude. Could be better: the lines are too long.",
             status_row="already runs with a saved prompt"),
    ], lens="Individual")


def fx_m_personal_backlog(t):
    fx_meals(t)
    biz = t / "registry" / "businesses" / "business.md"
    biz.write_text(biz.read_text().rstrip("\n") + "\n\n## Objectives\n\n- Eat at home five nights a week\n- One shop a week\n")
    (t / "framework").mkdir(parents=True, exist_ok=True)
    (t / "framework" / "ai-opportunity-report.md").write_text(card_report([
        card("Weekly Meal Planning", "Household Routines", "Eat at home five nights a week",
             "Plans the week's dinners and the shopping list. A meal plan and a list for Saturday's shop.",
             "Sunday afternoon", "A meal plan and a shopping list", "Weekly",
             changes="Dinners are decided before the week starts, and there's one shop a week.")], "Individual"))


FIXTURES = {
    "card-backlog": fx_card_backlog, "card-not-clear": fx_card_not_clear, "card-no-goal": fx_card_no_goal,
    "card-running": fx_card_running, "card-monthly": fx_card_monthly, "light-progress-old": fx_light_progress_old,
    "light-progress-rules-old": fx_light_progress_rules_old,
    "m-backlog-full": fx_m_backlog_full, "m-backlog-light": fx_m_backlog_light, "m-backlog-switch": fx_m_backlog_switch,
    "m-running-light": fx_m_running_light, "m-personal-backlog": fx_m_personal_backlog,
    "sales": fx_sales, "expenses": fx_expenses, "meals": fx_meals, "winstory": fx_winstory,
    "R1": fx_r1, "R10": fx_r10,
    "one-unfinished": fx_one_unfinished, "two-unfinished": fx_two_unfinished,
    "analyze-unfinished": fx_analyze_unfinished, "wrong-place": fx_wrong_place,
    "backlog-filter": fx_backlog_filter, "newsletter": fx_newsletter, "newsletter-git": fx_newsletter_git,
    "newsletter-second": fx_newsletter_second, "newsletter-standing": fx_newsletter_standing,
    "cold-registry": fx_cold_registry, "cold-registry-no-fit": fx_cold_registry_no_fit,
    "redo-with-rounds": fx_redo_with_rounds, "redo-no-set-aside": fx_redo_no_set_aside,
    "backlog-md-beside-registry": fx_backlog_md_beside_registry, "backlog-plus-retired": fx_backlog_plus_retired,
}

# Fixtures copied from framework-fixtures/ need no tidy; the interview fixtures recompose their fresh
# registry's derived views so it lints clean, as a real leader's would.
TOOLS = ROOT / "registry-template" / "tools"
COMPOSE = {"sales", "expenses", "meals", "winstory", "m-backlog-full", "m-backlog-light", "m-backlog-switch",
           "m-running-light", "m-personal-backlog"}


def tidy(t):
    reg = Path(t).resolve() / "registry"
    if not reg.is_dir():
        return
    r = subprocess.run(["node", str(TOOLS / "compose-registry.js"), str(reg)], cwd=t, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"compose failed for {t}: {r.stderr[-600:]}")


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
    if sys.argv[1] in COMPOSE:
        tidy(target)
    print(target)
