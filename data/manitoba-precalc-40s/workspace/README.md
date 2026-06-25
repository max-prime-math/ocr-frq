# Manitoba Pre-Calculus 40S Exam Ingestion Workspace

This directory keeps original PDFs, derived audit artifacts, Mathpix output, and archived experimental exports separate.

Repo-relative path: `data/manitoba-precalc-40s/workspace/`.

## Layout

- `source-pdfs/student-booklets/`: original student booklets, one PDF per booklet.
- `source-pdfs/marking-guides/`: marking guides split to one PDF per sitting.
- `source-pdfs/combined/`: combined PDFs used to build split/audit artifacts.
- `catalog/`: CSV/JSON audit tables that map questions, answer keys, learning outcomes, and source pages.
- `derived/filtered-pdfs/`: temporary extracted PDFs such as answer-key-only or question-only PDFs.
- `derived/pqp-pdf-crop-v0/`: archived first-pass PQPs built from PDF text and page screenshots. Do not use for final export.
- `mathpix/manual-combined/`: manually uploaded Mathpix output from the combined PDFs.
- `mathpix/api-cache/`: API-driven Mathpix manifest and downloaded `mmd`, `lines.json`, and `tex.zip` artifacts.

## Mathpix API Keys

Set these two environment variables before running any script that calls Mathpix:

```sh
export MATHPIX_APP_ID="your-app-id"
export MATHPIX_APP_KEY="your-app-key"
```

For a one-machine setup, putting those two lines in `~/.zshrc` is fine. Do not commit them to this repo. If you prefer a local file, copy the shape of `ocr-frq/.mathpix.env.example` into an untracked `ocr-frq/.mathpix.env` and run `source ocr-frq/.mathpix.env` before the submit/fetch commands.

## Workflow

From the repository root:

```sh
python3 tools/manitoba-precalc-40s/pqp/mathpix_status_manitoba.py
python3 tools/manitoba-precalc-40s/pqp/mathpix_prepare_manitoba_inputs.py
python3 tools/manitoba-precalc-40s/pqp/mathpix_submit_manitoba.py --dry-run
python3 tools/manitoba-precalc-40s/pqp/mathpix_submit_manitoba.py
python3 tools/manitoba-precalc-40s/pqp/mathpix_fetch_manitoba.py --poll
python3 tools/manitoba-precalc-40s/pqp/export_manitoba_pqp_mathpix.py
python3 tools/manitoba-precalc-40s/pqp/audit_manitoba_pqp_mathpix_content.py
```

Useful narrower commands:

```sh
python3 tools/manitoba-precalc-40s/pqp/mathpix_submit_manitoba.py --kind marking-guide --limit 1 --dry-run
python3 tools/manitoba-precalc-40s/pqp/mathpix_submit_manitoba.py --id pc_2026_jun_sb1
python3 tools/manitoba-precalc-40s/pqp/mathpix_fetch_manitoba.py --id pc_2026_jun_sb1 --poll
```

The submit script writes `mathpix/api-cache/mathpix_manifest.json`. The fetch script downloads each completed document into `mathpix/api-cache/<document-id>/`.

Run `mathpix_prepare_manitoba_inputs.py` before submitting. It writes lower-cost page-filtered PDFs under `mathpix/api-inputs/page-filtered/`. The submit script uses those filtered PDFs automatically when present; pass `--input-set original` only if you intentionally want to upload the full original PDFs.

The current final exporter is `tools/manitoba-precalc-40s/pqp/export_manitoba_pqp_mathpix.py`. It uses local Mathpix `lines.json`/`mmd` data and converts LaTeX math to Typst with `mitex` when available.
