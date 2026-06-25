#!/usr/bin/env python3
"""
Full pipeline: Combine MG-only files, then clean all exemplars.
Creates optimized PDFs ready for MathPix with minimal page count.
"""

import sys
import re
from pathlib import Path
from src.pdf_combiner_mg_only import combine_mg_only
from src.pdf_cleaner import clean_combined_pdf


def process_all_exams(base_dir: Path) -> None:
    """
    Process all exam years: combine MG-only, then clean.
    """
    base_dir = Path(base_dir)

    # Extract exam codes from filenames
    exam_codes = set()
    for f in base_dir.glob("pc_mg*.pdf"):
        match = re.search(r"pc_mg[12]?_(.+)\.pdf", f.name)
        if match:
            exam_codes.add(match.group(1))

    exam_codes = sorted(exam_codes)

    if not exam_codes:
        print(f"No exam files found in {base_dir}")
        return

    print(f"Processing {len(exam_codes)} exam years (MG-only mode)")
    print("=" * 70)

    total_original = 0
    total_removed = 0
    successes = []
    failures = []

    for exam_code in exam_codes:
        try:
            # Step 1: Combine MG files
            combine_mg_only(base_dir, exam_code)

            # Find the combined PDF we just created
            combined_pdf = base_dir / f"pre-calc-40s_{exam_code}_mg-only.pdf"
            offsets_json = base_dir / f"pre-calc-40s_{exam_code}_mg-only_offsets.json"

            # Step 2: Clean it
            result = clean_combined_pdf(
                str(combined_pdf),
                str(offsets_json),
                output_dir=str(base_dir),
                remove_types=["exemplar"],
            )

            total_original += result["original_pages"]
            total_removed += result["removed_pages"]

            print(
                f"✓ {exam_code:12s}: "
                f"{result['original_pages']:3d} → {result['remaining_pages']:3d} pages "
                f"({result['removal_percentage']:5.1f}% removed)"
            )

            successes.append(exam_code)

        except Exception as e:
            print(f"✗ {exam_code}: {type(e).__name__}: {e}")
            failures.append(exam_code)

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY - MG-ONLY PIPELINE")
    print("=" * 70)
    print(f"Total original MG pages:     {total_original:5d}")
    print(f"Total pages removed:         {total_removed:5d}")
    print(f"Total pages remaining:       {total_original - total_removed:5d}")
    if total_original > 0:
        reduction_pct = (total_removed / total_original) * 100
        print(f"Overall reduction:           {reduction_pct:5.1f}%")

    print()

    # Budget impact
    original_total = 3592  # From earlier analysis
    sb_pages = 1176
    remaining_cost = max(0, (total_original - 1000) * 0.0035)
    cleaned_cost = max(0, (total_original - total_removed - 1000) * 0.0035)

    print("BUDGET IMPACT:")
    print(f"  Original (SB + SB + MG): {original_total} pages → ${original_total * 0.0035:.2f}")
    print(f"  MG-only (raw):           {total_original} pages → ${remaining_cost:.2f} overage")
    print(f"  MG-only (cleaned):       {total_original - total_removed} pages → ${cleaned_cost:.2f} overage")
    print(f"  Total savings:           ${max(0, original_total * 0.0035) - cleaned_cost:.2f}/month")

    print()
    print(f"Results: {len(successes)} succeeded, {len(failures)} failed")
    if failures:
        print(f"Failed: {', '.join(failures)}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python combine_and_clean_mg_only.py <base_dir>")
        print()
        print("This script:")
        print("  1. Combines ONLY marking guide files (skips student booklets)")
        print("  2. Removes exemplar/student work pages")
        print("  3. Produces cleaned PDFs ready for MathPix")
        print()
        print("Example:")
        print("  python combine_and_clean_mg_only.py example-pdfs/pre-calculus-40s")
        sys.exit(1)

    base_dir = Path(sys.argv[1])
    process_all_exams(base_dir)
