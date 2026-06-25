#!/usr/bin/env python3
"""
Convert a Mathpix-processed Manitoba Pre-Calc 40S zip into an exam-class LaTeX file
matching the format of outputs/ap-calculus-bc/latex/output_frq.tex.

Usage:
    python tools/manitoba-precalc-40s/convert_precalc_zip.py <zip_file> [output_tex]

Example:
    python tools/manitoba-precalc-40s/convert_precalc_zip.py data/legacy/manitoba-prototype-mathpix/raw-mathpix/pre-calc-40s_jan_13_mg-only_cleaned_aggressive.zip
"""

import re
import sys
import zipfile
from pathlib import Path


# ── Preamble matching output_frq.tex ──────────────────────────────────────────

_PREAMBLE = r"""\documentclass[12pt,addpoints,answers]{exam}
\usepackage[margin=1in]{geometry}
\usepackage{amsmath,amssymb,amsfonts}
\usepackage{graphicx}
\usepackage{multirow}
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\printanswers
\unframedsolutions
\renewcommand{\solutiontitle}{}

\begin{document}
"""

_POSTAMBLE = "\n\\end{document}\n"


# ── ZIP extraction ─────────────────────────────────────────────────────────────

def extract_zip(zip_path: Path, output_dir: Path) -> tuple[str, Path]:
    """Extract zip; return (tex_content, images_dir)."""
    images_dir = output_dir / "figures"
    images_dir.mkdir(parents=True, exist_ok=True)

    tex_content = None
    with zipfile.ZipFile(zip_path) as zf:
        for name in zf.namelist():
            if name.endswith(".tex"):
                tex_content = zf.read(name).decode("utf-8")
            elif "/images/" in name and not name.endswith("/"):
                basename = Path(name).name
                dest = images_dir / basename
                dest.write_bytes(zf.read(name))

    if tex_content is None:
        raise ValueError(f"No .tex file found inside {zip_path}")
    return tex_content, images_dir


# ── LaTeX cleanup helpers ──────────────────────────────────────────────────────

def extract_body(tex: str) -> str:
    """Return content between \\begin{document} and \\end{document}."""
    m = re.search(r"\\begin\{document\}(.*?)\\end\{document\}", tex, re.DOTALL)
    body = m.group(1) if m else tex
    body = re.sub(r"\\captionsetup\{[^}]*\}\n?", "", body)
    return body.strip()


def fix_images(text: str, figures_subdir: str = "figures") -> str:
    """Normalise \\includegraphics to a clean width + figures/ path."""
    def repl(m: re.Match) -> str:
        name = Path(m.group(2)).name  # drop any subdirectory prefix
        return rf"\includegraphics[width=0.6\linewidth]{{{figures_subdir}/{name}}}"

    return re.sub(
        r"\\includegraphics\[[^\]]*\]\{([^}]+)\}",
        lambda m: (
            rf"\includegraphics[width=0.6\linewidth]"
            rf"{{{figures_subdir}/{Path(m.group(1)).name}}}"
        ),
        text,
    )


def clean_section_headers(text: str) -> str:
    """Convert \\section*{...} rubric/method labels to inline \\textbf."""
    # Method headers → bold
    text = re.sub(
        r"\\section\*\{(Method \d+|Solutions?)\}\s*",
        r"\n\\textbf{\1}\\par\n",
        text,
    )
    # Any \section*{...mark...} rubric-total headers → drop
    text = re.sub(r"\\section\*\{[^}]*\bmarks?\b[^}]*\}\s*", "", text, flags=re.IGNORECASE)
    # "Question N" section headers → drop
    text = re.sub(r"\\section\*\{Question \d+\}\s*", "", text)
    # R-code artefacts like \nR8\n → drop
    text = re.sub(r"\nR\d+\s*\n", "\n", text)
    return text


def clean_question_preamble(text: str) -> str:
    """Remove artefacts that appear at the top of some question blocks."""
    # "Question NN\nRN" artefacts
    text = re.sub(r"^Question \d+\s*\nR\d+\s*\n", "", text, flags=re.MULTILINE)
    text = re.sub(r"^Question \d+\s*\n", "", text, flags=re.MULTILINE)
    # Rubric section headers that leaked through boundary detection
    text = re.sub(r"\\section\*\{[^}]*\bmarks?\b[^}]*\}\s*\n?", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\\section\*\{Question \d+\}\s*\n?", "", text)
    # Method headers that leaked (e.g. when merge_extra_solution_markers missed something)
    text = re.sub(r"\\section\*\{Method \d+\}\s*\n?", "", text)
    return text.strip()


# ── Question/solution splitting ────────────────────────────────────────────────

# Standalone total-marks line ("3 marks" alone on a line) OR \section*{N marks} header.
_TOTAL_MARKS_RE = re.compile(
    r"(?m)^[ \t]*\d+(?:\.\d+)?[ \t]+marks?[ \t]*$"
    r"|\\section\*\{[ \t]*\d+(?:\.\d+)?[ \t]+marks?[ \t]*\}",
    re.IGNORECASE,
)
_END_ITEMIZE_RE = re.compile(r"\\end\{itemize\}")


def _advance_past_blanks(text: str, pos: int) -> int:
    """Skip whitespace-only content from pos and return first non-WS position."""
    m = re.search(r"\S", text[pos:])
    return pos + m.start() if m else len(text)


def find_boundary(chunk: str) -> int:
    """
    Within `chunk` (solution content followed by the next question's text),
    return the index where the next question begins.
    """
    # --- Strategy 1: last standalone "N marks" line, then optional Notes block ---
    marks_matches = list(_TOTAL_MARKS_RE.finditer(chunk))
    if marks_matches:
        pos = marks_matches[-1].end()

        # Absorb any following Notes / \begin{itemize}...\end{itemize}
        notes_m = re.search(r"Note\(?s?\)?:", chunk[pos:], re.IGNORECASE)
        if notes_m and notes_m.start() < 300:
            end_item_m = _END_ITEMIZE_RE.search(chunk, pos + notes_m.start())
            if end_item_m:
                pos = end_item_m.end()

        # Absorb any "or\n<alternative answer>\n" clauses that follow marks
        # (common in 1-mark questions where two equivalent forms are shown)
        while True:
            rest = chunk[pos:]
            or_m = re.match(r"\s*\n\s*or\s*\n\s*", rest, re.IGNORECASE)
            if not or_m:
                break
            after_or = pos + or_m.end()
            blank_m = re.search(r"\n\s*\n", chunk[after_or:])
            if blank_m:
                pos = after_or + blank_m.end()
            else:
                pos = after_or
                break

        return _advance_past_blanks(chunk, pos)

    # --- Strategy 2: last \end{itemize} (Notes without a marks total) ---
    item_matches = list(_END_ITEMIZE_RE.finditer(chunk))
    if item_matches:
        pos = item_matches[-1].end()
        return _advance_past_blanks(chunk, pos)

    # --- Strategy 3: locate the end of the solution using mark annotations ---
    # Find the last $$...$$  block that contains inline "mark" annotations.
    # If a \section*{Method N} follows that block, advance past the last method's
    # final env-end instead (handles multi-method solutions with no marks total
    # in the later methods).

    # Collect all display-math block spans
    math_blocks = list(re.finditer(r"\$\$(.*?)\$\$", chunk, re.DOTALL))
    # Pattern for inline mark annotations (inside \text{...} or bare)
    _MARK_ANNO = re.compile(r"\bmarks?\b", re.IGNORECASE)

    # Find the last math block that contains a mark annotation
    last_mark_block_end = None
    for blk in math_blocks:
        if _MARK_ANNO.search(blk.group(1)):
            last_mark_block_end = blk.end()

    if last_mark_block_end is not None:
        # Check whether a \section*{Method N} label appears AFTER this block.
        # If so, more solution content follows → advance past the last method's
        # trailing environment instead.
        method_after = list(
            re.finditer(r"\\section\*\{Method \d+\}", chunk[last_mark_block_end:])
        )
        if method_after:
            # Position of last \section*{Method N} in the chunk
            last_method_abs = last_mark_block_end + method_after[-1].start()
            # Find the last $$ or \end{...} after that method label
            env_after_method = list(re.finditer(
                r"(?:\\end\{[^}]+\}|\$\$)\s*\n",
                chunk[last_method_abs:]
            ))
            if env_after_method:
                pos = last_method_abs + env_after_method[-1].end()
                return _advance_past_blanks(chunk, pos)

        # No further methods: next question starts after last mark block
        return _advance_past_blanks(chunk, last_mark_block_end)

    # --- Fallback: give up, treat entire chunk as solution ---
    return len(chunk)


def merge_method_continuations(pairs: list[dict]) -> list[dict]:
    """
    Some questions (e.g. Q13 trig identity, Q34 sinusoidal) have a spurious
    extra \\section*{Solution} header before a later method, which causes the
    split to create extra pairs whose 'question' is actually solution content.

    Detect those pairs (question is empty OR starts with \\section*{Method})
    and fold them back into the preceding pair's solution.
    """
    merged: list[dict] = []
    for pair in pairs:
        q = pair["question"].strip()
        is_continuation = not q or bool(re.match(r"\\section\*\{Method", q))
        if merged and is_continuation:
            prev = merged[-1]
            if q:
                prev["solution"] = (prev["solution"] + "\n\n" + q).strip()
            if pair["solution"]:
                prev["solution"] = (prev["solution"] + "\n\n" + pair["solution"]).strip()
        else:
            merged.append(pair)
    return merged


def split_into_pairs(body: str) -> list[dict]:
    """
    Parse the Mathpix document body into a list of
      {'question': str, 'solution': str}
    by splitting on \\section*{Solution} boundaries.
    """
    parts = re.split(r"\\section\*\{Solutions?\}", body)

    pairs: list[dict] = []
    pending_q = parts[0].strip()

    for i in range(1, len(parts)):
        chunk = parts[i]
        boundary = find_boundary(chunk)
        sol_text = chunk[:boundary].strip()
        next_q = chunk[boundary:].strip()

        # If pending_q contains MCQ questions followed by an FRQ, emit the MCQ
        # questions first and keep only the FRQ text as this pair's question.
        mcq_prefix, actual_q = split_mcq_and_remaining(pending_q)
        pairs.extend(mcq_prefix)
        pairs.append({"question": actual_q, "solution": sol_text})
        pending_q = next_q

    # Handle remaining content after the last solution
    if pending_q.strip():
        pairs.extend(split_mcq_block(pending_q))

    return merge_method_continuations(pairs)


# ── MCQ detection & splitting ─────────────────────────────────────────────────

# Detect "a) ...\nb) ...\nc) ...\nd) ..." choice blocks.
_CHOICE_LINE_RE = re.compile(
    r"(?m)^(?:[ \t]*([a-d])\)[ \t]+(.+?)(?=\n[a-d]\)|$))",
    re.DOTALL,
)


def detect_mcq(text: str) -> tuple[str, list[tuple[str, str]]]:
    """
    Return (body_without_choices, [(label, text), ...]).
    If fewer than 2 choices found, returns (text, []).
    """
    matches = list(_CHOICE_LINE_RE.finditer(text))
    if len(matches) < 2:
        return text, []

    body = text[: matches[0].start()].strip()
    choices = []
    for m in matches:
        label = m.group(1).upper()
        choice_text = m.group(2).strip().rstrip("\\").strip()
        choices.append((label, choice_text))
    return body, choices


# ── MCQ block sub-splitting ───────────────────────────────────────────────────

def _mcq_split_paras(text: str) -> tuple[list[dict], str]:
    """
    Core paragraph accumulator: returns (mcq_pairs, leftover_text).
    MCQ questions are emitted once 2+ letter choices are detected;
    any trailing paragraphs without detected choices stay in leftover.
    """
    paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    questions: list[dict] = []
    current: list[str] = []

    for para in paras:
        current.append(para)
        body = "\n\n".join(current)
        _, choices = detect_mcq(body)
        if len(choices) >= 2:
            questions.append({"question": body, "solution": ""})
            current = []

    leftover = "\n\n".join(current).strip()
    return questions, leftover


def split_mcq_block(text: str) -> list[dict]:
    """
    Split a block of consecutive MCQ questions (no solution) into individual
    question dicts.  Any trailing non-MCQ text becomes a plain FRQ entry.
    """
    mcq_pairs, leftover = _mcq_split_paras(text)
    if leftover:
        if mcq_pairs:
            mcq_pairs[-1]["question"] = (
                mcq_pairs[-1]["question"] + "\n\n" + leftover
            )
        else:
            mcq_pairs.append({"question": leftover, "solution": ""})
    return mcq_pairs


def split_mcq_and_remaining(text: str) -> tuple[list[dict], str]:
    """
    Extract MCQ questions from `text`, returning (mcq_pairs, remaining_frq_text).
    Used when pending_q may contain a prefix of MCQ questions followed by an FRQ
    question whose solution will be assigned by the caller.
    """
    return _mcq_split_paras(text)


# ── Rendering ─────────────────────────────────────────────────────────────────

def render_question(q_num: int, q: dict, label: str, figures_subdir: str) -> str:
    """Render one question/solution pair as exam-class LaTeX."""
    lines: list[str] = []
    lines.append(r"\question")
    lines.append(r"\leavevmode")
    lines.append(f"% Q{q_num} | {label}")

    q_text = fix_images(q["question"], figures_subdir)
    q_text = clean_question_preamble(q_text)
    # Remove \begin{figure}...\end{figure} wrappers but keep the includegraphics
    q_text = re.sub(
        r"\\begin\{figure\}\[h\]\s*\\begin\{center\}\s*"
        r"\\captionsetup\{labelformat=empty\}\s*"
        r"\\caption\{([^}]*)\}\s*"
        r"(\\includegraphics[^\n]+)\s*"
        r"\\end\{center\}\s*\\end\{figure\}",
        r"\1\\\\\n\2",
        q_text,
        flags=re.DOTALL,
    )

    q_body, choices = detect_mcq(q_text)
    lines.append(q_body)

    if choices:
        lines.append(r"\begin{choices}")
        for _label, ctext in choices:
            lines.append(rf"\choice {ctext}")
        lines.append(r"\end{choices}")

    sol = q.get("solution", "").strip()
    if sol:
        sol = fix_images(sol, figures_subdir)
        sol = clean_section_headers(sol)
        # Remove \begin{figure}...\end{figure} wrappers in solutions too
        sol = re.sub(
            r"\\begin\{figure\}\[h\]\s*\\begin\{center\}\s*"
            r"(?:\\captionsetup\{labelformat=empty\}\s*\\caption\{[^}]*\}\s*)?"
            r"(\\includegraphics[^\n]+)\s*"
            r"\\end\{center\}\s*\\end\{figure\}",
            r"\\begin{center}\1\\end{center}",
            sol,
            flags=re.DOTALL,
        )
        lines.append(r"\begin{solution}")
        lines.append(r"\textbf{Solution:}\par")
        lines.append(sol)
        lines.append(r"\end{solution}")

    return "\n".join(lines)


# ── Section title from zip filename ───────────────────────────────────────────

_MONTH_MAP = {
    "jan": "January", "feb": "February", "mar": "March",
    "apr": "April", "may": "May", "jun": "June",
    "jul": "July", "aug": "August", "sep": "September",
    "oct": "October", "nov": "November", "dec": "December",
}


def zip_to_section_title(zip_path: Path) -> str:
    """
    'pre-calc-40s_jan_13_mg-only_cleaned_aggressive.zip'
    → 'Pre-Calculus 40S --- January 2013'
    """
    stem = zip_path.stem  # e.g. pre-calc-40s_jan_13_mg-only_cleaned_aggressive
    parts = stem.split("_")
    # Find month/year tokens
    month = year = None
    for i, p in enumerate(parts):
        if p.lower() in _MONTH_MAP:
            month = _MONTH_MAP[p.lower()]
            if i + 1 < len(parts) and re.fullmatch(r"\d{2,4}", parts[i + 1]):
                yr = parts[i + 1]
                year = f"20{yr}" if len(yr) == 2 else yr
    if month and year:
        return rf"Pre-Calculus 40S --- {month} {year}"
    return "Pre-Calculus 40S"


# ── Main ──────────────────────────────────────────────────────────────────────

def convert(zip_path: Path, output_tex: Path) -> None:
    output_dir = output_tex.parent
    figures_subdir = "figures"

    print(f"Extracting {zip_path.name} ...")
    tex_content, images_dir = extract_zip(zip_path, output_dir)
    print(f"  → images extracted to {images_dir}")

    body = extract_body(tex_content)
    raw_pairs = split_into_pairs(body)
    print(f"  → {len(raw_pairs)} raw question blocks found")

    section_title = zip_to_section_title(zip_path)

    # Expand any blocks that look like MCQ-only (no solution) into individual Qs
    pairs: list[dict] = []
    for pair in raw_pairs:
        if not pair["solution"].strip():
            sub = split_mcq_block(pair["question"])
            pairs.extend(sub)
        else:
            pairs.append(pair)

    label = section_title
    doc_lines: list[str] = []
    doc_lines.append(rf"\section*{{{section_title}}}")
    doc_lines.append("")
    doc_lines.append(r"\begin{questions}")
    doc_lines.append("")

    for i, pair in enumerate(pairs, start=1):
        doc_lines.append(render_question(i, pair, label, figures_subdir))
        doc_lines.append("")

    doc_lines.append(r"\end{questions}")

    content = _PREAMBLE + "\n".join(doc_lines) + _POSTAMBLE
    output_tex.write_text(content, encoding="utf-8")
    print(f"  → wrote {output_tex}  ({len(pairs)} questions)")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    zip_file = Path(sys.argv[1])
    if not zip_file.exists():
        print(f"Error: {zip_file} not found")
        sys.exit(1)

    # Default output alongside the existing output_frq.tex
    default_out = Path("outputs") / "manitoba-precalc-40s" / "latex" / (
        zip_file.stem.replace("_mg-only_cleaned_aggressive", "") + ".tex"
    )
    out_tex = Path(sys.argv[2]) if len(sys.argv) > 2 else default_out
    out_tex.parent.mkdir(parents=True, exist_ok=True)

    convert(zip_file, out_tex)
