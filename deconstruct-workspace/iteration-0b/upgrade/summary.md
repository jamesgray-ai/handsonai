# Round summary

## U4 — upgrade-in-production

Runs: run-1 valid 2/5

- FAIL 0/1 (needs 1) [scripted] The AI says "This workflow already has a Design Plan, so changes to its requirements go through Improve. Say 'run the improve skill'."
- FAIL 0/1 (needs 1) [scripted] Deconstruct does not re-run: no AI message says the Deconstruct opening (the 10.0 opening or 9.1's)
- PASS 1/1 (needs 1) [scripted] No loss: `framework/*` is byte-identical before and after (every record file of the in-production workflow)
- PASS 1/1 (needs 1) [scripted] The node's `status` stays `in-production`
- FAIL 0/1 (needs 1) [judged, must] The AI gives the Improve message on its own (it may name the workflow) and starts no interview, design, build or test work
