# AP Calculus FRQ bank — durable progress ledger

Last updated: 2026-09-13

This is the handoff document for any later agent. Read it before changing the
AP Calculus pipeline or publishing questions. Update it in the same commit as
every completed, staged, published, or blocked tranche transition.

## Objective and non-negotiable gates

Build a private TestGen bank of AP Calculus AB/BC FRQs from the locally held
College Board sources. A question may be published only after:

1. exact source prompt and scoring-guide PDF/hash/page references;
2. complete prompt boundary and any required graph/table/axes;
3. a source-aware, manually rewritten classroom solution (not raw rubric);
4. native Typst body and solution compilation;
5. candidate and live TestGen import/round-trip validation; and
6. manual mathematical and visual review.

Raw OCR is evidence only. Do not emit raw Mathpix/legacy Mathpix solutions.
Never publish an item whose `publishState` is `blocked`.

## Scope inventory

- 34 BC prompt releases; 33 have paired scoring guides. BC 2024 is prompt-only
  and excluded. BC 2021 has a paired guide but no retained legacy ZIP.
- 34 AB prompt releases; 33 have paired scoring guides. AB 2024 is prompt-only
  and excluded. AB releases have no retained Mathpix ZIPs.
- Working first-pass scope: **66 paired releases / 396 FRQs**.
- Published: **24 FRQs**. Staged but unreviewed: **36 FRQs**. Remaining to
  source-lock/stage: **336 FRQs**.

## Published bank

Repository: `/home/max/dev/ap-calculus-exam-banks`

- Current published count: **24 questions, 14 image assets**.
- Latest bank commit/push: `8f70b42 Publish reviewed BC 2000 AP Calculus FRQs`.
- Included: 12-question calibration pilot, BC 1999 Q1–Q6, BC 2000 Q1–Q6.
- Import and round-trip validation passed after every promotion.

## Pipeline repository and current state

Repository: `/home/max/testgen-suite/testgen-ingest/tools/ocr-frq`

- Latest committed tranche-02 baseline: `23052d0 Stage AP Calculus FRQ tranche 02`.
- Deliberately untracked local material includes raw source PDFs, Mathpix
  caches/recovery inputs, and generated staging directories. Do not stage it.
- Key pipeline folder: `tools/ap-calculus/pqp/`.

### Completed tranches

| Tranche | Scope | State |
| --- | --- | --- |
| Pilot | 12 mixed AB/BC | Manually reviewed and published. |
| 01 | BC 1999 + BC 2000 (12) | Manually reviewed and published. |
| 02 | BC 2001 + BC 2002 (12) | Source-locked; page-limited Mathpix guide recovery complete; 12/12 bodies and guides compile; **blocked pending audit**. |
| 03 | BC 2003 standard + Form B (12) | Source-locked; recovery complete; 12/12 bodies and guides compile; **blocked pending audit**. |
| 04 | BC 2004 standard + Form B (12) | Source-locked; 12/12 prompt bodies compile; **blocked pending guide recovery and audit**. |

### Latest repair

`ap-calc-bc-2003-frq-02` used `<-4.5, -2.5>` for a velocity vector. The generic
preprocessor now converts only comma-containing angle brackets to parenthesized
vector notation, while preserving rubric deductions such as `<-1>`. Tranche 03
was regenerated and now compiles 12/12.

## Reusable first-pass workflow

`build_tranche_catalog.py`, `build_tranche_legacy_intermediate.py`,
`build_tranche_typst_candidates.py`, and
`prepare_tranche_scoring_recovery_inputs.py` all accept explicit paths.

For a cache-ready BC tranche:

```bash
python3 tools/ap-calculus/pqp/build_tranche_catalog.py --manifest MANIFEST --output CATALOG
python3 tools/ap-calculus/pqp/build_tranche_legacy_intermediate.py --catalog CATALOG --stage STAGE
python3 tools/ap-calculus/pqp/build_tranche_typst_candidates.py --intermediate STAGE --output CANDIDATES
python3 tools/ap-calculus/pqp/prepare_tranche_scoring_recovery_inputs.py --catalog CATALOG --output-dir RECOVERY_INPUTS --write
python3 tools/ap-calculus/pqp/submit_tranche_scoring_recovery.py --queue RECOVERY_INPUTS/submission-queue.json --cache RECOVERY_CACHE/manifest.json --dry-run
python3 tools/ap-calculus/pqp/submit_tranche_scoring_recovery.py --queue RECOVERY_INPUTS/submission-queue.json --cache RECOVERY_CACHE/manifest.json
python3 tools/ap-calculus/pqp/fetch_tranche_scoring_recovery.py --cache RECOVERY_CACHE/manifest.json --poll --sleep 10 --timeout 60
python3 tools/ap-calculus/pqp/attach_tranche_scoring_recovery.py --cache RECOVERY_CACHE/manifest.json --stage STAGE
python3 tools/ap-calculus/pqp/build_tranche_typst_candidates.py --intermediate STAGE --output CANDIDATES --replace
```

The recovery scripts are idempotent by input hash. They store Mathpix IDs and
artifacts locally; they never publish a question.

## Publishing workflow after the later audit

1. Create/review an explicit approval JSON with rewritten Typst bodies and
   solutions plus required source assets.
2. Compile each body and solution independently.
3. Use `emit_approved_pilot_questions.mjs` to create a candidate copy of the
   bank. It supports top-level `assetRoot` in an approval JSON.
4. Validate candidate import/round-trip, promote only into a clean bank,
   validate live import/round-trip, then commit and push both repositories.

## Immediate next action

1. Commit/push `tranche_03_manifest.json`, its deterministic catalog, the
   preprocessor fix, and this ledger update. Exclude generated artifacts.
2. Prepare/submit page-limited scoring-guide recovery for tranche 04, attach it,
   and require 12/12 compile before advancing its state.
3. Continue cache-first BC releases in 12-question tranches. Once BC cache
   sources are source-locked/staged, prepare AB/BC-2021 page-limited source
   OCR batches; do not publish them before the systematic audit.
