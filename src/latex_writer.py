"""
latex_writer.py — Render QuestionBlock records as exam-class LaTeX.

Document structure:
  \\section*{YEAR AP Calculus BC [Form B]}
  \\begin{questions}
  \\question
  % Q1 | YEAR Calculus BC | Part A | Calculator Active
  question intro...
  \\begin{parts}
  \\part sub-part (a)...
  \\end{parts}
  \\begin{solution}
  (combined solution + rubric from SG)
  \\end{solution}
  ...
  \\end{questions}

Metadata comment goes UNDER \\question (not above it).
"""

from __future__ import annotations

import re
from pathlib import Path

from .contracts import QuestionBlock


# ── document preamble / postamble ─────────────────────────────────────────────

_PREAMBLE = r"""\documentclass[12pt,addpoints,answers]{exam}
\usepackage[margin=1in]{geometry}
\usepackage{amsmath,amssymb,amsfonts}
\usepackage{graphicx}
\usepackage{multirow}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\printanswers
\unframedsolutions

\begin{document}
"""

_POSTAMBLE = r"""
\end{document}
"""


# ── math sanitization (adapted from existing latex_writer.py) ─────────────────

_UNICODE_MATH = {
    "−": "-",
    "∞": r"\infty",
    "≤": r"\le",
    "≥": r"\ge",
    "≈": r"\approx",
    "≠": r"\ne",
    "×": r"\times",
}

_PROTECTED_RE = re.compile(
    r"(\\\(.+?\\\)|\\\[.+?\\\]|\$\$.+?\$\$|(?<!\\)\$.+?(?<!\\)\$)",
    re.DOTALL,
)

_DISPLAY_MATH_RE = re.compile(r"\$\$(.+?)\$\$", re.DOTALL)


def _strip_control(text: str) -> str:
    return "".join(ch for ch in text if ch in "\n\r\t" or ord(ch) >= 32)


def _apply_unicode(text: str) -> str:
    for src, dst in _UNICODE_MATH.items():
        text = text.replace(src, dst)
    return text


def _normalize_display_math(text: str) -> str:
    def repl(m: re.Match) -> str:
        inner = m.group(1).strip()
        if not inner:
            return ""
        if r"\begin{aligned}" in inner or r"\begin{cases}" in inner or r"\begin{array}" in inner:
            return rf"\[{inner}\]"
        if "\n" in inner:
            return rf"\[{inner}\]"
        return rf"\[{inner}\]"
    return _DISPLAY_MATH_RE.sub(repl, text)


def _balance_dollars(text: str) -> str:
    count = len(re.findall(r"(?<!\\)\$", text))
    if count % 2 == 1:
        text += "$"
    return text


def _escape_percent(text: str) -> str:
    return re.sub(r"(?<!\\)%", r"\\%", text)


def _sanitize(text: str) -> str:
    """Light sanitization pass on Mathpix-sourced LaTeX."""
    text = _strip_control(text)
    text = _apply_unicode(text)
    text = _normalize_display_math(text)
    text = _escape_percent(text)
    text = _balance_dollars(text)
    # Normalize runs of 3+ newlines
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


# ── question/part splitting ───────────────────────────────────────────────────

_PART_RE = re.compile(r"(?:^|\n)[ \t]*\(([a-f])\)[ \t]+", re.MULTILINE)


def _split_parts(text: str) -> tuple[str, list[tuple[str, str]]]:
    """
    Split text into (intro, [(label, body), ...]).

    Returns empty parts list if no (a), (b), ... sub-parts are found.
    """
    matches = list(_PART_RE.finditer(text))
    if not matches:
        return text.strip(), []

    intro = text[: matches[0].start()].strip()
    parts: list[tuple[str, str]] = []
    for i, m in enumerate(matches):
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[start:end].strip()
        # Strip trailing \\ (Mathpix line-break artifact at end of sub-part text)
        body = re.sub(r"\\\\+\s*$", "", body).strip()
        if body:
            parts.append((m.group(1), body))

    return intro, parts


# ── solution / rubric splitting ───────────────────────────────────────────────

# Matches the separator immediately before the first rubric annotation block.
# Rubric annotations always appear after all solution sub-parts and take the form:
#   $N:\left\{...\right.$    (inline math rubric array)
#   $$N:\{...\}$$            (display math rubric block)
#   N : criterion text       (standalone point annotation)
#   Note: ...
_RUBRIC_START_RE = re.compile(
    r"(?:"
    # \\ + newline: only safe before a $-prefixed rubric (not inside array rows)
    r"\\\\\n(?=\$\$?\s*\d+\s*(?:[:\\]|\\left|\\{))"
    r"|\n\n(?="                               # blank line before any rubric form
    r"\$\$?\s*\d+\s*(?:[:\\]|\\left|\\{)"    # $N:, $N\left{, $$N: etc.
    r"|\d+\s*:\s+[a-z]"                      # N : lowercase criterion
    r"|Note\s*:"                              # Note:
    r"))",
    re.IGNORECASE,
)

# Matches one complete rubric annotation item.
# Handles the many notation variants found across years 1998–2019:
#   $N:\left\{  (modern)       $N\left\{   (old, no colon)
#   N $\left\{  (1999 style)   $\mathbf{N}\left\{  (some years)
#   $$N..$$     (display math) N : criterion   Note: ...
_RUBRIC_ITEM_RE = re.compile(
    r"\$\$\s*\d+.*?\$\$"                                  # $$N...$$ display math
    r"|\$\\mathbf\{\d+\}\\left.*?\$(?:\\\\\n?)?"          # $\mathbf{N}\left{...$
    r"|\$\d+\s*(?:[:\\]|\\left|\\{).*?\$(?:\\\\\n?)?"     # $N:..$ or $N\left{..$
    r"|\d+\s*\$\\left.*?\$(?:\\\\\n?)?"                   # N $\left{..$ (digit then $)
    r"|\d+\s*:\s+\$\$.*?\$\$(?:\\\\\n?)?"                 # N: $$...$$ (digit-colon-$$)
    r"|\d+\s*:\s+\$.*?\$(?:\\\\\n?)?"                     # N: $...$ (digit-colon-$)
    r"|\d+\s*:\s+[a-z][^\n]*(?:\\\\\n?)?"                 # N : criterion line
    r"|Note\s*:[^\n]+",                                    # Note: ...
    re.DOTALL | re.IGNORECASE,
)


def _split_solution_rubric(text: str) -> tuple[str, str]:
    """
    Split combined SG text into (solution_text, rubric_text).

    Rubric annotations always appear as a trailing block after all solution
    sub-parts. Returns (text, "") if no rubric boundary is found.
    """
    m = _RUBRIC_START_RE.search(text)
    if m is None:
        return text.strip(), ""
    return text[: m.start()].strip(), text[m.end() :].strip()


def _split_rubric_items(rubric_text: str) -> list[str]:
    """Extract individual rubric annotation items from the rubric block."""
    return [
        m.group(0).rstrip("\\\\\n").strip()
        for m in _RUBRIC_ITEM_RE.finditer(rubric_text)
        if m.group(0).strip()
    ]


_UNDELIMITED_MATH_RE = re.compile(
    r"(?<!\\)(?<!\$)"       # not inside existing math
    r"(?:[a-zA-Z\d])"       # letter or digit
    r"(?:\^|_)"             # followed by ^ or _
    r"\{"                   # opening brace — marks a bare superscript/subscript
)


def _rubric_item_safe(item: str) -> str:
    """
    Ensure a rubric item can be placed as \\part content.

    Criterion lines like '1: x^{\\prime\\prime}(4)' contain bare LaTeX math
    outside $...$ which crashes pdflatex. Wrap such items in \\( \\).
    Items that are already $...$ or \\[...\\] blocks are left unchanged.
    """
    stripped = item.strip()
    if stripped.startswith(("$", "\\[", "\\(")):
        return item  # already fully in math delimiters
    # Only look for bare math OUTSIDE existing $...$ spans
    outside_math = re.sub(r"\$.*?\$", "", stripped, flags=re.DOTALL)
    if _UNDELIMITED_MATH_RE.search(outside_math):
        return rf"\({stripped}\)"
    return item


# ── per-block rendering ───────────────────────────────────────────────────────

def _meta_comment(block: QuestionBlock) -> str:
    form_label = " Form B" if block.form.upper() == "B" else ""
    calc = "Calculator Active" if block.calculator_active else "Calculator Prohibited"
    part = f"Part {block.part}"
    return f"% Q{block.question_number} | {block.year} Calculus BC{form_label} | {part} | {calc}"


def _render_question_block(block: QuestionBlock) -> str:
    lines: list[str] = []
    lines.append(r"\question")
    lines.append(_meta_comment(block))

    q_text = _sanitize(block.question_text)
    intro, parts = _split_parts(q_text)

    if intro:
        lines.append(intro)

    if parts:
        lines.append(r"\begin{parts}")
        for _label, body in parts:
            lines.append(rf"\part {_sanitize(body)}")
        lines.append(r"\end{parts}")
    elif not intro:
        # No intro and no parts — question text is empty (shouldn't happen)
        lines.append(r"\emph{[Question text not available]}")

    # Solution block: split on RAW text so that rubric boundary patterns see
    # $$...$$ (before _sanitize converts them to \[...\]), then sanitize each piece.
    if block.sg_text:
        sol_text_raw, rubric_text_raw = _split_solution_rubric(block.sg_text)
        sol_text = _sanitize(sol_text_raw or block.sg_text)
        # Extract rubric items from raw text, sanitize each individually
        rubric_items_raw = _split_rubric_items(rubric_text_raw)
        rubric_items = [_sanitize(item) for item in rubric_items_raw]

        lines.append(r"\begin{solution}")

        # ── Solution ──────────────────────────────────────────────────────────
        lines.append(r"\textbf{Solution:}\par")
        sol_intro, sol_parts = _split_parts(sol_text)
        if sol_intro:
            lines.append(sol_intro)
        if sol_parts:
            lines.append(r"\begin{parts}")
            for _label, body in sol_parts:
                lines.append(rf"\part {body}")
            lines.append(r"\end{parts}")
        elif not sol_intro:
            lines.append(sol_text)

        # ── Rubric ────────────────────────────────────────────────────────────
        if rubric_items:
            lines.append(r"\par\medskip")
            lines.append(r"\textbf{Rubric:}\par")
            lines.append(r"\begin{parts}")
            for item in rubric_items:
                lines.append(rf"\part {_rubric_item_safe(item)}")
            lines.append(r"\end{parts}")
        elif rubric_text_raw.strip():
            # Items couldn't be extracted — show as a flat block
            lines.append(r"\par\medskip")
            lines.append(r"\textbf{Rubric:}\par")
            lines.append(_sanitize(rubric_text_raw))

        lines.append(r"\end{solution}")

    return "\n".join(lines)


# ── year section rendering ────────────────────────────────────────────────────

def _section_title(year: int, form: str) -> str:
    form_label = " Form B" if form.upper() == "B" else ""
    return rf"\section*{{{year} AP Calculus BC{form_label}}}"


def _render_year_section(year: int, blocks: list[QuestionBlock], form: str = "") -> str:
    lines: list[str] = []
    lines.append(_section_title(year, form))
    lines.append("")
    lines.append(r"\begin{questions}")
    lines.append("")
    for block in sorted(blocks, key=lambda b: b.question_number):
        lines.append(_render_question_block(block))
        lines.append("")
    lines.append(r"\end{questions}")
    return "\n".join(lines)


# ── combined document ─────────────────────────────────────────────────────────

def build_combined_document(
    blocks_by_year: dict[int, list[QuestionBlock]],
    form_b_by_year: dict[int, list[QuestionBlock]] | None = None,
) -> str:
    """
    Build a single combined LaTeX document for all years.

    blocks_by_year:  {year: [QuestionBlock, ...]} for standard exams
    form_b_by_year:  {year: [QuestionBlock, ...]} for Form B exams (optional)
    """
    sections: list[str] = []

    all_years = sorted(set(list(blocks_by_year.keys()) + list((form_b_by_year or {}).keys())))

    for year in all_years:
        if year in blocks_by_year and blocks_by_year[year]:
            sections.append(_render_year_section(year, blocks_by_year[year], form=""))
        if form_b_by_year and year in form_b_by_year and form_b_by_year[year]:
            sections.append(_render_year_section(year, form_b_by_year[year], form="B"))

    body = "\n\n".join(sections)
    return _PREAMBLE + "\n" + body + "\n" + _POSTAMBLE


# ── file I/O ──────────────────────────────────────────────────────────────────

def write_tex(path: str, content: str) -> None:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(content, encoding="utf-8")
