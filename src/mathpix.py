"""
mathpix.py — Parse Mathpix zip exports into structured question data.

Handles two SG formats:
  - 2000+: questions separated by \\section*{Question N}
  - 1998-1999: questions in \\begin{enumerate}\\item or plain "N. text" format

Handles two exam formats:
  - 2000+: explicit Part A / Part B section separators
  - 1998-1999: no explicit separator (default Q1-3 = Part A, Q4-6 = Part B)
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from zipfile import ZipFile

from .contracts import ExamQuestion


# ── zip loading ───────────────────────────────────────────────────────────────

def _load_zip(zip_path: str) -> tuple[str, dict[str, bytes]]:
    with ZipFile(zip_path) as zf:
        names = zf.namelist()
        tex_name = next((n for n in names if n.endswith(".tex")), None)
        if tex_name is None:
            raise ValueError(f"No .tex file in {zip_path}")
        tex = zf.read(tex_name).decode("utf-8", errors="replace")
        images: dict[str, bytes] = {}
        for name in names:
            if not name.endswith("/") and not name.endswith(".tex"):
                stem = Path(name).stem
                if stem:
                    images[stem] = zf.read(name)
    return tex, images


def _strip_header(tex: str) -> str:
    """Remove \\documentclass...\\begin{document} preamble."""
    m = re.search(r"\\begin\{document\}", tex)
    if m:
        tex = tex[m.end():]
    tex = re.sub(r"\\maketitle\s*", "", tex)
    return tex


# ── figure handling ───────────────────────────────────────────────────────────

_INCLUDEGRAPHICS_RE = re.compile(
    r"\\includegraphics(?:\[([^\]]*)\])?\{([^}]+)\}"
)

def _normalize_includegraphics_opts(opts: str) -> str:
    """Convert adjustbox options to plain graphicx options."""
    opts = re.sub(r"\balt=\{[^}]*\}", "", opts)
    opts = re.sub(r"\bmax\s+width\s*=[^,\]]+", r"width=0.8\\linewidth", opts)
    opts = re.sub(r"(?:,\s*)?\bcenter\b(?:\s*,)?", "", opts)
    opts = re.sub(r",\s*,", ",", opts)
    return opts.strip(" ,")


def _extract_and_save_figures(
    tex: str,
    images: dict[str, bytes],
    figures_dir: str,
    prefix: str,
) -> tuple[str, list[str]]:
    """
    Save figure images from the zip to figures_dir and rewrite \\includegraphics refs.

    Returns (modified_tex, [relative_paths]).
    """
    out_dir = Path(figures_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    refs_in_order: list[str] = []
    seen: set[str] = set()
    for m in _INCLUDEGRAPHICS_RE.finditer(tex):
        ref = m.group(2)
        if ref not in seen:
            seen.add(ref)
            refs_in_order.append(ref)

    # Map internal ref → output path
    internal_to_out: dict[str, str] = {}
    saved: list[str] = []

    for idx, ref in enumerate(refs_in_order, start=1):
        ref_stem = Path(ref).stem
        matching = None
        for key, data in images.items():
            if key == ref or key == ref_stem or ref_stem.startswith(key) or key.startswith(ref_stem):
                matching = (key, data)
                break
        if matching is None:
            # Fuzzy: find key that contains ref_stem or vice versa
            for key, data in images.items():
                if ref_stem in key or key in ref_stem:
                    matching = (key, data)
                    break
        if matching is None:
            continue

        ext = ".jpg"  # Mathpix images are typically JPEG
        out_name = f"{prefix}_fig{idx}{ext}"
        out_path = out_dir / out_name
        out_path.write_bytes(matching[1])
        rel = f"figures/{out_name}"
        internal_to_out[ref] = rel
        saved.append(rel)

    def repl(m: re.Match) -> str:
        opts = _normalize_includegraphics_opts(m.group(1) or "")
        ref = m.group(2)
        new_ref = internal_to_out.get(ref, ref)
        if not opts or "width" not in opts:
            opts = "width=0.8\\linewidth"
        return f"\\includegraphics[{opts}]{{{new_ref}}}"

    tex = _INCLUDEGRAPHICS_RE.sub(repl, tex)
    return tex, saved


# ── question boundary detection ───────────────────────────────────────────────

def _find_question_starts(body: str) -> list[tuple[int, int]]:
    """
    Return list of (char_pos, question_number) for each question start, sorted by position.

    Handles:
    1. \\setcounter{enumi}{N}\\n  \\item  → question N+1
    2. First \\item with no preceding setcounter → question 1
    3. Consecutive \\item in same enumerate block → increments question number
    4. Plain "N. text" at line start (1998-1999 SG free-form) → question N
    """
    starts: list[tuple[int, int]] = []

    # Pattern 1 & 3: scan all \item occurrences and infer question numbers
    # Track the running question counter
    pending_qnum: int | None = None
    current_qnum = 0
    in_enumerate = 0

    token_re = re.compile(
        r"\\begin\{enumerate\}|\\end\{enumerate\}"
        r"|\\setcounter\{enumi\}\{(\d+)\}"
        r"|\\item\b"
    )

    for m in token_re.finditer(body):
        text = m.group(0)
        if text == r"\begin{enumerate}":
            in_enumerate += 1
        elif text == r"\end{enumerate}":
            in_enumerate = max(0, in_enumerate - 1)
        elif m.group(1) is not None:
            pending_qnum = int(m.group(1)) + 1
        elif text.startswith(r"\item"):
            if pending_qnum is not None:
                current_qnum = pending_qnum
                pending_qnum = None
            else:
                current_qnum += 1
            starts.append((m.start(), current_qnum))

    # Pattern 4: plain "N. " at line start (for old SG / some exam years)
    plain_re = re.compile(r"(?m)^[ \t]*([1-9])\.\s+(?=[A-Z\$\\])")
    for m in plain_re.finditer(body):
        qnum = int(m.group(1))
        pos = m.start()
        if not any(abs(s[0] - pos) < 30 for s in starts):
            starts.append((pos, qnum))

    starts.sort(key=lambda x: x[0])

    # Deduplicate: for each question number, keep first occurrence
    seen: set[int] = set()
    result: list[tuple[int, int]] = []
    for pos, qnum in starts:
        if qnum not in seen:
            seen.add(qnum)
            result.append((pos, qnum))
    result.sort(key=lambda x: x[0])
    return result


_CENTER_BLOCK_RE = re.compile(r"\\begin\{center\}.*?\\end\{center\}", re.DOTALL)
_CAPTION_TAIL_RE = re.compile(r"\s*\n[^\n]*\\\\\s*$")


def _find_tail_preamble(text: str) -> tuple[str, int] | None:
    """
    Find the last \\begin{center}...\\end{center} block at the tail of text,
    optionally followed by a caption line ending with \\\\.

    Returns (preamble_text, start_position) or None.
    """
    matches = list(_CENTER_BLOCK_RE.finditer(text))
    if not matches:
        return None
    last = matches[-1]
    after = text[last.end():]
    # After the center block, allow only optional caption line + whitespace
    if after.strip():
        # Check if it's just a caption line (no newlines in significant content)
        cap_m = _CAPTION_TAIL_RE.match(after)
        if cap_m is None:
            return None
        return text[last.start() :], last.start()
    return text[last.start() :], last.start()


def _extract_blocks(body: str, starts: list[tuple[int, int]]) -> dict[int, str]:
    """
    Slice body into per-question text blocks.

    For plain-text question starts ("N. text"), any figure+caption that
    immediately precedes the start (visually above the question in print)
    is moved into the beginning of that block.
    """
    # Detect plain-text starts (not preceded by \item)
    plain_positions: set[int] = set()
    for pos, _qnum in starts:
        preceding = body[max(0, pos - 60) : pos]
        if not re.search(r"\\item\s*$", preceding.strip()):
            plain_positions.add(pos)

    blocks: dict[int, str] = {}
    for i, (pos, qnum) in enumerate(starts):
        end = starts[i + 1][0] if i + 1 < len(starts) else len(body)
        raw = body[pos:end]

        # Strip \item or "N. " prefix and trailing enumerate-starters
        raw_clean = re.sub(r"^\s*\\item\s*", "", raw.strip())
        raw_clean = re.sub(r"^\s*\d+\.\s*", "", raw_clean)
        # Strip trailing \begin{enumerate}/\setcounter that are the wrapper for the NEXT question
        raw_clean = re.sub(
            r"(?:\n[ \t]*\\begin\{enumerate\}|\n[ \t]*\\setcounter\{enumi\}\{\d+\})+\s*$",
            "",
            raw_clean,
        ).rstrip()

        # Pull any \begin{center}...\end{center} preamble from the end of the
        # previous block into the start of this block — Mathpix places figures
        # and tables before the \item they belong to in the printed exam.
        preamble = ""
        if i > 0:
            prev_pos, prev_qnum = starts[i - 1]
            prev_content = blocks.get(prev_qnum, body[prev_pos:pos])
            result = _find_tail_preamble(prev_content)
            if result is not None:
                tail_text, tail_start = result
                preamble = tail_text.strip() + "\n"
                if prev_qnum in blocks:
                    blocks[prev_qnum] = blocks[prev_qnum][:tail_start].rstrip()

        blocks[qnum] = (preamble + raw_clean).strip()

    return blocks


# ── part / calculator detection ───────────────────────────────────────────────

def _detect_part_calculator(body: str, starts: list[tuple[int, int]]) -> dict[int, tuple[bool, str]]:
    """
    Return {qnum: (calculator_active, part)} based on section header markers.
    Falls back to standard AP BC default (Q1-3 Part A, Q4-6 Part B).
    """
    default: dict[int, tuple[bool, str]] = {
        1: (True, "A"), 2: (True, "A"), 3: (True, "A"),
        4: (False, "B"), 5: (False, "B"), 6: (False, "B"),
    }

    # Build list of (position, calc, part) transitions from section markers
    transitions: list[tuple[int, bool, str]] = []
    for m in re.finditer(r"\\section\*\{([^}]+)\}", body):
        text = m.group(1).upper()
        pos = m.start()
        if "END OF PART A" in text:
            transitions.append((pos, False, "B"))
        elif "NO CALCULATOR" in text or "NOT ALLOWED" in text:
            transitions.append((pos, False, "B"))
    # Also catch plain-text "No calculator is allowed" (some years)
    for m in re.finditer(r"No calculator is allowed", body, re.IGNORECASE):
        transitions.append((m.start(), False, "B"))

    if not transitions:
        return default

    result: dict[int, tuple[bool, str]] = dict(default)
    for qpos, qnum in starts:
        before = [(tpos, tcalc, tpart) for tpos, tcalc, tpart in transitions if tpos < qpos]
        if before:
            _, calc, part = max(before, key=lambda x: x[0])
            result[qnum] = (calc, part)
    return result


# ── text cleanup ──────────────────────────────────────────────────────────────

_BOILERPLATE_ENV_RE = re.compile(
    r"\\begin\{displayquote\}.*?\\end\{displayquote\}", re.DOTALL
)

_BOILERPLATE_SECTION_TITLES = re.compile(
    r"\\section\*\{(?:"
    r"The College Board[^}]*"
    r"|Permission to Reprint[^}]*"
    r"|Equity Policy[^}]*"
    r"|For further information[^}]*"
    r"|REMEMBER TO SHOW[^}]*"
    r"|WRITE ALL WORK[^}]*"
    r"|END OF(?:PART A)?[^}]*"
    r"|STOP[^}]*"
    r")\}",
    re.IGNORECASE,
)


def _remove_boilerplate_sections(tex: str) -> str:
    """Remove copyright/instruction blocks that appear before question content."""
    tex = _BOILERPLATE_ENV_RE.sub("", tex)
    # Remove boilerplate \section* lines (just the command line, keep following content)
    tex = _BOILERPLATE_SECTION_TITLES.sub("", tex)
    return tex


def _strip_command_with_braces(text: str, cmd: str) -> str:
    """
    Remove all occurrences of \\cmd{...} using brace-depth counting.

    Handles nested braces and multi-line titles correctly.
    """
    needle = f"\\{cmd}" + "{"
    result: list[str] = []
    i = 0
    while i < len(text):
        if text[i:i + len(needle)] == needle:
            brace_start = i + len(needle) - 1  # position of opening {
            depth = 0
            j = brace_start
            while j < len(text):
                if text[j] == "{":
                    depth += 1
                elif text[j] == "}":
                    depth -= 1
                    if depth == 0:
                        j += 1
                        break
                j += 1
            # Skip trailing whitespace / newline
            while j < len(text) and text[j] in " \t\n":
                j += 1
            i = j
        else:
            result.append(text[i])
            i += 1
    return "".join(result)


def _clean_block(text: str) -> str:
    """Strip enumerate/section noise and normalize whitespace within a block."""
    text = _strip_command_with_braces(text, "section*")
    text = _strip_command_with_braces(text, "section")
    text = re.sub(r"\\(?:begin|end)\{enumerate\}\s*", "", text)
    text = re.sub(r"\\setcounter\{enumi\}\{\d+\}\s*", "", text)
    text = re.sub(r"\r\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


_EXAM_BOILERPLATE_RE = re.compile(
    r"(?m)^[^\n]*"                           # start of any line
    r"(?:"
    r"©\s*\d{4}|Copyright\s*©"              # copyright symbol
    r"|All rights reserved"                  # rights notice
    r"|apcentral\.collegeboard|collegeboard\.com|collegeboard\.org"  # URLs
    r"|CALCULUS BC\b|AP\s+CALCULUS"          # exam header
    r"|SECTION\s+II\b"                       # section header
    r"|Time[\s\-—]\d"                        # time notice  e.g. "Time-45 minutes"
    r"|Number of (?:questions|problems)"
    r"|Percent of total"
    r"|REMEMBER TO SHOW|WRITE ALL WORK"
    r"|END OF (?:PART|SECTION|EXAM)"
    r"|Note:\s*Use the axes"                 # common exam note
    r")"
    r"[^\n]*$"                               # rest of line
    r"(?:\n|$)",
    re.IGNORECASE,
)


_ABOVE_REF_RE = re.compile(
    r"(?:in the |the )?(?:figure|graph|table|diagram|curve)\s+above|shown\s+above",
    re.IGNORECASE,
)
_VISUAL_ELEMENT_RE = re.compile(
    r"\\includegraphics|\\begin\{center\}|\\begin\{tabular\}",
)


def _fix_above_below_language(text: str) -> str:
    """
    When question text says 'figure/table above' but there is no visual element
    (figure or table) before that reference, replace 'above' with 'below'.

    This handles cases where Mathpix placed the reference figure/table after the
    question text (e.g. inside a \\part body that follows).
    """
    result: list[str] = []
    last = 0
    for m in _ABOVE_REF_RE.finditer(text):
        before_ref = text[last:m.start()]
        result.append(before_ref)
        # Check whether a visual element appears anywhere before this reference
        has_visual_before = bool(_VISUAL_ELEMENT_RE.search(text[:m.start()]))
        matched = m.group(0)
        if not has_visual_before:
            # Change 'above' → 'below' since the figure/table follows the text
            matched = re.sub(r"\babove\b", "below", matched, flags=re.IGNORECASE)
        result.append(matched)
        last = m.end()
    result.append(text[last:])
    return "".join(result)


def _clean_exam_question(text: str) -> str:
    text = _clean_block(text)
    text = re.sub(r"\\graphicspath\{[^}]+\}\s*", "", text)
    text = re.sub(r"(?:\\end\{document\}|\\begin\{document\})\s*$", "", text).rstrip()
    text = re.sub(r"\\href\{[^}]+\}\{([^}]+)\}", r"\1", text)
    text = re.sub(r"\\footnotetext\{.*?\}", "", text, flags=re.DOTALL)
    text = re.sub(r"\\urlstyle\{[^}]+\}\s*", "", text)
    text = _EXAM_BOILERPLATE_RE.sub("", text)
    # Strip float wrappers — invalid inside \begin{parts}; keep inner includegraphics
    text = re.sub(r"\\begin\{figure\}(?:\[[^\]]*\])?\s*", "", text)
    text = re.sub(r"\\end\{figure\}\s*", "", text)
    text = re.sub(r"\\begin\{table\}(?:\[[^\]]*\])?\s*", "", text)
    text = re.sub(r"\\end\{table\}\s*", "", text)
    text = _strip_command_with_braces(text, "captionsetup")
    text = _strip_command_with_braces(text, "caption")
    # Wrap bare \includegraphics (not already inside \begin{center}) in a center env
    text = _center_bare_figures(text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


_BARE_FIGURE_RE = re.compile(
    r"\\includegraphics(?:\[[^\]]*\])?\{[^}]+\}(?:\\\\)?"  # figure + optional trailing \\
)


def _center_bare_figures(text: str) -> str:
    """Wrap \\includegraphics not already inside \\begin{center} with a center env."""
    result: list[str] = []
    last = 0
    for m in _BARE_FIGURE_RE.finditer(text):
        before = text[last:m.start()]
        preceding = text[max(0, m.start() - 60) : m.start()]
        # Strip the optional trailing \\ from the match so it doesn't appear after \end{center}
        fig_cmd = re.sub(r"\\\\$", "", m.group(0))
        if "\\begin{center}" in preceding and "\\end{center}" not in preceding:
            result.append(before)
            result.append(fig_cmd)
        else:
            result.append(before)
            result.append(f"\\begin{{center}}\n{fig_cmd}\n\\end{{center}}")
        last = m.end()
    result.append(text[last:])
    return "".join(result)


_UUID_FIGURE_RE = re.compile(
    r"(?:\\begin\{center\}\s*)?"
    r"\\includegraphics(?:\[[^\]]*\])?\{[a-f0-9]{8}-[a-f0-9]{4}[^}]*\}[^\n]*"
    r"(?:\s*\\end\{center\})?",
    re.IGNORECASE,
)


_PART_A_RE = re.compile(r"(?m)^[ \t]*\(a\)")


def _strip_sg_question_preamble(text: str) -> str:
    """
    Strip the question statement that appears at the top of SG blocks in 1998–2017.

    The SG format for those years repeats the question: context paragraph, then
    (a) question text\\, (b) question text\\, ..., then (a) solution, (b) solution, ...

    The second occurrence of '^(a)' at line-start is where the solution begins.
    For 2018+ the SG already starts with '(a) solution', so there is only one
    occurrence and nothing is stripped.
    """
    matches = list(_PART_A_RE.finditer(text))
    if len(matches) < 2:
        return text
    return text[matches[1].start():].strip()


def _clean_sg_block(text: str) -> str:
    text = _clean_block(text)
    text = re.sub(r"\\href\{[^}]+\}\{([^}]+)\}", r"\1", text)
    text = re.sub(r"\\footnotetext\{.*?\}", "", text, flags=re.DOTALL)
    text = re.sub(r"^\\item\s*", "", text)
    text = re.sub(r"(?:\\end\{document\}|\\begin\{document\})\s*$", "", text).rstrip()
    # Strip list environments — may be split across section boundaries
    text = re.sub(r"\\(?:begin|end)\{(?:itemize|enumerate)\}\s*", "", text)
    text = re.sub(r"\\item\s*", "", text)
    # Strip float wrappers first (before UUID figure removal so center blocks are bare)
    text = re.sub(r"\\begin\{figure\}(?:\[[^\]]*\])?\s*", "", text)
    text = re.sub(r"\\end\{figure\}\s*", "", text)
    text = re.sub(r"\\begin\{table\}(?:\[[^\]]*\])?\s*", "", text)
    text = re.sub(r"\\end\{table\}\s*", "", text)
    # Strip caption commands (with brace counting for nested math)
    text = _strip_command_with_braces(text, "captionsetup")
    text = _strip_command_with_braces(text, "caption")
    # Now remove UUID \includegraphics with their \begin{center}...\end{center} wrappers
    text = _UUID_FIGURE_RE.sub("", text)
    # Strip empty center environments left behind
    text = re.sub(r"\\begin\{center\}\s*\\end\{center\}", "", text)
    # Balance any remaining unpaired center tags
    n_begin = len(re.findall(r"\\begin\{center\}", text))
    n_end = len(re.findall(r"\\end\{center\}", text))
    diff = n_end - n_begin
    if diff > 0:
        for _ in range(diff):
            text = re.sub(r"\\end\{center\}\s*", "", text, count=1)
    elif diff < 0:
        text = text.rstrip() + "\n\\end{center}" * (-diff)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = _strip_sg_question_preamble(text)
    return text.strip()


# ── public API ────────────────────────────────────────────────────────────────

def parse_exam_zip(
    zip_path: str,
    figures_dir: str,
    year: int,
    form: str = "",
) -> dict[int, ExamQuestion]:
    """
    Parse a Mathpix exam zip into ExamQuestion records.

    Args:
        zip_path:    Path to BC-YEAR.zip or BC-YEAR-FORM-B.zip
        figures_dir: Directory to save extracted figure images
        year:        Four-digit exam year
        form:        "" for standard, "B" for Form B
    """
    tex, images = _load_zip(zip_path)
    tex = _strip_header(tex)
    tex = _remove_boilerplate_sections(tex)

    form_tag = "-form-b" if form.upper() == "B" else ""
    prefix = f"bc-{year}{form_tag}"

    tex, fig_paths = _extract_and_save_figures(tex, images, figures_dir, prefix)

    # Wrap figures in \begin{center}...\end{center} BEFORE block extraction so
    # _find_tail_preamble can detect inter-question figures and assign them to
    # the correct question's intro (e.g. a graph shown before "5. A car is...")
    tex = _center_bare_figures(tex)

    starts = _find_question_starts(tex)
    if not starts:
        return {}

    part_calc = _detect_part_calculator(tex, starts)
    raw_blocks = _extract_blocks(tex, starts)

    questions: dict[int, ExamQuestion] = {}
    for qnum, raw in raw_blocks.items():
        calc, part = part_calc.get(qnum, (qnum <= 3, "A" if qnum <= 3 else "B"))

        # Associate figure paths with this question block
        refs = set(re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", raw))
        q_figs = [p for p in fig_paths if any(Path(p).stem in r or r in Path(p).stem for r in refs)]

        questions[qnum] = ExamQuestion(
            question_number=qnum,
            question_text=_clean_exam_question(raw),
            figure_paths=q_figs,
            calculator_active=calc,
            part=part,
        )

    # Content (figures, tables) that appeared before the first question marker in
    # Mathpix is not captured by block extraction.  Two cases:
    #
    # 1. Orphan IMAGES: figures saved to fig_paths but not assigned to any block.
    # 2. Orphan TABLES: \begin{center}\begin{tabular}...\end{tabular}\end{center}
    #    blocks in the tex before the first question position (e.g. 2012/2016/2017 Q1).
    #
    # Both are prepended to Q1's question text so "the table/figure above" language
    # in Q1's question body is visually correct.
    if 1 in questions:
        q1 = questions[1]
        extra_prefix_parts: list[str] = []

        # Orphan images
        assigned = {p for q in questions.values() for p in q.figure_paths}
        orphan_figs = [p for p in fig_paths if p not in assigned]
        for p in orphan_figs:
            extra_prefix_parts.append(
                f"\\begin{{center}}\n\\includegraphics[width=0.8\\linewidth]{{{p}}}\n\\end{{center}}"
            )

        # Orphan tables (before first question position)
        if starts:
            first_pos = starts[0][0]
            pre_q = tex[:first_pos]
            # Find center-wrapped blocks containing tabular content
            for m in re.finditer(r"\\begin\{center\}(.*?)\\end\{center\}", pre_q, re.DOTALL):
                inner = m.group(1)
                if "\\begin{tabular}" in inner or "\\begin{array}" in inner:
                    block = _clean_block(m.group(0))
                    if block:
                        extra_prefix_parts.append(block)

        if extra_prefix_parts:
            prefix = "\n".join(extra_prefix_parts)
            questions[1] = ExamQuestion(
                question_number=q1.question_number,
                question_text=(prefix + "\n" + q1.question_text).strip(),
                figure_paths=orphan_figs + q1.figure_paths,
                calculator_active=q1.calculator_active,
                part=q1.part,
            )

    # Fix directional language ("figure above") once all orphan content is in place.
    for qnum, q in questions.items():
        fixed = _fix_above_below_language(q.question_text)
        if fixed != q.question_text:
            questions[qnum] = ExamQuestion(
                question_number=q.question_number,
                question_text=fixed,
                figure_paths=q.figure_paths,
                calculator_active=q.calculator_active,
                part=q.part,
            )

    return questions


def parse_sg_zip(zip_path: str) -> dict[int, str]:
    """
    Parse a Mathpix scoring guide zip into {question_number: combined_sg_text}.

    The returned text is the solution + rubric for each question, ready to drop
    into a \\begin{solution}...\\end{solution} block.
    """
    tex, _images = _load_zip(zip_path)
    tex = _strip_header(tex)
    tex = _remove_boilerplate_sections(tex)

    # Detect format by presence of \section*{Question N}
    if re.search(r"\\section\*\{(?:[^}]*\s)?Question\s+\d+", tex, re.IGNORECASE):
        return _parse_sg_new(tex)
    return _parse_sg_old(tex)


def _parse_sg_new(tex: str) -> dict[int, str]:
    """Parse 2000+ SG format: \\section*{Question N} or \\caption{Question N} delimiters."""
    repeating_header = re.compile(
        r"\\section\*\{AP[^}]*(?:SCORING GUIDELINES|CALCULUS)[^}]*\}",
        re.IGNORECASE,
    )
    tex = repeating_header.sub("", tex)

    # Match both \section*{...Question N...} and \caption{Question N}
    pattern = re.compile(
        r"(?:\\section\*\{[^}]*Question\s+(\d+)[^}]*\}|\\caption\{Question\s+(\d+)\})",
        re.IGNORECASE,
    )
    raw_matches = list(pattern.finditer(tex))
    # Normalise: each match → (position, question_number)
    matches = []
    for m in raw_matches:
        qnum = int(m.group(1) or m.group(2))
        matches.append((m.start(), m.end(), qnum))
    if not matches:
        return {}

    result: dict[int, str] = {}
    for i, (mstart, mend, qnum) in enumerate(matches):
        start = mend
        end = matches[i + 1][0] if i + 1 < len(matches) else len(tex)
        block = _clean_sg_block(tex[start:end])
        if block:
            result[qnum] = block

    return result


def _parse_sg_old(tex: str) -> dict[int, str]:
    """Parse 1998-1999 SG format: questions via \\item and plain 'N. text'."""
    starts = _find_question_starts(tex)
    if not starts:
        return {}
    raw_blocks = _extract_blocks(tex, starts)
    return {
        qnum: _clean_sg_block(raw)
        for qnum, raw in raw_blocks.items()
        if _clean_sg_block(raw)
    }
