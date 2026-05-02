from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

import anthropic

from .compile_gate import compile_latex
from .contracts import RunManifest
from .pipeline import merge_blocks
from .renderer import build_latex_document, write_tex
from .review import load_skip_set, write_review_template


def _insert_src_path() -> None:
    repo_root = Path(__file__).resolve().parent.parent
    src_path = repo_root / "src"
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))


_QNUM_PATTERNS = (
    re.compile(r"(?im)\bquestion\s*(\d{1,2})\b"),
    re.compile(r"(?m)^\s*(\d{1,2})\s*[.)]\s+"),
)


def _recover_question_number(*texts: str) -> int | None:
    for text in texts:
        if not text:
            continue
        for pattern in _QNUM_PATTERNS:
            match = pattern.search(text)
            if match:
                try:
                    return int(match.group(1))
                except ValueError:
                    continue
    return None


def _is_nontrivial_text(value: object) -> bool:
    return isinstance(value, str) and len(value.strip()) >= 12


def _is_table_like_figure(figure: dict) -> bool:
    text = " ".join(
        str(figure.get(key) or "")
        for key in ("description", "caption", "label")
    ).lower()
    if not text:
        return False
    if "table" in text and not any(token in text for token in ("graph", "diagram", "plot", "curve")):
        return True
    return False


def _normalize_sg_extraction(extraction: dict) -> tuple[dict, list[str]]:
    warnings: list[str] = []
    raw_page_type = str(extraction.get("page_type") or "").strip().lower()
    if raw_page_type in {"frq", "real_frq", "real_frq_page", "real_frq_question", "question", "question_page", "frq_page"}:
        page_type = "frq"
    elif raw_page_type in {"skip", "other", "cover", "title"}:
        page_type = "skip"
    else:
        page_type = "skip"
        warnings.append("invalid_page_type")
    extraction["page_type"] = page_type

    if page_type == "skip":
        extraction.setdefault("skip_reason", extraction.get("skip_reason") or "other")
        return extraction, warnings

    if "question" not in extraction and isinstance(extraction.get("question_prompt"), str):
        extraction["question"] = extraction.get("question_prompt")

    question_text = extraction.get("question") or ""
    solution_text = extraction.get("solution") or ""
    grading_text = extraction.get("grading_scheme") or ""

    qnum = extraction.get("question_number")
    if not isinstance(qnum, int):
        recovered = _recover_question_number(question_text, solution_text, grading_text)
        if recovered is not None:
            extraction["question_number"] = recovered
            warnings.append("recovered_question_number")
        else:
            warnings.append("missing_question_number")

    if not _is_nontrivial_text(question_text):
        warnings.append("missing_question_text")
    if not _is_nontrivial_text(solution_text):
        warnings.append("missing_solution_text")
    if not _is_nontrivial_text(grading_text):
        warnings.append("missing_grading_text")

    if extraction.get("tables") and extraction.get("figures"):
        extraction["figures"] = [fig for fig in extraction.get("figures", []) if not _is_table_like_figure(fig)]

    return extraction, warnings


def _normalize_exam_extraction(extraction: dict) -> tuple[dict, list[str]]:
    warnings: list[str] = []
    raw_page_type = str(extraction.get("page_type") or "").strip().lower()
    if raw_page_type in {"exam", "question", "exam_page"}:
        page_type = "exam"
    elif raw_page_type in {"skip", "other", "cover", "title"}:
        page_type = "skip"
    else:
        page_type = "skip"
        warnings.append("invalid_exam_page_type")
    extraction["page_type"] = page_type

    if page_type == "skip":
        return extraction, warnings

    normalized_questions: list[dict] = []
    for question in extraction.get("questions", []):
        if "question" not in question and isinstance(question.get("question_text"), str):
            question["question"] = question.get("question_text")
        normalized_figures: list[dict] = []
        for figure in question.get("figures", []) or []:
            if question.get("tables") and _is_table_like_figure(figure):
                continue
            if all(key in figure for key in ("x", "y", "width", "height")):
                normalized_figures.append(figure)
                continue
            bbox = figure.get("bounding_box")
            if isinstance(bbox, list) and len(bbox) == 4:
                normalized_figures.append(
                    {
                        "x": bbox[0],
                        "y": bbox[1],
                        "width": bbox[2],
                        "height": bbox[3],
                        "caption": figure.get("caption"),
                    }
                )
        if normalized_figures:
            question["figures"] = normalized_figures
        qtext = question.get("question") or ""
        qnum = question.get("question_number")
        if not isinstance(qnum, int):
            recovered = _recover_question_number(qtext)
            if recovered is not None:
                question["question_number"] = recovered
            else:
                warnings.append("exam_missing_question_number")
        if _is_nontrivial_text(qtext):
            normalized_questions.append(question)
        else:
            warnings.append("exam_missing_question_text")

    extraction["questions"] = normalized_questions
    return extraction, warnings


def _extract_with_retry(extract_fn, image_path: str, *, client: anthropic.Anthropic, cache, force: bool, model: str, normalize_fn, max_attempts: int, debug_dir: Path | None = None, debug_prefix: str = "") -> tuple[dict, list[str], int]:
    last = None
    last_warnings: list[str] = []
    for attempt in range(1, max_attempts + 1):
        attempt_force = force or attempt > 1
        debug_payload: list[dict] = []
        try:
            current = extract_fn(
                image_path,
                client=client,
                cache=cache,
                force=attempt_force,
                model=model,
                usage_out=[],
                debug_out=debug_payload,
            )
        except Exception as exc:
            last_warnings = [f"extract_exception:{type(exc).__name__}"]
            if debug_dir is not None:
                debug_dir.mkdir(parents=True, exist_ok=True)
                (debug_dir / f"{debug_prefix}-attempt{attempt}.json").write_text(json.dumps({"error": str(exc)}, indent=2), encoding="utf-8")
            continue

        if debug_dir is not None and debug_payload:
            debug_dir.mkdir(parents=True, exist_ok=True)
            (debug_dir / f"{debug_prefix}-attempt{attempt}.json").write_text(json.dumps(debug_payload[0], indent=2), encoding="utf-8")

        normalized, warnings = normalize_fn(current)
        last = normalized
        last_warnings = warnings
        if not warnings:
            return normalized, warnings, attempt
        if normalized.get("page_type") == "frq" and isinstance(normalized.get("question_number"), int):
            return normalized, warnings, attempt
        if normalized.get("page_type") == "exam" and normalized.get("questions"):
            return normalized, warnings, attempt
    if last is None:
        return {"page_type": "skip", "skip_reason": "other"}, ["empty_extraction"], max_attempts
    return last, last_warnings, max_attempts


def _collect_exam_questions(exam_file: Path, client: anthropic.Anthropic, model: str, force: bool, cache_exam: str, max_attempts: int, debug_dir: Path) -> tuple[dict[int, dict], list[str]]:
    from cache import FRQCache
    from exam_extractor import extract_exam_page
    from figure_extract import materialise_figures
    from renderer import page_count, render_page, save_temp_image

    q_by_num: dict[int, dict] = {}
    warnings: list[str] = []
    exam_cache = FRQCache(cache_exam)
    total = page_count(str(exam_file))
    for page_idx in range(total):
        print(f"Exam page {page_idx + 1}/{total}...", flush=True)
        img = render_page(str(exam_file), page_idx, dpi=220)
        tmp = save_temp_image(img)
        try:
            extraction, extraction_warnings, attempts_used = _extract_with_retry(
                extract_exam_page,
                tmp,
                client=client,
                cache=exam_cache,
                force=force,
                model=model,
                normalize_fn=_normalize_exam_extraction,
                max_attempts=max_attempts,
                debug_dir=debug_dir,
                debug_prefix=f"exam-page{page_idx + 1}",
            )
        finally:
            Path(tmp).unlink(missing_ok=True)
        if extraction_warnings:
            warnings.append(f"exam:p{page_idx + 1}:attempts={attempts_used}:{','.join(extraction_warnings)}")
        if extraction.get("page_type") != "exam":
            continue
        for question in extraction.get("questions", []):
            qnum = question.get("question_number")
            if qnum is None:
                continue
            if question.get("figures"):
                question["figures"] = materialise_figures(
                    question["figures"],
                    img,
                    str(exam_file),
                    page_idx,
                    str(Path("output_latex/figures")),
                    exam_file.stem,
                    question_number=qnum,
                )
            q_by_num[int(qnum)] = question
    return q_by_num, warnings


def _collect_sg_rows(sg_file: Path, client: anthropic.Anthropic, model: str, force: bool, cache_frq: str, max_attempts: int, debug_dir: Path) -> tuple[list[dict], int, list[str]]:
    from cache import FRQCache
    from extractor import extract_page
    from figure_extract import materialise_figures
    from renderer import page_count, render_page, save_temp_image

    sg_cache = FRQCache(cache_frq)
    rows: list[dict] = []
    frq_page_count = 0
    warnings: list[str] = []
    total = page_count(str(sg_file))
    figures_dir = Path("output_latex/figures")
    figures_dir.mkdir(parents=True, exist_ok=True)
    for page_idx in range(total):
        print(f"SG page {page_idx + 1}/{total}...", flush=True)
        img = render_page(str(sg_file), page_idx, dpi=220)
        tmp = save_temp_image(img)
        try:
            extraction, extraction_warnings, attempts_used = _extract_with_retry(
                extract_page,
                tmp,
                client=client,
                cache=sg_cache,
                force=force,
                model=model,
                normalize_fn=_normalize_sg_extraction,
                max_attempts=max_attempts,
                debug_dir=debug_dir,
                debug_prefix=f"sg-page{page_idx + 1}",
            )
        finally:
            Path(tmp).unlink(missing_ok=True)

        if extraction_warnings:
            warnings.append(f"sg:p{page_idx + 1}:attempts={attempts_used}:{','.join(extraction_warnings)}")

        if extraction.get("figures"):
            extraction["figures"] = materialise_figures(
                extraction["figures"], img, str(sg_file), page_idx, str(figures_dir), sg_file.stem, question_number=extraction.get("question_number")
            )

        if extraction.get("page_type") == "frq":
            frq_page_count += 1

        rows.append({
            "fname": sg_file.name,
            "page": page_idx,
            "extraction": extraction,
            "error": None,
            "pdf_path": str(sg_file),
        })
    return rows, frq_page_count, warnings


def _write_manifest(path: str, manifest: RunManifest) -> None:
    payload = {
        "sg_pdf": manifest.sg_pdf,
        "exam_pdf": manifest.exam_pdf,
        "output_tex": manifest.output_tex,
        "output_pdf": manifest.output_pdf,
        "model": manifest.model,
        "compile_ok": manifest.compile_ok,
        "compile_output": manifest.compile_output,
        "skipped_blocks": manifest.skipped_blocks,
        "unresolved_blocks": manifest.unresolved_blocks,
    }
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="OCR-FRQ LaTeX runner")
    parser.add_argument("--sg", required=True, help="Scoring guide PDF path (SG-*.pdf)")
    parser.add_argument("--exam", help="Exam PDF path")
    parser.add_argument("--output-tex", default="output_latex/output.tex")
    parser.add_argument("--output-pdf", default="output_latex/output.pdf")
    parser.add_argument("--review-file", default="output_latex/review.json")
    parser.add_argument("--manifest", default="output_latex/manifest.json")
    parser.add_argument("--cache-frq", default="cache/frq")
    parser.add_argument("--cache-exam", default="cache/exam")
    parser.add_argument("--model", default="claude-haiku-4-5")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--max-attempts", type=int, default=2, help="Max extraction attempts per page")
    parser.add_argument("--debug-dir", default="output_latex/debug", help="Directory for raw per-page extraction payloads")
    args = parser.parse_args()

    api_key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if not api_key:
        raise SystemExit("ANTHROPIC_API_KEY is required")

    sg_path = Path(args.sg)
    if not sg_path.exists():
        raise SystemExit(f"SG PDF not found: {sg_path}")
    exam_path = Path(args.exam) if args.exam else None
    if exam_path and not exam_path.exists():
        raise SystemExit(f"Exam PDF not found: {exam_path}")

    _insert_src_path()
    client = anthropic.Anthropic(api_key=api_key)
    started = time.time()

    print("Starting OCR-FRQ LaTeX run", flush=True)
    print(f"SG: {sg_path}", flush=True)
    if exam_path:
        print(f"Exam: {exam_path}", flush=True)
    print(f"Model: {args.model}", flush=True)

    exam_q_by_num: dict[int, dict] = {}
    extraction_warnings: list[str] = []
    debug_dir = Path(args.debug_dir)
    if exam_path is not None:
        print("Extracting exam questions...", flush=True)
        exam_q_by_num, exam_warnings = _collect_exam_questions(exam_path, client, args.model, args.force, args.cache_exam, args.max_attempts, debug_dir)
        extraction_warnings.extend(exam_warnings)

    print("Extracting scoring guide...", flush=True)
    sg_rows, frq_pages, sg_warnings = _collect_sg_rows(sg_path, client, args.model, args.force, args.cache_frq, args.max_attempts, debug_dir)
    extraction_warnings.extend(sg_warnings)
    print("Merging blocks and rendering LaTeX...", flush=True)
    blocks = merge_blocks(sg_rows, exam_q_by_num)
    unresolved_blocks = [b.block_id for b in blocks if b.warnings]

    print(f"Exam questions extracted: {len(exam_q_by_num)}", flush=True)
    print(f"SG pages scanned: {len(sg_rows)}", flush=True)
    print(f"SG FRQ pages detected: {frq_pages}", flush=True)
    print(f"Question blocks emitted: {len(blocks)}", flush=True)
    if extraction_warnings:
        print(f"Extraction warnings: {len(extraction_warnings)}", flush=True)

    if len(blocks) == 0:
        compile_ok = False
        compile_output = "No question blocks were produced. Extraction likely failed to detect FRQ pages or question numbers."
        run_manifest = RunManifest(
            sg_pdf=str(sg_path),
            exam_pdf=str(exam_path) if exam_path else None,
            output_tex=args.output_tex,
            output_pdf=args.output_pdf,
            model=args.model,
            compile_ok=compile_ok,
            compile_output=compile_output,
            skipped_blocks=[],
            unresolved_blocks=extraction_warnings,
        )
        _write_manifest(args.manifest, run_manifest)
        print("Compile gate: FAIL", flush=True)
        print(compile_output, flush=True)
        raise SystemExit(2)

    if not Path(args.review_file).exists():
        write_review_template(args.review_file, unresolved_blocks)
    skipped = load_skip_set(args.review_file)

    tex = build_latex_document(blocks, skipped)
    write_tex(args.output_tex, tex)

    compile_ok, compile_output = compile_latex(args.output_tex, args.output_pdf)
    run_manifest = RunManifest(
        sg_pdf=str(sg_path),
        exam_pdf=str(exam_path) if exam_path else None,
        output_tex=args.output_tex,
        output_pdf=args.output_pdf,
        model=args.model,
        compile_ok=compile_ok,
        compile_output=compile_output,
        skipped_blocks=sorted(skipped),
        unresolved_blocks=unresolved_blocks + extraction_warnings,
    )
    _write_manifest(args.manifest, run_manifest)

    print(f"LaTeX: {args.output_tex}")
    print(f"PDF: {args.output_pdf}")
    print(f"Manifest: {args.manifest}")
    print(f"Review file: {args.review_file}")
    print(f"Elapsed: {time.time() - started:.1f}s")
    if compile_ok:
        print("Compile gate: PASS")
    else:
        print("Compile gate: FAIL")
        print(compile_output)


if __name__ == "__main__":
    main()
