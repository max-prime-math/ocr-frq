#!/usr/bin/env python3
"""Create source-traceable, unreviewed records for the 12-question FRQ pilot.

These records are deliberately not PQPs.  They retain raw OCR separately from
the scoring guide, source fingerprints, and extracted image ownership before
any Typst or publication step can discard evidence.
"""

from __future__ import annotations

import json
import re
import shutil
import tempfile
import zipfile
from pathlib import Path
from typing import Any

from build_pilot_catalog import OUT as CATALOG, ROOT

import sys
sys.path.insert(0, str(ROOT))
from src.mathpix import parse_exam_zip, parse_sg_zip  # noqa: E402


STAGE = ROOT / "data" / "ap-calculus" / "pilot" / "staging" / "intermediate"
MATHPIX = ROOT / "data" / "ap-calculus" / "pilot" / "mathpix-cache" / "artifacts"
QUESTION_ITEM = re.compile(r"(?m)^(?:\\item\[(?P<item>\d+)\.\]|(?P<plain>\d+)\.)\s*")


def read_mmd(question_id: str, kind: str) -> tuple[str, Path]:
    directory = MATHPIX / f"{question_id}-{kind}"
    path = directory / "mmd"
    if not path.is_file():
        raise FileNotFoundError(f"Missing fetched Mathpix artifact: {path}")
    return path.read_text(encoding="utf-8"), directory


def strip_prompt_to_question(raw: str, question: int) -> str:
    """Retain a preceding figure when it visually belongs to this question."""
    matches = list(QUESTION_ITEM.finditer(raw))
    match = next((item for item in matches if int(item.group("item") or item.group("plain")) == question), None)
    if match is None:
        raise ValueError(f"Could not find question {question} in Mathpix prompt")
    before = raw[:match.start()]
    figure_start = before.rfind(r"\begin{figure}")
    prefix = before[figure_start:] if figure_start >= 0 and r"\end{figure}" in before[figure_start:] else ""
    text = prefix + raw[match.start():]
    text = re.split(r"\\section\*\{(?:WRITE ALL WORK|STOP|END OF EXAM)", text, maxsplit=1)[0]
    return text.strip()


def strip_scoring_to_question(raw: str, question: int) -> str:
    marker = re.compile(rf"(?:\\section\*\{{)?Question\s+{question}\b", re.I)
    match = marker.search(raw)
    if match is None:
        raise ValueError(f"Could not find Question {question} in Mathpix scoring guide")
    return raw[match.start():].strip()


def extract_zip_images(zip_path: Path, destination: Path, prefix: str) -> list[dict[str, str]]:
    images: list[dict[str, str]] = []
    with zipfile.ZipFile(zip_path) as archive:
        for name in archive.namelist():
            if name.endswith("/") or "/images/" not in name:
                continue
            suffix = Path(name).suffix.lower()
            if suffix not in {".jpg", ".jpeg", ".png", ".webp"}:
                continue
            out_name = f"{prefix}-{Path(name).name}"
            target = destination / out_name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(archive.read(name))
            images.append({"sourceName": Path(name).stem, "filename": out_name})
    return images


def legacy_record(row: dict[str, Any], assets: Path) -> dict[str, Any]:
    legacy = row["legacyMathpix"]
    with tempfile.TemporaryDirectory(prefix="ap-calc-pilot-") as directory:
        figures = Path(directory) / "figures"
        exam = parse_exam_zip(str(ROOT / legacy["promptZip"]["path"]), str(figures), row["year"], "" if row["form"] == "standard" else row["form"])
        scoring = parse_sg_zip(str(ROOT / legacy["scoringGuideZip"]["path"]), str(figures), row["year"], "" if row["form"] == "standard" else row["form"])
        block = exam[row["question"]]
        copied: list[str] = []
        for figure in block.figure_paths:
            source = figures / Path(figure).name
            if source.is_file():
                target = assets / f"{row['id']}-{source.name}"
                shutil.copy2(source, target)
                copied.append(target.name)
    return {
        "rawPrompt": block.question_text,
        "rawScoringGuide": scoring.get(row["question"], ""),
        "assets": copied,
        "ocrOrigin": "retained-legacy-mathpix-zip",
    }


def new_ab_record(row: dict[str, Any], assets: Path) -> dict[str, Any]:
    prompt, prompt_dir = read_mmd(row["id"], "prompt")
    scoring, scoring_dir = read_mmd(row["id"], "scoring-guide")
    prompt_raw = strip_prompt_to_question(prompt, row["question"])
    scoring_raw = strip_scoring_to_question(scoring, row["question"])
    images = extract_zip_images(prompt_dir / "tex_zip", assets, f"{row['id']}-prompt")
    images += extract_zip_images(scoring_dir / "tex_zip", assets, f"{row['id']}-scoring")
    return {
        "rawPrompt": prompt_raw,
        "rawScoringGuide": scoring_raw,
        "assets": images,
        "ocrOrigin": "pilot-mathpix-api",
    }


def main() -> int:
    if not CATALOG.is_file():
        raise SystemExit("Pilot catalog missing; run build_pilot_catalog.py first")
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    if STAGE.exists():
        shutil.rmtree(STAGE)
    records = STAGE / "records"
    assets = STAGE / "assets"
    records.mkdir(parents=True)
    assets.mkdir(parents=True)
    all_rows: list[dict[str, str]] = []
    for row in catalog["questions"]:
        extracted = legacy_record(row, assets) if row["legacyMathpix"] else new_ab_record(row, assets)
        record = {
            "schemaVersion": 1,
            "id": row["id"],
            "course": row["course"],
            "year": row["year"],
            "form": row["form"],
            "question": row["question"],
            "source": row["source"],
            "legacyMathpix": row["legacyMathpix"],
            "focus": row["focus"],
            **extracted,
            "solutionExtractionStatus": "unsegmented-scoring-guide",
            "reviewState": "unreviewed",
            "publishState": "blocked",
        }
        target = records / f"{row['id']}.json"
        target.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
        all_rows.append({"id": row["id"], "record": target.name})
    (STAGE / "index.json").write_text(json.dumps({"schemaVersion": 1, "records": all_rows}, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"records": len(all_rows), "stage": str(STAGE), "publishState": "blocked"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
