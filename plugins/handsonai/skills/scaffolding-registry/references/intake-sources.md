# Intake Sources

What a student may already have that describes their business, and what each
one lets you draft before the interview asks. **Drafted is not confirmed:**
nothing from a source is written until the student confirms it in the phase
that owns it. Functions are named for the area or role, never the person; a
person's name goes in a `lead:` field only when the student asks. A verbal
answer in Phase 0 that covers a later phase is a source too.

## Where sources come from

- **Workspace scan (write mode only).** `knowledge/` (read only — never write
  or lint it here), `sops/`, `process-guides/`, `CLAUDE.md` or `AGENTS.md`,
  `outputs/ai-opportunity-report*.md`. A `knowledge/` graph's type names are
  whatever its owner chose: read its `overview.md` and `index.md` first and
  treat each page as a pasted document — evidence to draft from, mapped by
  what it says, not by its folder name.
- **Pasted or uploaded (both modes).** Anything the student pastes or
  attaches in reply to the Phase 0 question.

## Mapping

| Source | Drafts | The student still decides |
|---|---|---|
| Services page, offerings list, capabilities deck, product list, `knowledge/` pages about offerings | Lines of Business; the Business identity sentence | Order of importance; which are dormant or incubating; whether to collapse to one default line |
| Org chart, team list, job descriptions | Functions **named for the area or role** ("Client Delivery"), never the person; `lead:` only on request | Trim to how work is actually owned; which are unstaffed |
| Personal life: a list of life areas, a shared calendar, a budget spreadsheet, a chores list | Lines of Business (the areas); Processes (the recurring routines); Functions as roles ("Me", "Partner") | Order of the areas; who owns each routine |
| Process inventory, SOP folder, process guides, `knowledge/` pages about processes | Processes with `owner:`; `guide:` links to existing SOPs or guides | Which three to five deliver each LOB; confirm each owner |
| Strategy page, OKRs, annual plan, prior opportunity report | Two or three objectives as prose for the Business node's `## Objectives` | Which matter this year |
| Team charter, mission statement | Business identity sentence (professional persona: the team is the Business) | Wording |
| `CLAUDE.md` / `AGENTS.md` | Business identity; folder conventions | Confirm nothing stale |

## How to present a draft

One phase at a time, in that phase's slot: "From your [source], here's what
I'd write: … Anything wrong or missing?" Show the draft as the node body it
would become, not as a summary. If the source contradicts something the
student said, ask which is current; never silently prefer the document.

## Privacy

Say once in Phase 0: role titles by default, names only on request. If the
registry may live on public GitHub Pages, remind the student before writing
any name.
