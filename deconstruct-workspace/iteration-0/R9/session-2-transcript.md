## Student

Run the deconstruct skill for Weekly Status Report.

## AI

Weekly Status Report has already been through this step, so I haven't re-run it. Running it again would archive your current requirements file and start the whole interview over.

Here's what's already in `framework/weekly-status-report/`:

- **`requirements.md`**: the full requirements from Step 2. It covers 4 steps (pull the week's updates → draft the report → Maya reviews → save and log), 3 context items, 3 acceptance criteria (AC1, "nothing is invented", must pass), 5 rules, 2 review points where Maya approves or decides (G1, G2), and 3 test inputs.
- **`inputs/`**: E1–E3 (typical week, a week with many blocked tasks, quiet week), each saved as its own file.
- **`design-spec.md`**: the Step 3 design, marked approved. It plans the workflow as a skill Maya runs by name.

So you've completed through Step 3 (Design). **Next is Step 4 (Build).** To start it, say "run the build skill".

The requirements are now out of date in one place. They list the tone guide (C3) as "Needs Creation — does not exist yet", but `context/tone-guide.md` now exists. It matches the rules in the requirements: direct, no hedging, every blocker has an owner, under 400 words, the four sections in order. The design spec also plans to create it during Build, so Build will find it already there. I can mark C3 as existing in the requirements now; it's a one-line change.

You don't have a registry yet, so this workflow's requirements live in its folder for now. When you want your workflows saved and shown on a dashboard, say "run the scaffolding-registry skill".

If you meant to redo Step 2 because something changed, tell me what changed. I can update just that part, or redo the whole interview with the current file saved as `requirements-2026-10-15.md`. A redo would also likely mean revisiting the design.

## Student

no

## AI

OK, I've left everything as it is: no edit to the tone guide entry and no redo of Step 2.

When you're ready for the next step, say "run the build skill". It will find `context/tone-guide.md` already in place.
