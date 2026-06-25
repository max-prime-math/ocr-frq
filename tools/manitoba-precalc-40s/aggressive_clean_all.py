#!/usr/bin/env python3
"""
Aggressively clean all MG-only PDFs by keeping only content pages.
Removes boilerplate, TOCs, scoring guidelines, and other non-essential pages.
"""

import sys
from pathlib import Path
from src.pdf_aggressive_cleaner import AggressiveCleaner


def aggressive_clean_all(base_dir: Path) -> None:
    """
    Find all cleaned MG-only PDFs and aggressively clean them.
    """
    base_dir = Path(base_dir)

    # Find all mg-only_cleaned.pdf files (not the aggressive ones)
    pdfs = sorted(base_dir.glob("pre-calc-40s_*_mg-only_cleaned.pdf"))
    pdfs = [p for p in pdfs if "_aggressively" not in p.name]

    if not pdfs:
        print(f"No MG-only cleaned PDFs found in {base_dir}")
        return

    print(f"Aggressively cleaning {len(pdfs)} PDFs")
    print("=" * 70)

    total_original = 0
    total_removed = 0
    successes = []

    for pdf_path in pdfs:
        try:
            with AggressiveCleaner(str(pdf_path)) as cleaner:
                stats = cleaner.get_stats()
                removed = cleaner.remove_unmarked_pages()

                output = str(pdf_path).replace(
                    "_mg-only_cleaned.pdf", "_mg-only_cleaned_aggressive.pdf"
                )
                cleaner.save(output)

            exam_name = pdf_path.stem.replace("pre-calc-40s_", "").replace("_mg-only_cleaned", "")
            total_original += stats["total"]
            total_removed += removed

            print(
                f"✓ {exam_name:12s}: "
                f"{stats['total']:3d} → {stats['kept']:3d} pages "
                f"({(removed/stats['total']*100):5.1f}% removed)"
            )

            successes.append(exam_name)

        except Exception as e:
            print(f"✗ {pdf_path.name}: {e}")

    # Summary
    print("\n" + "=" * 70)
    print("AGGRESSIVE CLEAN SUMMARY")
    print("=" * 70)
    print(f"Processed:           {len(successes)} exams")
    print(f"Total pages before:  {total_original:5d}")
    print(f"Total pages removed: {total_removed:5d}")
    print(f"Total pages after:   {total_original - total_removed:5d}")
    print(f"Overall reduction:   {(total_removed/total_original*100):5.1f}%")

    # Calculate combined impact
    print("\n" + "=" * 70)
    print("CUMULATIVE PAGE REDUCTION")
    print("=" * 70)
    original_all = 3592
    sb_pages = 1176
    after_exemplar_removal = int(2416 * 0.695)  # 2416 * (1 - 0.305)
    after_aggressive = total_original - total_removed

    print(f"\n1. Original (SB1 + SB2 + MG): {original_all:5d} pages")
    print(f"2. Remove SB files:            {original_all - sb_pages:5d} pages")
    print(f"3. Remove exemplars:           {after_exemplar_removal:5d} pages")
    print(f"4. Aggressive clean:           {after_aggressive:5d} pages")

    total_savings = original_all - after_aggressive
    total_savings_pct = (total_savings / original_all) * 100

    print(f"\nTotal reduction: {original_all} → {after_aggressive} pages ({total_savings_pct:.1f}%)")

    # Cost analysis
    original_cost = max(0, (original_all - 1000) * 0.0035)
    final_cost = max(0, (after_aggressive - 1000) * 0.0035)
    savings = original_cost - final_cost

    print(f"\nCost impact:")
    print(f"  Original:  ${original_cost:.2f}/month overage")
    print(f"  Final:     ${final_cost:.2f}/month overage")
    print(f"  Savings:   ${savings:.2f}/month")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python aggressive_clean_all.py <base_dir>")
        print()
        print("Keeps only pages with:")
        print("  • Question N")
        print("  • Answer Key for Multiple-Choice Questions")
        print("  • Appendix C")
        print()
        print("Example:")
        print("  python aggressive_clean_all.py example-pdfs/pre-calculus-40s")
        sys.exit(1)

    base_dir = Path(sys.argv[1])
    aggressive_clean_all(base_dir)
