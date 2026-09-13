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
const approvals = JSON.parse(fs.readFileSync(path.join(here, 'pilot_approved_questions.json'), 'utf8'));
const manifest = JSON.parse(fs.readFileSync(path.join(bank, 'manifest.json'), 'utf8'));
const entries = [...manifest.files.map(file => ({path: file.path, kind: 'file', content: file.path.startsWith('images/') ? new Uint8Array(fs.readFileSync(path.join(bank, file.path))) : fs.readFileSync(path.join(bank, file.path), 'utf8')})), {path: 'manifest.json', kind: 'file', content: fs.readFileSync(path.join(bank, 'manifest.json'), 'utf8')}];
const imported = model.importRepoEntriesToAppData(entries);
const existing = new Set(imported.appData.questions.map(question => question.id));
const createdAt = Date.UTC(2026, 8, 12, 0, 0, 0);
for (const item of approvals.questions) {
  if (existing.has(item.id)) throw new Error(`Question already exists in working bank: ${item.id}`);
  imported.appData.questions.push({id: item.id, body: item.body, solution: item.solution, points: item.points, tags: item.tags, images: [], questionType: 'frq', createdAt, updatedAt: createdAt});
}
const generated = model.exportAppDataToRepoEntries(imported.appData);
const existingReadme = fs.readFileSync(path.join(bank, 'README.md'), 'utf8');
const readme = generated.find(entry => entry.path === 'README.md');
readme.content = existingReadme.replace('Current status: initialized; 0 published questions.', 'Current status: 6 manually reviewed, figure-free FRQ pilot questions published. Six diagram-dependent pilot questions remain in review.');
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
console.log(JSON.stringify({questions: checked.appData.questions.length, added: approvals.questions.length, images: checked.appData.images?.length ?? 0, import: 'passed', roundtrip: 'passed', output}));
