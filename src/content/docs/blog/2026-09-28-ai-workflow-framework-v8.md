---
date: 2026-09-28
authors:
  - jamesgray
tags:
  - Framework
  - Plugins
  - New Content
description: "Framework v8: every skill rewritten for clarity — a yes/no report card for testing, Skill or Agent, a draft-then-approve Design Spec, a Run Card, and a glossary."
title: "AI Workflow Framework v8: clearer steps, a report card, and one plugin release"
---

The Hands-on AI plugin is now at 8.0.0, and every one of the seven framework skills was rewritten for the person running it: each opens with an agenda and a time, signposts its phases as it goes, and closes by naming the next step and how long it takes. Plan about a working day, over three or four sessions, to take one workflow from Analyze to Run. The [Framework Glossary](/ai-workflow-framework/glossary/) defines every term in plain language.

<!-- more -->

**Testing is a report card, not a score.** [Deconstruct](/ai-workflow-framework/deconstruct/) now asks for a real recent good output and turns it into numbered yes/no acceptance criteria, rules, and human gates. [Test](/ai-workflow-framework/test/) runs the workflow in a fresh conversation and grades each line Met or Not met, with evidence; Ready means every line met. [Improve](/ai-workflow-framework/improve/) names the lines that flipped since the baseline and ends with one of three calls: leave it, tune it, or redesign.

**Two mechanisms.** A workflow runs as a Skill or an Agent. [Design](/ai-workflow-framework/design/) asks the question in plain terms, reuses the skills you already have before proposing new ones, and writes the Design Spec as a draft you read and approve; [Build](/ai-workflow-framework/build/) refuses an unapproved spec. See the [AI Workflow Design Matrix](/ai-workflow-framework/workflow-design-matrix/).

**Registry first.** [Set up your AI Registry](/builder-setup/ai-registry-setup/) before you start; [Analyze](/ai-workflow-framework/analyze/) registers its candidate workflows there as backlog nodes, so every later step knows what is next.

**Build builds by intent.** Build starts by preparing context (connect it, provide it, or build it in), then states what it wants built and lets your platform's own model create the skill or agent its own way. It ends with a reconciliation table of every artifact, and a fix mode that rebuilds only what Test named. Platform-specific facts now live in the plugin's platform registry, so the skills read the same on Claude, ChatGPT, Gemini, and Copilot.

**A Run Card.** [Run](/ai-workflow-framework/run/) leaves a six-section Run Card for your first real run, offers scheduling only when the workflow is automated, and sets the review date Improve comes back to.

Install or update from the [plugin marketplace](/use-the-playbook/build/), or download the [skill ZIPs](/ai-workflow-framework/skills/) for platforms without plugins. The Design Spec format changed (version 3.0), which is why this is a major release; older specs are still read.
