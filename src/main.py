"""
main.py — FRQ pipeline entry point.

Usage:
  python -m src.main [--years 1998,1999,...] [--output-dir OUTPUT_DIR] [--force]
  python -m src.main --year 2018

Processes BC and BC Form B exams from the mathpix/ directory.
Produces a single combined exam-class LaTeX/PDF in output_dir.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .compile_gate import compile_latex
from .contracts import QuestionBlock
from .latex_writer import build_combined_document, write_tex
from .mathpix import parse_exam_zip, parse_sg_zip

REPO_ROOT = Path(__file__).resolve().parent.parent
MATHPIX_DIR = REPO_ROOT / "mathpix"
DEFAULT_OUTPUT_DIR = REPO_ROOT / "output_latex"
CORRECTIONS_FILE = REPO_ROOT / "corrections" / "corrections.json"


def _load_corrections() -> dict[tuple[int, str, int], list[dict]]:
    """Load corrections.json into a lookup keyed by (year, form, question)."""
    if not CORRECTIONS_FILE.exists():
        return {}
    data = json.loads(CORRECTIONS_FILE.read_text(encoding="utf-8"))
    result: dict[tuple[int, str, int], list[dict]] = {}
    for entry in data.get("corrections", []):
        key = (int(entry["year"]), entry.get("form", "").upper(), int(entry["question"]))
        result[key] = entry.get("sg_patches", [])
    return result


def _apply_corrections(
    blocks: list[QuestionBlock],
    corrections: dict[tuple[int, str, int], list[dict]],
) -> list[QuestionBlock]:
    """Apply manual sg_text corrections to matching blocks."""
    if not corrections:
        return blocks
    patched: list[QuestionBlock] = []
    for block in blocks:
        key = (block.year, block.form.upper(), block.question_number)
        patches = corrections.get(key, [])
        if not patches:
            patched.append(block)
            continue
        sg = block.sg_text
        for patch in patches:
            if "sg_find" in patch and "sg_replace" in patch:
                sg = sg.replace(patch["sg_find"], patch["sg_replace"])
            elif "sg_append" in patch:
                sg = sg.rstrip() + "\n\n" + patch["sg_append"]
        patched.append(QuestionBlock(
            question_number=block.question_number,
            year=block.year,
            exam=block.exam,
            form=block.form,
            part=block.part,
            calculator_active=block.calculator_active,
            question_text=block.question_text,
            sg_text=sg,
            figure_paths=block.figure_paths,
        ))
    return patched

# All years with Mathpix zips (no 2024)
_ALL_YEARS = list(range(1998, 2020))

# Years that have a Form B exam
_FORM_B_YEARS = list(range(2002, 2012))


def _zip_path(year: int, form: str = "") -> tuple[Path, Path] | None:
    """Return (exam_zip, sg_zip) paths if both exist, else None."""
    form_tag = "-FORM-B" if form.upper() == "B" else ""
    exam = MATHPIX_DIR / f"BC-{year}{form_tag}.zip"
    sg = MATHPIX_DIR / f"SG-BC-{year}{form_tag}.zip"
    if exam.exists() and sg.exists():
        return exam, sg
    return None


def process_year(
    year: int,
    figures_dir: Path,
    form: str = "",
) -> list[QuestionBlock]:
    zips = _zip_path(year, form)
    if zips is None:
        tag = f"{year}" + (" Form B" if form else "")
        print(f"  Skipping {tag}: missing zip(s)", flush=True)
        return []

    exam_zip, sg_zip = zips
    form_tag = " Form B" if form.upper() == "B" else ""
    print(f"  {year} BC{form_tag}:", flush=True)

    print(f"    Parsing exam zip…", flush=True)
    exam_qs = parse_exam_zip(str(exam_zip), str(figures_dir), year, form)
    print(f"    Parsing SG zip…", flush=True)
    sg_texts = parse_sg_zip(str(sg_zip), str(figures_dir), year, form)

    if not exam_qs:
        print(f"    No questions parsed from exam zip!", flush=True)
        return []

    blocks: list[QuestionBlock] = []
    for qnum in sorted(exam_qs.keys()):
        eq = exam_qs[qnum]
        block = QuestionBlock(
            question_number=qnum,
            year=year,
            exam="BC",
            form=form.upper() if form else "",
            part=eq.part,
            calculator_active=eq.calculator_active,
            question_text=eq.question_text,
            sg_text=sg_texts.get(qnum, ""),
            figure_paths=eq.figure_paths,
        )
        blocks.append(block)

    print(f"    {len(blocks)} question(s) parsed", flush=True)
    return blocks


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="FRQ pipeline — Mathpix → LaTeX → PDF")
    parser.add_argument(
        "--years",
        help="Comma-separated years to process (default: all)",
    )
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Output directory for .tex and .pdf files",
    )
    parser.add_argument(
        "--no-form-b",
        action="store_true",
        help="Skip Form B exams",
    )
    parser.add_argument(
        "--compile",
        action="store_true",
        default=True,
        help="Compile .tex to PDF after rendering (default: on)",
    )
    parser.add_argument(
        "--no-compile",
        action="store_true",
        help="Skip PDF compilation",
    )
    args = parser.parse_args(argv)

    years = (
        [int(y.strip()) for y in args.years.split(",")]
        if args.years
        else _ALL_YEARS
    )

    output_dir = Path(args.output_dir)
    figures_dir = output_dir / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)

    corrections = _load_corrections()
    if corrections:
        print(f"Loaded {len(corrections)} manual correction(s) from corrections.json", flush=True)

    print("FRQ pipeline", flush=True)
    print(f"Years: {years}", flush=True)
    print(f"Output: {output_dir}", flush=True)
    print()

    blocks_by_year: dict[int, list[QuestionBlock]] = {}
    form_b_by_year: dict[int, list[QuestionBlock]] = {}

    for year in years:
        print(f"Processing {year}…", flush=True)
        std = process_year(year, figures_dir, form="")
        if std:
            blocks_by_year[year] = _apply_corrections(std, corrections)

        if not args.no_form_b and year in _FORM_B_YEARS:
            fb = process_year(year, figures_dir, form="B")
            if fb:
                form_b_by_year[year] = _apply_corrections(fb, corrections)

    total_qs = sum(len(v) for v in blocks_by_year.values()) + sum(len(v) for v in form_b_by_year.values())
    print(f"\nTotal questions: {total_qs}", flush=True)

    if total_qs == 0:
        print("No questions to render.", flush=True)
        return 1

    tex = build_combined_document(blocks_by_year, form_b_by_year or None)
    tex_path = output_dir / "output_frq.tex"
    pdf_path = output_dir / "output_frq.pdf"
    write_tex(str(tex_path), tex)
    print(f"\nTeX: {tex_path}", flush=True)

    if not args.no_compile:
        print("Compiling…", flush=True)
        ok, log = compile_latex(str(tex_path), str(pdf_path))
        if ok:
            print(f"PDF: {pdf_path}", flush=True)
        else:
            print("Compile FAILED. Last 3000 chars of log:", flush=True)
            print(log[-3000:], flush=True)
            return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
