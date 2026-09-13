#!/usr/bin/env python3
"""Stage blocked AP Calculus tranche records from retained BC Mathpix ZIPs."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DEFAULT_CATALOG = ROOT / "data" / "ap-calculus" / "tranches" / "tranche-01" / "catalog.json"
DEFAULT_STAGE = ROOT / "data" / "ap-calculus" / "tranches" / "tranche-01" / "staging" / "intermediate"

sys.path.insert(0, str(ROOT))
from src.mathpix import parse_exam_zip, parse_sg_zip  # noqa: E402


def legacy_record(row: dict[str, Any], assets: Path) -> dict[str, Any]:
    legacy = row["legacyMathpix"]
    with tempfile.TemporaryDirectory(prefix="ap-calc-tranche-") as directory:
        figures = Path(directory) / "figures"
        form = "" if row["form"] == "standard" else row["form"]
        exam = parse_exam_zip(str(ROOT / legacy["promptZip"]["path"]), str(figures), row["year"], form)
        scoring = parse_sg_zip(str(ROOT / legacy["scoringGuideZip"]["path"]), str(figures), row["year"], form)
        block = exam[row["question"]]
        copied: list[str] = []
        for figure in block.figure_paths:
            source = figures / Path(figure).name
            if source.is_file():
                target = assets / f"{row['id']}-{source.name}"
                shutil.copy2(source, target)
                copied.append(target.name)
    # Old scoring-guide ZIPs do not reliably delimit a question: for example,
    # a nonempty block can contain a later question's rubric. Retain it for
    # comparison, but never pass it to conversion or solution review.
    return {"rawPrompt": block.question_text, "retainedRawScoringGuide": scoring.get(row["question"], ""), "rawScoringGuide": "", "assets": copied, "ocrOrigin": "retained-legacy-mathpix-zip", "scoringGuideOcrStatus": "source-scoped-recovery-required"}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    parser.add_argument("--stage", type=Path, default=DEFAULT_STAGE)
    parser.add_argument("--replace", action="store_true", help="Replace this generated staging directory")
    args = parser.parse_args()
    if not args.catalog.is_file():
        raise SystemExit("Tranche catalog missing; run build_tranche_catalog.py first")
    catalog = json.loads(args.catalog.read_text(encoding="utf-8"))
    if catalog.get("questionCount") != 12 or len(catalog.get("questions", [])) != 12:
        raise SystemExit("Expected exactly 12 source-locked tranche questions")
    if args.stage.exists():
        if not args.replace:
            raise SystemExit(f"Refusing to replace existing stage: {args.stage}; pass --replace")
        shutil.rmtree(args.stage)
    records, assets = args.stage / "records", args.stage / "assets"
    records.mkdir(parents=True)
    assets.mkdir(parents=True)
    index: list[dict[str, str]] = []
    for row in catalog["questions"]:
        extracted = legacy_record(row, assets)
        record = {"schemaVersion": 1, "id": row["id"], "course": row["course"], "year": row["year"], "form": row["form"], "question": row["question"], "source": row["source"], "legacyMathpix": row["legacyMathpix"], "focus": row["focus"], **extracted, "solutionExtractionStatus": "source-scoped-scoring-ocr-required", "reviewState": "unreviewed", "publishState": "blocked"}
        target = records / f"{row['id']}.json"
        target.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
        index.append({"id": row["id"], "record": target.name})
    (args.stage / "index.json").write_text(json.dumps({"schemaVersion": 1, "records": index}, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"records": len(index), "assets": len(list(assets.iterdir())), "stage": str(args.stage), "publishState": "blocked", "mathpixSubmission": "not-required"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
