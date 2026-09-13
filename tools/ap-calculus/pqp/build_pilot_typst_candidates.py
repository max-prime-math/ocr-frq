#!/usr/bin/env python3
"""Convert blocked AP pilot records to compile-checked Typst candidates.

This is intentionally a candidate stage, not a PQP exporter: AP scoring guides
must be separated into worked solutions and rubrics by review before a
question may be emitted to the TestGen working bank.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
INTERMEDIATE = ROOT / "data" / "ap-calculus" / "pilot" / "staging" / "intermediate"
OUT = ROOT / "data" / "ap-calculus" / "pilot" / "staging" / "typst-candidates"

sys.path.insert(0, str(ROOT / "tools" / "manitoba-precalc-40s" / "pqp"))
from manitoba_typst_conversion import convert_many  # noqa: E402


def prepare_latex(raw: str) -> str:
    # AP Mathpix Markdown uses LaTeX math delimiters. MiTeX expects dollar
    # delimiters, and an isolated question often starts inside the outer list.
    raw = raw.replace(r"\(", "$").replace(r"\)", "$")
    raw = raw.replace(r"\[", "$$").replace(r"\]", "$$")
    # AP rubrics use this as prose for a one-point deduction, not as a
    # mathematical angle. Keeping it as plain text avoids a malformed Typst
    # symbol modifier without changing its scoring meaning.
    raw = raw.replace(r"\langle-1\rangle", "(minus 1)")
    # MiTeX intentionally does not support LaTeX float/caption macros. Keep a
    # visible marker while the source crop remains in candidate metadata; a
    # reviewer later assigns it to the body or solution before publication.
    raw = re.sub(r"\\begin\{figure\}.*?\\end\{figure\}", "\n[Source figure retained for review.]\n", raw, flags=re.S)
    raw = re.sub(r"!\[\]\(https://cdn\.mathpix\.com/cropped/[^)]*\)", "\n[Source figure retained for review.]\n", raw)
    raw = re.sub(r"\\includegraphics(?:\[[^]]*\])?\{[^}]+\}", "\n[Source figure retained for review.]\n", raw)
    raw = raw.replace(r"\begin{center}", "").replace(r"\end{center}", "")
    if raw.lstrip().startswith(r"\item["):
        raw = r"\begin{itemize}" + raw
    return raw


def compile_typst(identifier: str, field: str, text: str) -> str | None:
    with tempfile.TemporaryDirectory(prefix="ap-calc-typst-") as directory:
        source = Path(directory) / f"{identifier}-{field}.typ"
        output = source.with_suffix(".pdf")
        source.write_text(text, encoding="utf-8")
        result = subprocess.run(["typst", "compile", str(source), str(output)], text=True, capture_output=True)
        return None if result.returncode == 0 else (result.stderr or result.stdout).strip()[-2000:]


def convert_field(raw: str) -> tuple[str, str | None]:
    try:
        return convert_many([prepare_latex(raw)])[0], None
    except RuntimeError as error:
        return "", str(error)


def main() -> int:
    records = sorted((INTERMEDIATE / "records").glob("*.json"))
    if len(records) != 12:
        raise SystemExit("Expected the 12 intermediate records; run build_pilot_intermediate.py first")
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    summary = []
    for path in records:
        record = json.loads(path.read_text(encoding="utf-8"))
        body, body_conversion_error = convert_field(record["rawPrompt"])
        scoring, scoring_conversion_error = convert_field(record["rawScoringGuide"])
        body_error = body_conversion_error or compile_typst(record["id"], "body", body)
        scoring_error = scoring_conversion_error or compile_typst(record["id"], "scoring", scoring)
        candidate = {
            "schemaVersion": 1,
            "id": record["id"],
            "course": record["course"],
            "year": record["year"],
            "form": record["form"],
            "question": record["question"],
            "source": record["source"],
            "focus": record["focus"],
            "assets": record["assets"],
            "bodyTypst": body,
            "scoringGuideTypst": scoring,
            "compile": {"body": body_error is None, "scoringGuide": scoring_error is None, "errors": {"body": body_error, "scoringGuide": scoring_error}},
            "solutionExtractionStatus": "unsegmented-scoring-guide",
            "reviewState": "unreviewed",
            "publishState": "blocked",
        }
        target = OUT / path.name
        target.write_text(json.dumps(candidate, indent=2) + "\n", encoding="utf-8")
        summary.append({"id": record["id"], "bodyCompiles": body_error is None, "scoringCompiles": scoring_error is None})
    (OUT / "index.json").write_text(json.dumps({"schemaVersion": 1, "candidates": summary}, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"candidates": len(summary), "bodyCompilePassed": sum(row["bodyCompiles"] for row in summary), "scoringCompilePassed": sum(row["scoringCompiles"] for row in summary), "publishState": "blocked"}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
