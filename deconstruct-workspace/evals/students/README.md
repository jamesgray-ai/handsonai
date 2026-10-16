# Simulated students

Each file is the script a second agent follows when it plays the student in an interview eval (decided R10-5). The student agent sees only its script and the conversation so far. It answers one message at a time, in the student's own words, and never helps the AI by naming framework terms it hasn't been taught.

Every script has the same parts:
- **Who you are:** the persona.
- **What you know:** the facts the student draws on. Say only what the question asks; volunteer nothing else unless the script says to.
- **How you answer:** the behaviours the eval is testing.
- **When to stop:** reply exactly `END` then.
