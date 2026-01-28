# AI Operations Registry Setup

Set up your personal AI Operations Registry in Notion to track business processes, workflows, AI assets, and connected applications.

## Prerequisites

- Notion account (free or paid)
- Basic familiarity with Notion databases

## Quick Setup (5 minutes)

### Step 1: Open the Template

Click this link to access the AI Operations Registry template:

**[AI Operations Registry - Template](https://www.notion.so/2f3edcfdb924813f86f3eacca6b836bb)**

### Step 2: Duplicate to Your Workspace

1. Click the **"Duplicate"** button in the top-right corner
2. Select your destination workspace
3. The template will copy to your workspace with all 4 databases and sample entries

### Step 3: Verify the Copy

After duplication, confirm you have:

- [ ] **Business Processes** database with 3 sample entries
- [ ] **Workflows** database with 3 sample entries
- [ ] **AI Assets** database with 3 sample entries
- [ ] **Apps** database with 3 sample entries
- [ ] Relations between databases are working (click a workflow to see linked items)

## Understanding the Registry Structure

### The Four Databases

| Database | Purpose | Key Fields |
|----------|---------|------------|
| **Business Processes** | High-level business functions | Domain, LOB, Description |
| **Workflows** | Specific workflows within processes | Status, Type, Trigger, Process Outcome |
| **AI Assets** | Skills, prompts, agents, projects | Asset Type, Platform, Status, Dependencies |
| **Apps** | Connected applications & integrations | Type, Auth Type, Connection Status |

### How Relations Work

The databases are linked to show how your operations connect:

```
Business Process → Workflows → AI Assets
                           ↘ Apps
```

- Each **Business Process** contains multiple **Workflows**
- Each **Workflow** can use multiple **AI Assets** and **Apps**
- Changes propagate automatically through relations

## Customizing Your Registry

### 1. Update Domain Options

Edit the **Domain** select field in Business Processes to match your business areas:
- Click any Domain cell → "Edit property" → Add/remove options

### 2. Add Your Asset Types

Customize the **Asset Type** options in AI Assets:
- Skill, Prompt, Agent, Project, Context MD, etc.

### 3. Configure App Types

Update the **Type** field in Apps for your integration patterns:
- API, MCP Server, Native Integration, Webhook, AI Browser

## Next Steps

1. **Clear sample entries** - Delete the example data when ready
2. **Add your first process** - Start with one business domain
3. **Document existing workflows** - Capture what you're already doing
4. **Connect to Claude** - Add the Notion MCP server to give Claude access to your registry

## Connecting to Claude (Optional)

To let Claude read and update your registry:

1. Configure the Notion MCP server (see [Notion MCP documentation](https://www.npmjs.com/package/@modelcontextprotocol/server-notion))
2. Share your registry page with the Notion integration
3. Ask Claude to help you document workflows or suggest AI assets

## Troubleshooting

**Relations not copying correctly?**
- This is rare with Notion duplicates. Try duplicating again.
- Ensure you're duplicating the entire page, not individual databases.

**Can't find the template?**
- The template must be shared publicly. Contact the course instructor if the link doesn't work.

**Need to start over?**
- Delete your copy and duplicate the template again.

## Questions?

Post in Slack or attend office hours for setup support.
