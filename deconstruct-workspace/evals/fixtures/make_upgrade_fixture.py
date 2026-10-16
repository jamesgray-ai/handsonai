#!/usr/bin/env python3
"""Build the workspace an upgrade, framework-agent or chain eval starts from (evals-upgrade.json).

Usage: python3 make_upgrade_fixture.py <fixture-name> <target-dir>
       python3 make_upgrade_fixture.py --list

Every upgrade variant is built from the frozen 9.1.0 copy of the worked example
(fixtures/upgrade-9x), never from examples/ (Task 14 regenerates that in the new format).
The -gen variants are built from fixtures/upgrade-9x-generated/<I1|I2>/ (9.1.0 output made
by the I1 and I2 scripts, Task 1 Step 2); until that folder exists they fail with a message.

  U1   an unapproved 9.1 design-spec.md draft (not linked; 9.1 links it only on approval)
  U2   an approved 9.1 design-spec.md, nothing built
  U3   built, the first Test round in progress (E1 graded, E2 and E3 not)
  U4   in-production (the full record, backlog nodes removed)
  U5   the pre-9.0 layout: the full record under outputs/weekly-status-report/
  U6   the full 9.1.0 worked example, as shipped (outputs/ and README.md included)
  U1-gen … U4-gen      the same states on upgrade-9x-generated/I1 (…-I2 for the I2 output)
  A1   an unfinished Deconstruct (renamed backlog workflow, stopped after Part 3)
  C1   the sales registry the I1 script starts from (the chain eval's first session)
"""
import re
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import make_fixture as MF  # noqa: E402  (shared helpers; its EXAMPLE is the frozen upgrade-9x copy)

EXAMPLE = HERE / "upgrade-9x"
GENERATED = HERE / "upgrade-9x-generated"
WSR = MF.WSR
BACKLOG = ["onboarding-checklist-drafting", "program-risk-register", "stakeholder-meeting-prep"]


# ---------- helpers ----------

def drop_field(t, slug, field):
    p = MF.node_path(t, slug)
    p.write_text(re.sub(rf"^{field}: .*\n", "", p.read_text(), count=1, flags=re.M))


def set_generated(t, slug, by):
    p = MF.node_path(t, slug)
    s, n = re.subn(r"^generated: \{ by: [^,]+,", f"generated: {{ by: {by},", p.read_text(), count=1, flags=re.M)
    assert n == 1, slug
    p.write_text(s)


def drop_link(t, slug, label):
    p = MF.node_path(t, slug)
    p.write_text("".join(l for l in p.read_text().splitlines(True) if not l.startswith(f"- [{label}](")))


def wsr_only(t):
    """The worked example with its three backlog nodes removed and the node mid-build."""
    MF.copy_example(t)
    for s in BACKLOG:
        MF.remove_node(t, s)
    MF.set_field(t, WSR, "status", "under-development")
    drop_field(t, WSR, "stale_after")


def in_progress_round(src):
    """A first Test round with only E1 graded, as 9.1 Test leaves it between scenarios
    (test/SKILL.md: counts and readiness are written only at the verdict)."""
    head, body = src.split("\n---\n", 1)
    head = re.sub(r"^round_status: .*$", "round_status: in-progress", head, flags=re.M)
    head = re.sub(r"^readiness: .*\n", "", head, flags=re.M)
    head = re.sub(r"^criteria_total: .*$", "criteria_total: 0", head, flags=re.M)
    head = re.sub(r"^criteria_met: .*$", "criteria_met: 0", head, flags=re.M)
    head = re.sub(r"^  E[23]: .*\n?", "", head, flags=re.M).rstrip("\n")
    card_start = body.index("## Report card")
    card = body[card_start:body.index("**E2", card_start)].rstrip() + "\n"
    deltas_start = body.index("## Golden example deltas")
    deltas_end = body.index("\n## ", deltas_start + 3)
    deltas = body[deltas_start:deltas_end]
    if "**E2" in deltas:
        deltas = deltas[:deltas.index("**E2")]
    return head + "\n---\n" + body[:card_start] + card + "\n" + deltas.rstrip() + "\n"


# ---------- the 9.1.0 worked-example variants ----------

def fx_u1(t):  # an unapproved design-spec.md draft
    wsr_only(t)
    MF.keep_artifacts(t, WSR, ["Opportunity report", "Requirements", "Design spec"], keep_skills=False)
    MF.set_spec_field(t, WSR, "approved", "false")
    # 9.1 Design links the spec and sets execution_mode and autonomy only on approval.
    drop_link(t, WSR, "Design spec")
    drop_field(t, WSR, "execution_mode")
    drop_field(t, WSR, "autonomy")
    set_generated(t, WSR, "process:deconstruct")


def fx_u2(t):  # approved plan, nothing built
    wsr_only(t)
    MF.keep_artifacts(t, WSR, ["Opportunity report", "Requirements", "Design spec"], keep_skills=False)
    set_generated(t, WSR, "process:design")


def fx_u3(t):  # built; the first Test round in progress
    wsr_only(t)
    MF.keep_artifacts(t, WSR, ["Opportunity report", "Requirements", "Design spec"], keep_skills=True)
    set_generated(t, WSR, "process:build")
    folder = t / "framework" / WSR
    src = (EXAMPLE / "framework" / WSR / "test-results-2026-06-05.md").read_text()
    (folder / "test-results.md").write_text(in_progress_round(src))
    (folder / "test-runs").mkdir(exist_ok=True)
    shutil.copy2(EXAMPLE / "framework" / WSR / "test-runs" / "E1-2026-06-05.md", folder / "test-runs")


def fx_u4(t):  # in-production, the full record
    MF.copy_example(t)
    for s in BACKLOG:
        MF.remove_node(t, s)


def to_pre9(text):
    """framework/ paths to the moved record files → their pre-9.0 outputs/ paths (skills/ → skill/).
    Only paths to files or folders the record really holds are rewritten (the spec's packaged .zip
    paths name files that don't exist, so the routine would leave them). The move routine
    (registry-bundle.md, 'Moving a pre-9.0 record out of outputs/') reverses this exactly, so after
    the move every record file should read as it does in upgrade-9x."""
    def swap(m):
        path = m.group(0)
        tail = path[len(path.rstrip(".")):]
        path = path[:len(path) - len(tail)]
        if not (EXAMPLE / path.rstrip("/")).exists():
            return path + tail
        path = path.replace(f"framework/{WSR}/skills/", f"outputs/{WSR}/skill/", 1)
        return path.replace("framework/", "outputs/", 1) + tail
    return re.sub(rf"framework/(?:{WSR}/[^\s`)\]|,;:'\"]*|ai-opportunity-report\.md)", swap, text)


def fx_u5(t):  # the pre-9.0 outputs/ layout
    shutil.copytree(EXAMPLE, t, ignore=shutil.ignore_patterns("README.md"))
    rec = t / "framework" / WSR
    out = t / "outputs" / WSR
    for item in sorted(rec.iterdir()):
        dest = out / ("skill" if item.name == "skills" else item.name)
        shutil.move(str(item), str(dest))
    shutil.move(str(t / "framework" / "ai-opportunity-report.md"), str(t / "outputs" / "ai-opportunity-report.md"))
    shutil.rmtree(t / "framework")
    for p in t.rglob("*.md"):
        if p.relative_to(t).as_posix() == "registry/SCHEMA.md":
            continue
        s = p.read_text()
        if to_pre9(s) != s:
            p.write_text(to_pre9(s))


def fx_u6(t):  # the full 9.1.0 worked example, as shipped
    shutil.copytree(EXAMPLE, t)


# ---------- the generated 9.1.0 variants (pending until Task 1 Step 2 makes them) ----------

def gen_source(which):
    src = GENERATED / which
    if not src.is_dir():
        sys.exit(f"pending: fixtures/upgrade-9x-generated/{which}/ doesn't exist yet. Task 1 Step 2 makes it "
                 f"(9.1.0 output from the {which} script, run on plugin 9.1.0 at commit 5356c73cd).")
    return src


def gen_slug(t, which):
    folders = [p.parent.name for p in (t / "framework").glob("*/requirements.md")]
    if len(folders) != 1:
        sys.exit(f"upgrade-9x-generated/{which}/ should hold one framework/<slug>/requirements.md; found {folders}")
    return folders[0]


def gen_need(t, which, slug, names, state):
    missing = [n for n in names if not (t / "framework" / slug / n).exists()]
    if missing:
        sys.exit(f"upgrade-9x-generated/{which}/ can't make the {state} state: framework/{slug}/ has no "
                 f"{', '.join(missing)}. It needs 9.1.0 output for that step too (run the 9.1.0 step on it).")


# Which saved 9.1.0 stage each state starts from (Task 1 Step 2; evals-generate-9x.json G1/G2).
GEN_STAGE = {"U1": "designed", "U2": "designed", "U3": "test-in-progress", "U4": "running"}


def make_gen(state, which):
    def build(t):
        stage = which if which == "I2" else f"{which}-{GEN_STAGE[state]}"
        shutil.copytree(gen_source(stage), t)
        slug = gen_slug(t, which)
        if state == "U1":
            gen_need(t, which, slug, ["design-spec.md"], "unapproved-draft")
            MF.keep_artifacts(t, slug, ["Opportunity report", "Requirements", "Design spec"], keep_skills=False)
            MF.set_spec_field(t, slug, "approved", "false")
            drop_link(t, slug, "Design spec")
        elif state == "U2":
            gen_need(t, which, slug, ["design-spec.md"], "approved-plan")
            MF.keep_artifacts(t, slug, ["Opportunity report", "Requirements", "Design spec"], keep_skills=False)
            MF.set_spec_field(t, slug, "approved", "true")
        elif state == "U3":
            gen_need(t, which, slug, ["design-spec.md", "skills", "test-results.md"], "Test-round-in-progress")
            tr = t / "framework" / slug / "test-results.md"
            if not re.search(r"^round_status: in-progress", tr.read_text(), re.M):
                sys.exit(f"upgrade-9x-generated/{which}/: framework/{slug}/test-results.md is not a round in progress")
        elif state == "U4":
            gen_need(t, which, slug, ["design-spec.md", "test-results.md", "run-guide.md"], "in-production")
            MF.set_field(t, slug, "status", "in-production")
    return build


FIXTURES = {
    "U1": fx_u1, "U2": fx_u2, "U3": fx_u3, "U4": fx_u4, "U5": fx_u5, "U6": fx_u6,
    "A1": MF.fx_r5,
    "C1": MF.fx_sales,
}
for _n in ("U1", "U2", "U3", "U4"):
    FIXTURES[f"{_n}-gen"] = make_gen(_n, "I1")
    FIXTURES[f"{_n}-gen-I2"] = make_gen(_n, "I2")

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
    MF.tidy(target)
    print(target)
