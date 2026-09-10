#!/usr/bin/env python3
"""Report Mathpix ingestion status for Manitoba source PDFs."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from typing import Any

from manitoba_mathpix_common import (
    MANIFEST_PATH,
    downloaded_outputs,
    filtered_input_path,
    load_manifest,
    manifest_entry_for,
    selected_ids,
    sha256_file,
    source_documents,
)


def document_status(entry: dict[str, Any] | None, doc_id: str) -> str:
    if not entry:
        return "not-submitted"
    if entry.get("error"):
        return "error"
    status = str(entry.get("status") or "").strip()
    if status:
        return status
    if entry.get("pdfId"):
        return "submitted"
    return "not-submitted"


def current_upload_path(doc, entry: dict[str, Any] | None):
    """Resolve the input that would be uploaded now for an existing manifest entry."""
    if entry and entry.get("uploadInputSet") == "original":
        return doc.path
    filtered = filtered_input_path(doc)
    return filtered if filtered.exists() else doc.path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--kind", choices=["student-booklet", "marking-guide"], help="Limit by source type.")
    parser.add_argument("--id", action="append", dest="ids", help="Limit to one document id. Repeatable.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    args = parser.parse_args()

    manifest = load_manifest()
    documents = source_documents(kind=args.kind, ids=selected_ids(args.ids))

    rows: list[dict[str, Any]] = []
    counts: Counter[str] = Counter()
    for doc in documents:
        expected = manifest_entry_for(doc)
        entry = manifest.get("documents", {}).get(doc.id)
        outputs = downloaded_outputs(doc.id)
        status = document_status(entry, doc.id)
        upload_path = current_upload_path(doc, entry)
        current_upload_sha = sha256_file(upload_path)
        recorded_upload_sha = entry.get("uploadSha256") if entry else None
        upload_changed = bool(recorded_upload_sha and current_upload_sha != recorded_upload_sha)
        source_changed = bool(
            entry and entry.get("sourceSha256") and entry.get("sourceSha256") != expected["sourceSha256"]
        )
        missing_outputs = [ext for ext in ("mmd", "lines_json", "tex_zip") if ext not in outputs]
        if source_changed or upload_changed:
            status = "input-changed"
        elif missing_outputs and status == "completed":
            status = "cache-incomplete"
        counts[status] += 1
        rows.append(
            {
                **expected,
                "pdfId": entry.get("pdfId") if entry else None,
                "status": status,
                "recordedStatus": document_status(entry, doc.id),
                "percentDone": entry.get("percentDone") if entry else None,
                "outputs": outputs,
                "missingOutputs": missing_outputs,
                "currentUploadPdf": str(upload_path),
                "recordedUploadSha256": recorded_upload_sha,
                "currentUploadSha256": current_upload_sha,
                "uploadChanged": upload_changed,
                "sourceChanged": source_changed,
            }
        )

    result = {
        "sourceCount": len(documents),
        "counts": dict(sorted(counts.items())),
        "manifestPath": str(MANIFEST_PATH),
        "documents": rows,
    }
    if args.json:
        print(json.dumps(result, indent=2))
        return

    print(f"Sources: {result['sourceCount']}")
    for name, count in result["counts"].items():
        print(f"{name}: {count}")
    print()
    for row in rows:
        output_text = ", ".join(sorted(row["outputs"])) or "-"
        pdf_id = row["pdfId"] or "-"
        print(
            f"{row['id']:18} {row['kind']:15} pages={row['sourcePages']:>3} "
            f"status={row['status']:14} pdf_id={pdf_id} outputs={output_text}"
        )


if __name__ == "__main__":
    main()
