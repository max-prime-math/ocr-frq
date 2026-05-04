#!/usr/bin/env python3
"""
Combine multiple PDFs into a single document while tracking page offsets.
Useful for batch uploading to MathPix while maintaining source attribution.
"""

import json
from pathlib import Path
from typing import Optional
import fitz  # PyMuPDF


def combine_pdfs(
    pdf_files: list[str],
    output_path: str,
    metadata_path: Optional[str] = None,
    labels: Optional[list[str]] = None,
) -> dict:
    """
    Combine multiple PDFs into one and track page offsets for each source.

    Args:
        pdf_files: List of paths to PDF files to combine
        output_path: Path for the combined output PDF
        metadata_path: Path for the offset metadata JSON (optional)
        labels: List of labels for each PDF (defaults to filenames)

    Returns:
        Dictionary mapping labels to page ranges:
        {
            "sb1": {"start": 1, "end": 4, "path": "..."},
            "sb2": {"start": 5, "end": 8, "path": "..."},
            ...
        }
    """
    if not pdf_files:
        raise ValueError("At least one PDF file must be provided")

    if labels is None:
        labels = [Path(f).stem for f in pdf_files]

    if len(labels) != len(pdf_files):
        raise ValueError("Number of labels must match number of PDFs")

    combined_doc = fitz.open()
    offsets = {}
    current_page = 0

    for label, pdf_path in zip(labels, pdf_files):
        pdf_path = Path(pdf_path)
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF not found: {pdf_path}")

        doc = fitz.open(pdf_path)
        page_count = len(doc)

        offsets[label] = {
            "start": current_page + 1,  # 1-indexed for readability
            "end": current_page + page_count,
            "count": page_count,
            "path": str(pdf_path),
        }

        combined_doc.insert_pdf(doc)
        doc.close()
        current_page += page_count

    # Save combined PDF
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    combined_doc.save(output_path)
    combined_doc.close()

    # Save metadata if requested
    if metadata_path:
        metadata_path = Path(metadata_path)
        metadata_path.parent.mkdir(parents=True, exist_ok=True)
        with open(metadata_path, "w") as f:
            json.dump(offsets, f, indent=2)

    return offsets


def auto_detect_exam_code(base_dir: Path) -> str:
    """
    Auto-detect exam code from existing PDF files.
    Looks for files matching pc_sb1_*.pdf pattern.
    """
    for f in base_dir.glob("pc_sb1_*.pdf"):
        # Extract the exam code (e.g., "jan_26" from "pc_sb1_jan_26.pdf")
        return f.stem.replace("pc_sb1_", "")
    raise FileNotFoundError("No pc_sb1_*.pdf files found in directory")


def combine_exam_year(
    base_dir: Path,
    exam_year: Optional[str] = None,
    output_dir: Optional[Path] = None,
) -> dict:
    """
    Combine all booklets for a single exam year.
    Supports two naming conventions:
    - Separate: pc_sb1_*.pdf, pc_sb2_*.pdf, pc_mg1_*.pdf, pc_mg2_*.pdf (4 files)
    - Combined: pc_sb1_*.pdf, pc_sb2_*.pdf, pc_mg_*.pdf (3 files)

    Args:
        base_dir: Directory containing the exam PDFs
        exam_year: Year identifier (e.g., "jan_26"). If None, auto-detects from files.
        output_dir: Where to save combined PDF and metadata (defaults to base_dir)

    Returns:
        Offset metadata dictionary
    """
    base_dir = Path(base_dir)
    if output_dir is None:
        output_dir = base_dir

    # Auto-detect exam code if not provided
    if exam_year is None:
        exam_year = auto_detect_exam_code(base_dir)

    # Construct file paths - try separate mg1/mg2 first, fall back to single mg
    sb1 = base_dir / f"pc_sb1_{exam_year}.pdf"
    sb2 = base_dir / f"pc_sb2_{exam_year}.pdf"
    mg1 = base_dir / f"pc_mg1_{exam_year}.pdf"
    mg2 = base_dir / f"pc_mg2_{exam_year}.pdf"
    mg_single = base_dir / f"pc_mg_{exam_year}.pdf"

    # Determine which structure we have
    if mg1.exists() and mg2.exists():
        files = [sb1, sb2, mg1, mg2]
        labels = ["sb1", "sb2", "mg1", "mg2"]
    elif mg_single.exists():
        files = [sb1, sb2, mg_single]
        labels = ["sb1", "sb2", "mg"]
    else:
        raise FileNotFoundError(
            f"Missing marking guide(s): need either "
            f"pc_mg1_{exam_year}.pdf + pc_mg2_{exam_year}.pdf "
            f"or pc_mg_{exam_year}.pdf"
        )

    # Check all files exist
    for f in files:
        if not f.exists():
            raise FileNotFoundError(f"Missing: {f}")

    combined_output = output_dir / f"pre-calc-40s_{exam_year}_combined.pdf"
    metadata_output = output_dir / f"pre-calc-40s_{exam_year}_offsets.json"

    print(f"Combining PDFs for {exam_year}...")
    offsets = combine_pdfs(
        [str(f) for f in files],
        str(combined_output),
        str(metadata_output),
        labels,
    )

    print(f"✓ Combined PDF: {combined_output}")
    print(f"✓ Metadata: {metadata_output}")
    print("\nPage ranges:")
    for label, info in offsets.items():
        print(f"  {label:4s}: pages {info['start']:3d}-{info['end']:3d} ({info['count']} pages)")

    return offsets


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage: python pdf_combiner.py <base_dir> <exam_year>")
        print("Example: python pdf_combiner.py ./example-pdfs/pre-calculus-40s jan_26")
        sys.exit(1)

    base_dir = Path(sys.argv[1])
    exam_year = sys.argv[2]

    try:
        combine_exam_year(base_dir, exam_year)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
