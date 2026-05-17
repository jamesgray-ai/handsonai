import type { APIRoute } from 'astro';
import { getCollection } from 'astro:content';

export async function getStaticPaths() {
  const entries = await getCollection('docs', (e: any) => {
    return e.id.startsWith('questions/') && !/^questions\/index\.(md|mdx)$/.test(e.id);
  });
  return entries.map((e: any) => {
    const raw = typeof e.slug === 'string' && e.slug
      ? e.slug
      : String(e.id || '').replace(/\.(md|mdx)$/, '');
    const slug = raw.replace(/^questions\//, '');
    return {
      params: { slug },
      props: {
        question: e.data?.question || e.data?.title || slug,
      },
    };
  });
}

function escapeXml(s: string): string {
  return s.replace(/[<>&'"]/g, (c) => ({
    '<': '&lt;',
    '>': '&gt;',
    '&': '&amp;',
    "'": '&apos;',
    '"': '&quot;',
  }[c] as string));
}

function wrapText(text: string, maxCharsPerLine: number): string[] {
  const words = text.split(/\s+/);
  const lines: string[] = [];
  let current = '';
  for (const w of words) {
    const candidate = current ? `${current} ${w}` : w;
    if (candidate.length > maxCharsPerLine && current) {
      lines.push(current);
      current = w;
    } else {
      current = candidate;
    }
  }
  if (current) lines.push(current);
  return lines;
}

export const GET: APIRoute = ({ props }) => {
  const question = String(props.question || '').trim();
  const rawLines = wrapText(question, 30);
  const lines = rawLines.slice(0, 4);
  if (rawLines.length > 4) lines[3] = lines[3].replace(/[.,;:!?]?\s*$/, '…');
  const lineHeight = 80;
  const blockHeight = lines.length * lineHeight;
  const startY = 200 + (320 - blockHeight) / 2;
  const tspans = lines
    .map((line, i) => `<tspan x="80" dy="${i === 0 ? 0 : lineHeight}">${escapeXml(line)}</tspan>`)
    .join('');
  const svg = `<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0b0f17"/>
      <stop offset="100%" stop-color="#1a2540"/>
    </linearGradient>
  </defs>
  <rect width="1200" height="630" fill="url(#bg)"/>
  <text x="80" y="100" font-family="Inter, system-ui, sans-serif" font-size="32" fill="#7dd3fc" font-weight="600">Hands-on AI Playbook · Q&amp;A</text>
  <text font-family="Inter, system-ui, sans-serif" font-size="64" fill="#ffffff" font-weight="700" y="${startY}">${tspans}</text>
  <text x="80" y="560" font-family="Inter, system-ui, sans-serif" font-size="28" fill="#94a3b8">handsonai.info</text>
  <text x="80" y="600" font-family="Inter, system-ui, sans-serif" font-size="22" fill="#64748b">Curated by James Gray · AI instructor at UC Berkeley</text>
</svg>`;
  return new Response(svg, {
    headers: {
      'Content-Type': 'image/svg+xml; charset=utf-8',
      'Cache-Control': 'public, max-age=31536000, immutable',
    },
  });
};
