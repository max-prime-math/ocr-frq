#!/usr/bin/env python3
"""
Batch combine PDF booklets for multiple exam years.
Generates combined PDFs ready for MathPix upload along with offset metadata.

Supports two directory structures:
1. Subdirectories (each containing exam files): example26/, example27/, etc.
2. Flat structure (files at root): pc_sb1_jan_13.pdf, pc_sb2_jan_13.pdf, etc.
"""

import re
import sys
from pathlib import Path
from src.pdf_combiner import combine_exam_year


def extract_exam_codes(base_dir: Path) -> list[str]:
    """
    Extract unique exam codes from PDF filenames.
    Looks for patterns like jan_13, jun_14, etc. from pc_sb1_*.pdf files.
    """
    codes = set()
    for f in base_dir.glob("pc_sb1_*.pdf"):
        # Extract code like "jan_13" from "pc_sb1_jan_13.pdf"
        match = re.search(r"pc_sb1_(.+)\.pdf", f.name)
        if match:
            codes.add(match.group(1))
    return sorted(codes)


def batch_combine(base_dir: Path, exam_ids: list[str]) -> None:
    """
    Combine PDFs for multiple exam years in batch.

    Args:
        base_dir: Base directory containing exams
        exam_ids: List of exam IDs to process.
                  Can be subdirectory names (e.g., ["example26", "example27"])
                  or exam codes (e.g., ["jan_13", "jun_14"]).
                  If empty, auto-discovers from files/subdirectories.
    """
    base_dir = Path(base_dir)

    if not exam_ids:
        # Auto-discover: process both subdirectories AND root-level files
        subdirs = sorted([d for d in base_dir.iterdir() if d.is_dir() and not d.name.startswith(".")])
        root_codes = extract_exam_codes(base_dir)

        if subdirs and root_codes:
            # Process in mixed mode
            print(f"Found {len(subdirs)} subdirectories and {len(root_codes)} root-level exam codes")
            print("Will process both.\n")

            # Process subdirectories
            successes = []
            failures = []
            for subdir in subdirs:
                try:
                    combine_exam_year(subdir)
                    successes.append(subdir.name)
                except Exception as e:
                    print(f"✗ {subdir.name}: {e}")
                    failures.append(subdir.name)

            # Process root-level exams
            for code in root_codes:
                try:
                    combine_exam_year(base_dir, code)
                    successes.append(code)
                except Exception as e:
                    print(f"✗ {code}: {e}")
                    failures.append(code)

            # Skip the normal loop below
            print("\n" + "=" * 60)
            print(f"Summary: {len(successes)} succeeded, {len(failures)} failed")
            if successes:
                print(f"✓ Successful: {', '.join(successes)}")
            if failures:
                print(f"✗ Failed: {', '.join(failures)}")
            return
        elif subdirs:
            exam_ids = [d.name for d in subdirs]
            mode = "subdirectory"
        elif root_codes:
            exam_ids = root_codes
            mode = "flat"
        else:
            print(f"No exams found in {base_dir}")
            return
    else:
        # Determine mode based on what we're processing
        test_path = base_dir / exam_ids[0]
        mode = "subdirectory" if test_path.is_dir() else "flat"

    print(f"Processing {len(exam_ids)} exam(s) ({mode} mode)...\n")

    successes = []
    failures = []

    for exam_id in exam_ids:
        if mode == "subdirectory":
            exam_dir = base_dir / exam_id
            if not exam_dir.exists():
                print(f"✗ {exam_id}: Directory not found")
                failures.append(exam_id)
                continue
        else:
            # Flat mode: exam_id is the code like "jan_13"
            exam_dir = base_dir
            exam_id_display = exam_id

        try:
            combine_exam_year(exam_dir, exam_id if mode == "flat" else None)
            successes.append(exam_id)
            print()
        except FileNotFoundError as e:
            print(f"✗ {exam_id}: {e}\n")
            failures.append(exam_id)
        except Exception as e:
            print(f"✗ {exam_id}: {type(e).__name__}: {e}\n")
            failures.append(exam_id)

    # Summary
    print("=" * 60)
    print(f"Summary: {len(successes)} succeeded, {len(failures)} failed")
    if successes:
        print(f"✓ Successful: {', '.join(successes)}")
    if failures:
        print(f"✗ Failed: {', '.join(failures)}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python combine_exams.py <base_dir> [exam_year1 exam_year2 ...]")
        print()
        print("Examples:")
        print("  python combine_exams.py example-pdfs/pre-calculus-40s")
        print("  python combine_exams.py example-pdfs/pre-calculus-40s jan_26 june_26")
        sys.exit(1)

    base_dir = Path(sys.argv[1])
    exam_years = sys.argv[2:] if len(sys.argv) > 2 else []

    batch_combine(base_dir, exam_years)
