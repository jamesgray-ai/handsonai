---
type: Workflow
title: "Legacy Review"
description: "Fixture workflow carrying the legacy step-decomposed definition_type spelling."
generated: { by: process:fixture, at: 2026-08-01 }
status: under-development
definition_type: step-decomposed
execution_mode: manual
autonomy: guided
trigger: "manual"
---
# Legacy Review

Fixture workflow whose `definition_type` still carries the legacy
`step-decomposed` spelling -- lint must warn, not error, on this value
(see `LEGACY_TOLERATED` in `registry-lib.js`).
