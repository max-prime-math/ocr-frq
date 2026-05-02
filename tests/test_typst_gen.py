"""Tests for Typst generation from FRQ extractions."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import typst_gen
from typst_gen import build_document, render_frq_block, render_text


def _frq(
    question_number=1,
    question="What is x?",
    solution="x = 1",
    grading_scheme="1 point for the correct answer",
    flagged=False,
    flag_reason=None,
    figures=None,
    tables=None,
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
        "unit": None,
        "section": None,
        "calculator": None,
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


def test_render_text_passthrough():
    assert render_text("plain text") == "plain text"


def test_render_text_fixes_common_ocr_splits():
    text = "Use $di f y/di f x$ and $c os(x) + ta n(x)$."
    rendered = render_text(text)
    assert "di f" not in rendered
    assert "c os" not in rendered
    assert "ta n" not in rendered
    assert "dif y/dif x" in rendered
    assert "cos(x) + tan(x)" in rendered


def test_render_text_removes_stray_asterisks():
    rendered = render_text("Compare $x * y$ with $c * os(x)$.")
    assert "*" not in rendered
    assert "x y" in rendered
    assert "cos(x)" in rendered


def test_render_text_expands_kx():
    rendered = render_text("Let $kx^2 + ky$ be the model.")
    assert "$k x^2 + k y$" in rendered


def test_render_text_expands_digit_prefixed_kx():
    rendered = render_text("Perimeter is $k + integral_0^k sqrt(1 + (2kx - 3x^2)^2) dif x$.")
    assert "2 k x" in rendered
    assert "3 x^2" in rendered


def test_build_document_repairs_trailing_unit_exponent():
    doc = build_document([_page_result(extraction=_frq(
        question="(a) $a(7.5) = v'(7.5) = (v(8) - v(7))/(8 - 7) = -0.1$ miles/minute$^2$"
    ))])
    assert '$text("miles/minute")^2$' in doc


def test_question_parts_render_as_native_enum():
    block = render_frq_block(_frq(question="(a) Find $f(x)$.\n(b) Explain the result."))
    assert '#enum(numbering: "(a)"' in block
    assert "[\n    Find $f(x)$." in block
    assert "[\n    Explain the result." in block


def test_question_table_renders_as_typst_table():
    tables = [{
        "section": "question",
        "headers": ["x", "f(x)"],
        "rows": [["1", "2"], ["3", "4"]],
        "caption": "values",
    }]
    block = render_frq_block(_frq(tables=tables))
    assert "#table(" in block
    assert "[*x*]," in block
    assert "[4]," in block


def test_figures_use_page_relative_width_and_omit_captions():
    figures = [{
        "section": "question",
        "x": 0.1,
        "y": 0.2,
        "width": 0.25,
        "height": 0.2,
        "caption": "Graph of f",
        "file_path": "figures/q1.png",
        "render_width": 0.25,
    }]
    block = render_frq_block(_frq(figures=figures))
    assert 'image("figures/q1.png", width: 25.0%)' in block
    assert "caption:" not in block


def test_block_contains_solution_and_rubric_wrappers():
    block = render_frq_block(_frq(solution="The answer is 2.", grading_scheme="1 point"))
    assert "#solution-block[" in block
    assert "#rubric-block[" in block
    assert "The answer is 2." in block
    assert "1 point" in block


def test_block_flagged_shows_warning():
    block = render_frq_block(_frq(flagged=True, flag_reason="solution column unclear"))
    assert "Flagged for review" in block
    assert "solution column unclear" in block


def test_document_has_preamble():
    doc = build_document([_page_result()])
    assert '#set document(title: "AP Exam Scoring Guidelines")' in doc
    assert '#set page(paper: "us-letter"' in doc


def test_document_includes_frq_content():
    doc = build_document([
        _page_result(page=0, extraction=_frq(question_number=1, question="Q1")),
        _page_result(page=1, extraction=_frq(question_number=2, question="Q2")),
    ])
    assert "= Question 1" in doc
    assert "= Question 2" in doc
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
        "figures": [],
        "tables": [],
        "unit": None,
        "section": None,
        "calculator": None,
        "flagged": False,
        "flag_reason": None,
    }
    doc = build_document([{
        "fname": "f.pdf",
        "page": 0,
        "extraction": skip,
        "error": None,
        "pdf_path": "/tmp/f.pdf",
    }], include_skipped_comments=True)
    assert "// Page 1 skipped: title_page" in doc


def test_error_pages_appear_as_comments():
    doc = build_document([{
        "fname": "f.pdf",
        "page": 2,
        "extraction": None,
        "error": "network timeout",
        "pdf_path": "/tmp/f.pdf",
    }])
    assert "// Error on page 3: network timeout" in doc


def test_compile_loop_repairs_unclosed_align_math(monkeypatch):
    def fake_validate(text: str):
        if "#align(center)[$ integral_0^1 f(x) dif x $]" in text:
            return None
        if "#align(center)[ integral_0^1 f(x) dif x ]" in text:
            return "error: unclosed delimiter\n  --> output.typ:4:20"
        return None

    monkeypatch.setattr(typst_gen, "_validate_typst_document", fake_validate)

    repaired, err, attempts = typst_gen._compile_with_repair("#align(center)[ integral_0^1 f(x) dif x ]\n", max_attempts=2)

    assert err is None
    assert attempts >= 1
    assert "#align(center)[$ integral_0^1 f(x) dif x $]" in repaired
