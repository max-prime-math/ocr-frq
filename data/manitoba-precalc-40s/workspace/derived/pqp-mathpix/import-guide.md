# Manitoba Pre-Calculus 40S PQP Import Guide

Generated packages are in `data/manitoba-precalc-40s/workspace/derived/pqp-mathpix/pqp/`.
Use the `.pqp.json` file inside each session folder, together with that folder's adjacent `assets/` directory.
Do not import from `data/manitoba-precalc-40s/workspace/derived/pqp-pdf-crop-v0/`; it is the obsolete PDF-crop output.

## Current Package Set

- Packages: 21
- Questions: 967
- FRQ: 779
- MCQ: 186
- Matching: 2
- Local image references: 425

## Validation Status

- `parseBulkImportJson`: passed for all 21 packages / 967 questions.
- Appendix/outcome tables in stems or solutions: 0.
- Empty or unmatched solutions: 0.
- Remote Mathpix image URLs in visible content: 0.
- Visible LaTeX figure/caption/includegraphics artifacts: 0.
- Raw alignment ampersands and known Typst OCR artifacts: 0.
- Bare multi-letter identifiers inside math spans: 0, except known Typst math functions/symbols.
- Units and labels inside math use upright text forms such as `upright("cm")`, `upright("mL")`, `upright("mEq")`, `upright("Ms")`, and `upright("FV")`.
- Missing local image files or undeclared `#image("assets/...")` references: 0.
- MCQs: one question each, four structured choices, answer A-D present.
- MCQ solutions: populated from answer-key data and structured choices.
- Matching questions: retained as `matching`, not ordinary MCQ.
- Curriculum metadata: Pre-Calculus 40S class/unit/section metadata present.

## Remaining Manual Review

None from the automated audit.

The previous unmatched set consisted of 186 MCQs plus `mb-pc40s-2013-jan-q32`.
The MCQs now have concise answer-key solutions, and `mb-pc40s-2013-jan-q32` now uses the marking-guide solution graph image after the `Solution` marker.

## Recommendation

Ready to upload into test-generator: yes.
