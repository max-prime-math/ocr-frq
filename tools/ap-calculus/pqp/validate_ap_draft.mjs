#!/usr/bin/env node
// Run with node --experimental-strip-types. Uses the checked-out TestGen code.
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { spawn } from 'node:child_process';
import { createHash } from 'node:crypto';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../..');
const args = process.argv.slice(2);
function option(name, fallback) {
  const i = args.indexOf(name);
  if (i < 0) return fallback;
  if (!args[i + 1] || args[i + 1].startsWith('--')) throw new Error(`Missing ${name} value`);
  return args[i + 1];
}
if (args.includes('--help')) {
  console.log('node --experimental-strip-types tools/ap-calculus/pqp/validate_ap_draft.mjs [--product DIR] [--inventory FILE] [--testgen DIR] [--workers 4] [--skip-compile]');
  process.exit(0);
}
const product = path.resolve(option('--product', path.join(root, 'data/ap-calculus/draft/product')));
const inventoryPath = path.resolve(option('--inventory', path.join(product, '../source-inventory.json')));
const testgen = path.resolve(option('--testgen', path.join(root, '../test-generator')));
const workers = Math.max(1, Math.min(8, Number(option('--workers', '4')) || 4));
const reportDir = path.join(product, 'validation');
fs.mkdirSync(reportDir, { recursive: true });
const report = {
  generatedAt: new Date().toISOString(), product, inventoryPath, testgen,
  status: 'running', checks: {}, compile: [], samples: [], errors: [],
  limitations: [
    'Local Typst and the actual TestGen template are exercised; this is not a browser interaction test.',
    'PQP JSON parsing normalizes question IDs away and does not install images. Use testgen-question-bank.json for the native one-file import with embedded images.',
    'Compilation and source inventory coverage cannot establish mathematical correctness or prove a source crop is visually complete. See the second-pass review queue.',
  ],
};
const writeReport = () => fs.writeFileSync(path.join(reportDir, 'validation-report.json'), JSON.stringify(report, null, 2) + '\n');
const readJson = (file) => JSON.parse(fs.readFileSync(file, 'utf8'));
const hash = (data) => createHash('sha256').update(data).digest('hex');
const sorted = (items) => [...items].sort();
function unique(items, label) {
  assert.equal(new Set(items).size, items.length, `${label}: duplicate IDs`);
}
function assertSame(actual, expected, label) {
  assert.deepEqual(sorted(actual), sorted(expected), label);
}
async function command(bin, params) {
  return await new Promise((resolve) => {
    const proc = spawn(bin, params, { cwd: product });
    let output = '';
    proc.stdout.on('data', (part) => { output += part; });
    proc.stderr.on('data', (part) => { output += part; });
    proc.on('error', (error) => resolve({ status: -1, output: error.message }));
    proc.on('close', (status) => resolve({ status, output: output.slice(-12000) }));
  });
}
try {
  const { parseBulkImportJson } = await import(pathToFileURL(path.join(testgen, 'src/lib/bulk-import.ts')));
  const { imageKeyFromReference } = await import(pathToFileURL(path.join(testgen, 'src/lib/image-keys.ts')));
  const model = await import(pathToFileURL(path.join(testgen, 'src/git/repoDataModel.ts')));
  const { generateTypst } = await import(pathToFileURL(path.join(testgen, 'src/lib/typst/template.ts')));
  const { defaultTestConfig } = await import(pathToFileURL(path.join(testgen, 'src/lib/types.ts')));
  const inventory = readJson(inventoryPath);
  const sourceRows = Array.isArray(inventory) ? inventory : inventory.questions;
  assert.ok(Array.isArray(sourceRows) && sourceRows.length, 'Inventory must contain questions[]');
  const expected = sourceRows.map((q) => q.id ?? q.questionId ?? q.question_id);
  assert.ok(expected.every((id) => typeof id === 'string' && id.length), 'Inventory IDs missing');
  unique(expected, 'Inventory');
  const pqpPath = path.join(product, 'ap-calculus-all-available-draft.pqp.json');
  const pqpText = fs.readFileSync(pqpPath, 'utf8');
  const pqp = JSON.parse(pqpText);
  const bankPath = path.join(product, 'testgen-question-bank.json');
  const native = readJson(bankPath);
  report.inputs = { pqpSha256: hash(pqpText), nativeSha256: hash(fs.readFileSync(bankPath)), inventorySha256: hash(fs.readFileSync(inventoryPath)) };
  const questions = native.questions;
  assert.equal(native.format, 'test-generator-question-bank');
  assert.ok(Array.isArray(questions), 'Native questions[] missing');
  unique(questions.map((q) => q.id), 'Native questions');
  unique(pqp.questions.map((q) => q.id), 'PQP questions');
  assertSame(questions.map((q) => q.id), expected, 'Native coverage differs from inventory');
  assertSame(pqp.questions.map((q) => q.id), expected, 'PQP coverage differs from inventory');
  const nativeById = new Map(questions.map((q) => [q.id, q]));
  const parsed = parseBulkImportJson(pqpText);
  assert.equal(parsed?.error, null, 'Actual TestGen PQP parser rejected package');
  assert.equal(parsed.kind, 'portable-question-package');
  assert.equal(parsed.questions.length, expected.length, 'Actual parser silently dropped questions');
  for (let i = 0; i < pqp.questions.length; i++) {
    const q = nativeById.get(pqp.questions[i].id);
    const draft = parsed.questions[i];
    assert.equal(draft.body, q.body.trim(), `${q.id} body changed across formats`);
    assert.equal(draft.solution, q.solution.trim(), `${q.id} solution changed across formats`);
    assert.equal(draft.points, q.points, `${q.id} scoring changed across formats`);
    assertSame((draft.images ?? []).map(imageKeyFromReference), (q.images ?? []).map(imageKeyFromReference), `${q.id} image references changed across formats`);
    assert.ok(q.body.trim() && q.solution.trim(), `${q.id} empty body/solution`);
    assert.ok(typeof q.points === 'number' && Array.isArray(q.tags) && Number.isFinite(q.createdAt), `${q.id} fails BankView stored-question acceptance`);
  }
  report.checks.coverage = { passed: true, expected: expected.length, pqp: pqp.questions.length, native: questions.length };
  report.checks.actualPqpParser = { passed: true, parsed: parsed.questions.length };
  const reviewedBank = path.resolve(option('--reviewed-bank', '/home/max/dev/ap-calculus-exam-banks'));
  let reviewedCount = 0;
  for (const file of fs.readdirSync(path.join(reviewedBank, 'questions')).filter((file) => file.endsWith('.json'))) {
    const original = readJson(path.join(reviewedBank, 'questions', file)).question;
    if (!original?.id) continue;
    const emitted = nativeById.get(original.id);
    assert.ok(emitted, `Reviewed record omitted: ${original.id}`);
    let body = original.body;
    if (original.id === 'ap-calc-bc-1999-frq-03' && body.startsWith('#table(\n')) {
      const split = body.indexOf('\n\n');
      body = body.slice(0, split).split('\n').map((line) => line.trim()).join(' ') + body.slice(split);
    }
    assert.equal(emitted.body, body, `${original.id}: reviewed body changed beyond documented whitespace normalization`);
    assert.equal(emitted.solution, original.solution, `${original.id}: reviewed solution changed`);
    assert.equal(emitted.points, original.points, `${original.id}: reviewed points changed`);
    reviewedCount++;
  }
  report.checks.reviewedContentPreserved = { passed: true, count: reviewedCount, compatibilityException: 'BC 1999 Q3 table whitespace only' };
  const images = native.images.map((img) => ({ ...img, bytes: new Uint8Array(Buffer.from(img.data, 'base64')) }));
  unique(images.map((img) => img.name), 'Native image keys');
  const byImage = new Map(images.map((img) => [img.name, img]));
  const referenced = new Set();
  function refs(source) {
    const result = new Set();
    for (const match of source.matchAll(/"\/imgs\/([^"\n]+)"|#?image\s*\(\s*"([^"\n]+)"/g)) {
      const key = imageKeyFromReference(match[1] ?? match[2]);
      if (key) result.add(key);
    }
    return result;
  }
  for (const q of questions) {
    const declared = new Set((q.images ?? []).map(imageKeyFromReference));
    for (const key of refs([q.body, q.solution, q.narrative, q.graphTypst, JSON.stringify(q.parts ?? {})].filter(Boolean).join('\n'))) {
      assert.ok(byImage.has(key), `${q.id}: unresolved image ${key}`);
      assert.ok(declared.has(key), `${q.id}: undeclared image ${key}`);
      referenced.add(key);
    }
    for (const key of declared) assert.ok(byImage.has(key), `${q.id}: missing declared asset ${key}`);
  }
  for (const img of images) {
    assert.ok(img.bytes.length > 0, `${img.name}: empty image`);
    assert.ok(/^(png|jpg|jpeg|svg|webp|gif|bmp|pdf)$/.test(img.ext), `${img.name}: unsupported image format`);
    const disk = path.join(product, 'imgs', `${img.name}.${img.ext}`);
    assert.deepEqual(Buffer.from(img.bytes), fs.readFileSync(disk), `${img.name}: inline and disk image bytes differ`);
    assert.ok(referenced.has(img.name), `${img.name}: orphan bundled image`);
  }
  const assetIds = pqp.assets.map((a) => a.id);
  unique(assetIds, 'PQP assets');
  const assetMap = new Map(pqp.assets.map((a) => [a.id, a]));
  for (const q of pqp.questions) for (const id of q.assets ?? []) assert.ok(assetMap.has(id), `${q.id}: unknown PQP asset ${id}`);
  report.checks.assets = { passed: true, count: images.length, referenced: referenced.size, bytes: images.reduce((n, img) => n + img.bytes.length, 0) };
  const appData = { questions, images, narratives: native.narratives ?? [], customClasses: native.customClasses ?? [], savedTests: [] };
  const exportOptions = { generatedAt: '2026-09-13T00:00:00.000Z' };
  const entries = model.exportAppDataToRepoEntries(appData, exportOptions);
  const restored = model.importRepoEntriesToAppData(entries).appData;
  const roundtrip = model.exportAppDataToRepoEntries(restored, exportOptions);
  assert.deepEqual(roundtrip.map((entry) => [entry.path, hash(entry.content)]), entries.map((entry) => [entry.path, hash(entry.content)]), 'Repo import/export changed bytes');
  for (const q of restored.questions) {
    const initial = nativeById.get(q.id);
    for (const key of ['body', 'solution', 'points', 'tags', 'images', 'classId', 'unitId', 'sectionId']) assert.deepEqual(q[key], initial[key], `${q.id}: repo roundtrip changed ${key}`);
  }
  report.checks.actualRepoRoundtrip = { passed: true, questions: restored.questions.length, images: restored.images.length, entries: entries.length, bytes: entries.reduce((n, entry) => n + Buffer.byteLength(entry.content), 0) };
  function imagePaths(source) {
    return source.replace(/"\/imgs\/([^"\n]+)"/g, (full, ref) => {
      const img = byImage.get(imageKeyFromReference(ref));
      assert.ok(img, `Unresolved render image ${ref}`);
      return `"/imgs/${img.name}.${img.ext}"`;
    });
  }
  function config(title) {
    return { ...defaultTestConfig(title), showAnswerKey: true, mcqFullSolutions: true, instructions: '', answerSpace: 0, showPoints: false, mcqFirst: false, fontSize: 10 };
  }
  const compileCachePath = path.join(reportDir, 'compile-cache.json');
  const oldCache = fs.existsSync(compileCachePath) ? readJson(compileCachePath) : {};
  const newCache = {};
  const version = await command('typst', ['--version']);
  assert.equal(version.status, 0, 'Typst unavailable');
  report.typstVersion = version.output.trim();
  async function render(name, selected) {
    const source = imagePaths(generateTypst(config(name), selected, native.narratives ?? []));
    const typ = path.join(reportDir, `${name}.typ`);
    const pdf = path.join(reportDir, `${name}.pdf`);
    fs.writeFileSync(typ, source);
    const key = hash(source + report.typstVersion + [...refs(source)].sort().map((ref) => hash(byImage.get(ref).bytes)).join(''));
    if (oldCache[name]?.key === key && fs.existsSync(pdf)) {
      newCache[name] = oldCache[name];
      return { id: name, passed: true, cached: true, pdf: path.relative(product, pdf) };
    }
    const result = await command('typst', ['compile', '--root', product, typ, pdf]);
    const row = { id: name, passed: result.status === 0, pdf: result.status === 0 ? path.relative(product, pdf) : null, ...(result.output ? { diagnostics: result.output } : {}) };
    if (row.passed) newCache[name] = { key };
    return row;
  }
  if (!args.includes('--skip-compile')) {
    let cursor = 0;
    await Promise.all(Array.from({ length: workers }, async () => {
      while (cursor < questions.length) {
        const question = questions[cursor++];
        const result = await render(question.id, [question]);
        report.compile.push(result);
        if (report.compile.length % 24 === 0) { console.log(`Compiled ${report.compile.length}/${questions.length}`); writeReport(); }
      }
    }));
    for (const course of ['ab', 'bc']) {
      const pool = questions.filter((q) => new RegExp(`(?:^|-)${course}(?:-|$)`, 'i').test(q.id));
      assert.ok(pool.length, `No ${course.toUpperCase()} questions`);
      const selected = [];
      const add = (q) => { if (q && !selected.some((row) => row.id === q.id)) selected.push(q); };
      add(pool.find((q) => refs(q.body).size > 1));
      add(pool.find((q) => refs(q.body).size > 0));
      add(pool.find((q) => !/Solution pending review/i.test(q.solution)));
      add(pool.find((q) => /2024/.test(q.id)));
      for (const q of pool) { if (selected.length >= 6) break; add(q); }
      const result = await render(`sample-${course.toUpperCase()}-exam`, selected);
      report.samples.push({ ...result, questions: selected.map((q) => q.id), multiImageQuestions: selected.filter((q) => refs(q.body).size > 1).map((q) => q.id) });
    }
    fs.writeFileSync(compileCachePath, JSON.stringify(newCache, null, 2) + '\n');
    report.compile.sort((a, b) => a.id.localeCompare(b.id));
    report.checks.actualTestGenRendering = { passed: report.compile.every((r) => r.passed) && report.samples.every((r) => r.passed), bodiesAndSolutions: report.compile.filter((r) => r.passed).length, total: questions.length, sampleExams: report.samples.filter((r) => r.passed).length };
    assert.ok(report.checks.actualTestGenRendering.passed, 'Some TestGen question/sample renders failed; see compile rows');
  } else report.checks.actualTestGenRendering = { passed: false, skipped: true };
  report.status = args.includes('--skip-compile') ? 'structural-checks-passed' : 'passed';
} catch (error) {
  report.status = 'failed';
  report.errors.push(error.stack ?? String(error));
  process.exitCode = 1;
} finally {
  writeReport();
  console.log(JSON.stringify({ status: report.status, checks: report.checks, errors: report.errors, report: path.join(reportDir, 'validation-report.json') }, null, 2));
}
