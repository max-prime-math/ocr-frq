# Native OCR conversion progress

## Completed first-draft pass

- Canonical OCR input: `data/ap-calculus/native-pass/intermediate/records/`.
- Editable candidate output: `data/ap-calculus/native-pass/candidates/`.
- Reproducible command: `python tools/ap-calculus/pqp/build_native_typst_candidates.py`.
- No whole-question images count as converted content. Mathematical grouping,
  source tables, subpart labels, and diagram references must survive conversion.
- Image references resolve to `/imgs/<name>`; candidate asset manifests retain
  the actual disk paths for exporters. Single-line table code supports TestGen.
- Compilation is necessary, not evidence of mathematical/source correctness.

## 2026-09-14 final verification

- Final full conversion completed: **408/408 native bodies compile**, all 408
  source-record and converter hashes are current. This does
  not certify mathematical correctness, source completeness, or visual layout.
- Nine converter regression tests pass (20 together with exporter tests): grouped square roots retain their powers,
  nested/indexed roots survive, stacked limit conditions retain both lines,
  native tables retain cells, list labels survive, image references require
  declared source assets, and spatial OCR subparts become separate paragraphs
  without splitting inline references.
- The converter records source-record and converter SHA-256 hashes to make
  stale candidates detectable after any source or converter revision.
- All source diagram corrections and subpart paragraph improvements are included.
- Fixed the shared cause of 30 actual-template failures: a terminal layout
  backslash escaped the wrapper's closing bracket. Remove only the terminal
  layout break, preserve literal escaped slashes, and compile inside the actual
  single-newline-processing/grid embedding pattern in regression checks.
- Final exported product passes **408/408 actual TestGen body+solution renders**
  and both AB/BC sample exams. See AP_CALCULUS_NATIVE_PASS.md for delivery paths.

Reproduce the regression checks with:

```sh
python -m unittest discover -s tools/ap-calculus/pqp/tests -p test_native_conversion.py
```

Next: targeted second-pass mathematical review, not another wholesale conversion.
No new paid OCR was needed. Existing reviewed bank and image draft remain unchanged.
