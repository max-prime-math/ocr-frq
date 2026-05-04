#!/usr/bin/env python3
"""
Analyze PDF pages to identify removable content:
- Exemplar pages (student work examples)
- Blank/near-blank pages
- Image-heavy pages
- Boilerplate pages (title, instructions, formula sheets, etc.)
"""

import re
from pathlib import Path
from typing import Optional
import fitz  # PyMuPDF


class PageAnalyzer:
    """Analyze pages in a PDF for removable content."""

    # Keywords that indicate exemplar/student work pages
    EXEMPLAR_KEYWORDS = [
        "exemplar",
        "student response",
        "student work",
        "sample answer",
        "student solution",
    ]

    # Keywords for boilerplate pages
    BOILERPLATE_KEYWORDS = [
        "formula sheet",
        "reference sheet",
        "terminology",
        "definitions",
        "instructions to students",
        "exam instructions",
        "marking guide instructions",
    ]

    # Thresholds
    BLANK_PAGE_THRESHOLD = 500  # chars of text = blank
    IMAGE_HEAVY_THRESHOLD = 5  # more than 5 images
    LOW_TEXT_RATIO = 0.1  # less than 10% of page area has text

    def __init__(self, pdf_path: str):
        """Initialize analyzer with a PDF."""
        self.pdf_path = Path(pdf_path)
        self.doc = fitz.open(self.pdf_path)
        self.pages = []
        self._analyze_all_pages()

    def _analyze_all_pages(self):
        """Analyze all pages in the PDF."""
        for page_num in range(len(self.doc)):
            page = self.doc[page_num]
            text = page.get_text()
            images = page.get_images()

            # Detect characteristics
            is_blank = len(text) < self.BLANK_PAGE_THRESHOLD
            is_image_heavy = len(images) > self.IMAGE_HEAVY_THRESHOLD
            is_exemplar = any(
                kw in text.lower() for kw in self.EXEMPLAR_KEYWORDS
            )
            is_boilerplate = any(
                kw in text.lower() for kw in self.BOILERPLATE_KEYWORDS
            )

            self.pages.append(
                {
                    "num": page_num + 1,
                    "text_length": len(text),
                    "image_count": len(images),
                    "is_blank": is_blank,
                    "is_image_heavy": is_image_heavy,
                    "is_exemplar": is_exemplar,
                    "is_boilerplate": is_boilerplate,
                    "text_preview": text[:200],
                }
            )

    def get_removable_pages(self) -> list[dict]:
        """Return list of pages flagged for removal."""
        removable = []
        for page in self.pages:
            reasons = []

            if page["is_exemplar"]:
                reasons.append("exemplar")
            if page["is_blank"]:
                reasons.append("blank")
            if page["is_image_heavy"]:
                reasons.append("image-heavy")
            if page["is_boilerplate"]:
                reasons.append("boilerplate")

            if reasons:
                page["removal_reasons"] = reasons
                removable.append(page)

        return removable

    def get_stats(self) -> dict:
        """Get overall statistics."""
        removable = self.get_removable_pages()
        return {
            "total_pages": len(self.pages),
            "removable_pages": len(removable),
            "pages_to_keep": len(self.pages) - len(removable),
            "removal_percentage": (
                len(removable) / len(self.pages) * 100
                if self.pages
                else 0
            ),
            "exemplar_pages": sum(
                1 for p in self.pages if p["is_exemplar"]
            ),
            "blank_pages": sum(1 for p in self.pages if p["is_blank"]),
            "image_heavy_pages": sum(
                1 for p in self.pages if p["is_image_heavy"]
            ),
            "boilerplate_pages": sum(
                1 for p in self.pages if p["is_boilerplate"]
            ),
        }

    def print_report(self, show_all: bool = False):
        """Print analysis report."""
        stats = self.get_stats()
        removable = self.get_removable_pages()

        print(f"\n📊 Page Analysis: {self.pdf_path.name}")
        print("=" * 70)
        print(f"Total pages:        {stats['total_pages']}")
        print(f"Pages to remove:    {stats['removable_pages']} ({stats['removal_percentage']:.1f}%)")
        print(f"Pages to keep:      {stats['pages_to_keep']}")
        print()
        print("Breakdown by type:")
        print(f"  • Exemplar pages:    {stats['exemplar_pages']}")
        print(f"  • Blank pages:       {stats['blank_pages']}")
        print(f"  • Image-heavy:       {stats['image_heavy_pages']}")
        print(f"  • Boilerplate:       {stats['boilerplate_pages']}")

        if removable:
            print("\nPages flagged for removal:")
            for page in removable[:20]:  # Show first 20
                reasons_str = ", ".join(page["removal_reasons"])
                print(f"  Page {page['num']:3d}: {reasons_str}")
                if page["is_exemplar"]:
                    print(
                        f"           Preview: {page['text_preview'][:60]}..."
                    )
            if len(removable) > 20:
                print(f"  ... and {len(removable) - 20} more")
        else:
            print("\n✓ No pages flagged for removal")

    def close(self):
        """Close the PDF document."""
        self.doc.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python pdf_page_analyzer.py <pdf_file>")
        sys.exit(1)

    with PageAnalyzer(sys.argv[1]) as analyzer:
        analyzer.print_report()
