import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import starlightBlog from 'starlight-blog';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://handsonai.info',
  trailingSlash: 'always',
  redirects: {
    '/courses/leaders/setup-checklist/': '/courses/tools-setup-checklist/',
    // Legacy "cookbook" → "playbook" rename
    '/use-the-cookbook/': '/use-the-playbook/',
    '/use-the-cookbook/build/': '/use-the-playbook/build/',
    '/use-the-cookbook/build/ai-registry/': '/use-the-playbook/build/ai-registry/',
    '/use-the-cookbook/build/business-first-ai/': '/use-the-playbook/build/',
    '/use-the-cookbook/build/agentic-coding/': '/use-cases/coding/agentic-coding/',
    // Framework step rename (discover → analyze)
    '/business-first-ai-framework/discover/': '/business-first-ai-framework/analyze/',
    // Platform-prefixed framework pages moved to top-level framework section
    '/platforms/business-first-ai-framework/deconstruct/': '/business-first-ai-framework/deconstruct/',
    '/platforms/business-first-ai-framework/analyze/': '/business-first-ai-framework/analyze/',
    // Removed how-to namespace — examples live under the framework now
    '/how-to/workflow-examples/autonomous-agent/': '/business-first-ai-framework/examples/autonomous-agent/',
    // Legacy builder-setup pages consolidated
    '/builder-setup/cli/': '/builder-setup/',
    '/builder-setup/ai-platforms/': '/builder-setup/',
    // Legacy feed URL
    '/feed/rss_created.xml': '/rss.xml',
    // Agents pages moved to building-blocks section
    '/platforms/claude/agents/building-agents/': '/agentic-building-blocks/agents/',
    '/platforms/openai/agents/building-agents/': '/agentic-building-blocks/agents/',
    // Skills subpage consolidated
    '/agentic-building-blocks/skills/questions/': '/agentic-building-blocks/skills/',
    // Misindexed as subpages of self-consistency (it's a leaf page)
    '/agentic-building-blocks/prompts/prompt-engineering/self-consistency-and-reflection/chain-of-thought/': '/agentic-building-blocks/prompts/prompt-engineering/chain-of-thought/',
    '/agentic-building-blocks/prompts/prompt-engineering/self-consistency-and-reflection/reframing-prompts/': '/agentic-building-blocks/prompts/prompt-engineering/reframing-prompts/',
  },
  integrations: [
    starlight({
      title: 'Hands-on AI Playbook',
      logo: {
        src: './public/assets/logo-horizontal.png',
      },
      favicon: '/assets/logo.png',
      social: [
        { icon: 'linkedin', label: 'LinkedIn', href: 'https://www.linkedin.com/in/jamesgray/' },
        { icon: 'github', label: 'GitHub', href: 'https://github.com/jamesgray-ai' },
        { icon: 'rss', label: 'RSS', href: '/rss.xml' },
      ],
      customCss: ['./src/styles/custom.css'],
      lastUpdated: true,
      editLink: {
        baseUrl: 'https://github.com/jamesgray-ai/handsonai/edit/main/',
      },
      tableOfContents: { minHeadingLevel: 2, maxHeadingLevel: 3 },
      head: [
        { tag: 'script', attrs: { src: 'https://www.googletagmanager.com/gtag/js?id=G-4YB89PWFET', async: true } },
        { tag: 'script', content: "window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}gtag('js',new Date());gtag('config','G-4YB89PWFET');" },
        { tag: 'link', attrs: { rel: 'stylesheet', href: 'https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&family=Roboto+Mono:wght@400&display=swap' } },
      ],
      components: {
        Head: './src/components/Head.astro',
      },
      sidebar: [
        { label: 'Home', link: '/' },
        { label: 'About', link: '/about/' },
        {
          label: 'Tools & Resources',
          collapsed: true,
          items: [
            { label: 'Overview', link: '/use-the-playbook/' },
            { label: 'MCP Server', link: '/mcp-server/' },
            {
              label: 'Agents & Skills',
              collapsed: true,
              items: [
                { label: 'Browse Agents & Skills', link: '/use-the-playbook/build/' },
                { label: 'Using Plugins', link: '/use-the-playbook/build/using-plugins/' },
                { label: 'AI Workflow Examples', link: '/use-the-playbook/build/ai-workflow-examples/' },
                { label: 'AI Registry', link: '/use-the-playbook/build/ai-registry/' },
              ],
            },
            {
              label: 'Resources',
              collapsed: true,
              items: [
                { label: 'Overview', link: '/resources/' },
                { label: 'OpenAI Use Cases Report', link: '/resources/openai-use-cases-report/' },
                { label: 'Anthropic Coding Trends', link: '/resources/anthropic-coding-trends/' },
                { label: 'Anthropic Skills Guide', link: '/resources/anthropic-skills-guide/' },
              ],
            },
            { label: 'Learn with James', link: '/courses/' },
          ],
        },
        { label: "What's New", link: '/blog/' },
        {
          label: 'Business-First AI Framework',
          collapsed: true,
          items: [
            { label: 'Overview', link: '/business-first-ai-framework/' },
            { label: 'AI Workflow Design Matrix', link: '/business-first-ai-framework/workflow-design-matrix/' },
            { label: 'Step 1: Analyze', link: '/business-first-ai-framework/analyze/' },
            { label: 'Step 2: Deconstruct', link: '/business-first-ai-framework/deconstruct/' },
            { label: 'Step 3: Design', link: '/business-first-ai-framework/design/' },
            { label: 'Step 4: Build', link: '/business-first-ai-framework/build/' },
            { label: 'Step 5: Test', link: '/business-first-ai-framework/test/' },
            { label: 'Step 6: Run', link: '/business-first-ai-framework/run/' },
            { label: 'Step 7: Improve', link: '/business-first-ai-framework/improve/' },
            { label: 'Set Up the Skills', link: '/business-first-ai-framework/skills/' },
            {
              label: 'Worked Examples',
              collapsed: true,
              items: [
                { label: 'Analyze: Example Reports', link: '/business-first-ai-framework/analyze-examples/' },
                { label: 'Deterministic Automation', link: '/business-first-ai-framework/examples/deterministic-automation/' },
                { label: 'AI Collaborative', link: '/business-first-ai-framework/examples/ai-collaborative/' },
                { label: 'Autonomous Agent', link: '/business-first-ai-framework/examples/autonomous-agent/' },
                { label: 'Full Example: Content Calendar Planning', link: '/business-first-ai-framework/examples/content-calendar-planning/' },
              ],
            },
            {
              label: 'Questions',
              collapsed: true,
              items: [
                { label: 'Find workflows worth applying AI to', link: '/business-first-ai-framework/questions/how-do-i-find-workflows-worth-applying-ai-to/' },
                { label: 'Identify the right AI tools for a workflow', link: '/business-first-ai-framework/questions/how-do-i-identify-the-right-ai-tools-for-a-workflow/' },
              ],
            },
          ],
        },
        {
          label: 'Agentic Building Blocks',
          collapsed: true,
          items: [
            { label: 'Overview', link: '/agentic-building-blocks/' },
            { label: 'Choosing the Right Building Block', link: '/agentic-building-blocks/comparison/' },
            {
              label: 'Intelligence',
              collapsed: true,
              items: [
                { label: 'Model', link: '/agentic-building-blocks/models/' },
                {
                  label: 'Context',
                  collapsed: true,
                  items: [
                    { label: 'Overview', link: '/agentic-building-blocks/context/' },
                    { label: 'Context Graphs', link: '/agentic-building-blocks/context/context-graphs/' },
                  ],
                },
                {
                  label: 'Projects',
                  collapsed: true,
                  items: [
                    { label: 'Overview', link: '/agentic-building-blocks/projects/' },
                    { label: 'Project Instructions', link: '/agentic-building-blocks/projects/workspace-instructions-meta-prompt/' },
                  ],
                },
                { label: 'Memory', link: '/agentic-building-blocks/memory/' },
              ],
            },
            {
              label: 'Orchestration',
              collapsed: true,
              items: [
                {
                  label: 'Prompts',
                  collapsed: true,
                  items: [
                    { label: 'Overview', link: '/agentic-building-blocks/prompts/' },
                    {
                      label: 'Prompt Engineering',
                      collapsed: true,
                      items: [
                        { label: 'Overview', link: '/agentic-building-blocks/prompts/prompt-engineering/' },
                        { label: 'Zero-Shot Prompting', link: '/agentic-building-blocks/prompts/prompt-engineering/zero-shot-prompting/' },
                        { label: 'Few-Shot Learning', link: '/agentic-building-blocks/prompts/prompt-engineering/few-shot-learning/' },
                        { label: 'Chain-of-Thought', link: '/agentic-building-blocks/prompts/prompt-engineering/chain-of-thought/' },
                        { label: 'Direct Instruction', link: '/agentic-building-blocks/prompts/prompt-engineering/direct-instruction/' },
                        { label: 'Contextual Prompting', link: '/agentic-building-blocks/prompts/prompt-engineering/contextual-prompting/' },
                        { label: 'Role Prompting', link: '/agentic-building-blocks/prompts/prompt-engineering/role-prompting/' },
                        { label: 'Output Formatting', link: '/agentic-building-blocks/prompts/prompt-engineering/output-formatting/' },
                        { label: 'Multi-Turn Conversation', link: '/agentic-building-blocks/prompts/prompt-engineering/multi-turn-conversation/' },
                        { label: 'Self-Consistency and Reflection', link: '/agentic-building-blocks/prompts/prompt-engineering/self-consistency-and-reflection/' },
                        { label: 'Emotional Prompting', link: '/agentic-building-blocks/prompts/prompt-engineering/emotional-prompting/' },
                        { label: 'Reframing Prompts', link: '/agentic-building-blocks/prompts/prompt-engineering/reframing-prompts/' },
                        { label: 'Style Unbundling', link: '/agentic-building-blocks/prompts/prompt-engineering/style-unbundling/' },
                        { label: 'Summarization and Distillation', link: '/agentic-building-blocks/prompts/prompt-engineering/summarization-and-distillation/' },
                        { label: 'Real-World Constraints', link: '/agentic-building-blocks/prompts/prompt-engineering/real-world-constraints/' },
                        { label: 'Resources', link: '/agentic-building-blocks/prompts/prompt-engineering/resources/' },
                      ],
                    },
                    {
                      label: 'Questions',
                      collapsed: true,
                      items: [
                        { label: 'What is a system prompt?', link: '/agentic-building-blocks/prompts/questions/what-is-a-system-prompt/' },
                      ],
                    },
                  ],
                },
                {
                  label: 'Skills',
                  collapsed: true,
                  items: [
                    { label: 'Overview', link: '/agentic-building-blocks/skills/' },
                    {
                      label: 'Questions',
                      collapsed: true,
                      items: [
                        { label: 'Difference between a skill and an agent', link: '/agentic-building-blocks/skills/questions/what-is-the-difference-between-a-skill-and-an-agent-in-claude-code/' },
                        { label: 'Do plugin skills conflict with custom skills?', link: '/agentic-building-blocks/skills/questions/do-plugin-skills-conflict-with-custom-skills/' },
                      ],
                    },
                  ],
                },
                {
                  label: 'Agents',
                  collapsed: true,
                  items: [
                    { label: 'Overview', link: '/agentic-building-blocks/agents/' },
                    { label: 'Programming Frameworks', link: '/agentic-building-blocks/agents/frameworks/' },
                    {
                      label: 'Capability Patterns',
                      collapsed: true,
                      items: [
                        { label: 'Overview', link: '/agentic-building-blocks/agents/capability-patterns/' },
                        { label: 'Reflection', link: '/agentic-building-blocks/agents/capability-patterns/reflection/' },
                        { label: 'Tool Use', link: '/agentic-building-blocks/agents/capability-patterns/tool-use/' },
                        { label: 'Planning', link: '/agentic-building-blocks/agents/capability-patterns/planning/' },
                        { label: 'Multi-Agent Collaboration', link: '/agentic-building-blocks/agents/capability-patterns/multi-agent-collaboration/' },
                        { label: 'Memory', link: '/agentic-building-blocks/agents/capability-patterns/memory/' },
                        { label: 'Guardrails', link: '/agentic-building-blocks/agents/capability-patterns/guardrails/' },
                        { label: 'Human-in-the-Loop', link: '/agentic-building-blocks/agents/capability-patterns/human-in-the-loop/' },
                      ],
                    },
                    {
                      label: 'Orchestration Patterns',
                      collapsed: true,
                      items: [
                        { label: 'Overview', link: '/agentic-building-blocks/agents/orchestration-patterns/' },
                        { label: 'Sequential', link: '/agentic-building-blocks/agents/orchestration-patterns/sequential/' },
                        { label: 'Parallel', link: '/agentic-building-blocks/agents/orchestration-patterns/parallel/' },
                        { label: 'Router', link: '/agentic-building-blocks/agents/orchestration-patterns/router/' },
                        { label: 'Hierarchical', link: '/agentic-building-blocks/agents/orchestration-patterns/hierarchical/' },
                        { label: 'Handoff', link: '/agentic-building-blocks/agents/orchestration-patterns/handoff/' },
                        { label: 'Evaluator-Optimizer', link: '/agentic-building-blocks/agents/orchestration-patterns/evaluator-optimizer/' },
                        { label: 'Group Chat', link: '/agentic-building-blocks/agents/orchestration-patterns/group-chat/' },
                        { label: 'Decentralized', link: '/agentic-building-blocks/agents/orchestration-patterns/decentralized/' },
                      ],
                    },
                    { label: 'Resources', link: '/agentic-building-blocks/agents/resources/' },
                  ],
                },
              ],
            },
            {
              label: 'Integration',
              collapsed: true,
              items: [
                {
                  label: 'MCP',
                  collapsed: true,
                  items: [
                    { label: 'Overview', link: '/agentic-building-blocks/mcp/' },
                    {
                      label: 'Questions',
                      collapsed: true,
                      items: [
                        { label: 'How do I connect an MCP server to Claude Code', link: '/agentic-building-blocks/mcp/questions/how-do-i-connect-an-mcp-server-to-claude-code/' },
                      ],
                    },
                  ],
                },
                { label: 'API', link: '/agentic-building-blocks/api/' },
                { label: 'SDK', link: '/agentic-building-blocks/sdk/' },
                { label: 'CLI', link: '/agentic-building-blocks/cli/' },
              ],
            },
          ],
        },
        {
          label: 'Use Cases',
          collapsed: true,
          items: [
            { label: 'Overview', link: '/use-cases/' },
            {
              label: 'Content Creation',
              collapsed: true,
              items: [
                { label: 'Overview', link: '/use-cases/content-creation/' },
                { label: 'Resources', link: '/use-cases/content-creation/resources/' },
              ],
            },
            {
              label: 'Research',
              collapsed: true,
              items: [
                { label: 'Overview', link: '/use-cases/research/' },
                { label: 'Resources', link: '/use-cases/research/resources/' },
              ],
            },
            {
              label: 'Coding',
              collapsed: true,
              items: [
                { label: 'Overview', link: '/use-cases/coding/' },
                { label: 'Agentic Coding', link: '/use-cases/coding/agentic-coding/' },
                { label: 'Resources', link: '/use-cases/coding/resources/' },
              ],
            },
            {
              label: 'Data Analysis',
              collapsed: true,
              items: [
                { label: 'Overview', link: '/use-cases/data-analysis/' },
                { label: 'Resources', link: '/use-cases/data-analysis/resources/' },
              ],
            },
            {
              label: 'Ideation & Strategy',
              collapsed: true,
              items: [
                { label: 'Overview', link: '/use-cases/ideation-and-strategy/' },
                { label: 'Resources', link: '/use-cases/ideation-and-strategy/resources/' },
              ],
            },
            {
              label: 'Automation',
              collapsed: true,
              items: [
                { label: 'Overview', link: '/use-cases/automation/' },
                { label: 'Resources', link: '/use-cases/automation/resources/' },
              ],
            },
          ],
        },
        {
          label: 'Platforms',
          collapsed: true,
          items: [
            { label: 'Overview', link: '/platforms/' },
            {
              label: 'Claude',
              collapsed: true,
              items: [
                { label: 'Overview', link: '/platforms/claude/' },
                { label: 'Getting Started', link: '/platforms/claude/getting-started/' },
                { label: 'Claude Projects', link: '/platforms/claude/projects/claude-projects-setup/' },
                {
                  label: 'Agents',
                  collapsed: true,
                  items: [
                    { label: 'Building Agents on Claude', link: '/platforms/claude/agents/building-agents/' },
                    { label: 'Scheduling Subagents', link: '/platforms/claude/subagents/scheduling-subagents/' },
                    { label: 'Troubleshooting', link: '/platforms/claude/subagents/scheduling-subagent-issues/' },
                  ],
                },
                {
                  label: 'Skills',
                  collapsed: true,
                  items: [
                    { label: 'Discover Your Best Claude Skills', link: '/platforms/claude/skills/skills-discovery-meta-prompt/' },
                    { label: 'Resources', link: '/platforms/claude/skills/resources/' },
                  ],
                },
                {
                  label: 'Questions',
                  collapsed: true,
                  items: [
                    { label: 'Overview', link: '/platforms/claude/questions/' },
                    { label: 'Best way to name agent skills?', link: '/platforms/claude/questions/what-is-the-best-way-to-name-claude-agent-skills/' },
                    { label: 'Schedule an automated subagent', link: '/platforms/claude/questions/how-do-i-schedule-an-automated-claude-subagent/' },
                  ],
                },
                { label: 'Topics', link: '/platforms/claude/topics/' },
                { label: 'Resources', link: '/platforms/claude/topics/resources/' },
              ],
            },
            {
              label: 'Google Gemini',
              collapsed: true,
              items: [
                { label: 'Overview', link: '/platforms/google-gemini/' },
                { label: 'Getting Started', link: '/platforms/google-gemini/getting-started/' },
                { label: 'Building Agents on Google', link: '/platforms/google-gemini/agents/building-agents/' },
                { label: 'Questions', link: '/platforms/google-gemini/questions/' },
                { label: 'Topics', link: '/platforms/google-gemini/topics/' },
                { label: 'Resources', link: '/platforms/google-gemini/topics/resources/' },
              ],
            },
            {
              label: 'M365 Copilot',
              collapsed: true,
              items: [
                { label: 'Overview', link: '/platforms/m365-copilot/' },
                { label: 'Getting Started', link: '/platforms/m365-copilot/getting-started/' },
                { label: 'Building Agents on M365 Copilot', link: '/platforms/m365-copilot/agents/building-agents/' },
                { label: 'Topics', link: '/platforms/m365-copilot/topics/' },
                { label: 'Resources', link: '/platforms/m365-copilot/topics/resources/' },
              ],
            },
            {
              label: 'OpenAI',
              collapsed: true,
              items: [
                { label: 'Overview', link: '/platforms/openai/' },
                { label: 'Getting Started', link: '/platforms/openai/getting-started/' },
                { label: 'Building Agents on OpenAI', link: '/platforms/openai/agents/building-agents/' },
                { label: 'Questions', link: '/platforms/openai/questions/' },
                { label: 'Topics', link: '/platforms/openai/topics/' },
                { label: 'Resources', link: '/platforms/openai/topics/resources/' },
              ],
            },
          ],
        },
        {
          label: 'Builder Tools Setup',
          collapsed: true,
          items: [
            { label: 'Overview', link: '/builder-setup/' },
            { label: 'AI Code Editor', link: '/builder-setup/editor-setup/' },
            { label: 'Git', link: '/builder-setup/git-install/' },
            { label: 'GitHub', link: '/builder-setup/github-setup/' },
            { label: 'Voice to Text', link: '/builder-setup/voice-to-text-setup/' },
            { label: 'AI Registry', link: '/builder-setup/notion-registry-setup/' },
            { label: 'Terminal Basics (reference)', link: '/builder-setup/terminal-basics/' },
          ],
        },
        {
          label: 'Product & Engineering',
          collapsed: true,
          items: [
            { label: 'Overview', link: '/product-engineering/' },
            {
              label: 'Product',
              collapsed: true,
              items: [
                { label: 'Product Requirements', link: '/product-engineering/requirements/' },
                { label: 'User Stories & Acceptance Criteria', link: '/product-engineering/user-stories/' },
                { label: 'Roadmaps & Prioritization', link: '/product-engineering/roadmapping/' },
                { label: 'Stakeholder Management', link: '/product-engineering/stakeholder-management/' },
              ],
            },
            {
              label: 'Engineering',
              collapsed: true,
              items: [
                { label: 'Software Development Lifecycle', link: '/product-engineering/sdlc/' },
                { label: 'Project Tracking with GitHub', link: '/product-engineering/tracking/' },
                { label: 'Architecture Decision Records', link: '/product-engineering/architecture-decisions/' },
                { label: 'Context Engineering', link: '/ai-engineering/context-engineering/' },
                { label: 'Evaluation', link: '/ai-engineering/evaluation/' },
              ],
            },
          ],
        },
        {
          label: 'Patterns',
          collapsed: true,
          items: [
            { label: 'Overview', link: '/patterns/' },
            {
              label: 'Workflow Architecture Patterns',
              collapsed: true,
              items: [
                { label: 'Overview', link: '/patterns/workflow-architecture/' },
                { label: 'Augmented LLM', link: '/patterns/workflow-architecture/augmented-llm/' },
                { label: 'Prompt Chaining', link: '/patterns/workflow-architecture/prompt-chaining/' },
                { label: 'Routing', link: '/patterns/workflow-architecture/routing/' },
                { label: 'Parallelization', link: '/patterns/workflow-architecture/parallelization/' },
                { label: 'Orchestrator-Workers', link: '/patterns/workflow-architecture/orchestrator-workers/' },
                { label: 'Evaluator-Optimizer', link: '/patterns/workflow-architecture/evaluator-optimizer/' },
                { label: 'Autonomous Agents', link: '/patterns/workflow-architecture/autonomous-agents/' },
              ],
            },
          ],
        },
        {
          label: 'Learn with James',
          collapsed: true,
          items: [
            { label: 'Overview', link: '/courses/' },
            { label: 'Tools Setup Checklist', link: '/courses/tools-setup-checklist/' },
            { label: 'Agentic AI for Leaders', link: '/courses/leaders/' },
            { label: 'Claude for Builders', link: '/courses/builders/' },
            {
              label: 'Questions',
              collapsed: true,
              items: [
                { label: 'Corporate AI Training', link: '/courses/questions/corporate-ai-training/' },
              ],
            },
          ],
        },
        { label: 'What People Built', link: '/what-people-built/' },
      ],
    }),
    starlightBlog({
      title: "What's New",
      prefix: 'blog',
      authors: {
        jamesgray: {
          name: 'James Gray',
          url: 'https://jamesgray.ai',
          picture: './public/assets/images/james-gray-headshot.jpg',
        },
      },
    }),
    sitemap(),
  ],
});
