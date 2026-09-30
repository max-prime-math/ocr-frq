#!/usr/bin/env python3
"""Apply the reviewed AP Calculus organization to already-built banks in place.

Class, unit, section and tags come from `ap_calculus_curriculum.organize`, which
reads the reviewed per-part topics in `ap_calculus_frq_topics.json`. The
exporters apply the same function, so this is only needed for existing output.
"""
from __future__ import annotations

import argparse
import json
import os
import zipfile
from collections import Counter
from pathlib import Path

from ap_calculus_curriculum import course_classes, load_part_topics, organize
from export_ap_draft import ROOT, PACKAGE_NAME, write_json

DEFAULT_PRODUCTS = [ROOT / "data/ap-calculus/native-pass/product"]
BANK_FIELDS = ("classId", "unitId", "sectionId", "tags")


def retag_question(question: dict, parts: dict) -> None:
    placement = organize(question["id"], parts[question["id"]])
    question.update({key: placement[key] for key in BANK_FIELDS})


def retag_product(product: Path, parts: dict) -> None:
    bank_path = product / "testgen-question-bank.json"
    bank = json.loads(bank_path.read_text())
    if {q["id"] for q in bank["questions"]} != set(parts):
        raise ValueError(f"{bank_path}: question IDs differ from the reviewed topic file")
    bank["customClasses"] = course_classes()
    for question in bank["questions"]:
        retag_question(question, parts)
    write_json(bank_path, bank)
    pqp_path = product / PACKAGE_NAME
    package = json.loads(pqp_path.read_text())
    package["classes"] = course_classes()
    for question in package["questions"]:
        question["classification"].update(organize(question["id"], parts[question["id"]]))
    write_json(pqp_path, package)
    for archive_path in product.glob("*.zip"):
        temporary = archive_path.with_suffix(".zip.tmp")
        with zipfile.ZipFile(archive_path) as source, zipfile.ZipFile(temporary, "w", zipfile.ZIP_DEFLATED) as target:
            for info in source.infolist():
                data = pqp_path.read_bytes() if info.filename == PACKAGE_NAME else source.read(info.filename)
                target.writestr(info, data)
        os.replace(temporary, archive_path)


def fnv1a32(data: bytes) -> str:
    value = 0x811C9DC5
    for byte in data:
        value ^= byte
        value = (value * 0x01000193) & 0xFFFFFFFF
    return f"fnv1a32:{value:08x}"


def refresh_manifest(folder: Path) -> None:
    path = folder / "manifest.json"
    manifest = json.loads(path.read_text())
    for row in manifest["files"]:
        data = (folder / row["path"]).read_bytes()
        row["size"] = len(data)
        row["hash"] = fnv1a32(data)
    write_json(path, manifest)


def retag_folder(folder: Path, parts: dict) -> None:
    paths = sorted(p for p in (folder / "questions").glob("*.json") if p.name != "index.json")
    if {json.loads(path.read_text())["question"]["id"] for path in paths} != set(parts):
        raise ValueError(f"{folder}: question IDs differ from the reviewed topic file")
    write_json(folder / "curriculum/custom-classes.json", {"classes": course_classes(), "version": 1})
    for path in paths:
        wrapper = json.loads(path.read_text())
        retag_question(wrapper["question"], parts)
        write_json(path, wrapper)
    refresh_manifest(folder)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--product", type=Path, action="append", help="Product directory (repeatable)")
    parser.add_argument("--folder", type=Path, action="append", default=[], help="Local-folder bank (repeatable)")
    args = parser.parse_args()
    parts = load_part_topics()
    for product in args.product or DEFAULT_PRODUCTS:
        retag_product(product, parts)
    for folder in args.folder:
        retag_folder(folder, parts)
    counts = Counter(organize(qid, value)["unitName"] for qid, value in parts.items())
    print(json.dumps({"questions": len(parts), "unitCounts": dict(sorted(counts.items()))}, indent=2))


if __name__ == "__main__":
    main()
