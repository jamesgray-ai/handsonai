---
title: AI Governance Policy
owner: Managing director
last_reviewed: 2026-08-05
---

# AI Governance Policy

This policy sets the rules every AI workflow, skill and agent the company runs must meet, and names the check that confirms each one. It covers all of them, whether they run with a person or on their own. The managing director owns it, approves every change to its rules, and reviews it each quarter and after any incident. It maps to the NIST AI Risk Management Framework: G1 to Govern 1.6 (an inventory of AI systems), G3 to Manage 4.1 (monitoring after deployment), and G10 to Govern 1.5 (periodic review of the risk process).

## Rules

| ID | Rule | Checked by | Since |
|---|---|---|---|
| G1 | Every AI workflow is in our AI Registry, with a name, a description, and a process owned by a team. | Weekly registry look: not started yet, from the managing director's first Monday look | 2026-08-05 |
| G2 | Every AI workflow can use only the tools and connections its work needs. | Access review: not started yet, from the managing director's first monthly access review | 2026-08-05 |
| G3 | Every workflow passes its tests before it goes live, and is re-checked by its re-check date. | Test results: in each workflow's folder; Weekly registry look: re-check dates passed, from the managing director's first Monday look | 2026-08-05 |
| G4 | Every live workflow the team relies on has an SOP. | Weekly registry look: live workflows with no SOP, from the managing director's first Monday look | 2026-08-05 |
| G5 | Every live workflow's SOP says when it runs, where its outputs go, and who is told when it fails. | Weekly registry look: live workflows whose SOP is missing these, from the managing director's first Monday look | 2026-08-05 |
| G6 | Every change to a skill, agent or workflow is reviewed by a second person before it's used for real. | Change review: not started yet, from the managing director naming a second reviewer | 2026-08-05 |
| G7 | Anything a workflow sends to a client, or changes in a system other people use, waits for a person's approval unless the managing director has approved otherwise in writing. | Test results: the approval step was checked; Change review: the approval step is still there after each change, from the managing director naming a second reviewer | 2026-08-05 |
| G8 | No AI workflow reads client contracts or staff salaries. | Access review: no build record lists access to them, from the managing director's first monthly access review | 2026-08-05 |
| G9 | Every live skill and agent has its own tests, updated whenever it changes. | Change review: tests updated with the change, from the first change review that adds them | 2026-08-05 |
| G10 | This policy is reviewed each quarter and after any incident. | Quarterly policy review | 2026-08-05 |
| G11 | Every workflow that runs without a person runs only reviewed instructions, and its schedule or what starts it is recorded in its registry entry. | Weekly registry look: workflows that run on a schedule or when something arrives, from the managing director's first Monday look | 2026-08-05 |

## Checks

| Check | Where it runs | Covers |
|---|---|---|
| Weekly registry look | The managing director opens the registry and its dashboard (REGISTRY.md) each Monday (planned) | G1, G3, G4, G5, G11 |
| Access review | Monthly, the managing director reads each live workflow's build record of what it can access (planned) | G2, G8 |
| Test results | test-results.md in each workflow's folder under framework/, before it goes live | G3, G7 |
| Change review | A second person reads each change to a skill, agent or workflow before it's used for real (planned) | G6, G7, G9 |
| Quarterly policy review | Each quarter, and after any incident, the managing director says "review our AI governance policy" | G10 |

## Retired rules

| ID | Rule | Checked by | Since | Retired |
|---|---|---|---|---|
