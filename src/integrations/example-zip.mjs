import { promises as fs } from 'node:fs';
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import JSZip from 'jszip';

// Zips the worked-example project folder into the build output so students can
// download the finished seven-step run. The folder (examples/weekly-status-report)
// is canonical and verified by scripts/test-compose-registry.sh; this file only
// packages it. Only git-tracked files ship (no editor backups or derived views),
// entries are added in sorted order with a fixed timestamp so the same commit
// always produces a byte-identical zip.

const EXAMPLE = 'weekly-status-report';
const FIXED_DATE = new Date('2026-10-08T00:00:00Z');

export async function buildExampleZip(repoRoot) {
  const folder = path.join(repoRoot, 'examples', EXAMPLE);
  try { await fs.access(folder); }
  catch { throw new Error(`example-zip: folder missing: ${folder}`); }
  let tracked;
  try {
    tracked = execFileSync('git', ['ls-files', '-z', '--', `examples/${EXAMPLE}`], { cwd: repoRoot })
      .toString('utf8').split('\0').filter(Boolean).sort();
  } catch (err) {
    throw new Error(`example-zip: git ls-files failed for examples/${EXAMPLE}: ${err.message}`);
  }
  if (tracked.length === 0) throw new Error(`example-zip: no tracked files under ${folder} — is the folder missing or ignored?`);
  const zip = new JSZip();
  for (const rel of tracked) {
    const inside = rel.replace(`examples/${EXAMPLE}/`, '');
    let data;
    try { data = await fs.readFile(path.join(repoRoot, rel)); }
    catch (err) { throw new Error(`example-zip: cannot read ${rel}: ${err.message}`); }
    // createFolders: false — implicit folder entries would carry the build time and break byte-identical output.
    zip.file(`${EXAMPLE}/${inside}`, data, { date: FIXED_DATE, createFolders: false });
  }
  const buffer = await zip.generateAsync({ type: 'nodebuffer', compression: 'DEFLATE', compressionOptions: { level: 9 } });
  return { buffer, count: tracked.length };
}

export default function exampleZip() {
  return {
    name: 'example-zip',
    hooks: {
      'astro:build:done': async ({ dir, logger }) => {
        const started = Date.now();
        const repoRoot = path.resolve(fileURLToPath(new URL('../../', import.meta.url)));
        const { buffer, count } = await buildExampleZip(repoRoot);
        const outFile = path.join(fileURLToPath(dir), 'assets', 'examples', `${EXAMPLE}.zip`);
        await fs.mkdir(path.dirname(outFile), { recursive: true });
        await fs.writeFile(outFile, buffer);
        logger.info(`Wrote assets/examples/${EXAMPLE}.zip (${count} files, ${Math.round(buffer.length / 1024)} KB, ${Date.now() - started} ms)`);
      },
    },
  };
}
