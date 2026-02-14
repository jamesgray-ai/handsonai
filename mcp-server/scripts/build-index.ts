/**
 * Builds content-index.json from docs/ markdown files.
 * Run with: npx tsx scripts/build-index.ts
 */

import fs from "node:fs";
import path from "node:path";
import { glob } from "glob";
import matter from "gray-matter";
import type { Page } from "../src/types.js";

const DOCS_DIR = path.resolve(import.meta.dirname, "../../docs");
const OUTPUT_FILE = path.resolve(import.meta.dirname, "../content-index.json");
const SITE_URL = "https://handsonai.info";

// Map directory prefixes to section IDs
const SECTION_MAP: Record<string, string> = {
  "business-first-ai-framework": "framework",
  "agentic-building-blocks": "building-blocks",
  "use-cases": "use-cases",
  "platforms": "platforms",
  "plugins": "plugins",
  "builder-setup": "builder-setup",
  "patterns": "patterns",
  "courses": "courses",
  "ai-engineering": "ai-engineering",
  "resources": "resources",
  "blog": "blog",
};

const SECTION_LABELS: Record<string, string> = {
  framework: "Business-First AI Framework",
  "building-blocks": "Agentic Building Blocks",
  "use-cases": "Use Cases",
  platforms: "Platforms",
  plugins: "Plugins",
  "builder-setup": "Builder Stack Setup",
  patterns: "Patterns",
  courses: "Courses",
  "ai-engineering": "AI Engineering",
  resources: "Resources",
  blog: "Blog",
  general: "General",
};

function getSection(filePath: string): string {
  const firstDir = filePath.split("/")[0];
  return SECTION_MAP[firstDir] ?? "general";
}

function getUrl(filePath: string): string {
  // Remove index.md → directory URL, remove .md → page URL
  let urlPath = filePath;
  if (urlPath.endsWith("/index.md")) {
    urlPath = urlPath.replace(/\/index\.md$/, "/");
  } else if (urlPath === "index.md") {
    urlPath = "";
  } else {
    urlPath = urlPath.replace(/\.md$/, "/");
  }
  return `${SITE_URL}/${urlPath}`;
}

function getPagePath(filePath: string): string {
  // Remove .md and index suffixes for a clean path identifier
  let p = filePath;
  if (p.endsWith("/index.md")) {
    p = p.replace(/\/index\.md$/, "");
  } else if (p === "index.md") {
    p = "home";
  } else {
    p = p.replace(/\.md$/, "");
  }
  return p;
}

function extractTitle(data: Record<string, unknown>, content: string): string {
  if (typeof data.title === "string") return data.title;
  if (typeof data.question === "string") return data.question;
  // Fall back to first heading
  const match = content.match(/^#\s+(.+)$/m);
  return match ? match[1] : "Untitled";
}

function stripMkDocsSyntax(content: string): string {
  let result = content;

  // Strip admonitions: !!! type "title" or ??? type "title"
  // Keep the content but remove the directive syntax
  result = result.replace(
    /^(!{3}|\?{3})\s+\w+(?:\s+"[^"]*")?\s*\n((?:    .+\n?)*)/gm,
    (_match, _prefix, body: string) => {
      return body.replace(/^    /gm, "") + "\n";
    }
  );

  // Strip tab syntax: === "Tab Title"
  result = result.replace(/^===\s+"[^"]*"\s*$/gm, "");

  // Strip attribute lists: { .class #id }
  result = result.replace(/\{\s*[.#][^}]+\}/g, "");

  // Strip emoji shortcodes: :material-xxx: :fontawesome-xxx:
  result = result.replace(
    /:(?:material|fontawesome|octicons|simple)-[a-z0-9-]+:/g,
    ""
  );

  // Strip HTML comments
  result = result.replace(/<!--[\s\S]*?-->/g, "");

  // Strip snippet includes: --8<--
  result = result.replace(/^--8<--.*$/gm, "");

  // Collapse multiple blank lines
  result = result.replace(/\n{3,}/g, "\n\n");

  return result.trim();
}

async function main() {
  const files = await glob("**/*.md", {
    cwd: DOCS_DIR,
    ignore: [
      "overrides/**",
      "_templates/**",
      "assets/**",
      "blog/.authors.yml",
    ],
  });

  console.log(`Found ${files.length} markdown files`);

  const pages: Page[] = [];
  const sectionCounts: Record<string, number> = {};

  for (const file of files.sort()) {
    try {
      const fullPath = path.join(DOCS_DIR, file);
      const raw = fs.readFileSync(fullPath, "utf-8");
      const { data, content } = matter(raw);

      const section = getSection(file);
      const title = extractTitle(data, content);
      const description =
        typeof data.description === "string" ? data.description : "";
      const cleanContent = stripMkDocsSyntax(content);

      const page: Page = {
        path: getPagePath(file),
        title,
        description,
        section,
        content: cleanContent,
        url: getUrl(file),
      };

      // Preserve Q&A frontmatter
      if (typeof data.question === "string") {
        page.question = data.question;
      }
      if (typeof data.short_answer === "string") {
        page.short_answer = data.short_answer;
      }

      pages.push(page);
      sectionCounts[section] = (sectionCounts[section] ?? 0) + 1;
    } catch (err) {
      console.error(`Error processing ${file}:`, err);
      process.exit(1);
    }
  }

  const sections: Record<string, { label: string; count: number }> = {};
  for (const [id, count] of Object.entries(sectionCounts)) {
    sections[id] = {
      label: SECTION_LABELS[id] ?? id,
      count,
    };
  }

  const index = {
    generatedAt: new Date().toISOString(),
    pageCount: pages.length,
    pages,
    sections,
  };

  fs.writeFileSync(OUTPUT_FILE, JSON.stringify(index, null, 2));
  console.log(
    `Content index written to ${OUTPUT_FILE} (${pages.length} pages)`
  );
  console.log("Sections:", sections);
}

main().catch((err) => {
  console.error("Build failed:", err);
  process.exit(1);
});
