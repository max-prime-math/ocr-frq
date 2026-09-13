#!/usr/bin/env python3
"""Create compile-checked, blocked Typst candidates for an AP FRQ tranche."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
DEFAULT_INTERMEDIATE = ROOT / "data" / "ap-calculus" / "tranches" / "tranche-01" / "staging" / "intermediate"
DEFAULT_OUT = ROOT / "data" / "ap-calculus" / "tranches" / "tranche-01" / "staging" / "typst-candidates"

sys.path.insert(0, str(ROOT / "tools" / "manitoba-precalc-40s" / "pqp"))
from manitoba_typst_conversion import convert_many  # noqa: E402


def prepare_latex(raw: str) -> str:
    raw = raw.replace(r"\(", "$").replace(r"\)", "$").replace(r"\[", "$$").replace(r"\]", "$$")
    raw = raw.replace(r"\langle-1\rangle", "(minus 1)")
    # Page-limited guides sometimes OCR a coordinate vector as `<a,b>`. This
    # is not Typst math syntax, unlike a rubric deduction such as `<-1>`.
    raw = re.sub(r"<([^<>]*,[^<>]*)>", r"(\1)", raw)
    raw = re.sub(r"\\begin\{figure\}.*?\\end\{figure\}", "\n[Source figure retained for review.]\n", raw, flags=re.S)
    raw = re.sub(r"!\[\]\(https://cdn\.mathpix\.com/cropped/[^)]*\)", "\n[Source figure retained for review.]\n", raw)
    raw = re.sub(r"\\includegraphics(?:\[[^]]*\])?\{[^}]+\}", "\n[Source figure retained for review.]\n", raw)
    return raw.replace(r"\begin{center}", "").replace(r"\end{center}", "")


def convert_and_compile(identifier: str, field: str, raw: str) -> tuple[str, str | None]:
    if not raw.strip():
        return "", "No source-scoped scoring-guide OCR is available; retained legacy guide text is deliberately blocked."
    try:
        converted = convert_many([prepare_latex(raw)])[0]
    except RuntimeError as error:
        return "", str(error)
    with tempfile.TemporaryDirectory(prefix="ap-calc-tranche-typst-") as directory:
        source = Path(directory) / f"{identifier}-{field}.typ"
        output = source.with_suffix(".pdf")
        source.write_text(converted, encoding="utf-8")
        result = subprocess.run(["typst", "compile", str(source), str(output)], text=True, capture_output=True)
    return converted, None if result.returncode == 0 else (result.stderr or result.stdout).strip()[-2000:]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--intermediate", type=Path, default=DEFAULT_INTERMEDIATE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--replace", action="store_true", help="Replace this generated candidate directory")
    args = parser.parse_args()
    records = sorted((args.intermediate / "records").glob("*.json"))
    if len(records) != 12:
        raise SystemExit("Expected 12 intermediate records")
    if args.output.exists():
        if not args.replace:
            raise SystemExit(f"Refusing to replace existing output: {args.output}; pass --replace")
        shutil.rmtree(args.output)
    args.output.mkdir(parents=True)
    summary = []
    for path in records:
        record = json.loads(path.read_text(encoding="utf-8"))
        body, body_error = convert_and_compile(record["id"], "body", record["rawPrompt"])
        scoring, scoring_error = convert_and_compile(record["id"], "scoring", record["rawScoringGuide"])
        candidate = {"schemaVersion": 1, "id": record["id"], "course": record["course"], "year": record["year"], "form": record["form"], "question": record["question"], "source": record["source"], "focus": record["focus"], "assets": record["assets"], "bodyTypst": body, "scoringGuideTypst": scoring, "compile": {"body": body_error is None, "scoringGuide": scoring_error is None, "errors": {"body": body_error, "scoringGuide": scoring_error}}, "solutionExtractionStatus": record["solutionExtractionStatus"], "reviewState": "unreviewed", "publishState": "blocked"}
        (args.output / path.name).write_text(json.dumps(candidate, indent=2) + "\n", encoding="utf-8")
        summary.append({"id": record["id"], "bodyCompiles": body_error is None, "scoringCompiles": scoring_error is None})
    (args.output / "index.json").write_text(json.dumps({"schemaVersion": 1, "candidates": summary}, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"candidates": len(summary), "bodyCompilePassed": sum(row["bodyCompiles"] for row in summary), "scoringCompilePassed": sum(row["scoringCompiles"] for row in summary), "publishState": "blocked"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
