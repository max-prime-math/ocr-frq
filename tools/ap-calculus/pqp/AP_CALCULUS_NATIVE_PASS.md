# AP Calculus native-text integration — completed first-draft handoff

Started 2026-09-13 (local). This is the active native-text pass requested after
the user clarified that the image-based bank was not a completed OCR product.

## Publication update — 2026-09-15

The user authorized replacing the 24-question GitHub publication with the latest
complete first draft. `max-prime-math/ap-calculus-exam-banks` main now points to
`8bdc1b3` (remote verified): 408 questions, 183 images, schema 1, no saved tests.
Fresh current-TestGen import/manifest validation passed and published files match
the native-bank snapshot byte-for-byte. Prior reviewed content is preserved
(class/source-ID metadata added, one table whitespace correction); the 384 draft
solutions remain placeholders. No raw PDFs/OCR cache, credentials, or student
data were published. Original independent local snapshots were not modified.
This user-authorized publication supersedes the original no-overwrite rule below
for the GitHub publication checkout only; do not overwrite other user folders.

## Organization and cleanup pass — 2026-09-30

- **Organization.** One bank, two classes: "Calculus AB" and "Calculus BC" (ids
  unchanged). Each lettered part of all 408 prompts was read and assigned a CED
  topic in `ap_calculus_frq_topics.json` (reviewed data, replaces the keyword
  classifier). Section = highest-numbered part topic. Tags are only year,
  `Form B`, `Part A`/`Part B` and `Calculator Active`/`No Calculator`; the part
  rule (Q1-3 through 2010, Q1-2 from 2011) matched the PDF "Part B" page for all
  384 text-layer PDFs. `organize()` in `ap_calculus_curriculum.py` is the single
  source used by both exporters and the retag script.
- **Source corrections** (`SOURCE_CORRECTIONS`, exact-match or fail): AB 2006B Q3
  requirement (ii) restored; AB 1999 Q6 "n PQR" -> triangle PQR; BC 2010B Q2 lost the
  P(t) table that belongs to Q3.
- **Converter cleanup**, verified by rendering all 408 old/new bodies: 260
  pixel-identical; every difference is an intended fix, a proper double-prime
  glyph, or a checked one-pixel/line-wrap shift. Trailing empty table cells,
  repeated rules, nested header tables, text run into tables, exam-booklet
  logistics, a page header, "dollar 120" prose, paragraph-end breaks, caption
  run-ins, roman-numeral item breaks and OCR math/prose spacing are fixed.
- **Tooling repairs.** Converter preflight refuses to write when the toolchain is
  broken (a missing mitex path had overwritten every candidate; restored from
  backup). mitex default path now finds `~/dev/apps/typr`. Validator/folder
  exporter default to `../test-generator` and pass current TestGen's
  `savedTests`. Validate reviewed content against the 24-record snapshot
  (ap-calculus-exam-banks commit 8f70b42) via `--reviewed-bank`.
- **Output.** New local folder `data/ap-calculus/ap-calculus-frq-bank` (schema 1,
  both importers pass). Product validation: all checks pass, 408/408 rendered by
  actual TestGen. Older folders were left untouched. Not committed or published.

## Scope and acceptance

All 408 locally available AB/BC prompts have saved OCR. This pass turns them into
editable native Typst questions with only required diagrams retained as images,
then delivers a new independent TestGen JSON/PQP and schema-1 local bank folder.
Placeholder classroom solutions and provisional points remain explicitly marked.
The original reviewed bank and the user's existing local-folder snapshot must
not be overwritten. No new OCR submissions are needed or planned.

Completion requires separate evidence for:

1. 408 source-linked records; preserve tables/graphs before question numbers.
2. Native prompt candidates with all subparts and explicit real diagram assets;
   full-page images and figure-placeholder text do not count as native conversion.
3. All exported questions compile through the actual TestGen template, including
   single-newline processing that previously broke table code.
4. 408 IDs and assets survive PQP/native import and schema-1 folder roundtrip.
5. Source-content checks and representative visual/math review; remaining minor
   draft issues must stay in a per-question repair queue rather than be hidden.

The deployed testgen.dev site previously rejected schema-2 folder manifests.
Use `export_ap_local_folder.mjs`, which verifies schema-1 output through both the
historical and current importers. Do not equate local app support with deployment.

## Parallel ownership

| Worker | Files owned | Output |
| --- | --- | --- |
| native_source_records | build_native_source_records.py; NATIVE_SOURCE_PROGRESS.md | native-pass/intermediate/records and assets |
| native_conversion | build_native_typst_candidates.py (or mjs); own tests; NATIVE_CONVERSION_PROGRESS.md | native-pass/candidates |
| native_export | native exporter; NATIVE_EXPORT_PROGRESS.md | native-pass/product and new schema-1 folder |
| parent | this handoff; independent content audit and final verification | audit/report and final handoff |

All generated paths above are under `data/ap-calculus/`. Worker files are under
`tools/ap-calculus/pqp/`. Agents must update their ledgers before stopping or
hitting a limit. Resume from written outputs, not duplicated paid OCR.

## Starting baseline

408 saved prompt OCRs; 396 saved scoring-guide OCRs; 359 intermediate records;
315 old native candidates, 307 with recorded successful body compilation.
Old candidates can contain dropped figures, unsafe math simplifications, and
incorrect source boundaries. Canonical source records and safe conversion are
being built separately; old staging remains untouched as evidence.

## Current state — first draft complete, 2026-09-14

Parent finished locally after the workers hit the usage limit, without restarting
agents or submitting new paid OCR. Final source, conversion and export runs are saved.

- Canonical source records: **408**, with 182 source diagram assets. Five
  guide-based prompt recoveries retain explicit review flags.
- Native candidates: **408/408 compile and are fresh** against both source and
  converter hashes. All exported prompts are editable; required figures remain images.
- Final native product: **408 questions**, 384 native drafts plus 24 preserved
  reviewed records; **183 images**, **zero whole-prompt image fallbacks**.
- Actual TestGen PQP parser, all image bytes/references, repository roundtrip:
  passed. Actual TestGen body+solution rendering: **408/408 passed**, plus two
  AB/BC sample exams. Validation report has no errors.
- New independent local folder: **schema 1**, 408 questions, 183 images, 597 files.
  Historical schema-1 and current importers both pass; all content, image bytes,
  manifest sizes/hashes and on-disk re-import verified. Browser click-through
  was not performed. No existing user-connected folder was overwritten.
- Native regression suite: **20 tests passed**. The 30 prior render failures
  shared a terminal Typst layout backslash escaping TestGen's closing bracket.
  Converter removes that final layout break and now tests the embedded wrapper.
- Source and native automated audits each cover 408 IDs, with no missing
  subpart labels or prompt placeholders. One BC 1999 Q1 header/word-spacing
  warning remains a documented false positive, not a mathematical certification.
- Visually inspected seven corrected diagram assets (AB 2005 Q6; BC 2009 Form B
  Q3/Q5, 2011 Q4, 2011 Form B Q4, 2014 Q3, 2019 Q6), plus final rendered AB 2024
  Q1 table/subparts and AB 2005 Q6 blank slope-field axes. Table border spacing
  and oversized low-resolution axes are cosmetic second-pass candidates.

### Use the completed draft

Paths relative to repository root:

- `data/ap-calculus/native-pass/ap-calculus-native-bank`: select this folder in
  testgen.dev Local Folder. It is schema 1, not the previously rejected schema 2.
- `data/ap-calculus/native-pass/ap-calculus-native-bank-validation.json`: folder verification.
- `data/ap-calculus/native-pass/product/testgen-question-bank.json`: alternative
  one-file import, including images. Import into a NEW bank to avoid duplicate-ID skips.
- `data/ap-calculus/native-pass/product/validation/validation-report.json`: render/import evidence.
- `data/ap-calculus/native-pass/product/repair-queue.json`: 384 second-pass items.
- `data/ap-calculus/native-pass/audit/`: raw-source and native-content triage reports.

Do not select the `product` directory as a Local Folder. The new folder is an
independent snapshot; rebuilding product JSON will not update it or user edits.
The old `data/ap-calculus/draft/product` and old user folder remain unchanged.

### What remains (second pass, not an OCR completion blocker)

384 classroom solutions are explicitly marked placeholders, with provisional
9-point totals. Detailed mathematical and exhaustive diagram review is pending;
none of those drafts were promoted to reviewed. Five recovered AB prompts are
priority review items. Save accepted fixes through durable source/converter
changes or implement reviewed overrides before changing generated JSON. Existing
nightly proposal automation was not changed by this completion pass and does not
automatically update this native folder. No deployment, commit or push was made.

To reproduce: source builder → native candidate builder → native exporter →
actual TestGen validator → local-folder exporter with a NEW output path. Commands
are in NATIVE_EXPORT_PROGRESS.md. Do not rerun Mathpix or restart the initial pass.

### Source-reconciliation finding

Five old AB cache entries had matching IDs but OCR from the wrong prompt pages:
AB 2005 Q6, AB 2007 Q6, AB 2009 Form B Q6, AB 2011 Q5 and Q6. The earlier
408/408 metric counted saved OCR evidence by ID and did not validate that content.
These statements were recovered from already saved scoring-guide OCR and
reconciled against original exam PDFs. Do not claim source correctness
from the earlier OCR percentage. No new paid OCR is being used for this recovery.

Read worker ledgers for checkpoints and this file for overall acceptance status.
