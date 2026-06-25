# ocr-frq

OCR and conversion workspace for exam questions.

The repository currently has two active domains:

- AP Calculus BC free-response conversion from Mathpix ZIP exports to LaTeX/PDF.
- Manitoba Pre-Calculus 40S provincial exam conversion to Portable Question Package (PQP) JSON for import into `test-generator`.

## Repository Layout

```text
apps/
  manitoba_figure_extractor.py      Streamlit helper for Manitoba figure extraction.

data/
  ap-calculus-bc/
    source-pdfs/                    Original AP PDFs.
    mathpix-zips/                   Mathpix ZIP exports consumed by src/main.py.
    corrections/                    Manual AP scoring-guide patches.
    cache/                          OCR/repair cache artifacts.

  manitoba-precalc-40s/
    workspace/                      Manitoba source PDFs, catalogs, Mathpix cache, generated PQPs, and reports.

  legacy/
    manitoba-prototype-mathpix/     Older one-off Manitoba Mathpix experiment artifacts.

docs/
  bulk-import.md                    Legacy bulk-import format notes.
  integration-summary.md            Historical integration notes.
  manitoba-processing.md            Older Manitoba PDF/Mathpix processing notes.
  test-generator-import-guide.md    Import guide for `test-generator`.

outputs/
  ap-calculus-bc/
    latex/                          Main generated AP LaTeX/PDF output.
    latex-v2/                       Experimental AP LaTeX/PDF output.

prompts/
  prompt.txt                        Historical prompt material.

src/
  Reusable Python library code for parsing, extraction, rendering, and compilation.

tests/
  Pytest coverage for the reusable library code.

tools/
  ap-calculus-bc/                   AP helper scripts.
  manitoba-precalc-40s/             Manitoba conversion tools.
    pqp/                            Current Manitoba PQP generation, Mathpix API, and audit scripts.
```

## AP Calculus BC Pipeline

The AP pipeline reads Mathpix ZIP exports from `data/ap-calculus-bc/mathpix-zips/` and writes the combined exam-class output to `outputs/ap-calculus-bc/latex/`.

```bash
python -m src.main
python -m src.main --years 2018,2019
python -m src.main --no-form-b
python -m src.main --output-dir outputs/ap-calculus-bc/latex
```

Important files:

- `src/main.py`: CLI entry point.
- `src/mathpix.py`: Mathpix ZIP parsing.
- `src/latex_writer.py`: exam-class LaTeX rendering.
- `src/compile_gate.py`: `pdflatex` invocation.
- `data/ap-calculus-bc/corrections/corrections.json`: manual scoring-guide patches.

## Manitoba Pre-Calculus 40S PQP Pipeline

The active Manitoba workspace is `data/manitoba-precalc-40s/workspace/`.

Primary import-ready output:

```text
data/manitoba-precalc-40s/workspace/derived/pqp-mathpix/pqp/
```

Current status documents:

- `data/manitoba-precalc-40s/workspace/derived/pqp-mathpix/import-guide.md`
- `data/manitoba-precalc-40s/workspace/derived/pqp-mathpix/content-audit-report.md`

Core commands:

```bash
python3 tools/manitoba-precalc-40s/pqp/mathpix_status_manitoba.py
python3 tools/manitoba-precalc-40s/pqp/mathpix_prepare_manitoba_inputs.py
python3 tools/manitoba-precalc-40s/pqp/mathpix_submit_manitoba.py --dry-run
python3 tools/manitoba-precalc-40s/pqp/mathpix_fetch_manitoba.py --poll
python3 tools/manitoba-precalc-40s/pqp/export_manitoba_pqp_mathpix.py
python3 tools/manitoba-precalc-40s/pqp/audit_manitoba_pqp_mathpix_content.py
```

The older image-crop PQP output remains archived under:

```text
data/manitoba-precalc-40s/workspace/derived/pqp-pdf-crop-v0/
```

Do not use that archive for final `test-generator` import unless you intentionally want the obsolete crop-heavy fallback.

## Setup

```bash
python -m pip install -r requirements.txt
```

The AP LaTeX build also needs `pdflatex` with the `exam` document class and standard AMS packages.

Mathpix API scripts need:

```bash
export MATHPIX_APP_ID="your-app-id"
export MATHPIX_APP_KEY="your-app-key"
```

Local secrets should stay in `.mathpix.env`, which is ignored by Git.

## Verification

```bash
pytest
python3 tools/manitoba-precalc-40s/pqp/audit_manitoba_pqp_mathpix_content.py
node --experimental-strip-types --input-type=module -e "import { readFileSync } from 'node:fs'; import { globSync } from 'node:fs'; import { parseBulkImportJson } from '/home/max/testgen-suite/test-generator/src/lib/bulk-import.ts'; const files = globSync('data/manitoba-precalc-40s/workspace/derived/pqp-mathpix/pqp/*/*.pqp.json'); let questions = 0; for (const file of files) { const parsed = parseBulkImportJson(readFileSync(file, 'utf8')); if (!parsed || parsed.error) throw new Error(file + ': ' + (parsed && parsed.error)); questions += parsed.questions.length; } console.log(JSON.stringify({ packages: files.length, questions }));"
```
