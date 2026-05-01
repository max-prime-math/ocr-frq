"""
latex_writer.py — Render extracted FRQ data as LaTeX.

Adapted from ocr-mcq's latex_writer.py with FRQ-specific rendering.
Produces a standalone article-class document with clearly separated
question, solution, and grading scheme sections.
"""

import logging
import re
from pathlib import Path
from typing import Optional

from models import FRQExtraction

logger = logging.getLogger(__name__)

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

_INTERVAL_ATOM = r"(?:-?(?:\d+(?:\.\d+)?|\\infty))"
_INTERVAL_PATTERN = re.compile(
    rf"(?<!\\)((?:[\(\[]\s*{_INTERVAL_ATOM}\s*,\s*{_INTERVAL_ATOM}\s*[\)\]])(?:\s+and\s+[\(\[]\s*{_INTERVAL_ATOM}\s*,\s*{_INTERVAL_ATOM}\s*[\)\]])*(?:\s+only)?)"
)
_RANGE_PATTERN = re.compile(
    r"(?<!\\)("
    r"(?:-?\d+(?:\.\d+)?)\s*(?:<=|>=|\\leq?|\\geq?)\s*[A-Za-z]\s*(?:<=|>=|\\leq?|\\geq?)\s*(?:-?\d+(?:\.\d+)?)"
    r"(?:\s+and\s+(?:-?\d+(?:\.\d+)?)\s*(?:<=|>=|\\leq?|\\geq?)\s*[A-Za-z]\s*(?:<=|>=|\\leq?|\\geq?)\s*(?:-?\d+(?:\.\d+)?))*"
    r")"
)
_INLINE_EQUATION_PATTERN = re.compile(
    r"(?<![A-Za-z\\])("
    r"(?:[A-Za-z](?:\([A-Za-z0-9,+\-*/^_{}\s]*\))?(?:_[A-Za-z0-9{}]+)?(?:\^[A-Za-z0-9{}]+)?)"
    r"\s*=\s*"
    r"[A-Za-z0-9\\{}_^()+\-*/\s]+"
    r")"
)
_COMMAND_MATH_PATTERN = re.compile(
    r"("
    r"\\(?:int|iint|iiint|sum|prod|lim|frac|dfrac|tfrac|sqrt|sin|cos|tan|cot|sec|csc|ln|log|exp|Rightarrow)"
    r"(?:\\.|[^?.!,;:])*"
    r")"
)
_MATH_ENVIRONMENTS = ("array", "cases", "matrix", "pmatrix", "bmatrix", "vmatrix", "Vmatrix")

_PREAMBLE = r"""\documentclass[12pt]{article}
\usepackage[margin=1in]{geometry}
\usepackage{amsmath,amssymb,amsfonts}
\usepackage{enumitem}
\usepackage{xcolor}
\usepackage{mdframed}
\usepackage{graphicx}

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

_POSTAMBLE = r"""
\end{document}
"""


def _escape_percent(text: str) -> str:
    return re.sub(r"(?<!\\)%", r"\\%", text)


def _strip_control_chars(text: str) -> str:
    return "".join(ch for ch in text if ch in "\n\r\t" or ord(ch) >= 32)


def _normalise_unicode_math(text: str) -> str:
    repaired = _strip_control_chars(text)
    for src, dst in _UNICODE_MATH_REPLACEMENTS.items():
        repaired = repaired.replace(src, dst)
    repaired = re.sub(r"(?<![A-Za-z\\])(?:bigint|igint)(?=\s*_)", r"\\int", repaired)
    repaired = _normalise_mixed_math_delimiters(repaired)
    return repaired


def _normalise_mixed_math_delimiters(text: str) -> str:
    repaired = text
    repaired = repaired.replace(r"\left(\(", r"\left(")
    repaired = repaired.replace(r"\left[\(", r"\left[")
    repaired = repaired.replace(r"\left\{\(", r"\left\{")
    repaired = repaired.replace(r"\left(\[", r"\left(")
    repaired = repaired.replace(r"\left[\[", r"\left[")
    repaired = repaired.replace(r"\)\right)", r"\right)")
    repaired = repaired.replace(r"\)\right]", r"\right]")
    repaired = repaired.replace(r"\)\right\}", r"\right\}")
    repaired = repaired.replace(r"\]\right)", r"\right)")
    repaired = repaired.replace(r"\]\right]", r"\right]")
    return repaired


def _count_unescaped_dollars(text: str) -> int:
    return len(re.findall(r"(?<!\\)\$", text))


def _normalise_dollar_runs(text: str) -> str:
    def repl(match: re.Match[str]) -> str:
        count = len(match.group(0))
        return "$$" if count % 2 == 0 else "$"

    return re.sub(r"(?<!\\)\${2,}", repl, text)


def _repair_math_content(text: str) -> str:
    repaired = text
    repaired = repaired.replace(r"\(", "")
    repaired = repaired.replace(r"\)", "")
    repaired = repaired.replace(r"\[", "")
    repaired = repaired.replace(r"\]", "")
    repaired = re.sub(r"\\([()\[\]])", "", repaired)
    repaired = repaired.replace("$$", "")
    repaired = re.sub(r"\\([)\]])(?=!)", "", repaired)
    return repaired


def _repair_protected_math(text: str) -> str:
    def repl(match: re.Match[str]) -> str:
        block = match.group(0)
        if block.startswith(r"\(") and block.endswith(r"\)"):
            return rf"\({_repair_math_content(block[2:-2])}\)"
        if block.startswith(r"\[") and block.endswith(r"\]"):
            return rf"\[{_repair_math_content(block[2:-2])}\]"
        if block.startswith("$$") and block.endswith("$$"):
            return f"$${_repair_math_content(block[2:-2])}$$"
        if block.startswith("$") and block.endswith("$"):
            return f"${_repair_math_content(block[1:-1])}$"
        return block

    return _PROTECTED_MATH_PATTERN.sub(repl, text)


def _dedupe_math_delimiters(text: str) -> str:
    repaired = text
    while r"\(\(" in repaired:
        repaired = repaired.replace(r"\(\(", r"\(")
    while r"\)\)" in repaired:
        repaired = repaired.replace(r"\)\)", r"\)")
    while r"\[\[" in repaired:
        repaired = repaired.replace(r"\[\[", r"\[")
    while r"\]\]" in repaired:
        repaired = repaired.replace(r"\]\]", r"\]")
    repaired = re.sub(r"(\\\(.+?\\\))\\\)", r"\1", repaired)
    repaired = re.sub(r"(\\\[.+?\\\])\\\]", r"\1", repaired)
    return repaired


def _wrap_inline_math(match: re.Match[str]) -> str:
    text = match.group(1).strip()
    return rf"\({text}\)"


def _wrap_math_environment_block(text: str) -> str | None:
    stripped = text.strip()
    for env in _MATH_ENVIRONMENTS:
        begin = rf"\begin{{{env}}}"
        end = rf"\end{{{env}}}"
        if stripped.startswith(begin) and stripped.endswith(end):
            return rf"\[{stripped}\]"
    return None


def _wrap_bare_math_spans(text: str) -> str:
    parts: list[str] = []
    last = 0
    for match in _PROTECTED_MATH_PATTERN.finditer(text):
        plain = text[last:match.start()]
        plain = _INTERVAL_PATTERN.sub(_wrap_inline_math, plain)
        plain = _RANGE_PATTERN.sub(_wrap_inline_math, plain)
        plain = _INLINE_EQUATION_PATTERN.sub(_wrap_inline_math, plain)
        plain = _COMMAND_MATH_PATTERN.sub(_wrap_inline_math, plain)
        parts.append(plain)
        parts.append(match.group(0))
        last = match.end()

    tail = text[last:]
    tail = _INTERVAL_PATTERN.sub(_wrap_inline_math, tail)
    tail = _RANGE_PATTERN.sub(_wrap_inline_math, tail)
    tail = _INLINE_EQUATION_PATTERN.sub(_wrap_inline_math, tail)
    tail = _COMMAND_MATH_PATTERN.sub(_wrap_inline_math, tail)
    parts.append(tail)
    return "".join(parts)


def _balance_delimited_math(text: str) -> str:
    repaired = text

    paren_open = repaired.count(r"\(")
    paren_close = repaired.count(r"\)")
    if paren_open > paren_close:
        repaired += r"\)" * (paren_open - paren_close)

    bracket_open = repaired.count(r"\[")
    bracket_close = repaired.count(r"\]")
    if bracket_open > bracket_close:
        repaired += r"\]" * (bracket_open - bracket_close)

    dollar_count = _count_unescaped_dollars(repaired)
    if dollar_count % 2 == 1:
        repaired += "$"

    return repaired


def _looks_like_bare_math(text: str) -> bool:
    stripped = text.strip()
    if not stripped:
        return False
    if any(token in stripped for token in (r"\(", r"\[", "$$", "$")):
        return False
    if len(stripped.split()) > 4 and not any(ch in stripped for ch in "=+-*/^_[]{}()\\"):
        return False

    import re
    if re.fullmatch(r"[A-Za-z0-9\\\^_{}\[\]()+\-*/=<>|.,'` :]+", stripped) is None:
        return False

    return any(
        (
            re.search(r"[=^_]", stripped),
            re.search(r"[A-Za-z]\(", stripped),
            re.search(r"\\[A-Za-z]+", stripped),
            re.search(r"\[[^\]]+\]", stripped),
            re.search(r"\d", stripped) and re.search(r"[A-Za-z]", stripped),
        )
    )


def _render_text(text: str) -> str:
    env_block = _wrap_math_environment_block(text)
    if env_block is not None:
        return env_block

    cleaned = _normalise_unicode_math(text)
    cleaned = _normalise_dollar_runs(cleaned)
    cleaned = _balance_delimited_math(_escape_percent(cleaned))
    cleaned = _repair_protected_math(cleaned)
    cleaned = _wrap_bare_math_spans(cleaned)
    cleaned = _repair_protected_math(cleaned)
    cleaned = _normalise_mixed_math_delimiters(cleaned)
    cleaned = _dedupe_math_delimiters(cleaned)
    cleaned = _balance_delimited_math(cleaned)
    if _looks_like_bare_math(cleaned):
        return rf"\({cleaned}\)"
    return cleaned


def _render_figures(lines: list[str], figures: list[dict]) -> None:
    for fig in figures:
        file_path = fig.get("file_path")
        if not file_path:
            continue
        lines.append(r"\begin{center}")
        lines.append(rf"\includegraphics[width=0.65\linewidth]{{{file_path}}}")
        lines.append(r"\end{center}")


def _render_tables(lines: list[str], tables: list[dict]) -> None:
    for table in tables:
        headers = table.get("headers", [])
        rows = table.get("rows", [])
        col_count = 0
        for row in [headers] + rows:
            col_count = max(col_count, len(row))
        col_count = max(1, col_count)

        lines.append(r"\begin{center}")
        lines.append(rf"\begin{{tabular}}{{{'l' * col_count}}}")
        lines.append(r"\hline")

        if headers:
            line_parts = [_render_text(cell) for cell in headers]
            lines.append(" & ".join(line_parts) + r" \\")
            lines.append(r"\hline")

        for row in rows:
            padded = row + [""] * (col_count - len(row))
            line_parts = [_render_text(cell) for cell in padded]
            lines.append(" & ".join(line_parts) + r" \\")

        lines.append(r"\hline")
        lines.append(r"\end{tabular}")
        lines.append(r"\end{center}")


def _by_section(items: list[dict], section: str) -> list[dict]:
    return [item for item in items if item.get("section") == section]


def render_frq_block(extraction: FRQExtraction, source: Optional[str] = None) -> str:
    """
    Render one FRQ extraction as a LaTeX block.

    Args:
        extraction: FRQExtraction dict with question/solution/grading_scheme.
        source:     Optional label (e.g. filename + page) added as a comment.

    Returns:
        Multi-line LaTeX string (no trailing newline).
    """
    lines: list[str] = []

    qnum = extraction.get("question_number")
    heading = f"Question {qnum}" if qnum is not None else "Question"
    lines.append(rf"\section*{{{heading}}}")

    if source:
        lines.append(f"% {source}")

    meta = []
    unit = extraction.get("unit")
    if unit:
        meta.append(f"\\textit{{{unit}}}")
    section = extraction.get("section")
    if section:
        meta.append(f"\\textit{{{section}}}")
    calculator = extraction.get("calculator")
    if calculator:
        meta.append(f"\\textit{{{calculator}}}")
    if meta:
        lines.append(" \\\\[6pt] ".join(meta))
        lines.append(r"\\[6pt]")

    if extraction.get("flagged"):
        reason = extraction.get("flag_reason") or "low confidence"
        lines.append(rf"\textbf{{\textcolor{{red}}{{[Flagged for review: {reason}]}}}} \\")
        lines.append("")

    figures = extraction.get("figures") or []
    tables = extraction.get("tables") or []
    question_figures = _by_section(figures, "question")
    solution_figures = _by_section(figures, "solution")
    rubric_figures = _by_section(figures, "grading_scheme")
    question_tables = _by_section(tables, "question")
    solution_tables = _by_section(tables, "solution")
    rubric_tables = _by_section(tables, "grading_scheme")

    question = extraction.get("question") or ""
    lines.append(_render_text(question) if question else r"\textit{[Question text not extracted]}")
    _render_tables(lines, question_tables)
    _render_figures(lines, question_figures)

    lines.append("")
    lines.append(r"\begin{frqsolution}")
    solution = extraction.get("solution") or ""
    lines.append(_render_text(solution) if solution else r"\textit{[Solution not extracted]}")
    _render_tables(lines, solution_tables)
    _render_figures(lines, solution_figures)
    lines.append(r"\end{frqsolution}")

    lines.append("")
    lines.append(r"\begin{frqrubric}")
    rubric = extraction.get("grading_scheme") or ""
    lines.append(_render_text(rubric) if rubric else r"\textit{[Grading scheme not extracted]}")
    _render_tables(lines, rubric_tables)
    _render_figures(lines, rubric_figures)
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

    Args:
        page_results:             List of PageResult dicts from extraction.
        include_skipped_comments: Whether to include % comments for skipped pages.

    Returns:
        Complete LaTeX document string.
    """
    blocks: list[str] = []

    for result in page_results:
        if result.get("error"):
            blocks.append(f"% Error on page {result['page'] + 1}: {result['error']}\n")
            continue

        extraction: Optional[dict] = result.get("extraction")
        if extraction is None:
            continue

        if extraction["page_type"] == "skip":
            if include_skipped_comments:
                reason = extraction.get("skip_reason") or "unknown"
                blocks.append(f"% Page {result['page'] + 1} skipped: {reason}")
            continue

        fname = result.get("fname", "")
        source = f"{fname} p{result['page'] + 1}" if fname else f"p{result['page'] + 1}"
        blocks.append(render_frq_block(extraction, source=source))
        blocks.append(r"\bigskip\hrule\bigskip")

    body = "\n\n".join(blocks)
    return _PREAMBLE + body + "\n" + _POSTAMBLE


def write_tex_file(
    page_results: list[dict],
    output_path: str,
    include_skipped_comments: bool = True,
) -> None:
    """
    Write a complete LaTeX .tex file for *page_results*.

    Args:
        page_results:             List of PageResult dicts from extraction.
        output_path:              Destination file path (created/overwritten).
        include_skipped_comments: Whether to include % comments for skipped pages.
    """
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    content = build_document(page_results, include_skipped_comments)

    with open(output_path, "w", encoding="utf-8") as fh:
        fh.write(content)

    logger.info("Wrote LaTeX to %s", output_path)
