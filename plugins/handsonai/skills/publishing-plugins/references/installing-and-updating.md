# Installing and Updating the Plugin

Checked against Anthropic's docs on 2026-11-02:
[Plugins in Claude](https://claude.com/docs/plugins/overview),
[Install and manage plugins](https://code.claude.com/docs/en/plugins/install.md),
[Host and maintain a marketplace](https://code.claude.com/docs/en/plugins/host-marketplace.md).
Recheck before relying on menu names.

The plugin repository is a **marketplace**: a GitHub repository Claude can install plugins from. It
can hold several plugins. In Claude Code a plugin is named `<plugin>@<marketplace>`, where the
marketplace name is the `name` at the top of `.claude-plugin/marketplace.json`.

**Why the version number matters:** Claude decides an update is available from the `version` in the
plugin's descriptor files. If files change but the number doesn't, people who installed it keep the
old copy. This is why every release gets a new number.

Give only the steps for where the user works.

## Claude (web, desktop app, Cowork)

**First release: add and install.**
1. Go to Customize › Plugins (claude.ai/customize/plugins), then Add › Add marketplace.
2. Enter `<owner>/<plugin-repo>` (or the repository's github.com address).
3. For a private repository, the dialog asks you to connect GitHub and give the Claude GitHub App
   access to that repository. Do it there; it's separate from the GitHub connector.
4. Install the plugin for your team from the marketplace and try one of its skills.

**Later releases.** Updates arrive on their own. To get one now, choose Check for updates. Turning
on Sync automatically for the marketplace keeps it current.

**Teammates** do the same steps. For a private repository, each one needs access to it on GitHub.
On a Team or Enterprise plan, an Owner can instead add the marketplace for everyone under
Organization settings › Plugins & skills, and may need to allow members to add their own.

## Claude Code

**First release: add and install.** In a session:
```
/plugin marketplace add <owner>/<plugin-repo>
/plugin install <plugin>@<marketplace>
```
For a private repository, Git on this computer must already be signed in to GitHub
(`gh auth login`, then `gh auth setup-git`).

**Later releases.** `/plugin` › Marketplaces › select it › Update marketplace, which also updates its
plugins. Then `/reload-plugins` (or start a new session). To stop doing this by hand: `/plugin` ›
Marketplaces › select it › Enable auto-update.
