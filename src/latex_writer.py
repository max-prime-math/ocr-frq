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
    Split question text into (intro, [(label, body), ...]).

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

    # Solution block: combined solution + rubric from SG
    sg = _sanitize(block.sg_text)
    if sg:
        lines.append(r"\begin{solution}")
        lines.append(sg)
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
