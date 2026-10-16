#!/usr/bin/env python3
"""Build the workspace a Deconstruct eval starts from.

Usage: python3 make_fixture.py <fixture-name> <target-dir>

Every fixture is built from the frozen 9.1.0 copy of the worked example
(fixtures/upgrade-9x) and registry-template/registry.
Run `python3 make_fixture.py --list` for the fixture names.
"""
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
# The frozen 9.1.0 copy of the worked example (Task 1 Step 2): Task 14 regenerates
# examples/weekly-status-report in the new format, and these fixtures must keep the old one.
EXAMPLE = Path(__file__).resolve().parent / "upgrade-9x"
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
    vendor_progress(t)


def vendor_progress(t):
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


def fx_r8_continue(t):  # retired, with Requirements, the only node (so "continue my workflow" finds one workflow)
    fx_r8(t)
    for s in ["onboarding-checklist-drafting", "program-risk-register", "stakeholder-meeting-prep"]:
        remove_node(t, s)


def fx_r9_runguide(t):  # no registry: requirements.md plus run-guide.md, which means running (check 2)
    no_registry_wsr(t)
    shutil.copy(EXAMPLE / "framework" / WSR / "run-guide.md", t / "framework" / WSR / "run-guide.md")


# ----- old requirements formats (Global Constraints "Back-compat"; spec section 6) -----

DT_ROW = "| Definition Type | Step-Driven |\n"


def req_path(t):
    return t / "framework" / WSR / "requirements.md"


def edit_req(t, *pairs):
    p = req_path(t)
    s = p.read_text()
    for old, new in pairs:
        assert old in s, old[:60]
        s = s.replace(old, new, 1)
    p.write_text(s)


def drop_section(t, heading, upto):
    """Remove the requirements text from `heading` up to (not including) `upto`."""
    p = req_path(t)
    s = p.read_text()
    p.write_text(s[:s.index(heading)] + s[s.index(upto):])


def drop_node_field(t, slug, field):
    p = node_path(t, slug)
    s, n = re.subn(rf"^{field}: .*\n", "", p.read_text(), count=1, flags=re.M)
    assert n == 1, (slug, field)
    p.write_text(s)


def fx_r10_norow(t):  # old step-driven: `## Steps Overview`, no Definition Type row (design/SKILL.md:52 reads it as step-driven)
    fx_r10(t)
    edit_req(t, (DT_ROW, ""))
    drop_node_field(t, WSR, "definition_type")


GOAL_INPUTS = """## Inputs

- This week's task changes and comments from the HubSpot project tracker "Q2 Delivery Tracker" (C1)
- The current date, which sets the 7-day window
- The report template and three past reports (C2)
- The tone guide (C3), once it exists

"""


def goal_driven(t, value, goal_heading):
    """Today's Deconstruct goal-driven layout (deconstruct/SKILL.md, "Goal-Driven middle block"):
    a Definition Type row, `## Inputs` between Metadata and Context Inventory, and no Steps Overview,
    Step Details, Sequence or Optimization Notes."""
    fx_r10(t)
    edit_req(t, (DT_ROW, f"| Definition Type | {value} |\n"))
    drop_section(t, "## Steps Overview", "## Context Inventory")
    edit_req(t, ("## Context Inventory", GOAL_INPUTS + "## Context Inventory"))
    p = req_path(t)
    s = p.read_text()
    s = s[:s.index("## Optimization Notes")].rstrip("\n") + "\n"
    for old, new in [
        ("| C1 | HubSpot project tracker | 1 |", "| C1 | HubSpot project tracker | All |"),
        ("| C2 | Report template + 3 past reports | 2 |", "| C2 | Report template + 3 past reports | All |"),
        ("| C3 | Tone guide | 2 |", "| C3 | Tone guide | All |"),
        ("tests R1 and the Step 2 ownerless-blocker edge case", "tests R1 and the ownerless-blocker edge case"),
        ("| G1 | Step 3 |", "| G1 | Before the report is saved or shared |"),
        ("| G2 | Step 2 |", "| G2 | While drafting |"),
    ]:
        assert old in s, old
        s = s.replace(old, new, 1)
    if goal_heading != "## Goal":
        s = s.replace("\n## Goal\n", f"\n{goal_heading}\n", 1)
    assert "## Path" not in s and "## Steps Overview" not in s and "### Step " not in s
    p.write_text(s)


def fx_r10_goal(t):  # old goal-driven: `Definition Type: Goal-Driven`, `## Inputs`, no `## Path`
    goal_driven(t, "Goal-Driven", "## Goal")
    set_field(t, WSR, "definition_type", "goal-driven")


def fx_r10_outcome(t):  # legacy goal-driven: the `Outcome-Driven` value and the `## Outcome` heading
    goal_driven(t, "Outcome-Driven", "## Outcome")
    set_field(t, WSR, "definition_type", "outcome-driven")


def fx_r10_nomarkers(t):  # none of the markers: no Definition Type row, Steps Overview, Inputs or Path
    fx_r10(t)
    edit_req(t, (DT_ROW, ""), ("## Steps Overview", "## How the work goes"), ("## Step Details", "## Notes on each part"))
    drop_section(t, "## Sequence", "## Context Inventory")
    s = req_path(t).read_text()
    for marker in ("Definition Type", "## Steps Overview", "## Inputs", "## Path"):
        assert marker not in s, marker
    drop_node_field(t, WSR, "definition_type")


def fx_r11(t):  # built (approved Design spec, # Skills linked), not running, named directly
    fx_r1(t)


def fx_r12(t):  # two unfinished interviews: R5's renamed backlog workflow and R6's cold-entry one
    fx_r5(t)
    vendor_progress(t)


FIXTURES = {
    "sales": fx_sales, "expenses": fx_expenses, "meals": fx_meals, "winstory": fx_winstory,
    "R1": fx_r1, "R2": fx_r2, "R3": fx_r3, "R4": fx_r4, "R5": fx_r5, "R6": fx_r6, "R7": fx_r7,
    "R8": fx_r8, "R8-continue": fx_r8_continue, "R9": fx_r9, "R9-not-ready": fx_r9_notready,
    "R9-ready": fx_r9_ready, "R9-in-progress": fx_r9_inprogress, "R9-run-guide": fx_r9_runguide,
    "R10": fx_r10, "R10-no-row": fx_r10_norow, "R10-goal": fx_r10_goal, "R10-outcome": fx_r10_outcome,
    "R10-no-markers": fx_r10_nomarkers, "R11": fx_r11, "R12": fx_r12,
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
