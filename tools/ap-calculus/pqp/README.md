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

# Make six page-limited AB prompt PDFs for the pilot only. This does not call
# Mathpix; inspect these files before any API submission.
python3 tools/ap-calculus/pqp/prepare_pilot_mathpix_inputs.py --write

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
