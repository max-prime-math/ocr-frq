"""Tests for LaTeX generation from FRQ extractions."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from latex_gen import build_document, render_frq_block, render_text


# ---------------------------------------------------------------------------
# render_text — math normalisation
# ---------------------------------------------------------------------------

def test_render_text_passthrough():
    assert render_text("plain text") == "plain text"


def test_render_text_unicode_minus():
    result = render_text("x − y")
    assert "−" not in result
    assert "-" in result


def test_render_text_unicode_infinity():
    result = render_text("∞")
    assert r"\infty" in result


def test_render_text_escapes_percent():
    result = render_text("50% confidence")
    assert r"\%" in result
    assert "50%" not in result


def test_render_text_already_escaped_percent():
    result = render_text(r"50\% done")
    assert result.count(r"\%") == 1


def test_render_text_balances_open_paren():
    result = render_text(r"value is \(x + 1")
    assert result.count(r"\(") == result.count(r"\)")


def test_render_text_balances_open_bracket():
    result = render_text(r"equation \[x = 1")
    assert result.count(r"\[") == result.count(r"\]")


# ---------------------------------------------------------------------------
# render_frq_block — single question rendering
# ---------------------------------------------------------------------------

def _frq(question_number=1, question="What is x?", solution="x = 1",
         grading_scheme="1 : correct answer", flagged=False, flag_reason=None):
    return {
        "page_type": "frq",
        "skip_reason": None,
        "question_number": question_number,
        "question": question,
        "solution": solution,
        "grading_scheme": grading_scheme,
        "flagged": flagged,
        "flag_reason": flag_reason,
    }


def test_block_contains_section_heading():
    block = render_frq_block(_frq(question_number=3))
    assert r"\section*{Question 3}" in block


def test_block_contains_question_text():
    block = render_frq_block(_frq(question="Find the derivative."))
    assert "Find the derivative." in block


def test_block_contains_solution_env():
    block = render_frq_block(_frq(solution="The answer is 2."))
    assert r"\begin{frqsolution}" in block
    assert r"\end{frqsolution}" in block
    assert "The answer is 2." in block


def test_block_contains_rubric_env():
    block = render_frq_block(_frq(grading_scheme="2 : { 1 : setup / 1 : answer }"))
    assert r"\begin{frqrubric}" in block
    assert r"\end{frqrubric}" in block
    assert "2 : { 1 : setup / 1 : answer }" in block


def test_block_flagged_shows_warning():
    block = render_frq_block(_frq(flagged=True, flag_reason="solution column unclear"))
    assert "Flagged for review" in block
    assert "solution column unclear" in block


def test_block_unflagged_no_warning():
    block = render_frq_block(_frq(flagged=False))
    assert "Flagged for review" not in block


def test_block_missing_solution_shows_placeholder():
    ext = _frq()
    ext["solution"] = None
    block = render_frq_block(ext)
    assert "Solution not extracted" in block


def test_block_missing_grading_scheme_shows_placeholder():
    ext = _frq()
    ext["grading_scheme"] = None
    block = render_frq_block(ext)
    assert "Grading scheme not extracted" in block


def test_block_no_question_number():
    ext = _frq(question_number=None)
    block = render_frq_block(ext)
    assert r"\section*{Question}" in block


# ---------------------------------------------------------------------------
# build_document — full document assembly
# ---------------------------------------------------------------------------

def _page_result(fname="test.pdf", page=0, extraction=None, error=None):
    return {
        "fname": fname,
        "page": page,
        "extraction": extraction or _frq(question_number=page + 1),
        "error": error,
        "pdf_path": f"/tmp/{fname}",
    }


def test_document_has_preamble_and_postamble():
    doc = build_document([_page_result()])
    assert r"\documentclass" in doc
    assert r"\begin{document}" in doc
    assert r"\end{document}" in doc


def test_document_includes_frq_content():
    results = [
        _page_result(page=0, extraction=_frq(question_number=1, question="Q1")),
        _page_result(page=1, extraction=_frq(question_number=2, question="Q2")),
    ]
    doc = build_document(results)
    assert "Q1" in doc
    assert "Q2" in doc


def test_skip_pages_appear_as_comments():
    skip = {
        "page_type": "skip",
        "skip_reason": "title_page",
        "question_number": None,
        "question": None,
        "solution": None,
        "grading_scheme": None,
        "flagged": False,
        "flag_reason": None,
    }
    results = [{"fname": "f.pdf", "page": 0, "extraction": skip, "error": None, "pdf_path": "/tmp/f.pdf"}]
    doc = build_document(results, include_skipped_comments=True)
    assert "% Page skipped: title_page" in doc


def test_skip_pages_omitted_when_comments_disabled():
    skip = {
        "page_type": "skip",
        "skip_reason": "cover_sheet",
        "question_number": None,
        "question": None,
        "solution": None,
        "grading_scheme": None,
        "flagged": False,
        "flag_reason": None,
    }
    results = [{"fname": "f.pdf", "page": 0, "extraction": skip, "error": None, "pdf_path": "/tmp/f.pdf"}]
    doc = build_document(results, include_skipped_comments=False)
    assert "cover_sheet" not in doc


def test_error_pages_appear_as_comments():
    results = [{"fname": "f.pdf", "page": 2, "extraction": None, "error": "network timeout", "pdf_path": "/tmp/f.pdf"}]
    doc = build_document(results)
    assert "% Error on page 3" in doc
    assert "network timeout" in doc


def test_empty_results_produces_valid_document():
    doc = build_document([])
    assert r"\begin{document}" in doc
    assert r"\end{document}" in doc


def test_source_label_in_comment():
    ext = _frq(question_number=1)
    block = render_frq_block(ext, source="myfile.pdf p2")
    assert "% myfile.pdf p2" in block
