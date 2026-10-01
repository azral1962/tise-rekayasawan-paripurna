import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const modules = process.env.CODEX_PRIMARY_RUNTIME_NODE_MODULES;
let sharp;
try { sharp = modules ? require(path.join(modules, 'sharp')) : require('sharp'); }
catch { throw new Error('Konversi membutuhkan sharp: npm install --no-save sharp'); }
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const files = new Set();
for (const folder of ['chapters', 'appendices']) {
  for (const name of await fs.readdir(path.join(root, folder))) {
    if (!name.endsWith('.qmd')) continue;
    const text = await fs.readFile(path.join(root, folder, name), 'utf8');
    for (const match of text.matchAll(/!\[[^\]]*\]\(([^)]+\.png)\)/g)) {
      files.add(path.resolve(root, folder, match[1]).replace(/\.png$/, '.svg'));
    }
  }
}
for (const file of files) {
  // Preserve spaces between Mermaid's nested text spans during SVG rasterization.
  const svg = (await fs.readFile(file, 'utf8')).replace('<svg ', '<svg xml:space="preserve" ');
  await sharp(Buffer.from(svg), { density: 300 })
    .flatten({ background: '#ffffff' }).png().toFile(file.replace(/\.svg$/, '.png'));
  console.log(path.relative(root, file));
}
console.log('Selesai: ' + files.size + ' gambar PNG.');
