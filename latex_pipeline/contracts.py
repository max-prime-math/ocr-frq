from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class FigureRef:
    section: str
    file_path: str
    caption: str | None = None
    render_width: float | None = None
    render_height: float | None = None


@dataclass(slots=True)
class TableRef:
    section: str
    headers: list[str]
    rows: list[list[str]]
    caption: str | None = None


@dataclass(slots=True)
class QuestionBlock:
    block_id: str
    question_number: int
    question_text: str
    solution_text: str
    grading_text: str
    figures: list[FigureRef] = field(default_factory=list)
    tables: list[TableRef] = field(default_factory=list)
    source_sg_page: int | None = None
    source_exam_page: int | None = None
    warnings: list[str] = field(default_factory=list)


@dataclass(slots=True)
class RunManifest:
    sg_pdf: str
    exam_pdf: str | None
    output_tex: str
    output_pdf: str
    model: str
    compile_ok: bool
    compile_output: str
    skipped_blocks: list[str] = field(default_factory=list)
    unresolved_blocks: list[str] = field(default_factory=list)
