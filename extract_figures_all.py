#!/usr/bin/env python3
"""
extract_figures_all.py — Process all aggressive-cleaned PDFs to extract figures.

Finds all *_mg-only_cleaned_aggressive.pdf files in a directory, runs figure extraction
for each, and outputs modified PDFs with figures replaced by [figure N] placeholders.

Usage:
    python extract_figures_all.py <base_dir> [--dry-run] [--model MODEL]
"""

import sys
from pathlib import Path

from anthropic import Anthropic

from src.cache import FRQCache
from src.pdf_figure_extractor import preprocess_pdf_figures


def extract_figures_all(base_dir: Path, dry_run: bool = False, model: str = "claude-haiku-4-5-20251001") -> None:
    """
    Find and process all aggressive-cleaned PDFs in base_dir.
    """
    base_dir = Path(base_dir)

    pdfs = sorted(base_dir.glob("pre-calc-40s_*_mg-only_cleaned_aggressive.pdf"))
    pdfs = [p for p in pdfs if "_nofigs" not in p.name]

    if not pdfs:
        print(f"No aggressive-cleaned PDFs found in {base_dir}")
        return

    print(f"Found {len(pdfs)} PDFs to process")
    print("=" * 70)

    if dry_run:
        print("DRY RUN MODE — no figure extraction will be performed\n")
        for pdf_path in pdfs:
            print(f"  {pdf_path.name}")
        print(f"\nTo process, run without --dry-run flag.")
        return

    cache = FRQCache()
    client = Anthropic()
    total_figures = 0
    successes = []

    for pdf_path in pdfs:
        try:
            exam_name = pdf_path.stem.replace("pre-calc-40s_", "").replace("_mg-only_cleaned_aggressive", "")

            output_pdf = str(pdf_path).replace("_mg-only_cleaned_aggressive.pdf", "_mg-only_cleaned_aggressive_nofigs.pdf")
            figures_dir = pdf_path.parent / f"{exam_name}_figures"
            manifest_path = pdf_path.parent / f"{exam_name}_figure_manifest.json"

            print(f"Processing: {exam_name}")
            print(f"  Input:    {pdf_path.name}")
            print(f"  Output:   {Path(output_pdf).name}")
            print(f"  Figures:  {figures_dir}/")

            manifest = preprocess_pdf_figures(
                input_pdf=str(pdf_path),
                output_pdf=output_pdf,
                figures_dir=str(figures_dir),
                manifest_path=str(manifest_path),
                claude_client=client,
                cache=cache,
                dpi=200,
            )

            num_figures = len(manifest["figures"])
            total_figures += num_figures
            successes.append((exam_name, num_figures))

            print(f"  ✓ Extracted {num_figures} figures")
            print(f"  ✓ Manifest: {manifest_path.name}")
            print()

        except Exception as e:
            print(f"  ✗ Error: {e}")
            print()

    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Processed: {len(successes)} exams")
    print(f"Total figures extracted: {total_figures}")

    for exam_name, count in successes:
        print(f"  {exam_name}: {count} figures")


if __name__ == "__main__":
    if "--help" in sys.argv or "-h" in sys.argv or len(sys.argv) < 2:
        print("Usage: python extract_figures_all.py <base_dir> [--dry-run] [--model MODEL]")
        print()
        print("Extracts vector figures from aggressive-cleaned PDFs before MathPix OCR.")
        print("For each PDF, creates:")
        print("  - *_nofigs.pdf (figures replaced with [figure N] placeholders)")
        print("  - {exam}_figures/ (directory with extracted PNG figures)")
        print("  - {exam}_figure_manifest.json (mapping of figure IDs to images)")
        print()
        print("Options:")
        print("  --dry-run          List PDFs that would be processed, don't extract figures")
        print("  --model MODEL      Claude model to use (default: claude-haiku-4-5-20251001)")
        print()
        print("Example:")
        print("  python extract_figures_all.py example-pdfs/pre-calculus-40s --dry-run")
        sys.exit(1 if len(sys.argv) < 2 else 0)

    base_dir = Path(sys.argv[1])
    dry_run = "--dry-run" in sys.argv
    model = "claude-haiku-4-5-20251001"

    if "--model" in sys.argv:
        idx = sys.argv.index("--model")
        if idx + 1 < len(sys.argv):
            model = sys.argv[idx + 1]

    extract_figures_all(base_dir, dry_run=dry_run, model=model)
