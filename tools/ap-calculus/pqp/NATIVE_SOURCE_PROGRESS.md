# Native source reconciliation — completed first draft

Final local build: 2026-09-14. Main agent completed the saved source worker's
changes after the usage limit; no new OCR uploads or subagents were required.

- Canonical output: `data/ap-calculus/native-pass/intermediate/records/`.
- 408 records, 182 source diagram assets, no missing expected subpart labels,
  no unresolved image references.
- Methods: 211 source-crop-filtered Mathpix line records; 192 retained Mathpix
  TeX ZIP records resegmented by actual question; five guide-prompt recoveries.
- Five old cache entries contained the wrong prompt despite matching IDs:
  AB 2005 Q6, 2007 Q6, 2009 Form B Q6, 2011 Q5/Q6. Statements recovered from
  existing guide OCR and reconciled with exam sources. Explicit source/math
  review flags remain on those five; no invented solution or paid re-OCR.
- Corrected six graph ownership/crop boundaries: BC 2009 Form B Q3/Q5,
  2011 Q4, 2011 Form B Q4, 2014 Q3, 2019 Q6. Removed those images from the
  preceding records that previously claimed them.
- Restored AB 2005 Q6's original blank slope-field axes and twelve dots after
  part (a), not the solved slope field from the scoring guide.
- Parent visually inspected all seven corrected figure assets. Raw-source and
  native automated audits cover 408 IDs, no missing subparts or prompt
  placeholders; one BC 1999 Q1 header/word-spacing false positive remains.
  Automated word matching is not exhaustive mathematical or diagram review.

Rebuild: `python3 tools/ap-calculus/pqp/build_native_source_records.py`.
Source edits invalidate candidate hashes: reconvert, re-export, validate and
emit a NEW folder snapshot before delivering changes. Current first-draft
delivery and verification are in AP_CALCULUS_NATIVE_PASS.md.
