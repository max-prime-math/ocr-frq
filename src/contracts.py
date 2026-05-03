from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ExamQuestion:
    question_number: int
    question_text: str          # cleaned LaTeX, full question including sub-parts
    figure_paths: list[str]     # relative paths for \includegraphics (e.g. "figures/bc-2018_fig1.jpg")
    calculator_active: bool
    part: str                   # "A" or "B"


@dataclass
class QuestionBlock:
    question_number: int
    year: int
    exam: str                   # "BC"
    form: str                   # "" or "B"
    part: str                   # "A" or "B"
    calculator_active: bool
    question_text: str          # from exam zip
    sg_text: str                # combined solution + rubric from SG zip
    figure_paths: list[str] = field(default_factory=list)
