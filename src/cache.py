"""
cache.py — Filesystem cache for Claude Vision API responses.

Stores raw JSON responses keyed by SHA-256 hash of the image content so
identical pages never hit the API twice.
"""

import hashlib
import json
import logging
from pathlib import Path
from typing import Iterable

logger = logging.getLogger(__name__)


def _image_hash(image_path: str | Iterable[str]) -> str:
    paths = [image_path] if isinstance(image_path, str) else list(image_path)
    h = hashlib.sha256()
    for path in paths:
        h.update(b"\0FILE\0")
        with open(path, "rb") as fh:
            for chunk in iter(lambda: fh.read(65536), b""):
                h.update(chunk)
    return h.hexdigest()


class FRQCache:
    """Read/write Claude Vision JSON responses to *cache_dir*."""

    def __init__(self, cache_dir: str = "cache/frq"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _path(self, image_path: str | Iterable[str]) -> Path:
        return self.cache_dir / f"{_image_hash(image_path)}.json"

    def get(self, image_path: str | Iterable[str]) -> dict | None:
        p = self._path(image_path)
        if p.exists():
            logger.debug("Cache hit: %s", p.name)
            with open(p, encoding="utf-8") as fh:
                return json.load(fh)
        return None

    def put(self, image_path: str | Iterable[str], data: dict) -> None:
        p = self._path(image_path)
        with open(p, "w", encoding="utf-8") as fh:
            json.dump(data, fh, ensure_ascii=False, indent=2)
        logger.debug("Cached → %s", p.name)

    def invalidate(self, image_path: str | Iterable[str]) -> None:
        p = self._path(image_path)
        if p.exists():
            p.unlink()
            logger.debug("Invalidated: %s", p.name)
