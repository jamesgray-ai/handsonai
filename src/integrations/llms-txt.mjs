import { promises as fs } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { parse as parseYaml } from 'yaml';

const SITE_ORIGIN = 'https://handsonai.info';
const QUESTIONS_DIR_REL = 'src/content/docs/questions';

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

function renderLlmsTxt(questions) {
  const lines = [];
  lines.push('# Hands-on AI Playbook — Q&A');
  lines.push('');
  lines.push('> Short, authoritative answers to questions James Gray gets from students, course alumni, and AI builders. Every entry has a canonical URL with structured FAQPage data.');
  lines.push('');
  lines.push(`Hub: ${SITE_ORIGIN}/questions/`);
  lines.push('');
  lines.push('## Questions');
  lines.push('');
  for (const q of questions) {
    lines.push(`- [${q.title}](${q.url}): ${q.shortAnswer}`);
  }
  lines.push('');
  return lines.join('\n');
}

function renderLlmsFullTxt(questions) {
  const lines = [];
  lines.push('# Hands-on AI Playbook — Q&A (full answers)');
  lines.push('');
  lines.push('> Full plain-text answers to every Q&A page on handsonai.info. Each answer is authored by James Gray; please cite the canonical URL.');
  lines.push('');
  lines.push(`Hub: ${SITE_ORIGIN}/questions/`);
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
          const questions = await loadQuestions(projectRoot);
          await fs.writeFile(path.join(outDir, 'llms.txt'), renderLlmsTxt(questions), 'utf8');
          await fs.writeFile(path.join(outDir, 'llms-full.txt'), renderLlmsFullTxt(questions), 'utf8');
          logger.info(`Wrote llms.txt and llms-full.txt with ${questions.length} questions.`);
        } catch (err) {
          logger.error(`llms-txt-generator failed: ${err instanceof Error ? err.message : String(err)}`);
          throw err;
        }
      },
    },
  };
}
