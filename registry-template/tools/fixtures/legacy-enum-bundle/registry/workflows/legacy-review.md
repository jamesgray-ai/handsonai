---
type: Workflow
title: "Legacy Review"
description: "Fixture workflow written before 10.0, with the legacy labels and the legacy step-decomposed definition_type spelling."
generated: { by: process:fixture, at: 2026-08-01 }
status: under-development
definition_type: step-decomposed
execution_mode: manual
autonomy: guided
trigger: "manual"
---
# Legacy Review

Fixture workflow from before 10.0: its `# Artifacts` keep the legacy labels "Design spec",
"Run guide" and "Improvement plan", tolerated on a node with a bare-date `generated.at` and
never written by a current step; its `definition_type` still carries the legacy
`step-decomposed` spelling, which lint warns about but never errors on (see
`LEGACY_TOLERATED` in `registry-lib.js`). Routing reads the folder as an earlier version.

# Artifacts

- [Requirements](framework/legacy-review/requirements.md)
- [Design spec](framework/legacy-review/design-spec.md)
- [Run guide](framework/legacy-review/run-guide.md)
- [Improvement plan](framework/legacy-review/improvement-plan.md)

# Skills

# Agents
