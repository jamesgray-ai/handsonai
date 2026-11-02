# Client Follow-Up — Workflow Definition

## Goal

For each client call, a plain-text follow-up email draft to the client, ready for you to review and send the same day.

## Metadata

| Field | Value |
|---|---|
| Workflow Name | Client Follow-Up |
| Definition Type | Step-Driven |
| Description | Drafts a follow-up email after each client call from your call notes, for you to review and send. |
| Trigger | You finish a client call and paste in your notes |
| Owner | Account lead |

## Steps Overview

1. Read the call notes
2. Draft the email
3. Review and send

## Acceptance Criteria

- The draft lists every next step named in the notes, each with its owner.
- The draft states no figure, date or commitment that isn't in the notes.

## Rules & Constraints

- M1: Must never send an email.
- RF1: Must flag anything it isn't sure of.

## Human Gates

- Before sending: you review the draft.
