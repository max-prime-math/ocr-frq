# Provincial bank Typst conversion review

All 967 questions (2,678 body/choice/solution fields) compile with Typst 0.15.1. All 21 exam PDFs compile. The final horizontal text-margin check reports zero flags and all questions have nonempty solutions. TestGen's full repository importer and canonical local-folder round trip both pass (967 questions, 598 images). No Mathpix API calls were made for this conversion.

Each `mb-pc40s-YYYY-term.pdf` is an exam review document with original question numbers and solutions. Original LaTeX remains in each PQP's `content.*.extensions.latexSource`. PDFs were spot-checked, including January 2014 Q12 and Q28; compilation and margin checks are automated, not a full mathematical proofread.

Six editorial repairs are recorded in `tools/manitoba-precalc-40s/pqp/typst_overrides.json`: the previously missing January 2013 Q32 graph answer (checked against marking-guide physical page 41); January 2015 Q45 menu columns (checked against student-booklet physical page 28); and readable algebraic solutions for June 2017 Q12/Q32, June 2019 Q2 and January 2020 Q12. Other OCR content still warrants review, particularly scoring annotations embedded in equations and diagrams.

The permanent exporter now uses MiTeX WASM and fails on conversion errors rather than passing LaTeX through unchanged. Set `MITEX_WASM_DIR` if `mitex-wasm` is installed somewhere other than `~/dev/typr/node_modules/mitex-wasm`. No native MiTeX binary is required.

To reproduce a staging bank, from the OCR repository:

```sh
python3 tools/manitoba-precalc-40s/pqp/convert_bank_typst.py \
  --bank /home/max/dev/manitoba-precalculus-40s-provincial-exams \
  --pqp-root data/manitoba-precalc-40s/workspace/derived/pqp-mathpix/pqp \
  --out /tmp/provincial-review-new \
  --testgen /home/max/dev/test-generator
```

This writes a separate staging bank, compares the canonical round trip, compiles every field, and generates review PDFs. It does not overwrite the live bank. The command should be used for source-based regeneration; reconcile local editorial edits before applying a new staging bank.

The archived `.typ` files reuse assets in the neighboring `pqp-mathpix/pqp` directories. Recompile them with `derived` as the Typst root.

The refreshed `pqp-mathpix/content-audit-report.json` retains heuristic OCR warnings for review. Some patterns also match valid Typst (alignment `&`, `plus.minus`, and escaped punctuation), so these are not compilation failures. Four solutions retain the `solution_source_pdf_text_requires_review` flag. Rendering validation does not resolve those source-quality checks.
