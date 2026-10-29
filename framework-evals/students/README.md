# Simulated leaders

Each file is the script a second agent follows when it plays the leader in an eval (decided R10-5). The leader agent sees only its script, the conversation so far and what its screen shows (`leader.py`'s platform simulations). It answers one message at a time, in the leader's own words, and never helps the AI by naming framework or evaluation terms it hasn't been taught.

Every script has the same parts:
- **Who you are:** the persona.
- **What you know:** the facts the leader draws on. Say only what the question asks; volunteer nothing else unless the script says to.
- **How you answer:** the behaviours the eval is testing.
- **When to stop:** reply exactly `END` then.

The scripts here are shared by the step eval sets (Design, Build, Test, indexing-registry). Deconstruct's interview scripts (I1–I20, NF1, R4, R10) stay with its own evals in `deconstruct-workspace/evals/students/`. The Run, Improve and upgrade scripts were retired with those skills (R9, R12).
