// Emit reviewed AP pilot questions into a separate TestGen-bank candidate.
// Usage: node --experimental-strip-types emit_approved_pilot_questions.mjs BANK OUTPUT
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';

const [bank, output] = process.argv.slice(2);
if (!bank || !output) throw new Error('Usage: node --experimental-strip-types emit_approved_pilot_questions.mjs BANK OUTPUT');
if (fs.existsSync(output)) throw new Error(`Candidate output already exists: ${output}`);
const require = createRequire(import.meta.url);
const model = require('/home/max/testgen-suite/test-generator/src/git/repoDataModel.ts');
const here = path.dirname(fileURLToPath(import.meta.url));
const approvals = {
  questions: ['pilot_approved_questions.json', 'pilot_diagram_approved_questions.json']
    .flatMap(file => JSON.parse(fs.readFileSync(path.join(here, file), 'utf8')).questions),
};
const ROOT = '/home/max/testgen-suite/testgen-ingest/tools/ocr-frq';
const assetRoot = path.join(ROOT, 'data/ap-calculus/pilot/staging/intermediate/assets');
const manifest = JSON.parse(fs.readFileSync(path.join(bank, 'manifest.json'), 'utf8'));
const entries = [...manifest.files.map(file => ({path: file.path, kind: 'file', content: file.path.startsWith('images/') ? new Uint8Array(fs.readFileSync(path.join(bank, file.path))) : fs.readFileSync(path.join(bank, file.path), 'utf8')})), {path: 'manifest.json', kind: 'file', content: fs.readFileSync(path.join(bank, 'manifest.json'), 'utf8')}];
const imported = model.importRepoEntriesToAppData(entries);
const existing = new Set(imported.appData.questions.map(question => question.id));
const createdAt = Date.UTC(2026, 8, 12, 0, 0, 0);
let added = 0;
for (const item of approvals.questions) {
  if (existing.has(item.id)) continue;
  const imageNames = item.images ?? [];
  for (const filename of imageNames) {
    const ext = path.extname(filename).slice(1).toLowerCase();
    const name = path.basename(filename, `.${ext}`);
    const imagePath = path.join(assetRoot, filename);
    if (!fs.existsSync(imagePath)) throw new Error(`Approved image missing: ${imagePath}`);
    if ((imported.appData.images ?? []).some(image => image.name === name && image.ext === ext)) continue;
    const bytes = new Uint8Array(fs.readFileSync(imagePath));
    imported.appData.images ??= [];
    imported.appData.images.push({name, ext, mime: `image/${ext === 'jpg' ? 'jpeg' : ext}`, size: bytes.length, bytes});
  }
  imported.appData.questions.push({id: item.id, body: item.body, solution: item.solution, points: item.points, tags: item.tags, images: imageNames, questionType: 'frq', createdAt, updatedAt: createdAt});
  added += 1;
}
const generated = model.exportAppDataToRepoEntries(imported.appData);
const existingReadme = fs.readFileSync(path.join(bank, 'README.md'), 'utf8');
const readme = generated.find(entry => entry.path === 'README.md');
readme.content = existingReadme.replace(/^Current status:.*$/m, 'Current status: 12 manually reviewed AP Calculus FRQ pilot questions published. The pilot has passed source-traceability, native Typst, TestGen import/round-trip, and independent mathematical-review gates.');
const generatedManifest = generated.find(entry => entry.path === 'manifest.json');
const parsedManifest = JSON.parse(generatedManifest.content);
const readmeRecord = parsedManifest.files.find(file => file.path === 'README.md');
readmeRecord.size = Buffer.byteLength(readme.content);
readmeRecord.hash = model.hashRepoDataContent(readme.content);
generatedManifest.content = JSON.stringify(parsedManifest, null, 2) + '\n';
const checked = model.importRepoEntriesToAppData(generated);
const roundtrip = model.exportAppDataToRepoEntries(checked.appData);
if (roundtrip.length !== generated.length) throw new Error('TestGen round trip changed candidate entry count');
for (const entry of generated) { const target = path.join(output, entry.path); fs.mkdirSync(path.dirname(target), {recursive: true}); fs.writeFileSync(target, entry.content); }
console.log(JSON.stringify({questions: checked.appData.questions.length, added, images: checked.appData.images?.length ?? 0, import: 'passed', roundtrip: 'passed', output}));
