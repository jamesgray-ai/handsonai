# Starter Rules

The starting point for a first draft, and for any new rule in Review mode. Each rule rests on one or more of the **eight governance practices**, in two groups:

- **Register it** (what the workflow is and where it lives): 1 name and description, 2 ownership (a team, not a person), 3 process (what comes before and after it).
- **Control it** (how it's built, checked and changed): 4 building blocks (its skills, agents, and the systems and files it touches), 5 evaluations (tests for the skills, the agents and the whole workflow), 6 SOP (how it runs, written for people), 7 operations (when it runs and where its outputs go), 8 change management (who approves a change and how it reaches the team).

Reword each rule in the company's own terms. The starter check is used only when the company has nothing that already does the job; a check that isn't in place yet is marked planned, with what will deliver it.

## Always start with these

| Practice | Starter rule | Starter check |
|---|---|---|
| 1–3 | Every AI workflow is in the AI Registry, with a name, a description, and a process owned by a team. | Weekly registry look: the policy owner opens the registry and its dashboard |
| 4 | Every agent can use only the tools and connections its work needs. | Access review: monthly, against each workflow's build record of what it can access |
| 5 | Every workflow passes its tests before it goes live, and is re-checked by its re-check date. | Test results: in the workflow's folder; Weekly registry look: re-check dates passed |
| 6 | Every live workflow that a team relies on has an SOP. | Weekly registry look: live team workflows with no SOP |
| 7 | Every live workflow's SOP says when it runs, where its outputs go, and who is told when it fails. | Weekly registry look: live workflows whose SOP is missing these |
| 8 | Every change to a skill, agent or workflow is reviewed before it reaches the team. Where skills reach the team as a plugin, add: and reaches them as a new plugin version. | Release review: before each release to the team |
| — | This policy is reviewed each quarter and after any incident. | Quarterly policy review: the owner runs "review our AI governance policy" |

## When to add

| Add when Part 1 shows | Rule | Starter check |
|---|---|---|
| Work that runs without a person (on a schedule, or when something arrives) | Every workflow that runs without a person runs only reviewed instructions, and its schedule or what starts it is recorded in its registry entry. | Weekly registry look: scheduled and triggered workflows |
| Anything sent to customers, or a change to a system other people use | Anything a workflow sends to a customer, or changes in a shared system, waits for a person's approval unless the owner has approved otherwise in writing. | Test results: the approval step was checked; Release review |
| Named confidential information | No AI workflow reads [the named categories]. | Access review: no build record lists access to them |
| Confidential information, but none named yet | No AI workflow reads information the policy owner names as confidential. | Quarterly policy review: the owner names the categories, from the first quarterly review |
| Outside AI tools or vendors that hold company information | Every outside AI tool that holds company information is approved by the policy owner before use. | Quarterly policy review: the list of outside AI tools, from the first quarterly review when none are named yet |
| Live workflows with no `test-results.md` | Every live skill and agent has its own tests, updated whenever it changes. | Release review: tests updated with the change, from the next release that adds them |

## Notes for drafting

- **Practices 1–3 and 8 are the foundation:** without them, nobody can say what exists or what changed. Explain this in one line before dropping one, then do as the user says.
- **Gaps from any governance records** (evaluations and SOPs are the usual ones) make a rule more important, not less: keep the rule and mark its check planned, so the gap is visible.
- **Keep the list short.** A rule that no check confirms within minutes belongs in a governance record's follow-up actions, not in the policy.
