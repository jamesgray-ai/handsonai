#!/usr/bin/env python3
"""Build the workspace a Deconstruct eval starts from.

Usage: python3 make_fixture.py <fixture-name> <target-dir>

Every fixture is built from files already in the repo
(examples/weekly-status-report and registry-template/registry), so the
fixtures stay in step with the worked example instead of being copied.
Run `python3 make_fixture.py --list` for the fixture names.
"""
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
EXAMPLE = ROOT / "examples" / "weekly-status-report"
TEMPLATE = ROOT / "registry-template" / "registry"
WSR = "weekly-status-report"


# ---------- helpers ----------

def copy_example(t):
    shutil.copytree(EXAMPLE, t, ignore=shutil.ignore_patterns("outputs", "README.md"))


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
        "generated: { by: process:scaffolding-registry, at: 2026-09-01 }\n---\n"
        f"# {business}\n"
    )


def node_path(t, slug):
    return t / "registry" / "workflows" / f"{slug}.md"


def add_node(t, slug, title, description, trigger, status="backlog", body_extra=""):
    node_path(t, slug).write_text(
        "---\ntype: Workflow\n"
        f'title: "{title}"\n'
        f'description: "{description}"\n'
        "generated: { by: process:analyze, at: 2026-09-01 }\n"
        f"status: {status}\n"
        f'trigger: "{trigger}"\n---\n'
        f"# {title}\n\n{description}\n{body_extra}\n"
        "# Artifacts\n\n# Skills\n\n# Agents\n"
    )
    idx = t / "registry" / "workflows" / "index.md"
    kept = [l for l in idx.read_text().splitlines() if not l.startswith("_No entries yet")]
    idx.write_text("\n".join(kept).rstrip("\n") + f"\n- [{title}](/workflows/{slug}.md)\n")


def remove_node(t, slug):
    p = node_path(t, slug)
    if p.exists():
        p.unlink()
    idx = t / "registry" / "workflows" / "index.md"
    idx.write_text("".join(l for l in idx.read_text().splitlines(True) if f"/{slug}.md)" not in l))
    shutil.rmtree(t / "framework" / slug, ignore_errors=True)


def set_field(t, slug, field, value):
    p = node_path(t, slug)
    s = p.read_text()
    s, n = re.subn(rf"^{field}: .*$", f"{field}: {value}", s, count=1, flags=re.M)
    assert n == 1, (slug, field)
    p.write_text(s)


def keep_artifacts(t, slug, labels, keep_skills):
    """Keep only the named # Artifacts links (and files); drop # Skills when keep_skills is False."""
    p = node_path(t, slug)
    lines = p.read_text().splitlines(True)
    out, section = [], None
    for l in lines:
        if l.startswith("# "):
            section = l.strip()
        if section == "# Artifacts" and l.startswith("- ["):
            label = l[3:l.index("]")]
            if label not in labels:
                continue
        if section == "# Skills" and l.startswith("- [") and not keep_skills:
            continue
        out.append(l)
    p.write_text("".join(out))
    folder = t / "framework" / slug
    keep_files = {
        "Requirements": ["requirements.md", "inputs", "context"],
        "Design spec": ["design-spec.md"],
        "Test results": ["test-results.md", "test-runs"],
    }
    wanted = {"inputs", "context"}
    for label in labels:
        wanted.update(keep_files.get(label, []))
    if keep_skills:
        wanted.add("skills")
    for item in list(folder.iterdir()):
        if item.name not in wanted:
            shutil.rmtree(item) if item.is_dir() else item.unlink()


def set_spec_field(t, slug, field, value):
    p = t / "framework" / slug / "design-spec.md"
    s = p.read_text()
    s, n = re.subn(rf"^{field}: .*$", f"{field}: {value}", s, count=1, flags=re.M)
    assert n == 1
    p.write_text(s)


def progress_file(t, folder, node, next_part, notes):
    d = t / "framework" / folder
    d.mkdir(parents=True, exist_ok=True)
    (d / "deconstruct-in-progress.md").write_text(
        f"Next: {next_part}\nWorkflow node: {node}\n\n{notes}\n"
    )


RISK_NOTES = """## What this is worth
Maya spends about half a day each month pulling risks out of tracker comments. Value: the steering group sees every open risk with an owner, and Maya gets the afternoon back.

## Scope and a name
Trigger: month end, before the steering meeting. Deliverable: the risk register in the steering group's format. Name: Monthly Risk Register (renamed from Program Risk Register). Law or regulation: no. Governing regime: None.

## The outcome
Goal: For each month end, a risk register for the steering group, ready the day before the steering meeting.
Checks: AC1 (must) every open risk in the tracker appears; AC2 (must) every risk names an owner; AC3 each risk has a status from the steering group's list.
Real output: none yet."""


# ---------- fixtures ----------

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


def fx_r1(t):  # walk d: designed and built, not tested, not running
    copy_example(t)
    for s in ["onboarding-checklist-drafting", "program-risk-register", "stakeholder-meeting-prep"]:
        remove_node(t, s)
    set_field(t, WSR, "status", "under-development")
    keep_artifacts(t, WSR, ["Opportunity report", "Requirements", "Design spec"], keep_skills=True)


def fx_r2(t):  # walk g: running, with Requirements
    copy_example(t)


def fx_r3(t):  # walk h: running work Analyze recorded, no Requirements
    copy_example(t)
    for s in [WSR, "onboarding-checklist-drafting", "program-risk-register"]:
        remove_node(t, s)
    set_field(t, "stakeholder-meeting-prep", "status", "in-production")
    p = node_path(t, "stakeholder-meeting-prep")
    s = p.read_text().replace("\n# Artifacts", "\nRuns today as a ChatGPT prompt Maya pastes before each stakeholder meeting.\n\n# Artifacts", 1)
    p.write_text(s)


def fx_r4(t):  # walk f: re-run of a designed-but-unbuilt workflow, stopped after Part 3
    copy_example(t)
    for s in ["onboarding-checklist-drafting", "program-risk-register", "stakeholder-meeting-prep"]:
        remove_node(t, s)
    set_field(t, WSR, "status", "under-development")
    keep_artifacts(t, WSR, ["Opportunity report", "Requirements", "Design spec"], keep_skills=False)
    set_spec_field(t, WSR, "approved", "false")
    progress_file(t, WSR, f"registry/workflows/{WSR}.md", "Part 4 — The path",
                  "## What this is worth\nMaya's Friday mornings back; leadership has the picture before the 11am sync.\n\n"
                  "## Scope and a name\nTrigger: Maya starts it Friday mornings. Deliverable: the leadership status report. Name: Weekly Status Report. Law or regulation: no. Governing regime: None.\n\n"
                  "## The outcome\nGoal: For each Friday, a one-page status report for the leadership team, ready by 10am.\n"
                  "Checks: AC1 (must) every status matches the tracker; AC2 the four sections in order; AC3 Maya could send it without rewording.")


def fx_r5(t):  # walk e: backlog workflow renamed in Part 2, stopped after Part 3
    copy_example(t)
    progress_file(t, "monthly-risk-register", "registry/workflows/program-risk-register.md",
                  "Part 4 — The path", RISK_NOTES)


def fx_r6(t):  # cold entry: a new workflow with no node, stopped after Part 2
    copy_example(t)
    progress_file(t, "vendor-invoice-intake", "none — new workflow", "Part 3 — The outcome",
                  "## What this is worth\nAbout two hours a week keying vendor invoices.\n\n"
                  "## Scope and a name\nTrigger: a vendor invoice arrives in the shared inbox. Deliverable: an invoice entry ready for approval. "
                  "Name: Vendor Invoice Intake. Law or regulation: no. Governing regime: None.")


def fx_r7(t):  # another workflow unfinished; the student names a different one
    fx_r5(t)


def fx_r8(t):  # retired, with Requirements
    copy_example(t)
    set_field(t, WSR, "status", "retired")


def no_registry_wsr(t):
    copy_example(t)
    for item in ["registry", "REGISTRY.md"]:
        p = t / item
        shutil.rmtree(p) if p.is_dir() else p.unlink()
    folder = t / "framework" / WSR
    for item in list(folder.iterdir()):
        if item.name not in {"requirements.md", "design-spec.md", "inputs", "context"}:
            shutil.rmtree(item) if item.is_dir() else item.unlink()


def fx_r9(t):  # walk i: no registry, plan, nothing built in the folder
    no_registry_wsr(t)


def r9_variant(t, readiness, round_status):
    no_registry_wsr(t)
    src = (EXAMPLE / "framework" / WSR / "test-results.md").read_text()
    src = re.sub(r"^readiness: .*$", f"readiness: {readiness}", src, count=1, flags=re.M)
    src = re.sub(r"^round_status: .*$", f"round_status: {round_status}", src, count=1, flags=re.M)
    (t / "framework" / WSR / "test-results.md").write_text(src)


def fx_r9_notready(t):
    r9_variant(t, "not-ready", "complete")


def fx_r9_ready(t):
    r9_variant(t, "ready", "complete")


def fx_r9_inprogress(t):
    r9_variant(t, "not-ready", "in-progress")


def fx_r10(t):  # old step-driven file, nothing built, no plan
    copy_example(t)
    for s in ["onboarding-checklist-drafting", "program-risk-register", "stakeholder-meeting-prep"]:
        remove_node(t, s)
    set_field(t, WSR, "status", "under-development")
    keep_artifacts(t, WSR, ["Opportunity report", "Requirements"], keep_skills=False)


FIXTURES = {
    "sales": fx_sales, "expenses": fx_expenses, "meals": fx_meals, "winstory": fx_winstory,
    "R1": fx_r1, "R2": fx_r2, "R3": fx_r3, "R4": fx_r4, "R5": fx_r5, "R6": fx_r6, "R7": fx_r7,
    "R8": fx_r8, "R9": fx_r9, "R9-not-ready": fx_r9_notready, "R9-ready": fx_r9_ready,
    "R9-in-progress": fx_r9_inprogress, "R10": fx_r10,
}

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
    print(target)
