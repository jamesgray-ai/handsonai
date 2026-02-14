import type {
  ContentIndex,
  Page,
  McpToolDefinition,
  McpResourceDefinition,
} from "./types.js";
import { searchPages } from "./search.js";

const MAX_CONTENT_LENGTH = 50_000;

const VALID_SECTIONS = [
  "building-blocks",
  "framework",
  "use-cases",
  "patterns",
  "platforms",
  "builder-setup",
  "plugins",
  "ai-engineering",
  "resources",
  "courses",
  "blog",
  "general",
];

const BUILDING_BLOCKS = [
  "model",
  "prompts",
  "context",
  "projects",
  "skills",
  "agents",
  "mcp",
];

const FRAMEWORK_STEPS = ["discover", "deconstruct", "build"];

const SETUP_TOOLS: Record<string, string> = {
  terminal: "builder-setup/terminal-basics",
  editor: "builder-setup/editor-setup",
  git: "builder-setup/git-install",
  github: "builder-setup/github-setup",
  "claude-code": "builder-setup/claude-code-install",
  registry: "builder-setup/notion-registry-setup",
  "voice-to-text": "builder-setup/voice-to-text-setup",
};

/** All tool definitions exposed via tools/list. */
export const TOOL_DEFINITIONS: McpToolDefinition[] = [
  {
    name: "search_cookbook",
    description:
      "Search the Hands-on AI Cookbook for pages matching a keyword query. Returns matching pages ranked by relevance with title, description, URL, and section.",
    inputSchema: {
      type: "object",
      properties: {
        query: {
          type: "string",
          description: "Search keywords (e.g. 'prompt engineering', 'MCP setup', 'workflow automation')",
        },
        section: {
          type: "string",
          description: `Optional section filter: ${VALID_SECTIONS.join(", ")}`,
          enum: VALID_SECTIONS,
        },
      },
      required: ["query"],
    },
    annotations: {
      readOnlyHint: true,
      destructiveHint: false,
      idempotentHint: true,
      openWorldHint: false,
    },
  },
  {
    name: "get_page",
    description:
      "Get the full markdown content of a specific cookbook page by its path. Use search_cookbook first to find the right path.",
    inputSchema: {
      type: "object",
      properties: {
        path: {
          type: "string",
          description:
            'Page path (e.g. "agentic-building-blocks/prompts", "use-cases/content-creation")',
        },
      },
      required: ["path"],
    },
    annotations: {
      readOnlyHint: true,
      destructiveHint: false,
      idempotentHint: true,
      openWorldHint: false,
    },
  },
  {
    name: "list_section",
    description:
      "List all pages in a cookbook section. Returns titles, descriptions, and paths for browsing.",
    inputSchema: {
      type: "object",
      properties: {
        section: {
          type: "string",
          description: `Section to browse: ${VALID_SECTIONS.join(", ")}`,
          enum: VALID_SECTIONS,
        },
      },
      required: ["section"],
    },
    annotations: {
      readOnlyHint: true,
      destructiveHint: false,
      idempotentHint: true,
      openWorldHint: false,
    },
  },
  {
    name: "get_building_block",
    description:
      "Get detailed content for an agentic building block and all its sub-pages. Building blocks are: model, prompts, context, projects, skills, agents, mcp.",
    inputSchema: {
      type: "object",
      properties: {
        name: {
          type: "string",
          description: `Building block name: ${BUILDING_BLOCKS.join(", ")}`,
          enum: BUILDING_BLOCKS,
        },
      },
      required: ["name"],
    },
    annotations: {
      readOnlyHint: true,
      destructiveHint: false,
      idempotentHint: true,
      openWorldHint: false,
    },
  },
  {
    name: "get_framework_step",
    description:
      "Get detailed content for a Business-First AI Framework step and all its sub-pages. Steps are: discover, deconstruct, build.",
    inputSchema: {
      type: "object",
      properties: {
        step: {
          type: "string",
          description: `Framework step: ${FRAMEWORK_STEPS.join(", ")}`,
          enum: FRAMEWORK_STEPS,
        },
      },
      required: ["step"],
    },
    annotations: {
      readOnlyHint: true,
      destructiveHint: false,
      idempotentHint: true,
      openWorldHint: false,
    },
  },
  {
    name: "list_questions",
    description:
      "List all Q&A pages in the cookbook. Each entry includes the question, short answer, section, and URL. Useful for quick answers.",
    inputSchema: {
      type: "object",
      properties: {
        section: {
          type: "string",
          description: "Optional section filter",
          enum: VALID_SECTIONS,
        },
      },
    },
    annotations: {
      readOnlyHint: true,
      destructiveHint: false,
      idempotentHint: true,
      openWorldHint: false,
    },
  },
  {
    name: "get_setup_guide",
    description:
      "Get a specific Builder Stack Setup guide with step-by-step instructions. Tools: terminal, editor, git, github, claude-code, registry, voice-to-text.",
    inputSchema: {
      type: "object",
      properties: {
        tool: {
          type: "string",
          description: `Setup tool: ${Object.keys(SETUP_TOOLS).join(", ")}`,
          enum: Object.keys(SETUP_TOOLS),
        },
      },
      required: ["tool"],
    },
    annotations: {
      readOnlyHint: true,
      destructiveHint: false,
      idempotentHint: true,
      openWorldHint: false,
    },
  },
];

/** The cookbook://index resource definition. */
export const RESOURCE_DEFINITION: McpResourceDefinition = {
  uri: "cookbook://index",
  name: "Cookbook Site Index",
  description:
    "Full site map of the Hands-on AI Cookbook with title, description, path, and section for every page",
  mimeType: "application/json",
};

// ── Tool handlers ──

function findPage(index: ContentIndex, pagePath: string): Page | undefined {
  return index.pages.find((p) => p.path === pagePath);
}

function formatPageSummary(page: Page): string {
  return `**${page.title}** — ${page.description || "(no description)"}\nPath: ${page.path} | URL: ${page.url}`;
}

function formatPageFull(page: Page): string {
  const header = [
    `# ${page.title}`,
    page.description ? `> ${page.description}` : "",
    `Section: ${page.section} | URL: ${page.url}`,
    "---",
  ]
    .filter(Boolean)
    .join("\n");
  return `${header}\n\n${page.content}`;
}

type ToolResult = { content: Array<{ type: string; text: string }>; isError?: boolean };

function requireString(args: Record<string, unknown>, key: string): string | ToolResult {
  const val = args[key];
  if (typeof val !== "string" || !val) {
    return { content: [{ type: "text", text: `Missing or invalid parameter: "${key}" must be a non-empty string.` }], isError: true };
  }
  return val;
}

function optionalString(args: Record<string, unknown>, key: string): string | undefined | ToolResult {
  const val = args[key];
  if (val === undefined || val === null) return undefined;
  if (typeof val !== "string") {
    return { content: [{ type: "text", text: `Invalid parameter: "${key}" must be a string.` }], isError: true };
  }
  return val;
}

export function handleToolCall(
  toolName: string,
  args: Record<string, unknown>,
  index: ContentIndex
): ToolResult {
  switch (toolName) {
    case "search_cookbook": {
      const query = requireString(args, "query");
      if (typeof query !== "string") return query;
      const section = optionalString(args, "section");
      if (section !== undefined && typeof section !== "string") return section;
      const results = searchPages(index.pages, query, section);
      if (results.length === 0) {
        return text(`No results found for "${query}".`);
      }
      const lines = results.map(
        (r, i) =>
          `${i + 1}. **${r.title}** (score: ${r.score})\n   ${r.description || "(no description)"}\n   Path: \`${r.path}\` | Section: ${r.section}\n   ${r.url}`
      );
      return text(
        `Found ${results.length} results for "${query}":\n\n${lines.join("\n\n")}`
      );
    }

    case "get_page": {
      const pagePath = requireString(args, "path");
      if (typeof pagePath !== "string") return pagePath;
      const page = findPage(index, pagePath);
      if (!page) {
        // Suggest similar paths
        const suggestions = index.pages
          .filter((p) => p.path.includes(pagePath) || pagePath.includes(p.path))
          .slice(0, 5);
        const hint = suggestions.length
          ? `\n\nDid you mean:\n${suggestions.map((s) => `- ${s.path}`).join("\n")}`
          : "\n\nUse search_cookbook to find the correct path.";
        return text(`Page not found: "${pagePath}".${hint}`);
      }
      return text(formatPageFull(page));
    }

    case "list_section": {
      const section = requireString(args, "section");
      if (typeof section !== "string") return section;
      const pages = index.pages.filter((p) => p.section === section);
      if (pages.length === 0) {
        return text(
          `No pages found in section "${section}". Valid sections: ${VALID_SECTIONS.join(", ")}`
        );
      }
      const sectionInfo = index.sections[section];
      const header = `# ${sectionInfo?.label ?? section} (${pages.length} pages)\n`;
      const lines = pages.map((p) => `- ${formatPageSummary(p)}`);
      return text(`${header}\n${lines.join("\n\n")}`);
    }

    case "get_building_block": {
      const name = requireString(args, "name");
      if (typeof name !== "string") return name;
      // Models has a different directory name
      const dirName = name === "model" ? "models" : name;
      const prefix = `agentic-building-blocks/${dirName}`;
      const pages = index.pages.filter(
        (p) => p.path === prefix || p.path.startsWith(`${prefix}/`)
      );
      if (pages.length === 0) {
        return text(
          `Building block "${name}" not found. Valid: ${BUILDING_BLOCKS.join(", ")}`
        );
      }
      return text(
        truncateMultiPage(`# Building Block: ${name}`, pages, prefix)
      );
    }

    case "get_framework_step": {
      const step = requireString(args, "step");
      if (typeof step !== "string") return step;
      const prefix = `business-first-ai-framework/${step}`;
      const pages = index.pages.filter(
        (p) =>
          p.path === prefix ||
          p.path.startsWith(`${prefix}/`) ||
          // "discover" is a single page, not a directory
          (step === "discover" &&
            p.path === "business-first-ai-framework/discover")
      );
      if (pages.length === 0) {
        return text(
          `Framework step "${step}" not found. Valid: ${FRAMEWORK_STEPS.join(", ")}`
        );
      }
      return text(
        truncateMultiPage(`# Framework Step: ${step}`, pages, prefix)
      );
    }

    case "list_questions": {
      const section = optionalString(args, "section");
      if (section !== undefined && typeof section !== "string") return section;
      let questions = index.pages.filter((p) => p.question);
      if (section) {
        questions = questions.filter((p) => p.section === section);
      }
      if (questions.length === 0) {
        return text("No Q&A pages found.");
      }
      const lines = questions.map(
        (q) =>
          `**Q: ${q.question}**\nA: ${q.short_answer || "(see full page)"}\nSection: ${q.section} | Path: \`${q.path}\`\n${q.url}`
      );
      return text(
        `# Cookbook Q&A (${questions.length} questions)\n\n${lines.join("\n\n---\n\n")}`
      );
    }

    case "get_setup_guide": {
      const tool = requireString(args, "tool");
      if (typeof tool !== "string") return tool;
      const pagePath = SETUP_TOOLS[tool];
      if (!pagePath) {
        return text(
          `Unknown setup tool "${tool}". Valid: ${Object.keys(SETUP_TOOLS).join(", ")}`
        );
      }
      const page = findPage(index, pagePath);
      if (!page) {
        return text(`Setup guide for "${tool}" not found in index.`);
      }
      return text(formatPageFull(page));
    }

    default:
      return {
        content: [{ type: "text", text: `Unknown tool: "${toolName}". Available: ${TOOL_DEFINITIONS.map(t => t.name).join(", ")}` }],
        isError: true,
      };
  }
}

/** Handle reading a resource by URI. */
export function handleResourceRead(
  uri: string,
  index: ContentIndex
): { contents: Array<{ uri: string; mimeType: string; text: string }> } {
  if (uri === "cookbook://index") {
    const siteMap = index.pages.map((p) => ({
      path: p.path,
      title: p.title,
      description: p.description,
      section: p.section,
      url: p.url,
    }));
    return {
      contents: [
        {
          uri,
          mimeType: "application/json",
          text: JSON.stringify(siteMap, null, 2),
        },
      ],
    };
  }
  throw new Error(`Unknown resource: ${uri}`);
}

/** Sort pages so overview/index pages come first, then key sequential pages. */
function sortPagesForDisplay(prefix: string, pages: Page[]): Page[] {
  return [...pages].sort((a, b) => {
    const pa = getPagePriority(prefix, a.path);
    const pb = getPagePriority(prefix, b.path);
    return pa - pb;
  });
}

function getPagePriority(prefix: string, pagePath: string): number {
  if (!prefix || !pagePath) return 10;
  // Overview page (exact match with the prefix) comes first
  if (pagePath === prefix) return 0;
  const lastSegment = pagePath.split("/").pop() ?? "";
  if (lastSegment === "design") return 1;
  if (lastSegment === "run") return 2;
  return 10;
}

/** Concatenate multi-page content with truncation if too large. */
function truncateMultiPage(heading: string, pages: Page[], prefix: string): string {
  const sorted = sortPagesForDisplay(prefix, pages);
  const parts: string[] = [];
  let totalLength = 0;
  let truncated = false;

  for (const page of sorted) {
    const formatted = formatPageFull(page);
    if (totalLength + formatted.length > MAX_CONTENT_LENGTH && parts.length > 0) {
      truncated = true;
      break;
    }
    parts.push(formatted);
    totalLength += formatted.length;
  }

  let result = `${heading} (${pages.length} pages)\n\n${parts.join("\n\n---\n\n")}`;
  if (truncated) {
    const remaining = sorted.slice(parts.length);
    result += `\n\n---\n\n(${remaining.length} more pages truncated. Use get_page to read individually: ${remaining.map((p) => p.path).join(", ")})`;
  }
  return result;
}

function text(
  content: string
): { content: Array<{ type: string; text: string }> } {
  return { content: [{ type: "text", text: content }] };
}
