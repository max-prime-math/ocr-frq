# AP Calculus native export progress

## Scope

Integrate all 384 non-reviewed native OCR prompts while preserving the 24 reviewed records. Keep the prior image draft and user-connected bank folders unchanged. Place generated product under `data/ap-calculus/native-pass/product` and create a new schema-1 Local Folder snapshot, never a schema-2 manifest.

## Current state

- Native exporter implemented at `export_ap_native_draft.py`.
- Export rejects missing candidates, failed compile checks, missing/unlisted assets, duplicate asset names, placeholder prompt text, and image-only/full-prompt crop fallbacks before writing product files.
- On 2026-09-14, eleven exporter regression tests pass (`python -m unittest discover -s tools/ap-calculus/pqp/tests -p 'test_native_export.py'`), including byte-exact embedded/bundled image preservation.
- Final product built on 2026-09-14 at 19:46 UTC: 408 questions, 384 editable OCR drafts, 24 reviewed records preserved, 183 image assets, zero full-prompt screenshot fallbacks. All 408 candidates compile and have current source/converter hashes.
- Actual TestGen validation PASSED: 408/408 body+solution renders, two sample exams, PQP parser, reviewed-content preservation, all image references/bytes and repository roundtrip. See `native-pass/product/validation/validation-report.json`.
- New independent schema-1 folder created at `data/ap-calculus/native-pass/ap-calculus-native-bank`: 408 questions, 183 images, 597 files. Historical and current importers, on-disk re-import, content/image preservation and manifest hash/size checks all pass. Report: `data/ap-calculus/native-pass/ap-calculus-native-bank-validation.json`. Browser click-through not performed.
- No placeholder solution is relabeled as reviewed; remaining tasks are recorded per question in the generated repair queue.

## Reproduce

1. Run `python3 tools/ap-calculus/pqp/build_native_source_records.py`, then `python3 tools/ap-calculus/pqp/build_native_typst_candidates.py --workers 6` if source/converter changes require regeneration.
2. Run `python tools/ap-calculus/pqp/export_ap_native_draft.py`.
3. Run `node --experimental-strip-types tools/ap-calculus/pqp/validate_ap_draft.mjs --product data/ap-calculus/native-pass/product --inventory data/ap-calculus/draft/source-inventory.json`.
4. Run `node --experimental-strip-types tools/ap-calculus/pqp/export_ap_local_folder.mjs --input data/ap-calculus/native-pass/product/testgen-question-bank.json --output NEW_FOLDER` after validation. The delivered native folder already exists: do not overwrite it or user edits.

Importing the native JSON into a bank already containing the image-draft IDs may skip duplicates. Use a new bank or connect the new independent native local-folder snapshot.
