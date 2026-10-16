# Round summary

## U3 — upgrade-test-round-in-progress

Runs: run-1 valid 12/14

- PASS 1/1 (needs 1) [scripted] Deconstruct does not re-run: no AI message says the Deconstruct opening (the 10.0 opening or 9.1's)
- FAIL 0/1 (needs 1) [scripted] The resume orientation names Step 5 (Test) as next (today's line: "You've completed through Step [N] ([name]) — next is Step [N+1] ([name]).
- FAIL 0/1 (needs 1) [scripted] Test resumes the round with today's line, naming 1 of 3 graded ("N of M graded — run E(next) in a new chat next")
- PASS 1/1 (needs 1) [scripted] Test opens no new round: the round file is not renamed (no `test-results-YYYY-MM-DD.md`)
- PASS 1/1 (needs 1) [scripted] No loss in `test-results.md`: either unchanged, or E1's frontmatter entry, the check list, scenarios and E1's report card, and E1's golden e
- PASS 1/1 (needs 1) [scripted] No loss: `framework/weekly-status-report/requirements.md` is byte-identical before and after (the 9.1 requirements)
- PASS 1/1 (needs 1) [scripted] No loss: `framework/weekly-status-report/design-spec.md` is byte-identical before and after (the approved 9.1 spec)
- PASS 1/1 (needs 1) [scripted] No loss: `framework/weekly-status-report/skills/*` is byte-identical before and after (the built skills)
- PASS 1/1 (needs 1) [scripted] No loss: `framework/weekly-status-report/test-runs/E1-2026-06-05.md` is byte-identical before and after (E1's saved test run)
- PASS 1/1 (needs 1) [scripted] No loss: `framework/weekly-status-report/inputs/*` is byte-identical before and after (the scenario inputs)
- PASS 1/1 (needs 1) [scripted] No loss: `framework/ai-opportunity-report.md` is byte-identical before and after (Analyze's report)
- PASS 1/1 (needs 1) [scripted] No loss in the Workflow node: its title, description, trigger and earlier `# Artifacts` links are kept (only the links and fields the reache
- PASS 1/1 (needs 1) [judged, must] Test reads the 9.1 round file (its `design_spec:` key and `round_status: in-progress`) and resumes that round: it doesn't open a new round, 
- PASS 1/1 (needs 1) [judged, must] Test names E2 (the blocked-heavy week) as the next scenario and hands over its input from `framework/weekly-status-report/inputs/E2-blocked-
