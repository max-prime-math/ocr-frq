from __future__ import annotations

import re
from pathlib import Path

from .contracts import FigureRef, QuestionBlock, TableRef


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
    r"[A-Za-z0-9\\{}_^()+\-*/.,\s]+"
    r")"
)
_COMMAND_MATH_PATTERN = re.compile(
    r"("
    r"\\(?:int|iint|iiint|sum|prod|lim|frac|dfrac|tfrac|sqrt|sin|cos|tan|cot|sec|csc|ln|log|exp|Rightarrow|theta|pi|alpha|beta|lambda|text)"
    r"(?:\\.|[^?.!,;:])*"
    r")"
)
_MATH_ENVIRONMENTS = ("array", "cases", "matrix", "pmatrix", "bmatrix", "vmatrix", "Vmatrix")
_MATH_ENV_PATTERN = re.compile(
    r"(\\begin\{(?:array|cases|matrix|pmatrix|bmatrix|vmatrix|Vmatrix)\}.*?\\end\{(?:array|cases|matrix|pmatrix|bmatrix|vmatrix|Vmatrix)\})",
    re.DOTALL,
)
_PART_MARKER_RE = re.compile(r"(?:^|(?<=[\n.?!:]))\s*\(([a-e])\)\s+")

_PREAMBLE = r"""\documentclass[12pt,addpoints,answers]{exam}
\usepackage[margin=1in]{geometry}
\usepackage{amsmath,amssymb,amsfonts}
\usepackage{graphicx}
\usepackage{float}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\printanswers
\unframedsolutions

\begin{document}
\begin{center}
{\Large AP FRQ Pack}
\end{center}
\begin{questions}
"""

_POSTAMBLE = r"""
\end{questions}
\end{document}
"""

_PAGE_TO_TEXT_WIDTH = 8.5 / 6.5


def _escape_percent(text: str) -> str:
    return re.sub(r"(?<!\\)%", r"\\%", text)


def _strip_control_chars(text: str) -> str:
    return "".join(ch for ch in text if ch in "\n\r\t" or ord(ch) >= 32)


def _escape_plain_text(text: str) -> str:
    replacements = {
        "&": r"\&",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    out = text
    for src, dst in replacements.items():
        out = out.replace(src, dst)
    return out


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


def _normalise_unicode_math(text: str) -> str:
    repaired = _strip_control_chars(text)
    for src, dst in _UNICODE_MATH_REPLACEMENTS.items():
        repaired = repaired.replace(src, dst)
    repaired = re.sub(r"(?<![A-Za-z\\])(?:bigint|igint)(?=\s*_)", r"\\int", repaired)
    repaired = _normalise_mixed_math_delimiters(repaired)
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


def _wrap_dollar_math(match: re.Match[str]) -> str:
    text = match.group(1).strip()
    return f"${text}$"


def _wrap_display_math(match: re.Match[str]) -> str:
    text = match.group(1).strip()
    return rf"\[{text}\]"


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
        plain = _MATH_ENV_PATTERN.sub(_wrap_display_math, plain)
        plain = _INTERVAL_PATTERN.sub(_wrap_inline_math, plain)
        plain = _RANGE_PATTERN.sub(_wrap_inline_math, plain)
        plain = _INLINE_EQUATION_PATTERN.sub(_wrap_inline_math, plain)
        plain = _COMMAND_MATH_PATTERN.sub(_wrap_inline_math, plain)
        parts.append(plain)
        parts.append(match.group(0))
        last = match.end()

    tail = text[last:]
    tail = _MATH_ENV_PATTERN.sub(_wrap_display_math, tail)
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

    if _count_unescaped_dollars(repaired) % 2 == 1:
        repaired += "$"

    return repaired


def _looks_like_bare_math(text: str) -> bool:
    stripped = text.strip()
    if not stripped:
        return False
    if any(token in stripped for token in (r"\(", r"\[", "$$", "$")):
        return False
    if len(stripped.split()) > 8:
        return False
    if len(stripped.split()) > 4 and not any(ch in stripped for ch in "=+-*/^_[]{}()\\"):
        return False
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


def _sanitize_latex_text(text: str, *, auto_wrap_whole: bool = True, wrap_bare_spans: bool = True) -> str:
    env_block = _wrap_math_environment_block(text)
    if env_block is not None:
        return env_block

    cleaned = _normalise_unicode_math(text)
    cleaned = _normalise_dollar_runs(cleaned)
    cleaned = _balance_delimited_math(_escape_percent(cleaned))
    cleaned = _repair_protected_math(cleaned)
    if wrap_bare_spans:
        cleaned = _wrap_bare_math_spans(cleaned)
    cleaned = _repair_protected_math(cleaned)
    cleaned = _normalise_mixed_math_delimiters(cleaned)
    cleaned = _dedupe_math_delimiters(cleaned)
    cleaned = _balance_delimited_math(cleaned)
    if auto_wrap_whole and _looks_like_bare_math(cleaned):
        return rf"\({cleaned}\)"
    return cleaned


def _render_text(text: str, *, auto_wrap_whole: bool = True, wrap_bare_spans: bool = True, wrap_bare_lines: bool = True) -> str:
    cleaned = _sanitize_latex_text(text, auto_wrap_whole=auto_wrap_whole, wrap_bare_spans=wrap_bare_spans)

    def render_plain_segment(segment: str) -> str:
        normalized = segment.replace("\r\n", "\n").replace("\r", "\n")
        lines: list[str] = []
        for raw_line in normalized.split("\n"):
            line = raw_line.strip()
            if not line:
                lines.append("")
                continue
            if wrap_bare_lines and _looks_like_bare_math(line):
                if any(token in line for token in ("=", r"\int", r"\frac", r"\sum", r"\lim", r"\prod")):
                    lines.append(rf"\[{line}\]")
                else:
                    lines.append(rf"\({line}\)")
                continue
            lines.append(_escape_plain_text(line))
        rendered = "\n".join(lines)
        rendered = rendered.replace("\n\n", " \\par ")
        rendered = rendered.replace("\n", " ")
        return rendered

    parts: list[str] = []
    last = 0
    for match in _PROTECTED_MATH_PATTERN.finditer(cleaned):
        plain = cleaned[last:match.start()]
        if plain:
            parts.append(render_plain_segment(plain))
        parts.append(match.group(0))
        last = match.end()
    tail = cleaned[last:]
    if tail:
        parts.append(render_plain_segment(tail))

    rendered = "".join(parts) if parts else _escape_plain_text(cleaned)
    rendered = re.sub(r"\s+", " ", rendered).strip()
    return rendered or r"\emph{[missing]}"


def _normalise_grading_text(text: str) -> str:
    cleaned = _strip_control_chars(text)
    cleaned = cleaned.replace(r"\{", "(")
    cleaned = cleaned.replace(r"\}", ")")
    cleaned = cleaned.replace(r"\left\{\begin{array}{l}", "(")
    cleaned = cleaned.replace(r"\begin{array}{l}", "(")
    cleaned = cleaned.replace(r"\end{array}\right.", ")")
    cleaned = cleaned.replace(r"\end{array}", ")")
    cleaned = cleaned.replace(r"\left<", "<")
    cleaned = cleaned.replace(r"\left(", "(")
    cleaned = cleaned.replace(r"\right.", ")")
    cleaned = cleaned.replace(r"\begin{cases}", "(")
    cleaned = cleaned.replace(r"\end{cases}", ")")
    cleaned = cleaned.replace(r"\\", "; ")
    cleaned = cleaned.replace("&", ";")
    cleaned = re.sub(r"\\text\{([^{}]*)\}", r"\1", cleaned)
    cleaned = cleaned.replace(" / ", "; ")
    cleaned = cleaned.replace(" - OR - ", " OR ")

    protected: list[str] = []

    def protect(match: re.Match[str]) -> str:
        protected.append(match.group(0))
        return f"__RUBRIC_MATH_{len(protected) - 1}__"

    def protect_command(match: re.Match[str]) -> str:
        protected.append(f"${match.group(1).strip()}$")
        return f"__RUBRIC_MATH_{len(protected) - 1}__"

    cleaned = _PROTECTED_MATH_PATTERN.sub(protect, cleaned)
    cleaned = _COMMAND_MATH_PATTERN.sub(protect_command, cleaned)

    def format_plain(segment: str) -> str:
        segment = segment.replace('"', "")
        segment = segment.replace("{", "(")
        segment = segment.replace("}", ")")
        segment = re.sub(r"\s*(Question\s+\d+[^:]*:)", r" \\par \1", segment)
        segment = re.sub(r"\s*(Part \([a-z]\):)", r" \\par \1", segment)
        segment = re.sub(r"\s*-\s*(\d+\s+point[s]?:)", r" \\par - \1", segment)
        segment = re.sub(r"([(;])\s*(\d+\s*:\s*)", r"\1 \\par \2", segment)
        segment = re.sub(r"\s*(Note:)", r" \\par \1", segment)
        segment = re.sub(r"\s*;\s*", "; ", segment)
        segment = segment.replace("Question \\par ", "Question ")
        return segment

    parts: list[str] = []
    last = 0
    for match in _PROTECTED_MATH_PATTERN.finditer(cleaned):
        plain = cleaned[last:match.start()]
        if plain:
            parts.append(format_plain(plain))
        parts.append(match.group(0))
        last = match.end()
    tail = cleaned[last:]
    if tail:
        parts.append(format_plain(tail))
    cleaned = "".join(parts)

    for idx, block in enumerate(protected):
        cleaned = cleaned.replace(f"__RUBRIC_MATH_{idx}__", block)

    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned


def _render_grading_text(text: str) -> str:
    cleaned = _normalise_grading_text(text)
    rendered = _render_text(cleaned, auto_wrap_whole=False, wrap_bare_spans=False, wrap_bare_lines=False)
    rendered = rendered.replace(r"\(\)", "")
    return rendered


def _split_parts(text: str) -> tuple[str, list[tuple[str, str]]]:
    stripped = text.strip()
    if not stripped:
        return "", []

    matches = list(_PART_MARKER_RE.finditer(stripped))
    if not matches:
        return stripped, []

    intro = stripped[:matches[0].start()].strip()
    parts: list[tuple[str, str]] = []
    for idx, match in enumerate(matches):
        start = match.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(stripped)
        body = stripped[start:end].strip()
        if body:
            parts.append((match.group(1), body))
    return intro, parts


def _parts_to_map(parts: list[tuple[str, str]]) -> dict[str, str]:
    return {label: body for label, body in parts}


def _combine_extra_parts(intro: str, parts: dict[str, str]) -> str:
    chunks: list[str] = []
    if intro:
        chunks.append(intro)
    for label in sorted(parts):
        chunks.append(f"({label}) {parts[label]}")
    return "\n\n".join(chunks).strip()


def _render_figures(lines: list[str], figures: list[FigureRef]) -> None:
    for fig in figures:
        fig_path = fig.file_path.replace("\\", "/")
        width_fraction = fig.render_width if fig.render_width is not None else 0.6
        width_fraction = min(0.95, max(0.12, width_fraction * _PAGE_TO_TEXT_WIDTH))
        lines.append(r"\begin{center}")
        lines.append(rf"\includegraphics[width={width_fraction:.3f}\linewidth]{{{fig_path}}}")
        if fig.caption:
            lines.append(rf"\\ { _escape_plain_text(fig.caption.strip()) }")
        lines.append(r"\end{center}")


def _render_table_cell(text: str) -> str:
    cell = _render_text(text, auto_wrap_whole=False)
    cell = cell.replace(r"\par", " ")
    cell = cell.replace("\n", " ")
    return re.sub(r"\s+", " ", cell).strip() or r"\mbox{}"


def _render_tables(lines: list[str], tables: list[TableRef]) -> None:
    for table in tables:
        widths = [len(table.headers)] if table.headers else []
        widths.extend(len(row) for row in table.rows)
        col_count = max(widths, default=0)
        if col_count == 0:
            continue
        col_spec = "|" + "|".join("l" for _ in range(col_count)) + "|"
        lines.append(r"\begin{center}")
        if table.caption:
            lines.append(rf"\textbf{{{_escape_plain_text(table.caption)}}}\\")
        lines.append(rf"\begin{{tabular}}{{{col_spec}}}")
        lines.append(r"\hline")
        if table.headers:
            headers = [_render_table_cell(cell) for cell in table.headers]
            headers.extend([r"\mbox{}"] * (col_count - len(headers)))
            lines.append(" & ".join(headers) + r" \\")
            lines.append(r"\hline")
        for row in table.rows:
            cells = [_render_table_cell(cell) for cell in row]
            cells.extend([r"\mbox{}"] * (col_count - len(cells)))
            lines.append(" & ".join(cells) + r" \\")
            lines.append(r"\hline")
        lines.append(r"\end{tabular}")
        lines.append(r"\end{center}")


def _append_solution(
    lines: list[str],
    solution: str,
    grading: str,
    solution_figures: list[FigureRef],
    rubric_figures: list[FigureRef],
    solution_tables: list[TableRef],
    rubric_tables: list[TableRef],
) -> None:
    if not solution and not grading and not solution_figures and not rubric_figures and not solution_tables and not rubric_tables:
        return

    lines.append(r"\begin{solution}")
    if solution:
        lines.append(_render_text(solution))
    if solution_tables:
        _render_tables(lines, solution_tables)
    if solution_figures:
        _render_figures(lines, solution_figures)
    if grading:
        if solution or solution_tables or solution_figures:
            lines.append(r"\par\medskip")
        lines.append(r"\textbf{Scoring Guide}\par")
        lines.append(_render_grading_text(grading))
    if rubric_tables:
        _render_tables(lines, rubric_tables)
    if rubric_figures:
        _render_figures(lines, rubric_figures)
    lines.append(r"\end{solution}")


def _combine_part_bodies(intro: str, parts: list[tuple[str, str]]) -> str:
    chunks: list[str] = []
    if intro:
        chunks.append(intro)
    for label, body in parts:
        if body:
            chunks.append(f"Part ({label}): {body}")
    return "\n\n".join(chunk for chunk in chunks if chunk).strip()


def _render_question_block(block: QuestionBlock) -> str:
    lines: list[str] = [r"\question"]
    lines.append(f"% {block.block_id}")

    question_figures = [fig for fig in block.figures if fig.section == "question"]
    solution_figures = [fig for fig in block.figures if fig.section == "solution"]
    rubric_figures = [fig for fig in block.figures if fig.section == "grading_scheme"]
    question_tables = [table for table in block.tables if table.section == "question"]
    solution_tables = [table for table in block.tables if table.section == "solution"]
    rubric_tables = [table for table in block.tables if table.section == "grading_scheme"]

    q_intro, q_parts = _split_parts(block.question_text)
    s_intro, s_parts = _split_parts(block.solution_text)
    g_intro, g_parts = _split_parts(block.grading_text)

    if not q_parts:
        lines.append(_render_text(block.question_text))
        if question_tables:
            _render_tables(lines, question_tables)
        if question_figures:
            _render_figures(lines, question_figures)
        _append_solution(lines, block.solution_text, block.grading_text, solution_figures, rubric_figures, solution_tables, rubric_tables)
        return "\n".join(lines)

    if q_intro:
        lines.append(_render_text(q_intro))
    if question_tables:
        _render_tables(lines, question_tables)
    if question_figures:
        _render_figures(lines, question_figures)

    lines.append(r"\begin{parts}")
    for label, prompt in q_parts:
        lines.append(rf"\part {_render_text(prompt)}")
    lines.append(r"\end{parts}")

    combined_solution = _combine_part_bodies(s_intro, s_parts)
    combined_grading = _combine_part_bodies(g_intro, g_parts)
    _append_solution(lines, combined_solution, combined_grading, solution_figures, rubric_figures, solution_tables, rubric_tables)
    return "\n".join(lines)


def build_latex_document(blocks: list[QuestionBlock], skipped_block_ids: set[str]) -> str:
    rendered_blocks: list[str] = []
    for block in sorted(blocks, key=lambda b: b.question_number):
        if block.block_id in skipped_block_ids:
            rendered_blocks.append(f"% SKIPPED {block.block_id} Q{block.question_number}")
            continue
        rendered_blocks.append(_render_question_block(block))
    return _PREAMBLE + "\n\n".join(rendered_blocks) + _POSTAMBLE


def write_tex(path: str, content: str) -> None:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(content, encoding="utf-8")
