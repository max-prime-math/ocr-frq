from __future__ import annotations

from collections.abc import Iterable
import re

from .contracts import FigureRef, QuestionBlock, TableRef


_MARKDOWN_TABLE_RE = re.compile(r"(?:^|\n)(?:\|.*\|\n?)+", re.MULTILINE)
_ARRAY_TABLE_RE = re.compile(r"\\begin\{array\}.*?\\end\{array\}", re.DOTALL)


def _strip_markdown_tables(text: str) -> str:
    cleaned = _MARKDOWN_TABLE_RE.sub("\n", text)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned.strip()


def _strip_embedded_table_blocks(text: str) -> str:
    cleaned = _ARRAY_TABLE_RE.sub(" ", text)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned.strip()


def merge_blocks(sg_results: Iterable[dict], exam_questions_by_num: dict[int, dict]) -> list[QuestionBlock]:
    blocks: list[QuestionBlock] = []

    for row in sg_results:
        extraction = row.get("extraction") or {}
        if extraction.get("page_type") != "frq":
            continue
        qnum = extraction.get("question_number")
        if qnum is None:
            continue

        exam_q = exam_questions_by_num.get(int(qnum), {})
        prompt = (exam_q.get("question") or extraction.get("question") or "").strip()
        solution = (extraction.get("solution") or "").strip()
        grading = (extraction.get("grading_scheme") or "").strip()

        figures: list[FigureRef] = []
        tables: list[TableRef] = []
        for fig in extraction.get("figures") or []:
            file_path = fig.get("file_path")
            if file_path:
                figures.append(
                    FigureRef(
                        section=str(fig.get("section") or "question"),
                        file_path=str(file_path),
                        caption=fig.get("caption"),
                        render_width=float(fig.get("render_width")) if fig.get("render_width") is not None else (float(fig.get("width")) if fig.get("width") is not None else None),
                        render_height=float(fig.get("render_height")) if fig.get("render_height") is not None else (float(fig.get("height")) if fig.get("height") is not None else None),
                    )
                )

        for table in extraction.get("tables") or []:
            tables.append(
                TableRef(
                    section=str(table.get("section") or "question"),
                    headers=[str(item) for item in table.get("headers") or []],
                    rows=[[str(cell) for cell in row] for row in table.get("rows") or []],
                    caption=table.get("caption"),
                )
            )

        for table in exam_q.get("tables") or []:
            tables.append(
                TableRef(
                    section="question",
                    headers=[str(item) for item in table.get("headers") or []],
                    rows=[[str(cell) for cell in row] for row in table.get("rows") or []],
                    caption=table.get("caption"),
                )
            )

        if any(table.section == "question" for table in tables):
            prompt = _strip_markdown_tables(prompt)
            prompt = _strip_embedded_table_blocks(prompt)
        if any(table.section == "solution" for table in tables):
            solution = _strip_markdown_tables(solution)
            solution = _strip_embedded_table_blocks(solution)
        if any(table.section == "grading_scheme" for table in tables):
            grading = _strip_markdown_tables(grading)
            grading = _strip_embedded_table_blocks(grading)

        for fig in exam_q.get("figures") or []:
            file_path = fig.get("file_path")
            if file_path:
                figures.append(
                    FigureRef(
                        section="question",
                        file_path=str(file_path),
                        caption=fig.get("caption"),
                        render_width=float(fig.get("render_width")) if fig.get("render_width") is not None else (float(fig.get("width")) if fig.get("width") is not None else None),
                        render_height=float(fig.get("render_height")) if fig.get("render_height") is not None else (float(fig.get("height")) if fig.get("height") is not None else None),
                    )
                )

        seen_paths: set[str] = set()
        deduped_figures: list[FigureRef] = []
        for fig in figures:
            if fig.file_path in seen_paths:
                continue
            seen_paths.add(fig.file_path)
            deduped_figures.append(fig)
        figures = deduped_figures

        block_id = f"q{int(qnum):02d}-sgp{int(row.get('page', 0)) + 1:02d}"
        warnings: list[str] = []
        if not prompt:
            warnings.append("missing_prompt")
        if not solution:
            warnings.append("missing_solution")
        if not grading:
            warnings.append("missing_grading")

        blocks.append(
            QuestionBlock(
                block_id=block_id,
                question_number=int(qnum),
                question_text=prompt,
                solution_text=solution,
                grading_text=grading,
                figures=figures,
                tables=tables,
                source_sg_page=int(row.get("page", 0)) + 1,
                source_exam_page=None,
                warnings=warnings,
            )
        )

    if blocks:
        return blocks

    fallback_qnum = 1
    for row in sg_results:
        extraction = row.get("extraction") or {}
        page = int(row.get("page", 0)) + 1
        prompt = (extraction.get("question") or "").strip()
        solution = (extraction.get("solution") or "").strip()
        grading = (extraction.get("grading_scheme") or "").strip()
        text_score = sum(1 for item in (prompt, solution, grading) if len(item) >= 12)
        if text_score == 0:
            continue

        block_id = f"fallback-p{page:02d}"
        blocks.append(
            QuestionBlock(
                block_id=block_id,
                question_number=fallback_qnum,
                question_text=prompt or "[Question text recovery failed on this page]",
                solution_text=solution or "[Solution text recovery failed on this page]",
                grading_text=grading or "[Grading text recovery failed on this page]",
                figures=[],
                tables=[],
                source_sg_page=page,
                source_exam_page=None,
                warnings=["fallback_block"],
            )
        )
        fallback_qnum += 1

    return blocks
