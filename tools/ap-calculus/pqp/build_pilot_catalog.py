#!/usr/bin/env python3
"""Build and verify the source-locked AP Calculus FRQ pilot catalog.

This deliberately has no Mathpix client.  It establishes source identity and
pilot scope before OCR costs or editorial changes are possible.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import fitz


HERE = Path(__file__).resolve().parent
# HERE is .../ocr-frq/tools/ap-calculus/pqp.
ROOT = HERE.parents[2]
MANIFEST = HERE / "pilot_manifest.json"
OUT = ROOT / "data" / "ap-calculus" / "pilot" / "pilot-catalog.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def resolve(relative: str) -> Path:
    path = ROOT / relative
    if not path.is_file():
        raise ValueError(f"Missing source file: {relative}")
    return path


def pdf_record(relative: str) -> dict[str, Any]:
    path = resolve(relative)
    with fitz.open(path) as pdf:
        pages = len(pdf)
    return {"path": relative, "sha256": sha256(path), "pages": pages}


def validate_manifest(data: dict[str, Any]) -> list[dict[str, Any]]:
    if data.get("schemaVersion") != 1:
        raise ValueError("Unsupported pilot manifest schemaVersion")
    rows = data.get("questions")
    if not isinstance(rows, list) or len(rows) != 12:
        raise ValueError("The calibration pilot must contain exactly 12 questions")

    ids: set[str] = set()
    catalog: list[dict[str, Any]] = []
    for row in rows:
        identifier = row.get("id")
        if not isinstance(identifier, str) or identifier in ids:
            raise ValueError(f"Missing or duplicate pilot ID: {identifier!r}")
        ids.add(identifier)
        if row.get("course") not in {"AB", "BC"}:
            raise ValueError(f"{identifier}: course must be AB or BC")
        if row.get("form") not in {"standard", "B"}:
            raise ValueError(f"{identifier}: form must be standard or B")
        if not isinstance(row.get("question"), int) or not 1 <= row["question"] <= 6:
            raise ValueError(f"{identifier}: question must be in 1..6")
        prompt = pdf_record(row["promptPdf"])
        scoring = pdf_record(row["scoringGuidePdf"])
        prompt_pages = row.get("promptPages")
        if not isinstance(prompt_pages, list) or not prompt_pages:
            raise ValueError(f"{identifier}: promptPages is required")
        if any(not isinstance(page, int) or page < 1 or page > prompt["pages"] for page in prompt_pages):
            raise ValueError(f"{identifier}: promptPages falls outside the prompt PDF")
        scoring_pages = row.get("scoringGuidePages")
        if scoring_pages is not None:
            if not isinstance(scoring_pages, list) or not scoring_pages:
                raise ValueError(f"{identifier}: scoringGuidePages must be a non-empty list when supplied")
            if any(not isinstance(page, int) or page < 1 or page > scoring["pages"] for page in scoring_pages):
                raise ValueError(f"{identifier}: scoringGuidePages falls outside the scoring guide")
        legacy: dict[str, Any] | None = None
        if "legacyMathpix" in row:
            legacy = {key: {"path": value, "sha256": sha256(resolve(value))}
                      for key, value in row["legacyMathpix"].items()}
        catalog.append({
            "id": identifier,
            "course": row["course"],
            "year": row["year"],
            "form": row["form"],
            "question": row["question"],
            "source": {"prompt": prompt, "scoringGuide": scoring, "promptPages": prompt_pages, "scoringGuidePages": scoring_pages},
            "legacyMathpix": legacy,
            "focus": row.get("focus", []),
            "status": "legacy-artifacts-available" if legacy else "ready-for-pilot-mathpix",
        })
    return catalog


def build() -> dict[str, Any]:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    questions = validate_manifest(manifest)
    return {
        "schemaVersion": 1,
        "pilot": manifest["pilot"],
        "purpose": manifest["purpose"],
        "questionCount": len(questions),
        "questions": questions,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Fail if the checked-in generated catalog is stale")
    args = parser.parse_args()
    rendered = json.dumps(build(), indent=2, sort_keys=True) + "\n"
    if args.check:
        if not OUT.is_file() or OUT.read_text(encoding="utf-8") != rendered:
            raise SystemExit(f"Pilot catalog is stale or missing: run {Path(__file__).name}")
        print(f"PASS: {OUT.relative_to(ROOT)} is source-locked and current")
        return 0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(rendered, encoding="utf-8")
    print(json.dumps({"questions": 12, "output": str(OUT), "status": "source-locked"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
