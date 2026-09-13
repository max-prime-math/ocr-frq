#!/usr/bin/env python3
"""Attach completed page-limited scoring OCR to blocked tranche records."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DEFAULT_CACHE = ROOT / "data" / "ap-calculus" / "tranches" / "tranche-01" / "mathpix-recovery-cache" / "manifest.json"
DEFAULT_STAGE = ROOT / "data" / "ap-calculus" / "tranches" / "tranche-01" / "staging" / "intermediate"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cache", type=Path, default=DEFAULT_CACHE)
    parser.add_argument("--stage", type=Path, default=DEFAULT_STAGE)
    args = parser.parse_args()
    state = json.loads(args.cache.read_text(encoding="utf-8"))
    records = sorted((args.stage / "records").glob("ap-*.json"))
    if len(records) != 12 or len(state.get("documents", {})) != 12:
        raise SystemExit("Expected 12 completed recovery documents and 12 intermediate records")
    attached = []
    for path in records:
        record = json.loads(path.read_text(encoding="utf-8"))
        entry = state["documents"].get(record["id"])
        if not entry or entry.get("status") != "completed":
            raise SystemExit(f"Recovery is not completed for {record['id']}")
        relative = entry.get("outputs", {}).get("mmd")
        mmd = ROOT / relative if relative else None
        if not mmd or not mmd.is_file():
            raise SystemExit(f"MMD artifact missing for {record['id']}")
        raw = mmd.read_text(encoding="utf-8").strip()
        if not raw:
            raise SystemExit(f"Empty MMD artifact for {record['id']}")
        record["rawScoringGuide"] = raw
        record["scoringGuideOcrStatus"] = "page-limited-mathpix-recovery"
        record["scoringGuideArtifact"] = relative
        record["solutionExtractionStatus"] = "unsegmented-scoring-guide"
        record["reviewState"] = "unreviewed"
        record["publishState"] = "blocked"
        path.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
        attached.append(record["id"])
    print(json.dumps({"attached": len(attached), "publishState": "blocked"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
