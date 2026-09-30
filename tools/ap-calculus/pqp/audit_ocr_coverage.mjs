#!/usr/bin/env node
// Count saved OCR evidence, NOT submission attempts or screenshot placeholders.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createHash } from 'node:crypto';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../..');
const read = file => JSON.parse(fs.readFileSync(file, 'utf8'));
const inventory = read(path.join(root, 'data/ap-calculus/draft/source-inventory.json'));
const rows = new Map(inventory.questions.map(q => [q.id, {
  id: q.id, course: q.course, year: q.year,
  promptOcrEvidence: [], scoringOcrEvidence: [], intermediateRecords: [],
  typstCandidates: [], stagedSourceMapsMatchInventory: false,
}]));
const sources = new Map(inventory.questions.map(q => [q.id, q.source]));
const relative = file => path.relative(root, file);
const sha = content => createHash('sha256').update(content).digest('hex');
const errors = [];
function scan(directory) {
  for (const entry of fs.readdirSync(directory, { withFileTypes: true })) {
    const file = path.join(directory, entry.name);
    if (entry.isDirectory()) { scan(file); continue; }
    const isCandidate = file.includes('/typst-candidates/') || file.includes('/native-pass/candidates/');
    if (!entry.name.endsWith('.json') || (!file.includes('/intermediate/records/') && !isCandidate && entry.name !== 'manifest.json')) continue;
    let record;
    try { record = read(file); } catch (error) { errors.push({ path: relative(file), error: error.message }); continue; }
    const row = rows.get(record.id);
    if (row) {
      if (typeof record.rawPrompt === 'string' && record.rawPrompt.trim()) {
        row.promptOcrEvidence.push({ type: 'rawPrompt', path: relative(file), characters: record.rawPrompt.length, textSha256: sha(record.rawPrompt) });
        row.intermediateRecords.push(relative(file));
        if (JSON.stringify(record.source?.promptPages) === JSON.stringify(sources.get(record.id).promptPages)
          && record.source?.prompt?.sha256 === sources.get(record.id).prompt.sha256) row.stagedSourceMapsMatchInventory = true;
      }
      if (typeof record.rawScoringGuide === 'string' && record.rawScoringGuide.trim()) {
        row.scoringOcrEvidence.push({ type: 'rawScoringGuide', path: relative(file), characters: record.rawScoringGuide.length, textSha256: sha(record.rawScoringGuide) });
      }
      if (isCandidate) row.typstCandidates.push({ path: relative(file), bodyCompiles: record.compile?.body === true });
    }
    for (const document of Object.values(record.documents ?? {})) {
      const id = document.questionId ?? document.id?.replace(/--.*$/, '');
      const target = rows.get(id);
      if (!target || !document.outputs?.mmd) continue;
      const artifact = path.resolve(root, document.outputs.mmd);
      if (!fs.existsSync(artifact) || !fs.statSync(artifact).isFile()) continue;
      const text = fs.readFileSync(artifact, 'utf8');
      if (!text.trim()) continue;
      const evidence = { type: 'cached-mmd', path: relative(artifact), manifest: relative(file), characters: text.length, textSha256: sha(text), status: document.status };
      if (document.kind === 'prompt' || document.id?.endsWith('--prompt')) target.promptOcrEvidence.push(evidence);
      if (document.kind === 'scoring-guide' || document.id?.endsWith('--scoring-guide')) target.scoringOcrEvidence.push(evidence);
    }
  }
}
for (const directory of ['pilot', 'tranches', 'fresh-tranches']) scan(path.join(root, 'data/ap-calculus', directory));
for (const directory of ['native-pass/intermediate/records', 'native-pass/candidates']) {
  const location = path.join(root, 'data/ap-calculus', directory);
  if (fs.existsSync(location)) scan(location);
}
const questions = [...rows.values()];
const counts = {
  total: questions.length,
  promptOcr: questions.filter(q => q.promptOcrEvidence.length).length,
  scoringOcr: questions.filter(q => q.scoringOcrEvidence.length).length,
  intermediatePromptRecords: questions.filter(q => q.intermediateRecords.length).length,
  typstCandidates: questions.filter(q => q.typstCandidates.length).length,
  compiledCandidateBodies: questions.filter(q => q.typstCandidates.some(c => c.bodyCompiles)).length,
  stagedPromptSourceMapsMatchingCurrentInventory: questions.filter(q => q.stagedSourceMapsMatchInventory).length,
};
const report = {
  generatedAt: new Date().toISOString(),
  definition: 'Unique source-question IDs with nonempty saved rawPrompt or prompt MMD OCR output. This is saved-ID evidence only: some older cache labels refer to the wrong prompt pages. Does not certify correct question content, full boundaries, mathematics, diagrams, conversion, or import integration. See AP_CALCULUS_NATIVE_PASS.md for source reconciliation.',
  counts, promptOcrPercent: 100 * counts.promptOcr / counts.total,
  missingPromptOcr: questions.filter(q => !q.promptOcrEvidence.length).map(q => q.id),
  missingTypstCandidate: questions.filter(q => !q.typstCandidates.length).map(q => q.id),
  errors, questions,
};
const out = path.join(root, 'data/ap-calculus/ocr-audit');
fs.mkdirSync(out, { recursive: true });
fs.writeFileSync(path.join(out, 'coverage.json'), JSON.stringify(report, null, 2) + '\n');
const pct = count => `${(100 * count / counts.total).toFixed(1)}%`;
const md = [
  '# AP Calculus actual OCR coverage', '', `Generated: ${report.generatedAt}`, '',
  report.definition, '',
  '| Stage | Unique questions | Percent of all local questions |', '| --- | ---: | ---: |',
  `| Saved prompt OCR | ${counts.promptOcr}/${counts.total} | ${pct(counts.promptOcr)} |`,
  `| Saved scoring-guide OCR | ${counts.scoringOcr}/${counts.total} | ${pct(counts.scoringOcr)} |`,
  `| Prompt OCR attached to intermediate records | ${counts.intermediatePromptRecords}/${counts.total} | ${pct(counts.intermediatePromptRecords)} |`,
  `| Generated Typst candidates | ${counts.typstCandidates}/${counts.total} | ${pct(counts.typstCandidates)} |`,
  `| Candidate bodies with recorded successful compilation | ${counts.compiledCandidateBodies}/${counts.total} | ${pct(counts.compiledCandidateBodies)} |`, '',
  `Missing prompt OCR: ${report.missingPromptOcr.join(', ') || 'none'}.`, '',
  '## Remaining coverage gaps and review', '',
  `Cached-only prompts: ${counts.promptOcr - counts.intermediatePromptRecords}; missing candidates: ${counts.total - counts.typstCandidates}; candidates without a recorded successful body compile: ${counts.typstCandidates - counts.compiledCandidateBodies}.`, '',
  'This audit now includes canonical native-pass records and candidates, as well as historical tranche evidence. It does not certify candidate freshness or exported product correctness. See tools/ap-calculus/pqp/AP_CALCULUS_NATIVE_PASS.md and native-pass/product/validation/validation-report.json for current integration evidence.', '',
  'The independent native-text first draft is under data/ap-calculus/native-pass/. The older image-based bank remains unchanged. Detailed mathematical/diagram review and classroom solutions remain second-pass work; the 2024 scoring guides are absent locally.', '',
  'Per-ID evidence paths, text hashes and remaining lists are in coverage.json. Repeat with:', '',
  '```bash', 'node tools/ap-calculus/pqp/audit_ocr_coverage.mjs', '```', '',
];
fs.writeFileSync(path.join(out, 'PROGRESS.md'), md.join('\n'));
console.log(JSON.stringify({ ...counts, promptOcrPercent: report.promptOcrPercent, missingPromptOcr: report.missingPromptOcr, errors, report: relative(path.join(out, 'coverage.json')) }, null, 2));
if (errors.length) process.exitCode = 1;
