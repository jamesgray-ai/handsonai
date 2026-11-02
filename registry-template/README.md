# AI Registry Template

A starter [OKF](https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md)
knowledge bundle for your AI Registry — the structured record of your business's
lines of business, processes, workflows, and insights that AI assistants read
and maintain.

**What this is:** an optional starting point. Your AI assistant can set up a
registry in any folder without this repository. Use it if you want your
registry on GitHub — or just grab the empty skeleton with **Code → Download ZIP**
(no account needed).

**Get started on GitHub:**
1. Click **Use this template** (top right) to create your own copy. Choose
   **Private** — only you can see it.
2. Set up your registry in it: open a copy of the repository with your AI
   assistant and say **"Set up my AI registry."** Your assistant runs the
   interview and writes every node and dashboard. (In a browser-only tool such
   as Claude on the web or ChatGPT, you don't need this repository: the
   assistant writes your registry into `registry/` in your working folder,
   `ai-workspace/` in your Google Drive or OneDrive, through its connection. Only where it can't save files at
   all does it give you each file to save yourself.)
3. The full guide lives on the Hands-on AI Playbook:
   https://handsonai.info/builder-setup/ai-registry-setup/

The `tools/` folder and GitHub Action check your registry against
`registry/SCHEMA.md` whenever you save a registry file: the **Actions** tab
shows a green ✓ when every file follows the rules, or a red ✗ — click it to
see which file to fix. While you're still saving your first set of files, a
red ✗ is normal. Nothing is published. You never run these scripts yourself.

Everything in `registry/` except `SCHEMA.md`, `index.md`, and `log.md` starts
empty: your AI assistant fills it with YOUR business through an interview.
