#!/usr/bin/env python3
"""Build the complete AP draft as PQP and a one-file TestGen bank import.

Source inventory crops use PDF points and 1-based pages. Published bank records
are preserved; every other question uses source images and an explicit pending
solution. This local, resumable exporter performs no OCR requests or publication.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import re
import shutil
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import fitz

from ap_calculus_curriculum import course_classes, load_part_topics, organize

ROOT = Path(__file__).resolve().parents[3]
DEFAULT_INVENTORY = ROOT / "data/ap-calculus/draft/source-inventory.json"
DEFAULT_OUTPUT = ROOT / "data/ap-calculus/draft/product"
DEFAULT_REVIEWED = Path("/home/max/dev/ap-calculus-exam-banks")
PACKAGE_NAME = "ap-calculus-all-available-draft.pqp.json"
IMAGE_RE = re.compile(r'#image\(\s*"(?:/imgs/)?([^"/]+)"')


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    temporary.replace(path)


def published_questions(bank: Path) -> dict[str, dict]:
    records = {}
    for path in sorted((bank / "questions").glob("*.json")):
        record = json.loads(path.read_text(encoding="utf-8")).get("question")
        if record and record.get("id"):
            records[record["id"]] = record
    return records


def image_asset(filename: str, *, source: dict | None = None) -> dict:
    suffix = Path(filename).suffix.lower()
    mime = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".svg": "image/svg+xml"}[suffix]
    return {"id": Path(filename).stem, "kind": "image", "filename": filename,
            "mimeType": mime, "storage": {"mode": "external", "path": f"imgs/{filename}"},
            "source": source or {}}


def build(inventory_path: Path, output: Path, reviewed_bank: Path, zoom: float) -> dict:
    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    rows = inventory["questions"]
    if not rows:
        raise ValueError("Source inventory contains no questions")
    ids = [row["id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("Source inventory contains duplicate question IDs")
    if any(not re.fullmatch(r"[a-z0-9-]+", qid) for qid in ids):
        raise ValueError("Question IDs must be safe lowercase filename stems")
    reviewed = published_questions(reviewed_bank)
    part_topics = load_part_topics()
    generated = inventory.get("generatedAt") or datetime.now(timezone.utc).isoformat()
    timestamp = int(datetime.fromisoformat(generated.replace("Z", "+00:00")).timestamp() * 1000)
    output.mkdir(parents=True, exist_ok=True)
    (output / "imgs").mkdir(exist_ok=True)
    cache_path = output / "crop-cache.json"
    cache = json.loads(cache_path.read_text()) if cache_path.exists() else {}
    docs: dict[Path, fitz.Document] = {}
    hashes: dict[Path, str] = {}
    assets: dict[str, dict] = {}
    questions = []
    stored_questions = []
    report_rows = []
    repairs = []
    classes = course_classes()
    try:
        for row in sorted(rows, key=lambda item: (str(item["course"]), int(item["year"]), str(item.get("form", "")), int(item["question"]))):
            qid = row["id"]
            course = str(row["course"]).lower()
            source = row["source"]["prompt"]
            source_path = Path(source["path"])
            if not source_path.is_absolute():
                source_path = ROOT / source_path
            if source_path not in hashes:
                hashes[source_path] = sha256(source_path)
            if source.get("sha256") and source["sha256"] != hashes[source_path]:
                raise ValueError(f"Source hash mismatch: {qid}")
            source_ref = {**source, "sha256": hashes[source_path], "pages": row["source"].get("promptPages", source.get("pages", []))}
            image_names = []
            published = reviewed.get(qid)
            crop_details = []
            compatibility_notes = []
            if published:
                body = published["body"]
                solution = published.get("solution", "")
                if qid == "ap-calc-bc-1999-frq-03" and body.startswith("#table(\n"):
                    # TestGen inserts markup line breaks into single-newline
                    # paragraphs, including code. Keep this existing table on
                    # one line; no wording, cell, mathematics or points change.
                    table, rest = body.split("\n\n", 1)
                    body = " ".join(line.strip() for line in table.splitlines()) + "\n\n" + rest
                    compatibility_notes.append("Flattened table-code whitespace for TestGen paragraph renderer; original bank unchanged")
                if not body or not solution:
                    raise ValueError(f"Published record missing body/solution: {qid}")
                names = list(published.get("images", []))
                names += IMAGE_RE.findall(body + "\n" + solution)
                for name in dict.fromkeys(names):
                    filename = Path(name).name
                    if not Path(filename).suffix:
                        candidates = list((reviewed_bank / "images").glob(filename + ".*"))
                        if len(candidates) != 1:
                            raise ValueError(f"Cannot resolve published image {name}")
                        filename = candidates[0].name
                    original = reviewed_bank / "images" / filename
                    if not original.is_file():
                        raise ValueError(f"Missing published image: {original}")
                    shutil.copy2(original, output / "imgs" / filename)
                    assets[filename] = image_asset(filename, source={"originalPath": str(original)})
                    image_names.append(filename)
                status = "preserved-published"
                points = published.get("points", 9)
                stored = dict(published)
            else:
                if not row.get("crops"):
                    raise ValueError(f"Draft question has no explicit source crop: {qid}")
                if source_path not in docs:
                    docs[source_path] = fitz.open(source_path)
                doc = docs[source_path]
                fragments = []
                for index, crop in enumerate(row["crops"], 1):
                    page_number = int(crop["page"])
                    if not 1 <= page_number <= len(doc):
                        raise ValueError(f"Invalid source page: {qid} page {page_number}")
                    page = doc[page_number - 1]
                    rect = fitz.Rect(crop["rect"])
                    if rect.is_empty or rect.is_infinite or not page.rect.contains(rect):
                        raise ValueError(f"Invalid crop rectangle: {qid} page {page_number}: {rect}")
                    filename = f"{qid}-source-{index:02d}.png"
                    target = output / "imgs" / filename
                    fingerprint = hashlib.sha256(json.dumps([hashes[source_path], page_number, list(rect), zoom]).encode()).hexdigest()
                    if cache.get(filename) != fingerprint or not target.is_file():
                        page.get_pixmap(matrix=fitz.Matrix(zoom, zoom), clip=rect, alpha=False).save(target)
                        cache[filename] = fingerprint
                    assets[filename] = image_asset(filename, source={"originalPath": f"{source_path.name}#page={page_number}", "extensions": {"sha256": hashes[source_path], "rect": list(rect)}})
                    image_names.append(filename)
                    # A bounded image remains usable within TestGen's numbered
                    # question grid. Contain preserves the complete crop.
                    height_mm = min(165.0, 165.0 * rect.height / rect.width)
                    fragments.append(f'#image("/imgs/{filename}", width: 100%, height: {height_mm:.2f}mm, fit: "contain")')
                    crop_details.append({"page": page_number, "rect": list(rect), "image": filename, "sha256": sha256(target)})
                body = "\n\n".join(fragments)
                solution = "Solution pending review. This first-draft question does not yet include a verified classroom solution."
                status = "draft-source-image"
                points = 9
                stored = {"createdAt": timestamp, "updatedAt": timestamp}
                repairs.append({"id": qid, "status": "open", "tasks": ["native-text", "classroom-solution", "points-review", "visual-review"], "source": source_ref, "scoringGuide": row["source"].get("scoringGuide"), "cropNotes": row.get("issues", [])})
            # Workflow status lives in extensions and the repair queue, not tags.
            classification = {"questionType": "frq", **organize(qid, part_topics[qid])}
            tags = classification["tags"]
            questions.append({"id": qid, "kind": "frq", "content": {"stem": {"format": "typst", "text": body}, "solution": {"format": "typst", "text": solution}}, "scoring": {"points": points}, "classification": classification, "assets": [Path(name).stem for name in image_names], "provenance": {"sourceApp": "ocr-frq", "sourceLabel": f"AP Calculus {course.upper()} {row['year']} {row.get('form', 'standard')}", "sourceQuestionNumber": str(row["question"]), "originFiles": [source_path.name], "extensions": {"stableSourceId": qid, "prompt": source_ref, "crops": crop_details}}, "extensions": {"apCalculusDraft": {"status": status, "solutionStatus": "preserved-published" if published else "placeholder", "pointsStatus": "preserved-published" if published else "provisional", "reviewedRecordPath": str(reviewed_bank / "questions" / f"{qid}.json") if published else None}}})
            stored.update({"id": qid, "body": body, "solution": solution, "questionType": "frq", "points": points, "tags": tags, "images": image_names, "classId": classification["classId"], "unitId": classification["unitId"], "sectionId": classification["sectionId"]})
            stored_questions.append(stored)
            report_rows.append({"id": qid, "status": status, "imageCount": len(image_names), "crops": crop_details, "compatibilityNotes": compatibility_notes})
    finally:
        for doc in docs.values():
            doc.close()
        write_json(cache_path, cache)
    asset_list = [assets[key] for key in sorted(assets)]
    package = {"format": "portable-question-package", "version": "1.0", "producer": {"app": "ocr-frq", "appVersion": "ap-calculus-draft-1", "exportedAt": generated}, "source": {"kind": "pdf", "label": "AP Calculus AB/BC available local exams — first draft", "publisher": "College Board", "collection": "AP Calculus AB/BC"}, "classes": classes, "questions": questions, "assets": asset_list, "diagnostics": [], "extensions": {"apCalculusDraft": {"inventorySha256": sha256(inventory_path), "quality": "first-draft", "notes": ["Published content is preserved; other bodies are source PDF crops.", "Draft solutions are explicit placeholders. Draft point totals are provisional.", "AB and BC release-specific question IDs remain separate even where prompts are shared."]}}}
    write_json(output / PACKAGE_NAME, package)
    embedded_images = []
    for asset in asset_list:
        path = output / asset["storage"]["path"]
        data = path.read_bytes()
        embedded_images.append({"name": path.stem, "ext": path.suffix[1:], "mime": asset["mimeType"], "size": len(data), "data": base64.b64encode(data).decode("ascii")})
    native = {"format": "test-generator-question-bank", "version": 2, "exportedAt": generated, "questions": stored_questions, "narratives": [], "customClasses": classes, "images": embedded_images}
    write_json(output / "testgen-question-bank.json", native)
    report = {"schemaVersion": 1, "generatedAt": generated, "inventory": str(inventory_path), "inventorySha256": sha256(inventory_path), "questionCount": len(questions), "preservedPublishedCount": sum(row["status"] == "preserved-published" for row in report_rows), "draftCount": len(repairs), "assetCount": len(assets), "sourcePdfCount": len(hashes), "pqp": PACKAGE_NAME, "testgenImport": "testgen-question-bank.json", "questions": report_rows}
    write_json(output / "build-report.json", report)
    write_json(output / "repair-queue.json", {"schemaVersion": 1, "generatedAt": generated, "questions": repairs})
    queue_markdown = ["# AP Calculus draft repair queue", "", f"{len(repairs)} draft questions need a second pass. The machine-readable source is `repair-queue.json`.", "", "For every open row: verify source crop visually, replace source images with complete native Typst when practical, write a verified classroom solution, and confirm points. Update the inventory/repair overrides and rerun exporter/validator; do not edit generated product JSON by hand.", "", "| Question ID | Status | Remaining tasks |", "| --- | --- | --- |"]
    queue_markdown.extend(f"| {item['id']} | {item['status']} | {', '.join(item['tasks'])} |" for item in repairs)
    (output / "REPAIR_QUEUE.md").write_text("\n".join(queue_markdown) + "\n", encoding="utf-8")
    readme = f"""# AP Calculus AB/BC first draft for TestGen

Contains {len(questions)} release-specific questions: {report['preservedPublishedCount']} preserved published records and {len(repairs)} drafts. Scope is all prompt PDFs in the accompanying source inventory, including prompt-only releases; this is not a claim to cover exams absent from the local collection.

## Recommended import: one JSON file

In TestGen's question bank, use **Import JSON** and select `testgen-question-bank.json`. This native bank import includes every image and preserves stable question IDs. It uses the app's existing `test-generator-question-bank` version 2 format. Import once; future imports with the same IDs may be treated as already present.

## Portable PQP alternative

Extract `ap-calculus-draft-pqp.zip`. Upload all files in `imgs/` through TestGen's bank image manager, then import `{PACKAGE_NAME}` and save the imported drafts. PQP import creates new TestGen IDs; the original stable IDs remain in PQP provenance (`stableSourceId`). The ZIP is a transport bundle, not a directly supported TestGen ZIP importer.

## First-draft limitations and second pass

Draft prompts are readable source PDF crops that preserve diagrams, tables, and notation. Their solutions explicitly say they are pending review, and their nine-point totals are provisional. Published content and images are preserved; BC 1999 Q3 has table-code whitespace flattened for TestGen compatibility, with no content change. Native text, solutions, classification, points, and visual checks are tracked by stable question ID in `repair-queue.json` and `REPAIR_QUEUE.md`. Questions shared between AB/BC exams are retained as separate exam-source records.

`build-report.json` describes package coverage and source image hashes. Consult `validation/validation-report.json`, when present, for independent import/render checks. Building a file alone does not assert visual or mathematical review.
"""
    (output / "README.md").write_text(readme, encoding="utf-8")
    members = [PACKAGE_NAME, "README.md", "build-report.json", "repair-queue.json", "REPAIR_QUEUE.md"] + [asset["storage"]["path"] for asset in asset_list]
    with zipfile.ZipFile(output / "ap-calculus-draft-pqp.zip", "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for relative in members:
            archive.write(output / relative, relative)
        archive.write(inventory_path, "source-inventory.json")
    return {key: value for key, value in report.items() if key != "questions"}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inventory", type=Path, default=DEFAULT_INVENTORY)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--reviewed-bank", type=Path, default=DEFAULT_REVIEWED)
    parser.add_argument("--zoom", type=float, default=2.0)
    args = parser.parse_args()
    if not 1 <= args.zoom <= 4:
        parser.error("zoom must be between 1 and 4")
    print(json.dumps(build(args.inventory, args.output, args.reviewed_bank, args.zoom), indent=2))


if __name__ == "__main__":
    main()
