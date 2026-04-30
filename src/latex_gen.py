"""
latex_gen.py — Render extracted FRQ data as LaTeX.

Produces a standalone article-class document with clearly separated
question, solution, and grading scheme sections for each FRQ page.
"""

import logging
import re
from typing import Optional

from models import FRQExtraction

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Math text normalisation (ported from MCQ app's latex_writer.py)
# ---------------------------------------------------------------------------

_UNICODE_MATH_REPLACEMENTS = {
    "−": "-",
    "∞": r"\infty",
    "≤": r"\le",
    "≥": r"\ge",
    "≈": r"\approx",
    "≠": r"\ne",
    "×": r"\times",
}

_PROTECTED_MATH_PATTERN = re.compile(
    r"(\\\(.+?\\\)|\\\[.+?\\\]|\$\$.+?\$\$|(?<!\\)\$.+?(?<!\\)\$)",
    re.DOTALL,
)


def _strip_control_chars(text: str) -> str:
    return "".join(ch for ch in text if ch in "\n\r\t" or ord(ch) >= 32)


def _escape_percent(text: str) -> str:
    return re.sub(r"(?<!\\)%", r"\\%", text)


def _normalise_unicode_math(text: str) -> str:
    t = _strip_control_chars(text)
    for src, dst in _UNICODE_MATH_REPLACEMENTS.items():
        t = t.replace(src, dst)
    return t


def _count_unescaped_dollars(text: str) -> int:
    return len(re.findall(r"(?<!\\)\$", text))


def _balance_delimited_math(text: str) -> str:
    t = text
    paren_open = t.count(r"\(")
    paren_close = t.count(r"\)")
    if paren_open > paren_close:
        t += r"\)" * (paren_open - paren_close)
    bracket_open = t.count(r"\[")
    bracket_close = t.count(r"\]")
    if bracket_open > bracket_close:
        t += r"\]" * (bracket_open - bracket_close)
    if _count_unescaped_dollars(t) % 2 == 1:
        t += "$"
    return t


def _dedupe_math_delimiters(text: str) -> str:
    t = text
    while r"\(\(" in t:
        t = t.replace(r"\(\(", r"\(")
    while r"\)\)" in t:
        t = t.replace(r"\)\)", r"\)")
    while r"\[\[" in t:
        t = t.replace(r"\[\[", r"\[")
    while r"\]\]" in t:
        t = t.replace(r"\]\]", r"\]")
    return t


def render_text(text: str) -> str:
    """Normalise math delimiters and unicode in a LaTeX text field."""
    t = _normalise_unicode_math(text)
    t = _escape_percent(t)
    t = _balance_delimited_math(t)
    t = _dedupe_math_delimiters(t)
    return t


# ---------------------------------------------------------------------------
# Document structure
# ---------------------------------------------------------------------------

_PREAMBLE = r"""\documentclass[12pt]{article}
\usepackage[margin=1in]{geometry}
\usepackage{amsmath,amssymb,amsfonts}
\usepackage{enumitem}
\usepackage{titlesec}
\usepackage{xcolor}
\usepackage{mdframed}

\definecolor{solutionbg}{rgb}{0.95,0.98,0.95}
\definecolor{rubricbg}{rgb}{0.95,0.95,1.00}

\newenvironment{frqsolution}{%
  \begin{mdframed}[backgroundcolor=solutionbg,linecolor=green!50!black,linewidth=0.8pt]
  \textbf{Solution}\par\smallskip
}{%
  \end{mdframed}
}

\newenvironment{frqrubric}{%
  \begin{mdframed}[backgroundcolor=rubricbg,linecolor=blue!60!black,linewidth=0.8pt]
  \textbf{Grading Scheme}\par\smallskip
}{%
  \end{mdframed}
}

\begin{document}
"""

_POSTAMBLE = r"\end{document}" + "\n"

_SKIPPED_PAGE_COMMENT = "% Page skipped: {reason} (page {page})\n"


def render_frq_block(extraction: FRQExtraction, source: Optional[str] = None) -> str:
    """
    Render one FRQ extraction as a LaTeX block.

    Returns a multi-line string (no trailing newline).
    """
    lines: list[str] = []

    qnum = extraction.get("question_number")
    heading = f"Question {qnum}" if qnum is not None else "Question"
    lines.append(rf"\section*{{{heading}}}")

    if source:
        lines.append(f"% {source}")

    if extraction.get("flagged"):
        reason = extraction.get("flag_reason") or "low confidence"
        lines.append(rf"\textbf{{\textcolor{{red}}{{[Flagged for review: {reason}]}}}} \\")

    question = extraction.get("question") or ""
    lines.append(render_text(question) if question else r"\textit{[Question text not extracted]}")

    lines.append("")
    solution = extraction.get("solution") or ""
    lines.append(r"\begin{frqsolution}")
    lines.append(render_text(solution) if solution else r"\textit{[Solution not extracted]}")
    lines.append(r"\end{frqsolution}")

    lines.append("")
    rubric = extraction.get("grading_scheme") or ""
    lines.append(r"\begin{frqrubric}")
    lines.append(render_text(rubric) if rubric else r"\textit{[Grading scheme not extracted]}")
    lines.append(r"\end{frqrubric}")

    return "\n".join(lines)


def build_document(
    page_results: list[dict],
    include_skipped_comments: bool = True,
) -> str:
    """
    Build a complete LaTeX document from a list of PageResult dicts.

    Only pages with page_type == "frq" produce content blocks.
    Skipped pages appear as comments if include_skipped_comments is True.
    """
    blocks: list[str] = []

    for r in page_results:
        if r.get("error"):
            blocks.append(f"% Error on page {r['page'] + 1}: {r['error']}\n")
            continue

        extraction: Optional[dict] = r.get("extraction")
        if extraction is None:
            continue

        if extraction["page_type"] == "skip":
            if include_skipped_comments:
                reason = extraction.get("skip_reason") or "unknown"
                blocks.append(
                    _SKIPPED_PAGE_COMMENT.format(reason=reason, page=r["page"] + 1)
                )
            continue

        fname = r.get("fname", "")
        source = f"{fname} p{r['page'] + 1}" if fname else f"p{r['page'] + 1}"
        blocks.append(render_frq_block(extraction, source=source))
        blocks.append(r"\bigskip\hrule\bigskip" + "\n")

    body = "\n\n".join(blocks)
    return _PREAMBLE + body + "\n" + _POSTAMBLE
