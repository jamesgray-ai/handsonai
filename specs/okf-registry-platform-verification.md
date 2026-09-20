# OKF Registry Platform Verification Checklist

Platform verification matrix for the OKF Registry redesign — see specs/okf-registry-redesign-prd.md Part 8 for implementation requirements.

No platform appears as an unqualified path in the setup page until its row is signed. Re-verify before each course run and after any MAJOR plugin release.

| Platform | Skill loads | Interview completes | Node written via platform write path | Cloud-drive write (assistant creates .md in Drive/OneDrive) | Print-and-save Close prints REGISTRY.md | Dashboard viewable | Verified by / date / platform version |
|----------|-------------|---------------------|-------------------------------------|---------------------|---------------------|--------------------|---------------------------------------|
| Claude Code | ☑ verified | ☑ verified | ☑ verified | n/a — local folder | n/a | ☑ verified | James Gray (authorized Claude Fable 5 behavioral run: scaffold interview, node writes, lint/compose, REGISTRY.md + HTML dashboard) / 2026-08-11 / Claude Code CLI 2.x, plugin v7.0.0 |
| Cowork | ☐ unverified | ☐ unverified | ☐ unverified | ☐ unverified | n/a | ☐ unverified | ☐ unverified |
| ChatGPT desktop (Codex) | ☐ unverified | ☐ unverified | ☐ unverified | ☐ unverified | n/a | ☐ unverified | ☐ unverified |
| claude.ai | ☐ unverified | ☐ unverified | ☐ unverified | ☐ unverified | ☐ unverified | ☐ unverified | ☐ unverified |
| ChatGPT web | ☐ unverified | ☐ unverified | ☐ unverified | ☐ unverified | ☐ unverified | ☐ unverified | ☐ unverified |
| M365 Copilot | ☐ unverified | ☐ unverified | ☐ unverified | ☐ unverified | ☐ unverified | ☐ unverified | ☐ unverified |

Columns added 2026-09-20 (ADR 004). Until a cloud-drive row is signed, the setup page says only "if your tool can create files in your drive" — it never names which tools can. Tests: (1) fresh chat, skill loaded, "Set up my AI registry in my Google Drive folder called `ai-registry`" — pass = `registry/SCHEMA.md` exists in Drive as plain `.md` (not a Doc) and a second chat reads it back; (2) browser tool, print-and-save interview with "I already have the empty registry skeleton" — pass = no skeleton reprinted, and Phase 6 prints `log.md`, the typed `index.md` updates, and `REGISTRY.md`. Gemini has no row yet; add one before the next course run.
