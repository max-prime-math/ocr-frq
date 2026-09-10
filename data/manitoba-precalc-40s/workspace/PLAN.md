# Manitoba Pre-Calculus 40S PQP Recovery Plan

## January 2014 pilot completed

The corrected 43-page marking guide has been submitted and fetched. All 43
question-header mappings agree with the original PDF. The two existing student
booklet caches also match their expected page headers and were reused.

See `derived/pilot-2014-jan/README.md` for the separate 44-question staging PQP,
portable ZIP, review PDF, and outstanding visual review. It contains 29 editable
Mathpix solutions, 5 original-guide image fallbacks, and 10 MCQ answer-key
solutions. All 44 complete questions render in Typst and parse in TestGen.
The original bulk export has not been replaced by this pilot.

For the next sitting, verify the ordered page mapping before paying for OCR;
a changed binary hash alone does not prove the old OCR content is unusable.

## Goal

Produce a working, traceable PQP record for every English Manitoba
Pre-Calculus 40S provincial-exam question, including MCQ choices and answer
keys, FRQ stems and scoring, diagrams, curriculum metadata, and marking-guide
solutions.

Question fidelity is the first release gate. Solution fidelity is a separate,
required gate so weak solutions never block recovery of otherwise usable
questions.

## Verified Inventory

- 21 sittings: January/June 2013–2019, January 2020, and January/June 2024–2026.
- 42 student booklets and 21 marking guides.
- 967 catalogued questions: 779 FRQ, 186 MCQ, and 2 matching.
- Student and marking-guide catalogs both contain all 967 question numbers.
- All 63 Mathpix jobs have local `lines.json`, `mmd`, and `tex.zip` output.
- The 2020–2023 gap is expected: provincial tests were suspended after January
  2020 through June 2023.

Run the reproducible inventory gate with:

```sh
python3 tools/manitoba-precalc-40s/pqp/audit_manitoba_source_inventory.py --strict
```

## Current Problems

1. The generated 21-package set is structurally valid but not editorially
   ready.
2. 669 solutions currently use raw PDF text fallback. Mathematical layout can
   be badly scrambled even though the content audit accepts the string.
3. The current page-filtered inputs differ from the inputs recorded for the
   completed Mathpix jobs. At least one old marking-guide upload used an
   incorrect page order (January 2014 begins with Question 34).
4. There is no end-to-end visual comparison gate between each PQP question and
   its source pages.
5. The Mathpix credentials are intentionally not stored in Git and must be
   loaded locally before a new submission.

## Direct Recovery Sequence

### 1. Freeze and preflight the sources

- Treat `source-pdfs/student-booklets/` and `source-pdfs/marking-guides/` as
  immutable originals.
- Regenerate the catalog and page-filter report only when source PDFs or catalog
  logic changes.
- Make filtered-PDF page selections deterministic and record the ordered source
  page list with every Mathpix job.
- Refuse export when the current source/input fingerprint differs from the
  completed job.

### 2. Finish questions before solutions

- Reuse the 42 completed student-booklet jobs; do not pay to rerun them unless a
  source-page comparison finds a specific defect.
- For every question, verify the original number, kind, complete stem, MCQ
  choice count/order, diagrams, points, booklet, calculator policy, and local
  asset references.
- Generate an HTML or PDF contact sheet with source-page crop beside rendered
  PQP content. Record review state per question (`unreviewed`, `question-ok`,
  `solution-ok`, `approved`, `needs-repair`).
- Import approved questions into a private TestGen staging bank while solution
  work continues.

### 3. Repair marking-guide extraction

- Start with one failed guide, January 2014, using the corrected ordered
  page-filtered PDF.
- Submit with a single explicit id and `--force`; fetch it; export only that
  sitting; compare all questions to the guide.
- If the pilot segments correctly, resubmit the other affected marking guides
  in small batches. Do not resubmit student booklets at the same time.
- Prefer marking-guide Mathpix `lines.json` because it preserves page geometry,
  question headers, equations, rubrics, and graph crops. Use `mmd` as a helpful
  secondary representation, not as the only source of page association.
- Keep the official MCQ answer tables authoritative for A–D answers. The
  marking guide remains authoritative for FRQ solutions and scoring notes.

Pilot commands, after loading Mathpix credentials:

```sh
python3 tools/manitoba-precalc-40s/pqp/mathpix_submit_manitoba.py \
  --id pc_2014_jan_mg --input-set filtered --force --dry-run
python3 tools/manitoba-precalc-40s/pqp/mathpix_submit_manitoba.py \
  --id pc_2014_jan_mg --input-set filtered --force
python3 tools/manitoba-precalc-40s/pqp/mathpix_fetch_manitoba.py \
  --id pc_2014_jan_mg --poll --overwrite
python3 tools/manitoba-precalc-40s/pqp/export_manitoba_pqp_mathpix.py \
  --year 2014 --term jan
python3 tools/manitoba-precalc-40s/pqp/audit_manitoba_pqp_mathpix_content.py
```

### 4. Use a faithful fallback, not scrambled text

- If a marking-guide solution cannot be segmented confidently, embed a crop of
  the exact marking-guide solution region/page as a local image.
- Label that solution source explicitly (`marking-guide-image-fallback`) and
  retain source PDF/page provenance.
- Never silently replace failed mathematical OCR with raw PDF text. Raw text can
  remain diagnostic evidence, but it is not a publishable solution.
- Later, convert image fallbacks to editable Typst without changing stable
  question ids.

### 5. Release gates

A question may enter the staging bank when its stem, type, choices, assets,
number, and source provenance are approved. It may enter the published bank
when its answer/solution and scoring are also approved.

The complete corpus is done only when:

- inventory, schema, TestGen import, and asset audits pass;
- every question has a recorded visual-review state;
- every MCQ has four verified choices and an answer-key match;
- every FRQ has a faithful solution or an explicitly reviewed guide-image
  fallback;
- there are zero `source-pdf-text` publishable solutions;
- regenerated PQPs are deterministic apart from export timestamps.

## Efficiency Notes

- The corrected marking-guide filters total 882 pages for all 21 guides. The 18
  sittings currently dependent on PDF-text solution fallback total 759 pages,
  approximately USD 3.80 at the estimator currently used by the pipeline.
- Submit the January 2014 pilot first. A successful end-to-end result is much
  cheaper than discovering a segmentation bug after a bulk submission.
- Marking guides often contain the question, solution, rubric, and answer key,
  but retain student booklets as the canonical question source: they preserve
  exact student-facing wording, MCQ distractors, calculator context, and
  diagrams without marking annotations.
- Cache every API response. Resubmission should be exceptional and identified by
  document id, not a blanket rerun.
