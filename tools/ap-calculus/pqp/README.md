# AP Calculus FRQ pilot

This is the replacement boundary for the older, BC-only LaTeX renderer.  It
is deliberately small: a 12-question calibration set, a source manifest, and
validation that is useful before OCR or editorial work begins.

The pilot includes three questions from each of four releases:

| Course | Release | Questions | Purpose |
| --- | --- | --- | --- |
| BC | 1998 | 1, 2, 6 | old layout; includes the known `1998 Q2` legacy-OCR concern |
| BC | 2010 Form B | 1, 3, 6 | calculator/non-calculator split and a source diagram |
| AB | 2005 Form B | 1, 4, 6 | a graph, a rate problem, and a differential equation |
| AB | 2019 | 1, 3, 6 | modern layout, a graph, and a tangent-line task |

The manifest records the exact source and scoring-guide PDF, page span, and
SHA-256 fingerprint.  It never treats Mathpix output as authoritative.

## Commands

From the `ocr-frq` repository:

```bash
# Verify source identity and write a deterministic catalog.
python3 tools/ap-calculus/pqp/build_pilot_catalog.py

# Verify without changing a generated catalog.
python3 tools/ap-calculus/pqp/build_pilot_catalog.py --check

# Make twelve page-limited AB prompt/scoring-guide PDFs for the pilot only.
# This does not call Mathpix; inspect these files before any API submission.
python3 tools/ap-calculus/pqp/prepare_pilot_mathpix_inputs.py --write

# Inspect the exact twelve documents. This is the last no-cost API gate.
python3 tools/ap-calculus/pqp/submit_pilot_mathpix.py --dry-run

# Submit only the calibration queue, then retain the returned Mathpix IDs and
# source hashes locally. This does not generate or publish PQPs.
python3 tools/ap-calculus/pqp/submit_pilot_mathpix.py

# Poll the twelve jobs and fetch Mathpix artifacts once each is complete.
python3 tools/ap-calculus/pqp/fetch_pilot_mathpix.py --poll

# Create source-locked intermediate records. These remain blocked from
# publication and keep raw OCR separate from scoring material.
python3 tools/ap-calculus/pqp/build_pilot_intermediate.py

# Create compile-checked Typst candidates. They are not PQPs and cannot be
# emitted until the scoring guide is split and each candidate is reviewed.
python3 tools/ap-calculus/pqp/build_pilot_typst_candidates.py

# Emit only manually approved pilot questions into a separate candidate copy
# of the private TestGen working bank. Validate and promote that candidate
# before committing it.
node --experimental-strip-types tools/ap-calculus/pqp/emit_approved_pilot_questions.mjs /home/max/dev/ap-calculus-exam-banks /tmp/ap-calculus-working-stage

# Run the skeleton's contract tests.
python3 -m unittest discover -s tools/ap-calculus/pqp/tests -v
```

`pilot_manifest.json` is the source of truth.  The generated catalog is kept
in Git as the immutable source-fingerprint record; prepared PDFs are excluded
because they can be reproduced exactly from that catalog.

## Promotion gate

No pilot question may become a PQP/TestGen question until it has:

1. a matching prompt and scoring guide (2024 prompt-only material is excluded),
2. an immutable source fingerprint and page reference,
3. native Typst body and solution generated from retained Mathpix artifacts,
4. an explicit distinction between worked solution and scoring rubric,
5. source-to-render and TestGen import/round-trip validation, and
6. an independent mathematical and visual review.

The next implementation step is an extractor that writes a per-question
intermediate record from either a retained BC Mathpix ZIP or a pilot Mathpix
result.  It must target this manifest rather than the old combined LaTeX
output.

## First scaled tranche

`tranche_01_manifest.json` selects six BC questions from each of 1999 and
2000. Both releases already have paired prompt/scoring Mathpix ZIPs, so its
catalog and blocked staging require no new Mathpix request:

```bash
python3 tools/ap-calculus/pqp/build_tranche_catalog.py
python3 tools/ap-calculus/pqp/build_tranche_legacy_intermediate.py
python3 tools/ap-calculus/pqp/build_tranche_typst_candidates.py
# Writes 12 page-limited scoring-guide PDFs, but does not submit them.
python3 tools/ap-calculus/pqp/prepare_tranche_scoring_recovery_inputs.py --write
```

The resulting records remain blocked. They must pass source-boundary, figure,
solution, Typst, and TestGen review before any question is emitted.
