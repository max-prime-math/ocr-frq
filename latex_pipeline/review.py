from __future__ import annotations

import json
from pathlib import Path


def load_skip_set(review_file: str) -> set[str]:
    path = Path(review_file)
    if not path.exists():
        return set()
    data = json.loads(path.read_text(encoding="utf-8"))
    return set(data.get("skip_block_ids", []))


def write_review_template(review_file: str, unresolved_blocks: list[str]) -> None:
    path = Path(review_file)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "skip_block_ids": [],
        "notes": {
            "instructions": "Add block IDs to skip_block_ids to omit those blocks from the LaTeX output.",
            "unresolved_block_ids": unresolved_blocks,
        },
    }
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
