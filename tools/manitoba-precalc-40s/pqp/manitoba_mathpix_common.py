"""Shared helpers for Manitoba Mathpix API ingestion scripts."""

from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

import fitz


ROOT = Path(__file__).resolve().parents[3]
MB_DIR = ROOT / "data" / "manitoba-precalc-40s" / "workspace"
SOURCE_DIR = MB_DIR / "source-pdfs"
STUDENT_BOOKLET_DIR = SOURCE_DIR / "student-booklets"
MARKING_GUIDE_DIR = SOURCE_DIR / "marking-guides"
CACHE_DIR = MB_DIR / "mathpix" / "api-cache"
API_INPUT_DIR = MB_DIR / "mathpix" / "api-inputs"
FILTERED_INPUT_DIR = API_INPUT_DIR / "page-filtered"
MANIFEST_PATH = CACHE_DIR / "mathpix_manifest.json"

MATHPIX_API_BASE = "https://api.mathpix.com"
DOWNLOAD_EXTENSIONS = ("mmd", "lines.json", "tex.zip")

PDF_RE = re.compile(
    r"pc_(?P<yy>\d{2})_(?P<term>jan|jun)_(?:(?P<booklet>sb[12])|(?P<mg>mg))\.pdf$",
    re.I,
)


@dataclass(frozen=True)
class SourceDocument:
    id: str
    kind: str
    year: int
    term: str
    path: Path
    booklet: int | None = None

    @property
    def relative_path(self) -> str:
        return self.path.relative_to(ROOT).as_posix()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def pdf_page_count(path: Path) -> int:
    doc = fitz.open(path)
    try:
        return len(doc)
    finally:
        doc.close()


def parse_source_document(path: Path) -> SourceDocument | None:
    match = PDF_RE.match(path.name)
    if not match:
        return None
    year = 2000 + int(match.group("yy"))
    term = match.group("term").lower()
    booklet_text = match.group("booklet")
    if booklet_text:
        booklet = int(booklet_text[-1])
        kind = "student-booklet"
        doc_id = f"pc_{year}_{term}_sb{booklet}"
    else:
        booklet = None
        kind = "marking-guide"
        doc_id = f"pc_{year}_{term}_mg"
    return SourceDocument(id=doc_id, kind=kind, year=year, term=term, booklet=booklet, path=path)


def source_documents(kind: str | None = None, ids: set[str] | None = None) -> list[SourceDocument]:
    docs: list[SourceDocument] = []
    for directory in (STUDENT_BOOKLET_DIR, MARKING_GUIDE_DIR):
        for path in sorted(directory.glob("pc_*.pdf")):
            doc = parse_source_document(path)
            if not doc:
                continue
            if kind and doc.kind != kind:
                continue
            if ids and doc.id not in ids:
                continue
            docs.append(doc)
    return sorted(docs, key=lambda item: (item.year, item.term, item.kind, item.booklet or 0, item.id))


def load_manifest() -> dict[str, Any]:
    if not MANIFEST_PATH.exists():
        return {"version": 1, "createdAt": utc_now(), "updatedAt": utc_now(), "documents": {}}
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def save_manifest(manifest: dict[str, Any]) -> None:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    manifest["updatedAt"] = utc_now()
    tmp = MANIFEST_PATH.with_suffix(".tmp")
    tmp.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    tmp.replace(MANIFEST_PATH)


def document_cache_dir(doc_id: str) -> Path:
    return CACHE_DIR / doc_id


def filtered_input_path(doc: SourceDocument) -> Path:
    if doc.kind == "student-booklet":
        return FILTERED_INPUT_DIR / "student-booklets" / doc.path.name
    return FILTERED_INPUT_DIR / "marking-guides" / doc.path.name


def downloaded_outputs(doc_id: str) -> dict[str, str]:
    out: dict[str, str] = {}
    cache_dir = document_cache_dir(doc_id)
    for ext in DOWNLOAD_EXTENSIONS:
        suffix = ext.replace(".", "_")
        path = cache_dir / f"{doc_id}.{ext}"
        if path.exists():
            out[suffix] = path.relative_to(ROOT).as_posix()
    return out


def manifest_entry_for(doc: SourceDocument) -> dict[str, Any]:
    return {
        "id": doc.id,
        "kind": doc.kind,
        "year": doc.year,
        "term": doc.term,
        "booklet": doc.booklet,
        "sourcePdf": doc.relative_path,
        "sourceSha256": sha256_file(doc.path),
        "sourcePages": pdf_page_count(doc.path),
    }


def mathpix_headers() -> dict[str, str]:
    app_id = os.environ.get("MATHPIX_APP_ID", "").strip()
    app_key = os.environ.get("MATHPIX_APP_KEY", "").strip()
    if not app_id or not app_key:
        raise RuntimeError("Set MATHPIX_APP_ID and MATHPIX_APP_KEY before calling the Mathpix API.")
    return {"app_id": app_id, "app_key": app_key}


def selected_ids(raw_ids: Iterable[str] | None) -> set[str] | None:
    if not raw_ids:
        return None
    return {item.strip() for item in raw_ids if item.strip()}
