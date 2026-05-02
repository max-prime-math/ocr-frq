"""
typst_gen.py — Render extracted FRQ data as a Typst document.

Produces a standalone Typst document with clearly separated
question, solution, and grading scheme sections for each FRQ page.
"""

import logging
import re
import subprocess
import tempfile
from pathlib import Path
from typing import Callable, Optional

from models import FRQExtraction

logger = logging.getLogger(__name__)

RepairCallback = Callable[[str, str, Optional[str]], Optional[str]]


_INLINE_MATH_RE = re.compile(r"\$\s*(.*?)\s*\$", re.DOTALL)
_DISPLAY_MATH_KEYWORDS = ("integral", "sum", "product", "lim")
_PARTS_RE = re.compile(r"(?m)^\(([a-z])\)\s+")
_BROKEN_TOKENS = (
    ("di f", "dif"),
    ("c os", "cos"),
    ("ta n", "tan"),
    ("si n", "sin"),
    ("l og", "log"),
    ("l n", "ln"),
    ("c do t", "dot"),
    ("d ot", "dot"),
)
_FUNCTION_NAMES = ("sin", "cos", "tan", "log", "ln", "exp", "lim", "dif", "dot")
_SPAN_REPAIR_RE = re.compile(r"\b(?:s\s*i\s*n|c\s*o\s*s|t\s*a\s*n|d\s*i\s*f|l\s*o\s*g|l\s*n|e\s*x\s*p|d\s*o\s*t)\b", re.IGNORECASE)
_TEXT_SENTINEL = "\x00\x01"


def _strip_control_chars(text: str) -> str:
    return "".join(ch for ch in text if ch in "\n\r\t" or ord(ch) >= 32)


def _convert_newlines(text: str) -> str:
    """Turn single newlines into Typst forced line breaks; keep paragraph breaks."""
    placeholder = "\x00PARA\x00"
    text = text.replace("\n\n", placeholder)
    text = text.replace("\n", "\\\n")
    text = text.replace(placeholder, "\n\n")
    return text


def _normalise_common_ocr(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"\\{2,}(?=(frac|text|cdot|times|div|sin|cos|tan|log|ln|exp|lim|dif)\b)", r"\\", text)
    text = text.replace(r"\cdot", "dot")
    text = text.replace(r"\times", "times")
    text = text.replace(r"\div", "div")
    text = text.replace("cdot", "dot")
    text = text.replace("−", "-")
    text = text.replace("×", "times")
    text = text.replace("•", "dot")

    for broken, fixed in _BROKEN_TOKENS:
        text = re.sub(rf"\b{re.escape(broken)}\b", fixed, text)

    for name in _FUNCTION_NAMES:
        pieces = r"\s*".join(re.escape(ch) for ch in name)
        text = re.sub(rf"\b{pieces}\b", name, text)

    # Remove OCR-noise asterisks when they sit between word/math characters.
    text = re.sub(r"(?<=[A-Za-z0-9\)\]])\s*\*\s*(?=[A-Za-z0-9\(\[])", " ", text)
    text = re.sub(r"[ \t]{2,}", " ", text)
    return text


def _looks_like_ocr_noise(text: str) -> bool:
    if _SPAN_REPAIR_RE.search(text):
        return True
    return bool(
        re.search(r"\b(?:[A-Za-z]\s+){2,}[A-Za-z]\b", text)
        or re.search(r"\b[A-Za-z]\s+[=+\-*/^_]\s+[A-Za-z0-9]\b", text)
    )


def _apply_span_repair(text: str, repair_callback: RepairCallback | None, kind: str) -> str:
    if repair_callback is None or not _looks_like_ocr_noise(text):
        return text

    repaired = repair_callback(kind, text, None)
    if not repaired:
        return text
    return _strip_control_chars(repaired)


def _normalise_rubric_artifacts(text: str) -> str:
    text = re.sub(r"([A-Za-z])\$(.+?)\$(?=[A-Za-z])", r"\1 $\2$ ", text)
    text = re.sub(r"\\\s*([{}])", r"\1", text)
    text = re.sub(r"\\\s*/\s*\\", " / ", text)
    text = re.sub(r"\\\s*/", " / ", text)
    text = re.sub(r"/\s*\\", " / ", text)
    text = re.sub(r"([A-Za-z])\$(?=[A-Za-z0-9(])", r"\1 $", text)
    text = re.sub(r"(?<=[0-9A-Za-z)])\$([A-Za-z])", r"$ \1", text)
    text = re.sub(r"(?<=\w)\$(?=-)", "", text)
    text = re.sub(r"(?<=\))\$(?=\d)", " $", text)
    text = re.sub(r"(?<=\})(?=\([a-z]\))", "\n", text)
    text = re.sub(r"\$\s*([0-9]+\s*:\s*\{)", r"\1", text)
    text = re.sub(r"(\})\$", r"\1", text)
    return text


def _extract_braced(text: str, start: int) -> tuple[str | None, int]:
    if start >= len(text) or text[start] != "{":
        return None, start
    depth = 0
    chars: list[str] = []
    for idx in range(start, len(text)):
        ch = text[idx]
        if ch == "{":
            if depth > 0:
                chars.append(ch)
            depth += 1
            continue
        if ch == "}":
            depth -= 1
            if depth == 0:
                return "".join(chars), idx + 1
            chars.append(ch)
            continue
        chars.append(ch)
    return None, start


def _replace_latex_frac(text: str) -> str:
    prefixes = (r"\frac", "frac")
    out: list[str] = []
    i = 0
    while i < len(text):
        matched = None
        for prefix in prefixes:
            if text.startswith(prefix, i):
                matched = prefix
                break
        if matched is None:
            out.append(text[i])
            i += 1
            continue

        j = i + len(matched)
        while j < len(text) and text[j].isspace():
            j += 1
        numer, j2 = _extract_braced(text, j)
        if numer is None:
            out.append(text[i])
            i += 1
            continue
        while j2 < len(text) and text[j2].isspace():
            j2 += 1
        denom, j3 = _extract_braced(text, j2)
        if denom is None:
            out.append(text[i])
            i += 1
            continue
        out.append(f"(({_replace_latex_frac(numer)})/({_replace_latex_frac(denom)}))")
        i = j3
    return "".join(out)


def _clean_math_span(span: str) -> str:
    span = _normalise_common_ocr(span)
    span = _replace_latex_frac(span)

    typst_math = {
        "alpha", "beta", "gamma", "delta", "epsilon", "zeta", "eta", "theta", "iota", "kappa",
        "lambda", "mu", "nu", "xi", "omicron", "pi", "rho", "sigma", "tau", "upsilon",
        "phi", "chi", "psi", "omega", "sqrt", "integral", "sum", "product", "lim", "sin",
        "cos", "tan", "log", "ln", "exp", "abs", "floor", "ceil", "dif", "dot", "times", "div",
    }
    for word in typst_math:
        span = span.replace(f"\\{word}", word)

    # Convert LaTeX-style text{...} fragments to Typst math text.
    span = re.sub(r"\\?text\s*\{([^{}]*)\}", lambda m: f'text("{m.group(1).strip()}")', span)
    span = re.sub(r'"([^"]+)"', lambda m: f'text("{m.group(1)}")', span)
    span = re.sub(r"(\^)\{([a-zA-Z0-9])\}", r"\1\2", span)
    span = re.sub(r"(?<=\d)(?=[A-Za-z])", " ", span)
    span = re.sub(r"\b([a-z])([a-z](?:\^|_))", r"\1 \2", span)
    span = re.sub(r"\b([a-eg-z])([xyt])\b", r"\1 \2", span)
    span = re.sub(r"\b([fgh])\s+([a-z])\b", r"\1(\2)", span)
    span = re.sub(r"\b([fgh])([a-z])\b", r"\1(\2)", span)

    protected: list[str] = []

    def protect_text(match: re.Match[str]) -> str:
        protected.append(match.group(0))
        return f"{_TEXT_SENTINEL}{len(protected) - 1}\x00"

    span = re.sub(r'text\(".*?"\)', protect_text, span)

    prose_pattern = re.compile(r"\b[A-Za-z][A-Za-z'-]*(?:\s+[A-Za-z][A-Za-z'-]*)*\b")

    def wrap_prose(match: re.Match[str]) -> str:
        phrase = match.group(0)
        words = phrase.split()
        if all(word in typst_math or len(word) == 1 for word in words):
            return phrase
        if len(words) == 1 and "'" in phrase:
            return phrase
        return f'text("{phrase}")'

    span = prose_pattern.sub(wrap_prose, span)

    def restore_text(match: re.Match[str]) -> str:
        return protected[int(match.group(1))]

    span = re.sub(rf"{re.escape(_TEXT_SENTINEL)}(\d+)\x00", restore_text, span)
    span = re.sub(r"[ \t]{2,}", " ", span).strip()
    return span


def _clean_math_spans(text: str, rubric_mode: bool = False) -> str:
    def replace_math(match: re.Match[str]) -> str:
        inner = _clean_math_span(match.group(1))
        if rubric_mode and (":" in inner or "/" in inner):
            return inner
        if "/" in inner or any(keyword in inner for keyword in _DISPLAY_MATH_KEYWORDS):
            return f"#align(center)[$ {inner} $]"
        return f"${inner}$"

    return _INLINE_MATH_RE.sub(replace_math, text)


def render_text(text: str, repair_callback: RepairCallback | None = None) -> str:
    """Prepare extracted text for embedding in a Typst content block."""
    t = _strip_control_chars(text)
    t = _apply_span_repair(t, repair_callback, "span")
    t = _normalise_common_ocr(t)
    t = _clean_math_spans(t)
    t = _convert_newlines(t)
    return t.strip()


def render_rubric_text(text: str, repair_callback: RepairCallback | None = None) -> str:
    """Prepare grading-scheme text with extra cleanup for malformed rubric notation."""
    t = _strip_control_chars(text)
    t = _apply_span_repair(t, repair_callback, "rubric")
    t = _normalise_common_ocr(t)
    t = _normalise_rubric_artifacts(t)
    t = _clean_math_spans(t, rubric_mode=True)
    t = t.replace("$", "")
    t = re.sub(r"(?<=\})(?=\([a-z]\))", "\n", t)
    t = re.sub(r"\s*/\s*", " / ", t)
    t = re.sub(r"[ \t]{2,}", " ", t)
    t = _convert_newlines(t)
    return t.strip()


def _repair_typst_document(text: str) -> str:
    """Repair common invalid Typst patterns without another API call."""

    def repair_trailing_unit_power(match: re.Match[str]) -> str:
        math_block = match.group(1)
        unit = " ".join(match.group(2).split())
        exponent = match.group(3).strip()
        return f'{math_block} $text("{unit}")^{exponent}$'

    def repair_inline_unit_power(match: re.Match[str]) -> str:
        math_span = match.group(1)
        unit = " ".join(match.group(2).split())
        exponent = match.group(3).strip()
        return f'{math_span} $text("{unit}")^{exponent}$'

    text = re.sub(
        r'(#align\(center\)\[\$.*?\$\])\s+([A-Za-z][A-Za-z0-9/ \-]+?)\$\^([^$]+)\$',
        repair_trailing_unit_power,
        text,
        flags=re.DOTALL,
    )
    text = re.sub(
        r'(\$[^$\n]+\$)\s+([A-Za-z][A-Za-z0-9/ \-]+?)\$\^([^$]+)\$',
        repair_inline_unit_power,
        text,
    )
    text = re.sub(r'(?<!\$)\$\^([^$]+)\$', lambda m: f'#super[{m.group(1).strip()}]', text)
    text = re.sub(r'\$([A-Za-z][A-Za-z0-9/ \-]+)\$', lambda m: m.group(1) if " " in m.group(1) or "/" in m.group(1) else m.group(0), text)
    return text


def _validate_typst_document(text: str) -> Optional[str]:
    """Compile-check generated Typst and return stderr on failure."""
    try:
        with tempfile.TemporaryDirectory(prefix="ocr-frq-typst-") as tmpdir:
            tmp_path = Path(tmpdir)
            typ_path = tmp_path / "output.typ"
            pdf_path = tmp_path / "output.pdf"
            typ_path.write_text(text, encoding="utf-8")
            result = subprocess.run(
                ["typst", "compile", str(typ_path), str(pdf_path)],
                capture_output=True,
                text=True,
                check=False,
            )
            if result.returncode == 0:
                return None
            return (result.stderr or result.stdout or "Typst compile failed").strip()
    except FileNotFoundError:
        return None
    except Exception as exc:
        return f"Typst validation failed unexpectedly: {exc}"


def _split_top_level_parts(text: str) -> Optional[list[tuple[str, str]]]:
    matches = list(_PARTS_RE.finditer(text))
    if not matches:
        return None
    expected = [chr(ord("a") + idx) for idx in range(len(matches))]
    labels = [match.group(1) for match in matches]
    if labels != expected:
        return None

    parts: list[tuple[str, str]] = []
    for idx, match in enumerate(matches):
        start = match.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        body = text[start:end].strip()
        parts.append((match.group(1), body))
    return parts


def _indent_block(text: str, prefix: str) -> str:
    return "\n".join(prefix + line if line else prefix.rstrip() for line in text.splitlines())


def _render_parts(text: str) -> Optional[str]:
    parts = _split_top_level_parts(text)
    if not parts:
        return None

    lines = ["#enum(numbering: \"(a)\","]
    for _, body in parts:
        rendered = render_text(body) if body else "_[Part text not extracted]_"
        lines.append("  [")
        lines.append(_indent_block(rendered, "    "))
        lines.append("  ],")
    lines.append(")")
    return "\n".join(lines)


def _render_table(table: dict) -> str:
    headers = [render_text(cell) for cell in table.get("headers", [])]
    rows = [[render_text(cell) for cell in row] for row in table.get("rows", [])]
    column_count = 0
    for row in [headers] + rows:
        column_count = max(column_count, len(row))
    column_count = max(1, column_count)

    lines = [
        "#table(",
        f"  columns: {column_count},",
        "  stroke: 0.5pt,",
        "  inset: 6pt,",
    ]

    if headers:
        padded = headers + [""] * (column_count - len(headers))
        for cell in padded:
            lines.append(f"  [*{cell}*],")

    for row in rows:
        padded = row + [""] * (column_count - len(row))
        for cell in padded:
            lines.append(f"  [{cell}],")

    lines.append(")")
    return "\n".join(lines)


def _figure_width(fig: dict) -> str:
    fraction = fig.get("render_width")
    if isinstance(fraction, (int, float)) and fraction > 0:
        return f"{min(100, max(1, round(fraction * 100, 1)))}%"
    width = fig.get("width")
    if isinstance(width, (int, float)) and width > 0:
        return f"{min(100, max(1, round(width * 100, 1)))}%"
    return "auto"


def _render_figure(fig: dict) -> Optional[str]:
    file_path = fig.get("file_path", "")
    if not file_path:
        return None
    width = _figure_width(fig)
    return "\n".join([
        "#figure(",
        f'  image("{file_path}", width: {width}),',
        ")",
    ])


def _render_question_body(text: str) -> str:
    rendered_parts = _render_parts(text)
    if rendered_parts is not None:
        return rendered_parts
    return render_text(text)


def _render_section_content(
    body_text: str,
    tables: list[dict],
    figures: list[dict],
    question_mode: bool = False,
    placeholder: str = "_[Content not extracted]_",
) -> list[str]:
    lines: list[str] = []
    if body_text:
        lines.append(_render_question_body(body_text) if question_mode else render_text(body_text))
    else:
        lines.append(placeholder)

    for table in tables:
        lines.append("")
        lines.append(_render_table(table))

    for fig in figures:
        rendered = _render_figure(fig)
        if rendered:
            lines.append("")
            lines.append(rendered)

    return lines


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
    lines.append(f"= Question {qnum}" if qnum is not None else "= Question")
    lines.append("")

    comment_parts = []
    if source:
        comment_parts.append(f"source: {source}")
    calculator = extraction.get("calculator")
    if calculator:
        comment_parts.append(calculator)
    unit = extraction.get("unit")
    if unit:
        comment_parts.append(unit)
    section = extraction.get("section")
    if section:
        comment_parts.append(section)
    if comment_parts:
        lines.append("// " + " | ".join(comment_parts))
        lines.append("")

    if extraction.get("flagged"):
        reason = extraction.get("flag_reason") or "low confidence"
        lines.append(f"#text(fill: red.darken(20%))[*Flagged for review: {reason}*]")
        lines.append("")

    figures = extraction.get("figures") or []
    tables = extraction.get("tables") or []
    question_figures = [fig for fig in figures if fig.get("section") == "question"]
    solution_figures = [fig for fig in figures if fig.get("section") == "solution"]
    rubric_figures = [fig for fig in figures if fig.get("section") == "grading_scheme"]
    question_tables = [table for table in tables if table.get("section") == "question"]
    solution_tables = [table for table in tables if table.get("section") == "solution"]
    rubric_tables = [table for table in tables if table.get("section") == "grading_scheme"]

    question = extraction.get("question") or ""
    lines.extend(_render_section_content(
        question,
        question_tables,
        question_figures,
        question_mode=True,
        placeholder="_[Question text not extracted]_",
    ) if question else ["_[Question text not extracted]_"])
    lines.append("")

    solution = extraction.get("solution") or ""
    lines.append("#solution-block[")
    for line in _render_section_content(
        solution,
        solution_tables,
        solution_figures,
        placeholder="_[Solution not extracted]_",
    ):
        lines.append(line)
    lines.append("]")
    lines.append("")

    rubric = extraction.get("grading_scheme") or ""
    lines.append("#rubric-block[")
    if rubric:
        lines.append(render_rubric_text(rubric))
        for table in rubric_tables:
            lines.append("")
            lines.append(_render_table(table))
        for fig in rubric_figures:
            rendered = _render_figure(fig)
            if rendered:
                lines.append("")
                lines.append(rendered)
    else:
        lines.append("_[Grading scheme not extracted]_")
    lines.append("]")
    return "\n".join(lines)


def build_document(
    page_results: list[dict],
    include_skipped_comments: bool = True,
    repair_callback: RepairCallback | None = None,
    max_repair_attempts: int = 1,
) -> str:
    """
    Build a complete Typst document from a list of PageResult dicts.

    Only pages with page_type == "frq" produce content blocks.
    Skipped pages appear as comments if include_skipped_comments is True.
    """
    blocks: list[str] = []

    for result in page_results:
        if result.get("error"):
            blocks.append(f"// Error on page {result['page'] + 1}: {result['error']}")
            continue

        extraction: Optional[dict] = result.get("extraction")
        if extraction is None:
            continue

        if extraction["page_type"] == "skip":
            if include_skipped_comments:
                reason = extraction.get("skip_reason") or "unknown"
                blocks.append(f"// Page {result['page'] + 1} skipped: {reason}")
            continue

        fname = result.get("fname", "")
        source = f"{fname} p{result['page'] + 1}" if fname else f"p{result['page'] + 1}"
        blocks.append(render_frq_block(extraction, source=source))
        blocks.append("#line(length: 100%, stroke: 0.5pt)\n\n#v(12pt)")

    body = "\n\n".join(blocks)
    document = _PREAMBLE + body + "\n"
    document = _repair_typst_document(document)
    validation_error = _validate_typst_document(document)

    attempts = 0
    while validation_error and repair_callback is not None and attempts < max_repair_attempts:
        attempts += 1
        repaired = repair_callback("document", document, validation_error)
        if not repaired or repaired == document:
            break
        document = _repair_typst_document(_strip_control_chars(repaired))
        validation_error = _validate_typst_document(document)

    if validation_error:
        logger.warning("Typst validation failed after local repair:\n%s", validation_error)
        document += f"\n// Typst validation warning:\n// {validation_error.replace(chr(10), chr(10) + '// ')}\n"
    return document
