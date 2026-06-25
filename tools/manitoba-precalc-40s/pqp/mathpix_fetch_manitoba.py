#!/usr/bin/env python3
"""Poll Mathpix PDF jobs and download finished Manitoba OCR artifacts."""

from __future__ import annotations

import argparse
import json
import time
from typing import Any

import requests

from manitoba_mathpix_common import (
    DOWNLOAD_EXTENSIONS,
    MATHPIX_API_BASE,
    document_cache_dir,
    downloaded_outputs,
    load_manifest,
    mathpix_headers,
    save_manifest,
    selected_ids,
    source_documents,
    utc_now,
)


COMPLETE_STATUSES = {"completed", "complete", "finished", "success"}
FAILED_STATUSES = {"error", "failed", "failure"}


def fetch_status(pdf_id: str, headers: dict[str, str]) -> dict[str, Any]:
    response = requests.get(f"{MATHPIX_API_BASE}/v3/pdf/{pdf_id}", headers=headers, timeout=60)
    try:
        payload = response.json()
    except ValueError:
        payload = {"text": response.text}
    if response.status_code >= 400:
        raise RuntimeError(f"Mathpix status failed for {pdf_id}: HTTP {response.status_code}: {payload}")
    return payload


def normalize_status(payload: dict[str, Any]) -> str:
    for key in ("status", "conversion_status", "state"):
        value = str(payload.get(key) or "").strip().lower()
        if value:
            return value
    if payload.get("error"):
        return "error"
    return "unknown"


def is_complete(status: str, payload: dict[str, Any]) -> bool:
    if status in COMPLETE_STATUSES:
        return True
    percent = payload.get("percent_done") or payload.get("percentDone")
    try:
        return float(percent) >= 100
    except (TypeError, ValueError):
        return False


def download_output(doc_id: str, pdf_id: str, ext: str, headers: dict[str, str], overwrite: bool) -> str:
    out_dir = document_cache_dir(doc_id)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{doc_id}.{ext}"
    if out_path.exists() and not overwrite:
        return "kept"

    response = requests.get(f"{MATHPIX_API_BASE}/v3/pdf/{pdf_id}.{ext}", headers=headers, timeout=120)
    if response.status_code == 404:
        return "missing"
    if response.status_code >= 400:
        raise RuntimeError(
            f"Mathpix download failed for {doc_id}.{ext}: HTTP {response.status_code}: {response.text[:500]}"
        )
    out_path.write_bytes(response.content)
    return "downloaded"


def process_once(
    manifest: dict[str, Any],
    doc_ids: list[str],
    headers: dict[str, str],
    overwrite: bool,
    download_only: bool,
) -> dict[str, Any]:
    documents = manifest.setdefault("documents", {})
    rows = []
    for doc_id in doc_ids:
        entry = documents.get(doc_id)
        if not entry or not entry.get("pdfId"):
            rows.append({"id": doc_id, "status": "not-submitted"})
            continue

        pdf_id = entry["pdfId"]
        if download_only:
            payload = {"status": entry.get("status", "unknown")}
            status = str(entry.get("status", "unknown")).lower()
        else:
            payload = fetch_status(pdf_id, headers)
            status = normalize_status(payload)
            entry["status"] = status
            entry["lastCheckedAt"] = utc_now()
            entry["mathpixStatus"] = payload
            if "percent_done" in payload:
                entry["percentDone"] = payload["percent_done"]
            elif "percentDone" in payload:
                entry["percentDone"] = payload["percentDone"]

        downloads = {}
        if is_complete(status, payload):
            for ext in DOWNLOAD_EXTENSIONS:
                downloads[ext] = download_output(doc_id, pdf_id, ext, headers, overwrite)
            entry["outputs"] = downloaded_outputs(doc_id)
            entry["downloadedAt"] = utc_now()
        elif status in FAILED_STATUSES:
            entry["error"] = payload

        rows.append({"id": doc_id, "status": entry.get("status"), "pdfId": pdf_id, "downloads": downloads})

    save_manifest(manifest)
    return {"documents": rows}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--kind", choices=["student-booklet", "marking-guide"], help="Limit by source type.")
    parser.add_argument("--id", action="append", dest="ids", help="Fetch one document id. Repeatable.")
    parser.add_argument("--poll", action="store_true", help="Keep polling until all selected jobs finish or fail.")
    parser.add_argument("--sleep", type=int, default=15, help="Seconds between poll attempts.")
    parser.add_argument("--timeout", type=int, default=3600, help="Maximum polling seconds.")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite downloaded artifacts.")
    parser.add_argument("--download-only", action="store_true", help="Skip status calls and try downloads from manifest ids.")
    args = parser.parse_args()

    docs = source_documents(kind=args.kind, ids=selected_ids(args.ids))
    doc_ids = [doc.id for doc in docs]
    headers = mathpix_headers()
    started = time.monotonic()

    while True:
        manifest = load_manifest()
        result = process_once(manifest, doc_ids, headers, args.overwrite, args.download_only)
        print(json.dumps(result, indent=2))

        unfinished = [
            row
            for row in result["documents"]
            if str(row.get("status") or "").lower() not in COMPLETE_STATUSES | FAILED_STATUSES
        ]
        if not args.poll or not unfinished:
            break
        if time.monotonic() - started > args.timeout:
            raise TimeoutError(f"Timed out with {len(unfinished)} unfinished Mathpix jobs.")
        time.sleep(args.sleep)


if __name__ == "__main__":
    main()
