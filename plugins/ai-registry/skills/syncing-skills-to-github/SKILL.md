---
name: syncing-skills-to-github
description: Sync Claude Agent Skills from ~/.claude/skills/ (local) to GitHub repository using git commands. Skills are stored in a flat directory structure. Commits changes, pushes to remote, and updates Notion AI Building Blocks with GitHub URLs. Designed for Claude Code with access to terminal and git credentials.
---

# Syncing Skills to GitHub

**⚡ This skill runs in Claude Code with access to your terminal and git credentials.**

## Purpose
Sync Claude Agent Skills from `~/.claude/skills/` (local machine) to GitHub repository `jamesgray007/agent-skills` with detailed commit history and automated Notion tracking. Skills are stored in a flat directory structure. Part 2 of the two-skill export→sync workflow.

## When to Use
Trigger this skill after:
- Exporting skills from cloud to local (using `exporting-skills-from-claude`)
- Creating/updating skills locally
- Weekly batch sync of multiple skills
- Any changes to skills in `~/.claude/skills/`

## How It Works
1. **Detect** changes in `~/.claude/skills/` using git status
2. **Review** what changed (new files, modifications, deletions)
3. **Identify** affected skill directories
4. **Generate** semantic commit messages based on changes
5. **Commit** to local git repository
6. **Push** to GitHub remote
7. **Update** Notion AI Building Blocks database with GitHub URLs
8. **Report** summary of sync operation

## Prerequisites

### Environment
- **Claude Code** running in terminal (has access to git credentials)
- Git installed and configured with GitHub authentication
- Repository `~/.claude/skills/` is a git repository
- Remote: `git@github.com:jamesgray007/agent-skills.git` or `https://github.com/jamesgray007/agent-skills.git`

### Notion
- AI Building Blocks database ID: `2d5edcfd-b924-80cf-a0a0-000ba0164e40`
- Notion API access configured

### Directory Structure
```
~/.claude/skills/
├── .git/                          # Git repository
├── README.md                      # Auto-generated skill index
├── generate-readme.sh             # Script to regenerate README
├── aggregating-post-performance/
├── analyzing-hubspot-deals/
├── creating-lesson-content/
├── designing-course-syllabus/
├── exporting-skills-from-claude/
├── syncing-skills-to-github/
├── writing-launch-email-sequence/
├── writing-linkedin-posts/
├── writing-substack-posts/
└── [other skills...]
```

## Implementation

### Step 1: Verify Git Repository

```bash
cd ~/.claude/skills

# Check if this is a git repo
if [ ! -d .git ]; then
    echo "❌ Not a git repository. Initialize first:"
    echo "  cd ~/.claude/skills"
    echo "  git init"
    echo "  git remote add origin git@github.com:jamesgray007/agent-skills.git"
    exit 1
fi

# Check remote
git remote -v
```

### Step 2: Detect Changes

```bash
cd ~/.claude/skills

# Get status
git status --porcelain

# Parse output:
# M  = Modified file
# A  = Added file (staged)
# D  = Deleted file
# ?? = Untracked file
# R  = Renamed file

# Examples:
# ?? exporting-skills-from-claude/SKILL.md   → New skill
# M  writing-linkedin-posts/SKILL.md         → Updated skill
# D  old-skill/SKILL.md                      → Deleted skill
```

### Step 3: Identify Affected Skills

```bash
# Parse git status to identify which skill directories changed
# Extract skill-name from file paths

# Example logic:
git status --porcelain | \
  grep -E "SKILL.md|references/" | \
  sed 's|^...||' | \
  cut -d'/' -f1 | \
  sort -u

# Output: List of skill-name paths with changes
# e.g., writing-linkedin-posts, syncing-skills-to-github
```

### Step 4: Generate Commit Message

**Single Skill:**
```
[CREATE|UPDATE|FIX] skill-name: Brief description

- What changed specifically
- Why this change was made
- Impact or benefit
```

**Multiple Skills:**
```
[SYNC] Updated N skills

New skills:
- skill-a: Description
- skill-b: Description

Updated skills:
- skill-c: What changed
- skill-d: What changed

Deleted skills:
- skill-e: Reason for removal
```

**Semantic Prefixes:**
- `[CREATE]` - New skill added
- `[UPDATE]` - Existing skill modified
- `[FIX]` - Bug fix or correction
- `[REFACTOR]` - Code improvement, no functionality change
- `[DOCS]` - Documentation updates only
- `[SYNC]` - Batch commit of multiple changes
- `[RETIRE]` - Skill archived/deprecated

### Step 5: Stage and Commit

```bash
cd ~/.claude/skills

# Stage all changes
git add .

# Or stage specific skill
git add skill-name/

# Commit with generated message
git commit -m "$COMMIT_MESSAGE"

# Verify commit
git log -1 --oneline
```

### Step 6: Push to GitHub

```bash
cd ~/.claude/skills

# Push to main branch
git push origin main

# If push fails (e.g., branch diverged), handle appropriately
# Option 1: Pull and merge
git pull --rebase origin main
git push origin main

# Option 2: Force push (use with caution)
# git push --force origin main
```

### Step 7: Update Notion AI Building Blocks

For each skill that was synced, update the GitHub URL in Notion.

**Instructions for Claude Code:**

For each changed skill directory (e.g., "exporting-skills-from-claude"):

1. **Search for the skill in Notion AI Building Blocks:**
   - Use tool: `Notion:notion-search`
   - Parameters:
     - `query`: The skill directory name (e.g., "exporting-skills-from-claude")
     - `data_source_url`: "collection://2d5edcfd-b924-80cf-a0a0-000ba0164e40"

2. **Extract the page ID from search results:**
   - Check if results array has at least one item
   - Get `page_id` from first result: `results[0].id`

3. **Build the GitHub URL:**
   - Format: `https://github.com/jamesgray007/agent-skills/tree/main/{skill-name}`
   - Example: `https://github.com/jamesgray007/agent-skills/tree/main/exporting-skills-from-claude`

4. **Update the Notion page:**
   - Use tool: `Notion:notion-update-page`
   - Parameters:
     ```json
     {
       "data": {
         "command": "update_properties",
         "page_id": "[page_id from step 2]",
         "properties": {
           "GitHub": "[github_url from step 3]",
           "Status": "Deployed"
         }
       }
     }
     ```

5. **Handle errors:**
   - If skill not found in search: Log warning "⚠️ {skill-name} not found in AI Building Blocks"
   - If update fails: Log error with details
   - Continue with next skill regardless

**Example execution:**
```
Skill: syncing-skills-to-github

1. Search: Notion:notion-search
   → Found page_id: 2e1edcfd-b924-811a-99b7-c1d4724722fa

2. GitHub URL: https://github.com/jamesgray007/agent-skills/tree/main/syncing-skills-to-github

3. Update: Notion:notion-update-page
   → Updated GitHub URL ✓
   → Set Status to "Deployed" ✓

Result: ✅ Notion updated successfully
```

### Step 8: Generate README.md

Auto-generate an index of all skills.

```bash
cd ~/.claude/skills

# Run the README generation script
./generate-readme.sh

# This script:
# - Scans all skill folders
# - Extracts skill descriptions from SKILL.md frontmatter
# - Generates a formatted README with a single table

# Stage and commit README
git add README.md
git commit -m "[DOCS] Update README with skill index"
git push origin main
```

## Usage Modes

### Mode 1: Single Skill Sync

**Trigger:** "Sync the exporting-skills-from-claude skill to GitHub"

**Process:**
1. Verify skill exists in `~/.claude/skills/`
2. Check git status for this skill only
3. If no changes: inform user, exit
4. If changes: show what changed
5. Generate commit message for this skill
6. Commit and push
7. Update Notion for this skill with GitHub URL

**Example:**
```
User: "Sync the writing-linkedin-posts skill to GitHub"

Claude (in Claude Code):
[Checking ~/.claude/skills/writing-linkedin-posts/...]
[Detected changes: SKILL.md modified]

Changes detected:
- writing-linkedin-posts/SKILL.md (modified)

Generating commit message...

[Staging changes...]
[Committing...]
[Pushing to GitHub...]

✅ Synced writing-linkedin-posts to GitHub
📝 Commit: abc123f
🔗 https://github.com/jamesgray007/agent-skills/tree/main/writing-linkedin-posts

[Updating Notion AI Building Blocks...]
✅ Updated GitHub URL in Notion

Complete!
```

### Mode 2: Batch Sync (All Changes)

**Trigger:** "Sync all changed skills to GitHub" or "Sync skills to GitHub"

**Process:**
1. Run `git status` to detect all changes
2. Identify all affected skill directories
3. Show summary of changes
4. Generate batch commit message
5. Commit all changes
6. Push to GitHub
7. Update Notion for all changed skills
8. Generate/update README.md

**Example:**
```
User: "Sync all changed skills to GitHub"

Claude (in Claude Code):
[Scanning ~/.claude/skills/...]
[Running git status...]

Changes detected in 3 skills:

New skills:
- exporting-skills-from-claude

Modified skills:
- writing-linkedin-posts
- creating-video-content

Generating commit message...

[Staging all changes...]
[Committing...]
[Pushing to GitHub...]

✅ Synced 3 skills to GitHub
📝 Commit: def456g
🔗 https://github.com/jamesgray007/agent-skills

[Updating Notion AI Building Blocks for 3 skills...]
✅ Updated exporting-skills-from-claude
✅ Updated writing-linkedin-posts
✅ Updated creating-video-content

[Updating README.md...]
✅ Generated skill index

Complete! All skills are now synced.
```

### Mode 3: Dry Run (Preview Changes)

**Trigger:** "Show what would sync to GitHub" or "Preview git sync"

**Process:**
1. Detect changes (don't commit)
2. Show what would be committed
3. Display generated commit message
4. Ask for confirmation before proceeding

**Example:**
```
User: "Show what would sync to GitHub"

Claude (in Claude Code):
[Scanning for changes...]

Would sync 2 skills:

Modified:
- writing-linkedin-posts/SKILL.md (347 lines changed)
- writing-linkedin-posts/references/HOOKS.md (new file)

Commit message would be:
---
[UPDATE] writing-linkedin-posts: Added 20 new hook templates

- New reference file with hook templates
- Updated main SKILL.md with examples
- Categorized by industry and use case
---

Ready to sync? (yes/no)
```

## Error Handling

### Scenario: Not in Git Repository

```
❌ Error: ~/.claude/skills is not a git repository

To fix:
1. cd ~/.claude/skills
2. git init
3. git remote add origin git@github.com:jamesgray007/agent-skills.git
4. git add .
5. git commit -m "[INIT] Initial skill repository"
6. git push -u origin main
```

### Scenario: Push Fails (Diverged Branches)

```
❌ Error: Push rejected (branch diverged)

This means the remote has commits you don't have locally.

Options:
A) Pull and rebase (recommended)
B) Pull and merge
C) Force push (⚠️  destructive)

Which would you like?
```

**If user chooses A:**
```bash
git pull --rebase origin main
git push origin main
```

### Scenario: Merge Conflicts

```
❌ Error: Merge conflicts detected

Conflicts in:
- writing-linkedin-posts/SKILL.md

You need to resolve these manually:
1. Open the file in your editor
2. Look for <<<<<<< HEAD markers
3. Resolve conflicts
4. git add writing-linkedin-posts/SKILL.md
5. git rebase --continue
6. git push origin main

Would you like me to show the conflicts?
```

### Scenario: Notion Update Fails

```
⚠️  Warning: GitHub sync succeeded but Notion update failed

Skills synced to GitHub: 3
Notion updates failed: 1
- exporting-skills-from-claude (not found in AI Building Blocks)

GitHub URL: https://github.com/jamesgray007/agent-skills

Would you like to register the missing skill in Notion?
```

### Scenario: No Changes Detected

```
ℹ️  No changes detected in ~/.claude/skills/

Everything is already synced to GitHub.

Last sync: 2026-01-12 14:30:45
Last commit: abc123f "[UPDATE] writing-linkedin-posts: Added hooks"
```

## Best Practices

### Commit Hygiene
- **Atomic commits:** One logical change per commit when possible
- **Descriptive messages:** Always explain WHY, not just WHAT
- **Consistent prefixes:** Use [CREATE], [UPDATE], [FIX], etc.
- **Link to issues:** Reference Notion pages or issues if relevant

### Sync Frequency
- **After each skill creation:** Immediate sync
- **After bulk updates:** Daily or end-of-day sync
- **Weekly review:** Sunday planning session
- **Before major changes:** Commit current state first

### Branch Strategy
**Recommendation: Simple main-only**
- All skills committed to `main` branch
- No feature branches (skills are standalone)
- Use tags for milestones: `v1.0-stable-2026-01`

**Alternative: Development branch**
```
main         → Production-ready skills
development  → Testing/in-progress skills
```

### Notion Integration
- **Always update Notion** after GitHub sync
- **Keep Status field current:** "Deployed" when synced
- **Track Last edited time** automatically (set by Notion)
- **Maintain GitHub URLs** for easy reference

## Integration Points

### With exporting-skills-from-claude
This skill is **Part 2** of the workflow:
1. Part 1: Export cloud → local (Claude Desktop)
2. Part 2: Local → GitHub (Claude Code) ← **This skill**

**Complete workflow:**
```
Claude.ai (/mnt/skills/user/)
    ↓ [Export]
Local (~/.claude/skills/)
    ↓ [Sync] ← This skill
GitHub (github.com/jamesgray007/agent-skills)
    ↓ [Update URLs]
Notion (AI Building Blocks database)
```

### With Notion AI Building Blocks
After successful GitHub sync:
- Updates GitHub property with URL
- Sets Status to "Deployed"
- Last edited time automatically updated by Notion

### With Business Process Guides
Skills synced to GitHub can be:
- Referenced in process documentation
- Shared with team members (if applicable)
- Included in client deliverables (if applicable)
- Version-controlled for auditing

## Security & Privacy

### Private Repository
- Repository `jamesgray007/agent-skills` is **private**
- No public access without explicit sharing
- Contains proprietary business workflows
- Protected by GitHub authentication

### No Sensitive Data
- Never commit API keys or credentials
- Use placeholder data in examples
- Sanitize client information
- Review diff before committing

### Git Credentials
- Claude Code uses your existing git credentials
- SSH keys or HTTPS tokens from your environment
- No credentials stored in skill itself

## Workflow Examples

### Example 1: Daily Workflow - Create and Sync New Skill

**Morning (Claude.ai):**
```
User: Create a skill for aggregating HubSpot metrics for weekly reviews

Claude: [Creates skill in Claude.ai]
[Skill saved to /mnt/skills/user/hubspot-metrics-aggregation/]
[Registered in Notion AI Building Blocks]
```

**End of Day (Claude Desktop):**
```
User: Export the hubspot-metrics-aggregation skill

Claude: [Exports to ~/.claude/skills/hubspot-metrics-aggregation/]
✅ Exported successfully
```

**End of Day (Claude Code - terminal):**
```
User: Sync the hubspot-metrics-aggregation skill to GitHub

Claude: [Detects new skill]
[Commits with "[CREATE] hubspot-metrics-aggregation: Pull weekly metrics"]
[Pushes to GitHub]
[Updates Notion]
✅ Complete!
```

### Example 2: Weekly Batch Sync

**Sunday Planning (Claude Code):**
```
User: Sync all changed skills to GitHub

Claude: [Scanning...]

Changes detected in 5 skills:

New: 2 skills
- hubspot-metrics-aggregation
- email-response-templates

Updated: 3 skills
- writing-linkedin-posts (added hooks)
- creating-video-content (new platforms)
- syncing-skills-to-github (refactored for flat structure)

[Commits with batch message]
[Pushes to GitHub]
[Updates all 5 skills in Notion]
[Generates README.md via generate-readme.sh]

✅ Synced 5 skills
```

### Example 3: Fix Broken Skill

**During work (Claude.ai):**
```
User: The importing-maven-students skill is broken, fix it

Claude: [Fixes skill]
[Tests fix]
```

**Immediately after (Claude Desktop):**
```
User: Export importing-maven-students

Claude: [Exports to ~/.claude/skills/importing-maven-students/, conflict detected]
[Shows diff]

User: Overwrite with cloud version

Claude: [Overwrites]
✅ Exported
```

**Immediately after (Claude Code):**
```
User: Sync importing-maven-students to GitHub - urgent fix

Claude: [Detects changes in importing-maven-students]
[Commits: "[FIX] importing-maven-students: Fixed CSV parsing bug"]
[Pushes to GitHub]
[Updates Notion]
✅ Fix deployed!
```

## Success Metrics
- ✅ Zero data loss (all skills in version control)
- ✅ Complete history (every change tracked)
- ✅ Instant recovery (git clone to restore)
- ✅ Automated tracking (Notion always current)
- ✅ Fast workflow (export to GitHub quickly)

## Future Enhancements
- [ ] Automated testing before sync
- [ ] Skill dependency tracking
- [ ] Change log generation
- [ ] Version tagging (v1.0, v2.0)
- [ ] Skill marketplace for sharing
- [ ] CI/CD pipeline for validation

## Dependencies
- Claude Code (terminal access with git credentials)
- Git installed and configured
- GitHub repository: `jamesgray007/agent-skills`
- Notion API access for AI Building Blocks database
- Bash shell for git commands

## Notes
- This is **Part 2** of two-skill system
- **Part 1** (exporting-skills-from-claude) runs in Claude Desktop
- **Part 2** (this skill) runs in Claude Code
- Git credentials come from your environment
- Works with both SSH and HTTPS git remotes
- Supports single-skill and batch operations
- Always updates Notion after successful sync
