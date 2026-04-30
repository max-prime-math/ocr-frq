"""
typst_gen.py — Render extracted FRQ data as a Typst document.

Produces a standalone Typst document with clearly separated
question, solution, and grading scheme sections for each FRQ page.
"""

import logging
from typing import Optional

from models import FRQExtraction

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Text helpers
# ---------------------------------------------------------------------------

def _strip_control_chars(text: str) -> str:
    return "".join(ch for ch in text if ch in "\n\r\t" or ord(ch) >= 32)


def _convert_newlines(text: str) -> str:
    """Turn single newlines into Typst forced line breaks; keep paragraph breaks."""
    placeholder = "\x00PARA\x00"
    text = text.replace("\n\n", placeholder)
    text = text.replace("\n", "\\\n")
    text = text.replace(placeholder, "\n\n")
    return text


def render_text(text: str) -> str:
    """Prepare extracted text for embedding in a Typst content block."""
    t = _strip_control_chars(text)
    t = _convert_newlines(t)
    return t


# ---------------------------------------------------------------------------
# Document structure
# ---------------------------------------------------------------------------

# The \\ in Python string literals → single \ in the output, which Typst
# treats as a forced line break when it appears at the end of a line.
_PREAMBLE = """\
#set document(title: "AP Exam Scoring Guidelines")
#set page(paper: "us-letter", margin: (x: 2.5cm, y: 2.5cm))
#set text(size: 11pt)
#set par(justify: true)

#let solution-block(body) = block(
  width: 100%,
  fill: rgb("#f0faf0"),
  stroke: (left: 3pt + rgb("#2e7d32")),
  inset: (x: 10pt, y: 8pt),
  radius: (right: 3pt),
)[
  *Solution* \\
  #body
]

#let rubric-block(body) = block(
  width: 100%,
  fill: rgb("#f0f0fa"),
  stroke: (left: 3pt + rgb("#1565c0")),
  inset: (x: 10pt, y: 8pt),
  radius: (right: 3pt),
)[
  *Grading Scheme* \\
  #body
]

"""


def render_frq_block(extraction: FRQExtraction, source: Optional[str] = None) -> str:
    """Render one FRQ extraction as a Typst block. Returns a multi-line string."""
    lines: list[str] = []

    qnum = extraction.get("question_number")
    heading = f"Question {qnum}" if qnum is not None else "Question"
    lines.append(f"= {heading}")
    lines.append("")

    if source:
        lines.append(f"// {source}")
        lines.append("")

    if extraction.get("flagged"):
        reason = extraction.get("flag_reason") or "low confidence"
        lines.append(f"#text(fill: red.darken(20%))[*⚠ Flagged for review: {reason}*]")
        lines.append("")

    question = extraction.get("question") or ""
    lines.append(render_text(question) if question else "_[Question text not extracted]_")
    lines.append("")

    solution = extraction.get("solution") or ""
    solution_body = render_text(solution) if solution else "_[Solution not extracted]_"
    lines.append("#solution-block[")
    lines.append(solution_body)
    lines.append("]")
    lines.append("")

    rubric = extraction.get("grading_scheme") or ""
    rubric_body = render_text(rubric) if rubric else "_[Grading scheme not extracted]_"
    lines.append("#rubric-block[")
    lines.append(rubric_body)
    lines.append("]")

    return "\n".join(lines)


def build_document(
    page_results: list[dict],
    include_skipped_comments: bool = True,
) -> str:
    """
    Build a complete Typst document from a list of PageResult dicts.

    Only pages with page_type == "frq" produce content blocks.
    Skipped pages appear as comments if include_skipped_comments is True.
    """
    blocks: list[str] = []

    for r in page_results:
        if r.get("error"):
            blocks.append(f"// Error on page {r['page'] + 1}: {r['error']}")
            continue

        extraction: Optional[dict] = r.get("extraction")
        if extraction is None:
            continue

        if extraction["page_type"] == "skip":
            if include_skipped_comments:
                reason = extraction.get("skip_reason") or "unknown"
                blocks.append(f"// Page {r['page'] + 1} skipped: {reason}")
            continue

        fname = r.get("fname", "")
        source = f"{fname} p{r['page'] + 1}" if fname else f"p{r['page'] + 1}"
        blocks.append(render_frq_block(extraction, source=source))
        blocks.append("#line(length: 100%, stroke: 0.5pt)\n\n#v(12pt)")

    body = "\n\n".join(blocks)
    return _PREAMBLE + body + "\n"
