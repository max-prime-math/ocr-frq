#!/usr/bin/env python3
"""Inventory every local AP Calculus release and isolate readable source crops.

Coordinates are unrotated PDF points and page numbers are one-based. Numbered
prompt markers must be at the left margin, visible, and ordered 1 through 6;
plain-text regex matches are unsafe in these PDFs (including off-page alt text).
Shared-page boundaries use the first substantial raster whitespace after the
previous question's final subpart, retaining diagrams above the next number.
No OCR service is used. Source hashes make every crop reproducible.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUTPUT = ROOT / "data/ap-calculus/draft/source-inventory.json"
RELEASE = re.compile(r"(AB|BC)-(\d{4})(-FORM-B)?")
MARKER = re.compile(r"([1-6])\.")
PART = re.compile(r"^\([a-f]\)(?:\s|$)")


def lines(page):
    return [(fitz.Rect(line["bbox"]), "".join(s["text"] for s in line["spans"]).strip())
            for block in page.get_text("dict")["blocks"]
            for line in block.get("lines", [])]


def markers(pdf):
    found = []
    for number, page in enumerate(pdf, 1):
        for word in page.get_text("words"):
            match = MARKER.fullmatch(word[4])
            if match and 20 <= word[0] <= 85 and 45 <= word[1] < page.rect.height - 80:
                found.append({"question": int(match[1]), "page": number, "rect": list(word[:4])})
    found.sort(key=lambda m: (m["page"], m["rect"][1]))
    if [m["question"] for m in found] != list(range(1, 7)):
        raise ValueError(f"Expected unique ordered left-margin questions 1..6: {found}")
    return found


def page_limits(page):
    top, bottom = 35.0, page.rect.height - 45
    for rect, text in lines(page):
        if rect.y0 < 90 and re.search(r"FREE.?RESPONSE QUESTIONS", text, re.I):
            top = max(top, rect.y1 + 5)
        if rect.y0 > page.rect.height * .65 and re.search(
            r"Copyright|©|Visit (?:the )?College|Visit apcentral|GO ON TO THE NEXT|"
            r"WRITE ALL WORK|END OF (?:PART|EXAM)|Write your responses|_{10,}", text, re.I
        ):
            bottom = min(bottom, rect.y0 - 6)
    return top, bottom


def raster_rows(page):
    pix = page.get_pixmap(matrix=fitz.Matrix(1, 1), colorspace=fitz.csGRAY, alpha=False)
    # Ink runs are robust to bogus text bboxes, embedded vector figures, and math.
    samples = pix.samples
    return [any(v < 220 for v in samples[y * pix.stride + 25:y * pix.stride + pix.width - 20])
            for y in range(pix.height)]


def shared_boundary(page, previous, current, rows):
    candidates = [(r, text) for r, text in lines(page)
                  if previous["rect"][1] < r.y0 < current["rect"][1] and r.x0 < 110 and PART.match(text)]
    if not candidates:
        raise ValueError(f"No subpart anchor before question {current['question']}")
    last_part = max(candidates, key=lambda item: item[0].y0)[0]
    start, stop = int(last_part.y1) + 2, int(current["rect"][1]) - 3
    blank_start = None
    for y in range(start, stop):
        if not rows[y]:
            if blank_start is None:
                blank_start = y
        elif blank_start is not None:
            if y - blank_start >= 15:
                return float(blank_start + min(8, (y - blank_start) / 2))
            blank_start = None
    if blank_start is not None and stop - blank_start >= 10:
        return float(blank_start + min(8, (stop - blank_start) / 2))
    raise ValueError(f"No safe visual separator before question {current['question']}")


def is_continuation(page):
    # All contemporary divider/stop pages contain no subparts. This retains the
    # sole current continuation, AB 2021 question 6 part (d), and supports others.
    return any(PART.match(text) and 25 < rect.y0 < page.rect.height - 90
               for rect, text in lines(page))


def trim_rect(page, top, bottom):
    # A raster bounding rectangle retains vector/image content as well as text.
    clip = fitz.Rect(20, max(0, top), page.rect.width - 15, min(page.rect.height, bottom))
    pix = page.get_pixmap(matrix=fitz.Matrix(1, 1), colorspace=fitz.csGRAY, alpha=False, clip=clip)
    samples = pix.samples
    occupied = []
    left, right = pix.width, 0
    for y in range(pix.height):
        row = samples[y * pix.stride:y * pix.stride + pix.width]
        ink = [x for x, value in enumerate(row) if value < 220]
        if ink:
            occupied.append(y)
            left, right = min(left, ink[0]), max(right, ink[-1])
    if not occupied:
        raise ValueError("Empty source crop")
    return [round(max(clip.x0, pix.x + left - 6), 2),
            round(max(clip.y0, pix.y + occupied[0] - 6), 2),
            round(min(clip.x1, pix.x + right + 7), 2),
            round(min(clip.y1, pix.y + occupied[-1] + 7), 2)]


def build_release(path):
    course, year, form_b = RELEASE.fullmatch(path.stem).groups()
    relative = path.relative_to(ROOT).as_posix()
    sha = hashlib.sha256(path.read_bytes()).hexdigest()
    guide = path.with_name("SG-" + path.name)
    questions = []
    with fitz.open(path) as pdf:
        starts = markers(pdf)
        boundaries = {}
        for previous, current in zip(starts, starts[1:]):
            if previous["page"] == current["page"]:
                page = pdf[current["page"] - 1]
                boundaries[current["question"]] = shared_boundary(page, previous, current, raster_rows(page))
        for i, marker in enumerate(starts):
            number, first = marker["question"], marker["page"]
            following = starts[i + 1] if i < 5 else None
            last_possible = following["page"] - 1 if following else len(pdf)
            pages = [first]
            pages.extend(p for p in range(first + 1, last_possible + 1) if is_continuation(pdf[p - 1]))
            crops = []
            for page_number in pages:
                page = pdf[page_number - 1]
                top, bottom = page_limits(page)
                if page_number == first and number in boundaries:
                    top = boundaries[number]
                if following and following["page"] == page_number:
                    bottom = boundaries[number + 1]
                rect = trim_rect(page, top, bottom)
                crops.append({"page": page_number, "rect": rect})
            ident = f"ap-calc-{course.lower()}-{year}{'-form-b' if form_b else ''}-frq-{number:02d}"
            if not fitz.Rect(crops[0]["rect"]).contains(fitz.Rect(marker["rect"])):
                raise ValueError(f"Question marker outside crop: {ident}")
            subparts = [text[1] for crop in crops for rect, text in lines(pdf[crop["page"] - 1])
                        if rect.x0 < 110 and PART.match(text)
                        and fitz.Rect(crop["rect"]).contains(rect.top_left)]
            if not subparts or subparts != list("abcdef"[:len(subparts)]):
                raise ValueError(f"Missing or unordered source subparts for {ident}: {subparts}")
            source = {"prompt": {"path": relative, "sha256": sha, "pages": pages}, "promptPages": pages}
            if guide.exists():
                source["scoringGuide"] = {"path": guide.relative_to(ROOT).as_posix(),
                                          "sha256": hashlib.sha256(guide.read_bytes()).hexdigest()}
            questions.append({"id": ident, "course": course, "year": int(year),
                              "form": "B" if form_b else "standard", "question": number,
                              "source": source, "crops": crops,
                              "markerRect": [round(v, 3) for v in marker["rect"]],
                              "boundaryMethod": "visible-left-margin-number-and-raster-whitespace",
                              "sourceSubparts": subparts,
                              "issues": [], "reviewStatus": "draft-source-crop",
                              "scoringGuideAvailable": guide.exists()})
    return questions


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    fitz.TOOLS.mupdf_display_errors(False)
    paths = sorted(path for course in ("ab", "bc")
                   for path in (ROOT / f"data/ap-calculus-{course}/source-pdfs").glob("*.pdf")
                   if RELEASE.fullmatch(path.stem))
    questions = [row for path in paths for row in build_release(path)]
    if len({q["id"] for q in questions}) != len(questions):
        raise ValueError("Duplicate question IDs")
    result = {"schemaVersion": 1, "scope": "all local AB/BC prompt releases, including prompt-only releases",
              "sourceReleaseCount": len(paths), "questionCount": len(questions),
              "pageNumbering": "one-based", "cropCoordinates": "PDF points, unrotated page",
              "sourceQuestionNumberingVerified": True,
              "validation": {"allMarkersInsideCrops": True, "allSubpartSequencesVerified": True,
                             "subpartCount": sum(len(q["sourceSubparts"]) for q in questions),
                             "multiPageQuestionIds": [q["id"] for q in questions if len(q["crops"]) > 1]},
              "questions": questions}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"output": str(args.output), "releases": len(paths), "questions": len(questions),
                      "crops": sum(len(q["crops"]) for q in questions)}))


if __name__ == "__main__":
    main()
