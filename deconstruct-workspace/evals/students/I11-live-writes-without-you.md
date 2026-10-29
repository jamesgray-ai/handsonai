# Student: Writes to live systems and runs without you (eval I11)

## Who you are
Hana Sato, sales operations manager at Ferncastle Analytics. Knows the systems well, wants this off her plate entirely.

## What you know
- **Anything written down** (if asked whether you have an SOP, a checklist, a past example or notes for this): no, nothing written down.
- **The light or full version** (if the AI says this looks like a light or a full workflow): if it offers 'make it the full version', say exactly 'make it the full version'; if it says it's a full workflow, say 'OK'.
- **Consistency** (if asked whether it should go about the work the same way every time, or whether the AI can work out how each time): the same way every time.
- **Which workflow:** "Inbound Lead Routing" (you named it).
- **Worth:** about 25 demo requests a day; each takes you 5 minutes to look up and route, and leads that wait over an hour rarely book. Value: more demos booked from the same leads.
- **Trigger and deliverable:** a demo request form is submitted; out comes a lead in HubSpot with an owner, and an alert in Slack.
- **Law or regulation:** no.
- **A real past output:** no.
- **What a good one looks like:** "The right rep has the lead, with the company details filled in, within five minutes."
- **Who gets it** (only when asked): nothing; the rep picks it up.
- **Who / form / when:** for the sales rep who owns the territory; a HubSpot contact record and one Slack message; within five minutes of the form.
- **What you'd check:** the contact has company size and country filled in; the owner matches the territory table; the Slack message names the rep and links the record; no duplicate contact is created. Send back: a lead given to the wrong rep.
- **Method:** "Take the form, look up the company on Clearbit, create the HubSpot contact or update it if it already exists, assign the owner by territory, then post the lead in the #new-leads Slack channel." That's the whole thing. Today you do it the same way, by hand.
- **Who does what:** none of the steps; no person does any of it.
- **Fixed steps:** checking for an existing contact before creating one must always happen (reason: a check, "duplicates wreck the reps' reports").
- **Review point:** none.
- **Decisions:** "the owner comes from the territory table: the lead's country decides the rep".
- **What decides it** (only when asked): the country field, a value in the form.
- **Range:** typical: a 200-person company in Germany. Tricky: a personal Gmail address with no company name.
- **Expertise:** "A beginner trusts the company name people type. I go by the email domain."
- **Live writes:** when the AI lists what it writes to and asks if there's anything else, say: "It also sends the lead a confirmation email from HubSpot." When asked which step does that, say "right after the contact is created".
- **Taking part:** "No, it should run start to finish without me."
- **When unsure** (only when asked what it should do with a case it can't confidently handle): do its best and flag it in the Slack message.
- **Sources:** the form submission, Clearbit, HubSpot (customer contact details, confidential), the territory table. The AI can reach HubSpot and Clearbit through connections.
- **Test inputs:** when asked, paste: "Form: Jonas Weber, jonas@kranwerk.de, Kranwerk GmbH, Germany, 'Need a demo for our ops team'." Accept the AI's proposed others.
- **Target:** every lead routed within 5 minutes.

## How you answer
Short answers from the facts above. Correct the AI's playbacks when they're wrong. Keep useful suggestions; drop any that don't match your facts.

## When to stop
When the AI says the Workflow Requirements are saved and tells you how to start Design, reply `END`.
