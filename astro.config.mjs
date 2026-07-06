import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import starlightBlog from 'starlight-blog';
import sitemap from '@astrojs/sitemap';
import llmsTxt from './src/integrations/llms-txt.mjs';

export default defineConfig({
  site: 'https://handsonai.info',
  trailingSlash: 'always',
  redirects: {
    '/courses/leaders/setup-checklist/': '/courses/tools-setup-checklist/',
    // Framework end-to-end exercise promoted from builders week 5 to a shared course resource (2026-07-06)
    '/courses/builders/week-5/': '/courses/framework-end-to-end/',
    // AI Registry moved from Notion to Markdown-first (2026-07-05)
    '/builder-setup/notion-registry-setup/': '/builder-setup/ai-registry-setup/',
    // Legacy "cookbook" → "playbook" rename
    '/use-the-cookbook/': '/use-the-playbook/',
    '/use-the-cookbook/build/': '/use-the-playbook/build/',
    '/use-the-cookbook/build/ai-registry/': '/use-the-playbook/build/handsonai/',
    '/use-the-cookbook/build/business-first-ai/': '/use-the-playbook/build/handsonai/',
    '/use-the-cookbook/build/agentic-coding/': '/use-cases/agentic-coding/',
    // Agentic coding moved to flat use case namespace (2026-05-17)
    '/use-cases/coding/agentic-coding/': '/use-cases/agentic-coding/',
    // Per-primitive resources pages removed (2026-05-17) — external resources live at /resources/
    '/use-cases/content-creation/resources/': '/resources/',
    '/use-cases/research/resources/': '/resources/',
    '/use-cases/coding/resources/': '/resources/',
    '/use-cases/data-analysis/resources/': '/resources/',
    '/use-cases/ideation-and-strategy/resources/': '/resources/',
    '/use-cases/automation/resources/': '/resources/',
    // Plugin consolidation — four old plugin pages → single handsonai plugin page
    '/use-the-playbook/build/ai-workflow-examples/': '/use-the-playbook/build/handsonai/',
    '/use-the-playbook/build/ai-registry/': '/use-the-playbook/build/handsonai/',
    '/use-the-playbook/build/business-first-ai/': '/use-the-playbook/build/handsonai/',
    '/use-the-playbook/build/agentic-coding/': '/use-the-playbook/build/handsonai/',
    // Framework step rename (discover → analyze)
    '/business-first-ai-framework/discover/': '/ai-workflow-framework/analyze/',
    // Platform-prefixed framework pages moved to top-level framework section
    '/platforms/business-first-ai-framework/deconstruct/': '/ai-workflow-framework/deconstruct/',
    '/platforms/business-first-ai-framework/analyze/': '/ai-workflow-framework/analyze/',
    // Removed how-to namespace — examples live under the framework now
    '/how-to/workflow-examples/autonomous-agent/': '/ai-workflow-framework/examples/autonomous-agent/',
    // Framework rename: Business-First AI Framework → AI Workflow Framework (2026-05-16)
    '/business-first-ai-framework/': '/ai-workflow-framework/',
    '/business-first-ai-framework/analyze/': '/ai-workflow-framework/analyze/',
    '/business-first-ai-framework/deconstruct/': '/ai-workflow-framework/deconstruct/',
    '/business-first-ai-framework/design/': '/ai-workflow-framework/design/',
    '/business-first-ai-framework/build/': '/ai-workflow-framework/build/',
    '/business-first-ai-framework/test/': '/ai-workflow-framework/test/',
    '/business-first-ai-framework/run/': '/ai-workflow-framework/run/',
    '/business-first-ai-framework/improve/': '/ai-workflow-framework/improve/',
    '/business-first-ai-framework/skills/': '/ai-workflow-framework/skills/',
    '/business-first-ai-framework/workflow-design-matrix/': '/ai-workflow-framework/workflow-design-matrix/',
    '/business-first-ai-framework/analyze-examples/': '/ai-workflow-framework/analyze-examples/',
    '/business-first-ai-framework/examples/deterministic-automation/': '/ai-workflow-framework/examples/deterministic-automation/',
    '/business-first-ai-framework/examples/ai-collaborative/': '/ai-workflow-framework/examples/ai-collaborative/',
    '/business-first-ai-framework/examples/autonomous-agent/': '/ai-workflow-framework/examples/autonomous-agent/',
    '/business-first-ai-framework/examples/content-calendar-planning/': '/ai-workflow-framework/examples/content-calendar-planning/',
    // Q&A flattened to /questions/<slug>/ (2026-05-17) — see redirects block below for all old nested paths
    '/business-first-ai-framework/questions/how-do-i-find-workflows-worth-applying-ai-to/': '/questions/how-do-i-find-workflows-worth-applying-ai-to/',
    '/business-first-ai-framework/questions/how-do-i-identify-the-right-ai-tools-for-a-workflow/': '/questions/how-do-i-identify-the-right-ai-tools-for-a-workflow/',
    '/ai-workflow-framework/questions/how-do-i-find-workflows-worth-applying-ai-to/': '/questions/how-do-i-find-workflows-worth-applying-ai-to/',
    '/ai-workflow-framework/questions/how-do-i-identify-the-right-ai-tools-for-a-workflow/': '/questions/how-do-i-identify-the-right-ai-tools-for-a-workflow/',
    '/agentic-building-blocks/mcp/questions/how-do-i-connect-an-mcp-server-to-claude-code/': '/questions/how-do-i-connect-an-mcp-server-to-claude-code/',
    '/agentic-building-blocks/prompts/questions/what-is-a-system-prompt/': '/questions/what-is-a-system-prompt/',
    '/agentic-building-blocks/skills/questions/do-plugin-skills-conflict-with-custom-skills/': '/questions/do-plugin-skills-conflict-with-custom-skills/',
    '/agentic-building-blocks/skills/questions/what-is-the-difference-between-a-skill-and-an-agent-in-claude-code/': '/questions/what-is-the-difference-between-a-skill-and-an-agent-in-claude-code/',
    '/courses/questions/corporate-ai-training/': '/questions/corporate-ai-training/',
    '/platforms/claude/questions/': '/questions/',
    '/platforms/claude/questions/how-do-i-schedule-an-automated-claude-subagent/': '/questions/how-do-i-schedule-an-automated-claude-subagent/',
    '/platforms/claude/questions/what-is-the-best-way-to-name-claude-agent-skills/': '/questions/what-is-the-best-way-to-name-claude-agent-skills/',
    '/platforms/google-gemini/questions/': '/questions/',
    '/platforms/openai/questions/': '/questions/',
    // Legacy builder-setup pages consolidated
    '/builder-setup/cli/': '/builder-setup/',
    '/builder-setup/ai-platforms/': '/builder-setup/',
    // Legacy feed URL
    '/feed/rss_created.xml': '/rss.xml',
    // Agents pages moved to building-blocks section
    '/platforms/claude/agents/building-agents/': '/agentic-building-blocks/agents/',
    '/platforms/openai/agents/building-agents/': '/agentic-building-blocks/agents/',
    // Skills subpage consolidated — now lands on the global Q&A hub
    '/agentic-building-blocks/skills/questions/': '/questions/',
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
        { icon: 'github', label: 'GitHub', href: 'https://github.com/jamesgray-ai/handsonai' },
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
        Footer: './src/components/QuestionPageFooter.astro',
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
                { label: 'The Hands-on AI Plugin', link: '/use-the-playbook/build/handsonai/' },
                { label: 'Example Gallery', link: '/use-cases/example-gallery/' },
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
        { label: 'Q&A', link: '/questions/' },
        {
          label: 'AI Workflow Framework',
          collapsed: true,
          items: [
            { label: 'Overview', link: '/ai-workflow-framework/' },
            { label: 'AI Workflow Design Matrix', link: '/ai-workflow-framework/workflow-design-matrix/' },
            { label: 'Step 1: Analyze', link: '/ai-workflow-framework/analyze/' },
            { label: 'Step 2: Deconstruct', link: '/ai-workflow-framework/deconstruct/' },
            { label: 'Step 3: Design', link: '/ai-workflow-framework/design/' },
            { label: 'Step 4: Build', link: '/ai-workflow-framework/build/' },
            { label: 'Step 5: Test', link: '/ai-workflow-framework/test/' },
            { label: 'Step 6: Run', link: '/ai-workflow-framework/run/' },
            { label: 'Step 7: Improve', link: '/ai-workflow-framework/improve/' },
            { label: 'Set Up the Skills', link: '/ai-workflow-framework/skills/' },
            {
              label: 'Worked Examples',
              collapsed: true,
              items: [
                { label: 'End-to-End: All 7 Steps & Files', link: '/ai-workflow-framework/examples/worked-example/' },
                { label: 'Analyze: Example Reports', link: '/ai-workflow-framework/analyze-examples/' },
                { label: 'Deterministic Automation', link: '/ai-workflow-framework/examples/deterministic-automation/' },
                { label: 'AI Collaborative', link: '/ai-workflow-framework/examples/ai-collaborative/' },
                { label: 'Autonomous Agent', link: '/ai-workflow-framework/examples/autonomous-agent/' },
                { label: 'Full Example: Content Calendar Planning', link: '/ai-workflow-framework/examples/content-calendar-planning/' },
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
                  ],
                },
                {
                  label: 'Skills',
                  collapsed: true,
                  items: [
                    { label: 'Overview', link: '/agentic-building-blocks/skills/' },
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
            { label: 'Content Creation', link: '/use-cases/content-creation/' },
            { label: 'Research', link: '/use-cases/research/' },
            {
              label: 'Coding',
              collapsed: true,
              items: [
                { label: 'Overview', link: '/use-cases/coding/' },
                { label: 'Agentic Coding', link: '/use-cases/agentic-coding/' },
              ],
            },
            { label: 'Data Analysis', link: '/use-cases/data-analysis/' },
            { label: 'Ideation & Strategy', link: '/use-cases/ideation-and-strategy/' },
            { label: 'Automation', link: '/use-cases/automation/' },
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
                { label: 'Cowork', link: '/platforms/claude/cowork/' },
                { label: 'Claude Projects', link: '/platforms/claude/projects/claude-projects-setup/' },
                {
                  label: 'CLI',
                  collapsed: true,
                  items: [
                    { label: 'Claude Code', link: '/platforms/claude/cli/' },
                  ],
                },
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
                    { label: 'Installing Skills on Claude', link: '/platforms/claude/skills/installing-skills/' },
                    { label: 'Find Your Skill Candidates (Quick Prompt)', link: '/platforms/claude/skills/find-skill-candidates/' },
                    { label: 'Discover Your Best Claude Skills (Worksheet)', link: '/platforms/claude/skills/skills-discovery-meta-prompt/' },
                    { label: 'Resources', link: '/platforms/claude/skills/resources/' },
                  ],
                },
                { label: 'Topics', link: '/platforms/claude/topics/' },
                { label: 'Resources', link: '/platforms/claude/topics/resources/' },
              ],
            },
            {
              label: 'Cursor',
              collapsed: true,
              items: [
                { label: 'Overview', link: '/platforms/cursor/' },
                {
                  label: 'Skills',
                  collapsed: true,
                  items: [
                    { label: 'Skills on Cursor', link: '/platforms/cursor/skills/' },
                  ],
                },
              ],
            },
            {
              label: 'Google Gemini',
              collapsed: true,
              items: [
                { label: 'Overview', link: '/platforms/google-gemini/' },
                { label: 'Getting Started', link: '/platforms/google-gemini/getting-started/' },
                {
                  label: 'CLI',
                  collapsed: true,
                  items: [
                    { label: 'Gemini CLI', link: '/platforms/google-gemini/cli/' },
                  ],
                },
                { label: 'Building Agents on Google', link: '/platforms/google-gemini/agents/building-agents/' },
                {
                  label: 'Skills',
                  collapsed: true,
                  items: [
                    { label: 'Skills on Google Gemini', link: '/platforms/google-gemini/skills/' },
                  ],
                },
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
                {
                  label: 'Skills',
                  collapsed: true,
                  items: [
                    { label: 'Skills on M365 Copilot', link: '/platforms/m365-copilot/skills/' },
                  ],
                },
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
                {
                  label: 'CLI',
                  collapsed: true,
                  items: [
                    { label: 'Codex CLI', link: '/platforms/openai/cli/' },
                  ],
                },
                { label: 'Building Agents on OpenAI', link: '/platforms/openai/agents/building-agents/' },
                {
                  label: 'Skills',
                  collapsed: true,
                  items: [
                    { label: 'Skills on OpenAI', link: '/platforms/openai/skills/' },
                  ],
                },
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
            { label: 'AI Registry', link: '/builder-setup/ai-registry-setup/' },
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
            { label: 'Framework End-to-End Exercise', link: '/courses/framework-end-to-end/' },
            { label: 'Agentic AI for Leaders', link: '/courses/leaders/' },
            { label: 'Claude for Builders', link: '/courses/builders/' },
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
    sitemap({
      // Q&A pages are high-value canonical answers; signal that to crawlers.
      serialize(item) {
        const url = new URL(item.url);
        if (url.pathname === '/questions/') {
          item.priority = 1.0;
          item.changefreq = 'weekly';
        } else if (url.pathname.startsWith('/questions/')) {
          item.priority = 0.9;
          item.changefreq = 'weekly';
        }
        return item;
      },
    }),
    llmsTxt(),
  ],
});
