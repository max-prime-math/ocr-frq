# AP Calculus local-folder bank

Updated 2026-09-14: the current delivery is the completed editable native first
draft. The earlier `draft/ap-calculus-local-bank` image snapshot is preserved,
but is no longer the recommended folder for a new bank.

The user requested Local Folder support after their running TestGen rejected
repository schema 2. This separate export uses the actual historical schema-1
exporter and is checked with both historical and current TestGen importers.
It does not modify the reviewed bank or the ongoing main-thread draft outputs.

Open this folder itself in TestGen's **Local Folder** workflow:

`/home/max/testgen-suite/testgen-ingest/tools/ocr-frq/data/ap-calculus/native-pass/ap-calculus-native-bank`

It contains `manifest.json`, `questions/`, `images/`, `curriculum/`, `narratives/`,
and the empty `tests/index.json` required by schema 1. All image files are
included and their bytes are checked after import. No separate upload is needed.
Select this folder, not its parent `native-pass/`, the `product/` directory, or `imgs/`.

Build and validation report:
`data/ap-calculus/native-pass/ap-calculus-native-bank-validation.json`.

Reproduce with:

```sh
node --experimental-strip-types tools/ap-calculus/pqp/export_ap_local_folder.mjs --input data/ap-calculus/native-pass/product/testgen-question-bank.json --output NEW_FOLDER
```

The exporter refuses to overwrite an existing bank. To refresh after future
draft changes, use `--output /absolute/path/to/a/new-folder` and preserve/merge
user edits deliberately. This bank is a snapshot, not synchronized with the PQP.
The input JSON SHA-256 is recorded in the report for future agents.

Content remains a first draft: 24 previously reviewed records and 384 editable
OCR prompts with placeholder solutions. All 408 questions pass actual TestGen
body/solution rendering. The folder includes 183 required images, with no
whole-prompt screenshot fallbacks. Detailed mathematical review and classroom
solutions remain second-pass work. No browser click-through is claimed.
