"""
pdf_figure_extractor.py — Extract vector figures from PDFs before MathPix OCR.

Two-stage detection:
1. Heuristic pre-screen using page.get_drawings() to filter candidate pages
2. Claude Vision to identify figure bounding boxes
3. PNG extraction and PDF redaction with placeholder insertion

Figures are identified by {session_stem}_{n} (e.g., jan_21_1, jan_21_2).
"""

import base64
import json
import logging
import re
from pathlib import Path
from typing import Optional

from PIL import Image

from .cache import FRQCache
from .renderer import render_page

logger = logging.getLogger(__name__)

try:
    import fitz  # PyMuPDF
    _FITZ_AVAILABLE = True
except ImportError:
    _FITZ_AVAILABLE = False
    logger.error("PyMuPDF (fitz) not installed — figure extraction unavailable.")


FIGURE_DETECTION_PROMPT = """You are analyzing a page from a Manitoba Pre-Calculus 40S exam marking guide.

Identify all mathematical figures, graphs, coordinate planes, or geometric diagrams on this page.
Exclude: headers, footers, tables of numbers, inline equations, plain text, page borders.

For each figure, provide its bounding box as [x1, y1, x2, y2] with normalized coordinates:
  (0.0, 0.0) = top-left corner of the page
  (1.0, 1.0) = bottom-right corner of the page

Return ONLY valid JSON, no other text:
{"figures": [{"id": 1, "bbox": [x1, y1, x2, y2]}]}

If no figures are present: {"figures": []}"""


def _extract_session_stem(pdf_path: str) -> str:
    """
    Extract session stem from filename (e.g., 'jan_21' from 'pre-calc-40s_jan_21_mg-only_cleaned_aggressive.pdf').
    """
    stem = Path(pdf_path).stem
    match = re.search(r'((?:jan|jun)_\d{2})', stem)
    if match:
        return match.group(1)
    return stem.replace('pre-calc-40s_', '').replace('_mg-only_cleaned_aggressive', '')


def _get_drawings_bbox(drawings: list) -> Optional[fitz.Rect]:
    """Get bounding box union of all drawing rects."""
    if not drawings:
        return None
    rects = [fitz.Rect(d.get('rect', [0, 0, 0, 0])) for d in drawings if 'rect' in d]
    if not rects:
        return None
    union = rects[0]
    for rect in rects[1:]:
        union = union | rect
    return union if not union.is_empty else None


def _is_full_width_rule(drawing: dict, page_rect: fitz.Rect) -> bool:
    """Check if drawing is a full-width horizontal rule."""
    rect = fitz.Rect(drawing.get('rect', [0, 0, 0, 0]))
    width_ratio = rect.width / max(1, page_rect.width)
    height = rect.height
    return width_ratio > 0.85 and height < 3


def _is_page_border(drawing: dict, page_rect: fitz.Rect) -> bool:
    """Check if drawing is a page border (nearly full-page rect)."""
    rect = fitz.Rect(drawing.get('rect', [0, 0, 0, 0]))
    area_ratio = (rect.width * rect.height) / max(1, page_rect.width * page_rect.height)
    return area_ratio > 0.90


def _has_candidate_drawings(drawings: list, page_rect: fitz.Rect) -> bool:
    """
    Filter drawings to identify candidate figure regions.
    Returns True if page has substantial vector drawing content (excluding decorative elements).
    """
    if not drawings:
        return False

    filtered = []
    for d in drawings:
        if _is_full_width_rule(d, page_rect) or _is_page_border(d, page_rect):
            continue
        rect = fitz.Rect(d.get('rect', [0, 0, 0, 0]))
        if rect.is_empty or rect.width < 1 or rect.height < 1:
            continue
        filtered.append(d)

    if not filtered:
        return False

    total_area = sum(fitz.Rect(d.get('rect')).get_area() for d in filtered)
    page_area = page_rect.get_area()
    drawing_ratio = total_area / max(1, page_area)
    return drawing_ratio > 0.005


def _detect_figures_claude(
    page_image: Image.Image,
    claude_client,
    cache: FRQCache,
    dpi: int = 150,
) -> list:
    """
    Use Claude Vision to detect figure bounding boxes.
    Returns list of {"id": N, "bbox": [x1, y1, x2, y2]}.
    """
    import os
    import tempfile

    tmp_fd, tmp_path = tempfile.mkstemp(suffix=".png")
    try:
        os.close(tmp_fd)
        page_image.save(tmp_path, format="PNG")

        cached = cache.get(tmp_path)
        if cached:
            logger.debug("Cache hit for figure detection")
            return cached.get("figures", [])

        with open(tmp_path, "rb") as f:
            img_data = f.read()
        img_b64 = base64.b64encode(img_data).decode("utf-8")

        response = claude_client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/png",
                                "data": img_b64,
                            },
                        },
                        {"type": "text", "text": FIGURE_DETECTION_PROMPT},
                    ],
                }
            ],
        )

        try:
            result = json.loads(response.content[0].text)
        except (json.JSONDecodeError, IndexError, AttributeError):
            logger.warning("Failed to parse Claude response for figure detection")
            return []

        figures = result.get("figures", [])
        cache.put(tmp_path, result)
        return figures

    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


def _bbox_to_fitz_rect(bbox_normalized: list, page_rect: fitz.Rect) -> Optional[fitz.Rect]:
    """Convert normalized [x1, y1, x2, y2] to fitz.Rect in PDF coordinates."""
    if len(bbox_normalized) < 4:
        return None
    x1, y1, x2, y2 = bbox_normalized[:4]
    x1 = max(0.0, min(1.0, float(x1)))
    y1 = max(0.0, min(1.0, float(y1)))
    x2 = max(x1, min(1.0, float(x2)))
    y2 = max(y1, min(1.0, float(y2)))

    pdf_x1 = page_rect.x0 + x1 * page_rect.width
    pdf_y1 = page_rect.y0 + y1 * page_rect.height
    pdf_x2 = page_rect.x0 + x2 * page_rect.width
    pdf_y2 = page_rect.y0 + y2 * page_rect.height

    rect = fitz.Rect(pdf_x1, pdf_y1, pdf_x2, pdf_y2)
    return rect if not rect.is_empty else None


def preprocess_pdf_figures(
    input_pdf: str,
    output_pdf: str,
    figures_dir: str,
    manifest_path: str,
    claude_client,
    cache: Optional[FRQCache] = None,
    dpi: int = 200,
) -> dict:
    """
    Extract vector figures from a PDF, replace with placeholders, save modified PDF.

    Args:
        input_pdf: Path to the aggressive-cleaned PDF
        output_pdf: Path where to save the modified PDF (figures replaced)
        figures_dir: Directory to save extracted PNG figures
        manifest_path: Path where to save the figure manifest JSON
        claude_client: Anthropic client for Claude API calls
        cache: FRQCache instance (optional, for caching Claude responses)
        dpi: Resolution for rendering figure regions

    Returns:
        Manifest dict (also written to manifest_path as JSON)
    """
    if cache is None:
        cache = FRQCache()

    if not _FITZ_AVAILABLE:
        raise ImportError("PyMuPDF is required for figure extraction")

    figures_dir = Path(figures_dir)
    figures_dir.mkdir(parents=True, exist_ok=True)

    session_stem = _extract_session_stem(input_pdf)
    doc = fitz.open(input_pdf)
    manifest = {
        "source_pdf": Path(input_pdf).name,
        "session_stem": session_stem,
        "figures": [],
    }

    global_figure_id = 1
    pages_with_figures = 0

    try:
        for page_index in range(len(doc)):
            page = doc.load_page(page_index)
            page_rect = page.rect

            drawings = page.get_drawings()
            if not _has_candidate_drawings(drawings, page_rect):
                logger.debug(f"Page {page_index}: no candidate drawings, skipping Claude")
                continue

            logger.info(f"Page {page_index}: detected candidate drawings, sending to Claude")
            page_image = render_page(input_pdf, page_index, dpi=150)

            detected_figures = _detect_figures_claude(page_image, claude_client, cache, dpi=150)
            if not detected_figures:
                logger.debug(f"Page {page_index}: Claude found no figures")
                continue

            pages_with_figures += 1
            logger.info(f"Page {page_index}: Claude detected {len(detected_figures)} figures")

            for fig_info in detected_figures:
                fig_bbox = fig_info.get("bbox", [0, 0, 1, 1])
                pdf_rect = _bbox_to_fitz_rect(fig_bbox, page_rect)
                if pdf_rect is None:
                    logger.warning(f"Failed to convert bbox {fig_bbox}")
                    continue

                figure_id = f"{session_stem}_{global_figure_id}"
                figure_filename = f"{session_stem}_p{page_index}_fig{global_figure_id}.png"
                figure_path = figures_dir / figure_filename

                try:
                    zoom = dpi / 72.0
                    pix = page.get_pixmap(clip=pdf_rect, matrix=fitz.Matrix(zoom, zoom), alpha=False)
                    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                    img.save(figure_path, format="PNG")
                    logger.debug(f"Saved figure: {figure_path}")

                    manifest["figures"].append({
                        "id": figure_id,
                        "page_index": page_index,
                        "bbox_normalized": fig_bbox,
                        "image_path": f"figures/{figure_filename}",
                    })

                    global_figure_id += 1

                except Exception as e:
                    logger.error(f"Failed to extract figure at {pdf_rect}: {e}")
                    continue

            # Apply redactions and insert placeholders
            for fig_record in manifest["figures"]:
                if fig_record["page_index"] != page_index:
                    continue

                fig_bbox = fig_record["bbox_normalized"]
                pdf_rect = _bbox_to_fitz_rect(fig_bbox, page_rect)
                if pdf_rect is None:
                    continue

                fig_id = fig_record["id"]
                try:
                    page.add_redact_annot(pdf_rect, fill=(1, 1, 1), text="")
                    page.apply_redactions()
                    placeholder_text = f"[figure {fig_id}]"
                    page.insert_text(
                        fitz.Point(pdf_rect.x0 + 4, pdf_rect.y0 + 14),
                        placeholder_text,
                        fontsize=10,
                        color=(0, 0, 0),
                    )
                    logger.debug(f"Inserted placeholder for {fig_id} on page {page_index}")
                except Exception as e:
                    logger.error(f"Failed to redact/label figure on page {page_index}: {e}")

    finally:
        doc.save(output_pdf, garbage=4, deflate=True)
        doc.close()

    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)

    logger.info(f"Extracted {global_figure_id - 1} figures from {pages_with_figures} pages")
    logger.info(f"Manifest saved to {manifest_path}")

    return manifest
