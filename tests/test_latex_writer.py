"""Tests for LaTeX generation from FRQ extractions."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from latex_writer import build_document, render_frq_block


def _frq(
    question_number=1,
    question="What is x?",
    solution="x = 1",
    grading_scheme="1 point for the correct answer",
    flagged=False,
    flag_reason=None,
    figures=None,
    tables=None,
    unit=None,
    section=None,
    calculator=None,
):
    return {
        "page_type": "frq",
        "skip_reason": None,
        "question_number": question_number,
        "question": question,
        "solution": solution,
        "grading_scheme": grading_scheme,
        "figures": figures or [],
        "tables": tables or [],
        "unit": unit,
        "section": section,
        "calculator": calculator,
        "flagged": flagged,
        "flag_reason": flag_reason,
    }


def _page_result(fname="test.pdf", page=0, extraction=None, error=None):
    return {
        "fname": fname,
        "page": page,
        "extraction": extraction or _frq(question_number=page + 1),
        "error": error,
        "pdf_path": f"/tmp/{fname}",
    }


def test_render_frq_block_escapes_special_chars():
    extraction = _frq(question="100%", solution="50%", grading_scheme="Full credit")
    output = render_frq_block(extraction)
    assert r"100\%" in output
    assert r"50\%" in output


def test_render_frq_block_basic():
    extraction = _frq(question_number=1)
    output = render_frq_block(extraction)
    assert r"\question" in output
    assert r"\begin{solution}" in output
    assert r"\end{solution}" in output


def test_render_frq_block_with_source():
    extraction = _frq()
    output = render_frq_block(extraction, source="exam.pdf p1")
    assert "exam.pdf p1" in output


def test_render_frq_block_flagged():
    extraction = _frq(flagged=True, flag_reason="low confidence")
    output = render_frq_block(extraction)
    assert "Flagged for review" in output
    assert "low confidence" in output


def test_render_frq_block_with_metadata():
    extraction = _frq(unit="Unit 1: Limits", section="Part A", calculator="Calculator active")
    output = render_frq_block(extraction)
    assert "Unit 1: Limits" in output
    assert "Part A" in output
    assert "Calculator active" in output


def test_build_document_single_page():
    results = [_page_result()]
    doc = build_document(results)
    assert r"\documentclass[12pt,addpoints]{exam}" in doc
    assert r"\begin{questions}" in doc
    assert r"\end{questions}" in doc
    assert r"\question" in doc


def test_build_document_multiple_pages():
    results = [
        _page_result(page=0),
        _page_result(page=1, extraction=_frq(question_number=2)),
    ]
    doc = build_document(results)
    assert r"\question" in doc
    assert doc.count(r"\question") == 2


def test_build_document_skipped_pages():
    extraction_skip = {
        "page_type": "skip",
        "skip_reason": "title_page",
    }
    results = [
        _page_result(page=0, extraction=extraction_skip),
        _page_result(page=1),
    ]
    doc = build_document(results, include_skipped_comments=True)
    assert "title_page" in doc
    assert r"\question" in doc


def test_build_document_errors():
    results = [
        _page_result(page=0, error="Failed to extract"),
    ]
    doc = build_document(results)
    assert "Error on page 1" in doc
    assert "Failed to extract" in doc


def test_rubric_in_solution():
    extraction = _frq(solution="x = 1", grading_scheme="1 point")
    output = render_frq_block(extraction)
    assert r"\begin{solution}" in output
    assert "Rubric:" in output
    assert "1 point" in output
    assert r"\end{solution}" in output
    # Rubric should be inside solution
    solution_start = output.index(r"\begin{solution}")
    solution_end = output.index(r"\end{solution}")
    rubric_pos = output.index("Rubric:")
    assert solution_start < rubric_pos < solution_end
