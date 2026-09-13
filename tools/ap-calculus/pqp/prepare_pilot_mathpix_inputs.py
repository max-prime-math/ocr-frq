#!/usr/bin/env python3
"""Prepare page-limited *AB-only* pilot inputs without contacting Mathpix."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import fitz

from build_pilot_catalog import OUT, ROOT


INPUT_DIR = ROOT / "data" / "ap-calculus" / "pilot" / "mathpix-inputs"
QUEUE = INPUT_DIR / "submission-queue.json"


def build_queue(write: bool) -> list[dict]:
    if not OUT.is_file():
        raise SystemExit("Pilot catalog missing; run build_pilot_catalog.py first")
    catalog = json.loads(OUT.read_text(encoding="utf-8"))
    queue: list[dict] = []
    for question in catalog["questions"]:
        # BC has retained ZIP artifacts.  Only AB needs a new, intentionally
        # tiny OCR pilot.  Every prompt remains paired to an SG in the catalog.
        if question["course"] != "AB":
            continue
        source = question["source"]
        output = INPUT_DIR / f"{question['id']}.pdf"
        record = {
            "id": question["id"],
            "sourcePdf": source["prompt"]["path"],
            "sourceSha256": source["prompt"]["sha256"],
            "sourcePages": source["promptPages"],
            "output": str(output.relative_to(ROOT)),
            "submissionState": "prepared" if output.exists() else "not-written",
        }
        if write:
            original = fitz.open(ROOT / source["prompt"]["path"])
            clipped = fitz.open()
            for page in source["promptPages"]:
                clipped.insert_pdf(original, from_page=page - 1, to_page=page - 1)
            output.parent.mkdir(parents=True, exist_ok=True)
            clipped.save(output)
            clipped.close()
            original.close()
            record["submissionState"] = "prepared"
        queue.append(record)
    if write:
        QUEUE.write_text(json.dumps({"schemaVersion": 1, "submission": "not-submitted", "questions": queue}, indent=2) + "\n", encoding="utf-8")
    return queue


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="Write the six reviewable input PDFs; no API request is made")
    args = parser.parse_args()
    queue = build_queue(args.write)
    print(json.dumps({"abPilotInputs": len(queue), "wrote": args.write, "submitted": False}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
