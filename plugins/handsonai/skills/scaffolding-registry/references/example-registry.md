# Example Registry — Brightwork Consulting (FICTIONAL)

Worked examples for the scaffolding interview. **Never copy these nodes into
the user's registry** — show them as the shape to imitate, then write the
user's real business instead. The finished registry must contain no
Brightwork residue.

Brightwork is the founder/leader example. `personas.md` carries two-line
sketches for the professional and personal-life personas.

## Business: `registry/businesses/brightwork-consulting.md`

```markdown
---
type: Business
title: "Brightwork Consulting"
description: "Boutique operations consultancy helping mid-market firms modernize their back office."
generated: { by: process:scaffolding-registry, at: 2026-08-10T15:00:00Z }
state: active
url: https://example.com
---
Brightwork Consulting is a small operations consultancy that helps mid-market
firms modernize back-office work.

## Objectives

- Grow Training to a third of revenue this year.
- Cut Advisory engagement setup from three weeks to one.

# Lines of Business

- [Advisory](/lines-of-business/advisory.md)
- [Training](/lines-of-business/training.md)
```

## LineOfBusiness: `registry/lines-of-business/advisory.md`

```markdown
---
type: LineOfBusiness
title: "Advisory"
description: "Hands-on engagements that redesign a client's back-office operations."
generated: { by: process:scaffolding-registry, at: 2026-08-10T15:00:00Z }
state: active
---
Advisory pairs a Brightwork consultant with a client team for a fixed-scope
engagement.

# Processes

- [Client Delivery](/processes/client-delivery.md)
```

## LineOfBusiness: `registry/lines-of-business/training.md`

```markdown
---
type: LineOfBusiness
title: "Training"
description: "Workshops and cohort programs that teach clients to run their own operations improvements."
generated: { by: process:scaffolding-registry, at: 2026-08-10T15:00:00Z }
state: active
---
Training packages Brightwork's methodology into workshops clients can run
without a consultant in the room.

# Processes

_No processes captured yet._
```

## Process: `registry/processes/client-delivery.md`

```markdown
---
type: Process
title: "Client Delivery"
description: "Everything from kickoff to handoff for a single advisory engagement."
generated: { by: process:scaffolding-registry, at: 2026-08-10T15:00:00Z }
owner: service-delivery
---
Client Delivery covers a Brightwork engagement end to end, from kickoff
through handoff.

# Workflows

- [Client Status Reporting](/workflows/client-status-reporting.md)
```

## Workflow: `registry/workflows/client-status-reporting.md`

```markdown
---
type: Workflow
title: "Client Status Reporting"
description: "Drafts the weekly client status update from delivery notes and open items."
generated: { by: process:test, at: 2026-08-10T15:00:00Z }
state: in-production
execution_mode: augmented
autonomy: guided
trigger: "Friday 3pm — weekly reporting window"
stale_after: 2026-11-10
---
Every Friday afternoon, this workflow pulls the week's delivery notes and
open items into a draft status update. A consultant reviews and sends it to
the client before end of day.

# Artifacts

- [Requirements](../../framework/client-status-reporting/requirements.md)
- [Design plan](../../framework/client-status-reporting/design-plan.md)
- [Test results](../../framework/client-status-reporting/test-results.md)
- [SOP](../../sops/client-status-reporting-sop.md)

# Skills

- [drafting-status-reports](../../.claude/skills/drafting-status-reports/SKILL.md)

# Insights

<!-- GENERATED:insights -->
<!-- /GENERATED -->
```

A live workflow's node links its requirements, design plan and test results;
its build record has no link (it sits beside them, at
`framework/client-status-reporting/build-record.md`). These links are
file-relative (OKF v0.3): from the node's folder, `registry/workflows/`, `../../`
climbs to the working folder (on Claude Code and Codex the workspace), so they
read the same on every platform. Its `generated` names Test, the step that last
changed it (taking it live). No step writes `definition_type`
any more; an older node may still carry it, and the lint accepts it.

## Function: `registry/functions/service-delivery.md`

```markdown
---
type: Function
title: "Service Delivery"
description: "Owns the processes that deliver Brightwork's client engagements."
generated: { by: process:scaffolding-registry, at: 2026-08-10T15:00:00Z }
---
Service Delivery is accountable for how Brightwork engagements get run, from
kickoff to handoff.

# Owns

<!-- GENERATED:owns -->
<!-- /GENERATED -->
```

## Directory index: `registry/workflows/index.md`

Every typed directory gets one. Each entry is the page's root-relative link and,
after ` — `, its `description` (OKF v0.3 §8): the same line compose writes. Never bare same-directory links like `[Client Status Reporting](client-status-reporting.md)`,
which read from the index's own folder and which the schema forbids for a
link to another page.

```markdown
# Workflows

- [Client Status Reporting](/workflows/client-status-reporting.md) — Drafts the weekly client status update from delivery notes and open items.
```

## Note: `registry/notes/2026-08-status-report-timing.md`

```markdown
---
type: Note
title: "Status report timing shifts read-through"
description: "Clients read Friday status reports the following Monday, not the same day."
generated: { by: process:scaffolding-registry, at: 2026-08-10T15:00:00Z }
---
Clients read Friday reports Monday morning; drafting Monday-for-Monday halved
rework.

Applies to [Client Status Reporting](/workflows/client-status-reporting.md).
```
