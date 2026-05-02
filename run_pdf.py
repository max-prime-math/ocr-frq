"""
run_pdf.py — CLI runner for OCR-FRQ.

Usage:
    python run_pdf.py SG-BC-2009.pdf
"""

import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

import anthropic
from cache import FRQCache
from extractor import extract_page
from renderer import page_count, render_page, save_temp_image
from typst_gen import build_document
from typst_repair import make_typst_repair_callback


def main() -> None:
    parser = argparse.ArgumentParser(description="OCR-FRQ: extract FRQ PDFs to Typst.")
    parser.add_argument("pdf", nargs="+", help="Input PDF file(s).")
    parser.add_argument("--output", default="output.typ", help="Output .typ file.")
    parser.add_argument("--model", default="claude-haiku-4-5", help="Claude model ID.")
    parser.add_argument("--cache", default="cache/frq", help="Cache directory.")
    parser.add_argument("--force", action="store_true", help="Bypass cache.")
    parser.add_argument("--repair", action="store_true", help="Use a second Claude pass for suspicious Typst spans and compile failures.")
    args = parser.parse_args()

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY not set.", file=sys.stderr)
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)
    cache = FRQCache(args.cache)
    repair_callback = make_typst_repair_callback(
        client,
        args.model,
        enable_span_repair=args.repair,
        enable_document_repair=args.repair,
    ) if args.repair else None

    all_results: list[dict] = []
    usage_log: list[dict] = []

    for pdf_path in args.pdf:
        fname = Path(pdf_path).name
        n = page_count(pdf_path)
        print(f"{fname}: {n} pages")

        for page_idx in range(n):
            print(f"  page {page_idx + 1}/{n} ...", end=" ", flush=True)
            try:
                img = render_page(pdf_path, page_idx, dpi=220)
                tmp = save_temp_image(img)
                try:
                    extraction = extract_page(
                        tmp,
                        client=client,
                        cache=cache,
                        force=args.force,
                        model=args.model,
                        usage_out=usage_log,
                    )
                finally:
                    Path(tmp).unlink(missing_ok=True)

                ptype = extraction.get("page_type", "?")
                qnum = extraction.get("question_number")
                flagged = extraction.get("flagged", False)
                tag = f"Q{qnum}" if qnum else ptype
                flag_marker = " [FLAGGED]" if flagged else ""
                print(f"{tag}{flag_marker}")

                all_results.append({
                    "fname": fname,
                    "page": page_idx,
                    "extraction": extraction,
                    "error": None,
                    "pdf_path": pdf_path,
                })

            except Exception as exc:
                print(f"ERROR: {exc}")
                all_results.append({
                    "fname": fname,
                    "page": page_idx,
                    "extraction": None,
                    "error": str(exc),
                    "pdf_path": pdf_path,
                })

    # Stats
    frq = [r for r in all_results if not r["error"] and r.get("extraction", {}).get("page_type") == "frq"]
    skipped = [r for r in all_results if not r["error"] and r.get("extraction", {}).get("page_type") == "skip"]
    flagged = [r for r in frq if r["extraction"].get("flagged")]
    errors = [r for r in all_results if r["error"]]

    print(f"\nFRQ pages: {len(frq)}  Skipped: {len(skipped)}  Flagged: {len(flagged)}  Errors: {len(errors)}")

    if usage_log:
        input_tok = sum(u.get("input_tokens", 0) for u in usage_log)
        output_tok = sum(u.get("output_tokens", 0) for u in usage_log)
        cache_read = sum(u.get("cache_read_input_tokens", 0) for u in usage_log)
        cache_write = sum(u.get("cache_creation_input_tokens", 0) for u in usage_log)
        print(f"API calls: {len(usage_log)}  tokens in/out: {input_tok}/{output_tok}  cache r/w: {cache_read}/{cache_write}")
    else:
        print("All pages served from cache.")

    typst_content = build_document(all_results, repair_callback=repair_callback)
    Path(args.output).write_text(typst_content, encoding="utf-8")
    print(f"\nOutput written to {args.output}")


if __name__ == "__main__":
    main()
