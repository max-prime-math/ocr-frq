#!/usr/bin/env python3
"""Canonical saved-OCR source records, without new API work or old-stage mutation.

Prefer line metadata spatially selected against the independently verified PDF
inventory, not cache filenames (several historical filenames name wrong pages).
Retained BC TeX ZIPs are the alternative; scoring-guide repeated statements
recover five AB prompts whose original prompt OCR cache labels were incorrect.
"""
from __future__ import annotations

import collections
import hashlib
import json
import re
import sys
import tempfile
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "data/ap-calculus/native-pass/intermediate"
sys.path.insert(0, str(ROOT))
from src.mathpix import parse_exam_zip  # noqa: E402

BOILERPLATE = re.compile(r"CALCULUS (?:AB|BC)|FREE.RESPONSE QUESTIONS|SECTION II|Time\s*[-–]|Number of (?:problems|questions)|Percent of total|calculator is|calculator.*required|REMEMBER TO SHOW|WRITE ALL WORK|END OF (?:PART|EXAM|SECTION)|STOP\b|Copyright|All rights reserved|collegeboard\.(?:com|org)|^GO ON TO|^CONTINUE|^Page \d|^A GRAPHING CALCULATOR|^FOR SOME PROBLEMS|^section of the examination", re.I)
IMAGE = re.compile(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}|!\[[^\]]*\]\(([^)]+)\)")

# Source-page visual audit, 2026-09-14: six legacy TeX figures were left at the
# end of the preceding question by the old parser. Explicit bounded corrections
# avoid inferring figure ownership from a generic "above"/"below" heuristic.
MISASSIGNED_FIGURES = {
    "ap-calc-bc-2009-form-b-frq-02": (1, "ap-calc-bc-2009-form-b-frq-03", 4, [170, 68, 442, 197]),
    "ap-calc-bc-2009-form-b-frq-04": (2, "ap-calc-bc-2009-form-b-frq-05", 6, [208, 68, 407, 201]),
    "ap-calc-bc-2011-form-b-frq-03": (2, "ap-calc-bc-2011-form-b-frq-04", 4, [211, 68, 401, 257]),
    "ap-calc-bc-2011-frq-03": (2, "ap-calc-bc-2011-frq-04", 5, [179, 63, 433, 309]),
    "ap-calc-bc-2014-frq-02": (2, "ap-calc-bc-2014-frq-03", 4, [207, 166, 404, 346]),
    "ap-calc-bc-2019-frq-05": (1, "ap-calc-bc-2019-frq-06", 7, [143, 94, 341, 322]),
}


# Source-page review, 2026-09-30: OCR text that is wrong against the printed
# exam. Each replacement must match exactly once, so a changed OCR input fails
# loudly instead of silently skipping the correction.
SOURCE_CORRECTIONS = {
    # Mathpix dropped requirement (ii); text from the source PDF (page 4).
    "ap-calc-ab-2006-form-b-frq-03": [(
        "slope of the graph of the function is 0.\n(iii)",
        "slope of the graph of the function is 0.\n(ii) At \\(x=4\\), the value of the function is 1 , and the slope of the graph of the function is 1.\n(iii)",
    )],
    # The released PDF's symbol font prints the triangle as "n" (page 7).
    "ap-calc-ab-1999-frq-06": [(r"\(\mathrm{n} P Q R\)", r"\(\triangle P Q R\)")],
    # The P(t) table printed above question 3 was attached to question 2.
    "ap-calc-bc-2010-form-b-frq-02": [(
        "\n\n\\begin{center}\n\\begin{tabular}{|c||c|c|c|c|c|c|c|}\n\\hline\n$t$ & 0 & 2 & 4 & 6 & 8 & 10 & 12 \\\\\n\\hline\n$P(t)$ & 0 & 46 & 53 & 57 & 60 & 62 & 63 \\\\\n\\hline\n\\end{tabular}\n\\end{center}",
        "",
    )],
}


def apply_source_corrections(qid, raw):
    applied = []
    for old, new in SOURCE_CORRECTIONS.get(qid, []):
        if raw.count(old) != 1:
            raise ValueError(f"{qid}: source correction no longer matches exactly once: {old[:60]!r}")
        raw = raw.replace(old, new)
        applied.append({"type": "reviewed-source-text-correction", "replaced": old, "with": new})
    return raw, applied


def read(path):
    return json.loads(Path(path).read_text())


def rel(path):
    return str(Path(path).relative_to(ROOT))


def write(path, data):
    Path(path).write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def clean(text):
    # Remove only document/list wrappers and recognizable exam instructions.
    text = re.sub(r"\\(?:begin|end)\{(?:itemize|enumerate|document)\}", "", text)
    text = re.sub(r"\\item\[\(([a-z])\)\]", r"(\1)", text)
    text = re.sub(r"\\item\[[1-6]\.\]", "", text)
    text = re.sub(r"\\setcounter\{enumi\}\{\d+\}", "", text)
    text = "\n".join(line for line in text.splitlines() if not BOILERPLATE.search(line))
    text = re.sub(r"\\section\*\{Question \d+\}", "", text)
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def source_lines(coverage):
    pages = collections.defaultdict(list)
    manifests = sorted({e["manifest"] for q in coverage for e in q["promptOcrEvidence"] if e["type"] == "cached-mmd"})
    for manifest in manifests:
        for entry in read(ROOT / manifest)["documents"].values():
            if entry.get("kind") != "prompt":
                continue
            linepath = entry.get("outputs", {}).get("lines.json")
            if not linepath or not (ROOT / linepath).is_file():
                continue
            for number, page in zip(entry.get("sourcePages", []), read(ROOT / linepath)["pages"]):
                pages[(entry["sourcePdf"], number)].append((page, entry, linepath))
    return pages


def render_asset(row, doc, page, rect, number):
    name = f"{row['id']}-diagram-{number:02d}.png"
    path = OUT / "assets" / name
    clip = fitz.Rect(rect) & doc[page - 1].rect
    doc[page - 1].get_pixmap(matrix=fitz.Matrix(2, 2), clip=clip, alpha=False).save(path)
    return {"name": name, "path": rel(path), "sourcePage": page, "sourceRect": list(clip), "origin": "original-pdf-diagram-region"}


def spatial_record(row, doc, pages):
    pieces, assets, evidence, selected = [], [], [], []
    for crop in row["crops"]:
        options = pages.get((row["source"]["prompt"]["path"], crop["page"]), [])
        if not options:
            return None
        # Highest text volume generally means the non-corrupt duplicate OCR.
        page, entry, linepath = max(options, key=lambda o: sum(len(l.get("text", "")) for l in o[0]["lines"] if l.get("conversion_output")))
        original = doc[crop["page"] - 1]
        sx, sy = original.rect.width / page["page_width"], original.rect.height / page["page_height"]
        region = fitz.Rect(crop["rect"])
        for line in page["lines"]:
            if not line.get("conversion_output"):
                continue
            r = line.get("region")
            if not r:
                continue
            rect = fitz.Rect(r["top_left_x"] * sx, r["top_left_y"] * sy, (r["top_left_x"] + r["width"]) * sx, (r["top_left_y"] + r["height"]) * sy)
            if not region.contains(fitz.Point((rect.x0 + rect.x1) / 2, (rect.y0 + rect.y1) / 2)):
                continue
            value = line.get("text", "")
            if BOILERPLATE.search(value):
                continue
            if line["type"] in {"chart", "diagram", "image"} or IMAGE.search(value):
                asset = render_asset(row, doc, crop["page"], rect + (-3, -3, 3, 3), len(assets) + 1)
                assets.append(asset)
                value = f"\\includegraphics{{{asset['name']}}}"
            elif not value.strip():
                continue
            value = re.sub(rf"^\s*{row['question']}\.\s+(?=[A-Za-z\\])", "", value)
            pieces.append(value)
            selected.append({"sourcePage": crop["page"], "line": line.get("line"), "type": line["type"], "rect": list(rect)})
        evidence.append({"type": "source-crop-filtered-mathpix-lines", "path": linepath, "cachedQuestionId": entry.get("questionId"), "sourcePage": crop["page"], "sourceSha256Matches": entry.get("sourceSha256") == row["source"]["prompt"]["sha256"]})
    return clean("\n".join(pieces)), assets, evidence, selected


def legacy_record(row, coverage_row, parsed):
    prior = next((read(ROOT / p) for p in coverage_row["intermediateRecords"] if read(ROOT / p).get("legacyMathpix")), None)
    if not prior:
        return None
    zippath = prior["legacyMathpix"]["promptZip"]["path"]
    if zippath not in parsed:
        # The parser's intermediate figure files stay in our new generated tree.
        figures = OUT / "legacy-figures" / Path(zippath).stem
        parsed[zippath] = (parse_exam_zip(str(ROOT / zippath), str(figures), row["year"], "B" if row["form"] != "standard" else ""), figures)
    blocks, figures = parsed[zippath]
    if row["question"] not in blocks:
        return None
    raw = blocks[row["question"]].question_text
    assets = []
    for match in list(IMAGE.finditer(raw)):
        ref = match.group(1) or match.group(2)
        old = figures / Path(ref).name
        if not old.is_file():
            continue
        name = f"{row['id']}-diagram-{len(assets) + 1:02d}{old.suffix}"
        path = OUT / "assets" / name
        path.write_bytes(old.read_bytes())
        assets.append({"name": name, "path": rel(path), "origin": "retained-mathpix-tex-zip", "originalReference": ref})
        raw = raw.replace(ref, name)
    return clean(raw), assets, [{"type": "retained-mathpix-tex-zip-resegmented", "path": zippath}], []


def scoring_statement(row, coverage_row):
    source = next(e for e in coverage_row["scoringOcrEvidence"] if e["type"] == "cached-mmd")
    raw = (ROOT / source["path"]).read_text()
    start = re.search(rf"\\section\*\{{Question {row['question']}\}}", raw)
    if start:
        raw = raw[start.end():]
    starts = list(re.finditer(r"\\item\[\(a\)\]|(?m:^\s*\(a\))", raw))
    if len(starts) < 2:
        raise ValueError(f"Cannot confidently segment scoring statement: {row['id']}")
    raw = raw[:starts[1].start()]
    raw = re.sub(r"\(Note: Use the axes provided in the pink test booklet\.\)", "", raw)
    return clean(raw), [], [{"type": "scoring-guide-repeated-prompt", "path": source["path"], "reason": "original-prompt-cache-source-pages-mislabeled"}], []


def restore_verified_source_diagrams(row, doc, data):
    """Recover a source-only figure absent from the guide's repeated statement.

    AB 2005 Q6 was visually checked against original PDF page 7. The guide's
    worked slope field cannot replace the exam's twelve unfilled slope points.
    The explicit region below includes the axes, labels, and all twelve points,
    but neither the question prose nor the worked solution.
    """
    raw, assets, evidence, selected = data
    if row["id"] in MISASSIGNED_FIGURES:
        number, proper_id, _, _ = MISASSIGNED_FIGURES[row["id"]]
        name = f"{row['id']}-diagram-{number:02d}.jpg"
        raw = re.sub(r"\\begin\{center\}\s*\\includegraphics(?:\[[^\]]*\])?\{" + re.escape(name) + r"\}\s*\\end\{center\}", "", raw).strip()
        assets = [a for a in assets if a["name"] != name]
        evidence.append({"type": "visually-verified-legacy-figure-boundary-correction", "removedFigure": name, "belongsToQuestion": proper_id})
    for previous_id, (_, proper_id, page, rect) in MISASSIGNED_FIGURES.items():
        if row["id"] != proper_id:
            continue
        asset = render_asset(row, doc, page, rect, len(assets) + 1)
        assets.append(asset)
        # Restore the source's directional wording now that the correct graph
        # is back before its prompt (the old parser changed these to "below").
        raw = raw.replace("shown in the figure below", "shown in the figure above").replace("is shown below", "is shown above")
        raw = f"\\includegraphics{{{asset['name']}}}\n\n" + raw
        evidence.append({"type": "visually-verified-original-pdf-diagram-recovery", "sourcePage": page, "sourceRect": asset["sourceRect"], "previouslyMisassignedTo": previous_id})
    if row["id"] == "ap-calc-ab-2005-frq-06" and not assets:
        asset = render_asset(row, doc, 7, [229, 138, 384, 343], 1)
        assets.append(asset)
        raw = raw.replace("\n(b)", f"\n\\includegraphics{{{asset['name']}}}\n\n(b)", 1)
        evidence.append({"type": "visually-verified-original-pdf-diagram-recovery", "sourcePage": 7, "sourceRect": asset["sourceRect"]})
    return raw, assets, evidence, selected


def main():
    rows = read(ROOT / "data/ap-calculus/draft/source-inventory.json")["questions"]
    coverage = read(ROOT / "data/ap-calculus/ocr-audit/coverage.json")["questions"]
    audit = {q["id"]: q for q in coverage}
    (OUT / "records").mkdir(parents=True, exist_ok=True)
    (OUT / "assets").mkdir(exist_ok=True)
    pages, parsed, docs, index = source_lines(coverage), {}, {}, []
    for row in rows:
        path = row["source"]["prompt"]["path"]
        doc = docs.setdefault(path, fitz.open(ROOT / path))
        data = spatial_record(row, doc, pages) or legacy_record(row, audit[row["id"]], parsed) or scoring_statement(row, audit[row["id"]])
        raw, assets, evidence, selected = restore_verified_source_diagrams(row, doc, data)
        raw, corrections = apply_source_corrections(row["id"], raw)
        evidence = evidence + corrections
        actual_parts = list(dict.fromkeys(re.findall(r"\(([a-d])\)", raw)))
        expected = row["sourceSubparts"]
        issues = []
        missing = [p for p in expected if p not in actual_parts]
        if missing:
            issues.append({"kind": "missing-source-subparts", "parts": missing})
        if any(e["type"] == "scoring-guide-repeated-prompt" for e in evidence):
            issues.append({"kind": "prompt-recovered-from-scoring-guide", "reviewRequired": True})
        unresolved = [m.group(1) or m.group(2) for m in IMAGE.finditer(raw) if (m.group(1) or m.group(2)) not in {a["name"] for a in assets}]
        if unresolved:
            issues.append({"kind": "unresolved-image-references", "references": unresolved})
        if len(raw) < 200:
            issues.append({"kind": "suspiciously-short-prompt", "characters": len(raw)})
        scoring_evidence = audit[row["id"]]["scoringOcrEvidence"]
        scoring_path = next((e["path"] for e in scoring_evidence if e["type"] == "cached-mmd"), None)
        scoring = (ROOT / scoring_path).read_text() if scoring_path else ""
        record = {"schemaVersion": 1, **{k: row[k] for k in ["id", "course", "year", "form", "question", "source"]}, "rawPrompt": raw, "assets": assets, "rawScoringGuide": scoring, "sourceChecks": {"expectedSubparts": expected, "detectedSubparts": actual_parts, "missingSubparts": missing, "sourceCrops": row["crops"], "selectedLines": selected, "allImageReferencesResolved": not unresolved, "mathematicalAccuracyReviewed": False}, "issues": issues, "ocrEvidence": evidence, "reviewState": "unreviewed-native-draft"}
        target = OUT / "records" / f"{row['id']}.json"
        write(target, record)
        index.append({"id": row["id"], "record": f"records/{target.name}", "characters": len(raw), "assetCount": len(assets), "issueCount": len(issues), "sourceMethod": evidence[0]["type"]})
    result = {"schemaVersion": 1, "questionCount": len(index), "assetCount": sum(q["assetCount"] for q in index), "sourceMethods": dict(collections.Counter(q["sourceMethod"] for q in index)), "questionsWithIssues": sum(q["issueCount"] > 0 for q in index), "records": index}
    write(OUT / "index.json", result)
    print(json.dumps({k: v for k, v in result.items() if k != "records"}, indent=2))


if __name__ == "__main__":
    main()
