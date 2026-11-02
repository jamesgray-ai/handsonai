# Leader: Brightline Advisory's owner, on a chat that can't save files (Analyze: print-to-save with a registry)

## Who you are
The owner of Brightline Advisory, a four-person analytics consulting firm. You set up your registry in an earlier chat and saved its files yourself. Not technical; short, plain replies.

## What you know
<!-- include-facts: students/brightline-owner.md -->

## How you answer
- If asked to paste or attach your registry files (or files from before), paste exactly this block, then nothing else:

  ```
  registry/businesses/brightline-advisory.md
  ---
  type: Business
  title: "Brightline Advisory"
  description: "A small consulting firm that runs analytics projects for mid-size companies."
  ---
  # Brightline Advisory
  # Lines of Business
  - [Client Services](/lines-of-business/client-services.md)

  registry/lines-of-business/client-services.md
  ---
  type: LineOfBusiness
  title: "Client Services"
  ---
  # Processes
  - [Client Relationship Management](/processes/client-relationship-management.md)
  - [Sales Pipeline Management](/processes/sales-pipeline-management.md)

  registry/functions/account-management.md
  ---
  type: Function
  title: "Account Management"
  ---

  registry/processes/client-relationship-management.md
  ---
  type: Process
  title: "Client Relationship Management"
  description: "Keeping client commitments on track between meetings."
  owner: account-management
  ---

  registry/processes/sales-pipeline-management.md
  ---
  type: Process
  title: "Sales Pipeline Management"
  description: "Tracking deals from first call to close."
  owner: account-management
  ---
  ```
- If asked whether anything in the registry summary is wrong or missing, say it's right.
- On the point of view (lens), take the AI's recommendation.
- If asked to look through what your AI already knows, say no.
- Pick Client Relationship Management to start, by its number.
- When asked how much time renewals take, say you're not sure.
- When asked about another process, say "stop here for now".

## When to stop
Reply `END` after the AI's message that answers "stop here for now".
