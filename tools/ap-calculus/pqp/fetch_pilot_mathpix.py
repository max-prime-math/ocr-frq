#!/usr/bin/env python3
"""Poll and retain only the OCR artifacts for the AP calibration queue."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any

import requests

from build_pilot_catalog import ROOT
from submit_pilot_mathpix import CACHE, load_local_mathpix_env, load_state, save_state, utc_now


API = "https://api.mathpix.com/v3/pdf"
OUTPUTS = ("mmd", "lines.json", "tex.zip")
DONE = {"completed", "complete", "finished", "success"}
FAILED = {"error", "failed", "failure"}


def status_of(payload: dict[str, Any]) -> str:
    for key in ("status", "conversion_status", "state"):
        if payload.get(key):
            return str(payload[key]).lower()
    return "error" if payload.get("error") else "unknown"


def complete(status: str, payload: dict[str, Any]) -> bool:
    if status in DONE:
        return True
    try:
        return float(payload.get("percent_done") or payload.get("percentDone") or 0) >= 100
    except (TypeError, ValueError):
        return False


def fetch(url: str, headers: dict[str, str]) -> requests.Response:
    response = requests.get(url, headers=headers, timeout=120)
    if response.status_code >= 400:
        raise RuntimeError(f"Mathpix request failed ({response.status_code}): {response.text[:500]}")
    return response


def process_once(headers: dict[str, str]) -> dict[str, list[dict[str, Any]]]:
    state = load_state()
    rows: list[dict[str, Any]] = []
    for input_path, entry in sorted(state.get("documents", {}).items()):
        payload = fetch(f"{API}/{entry['pdfId']}", headers).json()
        status = status_of(payload)
        entry["status"] = status
        entry["lastCheckedAt"] = utc_now()
        entry["mathpixStatus"] = payload
        row = {"input": input_path, "kind": entry["kind"], "status": status, "downloads": {}}
        if complete(status, payload):
            out_dir = CACHE.parent / "artifacts" / Path(input_path).stem
            out_dir.mkdir(parents=True, exist_ok=True)
            for extension in OUTPUTS:
                response = requests.get(f"{API}/{entry['pdfId']}.{extension}", headers=headers, timeout=120)
                if response.status_code == 404:
                    row["downloads"][extension] = "missing"
                    continue
                if response.status_code >= 400:
                    raise RuntimeError(f"Mathpix download failed for {input_path}.{extension}: HTTP {response.status_code}")
                target = out_dir / extension.replace(".", "_")
                target.write_bytes(response.content)
                row["downloads"][extension] = str(target.relative_to(ROOT))
            entry["outputs"] = row["downloads"]
            entry["downloadedAt"] = utc_now()
        elif status in FAILED:
            entry["error"] = payload
        rows.append(row)
    save_state(state)
    return {"documents": rows}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--poll", action="store_true")
    parser.add_argument("--sleep", type=int, default=10)
    parser.add_argument("--timeout", type=int, default=900)
    args = parser.parse_args()
    load_local_mathpix_env()
    headers = {"app_id": __import__("os").environ["MATHPIX_APP_ID"], "app_key": __import__("os").environ["MATHPIX_APP_KEY"]}
    started = time.monotonic()
    while True:
        result = process_once(headers)
        print(json.dumps(result, indent=2))
        pending = [row for row in result["documents"] if row["status"] not in DONE | FAILED]
        if not args.poll or not pending:
            return 0
        if time.monotonic() - started >= args.timeout:
            raise TimeoutError(f"Timed out while {len(pending)} pilot documents remain unfinished")
        time.sleep(args.sleep)


if __name__ == "__main__":
    raise SystemExit(main())
