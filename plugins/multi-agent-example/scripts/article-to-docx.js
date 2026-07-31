#!/usr/bin/env node
/**
 * article-to-docx.js — render a pipeline article (markdown) as a Word document.
 *
 *   node scripts/article-to-docx.js <input.md> <output.docx>
 *
 * Used by the hbr-publisher agent as the final stage of the multi-agent article
 * pipeline. The layout lives here, in version control, rather than being improvised
 * by the agent on each run — that is what makes the demo produce the same document
 * every time.
 *
 * Supported markdown: YAML frontmatter (title, subtitle, author, date), h1-h3,
 * paragraphs, bullet and numbered lists, blockquotes (rendered as pull quotes),
 * horizontal rules, and inline bold, italic, code spans, and links.
 *
 * docx-js footguns this file deliberately works around (see the `docx` skill):
 * page size defaults to A4, `\n` inside a TextRun is ignored, bullets need a
 * numbering config rather than literal characters, and a PageBreak must sit inside
 * a Paragraph.
 */

import fs from 'node:fs';
import path from 'node:path';
import {
  AlignmentType,
  BorderStyle,
  Document,
  ExternalHyperlink,
  Footer,
  Header,
  HeadingLevel,
  LevelFormat,
  PageBreak,
  PageNumber,
  Packer,
  Paragraph,
  TextRun,
} from 'docx';

// US Letter in DXA (1440 = 1 inch). docx-js defaults to A4 without this.
const LETTER = { width: 12240, height: 15840 };
const MARGIN = 1440;

const FONT = 'Georgia';
const SANS = 'Helvetica';

// ---------------------------------------------------------------------------
// Frontmatter
// ---------------------------------------------------------------------------

function parseFrontmatter(raw) {
  const meta = {};
  if (!raw.startsWith('---')) return { meta, body: raw };

  const end = raw.indexOf('\n---', 3);
  if (end === -1) return { meta, body: raw };

  // Read only keys at the frontmatter's own indentation level.
  //
  // Anchoring to column 0 meant a uniformly indented block silently lost its `title:`
  // and shipped a document headed "Untitled". Accepting any indentation instead was
  // worse: nested keys (`author:` / `  name:` / `  title:`) then overwrote the top-level
  // ones, producing a plausible-looking wrong title AND suppressing the missing-title
  // warning. So take the indentation of the first key as the document's level and ignore
  // anything deeper — nested values belong to their parent, not to the document.
  const lines = raw.slice(4, end).split('\n');
  let baseIndent = null;

  for (const line of lines) {
    const match = line.match(/^(\s*)([A-Za-z_][\w-]*):\s*(.*)$/);
    if (!match) continue;

    const [, indent, key, value] = match;
    if (baseIndent === null) baseIndent = indent.length;
    if (indent.length > baseIndent) continue;

    meta[key.toLowerCase()] = value.trim().replace(/^["']|["']$/g, '');
  }

  const body = raw.slice(end + 4).replace(/^\n+/, '');
  return { meta, body };
}

// ---------------------------------------------------------------------------
// Inline formatting
// ---------------------------------------------------------------------------

/**
 * Convert one line of inline markdown into docx runs.
 * Handles links, bold, italic (asterisk or underscore), and code spans, including
 * emphasis nested inside link text.
 */
function inlineRuns(text, base = {}) {
  const runs = [];
  // Ordered so links win before emphasis, and ** before *.
  const pattern = /\[([^\]]+)\]\(([^)\s]+)\)|\*\*([^*]+)\*\*|__([^_]+)__|\*([^*]+)\*|(?<![A-Za-z0-9])_([^_]+)_(?![A-Za-z0-9])|`([^`]+)`/;

  let rest = text;
  while (rest.length) {
    const m = rest.match(pattern);
    if (!m) {
      runs.push(new TextRun({ text: rest, ...base }));
      break;
    }

    if (m.index > 0) {
      runs.push(new TextRun({ text: rest.slice(0, m.index), ...base }));
    }

    const [, linkText, linkHref, bold1, bold2, ital1, ital2, code] = m;

    if (linkText !== undefined) {
      runs.push(
        new ExternalHyperlink({
          link: linkHref,
          children: inlineRuns(linkText, { ...base, style: 'Hyperlink' }),
        })
      );
    } else if (bold1 !== undefined || bold2 !== undefined) {
      runs.push(new TextRun({ text: bold1 ?? bold2, bold: true, ...base }));
    } else if (ital1 !== undefined || ital2 !== undefined) {
      runs.push(new TextRun({ text: ital1 ?? ital2, italics: true, ...base }));
    } else if (code !== undefined) {
      // font AFTER the spread. Every caller passes `font: FONT` in base, so spreading it
      // last silently overrode Courier New and rendered code spans in Georgia — a valid
      // file, just wrong, which is the kind of defect nothing downstream catches.
      runs.push(new TextRun({ text: code, ...base, font: 'Courier New' }));
    }

    rest = rest.slice(m.index + m[0].length);
  }

  return runs.length ? runs : [new TextRun({ text: '', ...base })];
}

// ---------------------------------------------------------------------------
// Block parsing
// ---------------------------------------------------------------------------

/**
 * Group markdown lines into blocks. Consecutive non-blank lines form one
 * paragraph, because a hard-wrapped source line is not a new paragraph in Word.
 */
function parseBlocks(body) {
  const blocks = [];
  const lines = body.split('\n');
  let paragraph = [];

  const flush = () => {
    if (paragraph.length) {
      blocks.push({ type: 'p', text: paragraph.join(' ').trim() });
      paragraph = [];
    }
  };

  for (const raw of lines) {
    const line = raw.replace(/\s+$/, '');

    if (!line.trim()) {
      flush();
      continue;
    }

    const heading = line.match(/^(#{1,6})\s+(.*)$/);
    if (heading) {
      flush();
      blocks.push({ type: 'h', level: heading[1].length, text: heading[2].trim() });
      continue;
    }

    if (/^(-{3,}|\*{3,}|_{3,})$/.test(line.trim())) {
      flush();
      blocks.push({ type: 'hr' });
      continue;
    }

    const quote = line.match(/^>\s?(.*)$/);
    if (quote) {
      flush();
      const previous = blocks[blocks.length - 1];
      if (previous && previous.type === 'quote') {
        previous.text += ' ' + quote[1].trim();
      } else {
        blocks.push({ type: 'quote', text: quote[1].trim() });
      }
      continue;
    }

    const bullet = line.match(/^\s*[-*+]\s+(.*)$/);
    if (bullet) {
      flush();
      blocks.push({ type: 'bullet', text: bullet[1].trim() });
      continue;
    }

    const numbered = line.match(/^\s*\d+[.)]\s+(.*)$/);
    if (numbered) {
      flush();
      blocks.push({ type: 'number', text: numbered[1].trim() });
      continue;
    }

    paragraph.push(line.trim());
  }

  flush();
  numberOrderedLists(blocks);
  return blocks;
}

// Give every ordered list its own counter.
//
// docx keys a concrete numbering instance by `${reference}-${instance}`, and `instance`
// defaults to 0. So every numbered paragraph sharing one reference also shares one
// running counter: an article with "Three Steps" followed later by "Five Metrics"
// renders the second list as 4, 5, 6 instead of restarting at 1. There is no error and
// the file is still valid — it is just visibly wrong in the delivered document.
//
// A list ends wherever a non-`number` block interrupts it, which is why this runs after
// parsing rather than during it.
function numberOrderedLists(blocks) {
  let instance = 0;
  let inList = false;
  for (const block of blocks) {
    if (block.type === 'number') {
      if (!inList) {
        instance += 1;
        inList = true;
      }
      block.instance = instance;
    } else {
      inList = false;
    }
  }
}

// ---------------------------------------------------------------------------
// Rendering
// ---------------------------------------------------------------------------

const HEADING_FOR = {
  1: HeadingLevel.HEADING_1,
  2: HeadingLevel.HEADING_1,
  3: HeadingLevel.HEADING_2,
  4: HeadingLevel.HEADING_3,
  5: HeadingLevel.HEADING_3,
  6: HeadingLevel.HEADING_3,
};

function titlePage(meta) {
  const children = [];

  children.push(
    new Paragraph({
      spacing: { before: 2400, after: 240 },
      children: [
        new TextRun({ text: meta.title || 'Untitled', bold: true, size: 60, font: FONT }),
      ],
    })
  );

  if (meta.subtitle || meta.description) {
    children.push(
      new Paragraph({
        spacing: { after: 480 },
        children: [
          new TextRun({
            text: meta.subtitle || meta.description,
            italics: true,
            size: 28,
            font: FONT,
            color: '444444',
          }),
        ],
      })
    );
  }

  children.push(
    new Paragraph({
      spacing: { after: 120 },
      border: { top: { style: BorderStyle.SINGLE, size: 6, color: 'BBBBBB', space: 8 } },
      children: [new TextRun({ text: '', size: 2 })],
    })
  );

  if (meta.author) {
    children.push(
      new Paragraph({
        spacing: { before: 240, after: 80 },
        children: [new TextRun({ text: `By ${meta.author}`, size: 24, font: SANS })],
      })
    );
  }

  if (meta.date) {
    children.push(
      new Paragraph({
        children: [new TextRun({ text: meta.date, size: 22, font: SANS, color: '666666' })],
      })
    );
  }

  children.push(new Paragraph({ children: [new PageBreak()] }));
  return children;
}

function renderBlocks(blocks) {
  return blocks.map((block) => {
    switch (block.type) {
      case 'h':
        return new Paragraph({
          // Built-in heading styles keep Word's navigation pane and TOC working;
          // explicit run properties override the default blue without losing that.
          heading: HEADING_FOR[block.level],
          spacing: { before: 360, after: 160 },
          keepNext: true,
          children: inlineRuns(block.text, {
            font: FONT,
            color: '1A1A1A',
            size: block.level <= 2 ? 30 : 25,
          }),
        });

      case 'quote':
        return new Paragraph({
          spacing: { before: 240, after: 240 },
          indent: { left: 720, right: 720 },
          border: { left: { style: BorderStyle.SINGLE, size: 18, color: 'AAAAAA', space: 12 } },
          children: inlineRuns(block.text, { italics: true, size: 26, font: FONT, color: '333333' }),
        });

      case 'bullet':
        return new Paragraph({
          numbering: { reference: 'article-bullets', level: 0 },
          spacing: { after: 80 },
          children: inlineRuns(block.text, { size: 22, font: FONT }),
        });

      case 'number':
        return new Paragraph({
          numbering: { reference: 'article-numbers', level: 0, instance: block.instance || 1 },
          spacing: { after: 80 },
          children: inlineRuns(block.text, { size: 22, font: FONT }),
        });

      case 'hr':
        return new Paragraph({
          spacing: { before: 240, after: 240 },
          border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: 'CCCCCC', space: 8 } },
          children: [new TextRun({ text: '', size: 2 })],
        });

      default:
        return new Paragraph({
          spacing: { before: 80, after: 200, line: 300 },
          alignment: AlignmentType.LEFT,
          children: inlineRuns(block.text, { size: 22, font: FONT }),
        });
    }
  });
}

function build(meta, blocks) {
  return new Document({
    creator: meta.author || 'Hands-On AI',
    title: meta.title || 'Article',
    description: meta.subtitle || meta.description || '',
    numbering: {
      config: [
        {
          reference: 'article-bullets',
          levels: [
            {
              level: 0,
              format: LevelFormat.BULLET,
              text: '•',
              alignment: AlignmentType.LEFT,
              style: { paragraph: { indent: { left: 720, hanging: 360 } } },
            },
          ],
        },
        {
          reference: 'article-numbers',
          levels: [
            {
              level: 0,
              format: LevelFormat.DECIMAL,
              text: '%1.',
              alignment: AlignmentType.START,
              style: { paragraph: { indent: { left: 720, hanging: 360 } } },
            },
          ],
        },
      ],
    },
    sections: [
      {
        properties: {
          page: { size: LETTER, margin: { top: MARGIN, right: MARGIN, bottom: MARGIN, left: MARGIN } },
          titlePage: true,
        },
        headers: {
          default: new Header({
            children: [
              new Paragraph({
                alignment: AlignmentType.RIGHT,
                children: [
                  new TextRun({
                    text: meta.title || '',
                    size: 18,
                    font: SANS,
                    color: '888888',
                  }),
                ],
              }),
            ],
          }),
          // Suppressed on the title page by `titlePage: true`.
          first: new Header({ children: [new Paragraph({ children: [] })] }),
        },
        footers: {
          default: new Footer({
            children: [
              new Paragraph({
                alignment: AlignmentType.CENTER,
                children: [
                  new TextRun({ children: [PageNumber.CURRENT], size: 18, font: SANS, color: '888888' }),
                ],
              }),
            ],
          }),
          first: new Footer({ children: [new Paragraph({ children: [] })] }),
        },
        children: [...titlePage(meta), ...renderBlocks(blocks)],
      },
    ],
  });
}

// ---------------------------------------------------------------------------
// Entry point
// ---------------------------------------------------------------------------

async function main() {
  const [input, output] = process.argv.slice(2);

  if (!input || !output) {
    console.error('Usage: node scripts/article-to-docx.js <input.md> <output.docx>');
    process.exit(1);
  }

  if (!fs.existsSync(input)) {
    console.error(`Input not found: ${input}`);
    process.exit(1);
  }

  const raw = fs.readFileSync(input, 'utf8');
  const { meta, body } = parseFrontmatter(raw);
  const blocks = parseBlocks(body);

  // A leading h1 is the article title, not a body heading — promote it and drop it
  // so the title is not printed twice.
  if (!meta.title && blocks.length && blocks[0].type === 'h' && blocks[0].level === 1) {
    meta.title = blocks.shift().text;
  } else if (blocks.length && blocks[0].type === 'h' && blocks[0].level === 1 && blocks[0].text === meta.title) {
    blocks.shift();
  }

  if (!blocks.length) {
    console.error('Nothing to render — the input has no body content.');
    process.exit(1);
  }

  warnAboutUnsupported(body, meta, input);

  const buffer = await Packer.toBuffer(build(meta, blocks));
  fs.mkdirSync(path.dirname(path.resolve(output)), { recursive: true });
  fs.writeFileSync(output, buffer);

  console.log(`Wrote ${output} (${blocks.length} blocks, ${(buffer.length / 1024).toFixed(1)} KB)`);
}

// Say out loud what this renderer cannot do.
//
// It supports a deliberate subset of markdown, and everything outside that subset is
// reinterpreted rather than rejected: a table becomes a paragraph of literal pipe
// characters, a fenced code block loses its indentation and newlines, an image becomes a
// link. Each of those produces a structurally valid .docx, so the pipeline's quality gate
// passes it and the damaged document becomes the deliverable. A warning does not fix the
// output — it makes the loss visible to whoever can.
function warnAboutUnsupported(body, meta, input) {
  const unsupported = [
    [/^\s*\|.*\|\s*$/m, 'a markdown table (rendered as literal text, not a table)'],
    [/^\s*```/m, 'a fenced code block (indentation and line breaks will be lost)'],
    [/!\[[^\]]*\]\(/, 'an image (rendered as a link — images are not embedded)'],
  ];

  for (const [pattern, description] of unsupported) {
    if (pattern.test(body)) {
      console.error(`WARNING: ${input} contains ${description}.`);
    }
  }

  if (!meta.title) {
    console.error(`WARNING: ${input} has no title in its frontmatter — the document will be titled "Untitled".`);
  }
}

main().catch((error) => {
  // stack, not message: `message` is undefined for anything thrown that is not an Error,
  // which prints the literal string "undefined" and loses the failure entirely.
  console.error(error?.stack || error);
  process.exit(1);
});
