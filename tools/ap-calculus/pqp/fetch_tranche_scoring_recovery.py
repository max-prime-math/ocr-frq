#!/usr/bin/env python3
"""Poll and retain Mathpix artifacts for tranche scoring-guide recovery."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import requests

from submit_tranche_scoring_recovery import API, CACHE, ROOT, load_credentials

DONE = {"completed", "complete", "finished", "success"}
FAILED = {"error", "failed", "failure"}
OUTPUTS = ("mmd", "lines.json", "tex.zip")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--poll", action="store_true")
    parser.add_argument("--sleep", type=int, default=10)
    parser.add_argument("--timeout", type=int, default=900)
    parser.add_argument("--cache", type=Path, default=CACHE)
    args = parser.parse_args()
    cache = args.cache if args.cache.is_absolute() else ROOT / args.cache
    headers, started = load_credentials(), time.monotonic()
    while True:
        state = json.loads(cache.read_text(encoding="utf-8"))
        rows = []
        for identifier, entry in sorted(state["documents"].items()):
            response = requests.get(f"{API}/{entry['pdfId']}", headers=headers, timeout=120)
            if response.status_code >= 400:
                raise RuntimeError(f"Mathpix status failed for {identifier}: HTTP {response.status_code}")
            payload = response.json()
            status = str(payload.get("status") or payload.get("conversion_status") or payload.get("state") or "unknown").lower()
            entry["status"] = status
            row = {"id": identifier, "status": status, "downloads": {}}
            if status in DONE or float(payload.get("percent_done") or payload.get("percentDone") or 0) >= 100:
                out = cache.parent / "artifacts" / identifier
                out.mkdir(parents=True, exist_ok=True)
                for extension in OUTPUTS:
                    artifact = requests.get(f"{API}/{entry['pdfId']}.{extension}", headers=headers, timeout=120)
                    if artifact.status_code == 404:
                        row["downloads"][extension] = "missing"
                    elif artifact.status_code >= 400:
                        raise RuntimeError(f"Mathpix download failed for {identifier}.{extension}: HTTP {artifact.status_code}")
                    else:
                        target = out / extension.replace(".", "_")
                        target.write_bytes(artifact.content)
                        row["downloads"][extension] = str(target.relative_to(ROOT))
                entry["outputs"] = row["downloads"]
                entry["status"] = "completed"
                row["status"] = "completed"
            elif status in FAILED:
                entry["error"] = payload
            rows.append(row)
        cache.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        print(json.dumps({"documents": rows}, indent=2))
        pending = [row for row in rows if row["status"] not in DONE | FAILED]
        if not args.poll or not pending:
            return 0
        if time.monotonic() - started >= args.timeout:
            raise TimeoutError(f"Timed out while {len(pending)} recovery documents remain unfinished")
        time.sleep(args.sleep)


if __name__ == "__main__":
    raise SystemExit(main())
