#!/usr/bin/env python3
"""Split the combined Manitoba marking-guide PDF into one PDF per sitting."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import fitz


ROOT = Path(__file__).resolve().parents[3]
MB_DIR = ROOT / "data" / "manitoba-precalc-40s" / "workspace"
COMBINED_MG_PDF = MB_DIR / "source-pdfs" / "combined" / "exams-mg-2013-2026.pdf"
OUT_DIR = MB_DIR / "source-pdfs" / "marking-guides"

TERM_FROM_MONTH = {"january": "jan", "june": "jun"}
SESSION_RE = re.compile(
    r"Grade\s+12\s+Pre-Calculus\s+Mathematics\s+Ach(?:ie|ei)vement\s+Test\s+"
    r"Marking\s+Guide\s+(?P<month>January|June)\s+(?P<year>20\d{2})",
    re.I,
)


def compact_text(text: str) -> str:
    return " ".join(text.replace("\x08", " ").split())


def detect_sessions(doc: fitz.Document) -> list[tuple[int, str, int, int]]:
    starts: list[tuple[int, str, int]] = []
    seen: set[tuple[int, str]] = set()
    for index, page in enumerate(doc, start=1):
        match = SESSION_RE.search(compact_text(page.get_text("text")))
        if not match:
            continue
        year = int(match.group("year"))
        term = TERM_FROM_MONTH[match.group("month").lower()]
        key = (year, term)
        if key in seen:
            continue
        seen.add(key)
        starts.append((year, term, index))

    sessions: list[tuple[int, str, int, int]] = []
    for index, (year, term, start) in enumerate(starts):
        end = starts[index + 1][2] - 1 if index + 1 < len(starts) else len(doc)
        sessions.append((year, term, start, end))
    return sessions


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing split marking guides.")
    args = parser.parse_args()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    source = fitz.open(COMBINED_MG_PDF)
    try:
        outputs = []
        for year, term, start, end in detect_sessions(source):
            out_path = OUT_DIR / f"pc_{year % 100:02d}_{term}_mg.pdf"
            if out_path.exists() and not args.overwrite:
                action = "kept"
            else:
                split = fitz.open()
                split.insert_pdf(source, from_page=start - 1, to_page=end - 1)
                split.save(out_path)
                split.close()
                action = "wrote"
            outputs.append(
                {
                    "year": year,
                    "term": term,
                    "sourcePages": [start, end],
                    "output": str(out_path),
                    "action": action,
                }
            )
    finally:
        source.close()

    print(json.dumps({"source": str(COMBINED_MG_PDF), "outputs": outputs}, indent=2))


if __name__ == "__main__":
    main()
