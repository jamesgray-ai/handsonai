# Quick Reference: Syncing Skills to GitHub

## Quick Start

### Sync All Skills
```
"Sync all my skills to GitHub"
```

### Sync Specific Skill
```
"Sync the [skill-name] skill to GitHub"
```

### After Creating New Skill
```
"I just created a new skill for [purpose]. Sync it to GitHub."
```

### After Updating Skill
```
"I updated the [skill-name] skill. Sync it to GitHub."
```

## What Happens

1. **Clone/Pull**: Repository cloned to `/tmp/agent-skills-sync` or latest pulled
2. **Scan**: All skills in `/mnt/skills/user` scanned for changes
3. **Compare**: Changed skills identified
4. **Copy**: Changed files copied to repository
5. **README**: Auto-generated skill index
6. **Commit**: Detailed commit message created
7. **Push**: Changes pushed to GitHub
8. **Notion**: GitHub URLs updated in AI Assets

## Repository Information

- **URL**: https://github.com/jamesgray007/agent-skills
- **Visibility**: Private
- **Working Directory**: `/tmp/agent-skills-sync`
- **Skills Directory**: `skills/`
- **Branch**: `main`

## Commit Message Format

### Single Skill
```
[ACTION] skill-name: Brief description

Detailed changes:
- Specific change 1
- Specific change 2
- Specific change 3
```

### Multiple Skills
```
[SYNC] Updated X skills

Skills updated:
- skill-1: brief description
- skill-2: brief description
- skill-3: brief description
```

## Actions
- `[CREATE]` - New skill added
- `[UPDATE]` - Existing skill modified
- `[DELETE]` - Skill removed
- `[SYNC]` - Multiple skills updated

## Notion Integration

After each sync:
- **Search**: AI Assets database for each synced skill
- **Update**: GitHub property with skill URL
- **Format**: `https://github.com/jamesgray007/agent-skills/tree/main/skills/[skill-name]`
- **Not Found**: Offer to register skill first

## Common Commands

### Check Repository Status
```bash
cd /tmp/agent-skills-sync
git status
```

### View Commit History
```bash
cd /tmp/agent-skills-sync
git log --oneline
```

### Pull Latest from GitHub
```bash
cd /tmp/agent-skills-sync
git pull origin main
```

### View Specific Skill
```bash
cat /tmp/agent-skills-sync/skills/[skill-name]/SKILL.md
```

## Authentication

### Personal Access Token
- Generate at: https://github.com/settings/tokens
- Scope needed: `repo` (full control)
- Enter as password when prompted

### SSH Keys
- Generate: `ssh-keygen -t ed25519`
- Add to GitHub: https://github.com/settings/keys
- Use SSH URL: `git@github.com:jamesgray007/agent-skills.git`

## Troubleshooting

### "Authentication failed"
→ Configure git credentials (see SETUP-GUIDE.md)

### "Repository not found"
→ Verify repository exists and you have access

### "Nothing to commit"
→ No skills have changed since last sync

### "Notion update failed"
→ GitHub sync succeeded, Notion update can be retried

## File Structure

```
agent-skills/
├── README.md              # Auto-generated index
└── skills/
    ├── skill-1/
    │   ├── SKILL.md
    │   └── references/    # Optional
    ├── skill-2/
    │   └── SKILL.md
    └── ...
```

## Success Indicators

✅ Repository cloned/pulled successfully  
✅ Skills scanned and compared  
✅ Changed skills identified  
✅ Files copied to repository  
✅ README.md generated  
✅ Commit created with message  
✅ Push to GitHub successful  
✅ Notion AI Assets updated  

## Integration Points

**With registering-building-blocks**:
- Register building block in Notion → Auto-sync to GitHub

**With skill-creator**:
- Create skill → Trigger sync to GitHub

**With local desktop**:
- Keep local clone: `git pull origin main`

## Security Notes

- Repository is private
- Only you have access
- Use tokens or SSH keys
- Never commit credentials

## Daily Workflow

1. Create or update skill in Claude
2. Say: "Sync to GitHub"
3. Verify success message
4. Check Notion AI Assets for GitHub URL
5. (Optional) Pull to desktop clone

## Best Practices

- ✅ Sync after every skill change
- ✅ Review commit messages for accuracy
- ✅ Keep desktop clone updated
- ✅ Use descriptive skill names
- ✅ Organize references in subdirectories
- ❌ Don't commit sensitive data
- ❌ Don't manually edit repository (use skills as source)

## Links

- **Repository**: https://github.com/jamesgray007/agent-skills
- **Settings**: https://github.com/settings
- **Tokens**: https://github.com/settings/tokens
- **SSH Keys**: https://github.com/settings/keys

## Quick Commands Cheatsheet

```bash
# View working directory
ls /tmp/agent-skills-sync/skills

# Check git status
cd /tmp/agent-skills-sync && git status

# View recent commits
cd /tmp/agent-skills-sync && git log -5 --oneline

# View specific skill
cat /tmp/agent-skills-sync/skills/[skill-name]/SKILL.md

# Count skills in repository
ls /tmp/agent-skills-sync/skills | wc -l

# View README
cat /tmp/agent-skills-sync/README.md
```
