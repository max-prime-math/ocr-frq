"""
figure_extract.py — Figure/diagram extraction from PDF pages.

Ported from ocr-mcq/src/utils.py, adapted for FRQ use case.
Handles PDF-native image extraction, clip rendering, and raster cropping.
"""

import logging
from pathlib import Path
from typing import Optional

from PIL import Image

logger = logging.getLogger(__name__)

try:
    import fitz  # PyMuPDF
    _FITZ_AVAILABLE = True
except ImportError:
    _FITZ_AVAILABLE = False
    logger.error("PyMuPDF (fitz) not installed — figure extraction unavailable.")

try:
    import cv2
    import numpy as np
    _CV2_AVAILABLE = True
except ImportError:
    _CV2_AVAILABLE = False


# ---------------------------------------------------------------------------
# Coordinate conversion
# ---------------------------------------------------------------------------

def _normalise_pdf_rect(raw_rect, page_rect):
    """Convert a raw PDF rect to normalized form, clipped to page bounds."""
    rect = fitz.Rect(raw_rect)
    rect = fitz.Rect(
        min(rect.x0, rect.x1),
        min(rect.y0, rect.y1),
        max(rect.x0, rect.x1),
        max(rect.y0, rect.y1),
    )
    clipped = rect & page_rect
    if clipped.is_empty or clipped.width <= 1 or clipped.height <= 1:
        return None
    return clipped


def _pixel_box_to_pdf_rect(box: tuple[int, int, int, int], image_size: tuple[int, int], page_rect):
    """Convert a pixel bounding box back to PDF coordinates."""
    iw, ih = image_size
    if iw <= 0 or ih <= 0:
        return None
    left, top, right, bottom = box
    sx = page_rect.width / iw
    sy = page_rect.height / ih
    rect = fitz.Rect(left * sx, top * sy, right * sx, bottom * sy)
    return _normalise_pdf_rect(rect, page_rect)


# ---------------------------------------------------------------------------
# PDF clip rendering
# ---------------------------------------------------------------------------

def _render_pdf_clip(page, clip_rect, image_size: tuple[int, int]) -> Optional[Image.Image]:
    """Render a clipped region of a PDF page at high quality."""
    iw, ih = image_size
    if iw <= 0 or ih <= 0:
        return None
    sx = iw / page.rect.width
    sy = ih / page.rect.height
    pix = page.get_pixmap(matrix=fitz.Matrix(sx, sy), clip=clip_rect, alpha=False)
    return Image.frombytes("RGB", [pix.width, pix.height], pix.samples)


# ---------------------------------------------------------------------------
# PDF-native figure extraction
# ---------------------------------------------------------------------------

def _rect_area(rect) -> float:
    """Compute area of a fitz.Rect."""
    return max(0.0, float(rect.width)) * max(0.0, float(rect.height))


def _rect_intersection(a, b) -> float:
    """Compute intersection area of two fitz.Rects."""
    left = max(float(a.x0), float(b.x0))
    top = max(float(a.y0), float(b.y0))
    right = min(float(a.x1), float(b.x1))
    bottom = min(float(a.y1), float(b.y1))
    if right <= left or bottom <= top:
        return 0.0
    return (right - left) * (bottom - top)


def _extract_pdf_figure_crop(
    pdf_path: str,
    page_index: int,
    image_size: tuple[int, int],
    original_box: tuple[int, int, int, int],
    refined_box: tuple[int, int, int, int],
) -> Optional[Image.Image]:
    """
    Try to extract a figure directly from the PDF page's embedded images.

    Returns a PIL Image if a suitable embedded image object is found,
    otherwise None (caller should fall back to raster rendering).
    """
    if not _FITZ_AVAILABLE:
        return None

    doc = fitz.open(pdf_path)
    try:
        if page_index < 0 or page_index >= len(doc):
            return None
        page = doc.load_page(page_index)
        page_rect = page.rect
        preferred_rect = _pixel_box_to_pdf_rect(refined_box, image_size, page_rect)
        source_rect = _pixel_box_to_pdf_rect(original_box, image_size, page_rect)
        if preferred_rect is None or source_rect is None:
            return None

        blocks = page.get_text("dict").get("blocks", [])
        image_rects = []
        min_area = max(64.0, _rect_area(page_rect) * 0.002)
        for block in blocks:
            if block.get("type") != 1:
                continue
            rect = _normalise_pdf_rect(block.get("bbox"), page_rect)
            if rect is None or _rect_area(rect) < min_area:
                continue
            if _rect_intersection(rect, source_rect) <= 0:
                continue
            image_rects.append(rect)

        if not image_rects:
            return None

        def score(rect) -> tuple[float, float, float]:
            inter_pref = _rect_intersection(rect, preferred_rect)
            inter_src = _rect_intersection(rect, source_rect)
            area = _rect_area(rect)
            contains_center = 0.0
            center = fitz.Point(
                (preferred_rect.x0 + preferred_rect.x1) / 2,
                (preferred_rect.y0 + preferred_rect.y1) / 2
            )
            if rect.contains(center):
                contains_center = 1.0
            return (
                inter_pref / max(1.0, _rect_area(preferred_rect)),
                contains_center,
                inter_src / max(1.0, area),
            )

        image_rects.sort(key=score, reverse=True)
        return _render_pdf_clip(page, image_rects[0], image_size)
    finally:
        doc.close()


# ---------------------------------------------------------------------------
# Raster crop refinement and rejection
# ---------------------------------------------------------------------------

def _refine_figure_crop(image: Image.Image, box: tuple[int, int, int, int]) -> tuple[int, int, int, int]:
    """
    Shrink a loose figure box around non-text content.

    Uses OpenCV contour analysis to find the tightest bounding box
    around graphic elements, clustering adjacent graphics and including
    nearby captions. Returns the original box if refinement is ineffective.
    """
    left, top, right, bottom = box
    region = image.crop(box)
    rw, rh = region.size
    if rw < 40 or rh < 40 or not _CV2_AVAILABLE:
        return box

    region_np = np.array(region.convert("L"))
    _, thresh = cv2.threshold(region_np, 235, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    region_area = max(1, rw * rh)
    noise_area = max(18, int(region_area * 0.00003))
    text_height = max(18, int(rh * 0.07))
    text_width = max(140, int(rw * 0.28))
    graphic_area = max(240, int(region_area * 0.0005))
    long_span = max(40, int(max(rw, rh) * 0.12))
    gap = max(18, int(max(rw, rh) * 0.035))
    label_gap = max(12, int(max(rw, rh) * 0.025))

    components: list[dict] = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < noise_area:
            continue
        x, y, w, h = cv2.boundingRect(cnt)
        if w < 3 or h < 3:
            continue

        fill = area / max(1, w * h)
        is_long_rule = (w >= long_span and h <= max(14, int(rh * 0.025))) or (
            h >= long_span and w <= max(14, int(rw * 0.025))
        )
        is_text_like = (
            h <= text_height
            and w <= text_width
            and area <= max(1500, int(region_area * 0.008))
            and fill <= 0.7
            and not is_long_rule
        )
        is_graphic = is_long_rule or area >= graphic_area or w >= long_span or h >= long_span
        components.append({
            "x": x,
            "y": y,
            "w": w,
            "h": h,
            "area": area,
            "fill": fill,
            "text_like": is_text_like,
            "graphic": is_graphic,
        })

    graphic_components = [comp for comp in components if comp["graphic"] and not comp["text_like"]]
    if not graphic_components:
        return box

    graphic_components.sort(key=lambda comp: comp["area"], reverse=True)
    seed = graphic_components[0]
    cluster = [seed]
    x1 = seed["x"]
    y1 = seed["y"]
    x2 = seed["x"] + seed["w"]
    y2 = seed["y"] + seed["h"]

    changed = True
    while changed:
        changed = False
        for comp in graphic_components:
            if comp in cluster:
                continue
            cx1 = comp["x"]
            cy1 = comp["y"]
            cx2 = comp["x"] + comp["w"]
            cy2 = comp["y"] + comp["h"]
            if cx2 < x1 - gap or cx1 > x2 + gap or cy2 < y1 - gap or cy1 > y2 + gap:
                continue
            cluster.append(comp)
            x1 = min(x1, cx1)
            y1 = min(y1, cy1)
            x2 = max(x2, cx2)
            y2 = max(y2, cy2)
            changed = True

    label_candidates = [
        comp for comp in components
        if comp["text_like"]
        and comp["x"] + comp["w"] >= x1 - label_gap
        and comp["x"] <= x2 + label_gap
        and comp["y"] + comp["h"] >= y1 - label_gap
        and comp["y"] <= y2 + label_gap
    ]
    if label_candidates:
        x1 = min([x1] + [comp["x"] for comp in label_candidates])
        y1 = min([y1] + [comp["y"] for comp in label_candidates])
        x2 = max([x2] + [comp["x"] + comp["w"] for comp in label_candidates])
        y2 = max([y2] + [comp["y"] + comp["h"] for comp in label_candidates])

    refined_area = max(1, (x2 - x1) * (y2 - y1))
    original_area = region_area

    # Only accept refinement if it shrinks the area meaningfully.
    if refined_area > original_area * 0.92:
        return box

    pad_x = max(8, int((x2 - x1) * 0.04))
    pad_y = max(8, int((y2 - y1) * 0.04))
    new_left = left + max(0, x1 - pad_x)
    new_top = top + max(0, y1 - pad_y)
    new_right = left + min(rw, x2 + pad_x)
    new_bottom = top + min(rh, y2 + pad_y)

    # Second pass: trim caption text bands below the figure.
    candidate = image.crop((new_left, new_top, new_right, new_bottom))
    cw, ch = candidate.size
    if ch >= 120:
        candidate_np = np.array(candidate.convert("L"))
        ink = candidate_np < 235
        row_density = ink.mean(axis=1)

        bands: list[tuple[int, int, float, float]] = []
        in_band = False
        start = 0
        for i, value in enumerate(row_density):
            if value > 0.01 and not in_band:
                in_band = True
                start = i
            elif value <= 0.01 and in_band:
                end = i - 1
                if end - start >= 3:
                    segment = row_density[start : end + 1]
                    bands.append((start, end, float(segment.mean()), float(segment.max())))
                in_band = False
        if in_band:
            end = ch - 1
            if end - start >= 3:
                segment = row_density[start : end + 1]
                bands.append((start, end, float(segment.mean()), float(segment.max())))

        if len(bands) >= 2:
            last_start, last_end, last_mean, last_max = bands[-1]
            prev_end = bands[-2][1]
            gap_rows = last_start - prev_end - 1
            if (
                last_start >= int(ch * 0.72)
                and gap_rows >= max(14, int(ch * 0.03))
                and last_mean >= 0.05
                and last_max >= 0.15
            ):
                trimmed_bottom = new_top + max(0, last_start - 6)
                if trimmed_bottom - new_top >= int(ch * 0.6):
                    new_bottom = trimmed_bottom

    return new_left, new_top, new_right, new_bottom


def _reject_figure_crop(cropped: Image.Image, page_size: tuple[int, int]) -> bool:
    """
    Return True when a proposed figure crop is obviously low-value.

    Rejects: very small crops, nearly blank crops, and large text-only crops.
    """
    cw, ch = cropped.size
    pw, ph = page_size
    if cw < 40 or ch < 40:
        return True

    if not _CV2_AVAILABLE:
        return False

    gray = np.array(cropped.convert("L"))
    ink = gray < 245
    ink_ratio = float(ink.mean())
    if ink_ratio < 0.003:
        return True

    crop_area = cw * ch
    page_area = max(1, pw * ph)
    if crop_area > page_area * 0.2 and ink_ratio < 0.05:
        return True

    _, thresh = cv2.threshold(gray, 235, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    text_like = 0
    graphic_like = 0
    text_height = max(18, int(ch * 0.08))
    text_width = max(120, int(cw * 0.35))
    long_span = max(36, int(max(cw, ch) * 0.12))
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area <= 8:
            continue
        x, y, w, h = cv2.boundingRect(cnt)
        fill = area / max(1, w * h)
        is_long_rule = (w >= long_span and h <= max(14, int(ch * 0.03))) or (
            h >= long_span and w <= max(14, int(cw * 0.03))
        )
        is_text_like = (
            h <= text_height
            and w <= text_width
            and area <= max(1500, int(crop_area * 0.008))
            and fill <= 0.72
            and not is_long_rule
        )
        if is_text_like:
            text_like += 1
        elif is_long_rule or area > max(300, crop_area * 0.01) or w >= long_span or h >= long_span:
            graphic_like += 1

    # Reject text-only crops.
    if graphic_like == 0 and text_like > 0:
        return True

    return False


# ---------------------------------------------------------------------------
# Main materialisation
# ---------------------------------------------------------------------------

def materialise_figures(
    figures: list[dict],
    page_image: Image.Image,
    pdf_path: str,
    page_index: int,
    output_dir: str,
    stem: str,
    question_number: Optional[int] = None,
) -> list[dict]:
    """
    Crop and save figure bounding boxes from a page.

    Args:
        figures:       List of figure dicts from Claude extraction
                      (with normalized x, y, width, height in [0,1] space).
        page_image:    PIL Image of the rendered PDF page.
        pdf_path:      Path to the source PDF file.
        page_index:    0-based page index in the PDF.
        output_dir:    Directory where to save cropped figure PNGs.
        stem:          Base filename stem (e.g., 'SG-BC-2009').
        question_number: Optional question number for naming.

    Returns:
        List of figure dicts with added "file_path" field (e.g., "figures/SG-BC-2009_q3_fig_1.png").
    """
    out: list[dict] = []
    base_dir = Path(output_dir)
    base_dir.mkdir(parents=True, exist_ok=True)

    if not figures:
        return out

    w, h = page_image.size
    for idx, fig in enumerate(figures, start=1):
        x = max(0.0, min(1.0, float(fig.get("x", 0.0))))
        y = max(0.0, min(1.0, float(fig.get("y", 0.0))))
        width = max(0.0, min(1.0 - x, float(fig.get("width", 0.0))))
        height = max(0.0, min(1.0 - y, float(fig.get("height", 0.0))))

        if width <= 0 or height <= 0:
            logger.warning("Skipping zero-sized figure crop: %s", fig)
            continue

        left = int(w * x)
        top = int(h * y)
        right = int(w * (x + width))
        bottom = int(h * (y + height))
        original_box = (left, top, right, bottom)
        refined_box = _refine_figure_crop(page_image, original_box)

        # Try PDF-native extraction first (highest quality).
        cropped = _extract_pdf_figure_crop(pdf_path, page_index, page_image.size, original_box, refined_box)

        # Fall back to raster crop.
        if cropped is None:
            cropped = page_image.crop(refined_box)

        # Reject low-value crops.
        if _reject_figure_crop(cropped, page_image.size):
            logger.warning("Rejecting low-value figure crop: %s", fig)
            continue

        # Generate filename.
        if question_number is not None:
            filename = f"{stem}_q{question_number}_fig_{idx}.png"
        else:
            filename = f"{stem}_p{page_index}_fig_{idx}.png"

        path = base_dir / filename
        cropped.save(path, format="PNG")
        logger.debug("Saved figure: %s", path)

        # Return updated figure dict with file path.
        result = dict(fig)
        result["file_path"] = f"figures/{filename}"
        out.append(result)

    return out
