#!/usr/bin/env python3
"""Submit Manitoba source PDFs to the Mathpix PDF API."""

from __future__ import annotations

import argparse
import json
from typing import Any

import requests

from manitoba_mathpix_common import (
    MATHPIX_API_BASE,
    ROOT,
    filtered_input_path,
    load_manifest,
    manifest_entry_for,
    mathpix_headers,
    pdf_page_count,
    save_manifest,
    selected_ids,
    sha256_file,
    source_documents,
    utc_now,
)


DEFAULT_OPTIONS = {
    "conversion_formats": {
        "tex.zip": True,
    }
}


def same_source(existing: dict[str, Any] | None, current: dict[str, Any]) -> bool:
    return bool(
        existing
        and existing.get("sourceSha256") == current["sourceSha256"]
        and existing.get("uploadSha256") == current.get("uploadSha256")
    )


def choose_upload_path(doc, input_set: str):
    filtered_path = filtered_input_path(doc)
    if input_set == "filtered":
        if not filtered_path.exists():
            raise FileNotFoundError(
                f"Filtered input is missing for {doc.id}: {filtered_path}. "
                "Run mathpix_prepare_manitoba_inputs.py first."
            )
        return filtered_path, "filtered"
    if input_set == "original":
        return doc.path, "original"
    if filtered_path.exists():
        return filtered_path, "filtered"
    return doc.path, "original"


def submit_pdf(path, headers: dict[str, str], options: dict[str, Any]) -> dict[str, Any]:
    with path.open("rb") as handle:
        response = requests.post(
            f"{MATHPIX_API_BASE}/v3/pdf",
            headers=headers,
            files={"file": (path.name, handle, "application/pdf")},
            data={"options_json": json.dumps(options)},
            timeout=120,
        )
    try:
        payload = response.json()
    except ValueError:
        payload = {"text": response.text}
    if response.status_code >= 400:
        raise RuntimeError(f"Mathpix upload failed for {path.name}: HTTP {response.status_code}: {payload}")
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--kind", choices=["student-booklet", "marking-guide"], help="Limit by source type.")
    parser.add_argument("--id", action="append", dest="ids", help="Submit one document id. Repeatable.")
    parser.add_argument("--limit", type=int, help="Submit at most this many PDFs.")
    parser.add_argument("--force", action="store_true", help="Resubmit even when the same source hash has a pdf_id.")
    parser.add_argument(
        "--input-set",
        choices=["auto", "filtered", "original"],
        default="auto",
        help="Which PDFs to upload. auto uses page-filtered PDFs when they exist.",
    )
    parser.add_argument("--dry-run", action="store_true", help="Show what would be submitted without calling Mathpix.")
    args = parser.parse_args()

    documents = source_documents(kind=args.kind, ids=selected_ids(args.ids))
    if args.limit is not None:
        documents = documents[: args.limit]

    manifest = load_manifest()
    manifest.setdefault("documents", {})
    headers = None if args.dry_run else mathpix_headers()

    submitted = []
    skipped = []
    for doc in documents:
        current = manifest_entry_for(doc)
        upload_path, input_set = choose_upload_path(doc, args.input_set)
        current.update(
            {
                "uploadInputSet": input_set,
                "uploadPdf": upload_path.relative_to(ROOT).as_posix()
                if upload_path.is_relative_to(ROOT)
                else str(upload_path),
                "uploadSha256": sha256_file(upload_path),
                "uploadPages": pdf_page_count(upload_path),
            }
        )
        existing = manifest["documents"].get(doc.id)
        if not args.force and same_source(existing, current) and existing.get("pdfId"):
            skipped.append(
                {
                    "id": doc.id,
                    "reason": "already-submitted",
                    "pdfId": existing["pdfId"],
                    "inputSet": existing.get("uploadInputSet"),
                    "sourcePages": existing.get("sourcePages"),
                    "uploadPages": existing.get("uploadPages"),
                }
            )
            continue

        if args.dry_run:
            submitted.append(
                {
                    "id": doc.id,
                    "sourcePath": doc.relative_path,
                    "uploadPath": current["uploadPdf"],
                    "inputSet": input_set,
                    "sourcePages": current["sourcePages"],
                    "uploadPages": current["uploadPages"],
                }
            )
            continue

        payload = submit_pdf(upload_path, headers, DEFAULT_OPTIONS)
        pdf_id = payload.get("pdf_id") or payload.get("pdfId")
        if not pdf_id:
            raise RuntimeError(f"Mathpix did not return pdf_id for {doc.id}: {payload}")

        manifest["documents"][doc.id] = {
            **current,
            "pdfId": pdf_id,
            "status": "submitted",
            "submittedAt": utc_now(),
            "mathpixResponse": payload,
        }
        save_manifest(manifest)
        submitted.append(
            {
                "id": doc.id,
                "pdfId": pdf_id,
                "inputSet": input_set,
                "sourcePages": current["sourcePages"],
                "uploadPages": current["uploadPages"],
            }
        )
        print(json.dumps({"submitted": submitted[-1]}, indent=2))

    if not args.dry_run:
        save_manifest(manifest)

    print(json.dumps({"submitted": submitted, "skipped": skipped}, indent=2))


if __name__ == "__main__":
    main()
