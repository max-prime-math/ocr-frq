"""
models.py — TypedDict definitions for FRQ extraction results.
"""

from typing import Literal, Optional, TypedDict


class FRQExtraction(TypedDict):
    page_type: Literal["frq", "skip"]
    skip_reason: Optional[str]       # title_page | cover_sheet | instructions | section_separator | other
    question_number: Optional[int]
    question: Optional[str]
    solution: Optional[str]
    grading_scheme: Optional[str]
    flagged: bool
    flag_reason: Optional[str]


class PageResult(TypedDict):
    fname: str
    page: int           # 0-based page index in the source PDF
    extraction: Optional[FRQExtraction]
    error: Optional[str]
    pdf_path: str
