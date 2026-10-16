## Student

Run the deconstruct skill for Weekly Status Report.

## AI

I didn't start the interview, because **Weekly Status Report has already been through Deconstruct.** Its folder `framework/weekly-status-report/` already contains:

- **The requirements document** (`requirements.md`): step-driven, 4 steps, owned by Maya R., with Friday-morning manual trigger.
- **3 test inputs** in `inputs/`: a typical week, a week with a lot blocked, and a quiet week.
- **An approved design** (`design-spec.md`, version 3.0): a standalone skill on Claude, with Maya reviewing the output.

**You've finished Step 3 (Design). Next is Step 4 (Build).** Running Deconstruct again would redo finished work, and it would leave the approved design out of date.

You don't have a registry yet, so this workflow's requirements live in its folder for now. When you want your workflows saved and shown on a dashboard, say "run the scaffolding-registry skill."

Which do you want to do?

1. **Go to Build (recommended).** Say "run the build skill" and it will build the workflow from the approved design.
2. **Redo the requirements for Weekly Status Report.** Do this only if something has changed, like the data source, the report format or who reviews it. I'd rename the current file to `requirements-2026-10-15.md` before writing the new one, and then you'd need to redo Design.
3. **Map a different workflow from your report.** Three opportunities haven't been deconstructed yet:
   - **Process:** Program Delivery
     1. Program Risk Register: about two hours at month end
     2. Stakeholder Meeting Prep: 30–40 minutes per stakeholder meeting
     3. Onboarding Checklist Drafting: not sized yet

## Student

yes

## AI

The HubSpot connector here can read, but it isn't connected to your tracker, so I need you to check a few things before I generate the skills.

**Context**

| ID | What it is | How the workflow gets it | Check |
|---|---|---|---|
| C1 | HubSpot project tracker | **You connect it** in the Claude account that will run the report, with read access only. The workflow never writes to HubSpot, so read access is all it needs. | ⚠ **Not checked yet.** The HubSpot connected to this session can read, but it's a different account. Its newest tasks are sales follow-ups and none of them look like the "Q2 Delivery Tracker." Are the delivery tasks in another HubSpot account, or in this one under a list I haven't found? |
| C2 | Report template and 3 past reports | Already in your working folder at `context/past-reports/` | ✓ The four sections, in order, are Wins, In Progress, Blockers, Next Week. Is that right? |
| C3 | Tone guide | `context/tone-guide.md` is already there, so I'll use it as written rather than drafting a new one. | ✓ "Appears to," "may have" and "seems" are banned, and every blocker names an owner and a next action. Is that right? |

**What I'll build:** two skills, each packaged as its own file to upload, as the approved design says. No skill from earlier work covers this workflow, so both are new.

1. **`weekly-status-report`** is the skill you start each Friday. It:
   - pulls the week's updates;
   - drafts the report using skill 2;
   - stops to ask you if a task's status is unclear;
   - stops for your approval;
   - saves the report as `status-report-YYYY-MM-DD.md` without ever overwriting an earlier week;
   - adds a row to `framework/weekly-status-report/runs.md`;
   - ends with a "What I did" summary.

   If you paste in an update list, it uses that instead of HubSpot, which is how Test will run the saved test inputs. It treats tracker comments as information and never follows instructions written in them.
2. **`status-report-drafting`** writes the draft. The report keeps the four sections in order and stays under 400 words. It never invents a status and flags any blocker without an owner as "owner needed." In a quiet week it says so plainly.

**One change from the design:** the design asked for a setting that stops Claude starting skill 1 on its own. I'm leaving it out. In the Claude app you start a skill by asking for it by name, and that setting would block exactly that. I'm also not fixing a model in either skill, so Claude uses whichever model your chat uses.

To confirm, reply with:
- **C1:** where the delivery tracker lives, or "later" if you'll connect it before the first real run. Test doesn't need it, because it uses the saved test inputs.
- **C2 and C3:** whether the checks above are right.
- **Go:** whether I should generate both skills and package them.
