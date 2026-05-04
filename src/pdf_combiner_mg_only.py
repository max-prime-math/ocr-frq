#!/usr/bin/env python3
"""
Combine ONLY marking guide PDFs (skip student booklets).
Optimized for budget-conscious processing.
"""

import json
from pathlib import Path
from typing import Optional
import fitz


def combine_mg_only(
    base_dir: Path,
    exam_year: Optional[str] = None,
    output_dir: Optional[Path] = None,
) -> dict:
    """
    Combine ONLY marking guide files for a single exam year.

    Supports both structures:
    - Separate: pc_mg1_*.pdf + pc_mg2_*.pdf
    - Combined: pc_mg_*.pdf

    Args:
        base_dir: Directory containing the exam PDFs
        exam_year: Year identifier (e.g., "jan_26"). If None, auto-detects.
        output_dir: Where to save (defaults to base_dir)

    Returns:
        Offset metadata dictionary
    """
    base_dir = Path(base_dir)
    if output_dir is None:
        output_dir = base_dir

    # Auto-detect exam code if not provided
    if exam_year is None:
        # Look for pc_mg*.pdf files
        mg_files = list(base_dir.glob("pc_mg*.pdf"))
        if mg_files:
            # Extract code from first match
            import re
            match = re.search(r"pc_mg[12]?_(.+)\.pdf", mg_files[0].name)
            if match:
                exam_year = match.group(1)
            else:
                raise FileNotFoundError("Could not detect exam year from filenames")
        else:
            raise FileNotFoundError("No pc_mg*.pdf files found")

    # Construct file paths
    mg1 = base_dir / f"pc_mg1_{exam_year}.pdf"
    mg2 = base_dir / f"pc_mg2_{exam_year}.pdf"
    mg_single = base_dir / f"pc_mg_{exam_year}.pdf"

    # Determine which structure
    if mg1.exists() and mg2.exists():
        files = [mg1, mg2]
        labels = ["mg1", "mg2"]
    elif mg_single.exists():
        files = [mg_single]
        labels = ["mg"]
    else:
        raise FileNotFoundError(
            f"No marking guides found for {exam_year}. "
            f"Expected: pc_mg1_{exam_year}.pdf + pc_mg2_{exam_year}.pdf "
            f"or pc_mg_{exam_year}.pdf"
        )

    # Check all files exist
    for f in files:
        if not f.exists():
            raise FileNotFoundError(f"Missing: {f}")

    # Combine PDFs
    combined_doc = fitz.open()
    offsets = {}
    current_page = 0

    for label, pdf_path in zip(labels, files):
        doc = fitz.open(pdf_path)
        page_count = len(doc)

        offsets[label] = {
            "start": current_page + 1,
            "end": current_page + page_count,
            "count": page_count,
            "path": str(pdf_path),
        }

        combined_doc.insert_pdf(doc)
        doc.close()
        current_page += page_count

    # Save combined PDF
    combined_output = output_dir / f"pre-calc-40s_{exam_year}_mg-only.pdf"
    combined_output.parent.mkdir(parents=True, exist_ok=True)
    combined_doc.save(combined_output)
    combined_doc.close()

    # Save metadata
    metadata_output = output_dir / f"pre-calc-40s_{exam_year}_mg-only_offsets.json"
    with open(metadata_output, "w") as f:
        json.dump(offsets, f, indent=2)

    return offsets


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python pdf_combiner_mg_only.py <base_dir> [exam_year]")
        print("Example: python pdf_combiner_mg_only.py ./exams jan_26")
        sys.exit(1)

    base_dir = Path(sys.argv[1])
    exam_year = sys.argv[2] if len(sys.argv) > 2 else None

    try:
        offsets = combine_mg_only(base_dir, exam_year)
        print(f"\n✓ Combined MG-only PDF created")
        print(f"  Offsets: {offsets}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
