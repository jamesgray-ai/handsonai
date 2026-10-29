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
  newsletter candidate for the light track, standing rules, a Git repository, and so on).

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


def progress_file(t, slug, node, next_part, track, notes, root="framework"):
    d = t / root / slug
    d.mkdir(parents=True, exist_ok=True)
    (d / "deconstruct-in-progress.md").write_text(
        f"Next: {next_part}\nWorkflow node: {node}\nTrack: {track}\n\n{notes}\n")


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


CFU_NOTES = ("## What this is worth\nAbout 20 minutes per call today; you'd like it down to 5.\n\n"
             "## Scope and a name\nClient Follow-Up: drafts a follow-up email after each client call from your call notes, "
             "for you to review and send. Law or regulation: no. Governing regime: None.")
WPS_NOTES = ("## What this is worth\nAbout an hour every Friday pulling deals out of HubSpot.\n\n"
             "## Scope and a name\nWeekly Pipeline Summary: summarises your open deals every Friday from HubSpot, "
             "for you to review before the Monday sales meeting. Law or regulation: no. Governing regime: None.")


def fx_one_unfinished(t):  # one interview partway (Client Follow-Up), Weekly Pipeline Summary still in the backlog
    ff(t, "continue/c-only-backlog/with-registry")
    progress_file(t, CFU, f"registry/workflows/{CFU}.md", "Part 3 — The outcome", "full", CFU_NOTES)


def fx_two_unfinished(t):  # two interviews partway, no workflow named: deconstruct 3.3's list question
    fx_one_unfinished(t)
    progress_file(t, WPS, f"registry/workflows/{WPS}.md", "Light — the goal", "light", WPS_NOTES)


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


def fx_newsletter(t):  # a first-time leader's backlog with a clearly light candidate (the light track)
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


FIXTURES = {
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
COMPOSE = {"sales", "expenses", "meals", "winstory"}


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
