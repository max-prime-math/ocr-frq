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


def _clean_math_spans(text: str) -> str:
    r"""
    Clean up math notation inside $...$ spans and promote complex math to display mode.

    - Removes LaTeX-specific syntax (\cdot, stray backslashes, etc.)
    - Fixes Typst-specific issues (e^{x} → e^x, implicit multiplication)
    - Promotes fractions, integrals, sums, products, and limits to display mode
    """
    import re

    # Known Typst math words that should not have backslashes
    typst_math = {
        "alpha", "beta", "gamma", "delta", "epsilon", "zeta", "eta", "theta", "iota", "kappa",
        "lambda", "mu", "nu", "xi", "omicron", "pi", "rho", "sigma", "tau", "upsilon",
        "phi", "chi", "psi", "omega", "sqrt", "integral", "sum", "product", "lim", "sin",
        "cos", "tan", "log", "ln", "exp", "abs", "floor", "ceil", "dif", "dot", "times",
    }

    def clean_span(match):
        span = match.group(0)
        # Replace LaTeX-style multiplication and other symbols
        span = span.replace(r"\cdot", "dot")
        span = span.replace(r"\times", "times")
        span = span.replace(r"\div", "div")

        # Strip backslashes before Typst math words
        for word in typst_math:
            span = span.replace(f"\\{word}", word)

        # Fix e^{x} → e^x (Typst doesn't need curly braces for single-character exponents)
        span = re.sub(r'(\^)\{([a-zA-Z0-9])\}', r'\1\2', span)

        # Fix implicit multiplication patterns: ft -> f(t), kx -> k x, kx^2 -> k x^2, etc.
        # Be conservative: only fix patterns we're confident about
        # Pattern 1: single letter followed by (lowercase letter) = function call -> f(x), g(t)
        span = re.sub(r'\b([a-z])([a-z])\b', lambda m: f"{m.group(1)}({m.group(2)})" if m.group(1) in "fghijklmnpqrstu" else m.group(0), span)
        # Pattern 2: digit or constant followed by letter at word boundary: k x, 2 x, etc.
        # But only for single-letter constants before single-letter variables
        span = re.sub(r'([a-z])([A-Z]+)(\^|\s|$)', r"\1 \2\3", span)  # k X^2 -> k X^2 (already has space)
        # Pattern 3: specific problematic cases: kx^2 -> k x^2 (when not already spaced)
        span = re.sub(r'([a-z])([a-z]\^)', lambda m: f"{m.group(1)} {m.group(2)}", span)

        return span

    def should_use_display_mode(span: str) -> bool:
        """Check if math expression should be rendered in display mode."""
        # Trigger on fractions, integrals, sums, products, limits
        return any(keyword in span for keyword in ["/", "integral", "sum", "product", "lim"])

    # Find and clean all $...$ and $ ... $ spans
    # This regex finds either $...$ or $ ... $ (with spaces), non-greedy
    def replace_math(match):
        full_match = match.group(0)
        inner = match.group(1)
        cleaned = clean_span(inner)

        # Decide on display mode
        if should_use_display_mode(cleaned):
            # Use aligned display mode (centered)
            return f"#align(center)[$ {cleaned} $]"
        else:
            # Keep as inline math
            return f"${cleaned}$"

    result = re.sub(r'\$\s*(.*?)\s*\$', replace_math, text)
    return result


def render_text(text: str) -> str:
    """Prepare extracted text for embedding in a Typst content block."""
    t = _strip_control_chars(text)
    t = _clean_math_spans(t)
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

    figures = extraction.get("figures") or []
    for fig in figures:
        if fig.get("section") == "question":
            caption = fig.get("caption") or ""
            file_path = fig.get("file_path", "")
            if file_path:
                lines.append(f"#figure(")
                lines.append(f'  image("{file_path}", width: 80%),')
                if caption:
                    lines.append(f'  caption: [{caption}],')
                lines.append(f")")
                lines.append("")

    solution = extraction.get("solution") or ""
    solution_body = render_text(solution) if solution else "_[Solution not extracted]_"
    lines.append("#solution-block[")
    lines.append(solution_body)
    for fig in figures:
        if fig.get("section") == "solution":
            caption = fig.get("caption") or ""
            file_path = fig.get("file_path", "")
            if file_path:
                lines.append("")
                lines.append(f"#figure(")
                lines.append(f'  image("{file_path}", width: 80%),')
                if caption:
                    lines.append(f'  caption: [{caption}],')
                lines.append(f")")
    lines.append("]")
    lines.append("")

    rubric = extraction.get("grading_scheme") or ""
    rubric_body = render_text(rubric) if rubric else "_[Grading scheme not extracted]_"
    lines.append("#rubric-block[")
    lines.append(rubric_body)
    for fig in figures:
        if fig.get("section") == "grading_scheme":
            caption = fig.get("caption") or ""
            file_path = fig.get("file_path", "")
            if file_path:
                lines.append("")
                lines.append(f"#figure(")
                lines.append(f'  image("{file_path}", width: 80%),')
                if caption:
                    lines.append(f'  caption: [{caption}],')
                lines.append(f")")
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
