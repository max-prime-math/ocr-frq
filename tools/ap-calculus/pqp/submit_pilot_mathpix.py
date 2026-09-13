#!/usr/bin/env python3
"""Submit only the prepared AP Calculus calibration pages to Mathpix.

The queue is intentionally separate from the source catalog.  This script
never changes a PQP or TestGen bank, and its hash check prevents an accidental
upload of a different PDF under a pilot identifier.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import fitz
import requests

from build_pilot_catalog import ROOT


INPUT_DIR = ROOT / "data" / "ap-calculus" / "pilot" / "mathpix-inputs"
QUEUE = INPUT_DIR / "submission-queue.json"
CACHE = ROOT / "data" / "ap-calculus" / "pilot" / "mathpix-cache" / "manifest.json"
API = "https://api.mathpix.com/v3/pdf"
# The PDF endpoint accepts a requested TeX ZIP.  Metadata and Markdown are
# fetched from their own endpoints; asking for them here is rejected before a
# document is accepted.
OPTIONS = {"conversion_formats": {"tex.zip": True}}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_local_mathpix_env() -> None:
    """Load the two local credentials without logging their values."""
    env_path = ROOT / ".mathpix.env"
    if env_path.is_file():
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip().removeprefix("export ").strip()
            if key in {"MATHPIX_APP_ID", "MATHPIX_APP_KEY"}:
                os.environ.setdefault(key, value.strip().strip('"').strip("'"))
    if not os.environ.get("MATHPIX_APP_ID") or not os.environ.get("MATHPIX_APP_KEY"):
        raise RuntimeError("MATHPIX_APP_ID and MATHPIX_APP_KEY are required in .mathpix.env or the environment")


def load_state() -> dict[str, Any]:
    if not CACHE.is_file():
        return {"schemaVersion": 1, "documents": {}}
    return json.loads(CACHE.read_text(encoding="utf-8"))


def save_state(state: dict[str, Any]) -> None:
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    tmp = CACHE.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    tmp.replace(CACHE)


def preflight(queue: dict[str, Any], selected: set[str] | None) -> list[dict[str, Any]]:
    if queue.get("submission") != "not-submitted":
        raise RuntimeError("Queue is not in the not-submitted state")
    artifacts = [artifact for item in queue["questions"] if selected is None or item["id"] in selected for artifact in item["artifacts"]]
    if not artifacts:
        raise RuntimeError("No selected pilot documents")
    for artifact in artifacts:
        path = ROOT / artifact["output"]
        if not path.is_file():
            raise RuntimeError(f"Prepared input missing: {artifact['output']}")
        source = ROOT / artifact["sourcePdf"]
        if not source.is_file() or sha256(source) != artifact["sourceSha256"]:
            raise RuntimeError(f"Source fingerprint changed after input preparation: {artifact['sourcePdf']}")
        with fitz.open(path) as pdf:
            if len(pdf) != 1:
                raise RuntimeError(f"Pilot input must be exactly one page: {artifact['output']}")
    return artifacts


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--id", action="append", help="Pilot question id; repeat to narrow the queue")
    parser.add_argument("--force", action="store_true", help="Resubmit a document already recorded with its current derived-PDF hash")
    args = parser.parse_args()
    if not QUEUE.is_file():
        raise SystemExit("Queue missing; run prepare_pilot_mathpix_inputs.py --write first")
    queue = json.loads(QUEUE.read_text(encoding="utf-8"))
    selected = set(args.id) if args.id else None
    artifacts = preflight(queue, selected)
    state = load_state()
    documents = state.setdefault("documents", {})
    result: dict[str, list[dict[str, Any]]] = {"submitted": [], "skipped": []}
    headers = None
    if not args.dry_run:
        load_local_mathpix_env()
        headers = {"app_id": os.environ["MATHPIX_APP_ID"], "app_key": os.environ["MATHPIX_APP_KEY"]}
    for artifact in artifacts:
        path = ROOT / artifact["output"]
        identifier = f"{artifact['output']}"
        upload_hash = sha256(path)
        old = documents.get(identifier)
        if old and old.get("uploadSha256") == upload_hash and old.get("pdfId") and not args.force:
            result["skipped"].append({"input": identifier, "reason": "already-submitted", "pdfId": old["pdfId"]})
            continue
        if args.dry_run:
            result["submitted"].append({"input": identifier, "dryRun": True, "kind": artifact["kind"]})
            continue
        with path.open("rb") as handle:
            response = requests.post(API, headers=headers, files={"file": (path.name, handle, "application/pdf")}, data={"options_json": json.dumps(OPTIONS)}, timeout=120)
        try:
            payload = response.json()
        except ValueError:
            payload = {"text": response.text[:500]}
        if response.status_code >= 400:
            raise RuntimeError(f"Mathpix upload failed for {path.name}: HTTP {response.status_code}: {payload}")
        pdf_id = payload.get("pdf_id") or payload.get("pdfId")
        if not pdf_id:
            raise RuntimeError(f"Mathpix supplied no pdf_id for {path.name}: {payload}")
        documents[identifier] = {
            "kind": artifact["kind"],
            "questionId": next(item["id"] for item in queue["questions"] if artifact in item["artifacts"]),
            "sourcePdf": artifact["sourcePdf"],
            "sourceSha256": artifact["sourceSha256"],
            "sourcePages": artifact["sourcePages"],
            "uploadSha256": upload_hash,
            "pdfId": pdf_id,
            "submittedAt": utc_now(),
            "response": payload,
        }
        save_state(state)
        result["submitted"].append({"input": identifier, "pdfId": pdf_id, "kind": artifact["kind"]})
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
