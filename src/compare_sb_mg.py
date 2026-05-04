#!/usr/bin/env python3
"""
Compare Student Booklet and Marking Guide content to determine if
question text is duplicated in the MG.
"""

import re
from pathlib import Path
import fitz


def extract_questions_from_sb(pdf_path: str) -> dict:
    """
    Extract question text from student booklet.

    Returns dict mapping question number to text.
    """
    doc = fitz.open(pdf_path)
    full_text = ""

    for page_num in range(len(doc)):
        full_text += doc[page_num].get_text() + "\n"

    doc.close()

    questions = {}

    # Split by question markers (Q1, Q2, 1., 2., etc.)
    # Look for patterns like "Question 1", "Q1.", or just "1."
    parts = re.split(r'\n\s*(?:Q|Question)?\s*(\d+)\s*[.:\s]', full_text)

    for i in range(1, len(parts), 2):
        if i + 1 < len(parts):
            q_num = int(parts[i])
            q_text = parts[i + 1][:1000]  # First 1000 chars
            questions[q_num] = q_text.strip()

    return questions


def extract_questions_from_mg(pdf_path: str) -> dict:
    """
    Extract question text from marking guide.

    Returns dict mapping question number to text.
    """
    doc = fitz.open(pdf_path)
    full_text = ""

    for page_num in range(len(doc)):
        full_text += doc[page_num].get_text() + "\n"

    doc.close()

    questions = {}

    # Look for "Question N" patterns in marking guide
    parts = re.split(r'(?:Question|Q)\s*(\d+)\s*\n', full_text)

    for i in range(1, len(parts), 2):
        if i + 1 < len(parts):
            q_num = int(parts[i])
            q_text = parts[i + 1]

            # Extract up to "Solution" keyword
            match = re.search(r'(.*?)(?:Solution|Exemplar|Example)', q_text, re.DOTALL)
            if match:
                q_text = match.group(1)

            questions[q_num] = q_text[:800].strip()

    return questions


def compare_documents(sb_path: str, mg_path: str) -> dict:
    """
    Compare SB and MG to see if questions are in both.
    """
    sb_questions = extract_questions_from_sb(sb_path)
    mg_questions = extract_questions_from_mg(mg_path)

    print(f"\n📊 Content Comparison")
    print("=" * 70)
    print(f"Student Booklet: {Path(sb_path).name}")
    print(f"  Found {len(sb_questions)} questions")
    print(f"\nMarking Guide: {Path(mg_path).name}")
    print(f"  Found {len(mg_questions)} questions")

    # Check overlap
    sb_q_nums = set(sb_questions.keys())
    mg_q_nums = set(mg_questions.keys())

    in_both = sb_q_nums & mg_q_nums
    only_in_sb = sb_q_nums - mg_q_nums
    only_in_mg = mg_q_nums - sb_q_nums

    print(f"\n📋 Question Coverage:")
    print(f"  Questions in both: {len(in_both)}")
    print(f"  Questions only in SB: {len(only_in_sb)} {only_in_sb}")
    print(f"  Questions only in MG: {len(only_in_mg)} {only_in_mg}")

    # Compare text for questions in both
    text_matches = 0
    partial_matches = 0

    for q_num in sorted(in_both):
        sb_text = sb_questions[q_num].lower()
        mg_text = mg_questions[q_num].lower()

        # Remove whitespace for comparison
        sb_clean = ' '.join(sb_text.split())
        mg_clean = ' '.join(mg_text.split())

        if sb_clean == mg_clean:
            text_matches += 1
        elif sb_clean in mg_clean or mg_clean in sb_clean:
            partial_matches += 1

    print(f"\n🔍 Text Comparison (for {len(in_both)} shared questions):")
    print(f"  Exact matches: {text_matches}")
    print(f"  Partial matches: {partial_matches}")
    print(f"  Missing/different: {len(in_both) - text_matches - partial_matches}")

    # Show a sample
    if in_both:
        sample_q = sorted(in_both)[0]
        print(f"\n📝 Sample (Question {sample_q}):")
        print(f"\nStudent Booklet:")
        print(f"  {sb_questions[sample_q][:150]}...")
        print(f"\nMarking Guide:")
        print(f"  {mg_questions[sample_q][:150]}...")

    return {
        "sb_questions": len(sb_questions),
        "mg_questions": len(mg_questions),
        "in_both": len(in_both),
        "only_in_sb": only_in_sb,
        "only_in_mg": only_in_mg,
        "text_matches": text_matches,
        "partial_matches": partial_matches,
    }


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage: python compare_sb_mg.py <sb_pdf> <mg_pdf>")
        sys.exit(1)

    result = compare_documents(sys.argv[1], sys.argv[2])

    # Summary recommendation
    print("\n" + "=" * 70)
    print("📌 RECOMMENDATION:")
    if result["in_both"] == result["sb_questions"] and result["text_matches"] + result["partial_matches"] == result["in_both"]:
        print("✓ Marking guide has all questions from SB")
        print("  → You can SKIP the student booklet!")
    else:
        print("⚠ Some questions or details only in SB")
        print("  → Keep student booklet for complete coverage")
