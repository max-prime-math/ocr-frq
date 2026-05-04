#!/usr/bin/env python3
"""
Aggressively clean PDFs by keeping ONLY pages with specific headers.
Removes all boilerplate, TOCs, scoring guidelines, etc.
"""

import re
from pathlib import Path
import fitz


class AggressiveCleaner:
    """Remove pages that don't contain key content markers."""

    # Headers that indicate valuable content
    KEEP_PATTERNS = [
        r"Question\s+\d+",  # Question 1, Question 2, etc.
        r"Answer\s+Key\s+for\s+Multiple[- ]Choice",  # MCQ answer key
    ]

    def __init__(self, pdf_path: str):
        """Initialize cleaner with a PDF."""
        self.pdf_path = Path(pdf_path)
        self.doc = fitz.open(self.pdf_path)
        self.original_page_count = len(self.doc)
        self.appendix_c_range = self._extract_appendix_c_range()

    def _extract_appendix_c_range(self) -> tuple[int, int]:
        """
        Extract Appendix C page range by looking for actual content.
        Searches for "Table of Questions by Unit and Learning Outcome" or "Appendix C"
        followed by "Learning Outcome".

        Returns:
            (start_page, end_page) tuple, or (None, None) if not found
        """
        if len(self.doc) < 1:
            return None, None

        appendix_c_start = None
        appendix_c_end = None

        # Search through PDF for Appendix C content marker
        # Look for "Table of Questions by Unit and Learning Outcome" followed by "Unit A:" or similar
        for page_num in range(len(self.doc)):
            text = self.doc[page_num].get_text()

            # Look for the actual Appendix C header (followed by Unit data, not just TOC entry)
            if ("Table of Questions by Unit and Learning Outcome" in text and
                ("Unit A:" in text or "Unit A :" in text)):
                appendix_c_start = page_num + 1  # Convert to 1-indexed
                break

        if appendix_c_start is None:
            return None, None

        # Appendix C goes to end of document (or until we hit another major section)
        # Look for the last page with "Learning Outcome" to find the end
        for page_num in range(len(self.doc) - 1, appendix_c_start - 2, -1):
            text = self.doc[page_num].get_text()
            if "Learning Outcome" in text or "Table of Questions" in text or "Unit" in text:
                appendix_c_end = page_num + 1  # Convert to 1-indexed
                break

        if appendix_c_end is None:
            appendix_c_end = len(self.doc)

        return appendix_c_start, appendix_c_end

    def analyze_pages(self) -> list[dict]:
        """
        Analyze each page to determine if it should be kept.

        Keeps:
        - Pages with "Question N" where N is a digit (actual question headers, not TOC)
        - Pages with "Answer Key for Multiple-Choice"
        - All pages in Appendix C range (determined from TOC)

        Removes:
        - Pages 1-2 (always - title/TOC/blank pages)
        - Pages without content markers

        Returns:
            List of page info dicts with keep/remove status
        """
        pages = []

        for page_num in range(len(self.doc)):
            page = self.doc[page_num]
            text = page.get_text()

            # Always remove pages 1-2 (cover/TOC/blank)
            if page_num < 2:
                pages.append(
                    {
                        "num": page_num + 1,
                        "keep": False,
                        "reason": f"Title/TOC/blank page",
                        "text_length": len(text),
                    }
                )
                continue

            # Check for actual Question headers (not TOC mentions)
            # Pattern: "Question" followed by whitespace and a digit at start of line
            has_question_header = bool(
                re.search(r"^\s*Question\s+\d+", text, re.IGNORECASE | re.MULTILINE)
            )

            # Check for Answer Key as a section header (not in TOC)
            # Should be at start of line and not followed by dots/page numbers (like in TOC)
            has_answer_key = bool(
                re.search(
                    r"^\s*Answer\s+Key\s+for\s+Multiple[- ]Choice\s*$",
                    text,
                    re.IGNORECASE | re.MULTILINE,
                )
            )

            matched_patterns = []
            if has_question_header:
                matched_patterns.append("Question header")
            if has_answer_key:
                matched_patterns.append("Answer Key")

            # Don't keep Appendix C - content is already encoded in question pages
            should_keep = has_question_header or has_answer_key

            pages.append(
                {
                    "num": page_num + 1,
                    "keep": should_keep,
                    "patterns": matched_patterns,
                    "text_length": len(text),
                    "preview": text[:100],
                }
            )

        return pages

    def remove_unmarked_pages(self) -> int:
        """
        Remove all pages that don't match keep patterns.

        Returns:
            Number of pages removed
        """
        pages = self.analyze_pages()

        # Get pages to remove (in reverse order to preserve indices)
        pages_to_remove = sorted(
            [p["num"] - 1 for p in pages if not p["keep"]], reverse=True
        )

        for page_num in pages_to_remove:
            self.doc.delete_page(page_num)

        return len(pages_to_remove)

    def save(self, output_path: str):
        """Save cleaned PDF."""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        self.doc.save(output_path)

    def get_stats(self) -> dict:
        """Get statistics about pages to keep/remove."""
        pages = self.analyze_pages()
        kept = [p for p in pages if p["keep"]]
        removed = [p for p in pages if not p["keep"]]

        return {
            "total": len(pages),
            "kept": len(kept),
            "removed": len(removed),
            "removal_percentage": (len(removed) / len(pages) * 100) if pages else 0,
            "kept_pages": [p["num"] for p in kept],
            "removed_pages": [p["num"] for p in removed],
        }

    def print_report(self, show_details: bool = False):
        """Print analysis report."""
        stats = self.get_stats()

        print(f"\n📊 Aggressive Clean Analysis: {self.pdf_path.name}")
        print("=" * 70)
        print(f"Total pages:        {stats['total']}")
        print(f"Pages to keep:      {stats['kept']} ({stats['kept']}/{stats['total']})")
        print(f"Pages to remove:    {stats['removed']} ({stats['removal_percentage']:.1f}%)")

        if show_details and stats["removed"] > 0:
            print(f"\nPages marked for removal: {stats['removed_pages'][:20]}")
            if len(stats["removed_pages"]) > 20:
                print(f"  ... and {len(stats['removed_pages']) - 20} more")

        if show_details and stats["kept"] > 0:
            print(f"\nPages to keep: {stats['kept_pages'][:20]}")
            if len(stats["kept_pages"]) > 20:
                print(f"  ... and {len(stats['kept_pages']) - 20} more")

    def close(self):
        """Close the PDF."""
        self.doc.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


def aggressively_clean_pdf(pdf_path: str, output_path: str) -> dict:
    """
    Clean a PDF by keeping only pages with key headers.

    Returns:
        Summary dictionary with statistics
    """
    with AggressiveCleaner(pdf_path) as cleaner:
        stats = cleaner.get_stats()
        removed_count = cleaner.remove_unmarked_pages()
        cleaner.save(output_path)

    return {
        "original_pages": stats["total"],
        "kept_pages": stats["kept"],
        "removed_pages": removed_count,
        "removal_percentage": (removed_count / stats["total"] * 100)
        if stats["total"] > 0
        else 0,
        "output_file": output_path,
    }


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python pdf_aggressive_cleaner.py <pdf_file>")
        print("       Keeps only pages with: Question N, Answer Key, or Appendix C")
        sys.exit(1)

    pdf_path = sys.argv[1]

    with AggressiveCleaner(pdf_path) as cleaner:
        cleaner.print_report(show_details=True)
        output = pdf_path.replace(".pdf", "_aggressively_cleaned.pdf")
        removed = cleaner.remove_unmarked_pages()
        cleaner.save(output)

    print(f"\n✓ Saved: {output}")
    print(f"  Pages removed: {removed}")
