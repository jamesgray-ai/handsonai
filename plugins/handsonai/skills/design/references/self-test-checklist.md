# Build Skill Needs Checklist

Run this checklist against the assembled Design Spec content **before** presenting it for approval. If any item fails, fix the underlying section first. The spec's **Self-Test Summary** section must enumerate every item below, in order, marked ✓ (passed) or ⚠️ (issue — described inline). A Self-Test Summary that doesn't match this list item-for-item means the checklist wasn't actually run.

## Structure

- [ ] **Frontmatter** is present with workflow, requirements_file, spec_version (`2.2`), definition_type, mechanism, involvement, platform, platform_mode, packaging, and counts
- [ ] **Source** section names the Workflow Requirements file path (`outputs/[workflow-name]/requirements.md`)
- [ ] `Architecture Decisions` table has Lens, Platform, Platform Mode, Orchestration, Involvement, Packaging, and Trigger rows
- [ ] Every step in the decomposition table has separate Orchestration, Integration, Intelligence, and Build Output columns
- [ ] Step IDs in the decomposition table match the Step IDs in the Workflow Requirements (Step 1, Step 2, …)
- [ ] Every step uses canonical autonomy terms: Human / Deterministic / Guided / Autonomous
- [ ] Every Integration column entry includes the block type, tool name, and use/build tag
- [ ] Every Build Output value is one of the canonical forms (`New skill: SN`, `Use existing: [name]`, `New agent: AN`, `Inline prompt → Workflow Requirements Step N`, `Handled by orchestrator` [legacy synonym `Handled by agent` accepted], `MCP server: [name]`, `Human (no artifact)`)
- [ ] Packaging value is one of the canonical forms (`Plugin`, `Standalone Skill`, `Workspace Agent`, `Loose Files`)

## Skill Candidates

- [ ] Every `New skill: SN` reference has a matching Skill Candidates entry with the SN ID
- [ ] Every Skill Candidate has all 12 fields: ID, Name, Description, Purpose, Covers Steps, Inputs, Outputs, Decision Logic, Failure Modes, Required Tools, Depends On, Stateful?
- [ ] Every Skill Candidate's Name conforms to format rules (lowercase-hyphen, ≤64 chars, no consecutive hyphens)
- [ ] Every Skill Candidate's Description starts with "This skill should be used when..." and is ≤1024 chars

## Agent Configuration

- [ ] Every `New agent: AN` reference has a matching Agent Configuration entry with the AN ID
- [ ] Every Agent Configuration has all 13 fields: ID, Name, Description, Mission, Responsibilities, Output Format, Tone & Style, Constraints, Model, Memory Scope, Tools, Skills, Trigger Examples
- [ ] Every Agent Configuration's Description starts with "Use this agent when..." and is ≤1024 chars
- [ ] If more than one agent is defined, Multi-Agent Configuration section is present with Orchestration Pattern, Coordinator, Handoff Contracts, and Aggregation Strategy

## Cross-references

- [ ] Every tool in the Integration column has a matching entry in Integration Options with at least one Source URL
- [ ] Every skill `Depends On` reference points to a defined skill ID

## Mechanism-specific

- [ ] Orchestrator Prompt Outline section is present when mechanism is `Prompt` or `Skill-Powered Prompt` (omitted when mechanism is `Agent`)
- [ ] Agent Configuration present when mechanism is `Agent` (or `agents: 0` is set and orchestration logic is documented in the Deployment Plan)

## Safety

- [ ] Safety & Permissions section is present in Layer 1 — all four questions answered (write access, untrusted input, unattended runs, blast radius) with mitigations, or the explicit "Read-only, human-triggered, trusted inputs" statement
- [ ] If the workflow consumes untrusted input AND has write access, at least one mitigation is a Human Gate or draft-don't-send constraint — not just "be careful"

## Completeness

- [ ] Model Recommendation section is present with a default capability and per-platform mapping
- [ ] Data Readiness Summary is present (even if "all accessible") — references Context IDs from the Workflow Requirements
- [ ] Deployment Plan is present with target location and deployment steps for each artifact, plus a Packaging note
- [ ] Evaluation Inputs section is present, pointing to the Workflow Requirements file (do not duplicate Acceptance Criteria or Example Scenarios)
- [ ] Deferred to Build section lists what Build will resolve at generation time
- [ ] Self-Test Summary section is present at the end of the spec, enumerating every item in this checklist with ✓ or ⚠️

## Outcome-driven modifications

For `Definition Type: Outcome-Driven`, apply these substitutions; all other items apply unchanged:

- Replace "Step-by-Step Decomposition" with "Capability Domain Mapping"
- Replace "Step IDs match Workflow Requirements Step IDs" with "Capability Domains are derived from Workflow Requirements (not restated from a section that doesn't exist there)"
- Replace "Inline prompt → Workflow Requirements Step N" Build Output value with "Handled by orchestrator" (accept legacy "Handled by agent" as a synonym)
- Agent Configuration is included whenever ≥1 sub-agent is defined; a zero-sub-agent design (orchestration logic + skills only) is valid with `agents: 0`. Never document the primary-loop orchestrator as an agent.
