#!/usr/bin/env node
// Independent snapshot export: never overwrite a bank the user may have edited.
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';
import { createHash } from 'node:crypto';
import { stripTypeScriptTypes } from 'node:module';
import { fileURLToPath, pathToFileURL } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../..');
const args = process.argv.slice(2);
function option(name, fallback) {
  const index = args.indexOf(name);
  if (index === -1) return fallback;
  assert.ok(args[index + 1] && !args[index + 1].startsWith('--'), `Missing value for ${name}`);
  return path.resolve(args[index + 1]);
}
if (args.includes('--help')) {
  console.log('node --experimental-strip-types tools/ap-calculus/pqp/export_ap_local_folder.mjs [--input FILE] [--output NEW_FOLDER] [--testgen DIR]');
  process.exit(0);
}
const input = option('--input', path.join(root, 'data/ap-calculus/draft/product/testgen-question-bank.json'));
const output = option('--output', path.join(root, 'data/ap-calculus/draft/ap-calculus-local-bank'));
const testgen = option('--testgen', path.join(root, '../test-generator'));
const reportPath = `${output}-validation.json`;
assert.ok(!fs.existsSync(output), `Refusing to overwrite existing bank: ${output}. Choose a new --output folder.`);
assert.ok(!fs.existsSync(reportPath), `Refusing to overwrite existing report: ${reportPath}`);
const bytes = fs.readFileSync(input);
const bank = JSON.parse(bytes);
assert.equal(bank.format, 'test-generator-question-bank');
assert.ok(bank.questions.length > 0 && Array.isArray(bank.images));
const sha256 = (value) => createHash('sha256').update(value).digest('hex');
const current = await import(pathToFileURL(path.join(testgen, 'src/git/repoDataModel.ts')));

// This is the actual last schema-1 implementation, not a hand-written downgrade.
// Type-only imports disappear; APP_VERSION is metadata, supplied explicitly below.
const legacyRevision = 'bd2acc1';
let { stdout: legacySource } = await promisify(execFile)('git', ['-C', testgen, 'show', `${legacyRevision}:src/git/repoDataModel.ts`], { encoding: 'utf8' });
assert.ok(legacySource.includes("import { APP_VERSION } from '../lib/version.ts';"));
legacySource = legacySource.replace("import { APP_VERSION } from '../lib/version.ts';", 'const APP_VERSION = null;');
const legacy = await import(`data:text/javascript;base64,${Buffer.from(stripTypeScriptTypes(legacySource)).toString('base64')}`);
assert.equal(legacy.REPO_DATA_SCHEMA_VERSION, 1);
const source = {
  questions: bank.questions,
  images: bank.images.map(({ name, ext, data }) => ({ name, ext, bytes: new Uint8Array(Buffer.from(data, 'base64')) })),
  narratives: bank.narratives ?? [],
  customClasses: bank.customClasses ?? [],
  savedTests: [],
};
assert.equal(new Set(source.questions.map((q) => q.id)).size, source.questions.length);
assert.equal(new Set(source.images.map((img) => img.name)).size, source.images.length);
const options = { generatedAt: bank.exportedAt ?? new Date().toISOString(), appVersion: null };
const entries = legacy.exportAppDataToRepoEntries(source, options);
const readme = entries.find((entry) => entry.path === 'README.md');
// Unreviewed native drafts: editable prompt (no full-prompt source crop) with a placeholder solution.
const nativeDraftCount = source.questions.filter((question) => !(question.images ?? []).some((name) => name.includes('-source-'))
  && question.solution.startsWith('Solution pending review')).length;
const draftDescription = nativeDraftCount
  ? `${nativeDraftCount} prompts use editable OCR text and figure assets. OCR correctness and diagram completeness still need review. Placeholder solutions remain unreviewed.`
  : 'Source-image prompts and placeholder solutions remain drafts; do not treat them as reviewed native OCR.';
readme.content = `# AP Calculus — local-folder first draft\n\nOpen this folder itself with TestGen's Local Folder workflow.\nIt includes ${source.questions.length} questions and ${source.images.length} image files; no separate image upload is needed.\n\nSchema 1 is intentional for compatibility with older TestGen builds.\nThe required tests/index.json is empty: no saved tests or student data are included.\n\nQuestion content matches the source draft package. ${draftDescription}\n\nThis is an independent snapshot, not a live link to the generated PQP/JSON.\nKeep user edits here; future exports must use a new folder.\n`;
const manifestEntry = entries.find((entry) => entry.path === 'manifest.json');
const manifest = JSON.parse(manifestEntry.content);
const readmeRow = manifest.files.find((entry) => entry.path === 'README.md');
readmeRow.size = legacy.repoDataContentByteLength(readme.content);
readmeRow.hash = legacy.hashRepoDataContent(readme.content);
manifestEntry.content = JSON.stringify(manifest, null, 2) + '\n';

function verify(restored, label) {
  const byId = new Map(restored.questions.map((q) => [q.id, q]));
  assert.equal(byId.size, source.questions.length, `${label}: question count`);
  for (const q of source.questions) {
    const actual = byId.get(q.id);
    assert.ok(actual, `${label}: missing ${q.id}`);
    for (const key of ['body', 'solution', 'points', 'tags', 'images', 'classId', 'unitId', 'sectionId', 'parts', 'questionType', 'createdAt', 'updatedAt']) {
      assert.deepEqual(actual[key], q[key], `${label}: changed ${q.id}.${key}`);
    }
  }
  const byImage = new Map(restored.images.map((img) => [img.name, img]));
  assert.equal(byImage.size, source.images.length, `${label}: image count`);
  for (const img of source.images) {
    assert.equal(byImage.get(img.name)?.ext, img.ext, `${label}: image extension`);
    assert.deepEqual(Buffer.from(byImage.get(img.name).bytes), Buffer.from(img.bytes), `${label}: image bytes ${img.name}`);
  }
  assert.deepEqual(restored.customClasses, legacy.importRepoEntriesToAppData(entries).appData.customClasses);
}
verify(legacy.importRepoEntriesToAppData(entries).appData, 'historical schema-1 importer');
const modernImport = current.importRepoEntriesToAppData(entries);
verify(modernImport.appData, 'current importer');
// Saved tests moved from legacyMigration into appData in newer TestGen builds.
assert.deepEqual(modernImport.appData.savedTests ?? modernImport.legacyMigration?.savedTests, []);

// Write only after the complete in-memory folder passes both importers.
fs.mkdirSync(output, { recursive: false });
for (const entry of entries) {
  const destination = path.resolve(output, entry.path);
  assert.ok(destination.startsWith(output + path.sep), 'Unsafe generated path');
  fs.mkdirSync(path.dirname(destination), { recursive: true });
  fs.writeFileSync(destination, entry.content, { flag: 'wx' });
}
const diskEntries = entries.map((entry) => {
  const content = fs.readFileSync(path.join(output, entry.path));
  assert.equal(sha256(content), sha256(entry.content), `Disk bytes differ: ${entry.path}`);
  return { ...entry, content: entry.path.startsWith('images/') ? new Uint8Array(content) : content.toString('utf8') };
});
verify(legacy.importRepoEntriesToAppData(diskEntries).appData, 'on-disk legacy import');
verify(current.importRepoEntriesToAppData(diskEntries).appData, 'on-disk current import');
const report = {
  status: 'passed', generatedAt: new Date().toISOString(), input, inputSha256: sha256(bytes),
  output, schemaVersion: 1, legacyRevision,
  questions: source.questions.length, images: source.images.length, files: entries.length,
  bytes: entries.reduce((sum, entry) => sum + Buffer.byteLength(entry.content), 0),
  checks: ['historical schema-1 importer', 'current importer', 'all question content preserved', 'all image bytes preserved', 'manifest sizes and hashes', 'on-disk folder re-import', 'empty saved-tests migration'],
  limitations: ['Browser Local Folder click-through not performed.', 'Source draft content and its review limitations are unchanged.', 'Independent snapshot: future exports do not overwrite user edits.'],
};
fs.writeFileSync(reportPath, JSON.stringify(report, null, 2) + '\n', { flag: 'wx' });
console.log(JSON.stringify(report, null, 2));
