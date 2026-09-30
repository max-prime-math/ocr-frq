#!/usr/bin/env python3
"""Independent source-vs-native completeness triage (not mathematical approval).

Compares visible source words inside canonical PDF crops to native candidate text,
checks required subpart labels, diagram refs, and known placeholder leakage. It
deliberately reports uncertain word mismatches for inspection, not silent repair.
"""
import argparse
import json
import re
from pathlib import Path
from datetime import datetime, timezone

import fitz

ROOT = Path(__file__).resolve().parents[3]
STOP = set("calculus college collegeboard board copyright rights reserved visit central apcentral collegeboardorg questions question response responses booklet separate designated pages page provided write work solution solutions instructions graphing calculator required section total points percent score examination problems minutes hours show remember general exam time part next temperature".split())
# 'temperature' is not ignored below: substantive prompt nouns must be checked.
STOP.discard("temperature")
STOP.update("allowed these grade setups described number parts".split())


def read(path):
    return json.loads(path.read_text())


def words(text):
    text = text.replace("’", "'").replace("−", "-")
    text = re.sub(r"-\s*\n\s*", "", text)
    return {w.lower() for w in re.findall(r"[A-Za-z]{5,}", text)} - STOP


def visible_text(page, rect):
    # PDF get_text() substitutes accessibility ActualText (e.g. "open
    # parenthesis") for equations. Texttrace follows actual displayed glyphs.
    strings = []
    for span in page.get_texttrace():
        if span["type"] == 3 or span.get("opacity", 1) == 0:
            continue
        chars = []
        previous = None
        for code, glyph, origin, box in span["chars"]:
            box = fitz.Rect(box)
            if rect.contains(fitz.Point((box.x0 + box.x1)/2, (box.y0 + box.y1)/2)):
                # Older PDFs position words without literal space glyphs.
                if previous is not None:
                    if abs(box.y0-previous.y0) > span["size"]*.6:
                        chars.append("\n")
                    elif box.x0-previous.x1 > span["size"]*.12:
                        chars.append(" ")
                chars.append(chr(code))
                previous = box
        strings.append("".join(chars))
    return "\n".join(strings)


def main():
    fitz.TOOLS.mupdf_display_errors(False)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--candidates", type=Path, default=ROOT / "data/ap-calculus/native-pass/candidates")
    parser.add_argument("--source-records", action="store_true", help="Audit raw canonical text before conversion")
    args = parser.parse_args()
    if args.source_records:
        args.candidates = ROOT / "data/ap-calculus/native-pass/intermediate/records"
    inventory = read(ROOT / "data/ap-calculus/draft/source-inventory.json")["questions"]
    docs = {}
    rows = []
    try:
        for source in inventory:
            file = args.candidates / (source["id"] + ".json")
            row = {"id": source["id"], "candidatePresent": file.exists()}
            if not file.exists():
                rows.append(row)
                continue
            candidate = read(file)
            body = candidate.get("rawPrompt" if args.source_records else "bodyTypst", "")
            pdf_path = ROOT / source["source"]["prompt"]["path"]
            if pdf_path not in docs:
                docs[pdf_path] = fitz.open(pdf_path)
            source_text = "\n".join(visible_text(docs[pdf_path][c["page"] - 1], fitz.Rect(c["rect"])) for c in source["crops"])
            expected = words(source_text)
            actual = words(re.sub(r'#image\([^\n]*?\)', '', body))
            missing = sorted(w for w in expected if w not in actual and not any(a.startswith(w) or w.startswith(a) for a in actual if len(a) >= 6))
            normalized_body = body.replace("\\", "")
            missing_parts = [part for part in source["sourceSubparts"] if not re.search(r"\(" + part + r"\)", normalized_body)]
            refs = re.findall(r'#image\([^)]*?"([^"]+)"', body)
            placeholders = re.findall(r"source figure retained|source image|prompt pending|TODO|conversion failed|placeholder", body, flags=re.I)
            row.update(bodyCompiles=candidate.get("compile", {}).get("body", False),
                       sourceWordCount=len(expected), missingSourceWords=missing,
                       wordRetention=round(1-len(missing)/max(1, len(expected)), 4),
                       missingSubpartLabels=missing_parts, imageReferences=refs,
                       placeholderLeakage=placeholders, candidateIssues=candidate.get("issues", []),
                       needsInspection=bool(missing_parts or placeholders or (len(missing) >= 3 and len(missing)/max(1, len(expected)) > .08)))
            rows.append(row)
    finally:
        for doc in docs.values():
            doc.close()
    report = {"generatedAt": datetime.now(timezone.utc).isoformat(),
              "purpose": "Automated completeness triage only; source word matching and compilation are not mathematical/diagram approval.",
              "expected": len(rows), "present": sum(r["candidatePresent"] for r in rows),
              "needsInspection": sum(r.get("needsInspection", False) for r in rows),
              "placeholderLeakage": sum(bool(r.get("placeholderLeakage")) for r in rows), "questions": rows}
    out = ROOT / "data/ap-calculus/native-pass/audit"
    out.mkdir(parents=True, exist_ok=True)
    name = "raw-source-content-audit.json" if args.source_records else "source-content-audit.json"
    (out / name).write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k:v for k,v in report.items() if k != "questions"}, indent=2))


if __name__ == "__main__":
    main()
