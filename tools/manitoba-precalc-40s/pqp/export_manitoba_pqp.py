#!/usr/bin/env python3
"""
Export Manitoba Pre-Calculus 40S audit catalog rows to PQP packages.

This exporter uses the PDFs as the source of truth for session/page boundaries
and emits cropped page images as external assets. The extracted PDF text is kept
as searchable plain text, while the image crop preserves diagrams, blank graph
paper, and layout-sensitive MCQ options.
"""

from __future__ import annotations

import json
import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import fitz


ROOT = Path(__file__).resolve().parents[3]
MB_DIR = ROOT / "data" / "manitoba-precalc-40s" / "workspace"
CATALOG_JSON = MB_DIR / "catalog" / "question_catalog.json"
OUT_DIR = MB_DIR / "derived" / "pqp-pdf-crop-v0" / "pqp"

QUESTION_RE_TEMPLATE = r"\bQuestion\s+{question}\b"
NEXT_QUESTION_RE = re.compile(r"\bQuestion\s+\d{1,2}\b", re.I)
CHOICE_RE = re.compile(r"(?:^|\s)([a-d])\)\s*(.*?)(?=(?:\s+[a-d]\)\s*)|$)", re.I | re.S)
OUTCOME_RE = re.compile(r"[A-Z]\d+")
FOOTER_RE = re.compile(
    r"\s*\d*\s*Pre-Calculus Mathematics:\s*"
    r"(?:Booklet\s*[12]|Marking Guide)\s*\([^)]*\)\s*\d*\s*$",
    re.I,
)

UNIT_NAMES = {
    "T": "Trigonometry",
    "P": "Permutations, Combinations, and Binomial Theorem",
    "R": "Relations and Functions",
}


class PdfCache:
    def __init__(self) -> None:
        self._docs: dict[Path, fitz.Document] = {}

    def doc(self, path: Path) -> fitz.Document:
        resolved = path.resolve()
        if resolved not in self._docs:
            self._docs[resolved] = fitz.open(resolved)
        return self._docs[resolved]

    def page(self, path: Path, page_number: int) -> fitz.Page:
        return self.doc(path)[page_number - 1]

    def close(self) -> None:
        for doc in self._docs.values():
            doc.close()
        self._docs.clear()


def compact_text(text: str) -> str:
    return " ".join(text.replace("\x08", " ").split())


def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def term_label(term: str) -> str:
    return "January" if term == "jan" else "June"


def read_page_text(cache: PdfCache, pdf_path: Path, page_number: int) -> str:
    return compact_text(cache.page(pdf_path, page_number).get_text("text"))


def question_block_from_text(text: str, question: int) -> str:
    pattern = re.compile(QUESTION_RE_TEMPLATE.format(question=question), re.I)
    match = pattern.search(text)
    if not match:
        return compact_text(text)
    next_match = NEXT_QUESTION_RE.search(text, match.end())
    end = next_match.start() if next_match else len(text)
    return FOOTER_RE.sub("", compact_text(text[match.start() : end])).strip()


def question_text(cache: PdfCache, row: dict[str, Any]) -> str:
    parts = []
    pdf_path = Path(row["sourcePdf"])
    for page in row["sourcePages"]:
        parts.append(question_block_from_text(read_page_text(cache, pdf_path, int(page)), int(row["question"])))
    return "\n\n".join(part for part in parts if part).strip()


def solution_text(cache: PdfCache, row: dict[str, Any]) -> str:
    if not row.get("mgSourcePdf") or not row.get("mgSourcePages"):
        return ""
    parts = []
    pdf_path = Path(row["mgSourcePdf"])
    for page in row["mgSourcePages"]:
        parts.append(question_block_from_text(read_page_text(cache, pdf_path, int(page)), int(row["question"])))
    return "\n\n".join(part for part in parts if part).strip()


def crop_rect_for_question(page: fitz.Page, question: int) -> fitz.Rect:
    header_re = re.compile(QUESTION_RE_TEMPLATE.format(question=question), re.I)
    words = page.get_text("words")
    text_dict = page.get_text("dict")
    page_rect = page.rect

    top = page_rect.y0
    bottom = page_rect.y1
    question_tops: list[tuple[int, float]] = []

    # Word extraction is more reliable for question headings than search_for on
    # OCR-normalized PDFs.
    for block in text_dict.get("blocks", []):
        for line in block.get("lines", []):
            line_text = "".join(span.get("text", "") for span in line.get("spans", []))
            qmatch = NEXT_QUESTION_RE.search(line_text)
            if not qmatch:
                continue
            num_match = re.search(r"\d{1,2}", qmatch.group(0))
            if not num_match:
                continue
            bbox = fitz.Rect(line["bbox"])
            question_tops.append((int(num_match.group(0)), bbox.y0))

    matches = [y for num, y in question_tops if num == question]
    if matches:
        top = max(page_rect.y0, min(matches) - 14)
        later = [y for _, y in question_tops if y > min(matches) + 8]
        if later:
            bottom = min(later) - 8
    else:
        needle = f"Question {question}"
        rects = page.search_for(needle)
        if rects:
            top = max(page_rect.y0, min(rect.y0 for rect in rects) - 14)
            later = [rect.y0 for rect in page.search_for("Question") if rect.y0 > top + 20]
            if later:
                bottom = min(later) - 8

    if bottom <= top + 80:
        bottom = page_rect.y1

    # Add horizontal margin but remove most page chrome.
    return fitz.Rect(page_rect.x0 + 24, top, page_rect.x1 - 24, min(page_rect.y1, bottom + 10))


def render_crop(
    cache: PdfCache,
    pdf_path: Path,
    page_number: int,
    question: int,
    output_path: Path,
    zoom: float = 2.0,
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    page = cache.page(pdf_path, page_number)
    clip = crop_rect_for_question(page, question)
    pixmap = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), clip=clip, alpha=False)
    pixmap.save(output_path)


def parse_choices(stem: str) -> list[dict[str, Any]]:
    matches = list(CHOICE_RE.finditer(stem))
    if len(matches) < 4:
        return []

    choices = []
    for match in matches[:4]:
        label = match.group(1).upper()
        text = compact_text(match.group(2))
        if not text:
            text = label
        choices.append(
            {
                "id": label,
                "body": {"format": "plain", "text": text},
            }
        )
    return choices


def outcome_codes(row: dict[str, Any]) -> list[str]:
    return sorted(set(OUTCOME_RE.findall(row.get("learningOutcome", ""))))


def first_outcome_prefix(row: dict[str, Any]) -> str:
    codes = outcome_codes(row)
    return codes[0][0] if codes else "unknown"


def classification(row: dict[str, Any]) -> dict[str, Any]:
    prefix = first_outcome_prefix(row)
    codes = outcome_codes(row)
    tags = [
        "Manitoba",
        "Pre-Calculus 40S",
        str(row["year"]),
        term_label(row["term"]),
        row["session"],
        f"Booklet {row['booklet']}",
        row["calculatorPolicy"],
        row["kind"],
    ]
    tags.extend(codes)
    if row.get("learningOutcome") and row["learningOutcome"] not in codes:
        tags.append(row["learningOutcome"])

    return {
        "questionType": row["kind"],
        "tags": tags,
        "classId": "manitoba-pre-calculus-40s",
        "className": "Manitoba Pre-Calculus 40S",
        "unitId": f"outcome-{prefix.lower()}",
        "unitName": UNIT_NAMES.get(prefix, "Unclassified Outcome"),
        "sectionId": codes[0].lower() if codes else "",
        "sectionName": codes[0] if codes else "",
        "extensions": {
            "manitobaPrecalc": {
                "learningOutcome": row.get("learningOutcome", ""),
                "learningOutcomeSource": row.get("learningOutcomeSource", ""),
                "booklet": row.get("booklet"),
                "calculatorPolicy": row.get("calculatorPolicy", ""),
            }
        },
    }


def answer_object(row: dict[str, Any]) -> dict[str, Any] | None:
    answer = str(row.get("answer", "")).strip()
    if not answer:
        return None
    if row["kind"] == "mcq":
        return {"type": "choice", "value": answer.upper()}
    if row["kind"] == "matching":
        values = [item.strip().upper() for item in answer.split(",") if item.strip()]
        return {
            "type": "mapping",
            "value": [
                {"itemId": str(index + 1), "choiceId": value}
                for index, value in enumerate(values)
            ],
            "extensions": {"rawAnswer": answer},
        }
    return {"type": "text", "value": answer}


def classes_for_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    sections_by_prefix: dict[str, set[str]] = defaultdict(set)
    for row in rows:
        for code in outcome_codes(row):
            sections_by_prefix[code[0]].add(code)

    units = []
    for prefix in sorted(sections_by_prefix):
        units.append(
            {
                "id": f"outcome-{prefix.lower()}",
                "name": UNIT_NAMES.get(prefix, "Unclassified Outcome"),
                "sections": [
                    {"id": code.lower(), "name": code}
                    for code in sorted(sections_by_prefix[prefix], key=lambda c: (c[0], int(c[1:])))
                ],
            }
        )

    return [{"id": "manitoba-pre-calculus-40s", "name": "Manitoba Pre-Calculus 40S", "units": units}]


def make_question(
    cache: PdfCache,
    row: dict[str, Any],
    package_dir: Path,
    asset_dir: Path,
    package_assets: list[dict[str, Any]],
    diagnostics: list[dict[str, Any]],
) -> dict[str, Any]:
    year = int(row["year"])
    term = row["term"]
    question = int(row["question"])
    qid = f"mb-pc40s-{year}-{term}-q{question:02d}"
    stem = question_text(cache, row)
    solution = solution_text(cache, row)

    question_asset_ids = []
    solution_asset_ids = []

    for index, page_number in enumerate(row["sourcePages"], start=1):
        filename = f"{qid}-question-p{index}.png"
        path = asset_dir / filename
        render_crop(cache, Path(row["sourcePdf"]), int(page_number), question, path)
        asset_id = f"{qid}-question-p{index}"
        question_asset_ids.append(asset_id)
        package_assets.append(
            {
                "id": asset_id,
                "kind": "image",
                "filename": filename,
                "mimeType": "image/png",
                "storage": {"mode": "external", "path": str(path.relative_to(package_dir))},
                "source": {"originalPath": f"{Path(row['sourcePdf']).name}#page={page_number}"},
                "extensions": {"role": "question-crop"},
            }
        )

    for index, page_number in enumerate(row.get("mgSourcePages", []), start=1):
        filename = f"{qid}-solution-p{index}.png"
        path = asset_dir / filename
        render_crop(cache, Path(row["mgSourcePdf"]), int(page_number), question, path)
        asset_id = f"{qid}-solution-p{index}"
        solution_asset_ids.append(asset_id)
        package_assets.append(
            {
                "id": asset_id,
                "kind": "image",
                "filename": filename,
                "mimeType": "image/png",
                "storage": {"mode": "external", "path": str(path.relative_to(package_dir))},
                "source": {"originalPath": f"{Path(row['mgSourcePdf']).name}#page={page_number}"},
                "extensions": {"role": "solution-crop"},
            }
        )

    content: dict[str, Any] = {
        "stem": {"format": "plain", "text": stem},
        "solution": {"format": "plain", "text": solution},
    }
    if row["kind"] == "mcq":
        choices = parse_choices(stem)
        if choices:
            content["choices"] = choices
        else:
            diagnostics.append(
                {
                    "level": "warning",
                    "code": "MCQ_CHOICES_NOT_PARSED",
                    "message": "MCQ choices are preserved in the question crop, but text choices were not parsed cleanly.",
                    "questionId": qid,
                }
            )

    question_record: dict[str, Any] = {
        "id": qid,
        "kind": row["kind"],
        "content": content,
        "scoring": {"points": float(row.get("points") or 0)},
        "classification": classification(row),
        "assets": question_asset_ids,
        "provenance": {
            "sourceApp": "ocr-frq",
            "sourceLabel": f"Manitoba Pre-Calculus 40S {row['session']}",
            "sourceQuestionNumber": str(question),
            "confidence": "medium",
            "originFiles": sorted(
                {
                    Path(row["sourcePdf"]).name,
                    Path(row["mgSourcePdf"]).name if row.get("mgSourcePdf") else "",
                }
                - {""}
            ),
            "extensions": {
                "studentPages": row["sourcePages"],
                "markingGuidePages": row.get("mgSourcePages", []),
                "marksText": row.get("marksText", ""),
            },
        },
        "extensions": {
            "manitobaPrecalc": {
                "sourceAssets": {
                    "questionCrops": question_asset_ids,
                    "solutionCrops": solution_asset_ids,
                },
                "sourcePdfTextPreview": row.get("preview", ""),
                "catalogDiagnostics": row.get("diagnostics", []),
            }
        },
    }

    answer = answer_object(row)
    if answer:
        question_record["answer"] = answer
    return question_record


def package_for_session(rows: list[dict[str, Any]]) -> dict[str, Any]:
    first = rows[0]
    return {
        "format": "portable-question-package",
        "version": "1.0",
        "producer": {
            "app": "ocr-frq",
            "appVersion": "manitoba-pqp-export-1",
            "exportedAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        },
        "source": {
            "kind": "pdf",
            "label": f"Manitoba Pre-Calculus 40S {first['session']}",
            "collection": "Manitoba Pre-Calculus 40S Provincial Exams",
            "publisher": "Manitoba Education and Early Childhood Learning",
            "year": int(first["year"]),
            "originFiles": sorted(
                {
                    Path(row["sourcePdf"]).name
                    for row in rows
                }
                | {
                    Path(row["mgSourcePdf"]).name
                    for row in rows
                    if row.get("mgSourcePdf")
                }
            ),
            "extensions": {"term": first["term"], "session": first["session"]},
        },
        "classes": classes_for_rows(rows),
        "questions": [],
        "assets": [],
        "diagnostics": [],
        "extensions": {
            "manitobaPrecalc": {
                "catalog": str(CATALOG_JSON),
                "notes": [
                    "Question and solution text were extracted from PDFs.",
                    "Question crops are attached as question assets.",
                    "Solution crops are preserved in question extensions but not attached as visible question assets.",
                ],
            }
        },
    }


def main() -> None:
    rows = json.loads(CATALOG_JSON.read_text(encoding="utf-8"))
    rows_by_session: dict[tuple[int, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        rows_by_session[(int(row["year"]), row["term"])].append(row)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    manifest = {
        "generatedAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "packageCount": 0,
        "questionCount": 0,
        "assetCount": 0,
        "packages": [],
    }

    cache = PdfCache()
    try:
        for (year, term), session_rows in sorted(rows_by_session.items()):
            session_rows.sort(key=lambda row: int(row["question"]))
            package_name = f"manitoba-pc40s-{year}-{term}.pqp.json"
            package_dir = OUT_DIR / f"manitoba-pc40s-{year}-{term}"
            asset_dir = package_dir / "assets"
            package_dir.mkdir(parents=True, exist_ok=True)

            package = package_for_session(session_rows)
            for row in session_rows:
                package["questions"].append(
                    make_question(
                        cache,
                        row,
                        package_dir,
                        asset_dir,
                        package["assets"],
                        package["diagnostics"],
                    )
                )

            output_path = package_dir / package_name
            output_path.write_text(json.dumps(package, indent=2), encoding="utf-8")
            manifest["packageCount"] += 1
            manifest["questionCount"] += len(package["questions"])
            manifest["assetCount"] += len(package["assets"])
            manifest["packages"].append(
                {
                    "session": session_rows[0]["session"],
                    "year": year,
                    "term": term,
                    "path": str(output_path),
                    "questions": len(package["questions"]),
                    "assets": len(package["assets"]),
                    "diagnostics": len(package["diagnostics"]),
                }
            )
    finally:
        cache.close()

    (OUT_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
