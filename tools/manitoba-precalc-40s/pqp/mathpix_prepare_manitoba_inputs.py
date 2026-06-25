#!/usr/bin/env python3
"""Build lower-cost Manitoba PDF inputs for Mathpix."""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

import fitz

from manitoba_mathpix_common import (
    FILTERED_INPUT_DIR,
    MB_DIR,
    filtered_input_path,
    pdf_page_count,
    source_documents,
)


CATALOG_JSON = MB_DIR / "catalog" / "question_catalog.json"
REPORT_PATH = FILTERED_INPUT_DIR / "page_filter_report.json"
QUESTION_RE = re.compile(r"\bQuestion\s+(?P<num>\d{1,2})\b", re.I)


def load_catalog() -> list[dict[str, Any]]:
    data = json.loads(CATALOG_JSON.read_text(encoding="utf-8"))
    return data["questions"] if isinstance(data, dict) and "questions" in data else data


def student_doc_id(row: dict[str, Any]) -> str:
    return f"pc_{int(row['year'])}_{row['term']}_sb{int(row['booklet'])}"


def mg_doc_id(row: dict[str, Any]) -> str:
    return f"pc_{int(row['year'])}_{row['term']}_mg"


def compact_text(text: str) -> str:
    return " ".join(text.replace("\x08", " ").split())


def question_start_pages(path: Path) -> list[int]:
    starts: list[int] = []
    doc = fitz.open(path)
    try:
        for page_index, page in enumerate(doc, start=1):
            text = compact_text(page.get_text("text"))
            if QUESTION_RE.search(text):
                starts.append(page_index)
    finally:
        doc.close()
    return starts


def student_keep_pages(path: Path) -> list[int]:
    """Keep question ranges, not just header pages, to preserve graph/work pages."""
    starts = question_start_pages(path)
    if not starts:
        return []
    doc = fitz.open(path)
    try:
        page_count = len(doc)
    finally:
        doc.close()

    keep: set[int] = set()
    for index, start in enumerate(starts):
        end = starts[index + 1] - 1 if index + 1 < len(starts) else page_count
        keep.update(range(start, end + 1))
    return sorted(keep)


def write_filtered_pdf(source: Path, output: Path, pages_1_based: list[int], overwrite: bool) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists() and not overwrite:
        return
    source_doc = fitz.open(source)
    try:
        page_count = len(source_doc)
        out_doc = fitz.open()
        for page_number in pages_1_based:
            if page_number < 1 or page_number > page_count:
                raise ValueError(
                    f"Cannot copy page {page_number} from {source}; source has {page_count} pages."
                )
            out_doc.insert_pdf(source_doc, from_page=page_number - 1, to_page=page_number - 1)
        out_doc.save(output)
        out_doc.close()
    finally:
        source_doc.close()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--overwrite", action="store_true", help="Rewrite existing filtered PDFs.")
    args = parser.parse_args()

    rows = load_catalog()
    mg_pages: dict[str, set[int]] = defaultdict(set)
    for row in rows:
        mg_pages[mg_doc_id(row)].update(int(page) for page in row.get("mgSourcePages", []))

    report_rows = []
    for doc in source_documents():
        if doc.kind == "student-booklet":
            keep_pages = student_keep_pages(doc.path)
            strategy = "question-ranges"
        else:
            keep_pages = sorted(mg_pages.get(doc.id, set()))
            strategy = "catalog-solution-pages"
        if not keep_pages:
            raise RuntimeError(f"No pages selected for {doc.id}")

        output = filtered_input_path(doc)
        write_filtered_pdf(doc.path, output, keep_pages, args.overwrite)
        report_rows.append(
            {
                "id": doc.id,
                "kind": doc.kind,
                "strategy": strategy,
                "sourcePdf": doc.relative_path,
                "filteredPdf": output.relative_to(MB_DIR.parent).as_posix(),
                "sourcePages": pdf_page_count(doc.path),
                "filteredPages": len(keep_pages),
                "keptOriginalPages": keep_pages,
            }
        )

    full_pages = sum(row["sourcePages"] for row in report_rows)
    filtered_pages = sum(row["filteredPages"] for row in report_rows)
    report = {
        "documents": len(report_rows),
        "fullPages": full_pages,
        "filteredPages": filtered_pages,
        "estimatedFullCostUsd": round(full_pages * 0.005, 2),
        "estimatedFilteredCostUsd": round(filtered_pages * 0.005, 2),
        "estimatedSavingsUsd": round((full_pages - filtered_pages) * 0.005, 2),
        "rows": report_rows,
    }
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k != "rows"}, indent=2))


if __name__ == "__main__":
    main()
