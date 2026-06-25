#!/usr/bin/env python3
"""Preflight Manitoba Mathpix artifacts before exporting PQP packages."""

from __future__ import annotations

import argparse
import json
import shutil
from collections import defaultdict
from pathlib import Path
from typing import Any

from manitoba_mathpix_common import CACHE_DIR, MB_DIR, downloaded_outputs, load_manifest, source_documents


CATALOG_JSON = MB_DIR / "catalog" / "question_catalog.json"
REPORT_PATH = CACHE_DIR / "pqp_preflight_report.json"


def load_catalog() -> list[dict[str, Any]]:
    data = json.loads(CATALOG_JSON.read_text(encoding="utf-8"))
    if isinstance(data, dict) and "questions" in data:
        return list(data["questions"])
    if isinstance(data, list):
        return data
    raise ValueError(f"Unexpected catalog shape in {CATALOG_JSON}")


def doc_id_for_catalog_row(row: dict[str, Any]) -> str:
    return f"pc_{int(row['year'])}_{row['term']}_sb{int(row['booklet'])}"


def mg_id_for_catalog_row(row: dict[str, Any]) -> str:
    return f"pc_{int(row['year'])}_{row['term']}_mg"


def missing_output_ids(doc_ids: set[str]) -> dict[str, list[str]]:
    missing: dict[str, list[str]] = {}
    for doc_id in sorted(doc_ids):
        outputs = downloaded_outputs(doc_id)
        absent = [name for name in ("mmd", "lines_json", "tex_zip") if name not in outputs]
        if absent:
            missing[doc_id] = absent
    return missing


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strict", action="store_true", help="Exit nonzero when required Mathpix outputs are missing.")
    args = parser.parse_args()

    catalog = load_catalog()
    manifest = load_manifest()
    source_ids = {doc.id for doc in source_documents()}
    catalog_student_ids = {doc_id_for_catalog_row(row) for row in catalog}
    catalog_mg_ids = {mg_id_for_catalog_row(row) for row in catalog}
    missing_sources = sorted((catalog_student_ids | catalog_mg_ids) - source_ids)
    missing_manifest = sorted((catalog_student_ids | catalog_mg_ids) - set(manifest.get("documents", {})))
    missing_outputs = missing_output_ids(catalog_student_ids | catalog_mg_ids)

    report = {
        "catalog": str(CATALOG_JSON),
        "questionCount": len(catalog),
        "sourceDocumentCount": len(source_ids),
        "requiredStudentBooklets": sorted(catalog_student_ids),
        "requiredMarkingGuides": sorted(catalog_mg_ids),
        "missingSources": missing_sources,
        "missingManifestEntries": missing_manifest,
        "missingOutputs": missing_outputs,
        "mitex": shutil.which("mitex") or "/home/max/.cargo/bin/mitex",
        "readyForExporter": not missing_sources and not missing_manifest and not missing_outputs,
        "note": (
            "This is a preflight scaffold. After the Mathpix cache is populated, "
            "the PQP exporter should segment lines.json/mmd by catalog pages and "
            "convert LaTeX math to Typst with mitex."
        ),
    }

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))

    if args.strict and not report["readyForExporter"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
