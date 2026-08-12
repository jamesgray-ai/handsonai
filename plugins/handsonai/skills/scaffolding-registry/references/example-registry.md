# Example Registry — Brightwork Consulting (FICTIONAL)

Worked examples for the scaffolding interview. **Never copy these nodes into
the user's registry** — show them as the shape to imitate, then write the
user's real business instead. The finished registry must contain no
Brightwork residue.

## Business: `registry/businesses/brightwork-consulting.md`

```markdown
---
type: Business
title: "Brightwork Consulting"
description: "Boutique operations consultancy helping mid-market firms modernize their back office."
generated: { by: process:scaffolding-registry, at: 2026-08-10 }
status: active
url: https://example.com
---
Brightwork Consulting is a small operations consultancy that helps mid-market
firms modernize back-office work.

# Lines of Business

1. [Advisory](/lines-of-business/advisory.md)
2. [Training](/lines-of-business/training.md)
```

## LineOfBusiness: `registry/lines-of-business/advisory.md`

```markdown
---
type: LineOfBusiness
title: "Advisory"
description: "Hands-on engagements that redesign a client's back-office operations."
generated: { by: process:scaffolding-registry, at: 2026-08-10 }
status: active
---
Advisory pairs a Brightwork consultant with a client team for a fixed-scope
engagement.

# Processes

1. [Client Delivery](/processes/client-delivery.md)
```

## LineOfBusiness: `registry/lines-of-business/training.md`

```markdown
---
type: LineOfBusiness
title: "Training"
description: "Workshops and cohort programs that teach clients to run their own operations improvements."
generated: { by: process:scaffolding-registry, at: 2026-08-10 }
status: active
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
generated: { by: process:scaffolding-registry, at: 2026-08-10 }
owner: service-delivery
---
Client Delivery covers a Brightwork engagement end to end, from kickoff
through handoff.

# Workflows

1. [Client Status Reporting](/workflows/client-status-reporting.md)
```

## Workflow: `registry/workflows/client-status-reporting.md`

```markdown
---
type: Workflow
title: "Client Status Reporting"
description: "Drafts the weekly client status update from delivery notes and open items."
generated: { by: process:scaffolding-registry, at: 2026-08-10 }
status: in-production
definition_type: step-driven
execution_mode: augmented
autonomy: guided
trigger: "Friday 3pm — weekly reporting window"
stale_after: 2026-11-01
---
Every Friday afternoon, this workflow pulls the week's delivery notes and
open items into a draft status update. A consultant reviews and sends it to
the client before end of day.

# Artifacts

- **Requirements:** [requirements.md](outputs/client-status-reporting/requirements.md)
- **SOP:** [client-status-reporting-sop.md](sops/client-status-reporting-sop.md)

# Skills

- [drafting-status-reports](.claude/skills/drafting-status-reports/SKILL.md)

# Insights

<!-- GENERATED:insights -->
<!-- /GENERATED -->
```

## Function: `registry/functions/service-delivery.md`

```markdown
---
type: Function
title: "Service Delivery"
description: "Owns the processes that deliver Brightwork's client engagements."
generated: { by: process:scaffolding-registry, at: 2026-08-10 }
---
Service Delivery is accountable for how Brightwork engagements get run, from
kickoff to handoff.

# Owns

<!-- GENERATED:owns -->
<!-- /GENERATED -->
```

## Directory index: `registry/workflows/index.md`

Every typed directory gets one. Entries are bundle-root-relative leading-slash
links — never bare same-directory links like `[Client Status Reporting](client-status-reporting.md)`,
which the schema's link discriminator resolves repo-root-relative and lint
flags as broken.

```markdown
# Workflows

- [Client Status Reporting](/workflows/client-status-reporting.md)
```

## Note: `registry/notes/2026-08-status-report-timing.md`

```markdown
---
type: Note
title: "Status report timing shifts read-through"
description: "Clients read Friday status reports the following Monday, not the same day."
generated: { by: process:scaffolding-registry, at: 2026-08-10 }
---
Clients read Friday reports Monday morning; drafting Monday-for-Monday halved
rework.

Applies to [Client Status Reporting](/workflows/client-status-reporting.md).
```
