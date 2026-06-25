#!/usr/bin/env python3
"""Repair Manitoba PQP solutions from the manual combined Mathpix export.

This is intentionally conservative: it relies on exam order, question number,
fuzzy stem verification, and a real Solution/Solutions heading before replacing
an FRQ solution.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from export_manitoba_pqp_mathpix import clean_typst_artifacts, latex_to_typst, load_catalog
from manitoba_mathpix_common import MB_DIR


PQP_DIR = MB_DIR / "derived" / "pqp-mathpix" / "pqp"
REPORT_DIR = MB_DIR / "derived" / "pqp-mathpix"
MANUAL_MG_DIR = (
    MB_DIR
    / "mathpix"
    / "manual-combined"
    / "marking-guides"
    / "provincial-exams-mathpix-mg"
)
MANUAL_MG_TEX = MANUAL_MG_DIR / "f67fedaf-ea11-42ad-a16e-f30d2fcf2bd3.tex"
MANUAL_MG_IMAGES = MANUAL_MG_DIR / "images"

TERM_ORDER = {"jan": 0, "jun": 1}
LOCAL_SCAN_TOKENS = 4_000
TOKEN_RE = re.compile(r"[A-Za-z0-9]+")
SOLUTION_HEADING_RE = re.compile(r"\\section\*\{Solutions?\}", re.I)
INCLUDEGRAPHICS_RE = re.compile(
    r"\\includegraphics(?P<opts>\[[^\]]*\])?\{(?P<path>[^}]+)\}"
)
GENERIC_START_TOKENS = {
    "cos",
    "f",
    "g",
    "h",
    "k",
    "n",
    "p",
    "pi",
    "q",
    "sin",
    "tan",
    "theta",
    "x",
    "y",
}
COMMON_TOKENS = {
    "a",
    "an",
    "all",
    "and",
    "are",
    "as",
    "at",
    "be",
    "below",
    "by",
    "correct",
    "determine",
    "equation",
    "express",
    "find",
    "for",
    "from",
    "given",
    "has",
    "in",
    "is",
    "mark",
    "marks",
    "none",
    "of",
    "on",
    "or",
    "question",
    "shown",
    "the",
    "to",
    "use",
    "using",
    "value",
    "what",
    "where",
    "which",
    "will",
    "with",
    "align",
    "aligned",
    "alt",
    "array",
    "begin",
    "center",
    "columns",
    "end",
    "frac",
    "hline",
    "includegraphics",
    "left",
    "mathrm",
    "right",
    "section",
    "solution",
    "stroke",
    "table",
    "text",
    "textwidth",
    "upright",
    "width",
}


@dataclass(frozen=True)
class Token:
    text: str
    raw_start: int


@dataclass
class Match:
    question_id: str
    question_number: int
    kind: str
    raw_start: int
    score: float
    overlap: int
    anchor_size: int
    anchor: list[str]
    status: str = "matched"
    reason: str = ""


def package_name(year: int, term: str) -> str:
    return f"manitoba-pc40s-{year}-{term}"


def pqp_path(year: int, term: str) -> Path:
    package = package_name(year, term)
    return PQP_DIR / package / f"{package}.pqp.json"


def token_text(raw: str) -> str:
    return raw.lower()


def tokenize_with_offsets(text: str) -> list[Token]:
    return [Token(token_text(match.group(0)), match.start()) for match in TOKEN_RE.finditer(text)]


def tokenize(text: str) -> list[str]:
    return [token_text(match.group(0)) for match in TOKEN_RE.finditer(text)]


def strip_typst_images(text: str) -> str:
    return re.sub(r"#image\([^)]*\)", " ", text)


def anchor_tokens(stem: str, max_tokens: int = 18) -> list[str]:
    tokens = tokenize(strip_typst_images(stem))
    useful: list[str] = []
    variable_tokens = {"f", "g", "h", "k", "n", "p", "q", "x", "y"}
    for token in tokens:
        if len(token) == 1 and not token.isdigit() and token not in variable_tokens:
            continue
        if token in COMMON_TOKENS:
            continue
        useful.append(token)
        if len(useful) >= max_tokens:
            break
    if len(useful) >= 3:
        return useful
    return tokens[:max_tokens]


def best_match_after(
    manual_tokens: list[Token],
    anchor: list[str],
    raw_cursor: int,
    max_scan_tokens: int | None = 12_000,
    window_extra: int = 50,
) -> tuple[int, float, int] | None:
    if not anchor:
        return None
    leading = [
        token
        for token in anchor
        if not token.isdigit() and token not in GENERIC_START_TOKENS
    ]
    if not leading:
        leading = [token for token in anchor if not token.isdigit()]
    if not leading:
        leading = anchor
    leading_tokens = set(leading[: min(3, len(leading))])
    start_index = 0
    while start_index < len(manual_tokens) and manual_tokens[start_index].raw_start < raw_cursor:
        start_index += 1

    anchor_set = set(anchor)
    best: tuple[int, float, int] | None = None
    end_index = len(manual_tokens)
    if max_scan_tokens is not None:
        end_index = min(len(manual_tokens), start_index + max_scan_tokens)
    window_size = max(len(anchor) + window_extra, 80)
    for index in range(start_index, end_index):
        if manual_tokens[index].text not in leading_tokens:
            continue
        window = manual_tokens[index : min(len(manual_tokens), index + window_size)]
        if not window:
            break
        window_tokens = {token.text for token in window}
        overlap = sum(1 for token in anchor_set if token in window_tokens)
        score = overlap / len(anchor_set)
        if best is None or score > best[1]:
            best = (manual_tokens[index].raw_start, score, overlap)
            if score >= 0.995:
                break
    return best


def expand_to_question_start(manual_text: str, raw_start: int, minimum_start: int = 0) -> int:
    lookback_start = max(0, raw_start - 450)
    prefix = manual_text[lookback_start:raw_start]
    question_markers = list(re.finditer(r"(?:^|\n)(?:\\section\*\{)?Question\s+\d+", prefix, re.I))
    for marker in reversed(question_markers):
        candidate = lookback_start + marker.start()
        if candidate > minimum_start:
            return candidate
    paragraph_break = prefix.rfind("\n\n")
    if paragraph_break >= 0:
        candidate = lookback_start + paragraph_break + 2
        if candidate > minimum_start:
            return candidate
    return raw_start


def next_session_after(year: int, term: str) -> tuple[int, str] | None:
    sessions: list[tuple[int, str]] = []
    for session_year in range(2013, 2027):
        for session_term in ("jan", "jun"):
            if load_catalog(session_year, session_term, None):
                sessions.append((session_year, session_term))
    sessions = sorted(set(sessions), key=lambda item: (item[0], TERM_ORDER[item[1]]))
    current = (year, term)
    if current not in sessions:
        return None
    index = sessions.index(current)
    if index + 1 >= len(sessions):
        return None
    return sessions[index + 1]


def load_questions_for_matching(pqp: dict[str, Any], year: int, term: str) -> list[dict[str, Any]]:
    questions: list[dict[str, Any]] = []
    in_mcq_block = False
    for question in pqp["questions"]:
        if question.get("kind") == "mcq":
            if not in_mcq_block:
                questions.append(question)
            in_mcq_block = True
            continue
        questions.append(question)
        in_mcq_block = False
    next_session = next_session_after(year, term)
    if not next_session:
        return questions

    next_year, next_term = next_session
    next_pqp = pqp_path(next_year, next_term)
    if not next_pqp.exists():
        return questions
    next_data = json.loads(next_pqp.read_text(encoding="utf-8"))
    if next_data.get("questions"):
        sentinel = dict(next_data["questions"][0])
        sentinel["_sentinel"] = True
        questions.append(sentinel)
    return questions


def match_questions(
    manual_text: str,
    questions: list[dict[str, Any]],
    min_score: float,
) -> list[Match]:
    manual_tokens = tokenize_with_offsets(manual_text)
    matches: list[Match] = []
    cursor = 0
    for question in questions:
        stem = question.get("content", {}).get("stem", {}).get("text", "")
        anchor = anchor_tokens(stem)
        max_scan_tokens = None if not matches else LOCAL_SCAN_TOKENS
        result = best_match_after(manual_tokens, anchor, cursor, max_scan_tokens=max_scan_tokens)
        question_number = int(question["provenance"]["sourceQuestionNumber"])
        match = Match(
            question_id=str(question["id"]),
            question_number=question_number,
            kind=str(question["kind"]),
            raw_start=-1,
            score=0.0,
            overlap=0,
            anchor_size=len(set(anchor)),
            anchor=anchor,
        )
        if not result:
            match.status = "unmatched"
            match.reason = "no fuzzy stem match"
            matches.append(match)
            continue
        raw_start, score, overlap = result
        match.raw_start = raw_start
        match.score = score
        match.overlap = overlap
        if score < min_score:
            match.status = "low-confidence"
            match.reason = f"fuzzy stem score {score:.2f} below {min_score:.2f}"
        cursor = raw_start + 1
        matches.append(match)
    adjust_premature_boundaries(manual_text, manual_tokens, matches, min_score)
    return matches


def adjust_premature_boundaries(
    manual_text: str,
    manual_tokens: list[Token],
    matches: list[Match],
    min_score: float,
) -> None:
    """Move next-question starts that were found inside the current question block."""
    for _ in range(3):
        changed = False
        for index in range(len(matches) - 1):
            current = matches[index]
            next_match = matches[index + 1]
            if current.kind == "mcq":
                continue
            if current.raw_start < 0 or next_match.raw_start < 0:
                continue
            heading = SOLUTION_HEADING_RE.search(
                manual_text,
                current.raw_start,
                min(len(manual_text), current.raw_start + 8_000),
            )
            if not heading or next_match.raw_start > heading.start():
                continue
            result = best_match_after(
                manual_tokens,
                next_match.anchor,
                heading.end(),
                max_scan_tokens=LOCAL_SCAN_TOKENS,
            )
            if not result:
                continue
            raw_start, score, overlap = result
            if score < min_score:
                continue
            if raw_start != next_match.raw_start:
                next_match.raw_start = raw_start
                next_match.score = score
                next_match.overlap = overlap
                next_match.status = "matched"
                next_match.reason = ""
                changed = True
        if not changed:
            break


def find_solution_heading(text: str, start: int, end: int) -> re.Match[str] | None:
    return SOLUTION_HEADING_RE.search(text, start, end)


def resolve_manual_image(path_text: str) -> tuple[str, Path] | None:
    original = Path(path_text)
    stem = original.stem
    candidates = [
        MANUAL_MG_IMAGES / original.name,
        MANUAL_MG_IMAGES / f"{stem}.jpg",
        MANUAL_MG_IMAGES / f"{stem}.jpeg",
        MANUAL_MG_IMAGES / f"{stem}.png",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate.name, candidate
    return None


def rewrite_and_copy_images(
    latex: str, assets_dir: Path, copy: bool
) -> tuple[str, list[str], list[str]]:
    copied: list[str] = []
    missing: list[str] = []
    assets_dir.mkdir(parents=True, exist_ok=True)

    def replace(match: re.Match[str]) -> str:
        opts = match.group("opts") or ""
        path_text = match.group("path")
        resolved = resolve_manual_image(path_text)
        if not resolved:
            missing.append(path_text)
            return match.group(0)
        filename, source = resolved
        if copy:
            target = assets_dir / filename
            if not target.exists():
                shutil.copy2(source, target)
        copied.append(filename)
        return rf"\includegraphics{opts}{{assets/{filename}}}"

    return INCLUDEGRAPHICS_RE.sub(replace, latex), copied, missing


def asset_record(filename: str) -> dict[str, Any]:
    asset_id = f"asset_{Path(filename).stem}"
    suffix = Path(filename).suffix.lower()
    mime = "image/png" if suffix == ".png" else "image/jpeg"
    return {
        "id": asset_id,
        "kind": "image",
        "filename": filename,
        "mimeType": mime,
        "storage": {"mode": "external", "path": f"assets/{filename}"},
        "source": {"originalPath": filename},
    }


def clean_repaired_solution_typst(text: str) -> str:
    text = re.sub(r"\bbold\(([^()]+)\)", r"\1", text)
    text = text.replace("abs(upright(de):) ", "")
    text = text.replace("upright(de)", '"de"')
    text = text.replace('"de": ', "")
    text = text.replace("arrow.b", "↓")
    text = re.sub(r"\bintegral\b", "∫", text)
    text = re.sub(r"\bapprox\b", "≈", text)
    return text


def repair_package(year: int, term: str, min_score: float, write: bool) -> dict[str, Any]:
    package_path = pqp_path(year, term)
    data = json.loads(package_path.read_text(encoding="utf-8"))
    manual_text = MANUAL_MG_TEX.read_text(encoding="utf-8", errors="replace")
    questions_for_matching = load_questions_for_matching(data, year, term)
    matches = match_questions(manual_text, questions_for_matching, min_score)
    match_by_id = {match.question_id: match for match in matches}
    next_match_by_id = {
        match.question_id: matches[index + 1]
        for index, match in enumerate(matches[:-1])
    }
    assets_dir = package_path.parent / "assets"
    assets_by_id = {asset["id"]: asset for asset in data.get("assets", [])}

    updated = 0
    skipped: list[dict[str, Any]] = []
    for question in data["questions"]:
        question_id = question["id"]
        match = match_by_id.get(question_id)
        next_match = next_match_by_id.get(question_id)
        if question.get("kind") == "mcq":
            continue
        if not match or match.status != "matched":
            skipped.append({"id": question_id, "reason": match.reason if match else "no match"})
            continue
        if not next_match or next_match.raw_start <= match.raw_start:
            skipped.append({"id": question_id, "reason": "missing next question delimiter"})
            continue
        raw_solution_end = next_match.raw_start
        heading = find_solution_heading(manual_text, match.raw_start, raw_solution_end)
        if not heading:
            skipped.append({"id": question_id, "reason": "no Solution heading before next question"})
            continue
        expanded_solution_end = expand_to_question_start(
            manual_text, raw_solution_end, heading.end()
        )
        solution_end = (
            expanded_solution_end
            if expanded_solution_end > heading.end()
            else raw_solution_end
        )
        latex_solution = manual_text[heading.end() : solution_end].strip()
        if not latex_solution:
            skipped.append({"id": question_id, "reason": "empty solution after heading"})
            continue

        latex_solution, image_files, missing_images = rewrite_and_copy_images(
            latex_solution, assets_dir, copy=write
        )
        typst_solution = clean_repaired_solution_typst(
            clean_typst_artifacts(latex_to_typst(latex_solution))
        )
        if not typst_solution.strip():
            skipped.append({"id": question_id, "reason": "empty typst conversion"})
            continue

        question["content"]["solution"] = {
            "format": "typst",
            "text": typst_solution,
            "extensions": {
                "latexSource": latex_solution,
                "source": "manual-combined-mathpix",
                "matchScore": round(match.score, 3),
                "matchOverlap": match.overlap,
                "matchAnchorSize": match.anchor_size,
                "missingManualImages": missing_images,
            },
        }
        question.setdefault("assets", [])
        for filename in image_files:
            record = asset_record(filename)
            assets_by_id[record["id"]] = record
            if record["id"] not in question["assets"]:
                question["assets"].append(record["id"])
        question["assets"] = sorted(set(question["assets"]))
        updated += 1

    data["assets"] = sorted(assets_by_id.values(), key=lambda item: item["id"])
    data.setdefault("diagnostics", [])
    data["diagnostics"].append(
        {
            "level": "info",
            "code": "manual-combined-solution-repair",
            "message": (
                f"Repaired {updated} non-MCQ solutions from manual combined Mathpix "
                f"for {year}-{term}."
            ),
        }
    )

    report = {
        "year": year,
        "term": term,
        "package": str(package_path),
        "manualSource": str(MANUAL_MG_TEX),
        "write": write,
        "updated": updated,
        "skipped": skipped,
        "matches": [
            {
                "id": match.question_id,
                "question": match.question_number,
                "kind": match.kind,
                "status": match.status,
                "reason": match.reason,
                "score": round(match.score, 3),
                "overlap": match.overlap,
                "anchorSize": match.anchor_size,
                "rawStart": match.raw_start,
                "anchor": match.anchor,
            }
            for match in matches
            if not match.question_id.endswith("-q01") or not match.question_id.startswith(f"mb-pc40s-{year + 1}-")
        ],
    }

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORT_DIR / f"solution-repair-{year}-{term}-report.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    if write:
        package_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        referenced = {asset["filename"] for asset in data["assets"]}
        for path in assets_dir.glob("f67fedaf-ea11-42ad-a16e-f30d2fcf2bd3-*"):
            if path.name not in referenced:
                path.unlink()
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--year", type=int, required=True)
    parser.add_argument("--term", choices=["jan", "jun"], required=True)
    parser.add_argument("--min-score", type=float, default=0.55)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    report = repair_package(args.year, args.term, args.min_score, args.write)
    print(
        json.dumps(
            {
                "year": report["year"],
                "term": report["term"],
                "write": report["write"],
                "updated": report["updated"],
                "skipped": len(report["skipped"]),
                "report": str(REPORT_DIR / f"solution-repair-{args.year}-{args.term}-report.json"),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
