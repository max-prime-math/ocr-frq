"""
run_pdf.py - CLI runner for OCR-FRQ Typst extraction.

Examples:
  python run_pdf.py PDFs/*.pdf
  python run_pdf.py --input-dir PDFs --output output_typst/output.typ --force
"""

import argparse
import os
import sys
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).parent / "src"))

import anthropic
from cache import FRQCache
from exam_extractor import extract_exam_page
from extractor import extract_page
from figure_extract import _are_similar_figures, materialise_figures
from renderer import page_count, render_page, save_temp_image
from typst_gen import build_document


def _collect_pdfs(paths: list[str], input_dirs: list[str]) -> list[Path]:
    found: list[Path] = []

    for raw in paths:
        p = Path(raw)
        if p.is_dir():
            found.extend(sorted(p.glob("*.pdf")))
            found.extend(sorted(p.glob("*.PDF")))
        elif p.suffix.lower() == ".pdf" and p.exists():
            found.append(p)

    for raw in input_dirs:
        d = Path(raw)
        if d.is_dir():
            found.extend(sorted(d.glob("*.pdf")))
            found.extend(sorted(d.glob("*.PDF")))

    dedup: dict[str, Path] = {}
    for p in found:
        dedup[str(p.resolve())] = p
    return sorted(dedup.values(), key=lambda p: p.name.lower())


def _detect_pairs(files: list[Path]) -> tuple[list[tuple[Path, Path | None]], list[str]]:
    sg_by_stem: dict[str, Path] = {}
    exam_by_name: dict[str, Path] = {}
    warnings: list[str] = []

    for file_path in files:
        name = file_path.name
        if name.startswith("SG-"):
            sg_by_stem[name[3:]] = file_path
        else:
            exam_by_name[name] = file_path

    pairs: list[tuple[Path, Path | None]] = []
    for stem, sg_file in sorted(sg_by_stem.items(), key=lambda item: item[0].lower()):
        exam_file = exam_by_name.pop(stem, None)
        pairs.append((sg_file, exam_file))

    for name in sorted(exam_by_name):
        warnings.append(f"Exam file '{name}' has no matching SG (SG-{name}). Skipping.")

    return pairs, warnings


def _deduplicate_saved_figures(combined_figs: list[dict], figures_dir: str) -> list[dict]:
    if not combined_figs or len(combined_figs) < 2:
        return combined_figs

    base_dir = Path(figures_dir)
    records = []
    for i, fig in enumerate(combined_figs):
        file_path = fig.get("file_path", "")
        if not file_path:
            continue
        full_path = base_dir / file_path.replace("figures/", "")
        if not full_path.exists():
            records.append((i, fig, None))
            continue
        try:
            img = Image.open(full_path)
            records.append((i, fig, img))
        except Exception:
            records.append((i, fig, None))

    survivors_idx = set()
    for i in range(len(records)):
        if i in survivors_idx:
            continue
        if records[i][2] is None:
            survivors_idx.add(i)
            continue

        survivors_idx.add(i)
        for j in range(i + 1, len(records)):
            if j in survivors_idx:
                continue
            if records[j][2] is not None and _are_similar_figures(records[i][2], records[j][2]):
                try:
                    fig_j = records[j][1]
                    file_path_j = fig_j.get("file_path", "")
                    if file_path_j:
                        full_path_j = base_dir / file_path_j.replace("figures/", "")
                        full_path_j.unlink(missing_ok=True)
                except Exception:
                    pass

    return [records[i][1] for i in sorted(survivors_idx)]


def _clear_old_figures(figures_dir: Path) -> None:
    if not figures_dir.exists():
        return
    for path in figures_dir.glob("*.png"):
        path.unlink(missing_ok=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="OCR-FRQ CLI: SG + exam PDFs to Typst")
    parser.add_argument("pdf", nargs="*", help="PDF files or directories")
    parser.add_argument("--input-dir", action="append", default=[], help="Directory to scan for PDFs")
    parser.add_argument("--output", default="output_typst/output.typ", help="Output Typst file path")
    parser.add_argument("--model", default="claude-haiku-4-5", help="Claude model ID")
    parser.add_argument("--force", action="store_true", help="Bypass cache and re-process every page")
    parser.add_argument("--cache-frq", default="cache/frq", help="Scoring-guide cache directory")
    parser.add_argument("--cache-exam", default="cache/exam", help="Exam-page cache directory")
    args = parser.parse_args()

    api_key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if not api_key:
        print("Error: ANTHROPIC_API_KEY not set.", file=sys.stderr)
        sys.exit(1)

    pdf_paths = _collect_pdfs(args.pdf, args.input_dir)
    if not pdf_paths:
        print("Error: No PDF files found.", file=sys.stderr)
        sys.exit(1)

    pairs, warnings = _detect_pairs(pdf_paths)
    if not pairs:
        print("Error: No scoring-guide files found (expected names starting with 'SG-').", file=sys.stderr)
        sys.exit(1)

    for warning in warnings:
        print(f"Warning: {warning}")

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    figures_dir = output_path.parent / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)
    _clear_old_figures(figures_dir)

    client = anthropic.Anthropic(api_key=api_key)
    sg_cache = FRQCache(args.cache_frq)
    exam_cache = FRQCache(args.cache_exam)

    all_results: list[dict] = []
    usage_log: list[dict] = []

    for sg_file, exam_file in pairs:
        print(f"\nPair: {exam_file.name if exam_file else '(no exam)'} <-> {sg_file.name}")
        sg_results: list[dict] = []
        exam_by_qnum: dict[int, dict] = {}

        sg_page_total = page_count(str(sg_file))
        sg_stem = sg_file.stem
        for page_idx in range(sg_page_total):
            print(f"  SG page {page_idx + 1}/{sg_page_total}...", end=" ", flush=True)
            try:
                img = render_page(str(sg_file), page_idx, dpi=220)
                tmp_img = save_temp_image(img)
                try:
                    extraction = extract_page(
                        tmp_img,
                        client=client,
                        cache=sg_cache,
                        force=args.force,
                        model=args.model,
                        usage_out=usage_log,
                    )
                finally:
                    Path(tmp_img).unlink(missing_ok=True)

                if extraction.get("figures"):
                    try:
                        qnum = extraction.get("question_number")
                        extraction["figures"] = materialise_figures(
                            extraction["figures"],
                            img,
                            str(sg_file),
                            page_idx,
                            str(figures_dir),
                            sg_stem,
                            question_number=qnum,
                        )
                    except Exception as exc:
                        print(f"warning (figure extraction): {exc}", file=sys.stderr)

                sg_results.append({
                    "fname": sg_file.name,
                    "page": page_idx,
                    "extraction": extraction,
                    "error": None,
                    "pdf_path": str(sg_file),
                })
                ptype = extraction.get("page_type", "?")
                qnum = extraction.get("question_number")
                label = f"Q{qnum}" if qnum is not None else ptype
                print(label)
            except Exception as exc:
                sg_results.append({
                    "fname": sg_file.name,
                    "page": page_idx,
                    "extraction": None,
                    "error": str(exc),
                    "pdf_path": str(sg_file),
                })
                print(f"ERROR: {exc}")

        if exam_file is not None:
            exam_total = page_count(str(exam_file))
            exam_stem = exam_file.stem
            for page_idx in range(exam_total):
                print(f"  Exam page {page_idx + 1}/{exam_total}...", end=" ", flush=True)
                try:
                    img = render_page(str(exam_file), page_idx, dpi=220)
                    tmp_img = save_temp_image(img)
                    try:
                        exam_extraction = extract_exam_page(
                            tmp_img,
                            client=client,
                            cache=exam_cache,
                            force=args.force,
                            model=args.model,
                            usage_out=usage_log,
                        )
                    finally:
                        Path(tmp_img).unlink(missing_ok=True)

                    if exam_extraction.get("page_type") == "exam":
                        for question in exam_extraction.get("questions", []):
                            qnum = question.get("question_number")
                            if qnum is None:
                                continue
                            if question.get("figures"):
                                try:
                                    question["figures"] = materialise_figures(
                                        question["figures"],
                                        img,
                                        str(exam_file),
                                        page_idx,
                                        str(figures_dir),
                                        exam_stem,
                                        question_number=qnum,
                                    )
                                except Exception as exc:
                                    print(f"warning (exam figure extraction): {exc}", file=sys.stderr)
                            exam_by_qnum[qnum] = question
                    print(exam_extraction.get("page_type", "?"))
                except Exception as exc:
                    print(f"ERROR: {exc}")

        for sg_result in sg_results:
            if sg_result.get("error") or sg_result.get("extraction", {}).get("page_type") != "frq":
                all_results.append(sg_result)
                continue

            ext = sg_result["extraction"]
            qnum = ext.get("question_number")
            if qnum in exam_by_qnum:
                exam_q = exam_by_qnum[qnum]
                ext["question"] = exam_q.get("question", ext.get("question"))
                ext["unit"] = exam_q.get("unit")
                ext["section"] = exam_q.get("section")
                ext["calculator"] = exam_q.get("calculator")
                ext["tables"] = [dict(table, section="question") for table in exam_q.get("tables", [])] + (ext.get("tables", []) or [])
                exam_figs = [dict(fig, section="question") for fig in exam_q.get("figures", [])]
                sg_figs = ext.get("figures", [])
                ext["figures"] = _deduplicate_saved_figures(exam_figs + sg_figs, str(figures_dir))
            else:
                ext["flagged"] = True
                ext["flag_reason"] = "Question text from SG (no matching exam page)"

            all_results.append(sg_result)

    typ_content = build_document(all_results)
    output_path.write_text(typ_content, encoding="utf-8")

    frq_count = len([r for r in all_results if not r.get("error") and r.get("extraction", {}).get("page_type") == "frq"])
    skip_count = len([r for r in all_results if not r.get("error") and r.get("extraction", {}).get("page_type") == "skip"])
    err_count = len([r for r in all_results if r.get("error")])
    print(f"\nDone. FRQ={frq_count} skipped={skip_count} errors={err_count}")
    print(f"Output: {output_path}")
    print(f"Figures: {figures_dir}")


if __name__ == "__main__":
    main()
