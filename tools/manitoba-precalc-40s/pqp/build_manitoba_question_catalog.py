#!/usr/bin/env python3
"""
Build audit tables for Manitoba Pre-Calculus 40S exams.

The tables produced here are intentionally intermediate artifacts. They tie
student-booklet question pages, answer keys, and marking-guide metadata together
before a PQP exporter tries to normalize Mathpix LaTeX.
"""

from __future__ import annotations

import csv
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

import fitz


ROOT = Path(__file__).resolve().parents[3]
MB_DIR = ROOT / "data" / "manitoba-precalc-40s" / "workspace"
OUT_DIR = MB_DIR / "catalog"
STUDENT_BOOKLET_DIR = MB_DIR / "source-pdfs" / "student-booklets"
COMBINED_PDF_DIR = MB_DIR / "source-pdfs" / "combined"
MARKING_GUIDE_DIR = MB_DIR / "source-pdfs" / "marking-guides"

ANSWER_KEY_JSON = OUT_DIR / "answer_keys_2013_2026.json"
COMBINED_MG_PDF = COMBINED_PDF_DIR / "exams-mg-2013-2026.pdf"
JUNE_2026_MG_PDF = MARKING_GUIDE_DIR / "pc_26_jun_mg.pdf"

MONTH_NAME = {"jan": "January", "jun": "June"}
TERM_FROM_MONTH = {"january": "jan", "june": "jun"}

SB_FILE_RE = re.compile(r"pc_(?P<yy>\d{2})_(?P<term>jan|jun)_sb(?P<booklet>[12])\.pdf$", re.I)
MG_FILE_RE = re.compile(r"pc_(?P<yy>\d{2})_(?P<term>jan|jun)_mg\.pdf$", re.I)

QUESTION_RE = re.compile(r"\bQuestion\s+(?P<num>\d{1,2})\b", re.I)
MARK_RE = re.compile(r"(?P<points>\d+(?:\.\d+)?)\s+marks?\b", re.I)
PART_MARK_RE = re.compile(r"\b[a-d]\)\s*(?P<points>\d+(?:\.\d+)?)\s+marks?\b", re.I)
OUTCOME_RE = re.compile(r"^[A-Z]\d+(?:\s*,\s*[A-Z]\d+)*$")
HEADING_RE = re.compile(
    r"\bQuestion\s+(?P<num>\d{1,2})\s+(?P<outcome>[A-Z]\d+(?:\s*,\s*[A-Z]\d+)*)\b"
)
PART_HEADING_RE = re.compile(
    r"\bQuestion\s+(?P<num>\d{1,2})\s+"
    r"(?P<parts>(?:[a-d]\)\s*[A-Z]\d+(?:\s*,\s*[A-Z]\d+)*\s*)+)",
    re.I,
)
PART_OUTCOME_RE = re.compile(r"(?P<part>[a-d])\)\s*(?P<outcome>[A-Z]\d+(?:\s*,\s*[A-Z]\d+)*)", re.I)
SESSION_RE = re.compile(
    r"Grade\s+12\s+Pre-Calculus\s+Mathematics\s+Ach(?:ie|ei)vement\s+Test\s+"
    r"Marking\s+Guide\s+(?P<month>January|June)\s+(?P<year>20\d{2})",
    re.I,
)


@dataclass
class StudentQuestionRow:
    year: int
    term: str
    session: str
    booklet: int
    question: int
    sourcePdf: str
    sourcePages: list[int]
    pageCount: int
    marksText: str
    points: float
    calculatorPolicy: str
    preview: str


@dataclass
class MarkingGuideRow:
    year: int
    term: str
    session: str
    question: int
    learningOutcome: str
    sourcePdf: str
    sourcePages: list[int]
    pageCount: int
    marksText: str
    points: float
    preview: str


@dataclass
class CatalogRow:
    year: int
    term: str
    session: str
    question: int
    kind: str
    booklet: int
    sourcePdf: str
    sourcePages: list[int]
    pageCount: int
    points: float
    marksText: str
    calculatorPolicy: str
    answer: str
    learningOutcome: str
    learningOutcomeSource: str
    mgSourcePdf: str
    mgSourcePages: list[int]
    diagnostics: list[str]
    preview: str


def compact_text(text: str) -> str:
    return " ".join(text.replace("\x08", " ").split())


def session_label(year: int, term: str) -> str:
    return f"{MONTH_NAME[term]} {year}"


def parse_points(block: str) -> tuple[str, float]:
    part_points = [float(m.group("points")) for m in PART_MARK_RE.finditer(block)]
    if part_points:
        text = "; ".join(m.group(0) for m in PART_MARK_RE.finditer(block))
        return text, sum(part_points)

    mark = MARK_RE.search(block)
    if not mark:
        return "", 0.0
    return mark.group(0), float(mark.group("points"))


def read_pdf_pages(path: Path) -> list[str]:
    doc = fitz.open(path)
    try:
        return [compact_text(page.get_text("text")) for page in doc]
    finally:
        doc.close()


def block_until_next_question(text: str, match: re.Match[str]) -> str:
    next_match = QUESTION_RE.search(text, match.end())
    end = next_match.start() if next_match else len(text)
    return text[match.start() : end]


def calculator_cutoff(pages: list[str]) -> int | None:
    """Infer the last calculator-active question in Booklet 1."""
    note_re = re.compile(r"calculator\s+is\s+not\s+required|calculator.*remaining", re.I)
    last_seen_question = None
    for text in pages:
        nums = [int(m.group("num")) for m in QUESTION_RE.finditer(text)]
        if nums:
            last_seen_question = max(nums)
        if note_re.search(text):
            return last_seen_question
    return None


def build_answer_lookup() -> dict[tuple[int, str, int], dict[str, str]]:
    data = json.loads(ANSWER_KEY_JSON.read_text(encoding="utf-8"))
    lookup: dict[tuple[int, str, int], dict[str, str]] = {}
    for session in data["sessions"]:
        year = int(session["year"])
        term = str(session["term"])
        for row in session["answers"]:
            lookup[(year, term, int(row["question"]))] = {
                "answer": str(row["answer"]),
                "learningOutcome": str(row["learningOutcome"]),
            }
    return lookup


def build_student_rows() -> list[StudentQuestionRow]:
    rows: list[StudentQuestionRow] = []
    for pdf_path in sorted(STUDENT_BOOKLET_DIR.glob("pc_*_sb*.pdf")):
        match = SB_FILE_RE.match(pdf_path.name)
        if not match:
            continue
        year = 2000 + int(match.group("yy"))
        term = match.group("term").lower()
        booklet = int(match.group("booklet"))
        pages = read_pdf_pages(pdf_path)
        cutoff = calculator_cutoff(pages) if booklet == 1 else None

        starts: list[tuple[int, int, re.Match[str]]] = []
        for page_index, text in enumerate(pages, start=1):
            for qmatch in QUESTION_RE.finditer(text):
                starts.append((int(qmatch.group("num")), page_index, qmatch))

        # One row per question. Use every page where the question header appears.
        seen_questions = sorted({question for question, _, _ in starts})
        for question in seen_questions:
            source_pages = sorted({page for q, page, _ in starts if q == question})
            first_page = source_pages[0]
            page_text = pages[first_page - 1]
            qmatch = next(m for m in QUESTION_RE.finditer(page_text) if int(m.group("num")) == question)
            block = block_until_next_question(page_text, qmatch)
            marks_text, points = parse_points(block)
            if booklet == 2:
                calculator_policy = "no-calculator"
            elif cutoff is not None and question <= cutoff:
                calculator_policy = "calculator-active"
            elif cutoff is not None:
                calculator_policy = "no-calculator"
            else:
                calculator_policy = "calculator-allowed"

            rows.append(
                StudentQuestionRow(
                    year=year,
                    term=term,
                    session=session_label(year, term),
                    booklet=booklet,
                    question=question,
                    sourcePdf=str(pdf_path),
                    sourcePages=source_pages,
                    pageCount=len(source_pages),
                    marksText=marks_text,
                    points=points,
                    calculatorPolicy=calculator_policy,
                    preview=block[:300],
                )
            )
    return rows


def detect_combined_mg_sessions() -> list[tuple[int, str, int, int]]:
    pages = read_pdf_pages(COMBINED_MG_PDF)
    starts: list[tuple[int, str, int]] = []
    for index, text in enumerate(pages, start=1):
        match = SESSION_RE.search(text)
        if not match:
            continue
        year = int(match.group("year"))
        term = TERM_FROM_MONTH[match.group("month").lower()]
        starts.append((year, term, index))

    # Keep first cover page per session.
    deduped: list[tuple[int, str, int]] = []
    seen: set[tuple[int, str]] = set()
    for year, term, page in starts:
        key = (year, term)
        if key in seen:
            continue
        seen.add(key)
        deduped.append((year, term, page))

    sessions: list[tuple[int, str, int, int]] = []
    for index, (year, term, start) in enumerate(deduped):
        end = (deduped[index + 1][2] - 1) if index + 1 < len(deduped) else len(pages)
        sessions.append((year, term, start, end))
    return sessions


def extract_mg_rows_from_pages(
    pdf_path: Path, year: int, term: str, page_offset: int, pages: list[str]
) -> list[MarkingGuideRow]:
    rows_by_question: dict[int, MarkingGuideRow] = {}
    for local_index, text in enumerate(pages, start=1):
        if "Answer Key" in text and "Question Answer Learning" in text:
            continue
        heading_matches: list[tuple[re.Match[str], str]] = []
        heading_matches.extend((match, "standard") for match in HEADING_RE.finditer(text))
        heading_matches.extend((match, "parts") for match in PART_HEADING_RE.finditer(text))

        for match, match_kind in sorted(heading_matches, key=lambda item: item[0].start()):
            question = int(match.group("num"))
            if match_kind == "parts":
                part_outcomes = [
                    f"{part_match.group('part').lower()}) "
                    f"{re.sub(r'\\s*,\\s*', ', ', part_match.group('outcome'))}"
                    for part_match in PART_OUTCOME_RE.finditer(match.group("parts"))
                ]
                outcome = "; ".join(part_outcomes)
            else:
                outcome = re.sub(r"\s*,\s*", ", ", match.group("outcome"))
                if not OUTCOME_RE.match(outcome):
                    continue
            block = block_until_next_question(text, match)
            marks_text, points = parse_points(block)
            source_page = page_offset + local_index - 1
            existing = rows_by_question.get(question)
            if existing:
                if source_page not in existing.sourcePages:
                    existing.sourcePages.append(source_page)
                    existing.pageCount = len(existing.sourcePages)
                if match_kind == "parts" and outcome:
                    existing.learningOutcome = outcome
                elif not existing.learningOutcome and outcome:
                    existing.learningOutcome = outcome
                continue
            rows_by_question[question] = MarkingGuideRow(
                year=year,
                term=term,
                session=session_label(year, term),
                question=question,
                learningOutcome=outcome,
                sourcePdf=str(pdf_path),
                sourcePages=[source_page],
                pageCount=1,
                marksText=marks_text,
                points=points,
                preview=block[:300],
            )
    return sorted(rows_by_question.values(), key=lambda row: row.question)


def build_marking_guide_rows() -> list[MarkingGuideRow]:
    rows: list[MarkingGuideRow] = []
    for pdf_path in sorted(MARKING_GUIDE_DIR.glob("pc_*_mg.pdf")):
        match = MG_FILE_RE.match(pdf_path.name)
        if not match:
            continue
        year = 2000 + int(match.group("yy"))
        term = match.group("term").lower()
        pages = read_pdf_pages(pdf_path)
        rows.extend(extract_mg_rows_from_pages(pdf_path, year, term, 1, pages))
    return rows


def classify_kind(answer: str) -> str:
    if not answer:
        return "frq"
    if "," in answer:
        return "matching"
    return "mcq"


def build_catalog(
    student_rows: Iterable[StudentQuestionRow],
    mg_rows: Iterable[MarkingGuideRow],
    answer_lookup: dict[tuple[int, str, int], dict[str, str]],
) -> list[CatalogRow]:
    mg_lookup = {(row.year, row.term, row.question): row for row in mg_rows}
    catalog: list[CatalogRow] = []
    for srow in sorted(student_rows, key=lambda row: (row.year, row.term, row.booklet, row.question)):
        key = (srow.year, srow.term, srow.question)
        answer_info = answer_lookup.get(key, {})
        mg_row = mg_lookup.get(key)
        answer = answer_info.get("answer", "")
        answer_outcome = answer_info.get("learningOutcome", "")
        mg_outcome = mg_row.learningOutcome if mg_row else ""
        diagnostics: list[str] = []
        if answer and not answer_outcome:
            diagnostics.append("answer key missing learning outcome")
        if not answer and not mg_outcome:
            diagnostics.append("missing marking-guide learning outcome")
        if not mg_row:
            diagnostics.append("missing marking-guide question heading")
        if not srow.points and (mg_row is None or not mg_row.points):
            diagnostics.append("missing point value")

        learning_outcome = answer_outcome or mg_outcome
        learning_source = "answer-key" if answer_outcome else ("marking-guide-heading" if mg_outcome else "")

        catalog.append(
            CatalogRow(
                year=srow.year,
                term=srow.term,
                session=srow.session,
                question=srow.question,
                kind=classify_kind(answer),
                booklet=srow.booklet,
                sourcePdf=srow.sourcePdf,
                sourcePages=srow.sourcePages,
                pageCount=srow.pageCount,
                points=srow.points or (mg_row.points if mg_row else 0.0),
                marksText=srow.marksText or (mg_row.marksText if mg_row else ""),
                calculatorPolicy=srow.calculatorPolicy,
                answer=answer,
                learningOutcome=learning_outcome,
                learningOutcomeSource=learning_source,
                mgSourcePdf=mg_row.sourcePdf if mg_row else "",
                mgSourcePages=mg_row.sourcePages if mg_row else [],
                diagnostics=diagnostics,
                preview=srow.preview,
            )
        )
    return catalog


def write_json(path: Path, rows: Iterable[object]) -> None:
    path.write_text(json.dumps([asdict(row) for row in rows], indent=2), encoding="utf-8")


def write_csv(path: Path, rows: list[object]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames = list(asdict(rows[0]).keys())
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(asdict(row))


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    answer_lookup = build_answer_lookup()
    student_rows = build_student_rows()
    mg_rows = build_marking_guide_rows()
    catalog = build_catalog(student_rows, mg_rows, answer_lookup)

    write_json(OUT_DIR / "student_question_index.json", student_rows)
    write_csv(OUT_DIR / "student_question_index.csv", student_rows)
    write_json(OUT_DIR / "marking_guide_question_index.json", mg_rows)
    write_csv(OUT_DIR / "marking_guide_question_index.csv", mg_rows)
    write_json(OUT_DIR / "question_catalog.json", catalog)
    write_csv(OUT_DIR / "question_catalog.csv", catalog)

    diagnostic_rows = [row for row in catalog if row.diagnostics]
    summary = {
        "studentQuestions": len(student_rows),
        "markingGuideQuestions": len(mg_rows),
        "catalogQuestions": len(catalog),
        "diagnosticQuestions": len(diagnostic_rows),
        "sessions": sorted({row.session for row in catalog}),
        "kindCounts": {
            kind: sum(1 for row in catalog if row.kind == kind)
            for kind in sorted({row.kind for row in catalog})
        },
        "diagnosticSamples": [asdict(row) for row in diagnostic_rows[:50]],
        "outputs": {
            "studentQuestionIndex": str(OUT_DIR / "student_question_index.json"),
            "markingGuideQuestionIndex": str(OUT_DIR / "marking_guide_question_index.json"),
            "questionCatalog": str(OUT_DIR / "question_catalog.json"),
        },
    }
    (OUT_DIR / "question_catalog_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
