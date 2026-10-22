// Copies the docs content and data that live at the repository root into the
// places Astro and Starlight expect them. Runs automatically before `dev` and
// `build`; run `npm run sync` to pick up content edits while `astro dev` runs.
//
//   <repo>/<section>/**       -> site/src/content/docs/<section>/**
//   <repo>/data/*.json        -> site/src/data/*.json
//
// Both destinations are gitignored copies; edit the originals at the repo root.
import { cpSync, existsSync, mkdirSync, readdirSync, rmSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const SECTIONS = ['infrastructure', 'security-stack', 'projects', 'lessons-learned', 'addons'];

const siteDir = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const repoRoot = resolve(siteDir, '..');

function fail(message) {
  console.error(`[sync-content] ${message}`);
  process.exit(1);
}

const docsDir = join(siteDir, 'src', 'content', 'docs');
for (const section of SECTIONS) {
  const from = join(repoRoot, section);
  if (!existsSync(from)) fail(`missing ${from}; is it included in the Docker build context?`);
  const to = join(docsDir, section);
  rmSync(to, { recursive: true, force: true });
  cpSync(from, to, { recursive: true });
}

const dataFrom = join(repoRoot, 'data');
if (!existsSync(dataFrom)) fail(`missing ${dataFrom}`);
const dataTo = join(siteDir, 'src', 'data');
rmSync(dataTo, { recursive: true, force: true });
mkdirSync(dataTo, { recursive: true });
const dataFiles = readdirSync(dataFrom).filter((file) => file.endsWith('.json'));
for (const file of dataFiles) cpSync(join(dataFrom, file), join(dataTo, file));

console.log(`[sync-content] copied ${SECTIONS.join(', ')} and data/{${dataFiles.join(',')}} into site/src`);
