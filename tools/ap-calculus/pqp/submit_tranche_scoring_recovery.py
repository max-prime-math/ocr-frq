#!/usr/bin/env python3
"""Submit only prepared, page-limited tranche scoring guides to Mathpix."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

import fitz
import requests

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
QUEUE = ROOT / "data" / "ap-calculus" / "tranches" / "tranche-01" / "mathpix-recovery-inputs" / "submission-queue.json"
CACHE = ROOT / "data" / "ap-calculus" / "tranches" / "tranche-01" / "mathpix-recovery-cache" / "manifest.json"
API = "https://api.mathpix.com/v3/pdf"
OPTIONS = {"conversion_formats": {"tex.zip": True}}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_credentials() -> dict[str, str]:
    env = ROOT / ".mathpix.env"
    if env.is_file():
        for line in env.read_text(encoding="utf-8").splitlines():
            if "=" not in line or line.lstrip().startswith("#"):
                continue
            key, value = line.split("=", 1)
            key = key.strip().removeprefix("export ").strip()
            if key in {"MATHPIX_APP_ID", "MATHPIX_APP_KEY"}:
                os.environ.setdefault(key, value.strip().strip("\"").strip("'"))
    if not os.environ.get("MATHPIX_APP_ID") or not os.environ.get("MATHPIX_APP_KEY"):
        raise RuntimeError("MATHPIX_APP_ID and MATHPIX_APP_KEY are required")
    return {"app_id": os.environ["MATHPIX_APP_ID"], "app_key": os.environ["MATHPIX_APP_KEY"]}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--id", action="append", help="Question ID; repeat to narrow the queue")
    args = parser.parse_args()
    queue = json.loads(QUEUE.read_text(encoding="utf-8"))
    wanted = set(args.id) if args.id else None
    rows = [row for row in queue["artifacts"] if wanted is None or row["id"] in wanted]
    if not rows:
        raise SystemExit("No selected recovery documents")
    state = json.loads(CACHE.read_text(encoding="utf-8")) if CACHE.is_file() else {"schemaVersion": 1, "documents": {}}
    documents = state["documents"]
    headers = None if args.dry_run else load_credentials()
    result = {"submitted": [], "skipped": []}
    for row in rows:
        input_path, source_path = ROOT / row["output"], ROOT / row["sourcePdf"]
        if not input_path.is_file() or not source_path.is_file() or sha256(source_path) != row["sourceSha256"]:
            raise RuntimeError(f"Source or prepared input changed: {row['id']}")
        with fitz.open(input_path) as pdf:
            if len(pdf) != 1:
                raise RuntimeError(f"Recovery input must be one page: {row['output']}")
        upload_hash = sha256(input_path)
        old = documents.get(row["id"])
        if old and old.get("uploadSha256") == upload_hash and old.get("pdfId"):
            result["skipped"].append({"id": row["id"], "reason": "already-submitted", "pdfId": old["pdfId"]})
            continue
        if args.dry_run:
            result["submitted"].append({"id": row["id"], "dryRun": True})
            continue
        with input_path.open("rb") as handle:
            response = requests.post(API, headers=headers, files={"file": (input_path.name, handle, "application/pdf")}, data={"options_json": json.dumps(OPTIONS)}, timeout=120)
        payload = response.json() if response.headers.get("content-type", "").startswith("application/json") else {"text": response.text[:500]}
        if response.status_code >= 400 or not (pdf_id := payload.get("pdf_id") or payload.get("pdfId")):
            raise RuntimeError(f"Mathpix upload failed for {row['id']}: HTTP {response.status_code}: {payload}")
        documents[row["id"]] = {**row, "uploadSha256": upload_hash, "pdfId": pdf_id, "submittedAt": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"), "response": payload}
        CACHE.parent.mkdir(parents=True, exist_ok=True)
        CACHE.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        result["submitted"].append({"id": row["id"], "pdfId": pdf_id})
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
