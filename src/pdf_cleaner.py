#!/usr/bin/env python3
"""
Remove identified pages from PDFs and update offset metadata.
Supports both removing specific pages and auto-removing exemplars.
"""

import json
from pathlib import Path
from typing import Optional, Set
import fitz  # PyMuPDF

try:
    from .pdf_page_analyzer import PageAnalyzer
except ImportError:
    from pdf_page_analyzer import PageAnalyzer


class PDFCleaner:
    """Remove pages from PDFs and update metadata."""

    def __init__(self, pdf_path: str, offsets_path: Optional[str] = None):
        """
        Initialize cleaner.

        Args:
            pdf_path: Path to combined PDF
            offsets_path: Path to offsets JSON (optional, for updating metadata)
        """
        self.pdf_path = Path(pdf_path)
        self.offsets_path = Path(offsets_path) if offsets_path else None
        self.doc = fitz.open(self.pdf_path)
        self.original_page_count = len(self.doc)

        # Load offsets if provided
        self.offsets = None
        if self.offsets_path and self.offsets_path.exists():
            with open(self.offsets_path) as f:
                self.offsets = json.load(f)

    def remove_pages(self, page_numbers: Set[int]) -> int:
        """
        Remove pages from PDF (1-indexed).

        Args:
            page_numbers: Set of 1-indexed page numbers to remove

        Returns:
            Number of pages removed
        """
        if not page_numbers:
            return 0

        # Convert to 0-indexed and sort descending (remove from end first)
        pages_to_remove = sorted(
            [p - 1 for p in page_numbers], reverse=True
        )

        for page_num in pages_to_remove:
            self.doc.delete_page(page_num)

        return len(pages_to_remove)

    def remove_exemplars(self) -> tuple[int, list[int]]:
        """
        Automatically detect and remove exemplar pages.

        Returns:
            (count_removed, pages_removed_list)
        """
        analyzer = PageAnalyzer(str(self.pdf_path))
        removable = analyzer.get_removable_pages()
        analyzer.close()

        exemplar_pages = {
            p["num"] for p in removable if p["is_exemplar"]
        }

        removed_count = self.remove_pages(exemplar_pages)
        return removed_count, sorted(exemplar_pages)

    def remove_boilerplate(self) -> tuple[int, list[int]]:
        """
        Automatically detect and remove boilerplate and blank pages.

        Returns:
            (count_removed, pages_removed_list)
        """
        analyzer = PageAnalyzer(str(self.pdf_path))
        removable = analyzer.get_removable_pages()
        analyzer.close()

        boilerplate_pages = {
            p["num"]
            for p in removable
            if p["is_boilerplate"] or p["is_blank"]
        }

        removed_count = self.remove_pages(boilerplate_pages)
        return removed_count, sorted(boilerplate_pages)

    def remove_all_identified(self) -> tuple[int, dict[str, list[int]]]:
        """
        Remove all identified removable pages.

        Returns:
            (total_removed, dict of removal types)
        """
        analyzer = PageAnalyzer(str(self.pdf_path))
        removable = analyzer.get_removable_pages()
        analyzer.close()

        removed_by_type = {
            "exemplar": [],
            "blank": [],
            "image_heavy": [],
            "boilerplate": [],
        }

        for page in removable:
            if page["is_exemplar"]:
                removed_by_type["exemplar"].append(page["num"])
            if page["is_blank"]:
                removed_by_type["blank"].append(page["num"])
            if page["is_image_heavy"]:
                removed_by_type["image_heavy"].append(page["num"])
            if page["is_boilerplate"]:
                removed_by_type["boilerplate"].append(page["num"])

        # Remove all unique pages
        all_pages = set()
        for pages in removed_by_type.values():
            all_pages.update(pages)

        removed_count = self.remove_pages(all_pages)
        return removed_count, removed_by_type

    def update_offsets(self, removed_pages: list[int]) -> dict:
        """
        Update offset metadata after page removal.

        Args:
            removed_pages: List of 1-indexed page numbers that were removed

        Returns:
            Updated offsets dictionary
        """
        if not self.offsets:
            return {}

        removed_set = set(removed_pages)

        # Calculate offset shift for each section
        updated = {}
        for section, info in self.offsets.items():
            # Count how many removed pages were before this section
            pages_removed_before = sum(
                1 for p in removed_pages if p < info["start"]
            )

            # Count how many removed pages were in this section
            pages_removed_in = sum(
                1
                for p in removed_pages
                if info["start"] <= p <= info["end"]
            )

            original_count = info["count"]
            new_count = original_count - pages_removed_in

            updated[section] = {
                "start": info["start"] - pages_removed_before,
                "end": info["start"]
                - pages_removed_before
                + new_count
                - 1,
                "count": new_count,
                "path": info["path"],
                "original_count": original_count,
                "pages_removed": pages_removed_in,
            }

        return updated

    def save(self, output_path: Optional[str] = None):
        """
        Save cleaned PDF.

        Args:
            output_path: Where to save. If None, overwrites original.
        """
        if output_path is None:
            output_path = str(self.pdf_path)

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        self.doc.save(output_path)

    def close(self):
        """Close the PDF document."""
        self.doc.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


def clean_combined_pdf(
    combined_pdf: str,
    offsets_json: Optional[str] = None,
    output_dir: Optional[str] = None,
    remove_types: list[str] = None,
) -> dict:
    """
    Clean a combined PDF and save cleaned version with updated metadata.

    Args:
        combined_pdf: Path to combined PDF
        offsets_json: Path to offsets JSON
        output_dir: Where to save cleaned files (defaults to same dir as PDF)
        remove_types: List of types to remove:
                      ["exemplar", "boilerplate", "blank", "all"]

    Returns:
        Summary dictionary with removal stats
    """
    if remove_types is None:
        remove_types = ["exemplar"]

    pdf_path = Path(combined_pdf)
    if output_dir is None:
        output_dir = pdf_path.parent

    output_dir = Path(output_dir)

    with PDFCleaner(combined_pdf, offsets_json) as cleaner:
        original_count = cleaner.original_page_count

        if "all" in remove_types:
            removed_count, removed_by_type = cleaner.remove_all_identified()
        else:
            # Analyze once, collect all pages to remove, then remove in one batch
            analyzer = PageAnalyzer(str(combined_pdf))
            removable = analyzer.get_removable_pages()
            analyzer.close()

            removed_by_type = {
                "exemplar": [],
                "boilerplate": [],
                "blank": [],
            }
            all_pages_to_remove = set()

            if "exemplar" in remove_types:
                pages = {p["num"] for p in removable if p["is_exemplar"]}
                removed_by_type["exemplar"] = sorted(pages)
                all_pages_to_remove.update(pages)

            if "boilerplate" in remove_types:
                pages = {p["num"] for p in removable if p["is_boilerplate"]}
                removed_by_type["boilerplate"] = sorted(pages)
                all_pages_to_remove.update(pages)

            if "blank" in remove_types:
                pages = {p["num"] for p in removable if p["is_blank"]}
                removed_by_type["blank"] = sorted(pages)
                all_pages_to_remove.update(pages)

            # Remove all at once
            removed_count = cleaner.remove_pages(all_pages_to_remove)

        # Save cleaned PDF
        cleaned_filename = f"{pdf_path.stem}_cleaned.pdf"
        cleaned_path = output_dir / cleaned_filename
        cleaner.save(str(cleaned_path))

        # Update and save offsets
        if "all" not in remove_types:
            all_removed_pages = []
            for pages in removed_by_type.values():
                all_removed_pages.extend(pages)
        else:
            # For "all" mode, removed_by_type is already a dict of lists
            all_removed_pages = []
            for pages in removed_by_type.values():
                all_removed_pages.extend(pages)

        updated_offsets = cleaner.update_offsets(all_removed_pages)

        if offsets_json and updated_offsets:
            offsets_path = Path(offsets_json)
            updated_offsets_path = (
                output_dir / f"{pdf_path.stem}_cleaned_offsets.json"
            )
            with open(updated_offsets_path, "w") as f:
                json.dump(updated_offsets, f, indent=2)

        return {
            "original_pages": original_count,
            "removed_pages": removed_count,
            "remaining_pages": original_count - removed_count,
            "removal_percentage": (
                removed_count / original_count * 100
                if original_count > 0
                else 0
            ),
            "removed_by_type": removed_by_type,
            "cleaned_pdf": str(cleaned_path),
            "cleaned_offsets": (
                str(updated_offsets_path) if updated_offsets else None
            ),
        }


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python pdf_cleaner.py <combined_pdf> [offsets_json]")
        print("       python pdf_cleaner.py <combined_pdf> [offsets_json] --exemplar-only")
        sys.exit(1)

    pdf_path = sys.argv[1]
    offsets_path = sys.argv[2] if len(sys.argv) > 2 else None

    # Quick exemplar removal
    result = clean_combined_pdf(
        pdf_path, offsets_path, remove_types=["exemplar"]
    )

    print("\n" + "=" * 70)
    print(f"Original pages:  {result['original_pages']}")
    print(f"Pages removed:   {result['removed_pages']}")
    print(f"Pages kept:      {result['remaining_pages']}")
    print(f"Reduction:       {result['removal_percentage']:.1f}%")
    print(f"\nCleaned PDF:     {result['cleaned_pdf']}")
    if result["cleaned_offsets"]:
        print(f"Updated offsets: {result['cleaned_offsets']}")
