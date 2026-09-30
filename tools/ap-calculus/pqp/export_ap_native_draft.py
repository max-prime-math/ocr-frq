#!/usr/bin/env python3
"""Integrate compiled editable OCR prompts into a new, independent AP draft.

Never overwrites the image-draft or a user-connected local folder. This exporter
requires every non-reviewed question to have a native candidate: missing/failed
candidates are errors, not permission to silently fall back to source screenshots.
"""
from __future__ import annotations

import argparse
import base64
import copy
import json
import re
import shutil
import zipfile
from datetime import datetime, timezone
from pathlib import Path

from ap_calculus_curriculum import course_classes, load_part_topics, organize
from export_ap_draft import ROOT, IMAGE_RE, PACKAGE_NAME, image_asset, sha256, write_json

DEFAULT_BASE = ROOT / "data/ap-calculus/draft/product"
DEFAULT_CANDIDATES = ROOT / "data/ap-calculus/native-pass/candidates"
DEFAULT_OUTPUT = ROOT / "data/ap-calculus/native-pass/product"


def image_names(body: str) -> set[str]:
    return set(IMAGE_RE.findall(body))


def native_text(body: str) -> str:
    # Only a guard against the old image-only fallback, not a quality review.
    return re.sub(r'#image\([^\n]*\)', '', body).strip()


def default_placements() -> dict:
    return {qid: organize(qid, parts) for qid, parts in load_part_topics().items()}


def build(base: Path, candidates_dir: Path, output: Path, records_dir: Path | None = None, placements: dict | None = None) -> dict:
    if output.resolve() == base.resolve() or output.resolve() == DEFAULT_BASE.resolve():
        raise ValueError("Refusing to overwrite the image-draft product")
    if (output / "manifest.json").exists():
        raise ValueError("Refusing to overwrite a connected local-folder bank")
    records_dir = records_dir or candidates_dir.parent / "intermediate" / "records"
    package = json.loads((base / PACKAGE_NAME).read_text())
    bank = json.loads((base / "testgen-question-bank.json").read_text())
    old_report = json.loads((base / "build-report.json").read_text())
    old_repairs = json.loads((base / "repair-queue.json").read_text())
    reviewed_ids = {q["id"] for q in old_report["questions"] if q["status"] == "preserved-published"}
    bank_ids = {q["id"] for q in bank["questions"]}
    pqp_by_id = {q["id"]: q for q in package["questions"]}
    if len(bank_ids) != len(bank["questions"]) or bank_ids != set(pqp_by_id):
        raise ValueError("Base package question IDs disagree or repeat")
    old_queue = {q["id"]: q for q in old_repairs["questions"]}
    prepared = {}
    errors = []
    for qid in sorted(bank_ids - reviewed_ids):
        path = candidates_dir / f"{qid}.json"
        if not path.exists():
            errors.append(f"{qid}: missing candidate")
            continue
        candidate = json.loads(path.read_text())
        source_record = records_dir / f"{qid}.json"
        if not source_record.is_file():
            errors.append(f"{qid}: missing canonical source record")
        elif candidate.get("sourceRecordSha256") != sha256(source_record):
            errors.append(f"{qid}: missing or stale source-record hash; regenerate candidate")
        body = candidate.get("bodyTypst", "").strip()
        if candidate.get("id") != qid or candidate.get("quality") != "native-draft":
            errors.append(f"{qid}: incorrect identity/quality")
        if candidate.get("compile", {}).get("body") is not True:
            errors.append(f"{qid}: native candidate has not compiled")
        if not native_text(body) or len(re.findall(r"[A-Za-z]{2,}", native_text(body))) < 8:
            errors.append(f"{qid}: missing substantive editable prompt text")
        if re.search(r"\b(?:prompt|question|ocr|transcription)\s+(?:is\s+)?(?:pending|unavailable|placeholder)|\bplaceholder\s+(?:prompt|question|text)\b", body, re.IGNORECASE):
            errors.append(f"{qid}: placeholder prompt cannot count as native OCR")
        supplied = {}
        for asset in candidate.get("assets", []):
            name = asset["name"]
            source = Path(asset["path"])
            if not source.is_absolute():
                source = ROOT / source
            if Path(name).name != name or not Path(name).suffix:
                errors.append(f"{qid}: unsafe or extensionless asset name {name}")
            elif not source.is_file():
                errors.append(f"{qid}: missing asset {source}")
            elif name in supplied:
                errors.append(f"{qid}: duplicate supplied asset name {name}")
            else:
                supplied[name] = source
        referenced = image_names(body)
        if referenced != set(supplied):
            errors.append(f"{qid}: referenced assets differ from supplied assets: {referenced ^ set(supplied)}")
        if any("-source-" in name for name in referenced):
            errors.append(f"{qid}: old full-prompt source crop cannot count as a native figure")
        prepared[qid] = {"body": body, "candidate": candidate, "path": path, "assets": supplied}
    if errors:
        raise ValueError(f"Native integration blocked ({len(errors)} errors):\n" + "\n".join(errors))

    generated = datetime.now(timezone.utc).isoformat()
    timestamp = int(datetime.now(timezone.utc).timestamp() * 1000)
    asset_sources = {}
    assets = {}
    rows = []
    repairs = []
    placements = default_placements() if placements is None else placements
    bank["customClasses"] = package["classes"] = course_classes()
    for question in bank["questions"]:
        qid = question["id"]
        portable = pqp_by_id[qid]
        # Workflow status lives in extensions and the repair queue, not tags.
        placement = placements[qid]
        question.update({key: placement[key] for key in ("classId", "unitId", "sectionId", "tags")})
        portable["classification"].update(placement)
        if qid in reviewed_ids:
            for name in question.get("images", []):
                source = base / "imgs" / name
                asset_sources[name] = source
                assets[name] = image_asset(name, source={"originalPath": str(source)})
            rows.append({"id": qid, "status": "preserved-published", "imageCount": len(question.get("images", []))})
            continue
        item = prepared[qid]
        candidate = item["candidate"]
        names = sorted(item["assets"])
        for name, source in item["assets"].items():
            if name in asset_sources and sha256(asset_sources[name]) != sha256(source):
                raise ValueError(f"Conflicting image bytes under same name: {name}")
            asset_sources[name] = source
            assets[name] = image_asset(name, source={"originalPath": str(source), "extensions": {"candidateId": qid}})
        question.update(body=item["body"], images=names, updatedAt=timestamp)
        portable["content"]["stem"]["text"] = item["body"]
        portable["assets"] = [Path(name).stem for name in names]
        portable["extensions"]["apCalculusDraft"].update(status="draft-native-ocr", solutionStatus="placeholder", pointsStatus="provisional", candidateSha256=sha256(item["path"]), candidatePath=str(item["path"]), issues=candidate.get("issues", []))
        portable["provenance"]["extensions"].update(ocrCandidateSource=candidate.get("source"), candidateSha256=sha256(item["path"]))
        # Old crop coordinates remain provenance, but no longer claim bundled files.
        portable["provenance"]["extensions"].pop("crops", None)
        row = {"id": qid, "status": "draft-native-ocr", "imageCount": len(names), "candidatePath": str(item["path"]), "candidateSha256": sha256(item["path"]), "issues": candidate.get("issues", [])}
        rows.append(row)
        repair = copy.deepcopy(old_queue[qid])
        repair.update(status="open", tasks=["ocr-content-review", "diagram-review", "classroom-solution", "points-review"], nativeCandidate=str(item["path"]), issues=candidate.get("issues", []))
        repairs.append(repair)
    if len({Path(name).stem for name in assets}) != len(assets):
        raise ValueError("Image filenames collide after TestGen removes file extensions")
    output.mkdir(parents=True, exist_ok=True)
    (output / "imgs").mkdir(exist_ok=True)
    for name, source in asset_sources.items():
        shutil.copy2(source, output / "imgs" / name)
    package["assets"] = [assets[name] for name in sorted(assets)]
    package["producer"].update(appVersion="ap-calculus-native-draft-1", exportedAt=generated)
    package["source"]["label"] = "AP Calculus AB/BC available local exams — editable OCR first draft"
    package["extensions"]["apCalculusDraft"].update(quality="native-ocr-first-draft", notes=["Reviewed records preserved. Every other prompt uses editable OCR text and figure assets, not a full-prompt screenshot fallback.", "Native OCR compilation does not establish mathematical correctness or diagram completeness.", "Unreviewed solutions remain explicit placeholders; unreviewed points remain provisional."])
    bank["exportedAt"] = generated
    bank["images"] = []
    for name in sorted(assets):
        image_path = output / "imgs" / name
        data = image_path.read_bytes()
        bank["images"].append({"name": image_path.stem, "ext": image_path.suffix[1:], "mime": assets[name]["mimeType"], "size": len(data), "data": base64.b64encode(data).decode("ascii")})
    report = {"schemaVersion": 1, "generatedAt": generated, "baseProduct": str(base), "baseImportSha256": sha256(base / "testgen-question-bank.json"), "inventory": old_report["inventory"], "inventorySha256": old_report["inventorySha256"], "questionCount": len(rows), "preservedPublishedCount": len(reviewed_ids), "nativeDraftCount": len(prepared), "draftCount": len(repairs), "sourceImageFallbackCount": 0, "assetCount": len(assets), "pqp": PACKAGE_NAME, "testgenImport": "testgen-question-bank.json", "questions": rows}
    write_json(output / PACKAGE_NAME, package)
    write_json(output / "testgen-question-bank.json", bank)
    write_json(output / "build-report.json", report)
    write_json(output / "repair-queue.json", {"schemaVersion": 1, "generatedAt": generated, "questions": repairs})
    markdown = ["# AP Calculus native draft — remaining review", "", f"{len(prepared)} editable OCR prompts are integrated; {len(reviewed_ids)} reviewed records are preserved. No full-prompt image fallback is counted as native. Compilation is not mathematical review. All unreviewed solutions remain placeholders.", "", "| Question | Remaining tasks | Candidate issues |", "| --- | --- | --- |"]
    for repair in repairs:
        issue_text = json.dumps(repair["issues"], ensure_ascii=False).replace("|", "\\|").replace("\n", " ")
        markdown.append(f"| {repair['id']} | {', '.join(repair['tasks'])} | {issue_text} |")
    (output / "REPAIR_QUEUE.md").write_text("\n".join(markdown) + "\n")
    (output / "README.md").write_text(f"""# AP Calculus editable OCR first draft

{len(rows)} questions: {len(reviewed_ids)} reviewed records preserved and {len(prepared)} compiled native OCR drafts. Figures remain images where needed. There are no image-only prompt fallbacks. OCR correctness, diagram completeness, solutions and point totals still need the recorded second pass.

## TestGen import

Use Import PQP / JSON with `testgen-question-bank.json` for one-file import including images. This JSON's bank-format version 2 is distinct from local-folder manifest schema 1. Stable IDs match the older image draft; importing into an existing bank may skip existing IDs. Use a new bank to inspect this independent native draft without changing user edits.

For Local Folder, use the separately generated `data/ap-calculus/ap-calculus-frq-bank` folder with manifest schema 1, compatible with the older deployed TestGen loader. Never select this `product` directory as a Local Folder bank. No local server is required.

The PQP ZIP is an archive for transport, not a direct ZIP importer. Its external `imgs/` assets require upload if using PQP JSON instead of the embedded bank JSON.

## Organization

One bank, two classes: Calculus AB (Units 1-8) and Calculus BC (Units 1-10), with CED unit and section names. Each question's section is the highest-numbered CED topic among its lettered parts, from the reviewed per-part topics in `tools/ap-calculus/pqp/ap_calculus_frq_topics.json`. Tags are the exam year, `Form B` where applicable, `Part A`/`Part B`, and `Calculator Active`/`No Calculator`. Draft status is recorded in PQP extensions and the repair queue, not in tags.

## Reproducibility and review

`build-report.json` records candidate hashes and counts. `repair-queue.json` and `REPAIR_QUEUE.md` track the remaining review. `validation/validation-report.json`, when present, records actual TestGen parser/render results. All placeholder solutions and provisional points remain labeled; generated native text is not presented as reviewed mathematics.

Rebuild in order: `build_native_source_records.py`, `build_native_typst_candidates.py`, then `export_ap_native_draft.py` (all in `tools/ap-calculus/pqp/`). Revalidate using `validate_ap_draft.mjs --product data/ap-calculus/native-pass/product --inventory data/ap-calculus/draft/source-inventory.json --reviewed-bank DIR`, where DIR holds the 24 reviewed records (ap-calculus-exam-banks at commit 8f70b42). Generate a new local-folder snapshot using `export_ap_local_folder.mjs --input data/ap-calculus/native-pass/product/testgen-question-bank.json --output NEW_FOLDER`; that exporter refuses to overwrite an existing folder.
""")
    members = [PACKAGE_NAME, "README.md", "build-report.json", "repair-queue.json", "REPAIR_QUEUE.md"] + [f"imgs/{name}" for name in sorted(assets)]
    with zipfile.ZipFile(output / "ap-calculus-native-draft-pqp.zip", "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for member in members:
            archive.write(output / member, member)
    return {key: value for key, value in report.items() if key != "questions"}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", type=Path, default=DEFAULT_BASE)
    parser.add_argument("--candidates", type=Path, default=DEFAULT_CANDIDATES)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--records", type=Path, help="Canonical source records; defaults to CANDIDATES/../intermediate/records")
    args = parser.parse_args()
    print(json.dumps(build(args.base, args.candidates, args.output, args.records), indent=2))


if __name__ == "__main__":
    main()
