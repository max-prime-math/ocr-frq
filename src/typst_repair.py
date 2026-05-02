"""
typst_repair.py — Optional Claude-based repair prompts for Typst output.
"""

from __future__ import annotations

import re
from typing import Callable, Optional


RepairCallback = Callable[[str, str, Optional[str]], Optional[str]]


def _response_text(response) -> str | None:
    for block in getattr(response, "content", []):
        if getattr(block, "type", None) == "text" and getattr(block, "text", None):
            return block.text.strip()
    return None


def _line_context(document: str, validation_error: str, radius: int = 4) -> str:
    match = re.search(r":(\d+):(\d+)", validation_error)
    if not match:
        match = re.search(r"line\s+(\d+)", validation_error, re.IGNORECASE)
    if not match:
        return document[:2000]

    line_no = int(match.group(1))
    lines = document.splitlines()
    start = max(0, line_no - 1 - radius)
    end = min(len(lines), line_no + radius)
    snippet = []
    for idx in range(start, end):
        snippet.append(f"{idx + 1}: {lines[idx]}")
    return "\n".join(snippet)


def make_typst_repair_callback(
    client,
    model: str,
    *,
    enable_span_repair: bool = True,
    enable_document_repair: bool = True,
) -> RepairCallback:
    """Create a callback that repairs suspicious spans or failed Typst documents."""

    span_system = (
        "You repair OCR-extracted AP Calculus text for Typst. "
        "Return only corrected Typst-ready text, with no markdown or explanation. "
        "Preserve meaning exactly and only fix obvious OCR splits, math typos, and malformed Typst syntax."
    )
    document_system = (
        "You repair OCR-generated Typst documents. "
        "Return only the full corrected Typst document, with no markdown or explanation. "
        "Preserve content exactly unless a change is needed to fix the Typst compile error."
    )

    def repair(kind: str, text: str, context: Optional[str]) -> Optional[str]:
        if kind == "span":
            if not enable_span_repair:
                return None
            prompt = "\n".join([
                "Correct this OCR-extracted Typst span.",
                "Return only the corrected text.",
                "",
                "Span:",
                text,
            ])
            response = client.messages.create(
                model=model,
                max_tokens=512,
                system=[{"type": "text", "text": span_system, "cache_control": {"type": "ephemeral"}}],
                messages=[{"role": "user", "content": [{"type": "text", "text": prompt}]}],
            )
            return _response_text(response)

        if kind == "rubric":
            if not enable_span_repair:
                return None
            prompt = "\n".join([
                "Correct this OCR-extracted grading-scheme span for Typst.",
                "Return only the corrected text.",
                "",
                "Span:",
                text,
            ])
            response = client.messages.create(
                model=model,
                max_tokens=512,
                system=[{"type": "text", "text": span_system, "cache_control": {"type": "ephemeral"}}],
                messages=[{"role": "user", "content": [{"type": "text", "text": prompt}]}],
            )
            return _response_text(response)

        if kind == "document":
            if not enable_document_repair:
                return None
            prompt = "\n".join([
                "Typst compile failed on this OCR-generated document.",
                "Fix only what is necessary to make it compile and keep the document content intact.",
                "Return only the full corrected Typst document.",
                "",
                "Compile error:",
                context or "(no context provided)",
                "",
                "Document excerpt:",
                _line_context(text, context or ""),
            ])
            response = client.messages.create(
                model=model,
                max_tokens=2048,
                system=[{"type": "text", "text": document_system, "cache_control": {"type": "ephemeral"}}],
                messages=[{"role": "user", "content": [{"type": "text", "text": prompt}]}],
            )
            return _response_text(response)

        return None

    return repair
