# Skill Specification — agentskills.io Format

When generating skills, follow this format. Skills are directories containing a `SKILL.md` file with YAML frontmatter and a markdown body. The full specification is at [agentskills.io/specification](https://agentskills.io/specification).

## File Structure

```
skill-name/
├── SKILL.md          # Required — skill definition
├── references/       # Optional — additional documentation agents read on demand
│   └── *.md
├── scripts/          # Optional — executable code agents can run
│   └── *.py, *.sh, *.js
└── assets/           # Optional — static resources (templates, images, data files)
    └── *
```

## YAML Frontmatter (Required)

```yaml
---
name: skill-name          # Required. Lowercase, hyphens only, max 64 chars. Must match directory name.
description: >            # Required. Max 1024 chars. What the skill does and when to use it.
  This skill should be used when the user wants to [trigger description].
  [What the skill does]. [What it produces].
license: MIT              # Optional. License name or reference to a bundled license file.
compatibility: >          # Optional. Max 500 chars. Environment requirements (free text).
  Designed for Claude Code (or similar products)
metadata:                 # Optional. Arbitrary key-value pairs.
  author: example-org
  version: "1.0.0"
allowed-tools: Bash(git:*) Read Write  # Optional (experimental). Space-delimited pre-approved tools.
---
```

### Field Rules

| Field | Required | Rules |
|-------|----------|-------|
| `name` | Yes | Lowercase letters, numbers, and hyphens only. Max 64 chars. Must not start or end with a hyphen. No consecutive hyphens (`--`). Must match directory name. |
| `description` | Yes | Max 1024 chars. Describe what the skill does and when to use it. Start with "This skill should be used when..." for discoverability. Include keywords that help agents identify relevant tasks. |
| `license` | No | License name or reference to a bundled license file. |
| `compatibility` | No | Max 500 chars. Free-text string describing environment requirements — intended product, required system packages, network access, etc. Most skills don't need this. |
| `metadata` | No | Arbitrary key-value mapping (string keys → string values). Use for author, version, or custom properties. |
| `allowed-tools` | No | Space-delimited list of pre-approved tools. Experimental — support varies between agent implementations. |

### Claude Code Extensions

These fields are recognized by Claude Code but are **not part of the agentskills.io standard**. Include them when generating skills specifically for Claude Code. The authoritative reference is the [Claude Code skills documentation](https://code.claude.com/docs/en/skills).

#### Frontmatter Fields

| Field | Description |
|-------|-------------|
| `argument-hint` | Hint shown during autocomplete to indicate expected arguments. Example: `[issue-number]` or `[filename] [format]`. |
| `disable-model-invocation` | Set to `true` to prevent Claude from automatically loading this skill. Use for workflows that should only be triggered manually with `/name`. Default: `false`. |
| `user-invocable` | Set to `false` to hide from the `/` menu. Use for background knowledge users shouldn't invoke directly. Default: `true`. |
| `model` | Model to use when this skill is active. |
| `context` | Set to `fork` to run in a forked subagent context. |
| `agent` | Which subagent type to use when `context: fork` is set. Options include built-in agents (`Explore`, `Plan`, `general-purpose`) or custom subagents from `.claude/agents/`. |
| `hooks` | Hooks scoped to this skill's lifecycle. |

**Invocation control summary:**

| Frontmatter | User can invoke | Claude can invoke | When loaded into context |
|-------------|-----------------|-------------------|------------------------|
| (default) | Yes | Yes | Description always in context; full skill loads when invoked |
| `disable-model-invocation: true` | Yes | No | Description not in context; full skill loads when user invokes |
| `user-invocable: false` | No | Yes | Description always in context; full skill loads when invoked |

#### String Substitutions

Skills support dynamic value substitution in the markdown body:

| Variable | Description |
|----------|-------------|
| `$ARGUMENTS` | All arguments passed when invoking the skill. If `$ARGUMENTS` is not present in the content, arguments are appended as `ARGUMENTS: <value>`. |
| `$ARGUMENTS[N]` | Access a specific argument by 0-based index (e.g., `$ARGUMENTS[0]`). |
| `$N` | Shorthand for `$ARGUMENTS[N]` (e.g., `$0`, `$1`). |
| `${CLAUDE_SESSION_ID}` | The current session ID. |
| `${CLAUDE_SKILL_DIR}` | The directory containing the skill's `SKILL.md` file. |

#### Dynamic Context Injection

The `` !`command` `` syntax runs shell commands before the skill content is sent to Claude. The command output replaces the placeholder. Example:

```yaml
---
name: pr-summary
description: Summarize changes in a pull request
context: fork
agent: Explore
---

## Pull request context
- PR diff: !`gh pr diff`
- Changed files: !`gh pr diff --name-only`
```

#### Example with Claude Code Extensions

```yaml
---
name: deploy
description: Deploy the application to production
disable-model-invocation: true
argument-hint: "[environment]"
allowed-tools: Bash(npm run *)
---

Deploy $ARGUMENTS to production:
1. Run the test suite
2. Build the application
3. Push to the deployment target
```

## Markdown Body

The body follows the frontmatter and defines the skill's behavior. There are no format restrictions in the spec — write whatever helps agents perform the task effectively. Keep the main `SKILL.md` under 500 lines; move detailed reference material to separate files in `references/`.

### Recommended Structure

```markdown
# Skill Title

One-line description of what the skill does.

## Workflow

Step-by-step instructions the model follows when executing the skill.
Number each step. Be explicit about inputs, decisions, and outputs.

## Outputs

### `outputs/filename.md` — Description

List every file the skill produces, with the path template and contents.

## Guidelines

- Behavioral rules and constraints
- Tone and style guidance
- Edge case handling
```

### Writing Guidelines

- **Workflow steps are instructions to the model**, not documentation for the user. Write them as directives: "Read the file", "Present a table", "Ask the user to confirm".
- **Be specific about file paths** — use `outputs/[workflow-name]-artifact.md` templates.
- **Separate concerns** — Design decisions go in the Workflow. Output format goes in Outputs. Behavioral rules go in Guidelines.
- **No platform-specific content in the skill body** — the skill defines *what* to do. The model provides *how* based on the user's platform.

## Progressive Disclosure

Skills should be structured for efficient context use:

1. **Metadata** (~100 tokens): `name` and `description` are loaded at startup for all skills
2. **Instructions** (< 5000 tokens recommended): The full `SKILL.md` body is loaded when the skill is activated
3. **Resources** (as needed): Files in `scripts/`, `references/`, and `assets/` are loaded only when required

## Example

```yaml
---
name: writing-status-reports
description: >
  This skill should be used when the user wants to generate a weekly status
  report from project data. Collects updates from configured sources, synthesizes
  key themes, and produces a formatted status report.
user-invocable: true
---
```

```markdown
# Writing Status Reports

Generate a weekly status report from project data sources.

## Workflow

1. **Identify sources** — Ask the user which project tracking tools they use (Jira, Linear, GitHub, etc.).
2. **Collect updates** — Read the last 7 days of activity from each source.
3. **Synthesize themes** — Group updates into categories: Completed, In Progress, Blocked, Upcoming.
4. **Draft report** — Write the status report using the format in Outputs.
5. **Review** — Present the draft and ask the user to confirm or adjust.

## Outputs

### `outputs/status-report-YYYY-MM-DD.md` — Weekly Status Report

Includes: date range, category sections, key metrics, blockers, next week priorities.

## Guidelines

- Use plain language; avoid jargon
- Keep each bullet to one sentence
- Flag blockers prominently
```
