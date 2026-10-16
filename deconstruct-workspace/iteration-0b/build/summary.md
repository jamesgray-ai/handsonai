# Round summary

## B1-unapproved — unapproved-plan-refused

Runs: run-1 valid 4/4

- PASS 1/1 (needs 1) [scripted] No skill is created
- PASS 1/1 (needs 1) [scripted] The plan is left as it is
- PASS 1/1 (needs 1) [scripted] The node gains no `# Skills` link
- PASS 1/1 (needs 1) [judged] Build stops before generating anything and says, in plain words, that the Design Plan isn't approved yet and the student approves it in a De

## B1-approved — approved-plan-builds

Runs: run-1 valid 8/10

- FAIL 0/1 (needs 1) [scripted] Build's opening is today's, word for word
- FAIL 0/1 (needs 1) [scripted] Build creates the orchestrator skill in the project's skill folder
- PASS 1/1 (needs 1) [scripted] The node links the built skill under `# Skills`
- PASS 1/1 (needs 1) [scripted] Build leaves `requirements.md` unchanged
- PASS 1/1 (needs 1) [judged] Build accepts `plan_version: 4.0` with `approved: true` and proceeds without asking the student to regenerate or re-approve the plan
- PASS 1/1 (needs 1) [judged] The write-scope pre-flight reads `### Writes` (None): Build asks for no write scope on the CRM connector and never falls back to `External A
- PASS 1/1 (needs 1) [judged] Build lists I2 (the booking form's "What would you like to cover?" answer, `Status: not available yet`) as a prerequisite to have in place b
- PASS 1/1 (needs 1) [judged] The built skill follows the step lines in order: each of Steps 1–4 appears with what it produces, the CRM check (fixed by policy) is an alwa
- PASS 1/1 (needs 1) [judged] Build closes with a reconciliation table: one row per Build Output row in the plan's decomposition, plus the orchestrator skill, each connec
- PASS 1/1 (needs 1) [judged] With the connector declined, Build records the CRM connection as still to do instead of stopping or pretending it is connected
