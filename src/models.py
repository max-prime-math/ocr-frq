"""
models.py — TypedDict definitions for FRQ extraction results.
"""

from typing import Literal, Optional, TypedDict


class FigureInfo(TypedDict):
    section: Literal["question", "solution", "grading_scheme"]
    x: float
    y: float
    width: float
    height: float
    caption: Optional[str]
    file_path: str


class TableInfo(TypedDict):
    section: Literal["question", "solution", "grading_scheme"]
    headers: list[str]
    rows: list[list[str]]
    caption: Optional[str]


class FRQExtraction(TypedDict):
    page_type: Literal["frq", "skip"]
    skip_reason: Optional[str]       # title_page | cover_sheet | instructions | section_separator | other
    question_number: Optional[int]
    question: Optional[str]
    solution: Optional[str]
    grading_scheme: Optional[str]
    figures: Optional[list]          # list of FigureInfo dicts
    tables: Optional[list]           # list of TableInfo dicts
    unit: Optional[str]              # e.g. "Unit 1: Limits and Continuity"
    section: Optional[str]           # e.g. "Part A" or "Part B"
    calculator: Optional[str]        # "Calculator active" or "Calculator prohibited"
    flagged: bool
    flag_reason: Optional[str]


class PageResult(TypedDict):
    fname: str
    page: int           # 0-based page index in the source PDF
    extraction: Optional[FRQExtraction]
    error: Optional[str]
    pdf_path: str


class ExamQuestion(TypedDict):
    question_number: Optional[int]
    question: str
    figures: Optional[list]  # list of FigureInfo dicts (pre-materialisation)
    tables: Optional[list]   # list of TableInfo dicts
    unit: Optional[str]      # e.g. "Unit 1: Limits and Continuity"
    section: Optional[str]   # e.g. "Part A" or "Part B"
    calculator: Optional[str]  # "Calculator active" or "Calculator prohibited"


class ExamPageResult(TypedDict):
    fname: str
    page: int           # 0-based page index in the source PDF
    questions: list     # list of ExamQuestion; empty for skipped pages
    page_type: str      # "exam" | "skip"
    error: Optional[str]
    pdf_path: str
