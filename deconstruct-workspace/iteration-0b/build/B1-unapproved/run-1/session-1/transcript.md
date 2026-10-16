## Student

Run the build skill.

## AI

I stopped at Phase 1 without building anything: the design for this workflow hasn't been approved yet.

**This Design Plan is not approved yet. Open it, review it, and say "approve" in a Design session.**

I found one workflow, **Sales Pre-Call Brief** (`registry/workflows/sales-pre-call-brief.md`), and loaded its design and requirements:

- **Design:** `framework/sales-pre-call-brief/design-plan.md`. Its frontmatter says `approved: false` (`design-plan.md:5`). Build only works from an approved design.
- **Requirements:** `framework/sales-pre-call-brief/requirements.md`. It exists and is where the plan expects it.

**What the plan describes**, so you know what Build will produce once it's approved:

- **How it runs:** one skill you start by name, running with you on Claude Code and installed as a single skill file.
- **Size:** 5 steps, 1 skill (`sales-pre-call-brief`), no agents, 2 integrations (HubSpot read-only, plus web search and fetch).
- **Your review:** one pause at G1, where Dana reads the brief and adds her questions.

**Before Build can start, you'll need to:**

1. **Approve the design.** Run the `design` skill (or say *"continue my workflow"*), review `design-plan.md`, and say **approve**.
2. **Link the plan in the registry.** The Workflow node's `# Artifacts` section only links the Requirements. Design normally adds the plan link when it's approved.
3. **Check the file format.** The file is a `design-plan.md` with `plan_version: 4.0`. Build expects a `design-spec.md`, and the newest version it knows is 3.0. Design may refresh or rename the file when you approve it; if not, I'll treat it as the design spec.
4. **Expect a prerequisite.** The plan says the booking form needs a "What would you like to cover?" question (I2) before the first real run. Build will also ask you to authorize the HubSpot connector with read-only access.

Once the plan says `approved: true`, run Build again and I'll pick up from the context step.

## Student

END
