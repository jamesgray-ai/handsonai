import { promises as fs } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { parse as parseYaml } from 'yaml';

const SITE_ORIGIN = 'https://handsonai.info';
const QUESTIONS_DIR_REL = 'src/content/docs/questions';
const USE_CASES_DIR_REL = 'src/content/docs/use-cases';

function splitFrontmatter(raw) {
  if (!raw.startsWith('---')) return { data: {}, body: raw };
  const end = raw.indexOf('\n---', 3);
  if (end === -1) return { data: {}, body: raw };
  const yamlBlock = raw.slice(3, end).trim();
  const body = raw.slice(end + 4).replace(/^\r?\n/, '');
  let data = {};
  try { data = parseYaml(yamlBlock) ?? {}; } catch { data = {}; }
  return { data, body };
}

function mdToPlainText(md) {
  return md
    .replace(/^import\s+.*?from\s+['"][^'"]+['"];?\s*$/gm, '')
    .replace(/^export\s+.*?;?\s*$/gm, '')
    .replace(/\{\/\*[\s\S]*?\*\/\}/g, ' ')
    .replace(/```[\s\S]*?```/g, ' ')
    .replace(/`([^`]+)`/g, '$1')
    .replace(/<[^>]+>/g, ' ')
    .replace(/!\[([^\]]*)\]\([^)]*\)/g, '$1')
    .replace(/\[([^\]]+)\]\([^)]*\)/g, '$1')
    .replace(/^\s{0,3}#{1,6}\s+/gm, '')
    .replace(/^[-*+]\s+/gm, '')
    .replace(/^>\s?/gm, '')
    .replace(/\*\*([^*]+)\*\*/g, '$1')
    .replace(/\*([^*]+)\*/g, '$1')
    .replace(/_{1,2}([^_]+)_{1,2}/g, '$1')
    .replace(/^\s*[-=]{3,}\s*$/gm, '')
    .replace(/[ \t]+/g, ' ')
    .replace(/\n{3,}/g, '\n\n')
    .trim();
}

async function loadQuestions(projectRoot) {
  const dir = path.join(projectRoot, QUESTIONS_DIR_REL);
  const files = await fs.readdir(dir);
  const out = [];
  for (const filename of files) {
    if (!filename.endsWith('.md')) continue;
    if (filename === 'index.md' || filename === 'index.mdx') continue;
    const slug = filename.replace(/\.md$/, '');
    const raw = await fs.readFile(path.join(dir, filename), 'utf8');
    const { data, body } = splitFrontmatter(raw);
    out.push({
      slug,
      url: `${SITE_ORIGIN}/questions/${slug}/`,
      title: data.question || data.title || slug,
      shortAnswer: data.short_answer || data.description || '',
      body: mdToPlainText(body),
    });
  }
  out.sort((a, b) => a.title.localeCompare(b.title));
  return out;
}

async function loadUseCases(projectRoot) {
  // Flat use case files only — files at /use-cases/<slug>.mdx, not under a primitive subfolder.
  const dir = path.join(projectRoot, USE_CASES_DIR_REL);
  const entries = await fs.readdir(dir, { withFileTypes: true });
  const out = [];
  for (const dirent of entries) {
    if (!dirent.isFile()) continue;
    const filename = dirent.name;
    if (!filename.endsWith('.mdx') && !filename.endsWith('.md')) continue;
    if (/^index\.(md|mdx)$/.test(filename)) continue;
    if (filename === 'example-gallery.md') continue;
    const slug = filename.replace(/\.(md|mdx)$/, '');
    const raw = await fs.readFile(path.join(dir, filename), 'utf8');
    const { data, body } = splitFrontmatter(raw);
    if (data.status === 'draft') continue;
    out.push({
      slug,
      url: `${SITE_ORIGIN}/use-cases/${slug}/`,
      title: data.title || slug,
      question: data.question || '',
      shortAnswer: data.short_answer || data.jtbd || data.description || '',
      primitives: Array.isArray(data.primitives) ? data.primitives : [],
      body: mdToPlainText(body),
    });
  }
  out.sort((a, b) => a.title.localeCompare(b.title));
  return out;
}

function renderLlmsTxt(questions, useCases) {
  const lines = [];
  lines.push('# Hands-on AI Playbook');
  lines.push('');
  lines.push('> Short, authoritative answers and worked use cases from James Gray. Q&A entries and use cases each have a canonical URL with structured FAQPage data.');
  lines.push('');
  lines.push(`Q&A hub: ${SITE_ORIGIN}/questions/`);
  lines.push(`Use case library: ${SITE_ORIGIN}/use-cases/`);
  lines.push('');
  lines.push('## Questions');
  lines.push('');
  for (const q of questions) {
    lines.push(`- [${q.title}](${q.url}): ${q.shortAnswer}`);
  }
  lines.push('');
  if (useCases.length > 0) {
    lines.push('## Use Cases');
    lines.push('');
    for (const uc of useCases) {
      const tag = uc.primitives.length ? ` [${uc.primitives.join(', ')}]` : '';
      const summary = uc.shortAnswer ? `: ${uc.shortAnswer}` : '';
      lines.push(`- [${uc.title}](${uc.url})${tag}${summary}`);
    }
    lines.push('');
  }
  return lines.join('\n');
}

function renderLlmsFullTxt(questions, useCases) {
  const lines = [];
  lines.push('# Hands-on AI Playbook — full text');
  lines.push('');
  lines.push('> Full plain-text answers and use case walkthroughs from handsonai.info. Authored by James Gray; please cite the canonical URL.');
  lines.push('');
  lines.push(`Q&A hub: ${SITE_ORIGIN}/questions/`);
  lines.push(`Use case library: ${SITE_ORIGIN}/use-cases/`);
  lines.push('');
  lines.push('# Questions');
  lines.push('');
  for (const q of questions) {
    lines.push('---');
    lines.push('');
    lines.push(`## ${q.title}`);
    lines.push('');
    lines.push(`URL: ${q.url}`);
    lines.push('');
    if (q.shortAnswer) {
      lines.push(`**Short answer:** ${q.shortAnswer}`);
      lines.push('');
    }
    lines.push(q.body);
    lines.push('');
  }
  if (useCases.length > 0) {
    lines.push('# Use Cases');
    lines.push('');
    for (const uc of useCases) {
      lines.push('---');
      lines.push('');
      lines.push(`## ${uc.title}`);
      lines.push('');
      lines.push(`URL: ${uc.url}`);
      if (uc.primitives.length) {
        lines.push(`Primitives: ${uc.primitives.join(', ')}`);
      }
      lines.push('');
      if (uc.question) {
        lines.push(`**Question:** ${uc.question}`);
        lines.push('');
      }
      if (uc.shortAnswer) {
        lines.push(`**Short answer:** ${uc.shortAnswer}`);
        lines.push('');
      }
      lines.push(uc.body);
      lines.push('');
    }
  }
  return lines.join('\n');
}

export default function llmsTxtIntegration() {
  return {
    name: 'llms-txt-generator',
    hooks: {
      'astro:build:done': async ({ dir, logger }) => {
        try {
          const outDir = fileURLToPath(dir);
          const projectRoot = path.resolve(outDir, '..');
          const [questions, useCases] = await Promise.all([
            loadQuestions(projectRoot),
            loadUseCases(projectRoot),
          ]);
          await fs.writeFile(path.join(outDir, 'llms.txt'), renderLlmsTxt(questions, useCases), 'utf8');
          await fs.writeFile(path.join(outDir, 'llms-full.txt'), renderLlmsFullTxt(questions, useCases), 'utf8');
          logger.info(`Wrote llms.txt and llms-full.txt with ${questions.length} questions and ${useCases.length} use cases.`);
        } catch (err) {
          logger.error(`llms-txt-generator failed: ${err instanceof Error ? err.message : String(err)}`);
          throw err;
        }
      },
    },
  };
}
