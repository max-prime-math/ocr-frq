"""
renderer.py — PDF page rendering via PyMuPDF.
"""

import logging
import tempfile
from pathlib import Path

from PIL import Image

logger = logging.getLogger(__name__)

try:
    import fitz  # PyMuPDF
    _FITZ_AVAILABLE = True
except ImportError:
    _FITZ_AVAILABLE = False
    logger.error("PyMuPDF (fitz) not installed — PDF rendering unavailable.")


def render_page(pdf_path: str, page_index: int, dpi: int = 220) -> Image.Image:
    """
    Render one PDF page to a PIL Image in RGB mode.

    Args:
        pdf_path:   Path to the PDF file.
        page_index: 0-based page number.
        dpi:        Render resolution.
    """
    if not _FITZ_AVAILABLE:
        raise ImportError("PyMuPDF is required for PDF rendering. Install pymupdf.")

    doc = fitz.open(pdf_path)
    if page_index >= len(doc):
        raise IndexError(f"Page {page_index} out of range (document has {len(doc)} pages).")

    page = doc.load_page(page_index)
    zoom = dpi / 72.0
    mat = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mat, alpha=False)
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    doc.close()
    return img


def page_count(pdf_path: str) -> int:
    if not _FITZ_AVAILABLE:
        raise ImportError("PyMuPDF is required.")
    doc = fitz.open(pdf_path)
    n = len(doc)
    doc.close()
    return n


def save_temp_image(image: Image.Image) -> str:
    """Save a PIL Image to a temporary PNG file; caller is responsible for deletion."""
    fd, path = tempfile.mkstemp(suffix=".png")
    import os
    os.close(fd)
    image.save(path, format="PNG")
    return path
