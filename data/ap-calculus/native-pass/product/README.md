# AP Calculus editable OCR first draft

408 questions: 24 reviewed records preserved and 384 compiled native OCR drafts. Figures remain images where needed. There are no image-only prompt fallbacks. OCR correctness, diagram completeness, solutions and point totals still need the recorded second pass.

## TestGen import

Use Import PQP / JSON with `testgen-question-bank.json` for one-file import including images. This JSON's bank-format version 2 is distinct from local-folder manifest schema 1. Stable IDs match the older image draft; importing into an existing bank may skip existing IDs. Use a new bank to inspect this independent native draft without changing user edits.

For Local Folder, use the separately generated `data/ap-calculus/ap-calculus-frq-bank` folder with manifest schema 1, compatible with the older deployed TestGen loader. Never select this `product` directory as a Local Folder bank. No local server is required.

The PQP ZIP is an archive for transport, not a direct ZIP importer. Its external `imgs/` assets require upload if using PQP JSON instead of the embedded bank JSON.

## Organization

One bank, two classes: Calculus AB (Units 1-8) and Calculus BC (Units 1-10), with CED unit and section names. Each question's section is the highest-numbered CED topic among its lettered parts, from the reviewed per-part topics in `tools/ap-calculus/pqp/ap_calculus_frq_topics.json`. Tags are the exam year, `Form B` where applicable, `Part A`/`Part B`, and `Calculator Active`/`No Calculator`. Draft status is recorded in PQP extensions and the repair queue, not in tags.

## Reproducibility and review

`build-report.json` records candidate hashes and counts. `repair-queue.json` and `REPAIR_QUEUE.md` track the remaining review. `validation/validation-report.json`, when present, records actual TestGen parser/render results. All placeholder solutions and provisional points remain labeled; generated native text is not presented as reviewed mathematics.

Rebuild in order: `build_native_source_records.py`, `build_native_typst_candidates.py`, then `export_ap_native_draft.py` (all in `tools/ap-calculus/pqp/`). Revalidate using `validate_ap_draft.mjs --product data/ap-calculus/native-pass/product --inventory data/ap-calculus/draft/source-inventory.json --reviewed-bank DIR`, where DIR holds the 24 reviewed records (ap-calculus-exam-banks at commit 8f70b42). Generate a new local-folder snapshot using `export_ap_local_folder.mjs --input data/ap-calculus/native-pass/product/testgen-question-bank.json --output NEW_FOLDER`; that exporter refuses to overwrite an existing folder.
