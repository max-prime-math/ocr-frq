#!/usr/bin/env python3
"""Prepare, but never submit, page-limited scoring-guide recovery PDFs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import fitz

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DEFAULT_CATALOG = ROOT / "data" / "ap-calculus" / "tranches" / "tranche-01" / "catalog.json"
DEFAULT_DIR = ROOT / "data" / "ap-calculus" / "tranches" / "tranche-01" / "mathpix-recovery-inputs"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_DIR)
    parser.add_argument("--write", action="store_true", help="Write reviewable PDFs; never contacts Mathpix")
    args = parser.parse_args()
    output_dir = args.output_dir if args.output_dir.is_absolute() else ROOT / args.output_dir
    catalog = json.loads(args.catalog.read_text(encoding="utf-8"))
    queue = []
    for row in catalog["questions"]:
        source = row["source"]["scoringGuide"]
        pages = row["source"]["scoringGuidePages"]
        output = output_dir / f"{row['id']}-scoring-guide.pdf"
        state = "not-written"
        if args.write:
            original, clipped = fitz.open(ROOT / source["path"]), fitz.open()
            for page in pages:
                clipped.insert_pdf(original, from_page=page - 1, to_page=page - 1)
            output.parent.mkdir(parents=True, exist_ok=True)
            if output.exists():
                output.unlink()
            clipped.save(output)
            clipped.close()
            original.close()
            state = "prepared"
        queue.append({"id": row["id"], "kind": "scoring-guide", "sourcePdf": source["path"], "sourceSha256": source["sha256"], "sourcePages": pages, "output": str(output.relative_to(ROOT)), "submissionState": state})
    if args.write:
        (output_dir / "submission-queue.json").write_text(json.dumps({"schemaVersion": 1, "submission": "not-submitted", "reason": "legacy scoring-guide segmentation is untrusted", "artifacts": queue}, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"scoringGuideRecoveryDocuments": len(queue), "wrote": args.write, "submitted": False}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
