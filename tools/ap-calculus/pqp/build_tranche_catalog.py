#!/usr/bin/env python3
"""Build a source-locked, cache-aware AP Calculus FRQ tranche catalog."""

from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path
from typing import Any

import fitz


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DEFAULT_MANIFEST = HERE / "tranche_01_manifest.json"
DEFAULT_OUT = ROOT / "data" / "ap-calculus" / "tranches" / "tranche-01" / "catalog.json"


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


def zip_record(relative: str) -> dict[str, Any]:
    path = resolve(relative)
    with zipfile.ZipFile(path) as archive:
        names = [name for name in archive.namelist() if not name.endswith("/")]
        tex = [name for name in names if name.endswith(".tex")]
        images = [name for name in names if "/images/" in name and Path(name).suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}]
    if len(tex) != 1:
        raise ValueError(f"{relative}: expected exactly one Mathpix TeX file")
    return {"path": relative, "sha256": sha256(path), "texMember": tex[0], "imageCount": len(images)}


def page_list(value: Any, maximum: int, identifier: str, label: str) -> list[int]:
    if not isinstance(value, list) or not value or any(not isinstance(page, int) or page < 1 or page > maximum for page in value):
        raise ValueError(f"{identifier}: invalid {label}")
    return value


def build(manifest_path: Path = DEFAULT_MANIFEST) -> dict[str, Any]:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("schemaVersion") != 1:
        raise ValueError("Unsupported tranche manifest schemaVersion")
    rows = manifest.get("questions")
    if not isinstance(rows, list) or len(rows) != 12:
        raise ValueError("A tranche must contain exactly 12 questions")
    ids: set[str] = set()
    catalog: list[dict[str, Any]] = []
    for row in rows:
        identifier = row.get("id")
        if not isinstance(identifier, str) or identifier in ids:
            raise ValueError(f"Missing or duplicate tranche ID: {identifier!r}")
        ids.add(identifier)
        if row.get("course") not in {"AB", "BC"} or row.get("form") not in {"standard", "B"}:
            raise ValueError(f"{identifier}: invalid course or form")
        if not isinstance(row.get("question"), int) or not 1 <= row["question"] <= 6:
            raise ValueError(f"{identifier}: question must be in 1..6")
        prompt, scoring = pdf_record(row["promptPdf"]), pdf_record(row["scoringGuidePdf"])
        prompt_pages = page_list(row.get("promptPages"), prompt["pages"], identifier, "promptPages")
        scoring_pages = page_list(row.get("scoringGuidePages"), scoring["pages"], identifier, "scoringGuidePages")
        legacy = row.get("legacyMathpix")
        if not isinstance(legacy, dict) or set(legacy) != {"promptZip", "scoringGuideZip"}:
            raise ValueError(f"{identifier}: paired retained Mathpix ZIPs are required")
        catalog.append({
            "id": identifier, "course": row["course"], "year": row["year"], "form": row["form"], "question": row["question"],
            "source": {"prompt": prompt, "scoringGuide": scoring, "promptPages": prompt_pages, "scoringGuidePages": scoring_pages},
            "legacyMathpix": {"promptZip": zip_record(legacy["promptZip"]), "scoringGuideZip": zip_record(legacy["scoringGuideZip"])},
            "focus": row.get("focus", []), "status": "legacy-artifacts-available", "publishState": "blocked",
        })
    return {"schemaVersion": 1, "tranche": manifest["tranche"], "purpose": manifest["purpose"], "questionCount": len(catalog), "questions": catalog}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    rendered = json.dumps(build(args.manifest), indent=2, sort_keys=True) + "\n"
    if args.check:
        if not args.output.is_file() or args.output.read_text(encoding="utf-8") != rendered:
            raise SystemExit("Tranche catalog is stale or missing; run build_tranche_catalog.py")
        print(f"PASS: {args.output.relative_to(ROOT)} is source-locked and current")
        return 0
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(rendered, encoding="utf-8")
    print(json.dumps({"questions": 12, "output": str(args.output), "status": "source-locked", "mathpixSubmission": "not-required"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
