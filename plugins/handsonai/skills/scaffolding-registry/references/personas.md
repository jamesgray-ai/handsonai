# Personas

Four kinds of student run this interview. The nodes written are identical for
all four — the same six types, the same frontmatter, the same `SCHEMA.md`.
What changes is the vocabulary of the questions and what each node stands for.
Ask once, in Phase 0, after the folder and mode are confirmed:

> "Who is this registry for — a business you own, a company or unit you lead,
> your role inside an organization, or your personal life?"

The persona is **not stored** in any node. The Business node's identity
sentence carries it ("a household of four" vs. "a boutique consultancy"), and
the `analyze` skill infers the lens from that sentence.

| Persona | Business node | Lines of Business | Functions | Processes | Analyze lens default |
|---|---|---|---|---|---|
| **Founder or owner** | the company | distinct offerings, or one default line named after the company | the starter set, trimmed | the processes that deliver each line | Organizational; Individual offered second |
| **CEO or business leader** | the company, or the unit they lead | business units or offerings | the departments that report in; direct reports as `lead:` only on request | the enterprise processes that deliver each unit, at the level the leader actually sees | Organizational |
| **Professional inside an organization** | their team, department, or function | the services the team provides to the rest of the company, or one default line named after the team | the groups the team hands work to and receives it from; the team itself when no other owner fits | the processes the team runs or takes part in | Individual first (their part of the team's processes); Organizational for the team offered second |
| **Personal life** | the person or household, titled as they choose | the areas of life they want to run better: household, finances, health, family, learning, a side project | the roles they play or the people and services they rely on — at least one, since every Process needs an owner; the starter set is **not** offered | the recurring routines that deliver each area: monthly budgeting, meal planning, travel planning, school logistics | Individual |

## Per-persona openings

Use these in place of the default opening question in each phase. Follow-ups
and "what to write" are unchanged.

### Founder or owner
- **Phase 1:** "What's the name of the business, and what does it do in one sentence?"
- **Phase 2:** "Does the business have distinct lines of business, or is it one thing end to end?"
- **Phase 3:** "Who owns the work day to day? I'll suggest a starter set and you can trim or rename it."
- **Phase 4:** "For each line of business, what are the three to five processes that deliver it — where the time, money, and customer outcomes actually flow? Rank them by how much they matter to the business."

### CEO or business leader
- **Phase 1:** "What's the company or unit you lead, and what does it exist to do, in one sentence?"
- **Phase 2:** "What are the business units or offerings, in the order they matter to you?"
- **Phase 3:** "Which departments report in? I'll start from a standard set; rename to match your org chart."
- **Phase 4:** "For each unit, what are the three to five processes that deliver it at the level you see — order-to-cash, hire-to-onboard, plan-to-report? Rank them by how much they matter."

### Professional inside an organization
- **Phase 1:** "What team or department is this registry for, and what is it responsible for, in one sentence? A team is a perfectly good 'business' here."
- **Phase 2:** "Does your team provide distinct services to the rest of the company, or is it really one thing? One default line named after the team is fine."
- **Phase 3:** "Who do you hand work to, and who hands work to you? Those groups are your functions. Your own team counts as one."
- **Phase 4:** "What are the three to five processes your team runs or takes part in that matter most? Rank them by how much they matter to the team's charter."

### Personal life
- **Phase 0 (add):** "This registry will describe money, health, and family. Keep it on your computer or in a private repository, and skip GitHub Pages."
- **Phase 1:** "Whose life is this registry for — you, or your household? Give it a name you'd be happy to see at the top of a dashboard, and one sentence on what running it well looks like."
- **Phase 2:** "Which areas of life do you want to run better — household, finances, health, family, learning, a side project? Pick the ones that matter now, in order."
- **Phase 3:** "Who does the work in each area — you, a partner, a service you pay for? I'll write each as a role ('Household admin', 'Me') rather than a name. We need at least one."
- **Phase 4:** "For each area, what are the three to five recurring routines that keep it running — monthly budgeting, meal planning, school logistics? Rank them by how much they matter."

## Sketches (shown, never copied)

**Professional:** Business "Data Platform Team" — *"The data platform team for a regional insurer: owns the warehouse, the pipelines, and the reporting layer."* One default LOB "Data Platform". Functions: Data Platform (the team), Finance, Claims, Underwriting. Processes: Pipeline Change Request (owner: data-platform), Monthly Close Reporting (owner: finance), Ad-hoc Analysis Request (owner: data-platform).

**Personal life:** Business "The Okafor Household" — *"A household of four; running well means the admin is invisible and weekends are free."* `## Objectives`: fewer evenings lost to admin; one weekly money check instead of surprises. LOBs: Household, Finances, Kids. Functions: Household admin (lead blank), Me. Processes: Meal Planning (owner: household-admin), Monthly Budget Review (owner: me), School Logistics (owner: household-admin).
