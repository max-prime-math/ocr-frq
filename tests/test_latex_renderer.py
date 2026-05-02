import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from latex_pipeline.contracts import FigureRef, QuestionBlock, TableRef
from latex_pipeline.renderer import build_latex_document


def _make_block(**overrides) -> QuestionBlock:
    payload = {
        "block_id": "q01-sgp02",
        "question_number": 1,
        "question_text": "What is 1+1?",
        "solution_text": "It is 2.",
        "grading_text": "1 point for correct answer.",
        "figures": [],
        "tables": [],
        "source_sg_page": 2,
        "source_exam_page": 1,
        "warnings": [],
    }
    payload.update(overrides)
    return QuestionBlock(**payload)


def test_document_uses_exam_class_and_solution_env():
    tex = build_latex_document([_make_block()], set())
    assert r"\documentclass[12pt,addpoints,answers]{exam}" in tex
    assert r"\begin{questions}" in tex
    assert r"\question" in tex
    assert r"\begin{solution}" in tex
    assert r"\textbf{Scoring Guide}\par" in tex


def test_multipart_question_renders_parts_with_partwise_solutions():
    block = _make_block(
        question_text="Find the values. (a) Compute x. (b) Compute y.",
        solution_text="(a) x = 1. (b) y = 2.",
        grading_text="(a) 1 point for x. (b) 1 point for y.",
    )
    tex = build_latex_document([block], set())
    assert r"\begin{parts}" in tex
    assert r"\part Compute x." in tex
    assert r"\part Compute y." in tex
    assert tex.count(r"\begin{solution}") == 1
    assert "Part (a):" in tex
    assert "Part (b):" in tex
    assert r"\(x = 1" in tex
    assert r"\(y = 2" in tex
    assert "Part (a): 1 point for x." in tex
    assert "Part (b): 1 point for y." in tex


def test_renderer_wraps_bare_latex_math_in_prose():
    block = _make_block(
        question_text=r"What are all values of k for which \int_{-3}^{k} x^2 dx = 0?",
        solution_text=r"The interval is $(−\infty, ∞)$.",
    )
    tex = build_latex_document([block], set())
    assert r"for which \(\int_{-3}^{k} x^2 dx = 0\)?" in tex
    assert r"$(-\infty, \infty)$" in tex


def test_question_figures_are_included():
    block = _make_block(
        question_text="See the graph. (a) Compute x.",
        figures=[FigureRef(section="question", file_path="figures/sample.png", caption="Sample graph")],
    )
    tex = build_latex_document([block], set())
    assert r"\includegraphics[width=0.8\linewidth]{figures/sample.png}" in tex
    assert "Sample graph" in tex


def test_grading_text_does_not_wrap_whole_rubric_in_math_mode():
    block = _make_block(grading_text=r"2 points: { 1 : answer, 1 : value of \frac{x}{2} }")
    tex = build_latex_document([block], set())
    assert r"\textbf{Scoring Guide}\par" in tex
    assert r"\(2 points" not in tex
    assert r"\frac{x}{2}" in tex


def test_tables_render_as_tabular_blocks():
    block = _make_block(
        tables=[
            TableRef(
                section="solution",
                headers=["$t$", "People in line"],
                rows=[["0", "20"], ["$t_1$", "3.803"]],
                caption="Table of values",
            )
        ]
    )
    tex = build_latex_document([block], set())
    assert r"\begin{tabular}{|l|l|}" in tex
    assert "Table of values" in tex
    assert r"$t$ & People in line" in tex
