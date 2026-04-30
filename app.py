"""
app.py — Streamlit interface for OCR-FRQ.

Run with:
    streamlit run app.py
"""

import io
import os
import sys
import tempfile
import zipfile
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).parent / "src"))

import anthropic
from cache import FRQCache
from extractor import extract_page
from exam_extractor import extract_exam_page
from figure_extract import materialise_figures
from typst_gen import build_document
from renderer import page_count, render_page, save_temp_image

# ---------------------------------------------------------------------------
# Pricing
# ---------------------------------------------------------------------------

_PRICING = {
    "claude-haiku-4-5":  {"input": 1.00, "output": 5.00,  "cache_read": 0.10, "cache_write": 1.25},
    "claude-sonnet-4-6": {"input": 3.00, "output": 15.00, "cache_read": 0.30, "cache_write": 3.75},
    "claude-opus-4-7":   {"input": 5.00, "output": 25.00, "cache_read": 0.50, "cache_write": 6.25},
}


def _compute_cost(usage_log: list, model: str) -> dict:
    p = _PRICING.get(model, _PRICING["claude-haiku-4-5"])
    totals = {"input": 0, "output": 0, "cache_read": 0, "cache_write": 0}
    for u in usage_log:
        totals["input"]      += u.get("input_tokens", 0)
        totals["output"]     += u.get("output_tokens", 0)
        totals["cache_read"] += u.get("cache_read_input_tokens", 0)
        totals["cache_write"] += u.get("cache_creation_input_tokens", 0)
    cost = (
        totals["input"]       * p["input"]       / 1_000_000
        + totals["output"]    * p["output"]       / 1_000_000
        + totals["cache_read"]  * p["cache_read"] / 1_000_000
        + totals["cache_write"] * p["cache_write"] / 1_000_000
    )
    return {**totals, "cost_usd": cost}


def _progress(done: int, total: int) -> float:
    return max(0.0, min(1.0, done / total)) if total > 0 else 0.0


def _detect_pairs(uploaded_files: list) -> tuple[list[dict], list[str]]:
    """
    Detect paired exam and SG files from uploaded files.

    Returns:
        (pairs, warnings)
        pairs: list of {"sg_file": file, "exam_file": file|None}
        warnings: list of warning strings (orphaned exam files, etc.)
    """
    pairs = []
    warnings = []
    sg_by_stem = {}
    exam_by_stem = {}

    # Categorize files
    for uf in uploaded_files:
        name = uf.name
        if name.startswith("SG-"):
            stem = name[3:]  # Remove "SG-" prefix
            sg_by_stem[stem] = uf
        else:
            exam_by_stem[name] = uf

    # Create pairs
    for stem, sg_file in sg_by_stem.items():
        exam_file = exam_by_stem.pop(stem, None)
        pairs.append({"sg_file": sg_file, "exam_file": exam_file})

    # Warn about orphaned exam files
    for name, exam_file in exam_by_stem.items():
        warnings.append(f"⚠️ Exam file '{name}' has no matching SG (SG-{name}). Skipping.")

    return pairs, warnings


def _build_zip(typ_content: str, figures_dir: str | None = None) -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("output.typ", typ_content.encode("utf-8"))
        if figures_dir:
            figures_path = Path(figures_dir)
            if figures_path.exists():
                for fig_file in figures_path.glob("*.png"):
                    arcname = f"figures/{fig_file.name}"
                    zf.write(fig_file, arcname=arcname)
    return buf.getvalue()


# ---------------------------------------------------------------------------
# Page config & session state
# ---------------------------------------------------------------------------

st.set_page_config(page_title="OCR-FRQ", page_icon="📝", layout="wide")

for key, default in {
    "results": [],
    "processed": False,
    "usage_log": [],
    "model_used": None,
    "processing_error": None,
    "figures_dir": None,
    "pairs": [],
    "pair_warnings": [],
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------

with st.sidebar:
    st.title("OCR-FRQ")
    st.caption("Free-response PDFs → Typst")
    st.divider()

    api_key = st.text_input(
        "Anthropic API key",
        type="password",
        autocomplete="current-password",
        value=os.environ.get("ANTHROPIC_API_KEY", ""),
        help="Starts with sk-ant-. Never saved to disk.",
    )

    model = st.selectbox(
        "Model",
        ["claude-haiku-4-5", "claude-sonnet-4-6", "claude-opus-4-7"],
        help="Haiku: fastest and cheapest. Sonnet: higher accuracy.",
    )

    force_ocr = st.checkbox(
        "Force re-process",
        value=False,
        help="Ignore cached results and re-call Claude for every page.",
    )

    st.divider()
    st.caption("Responses cached in `cache/frq/` — repeated runs are cheap.")
    st.caption("Output is Typst (`.typ`) — compile with `typst compile output.typ`.")

# ---------------------------------------------------------------------------
# Main area
# ---------------------------------------------------------------------------

st.title("OCR-FRQ")
st.caption("Upload AP exam scoring guidelines PDFs to extract FRQ content as Typst.")

uploaded_files = st.file_uploader(
    "Drop PDF files here",
    type="pdf",
    accept_multiple_files=True,
)

if not uploaded_files:
    st.info("Upload one or more PDFs to get started.")
    st.info("💡 Tip: Pair original exams with scoring guides (e.g. BC-2009.pdf + SG-BC-2009.pdf)")
    st.stop()

# Detect pairs before showing Process button
pairs, pair_warnings = _detect_pairs(uploaded_files)
for warning in pair_warnings:
    st.warning(warning)

# Show detected pairs
if pairs:
    st.markdown("**Detected file pairs:**")
    for i, pair in enumerate(pairs):
        sg_name = pair["sg_file"].name
        exam_name = pair["exam_file"].name if pair["exam_file"] else "(no exam file)"
        status_icon = "✓" if pair["exam_file"] else "⚠"
        st.caption(f"{status_icon} {exam_name} ↔ {sg_name}")

if st.button("Process PDFs", type="primary", use_container_width=True):
    if not api_key:
        st.error("Enter your Anthropic API key in the sidebar.")
        st.stop()

    tmpdir = tempfile.mkdtemp()
    figures_dir = os.path.join(tmpdir, "figures")
    client = anthropic.Anthropic(api_key=api_key)
    sg_cache = FRQCache("cache/frq")
    exam_cache = FRQCache("cache/exam")

    # Write uploaded files to tmpdir
    pdf_files = {}
    for uf in uploaded_files:
        dest = os.path.join(tmpdir, uf.name)
        with open(dest, "wb") as fh:
            fh.write(uf.read())
        pdf_files[uf.name] = dest

    # Calculate total pages for progress
    try:
        total_pages = sum(page_count(pdf_files[pair["sg_file"].name]) +
                         (page_count(pdf_files[pair["exam_file"].name]) if pair["exam_file"] else 0)
                         for pair in pairs)
    except Exception as exc:
        st.error(f"Could not read PDFs: {exc}")
        st.stop()

    all_results: list[dict] = []
    usage_log: list[dict] = []
    pages_done = 0
    progress_bar = st.progress(0, text="Starting…")
    status = st.empty()
    processing_error = None

    try:
        for pair in pairs:
            sg_file = pair["sg_file"]
            exam_file = pair["exam_file"]
            sg_path = pdf_files[sg_file.name]
            exam_path = pdf_files[exam_file.name] if exam_file else None
            sg_stem = Path(sg_path).stem

            # Process SG pages
            sg_results = []
            sg_page_count = page_count(sg_path)
            for page_idx in range(sg_page_count):
                status.text(f"SG: {sg_file.name} — page {page_idx + 1} of {sg_page_count}")
                try:
                    img = render_page(sg_path, page_idx, dpi=220)
                    tmp_img = save_temp_image(img)
                    try:
                        extraction = extract_page(
                            tmp_img,
                            client=client,
                            cache=sg_cache,
                            force=force_ocr,
                            model=model,
                            usage_out=usage_log,
                        )
                    finally:
                        Path(tmp_img).unlink(missing_ok=True)

                    # Materialise SG figures
                    if extraction.get("figures"):
                        try:
                            question_num = extraction.get("question_number")
                            materialised = materialise_figures(
                                extraction["figures"],
                                img,
                                sg_path,
                                page_idx,
                                figures_dir,
                                sg_stem,
                                question_number=question_num,
                            )
                            extraction["figures"] = materialised
                        except Exception as e:
                            import logging
                            logging.exception("Error materialising SG figures: %s", e)

                    sg_results.append({
                        "fname": sg_file.name,
                        "page": page_idx,
                        "extraction": extraction,
                        "error": None,
                        "pdf_path": sg_path,
                    })
                except Exception as exc:
                    sg_results.append({
                        "fname": sg_file.name,
                        "page": page_idx,
                        "extraction": None,
                        "error": str(exc),
                        "pdf_path": sg_path,
                    })

                pages_done += 1
                st.session_state.results = all_results
                st.session_state.usage_log = usage_log
                st.session_state.model_used = model
                progress_bar.progress(
                    _progress(pages_done, total_pages),
                    text=f"{pages_done} / {total_pages} pages (SG)",
                )

            # Process exam pages (if present) and merge
            exam_by_qnum = {}
            exam_stem = Path(exam_path).stem if exam_path else None
            if exam_path:
                exam_page_count = page_count(exam_path)
                for page_idx in range(exam_page_count):
                    status.text(f"Exam: {exam_file.name} — page {page_idx + 1} of {exam_page_count}")
                    try:
                        img = render_page(exam_path, page_idx, dpi=220)
                        tmp_img = save_temp_image(img)
                        try:
                            exam_extraction = extract_exam_page(
                                tmp_img,
                                client=client,
                                cache=exam_cache,
                                force=force_ocr,
                                model=model,
                                usage_out=usage_log,
                            )
                        finally:
                            Path(tmp_img).unlink(missing_ok=True)

                        # Build lookup: qnum -> exam question data
                        if exam_extraction.get("page_type") == "exam":
                            for q in exam_extraction.get("questions", []):
                                qnum = q.get("question_number")
                                if qnum is not None:
                                    # Materialise exam figures for this question
                                    if q.get("figures"):
                                        try:
                                            materialised = materialise_figures(
                                                q["figures"],
                                                img,
                                                exam_path,
                                                page_idx,
                                                figures_dir,
                                                exam_stem,
                                                question_number=qnum,
                                            )
                                            q["figures"] = materialised
                                        except Exception as e:
                                            import logging
                                            logging.exception("Error materialising exam figures: %s", e)
                                    exam_by_qnum[qnum] = q
                    except Exception:
                        pass  # Silently skip exam page errors for now

                    pages_done += 1
                    st.session_state.results = all_results
                    st.session_state.usage_log = usage_log
                    st.session_state.model_used = model
                    progress_bar.progress(
                        _progress(pages_done, total_pages),
                        text=f"{pages_done} / {total_pages} pages (Exam)",
                    )

            # Merge SG + exam results by question_number
            for sg_result in sg_results:
                if sg_result.get("error") or sg_result.get("extraction", {}).get("page_type") != "frq":
                    all_results.append(sg_result)
                else:
                    ext = sg_result["extraction"]
                    qnum = ext.get("question_number")
                    if qnum in exam_by_qnum:
                        exam_q = exam_by_qnum[qnum]
                        ext["question"] = exam_q["question"]
                        # Merge figures: exam question figures + SG solution/rubric figures
                        exam_figs = [dict(f, section="question") for f in exam_q.get("figures", [])]
                        sg_figs = ext.get("figures", [])
                        ext["figures"] = exam_figs + sg_figs
                    else:
                        # No exam match: flag it but use SG question text
                        ext["flagged"] = True
                        ext["flag_reason"] = "Question text from SG (no matching exam page)"
                    all_results.append(sg_result)

    except Exception as exc:
        processing_error = str(exc)

    progress_bar.empty()
    status.empty()
    st.session_state.results = all_results
    st.session_state.usage_log = usage_log
    st.session_state.model_used = model
    st.session_state.figures_dir = figures_dir
    st.session_state.pairs = pairs
    st.session_state.processed = bool(all_results)
    st.session_state.processing_error = processing_error

    if processing_error:
        st.warning("Processing stopped early. Partial results shown below.")
    else:
        st.rerun()

# ---------------------------------------------------------------------------
# Results
# ---------------------------------------------------------------------------

if st.session_state.processing_error:
    st.warning(f"Partial run — stopped after: {st.session_state.processing_error}")

if not (st.session_state.processed and st.session_state.results):
    st.stop()

results: list[dict] = st.session_state.results

frq_pages  = [r for r in results if not r["error"] and r.get("extraction", {}).get("page_type") == "frq"]
skip_pages = [r for r in results if not r["error"] and r.get("extraction", {}).get("page_type") == "skip"]
flagged    = [r for r in frq_pages if r["extraction"].get("flagged")]
errors     = [r for r in results if r["error"]]

st.divider()

col1, col2, col3, col4 = st.columns(4)
col1.metric("✅ FRQ pages", len(frq_pages))
col2.metric("⏭️ Skipped pages", len(skip_pages))
col3.metric("⚠️ Flagged", len(flagged))
col4.metric("❌ Errors", len(errors))

# Token usage
if st.session_state.usage_log:
    usage = _compute_cost(st.session_state.usage_log, st.session_state.model_used or "claude-haiku-4-5")
    api_calls = len(st.session_state.usage_log)
    cache_hits = len(results) - api_calls

    with st.expander(f"💰 Cost — ${usage['cost_usd']:.4f}", expanded=True):
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("API calls", api_calls)
        c2.metric("Cache hits", cache_hits)
        c3.metric("Total tokens", f"{usage['input'] + usage['output'] + usage['cache_read'] + usage['cache_write']:,}")
        c4.metric("Cost", f"${usage['cost_usd']:.4f}")
        st.caption(
            f"Model: `{st.session_state.model_used}` · "
            f"Input: {usage['input']:,} · Output: {usage['output']:,} · "
            f"Cache read: {usage['cache_read']:,} · Cache write: {usage['cache_write']:,}"
        )
elif st.session_state.processed:
    st.info("All pages served from cache — no API calls made.")

if skip_pages:
    with st.expander(f"Skipped pages ({len(skip_pages)})"):
        for r in skip_pages:
            reason = r["extraction"].get("skip_reason") or "unknown"
            st.write(f"• {r['fname']} p{r['page'] + 1} — {reason}")

if errors:
    with st.expander(f"Errors ({len(errors)})"):
        for r in errors:
            st.error(f"{r['fname']} p{r['page'] + 1}: {r['error']}")

# ---------------------------------------------------------------------------
# Review flagged pages
# ---------------------------------------------------------------------------

if flagged:
    st.subheader("Review flagged pages")
    st.caption("These pages were extracted but confidence was low. Review before downloading.")

    for r in flagged:
        label = f"{r['fname']} — Page {r['page'] + 1} (Q{r['extraction'].get('question_number') or '?'})"
        with st.expander(label, expanded=True):
            img_col, text_col = st.columns([1, 1])

            with img_col:
                try:
                    img = render_page(r["pdf_path"], r["page"], dpi=150)
                    st.image(img, caption="Page image", use_container_width=True)
                except Exception:
                    st.warning("Could not render page image.")

            with text_col:
                ext = r["extraction"]
                st.markdown(f"**Flag reason:** {ext.get('flag_reason') or 'unspecified'}")
                if ext.get("question"):
                    st.markdown("**Question (first 400 chars):**")
                    st.text(ext["question"][:400] + ("…" if len(ext["question"]) > 400 else ""))
                if ext.get("solution"):
                    st.markdown("**Solution (first 200 chars):**")
                    st.text(ext["solution"][:200] + ("…" if len(ext["solution"]) > 200 else ""))
                if ext.get("grading_scheme"):
                    st.markdown("**Grading scheme (first 200 chars):**")
                    st.text(ext["grading_scheme"][:200] + ("…" if len(ext["grading_scheme"]) > 200 else ""))

# ---------------------------------------------------------------------------
# Download
# ---------------------------------------------------------------------------

st.divider()
st.subheader("Download")

if not frq_pages:
    st.warning("No FRQ pages were extracted — nothing to download.")
    st.stop()

typ_content = build_document(results)
figures_dir = st.session_state.figures_dir
zip_bytes = _build_zip(typ_content, figures_dir=figures_dir)

st.download_button(
    label="⬇️ Download output.zip",
    data=zip_bytes,
    file_name="frq_output.zip",
    mime="application/zip",
    type="primary",
    use_container_width=True,
)

with st.expander("Preview Typst"):
    preview = typ_content[:5000]
    if len(typ_content) > 5000:
        preview += "\n\n// … (truncated)"
    st.code(preview, language="text")
