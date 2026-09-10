#!/usr/bin/env python3
"""Verify the complete English Manitoba Pre-Calculus 40S source inventory."""

from __future__ import annotations

import argparse
import json
from typing import Any

from manitoba_mathpix_common import MB_DIR, downloaded_outputs, load_manifest, source_documents


# Tests were suspended after January 2020 through June 2023. Add each newly
# published sitting here before submitting it to Mathpix.
EXPECTED_SESSIONS = (
    (2013, "jan"),
    (2013, "jun"),
    (2014, "jan"),
    (2014, "jun"),
    (2015, "jan"),
    (2015, "jun"),
    (2016, "jan"),
    (2016, "jun"),
    (2017, "jan"),
    (2017, "jun"),
    (2018, "jan"),
    (2018, "jun"),
    (2019, "jan"),
    (2019, "jun"),
    (2020, "jan"),
    (2024, "jan"),
    (2024, "jun"),
    (2025, "jan"),
    (2025, "jun"),
    (2026, "jan"),
    (2026, "jun"),
)

CATALOG_PATH = MB_DIR / "catalog" / "question_catalog.json"


def expected_document_ids() -> set[str]:
    return {
        f"pc_{year}_{term}_{suffix}"
        for year, term in EXPECTED_SESSIONS
        for suffix in ("sb1", "sb2", "mg")
    }


def catalog_rows() -> list[dict[str, Any]]:
    payload = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    return payload["questions"] if isinstance(payload, dict) else payload


def build_report() -> dict[str, Any]:
    documents = source_documents()
    actual_ids = {doc.id for doc in documents}
    expected_ids = expected_document_ids()
    manifest_ids = set(load_manifest().get("documents", {}))
    rows = catalog_rows()
    catalog_sessions = {(int(row["year"]), str(row["term"])) for row in rows}
    expected_sessions = set(EXPECTED_SESSIONS)
    missing_outputs = {
        doc_id: [name for name in ("mmd", "lines_json", "tex_zip") if name not in downloaded_outputs(doc_id)]
        for doc_id in sorted(expected_ids & actual_ids)
    }
    missing_outputs = {doc_id: names for doc_id, names in missing_outputs.items() if names}

    issues = {
        "missingSourceDocuments": sorted(expected_ids - actual_ids),
        "unexpectedSourceDocuments": sorted(actual_ids - expected_ids),
        "missingManifestEntries": sorted(expected_ids - manifest_ids),
        "missingMathpixOutputs": missing_outputs,
        "missingCatalogSessions": sorted(f"{year}-{term}" for year, term in expected_sessions - catalog_sessions),
        "unexpectedCatalogSessions": sorted(
            f"{year}-{term}" for year, term in catalog_sessions - expected_sessions
        ),
    }
    return {
        "scope": "English Manitoba Pre-Calculus 40S achievement tests under the current curriculum",
        "expectedSessions": len(expected_sessions),
        "expectedSourceDocuments": len(expected_ids),
        "studentBooklets": sum(doc.kind == "student-booklet" for doc in documents),
        "markingGuides": sum(doc.kind == "marking-guide" for doc in documents),
        "catalogQuestions": len(rows),
        "issues": issues,
        "complete": not any(issues.values()),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strict", action="store_true", help="Exit nonzero if the inventory is incomplete.")
    args = parser.parse_args()
    report = build_report()
    print(json.dumps(report, indent=2))
    if args.strict and not report["complete"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
