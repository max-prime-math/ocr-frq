#!/usr/bin/env python3
"""Export a small Manitoba PQP sample from Mathpix API artifacts."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import tempfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

from jsonschema import Draft202012Validator

from manitoba_mathpix_common import CACHE_DIR, MB_DIR, ROOT


CATALOG_JSON = MB_DIR / "catalog" / "question_catalog.json"
FILTER_REPORT_JSON = MB_DIR / "mathpix" / "api-inputs" / "page-filtered" / "page_filter_report.json"
OUT_DIR = MB_DIR / "derived" / "pqp-mathpix-sample"
SCHEMA_PATH = ROOT.parent / "docs" / "pqp" / "shared-question-package.schema.json"
MITEX = Path("/home/max/.cargo/bin/mitex")

IMAGE_MARKDOWN_RE = re.compile(
    r"!\[\]\(https://cdn\.mathpix\.com/cropped/(?P<base>[^?]+)\?"
    r"height=(?P<height>\d+)&width=(?P<width>\d+)&top_left_y=(?P<y>\d+)&top_left_x=(?P<x>\d+)\)"
)
CROP_URL_RE = re.compile(
    r"https://cdn\.mathpix\.com/cropped/(?P<base>[^?\"}\s]+)\?"
    r"height=(?P<height>\d+)\s*(?:&|\|)\s*width=(?P<width>\d+)\s*"
    r"(?:&|\|)\s*top_left_y=(?P<y>\d+)\s*(?:&|\|)\s*top_left_x=(?P<x>\d+)"
)
QUESTION_MARKER_RE = re.compile(r"^\s*Question\s+(?P<num>\d{1,2})\b(?P<tail>.*)$", re.I)
CHOICE_LABEL_RE = re.compile(r"^\s*([a-dA-D])[\).]\s*(.*)$", re.S)
INLINE_CHOICE_LABEL_RE = re.compile(r"(?<![A-Za-z0-9])([a-dA-D])[\).]\s+")

COURSE_ID = "pre-calculus-40s"
COURSE_NAME = "Pre-Calculus 40S"
COURSE_CODE = "3939"
CURRICULUM_SOURCE_URL = "https://www.edu.gov.mb.ca/k12/framework/english/math/grade_12/precal.html"

CURRICULUM_UNITS = [
    {
        "id": "trigonometry",
        "name": "Trigonometry",
        "glo": "Develop trigonometric reasoning.",
        "sections": [
            ("12P.T.1", "Demonstrate an understanding of angles in standard position, expressed in degrees and radians."),
            ("12P.T.2", "Develop and apply the equation of the unit circle."),
            ("12P.T.3", "Solve problems, using the six trigonometric ratios for angles expressed in radians and degrees."),
            ("12P.T.4", "Graph and analyze the trigonometric functions sine, cosine, and tangent to solve problems."),
            ("12P.T.5", "Solve, algebraically and graphically, first- and second-degree trigonometric equations with the domain expressed in degrees and radians."),
            ("12P.T.6", "Prove trigonometric identities."),
        ],
    },
    {
        "id": "relations-and-functions",
        "name": "Relations and Functions",
        "glo": "Develop algebraic and graphical reasoning through the study of relations.",
        "sections": [
            ("12P.R.1", "Demonstrate an understanding of operations on, and compositions of, functions."),
            ("12P.R.2", "Demonstrate an understanding of the effects of horizontal and vertical translations on the graphs of functions and their related equations."),
            ("12P.R.3", "Demonstrate an understanding of the effects of horizontal and vertical compressions and stretches on the graphs of functions and their related equations."),
            ("12P.R.4", "Apply translations, compressions, and stretches to the graphs and equations of functions."),
            ("12P.R.5", "Demonstrate an understanding of the effects of reflections on the graphs of functions and their related equations."),
            ("12P.R.6", "Demonstrate an understanding of inverses of relations."),
            ("12P.R.7", "Demonstrate an understanding of logarithms."),
            ("12P.R.8", "Demonstrate an understanding of the product, quotient, and power laws of logarithms."),
            ("12P.R.9", "Graph and analyze exponential and logarithmic functions."),
            ("12P.R.10", "Solve problems that involve exponential and logarithmic equations."),
            ("12P.R.11", "Demonstrate an understanding of factoring polynomials of degree greater than 2."),
            ("12P.R.12", "Graph and analyze polynomial functions."),
            ("12P.R.13", "Graph and analyze radical functions."),
            ("12P.R.14", "Graph and analyze rational functions."),
        ],
    },
    {
        "id": "permutations-combinations-binomial-theorem",
        "name": "Permutations, Combinations, and Binomial Theorem",
        "glo": "Develop algebraic and numeric reasoning that involves combinatorics.",
        "sections": [
            ("12P.P.1", "Apply the fundamental counting principle to solve problems."),
            ("12P.P.2", "Determine the number of permutations of n elements taken r at a time to solve problems."),
            ("12P.P.3", "Determine the number of combinations of n different elements taken r at a time to solve problems."),
            ("12P.P.4", "Expand powers of a binomial in a variety of ways, including using the binomial theorem."),
        ],
    },
]

OUTCOMES: dict[str, dict[str, str]] = {}
for unit in CURRICULUM_UNITS:
    for section_id, section_name in unit["sections"]:
        OUTCOMES[section_id] = {
            "unitId": str(unit["id"]),
            "unitName": str(unit["name"]),
            "glo": str(unit["glo"]),
            "sectionId": section_id,
            "sectionName": f"{section_id}: {section_name}",
            "slo": section_name,
        }


def combination_typst(n: str, r: str) -> str:
    return f'""_({n.strip()}) C_({r.strip()})'


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def load_catalog(year: int, term: str, booklet: int | None) -> list[dict[str, Any]]:
    data = json.loads(CATALOG_JSON.read_text(encoding="utf-8"))
    rows = data["questions"] if isinstance(data, dict) and "questions" in data else data
    filtered = [row for row in rows if int(row["year"]) == year and row["term"] == term]
    if booklet is not None:
        filtered = [row for row in filtered if int(row["booklet"]) == booklet]
    return sorted(filtered, key=lambda row: int(row["question"]))


def load_filter_pages(doc_id: str) -> list[int]:
    report = json.loads(FILTER_REPORT_JSON.read_text(encoding="utf-8"))
    for row in report["rows"]:
        if row["id"] == doc_id:
            return [int(page) for page in row["keptOriginalPages"]]
    raise KeyError(f"No page-filter report row for {doc_id}")


def load_lines(doc_id: str) -> list[dict[str, Any]]:
    path = CACHE_DIR / doc_id / f"{doc_id}.lines.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    return data["pages"]


def image_width_fraction(match: re.Match[str], page: dict[str, Any]) -> float:
    page_width = float(page.get("page_width") or 0)
    crop_width = float(match.group("width"))
    if page_width <= 0:
        return 1.0
    return max(0.05, min(1.0, crop_width / page_width))


def image_latex(match: re.Match[str], page: dict[str, Any]) -> str:
    filename = image_filename_from_match(match)
    width = image_width_fraction(match, page)
    return rf"\includegraphics[width={width:.3f}\textwidth]{{assets/{filename}}}"


def page_text_and_images(page: dict[str, Any]) -> tuple[str, list[str]]:
    parts: list[str] = []
    images: list[str] = []
    for line in page.get("lines", []):
        if not line.get("conversion_output"):
            continue
        text = line.get("text") or line.get("text_display") or ""
        match = IMAGE_MARKDOWN_RE.search(text)
        if match:
            images.append(image_filename_from_match(match))
            parts.append(image_latex(match, page))
            continue
        if text.strip() == "Solution":
            continue
        parts.append(text.strip())
    return "\n\n".join(part for part in parts if part), images


def line_text(line: dict[str, Any]) -> str:
    return (line.get("text") or line.get("text_display") or "").strip()


def caption_text(text: str) -> str:
    captions = re.findall(r"\\caption\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}", text)
    cleaned: list[str] = []
    for caption in captions:
        caption = caption.replace(r"\(", "$").replace(r"\)", "$")
        caption = re.sub(r"\s+", " ", caption).strip()
        if caption:
            cleaned.append(caption)
    return " ".join(cleaned)


def strip_latex_figure_wrappers(text: str) -> str:
    text = re.sub(r"\\begin\{figure\}", " ", text)
    text = re.sub(r"\\end\{figure\}", " ", text)
    text = re.sub(r"\\captionsetup\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}", " ", text)
    text = re.sub(r"\\caption\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}", " ", text)
    text = re.sub(r"\\includegraphics(?:\[[^\]]*\])?\{https://cdn\.mathpix\.com/cropped/[^{}]+\}", " ", text)
    text = re.sub(r"!\[\]\(https://cdn\.mathpix\.com/cropped/[^)]+\)", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def text_line_items(text: str, page: dict[str, Any]) -> list[dict[str, str | float]]:
    text = text.strip()
    if not text or text == "Solution":
        return []

    matches = list(CROP_URL_RE.finditer(text))
    if matches:
        items: list[dict[str, str | float]] = []
        caption = caption_text(text)
        if caption:
            items.append({"kind": "text", "text": caption})
        remaining = strip_latex_figure_wrappers(text)
        if remaining:
            items.append({"kind": "text", "text": remaining})
        for match in matches:
            items.append(
                {
                    "kind": "image",
                    "text": image_filename_from_match(match),
                    "width": image_width_fraction(match, page),
                }
            )
        return items

    cleaned = strip_latex_figure_wrappers(text)
    return [{"kind": "text", "text": cleaned}] if cleaned else []


def page_items(page: dict[str, Any]) -> list[dict[str, str | float]]:
    items: list[dict[str, str | float]] = []
    for line in page.get("lines", []):
        if not line.get("conversion_output"):
            continue
        text = line_text(line)
        if not text or text == "Solution":
            continue
        if re.fullmatch(r"Question\s+\d+", text, re.I):
            continue
        items.extend(text_line_items(text, page))
    return items


def page_items_for_question(page: dict[str, Any], question_number: int) -> list[dict[str, str | float]]:
    items: list[dict[str, str | float]] = []
    started = False
    saw_marker = False
    for line in page.get("lines", []):
        text = line_text(line)
        if not text:
            continue
        marker = QUESTION_MARKER_RE.match(text)
        if marker:
            marker_question = int(marker.group("num"))
            if marker_question == question_number:
                started = True
                saw_marker = True
                tail = marker.group("tail").strip()
                if tail:
                    items.extend(text_line_items(tail, page))
                continue
            if started:
                break
            continue
        if not line.get("conversion_output"):
            continue
        if started:
            items.extend(text_line_items(text, page))

    return items if saw_marker else page_items(page)


def items_to_text_and_images(items: list[dict[str, str | float]]) -> tuple[str, list[str]]:
    parts: list[str] = []
    images: list[str] = []
    for item in items:
        if item["kind"] == "image":
            filename = str(item["text"])
            width = float(item.get("width") or 1.0)
            images.append(filename)
            parts.append(rf"\includegraphics[width={width:.3f}\textwidth]{{assets/{filename}}}")
        else:
            parts.append(item["text"])
    return "\n\n".join(part for part in parts if part), images


def split_inline_choice_text(text: str) -> tuple[str, dict[str, str]] | None:
    matches = list(INLINE_CHOICE_LABEL_RE.finditer(text))
    labels = [match.group(1).upper() for match in matches]
    if labels[:4] != ["A", "B", "C", "D"]:
        return None
    stem = text[: matches[0].start()].strip()
    choices: dict[str, str] = {}
    for index, match in enumerate(matches[:4]):
        end = matches[index + 1].start() if index + 1 < len(matches[:4]) else len(text)
        choices[match.group(1).upper()] = text[match.end() : end].strip()
    return stem, choices


def split_choice_items(
    items: list[dict[str, str | float]]
) -> tuple[list[dict[str, str | float]], list[dict[str, Any]], list[str]]:
    stem_items: list[dict[str, str | float]] = []
    choices_by_id: dict[str, list[dict[str, str | float]]] = {}
    current_choice: str | None = None

    for item in items:
        if item["kind"] != "text":
            if current_choice:
                choices_by_id.setdefault(current_choice, []).append(item)
            else:
                stem_items.append(item)
            continue

        text = str(item["text"])
        inline = split_inline_choice_text(text)
        if inline:
            stem_text, inline_choices = inline
            if stem_text:
                if current_choice:
                    choices_by_id.setdefault(current_choice, []).append({"kind": "text", "text": stem_text})
                else:
                    stem_items.append({"kind": "text", "text": stem_text})
            for choice_id, choice_text in inline_choices.items():
                choices_by_id[choice_id] = [{"kind": "text", "text": choice_text}] if choice_text else []
            current_choice = "D"
            continue

        label_match = CHOICE_LABEL_RE.match(text)
        if label_match:
            current_choice = label_match.group(1).upper()
            choice_text = label_match.group(2).strip()
            choices_by_id.setdefault(current_choice, [])
            if choice_text:
                choices_by_id[current_choice].append({"kind": "text", "text": choice_text})
            continue

        if current_choice:
            choices_by_id.setdefault(current_choice, []).append(item)
        else:
            stem_items.append(item)

    expected = ["A", "B", "C", "D"]
    if any(choice_id not in choices_by_id for choice_id in expected):
        return items, [], []

    choices: list[dict[str, Any]] = []
    choice_asset_files: list[str] = []
    for choice_id in expected:
        latex_choice, image_files = items_to_text_and_images(choices_by_id[choice_id])
        choice_asset_files.extend(image_files)
        choices.append(
            {
                "id": choice_id,
                "body": {
                    "format": "typst",
                    "text": latex_to_typst(latex_choice),
                    "extensions": {"latexSource": latex_choice},
                },
            }
        )
    return stem_items, choices, choice_asset_files


def normalize_match_text(text: str) -> str:
    text = re.sub(r"\\includegraphics(?:\[[^\]]*\])?\{[^}]+\}", " ", text)
    text = re.sub(r"\\[a-zA-Z]+\*?(?:\s*\{[^{}]*\})?", " ", text)
    text = re.sub(r"[^A-Za-z0-9]+", " ", text)
    return re.sub(r"\s+", " ", text).strip().lower()


def is_repeated_prompt_line(stem_norm: str, solution_norm: str) -> bool:
    if not stem_norm or not solution_norm:
        return False
    if stem_norm == solution_norm:
        return True
    shorter = min(len(stem_norm), len(solution_norm))
    longer = max(len(stem_norm), len(solution_norm))
    if shorter / longer < 0.75:
        return False
    return stem_norm in solution_norm or solution_norm in stem_norm


def strip_repeated_question_items(
    stem_items: list[dict[str, str | float]], solution_items: list[dict[str, str | float]]
) -> list[dict[str, str | float]]:
    stem_texts = [
        str(item["text"])
        for item in stem_items
        if item["kind"] == "text" and not re.fullmatch(r"Question\s+\d+", str(item["text"]).strip(), re.I)
    ]
    solution_text_indexes = [index for index, item in enumerate(solution_items) if item["kind"] == "text"]
    remove_text_indexes: set[int] = set()
    stem_pos = 0
    for solution_index in solution_text_indexes:
        if stem_pos >= len(stem_texts):
            break
        if re.fullmatch(r"Question\s+\d+", str(solution_items[solution_index]["text"]).strip(), re.I):
            remove_text_indexes.add(solution_index)
            continue
        solution_norm = normalize_match_text(str(solution_items[solution_index]["text"]))
        if not solution_norm:
            continue
        matched_stem_pos: int | None = None
        for search_pos in range(stem_pos, len(stem_texts)):
            stem_norm = normalize_match_text(stem_texts[search_pos])
            if not stem_norm:
                continue
            if is_repeated_prompt_line(stem_norm, solution_norm):
                remove_text_indexes.add(solution_index)
                matched_stem_pos = search_pos
                stem_pos = search_pos + 1
                break
        if matched_stem_pos is None:
            break

    if not remove_text_indexes:
        return solution_items
    return [item for index, item in enumerate(solution_items) if index not in remove_text_indexes]


def image_filename_from_match(match: re.Match[str]) -> str:
    base = Path(match.group("base")).stem
    height = match.group("height")
    width = match.group("width")
    y = match.group("y")
    x = match.group("x")
    return f"{base}_{height}_{width}_{y}_{x}.jpg"


def extract_images(doc_ids: list[str], assets_dir: Path) -> set[str]:
    assets_dir.mkdir(parents=True, exist_ok=True)
    extracted: set[str] = set()
    for doc_id in doc_ids:
        zip_path = CACHE_DIR / doc_id / f"{doc_id}.tex.zip"
        if not zip_path.exists():
            continue
        with zipfile.ZipFile(zip_path) as archive:
            for name in archive.namelist():
                if not name.lower().endswith((".jpg", ".jpeg", ".png")):
                    continue
                out_name = Path(name).name
                with archive.open(name) as source, (assets_dir / out_name).open("wb") as target:
                    shutil.copyfileobj(source, target)
                extracted.add(out_name)
    return extracted


def latex_document(body: str) -> str:
    return "\n".join(
        [
            r"\documentclass{article}",
            r"\usepackage{amsmath,amssymb}",
            r"\usepackage{graphicx}",
            r"\begin{document}",
            body,
            r"\end{document}",
            "",
        ]
    )


def strip_mitex_preamble(text: str) -> str:
    marker = "#[\n"
    index = text.rfind(marker)
    if index >= 0:
        return text[index:].strip()
    return text.strip()


def compact_spaced_numbers(text: str) -> str:
    previous = None
    while previous != text:
        previous = text
        text = re.sub(r"(?<=\d)\s+\.\s+(?=\d)", ".", text)
        text = re.sub(r"(?<=\d)\s+(?=\d)", "", text)
    return text


def convert_absolute_bars(text: str) -> str:
    previous = None
    while previous != text:
        previous = text
        text = re.sub(r"\|\s*([^|]+?)\s*\|", lambda m: f"abs({m.group(1).strip()})", text)
    return text


def split_top_level_once(text: str, delimiter: str = ",") -> tuple[str, str] | None:
    depth = 0
    quote: str | None = None
    for index, char in enumerate(text):
        if quote:
            if char == quote and (index == 0 or text[index - 1] != "\\"):
                quote = None
            continue
        if char in {'"', "'"}:
            quote = char
            continue
        if char in "([{":
            depth += 1
        elif char in ")]}":
            depth = max(0, depth - 1)
        elif char == delimiter and depth == 0:
            return text[:index], text[index + 1 :]
    return None


def replace_balanced_call(text: str, name: str, convert: Callable[[str], str]) -> str:
    output: list[str] = []
    index = 0
    needle = f"{name}("
    while index < len(text):
        start = text.find(needle, index)
        if start < 0:
            output.append(text[index:])
            break
        output.append(text[index:start])
        cursor = start + len(needle)
        depth = 1
        quote: str | None = None
        while cursor < len(text):
            char = text[cursor]
            if quote:
                if char == quote and text[cursor - 1] != "\\":
                    quote = None
            elif char in {'"', "'"}:
                quote = char
            elif char == "(":
                depth += 1
            elif char == ")":
                depth -= 1
                if depth == 0:
                    break
            cursor += 1

        if depth != 0:
            output.append(text[start:])
            break

        output.append(convert(text[start + len(needle) : cursor]))
        index = cursor + 1
    return "".join(output)


def clean_mitex_array(inner: str) -> str:
    content = inner.strip()
    if content.startswith("arg0:"):
        split = split_top_level_once(content)
        if split:
            _, content = split
    content = content.strip()
    content = re.sub(r"\s*,\s*", ", ", content)
    content = re.sub(r"\s{2,}", " ", content)
    return content


def clean_mitex_helpers(text: str) -> str:
    previous = None
    while previous != text:
        previous = text
        text = replace_balanced_call(text, "mitexarray", clean_mitex_array)
        text = replace_balanced_call(text, "mitexmathbf", lambda inner: inner.strip())
        text = replace_balanced_call(text, "mitexsqrt", lambda inner: f"sqrt({inner.strip()})")
    return text


def clean_math_fragment(text: str) -> str:
    text = re.sub(r"\blr\(\s*\\\((.*?)\\\)\s*\)", r"(\1)", text, flags=re.S)
    text = text.replace(r"\(", "(").replace(r"\)", ")")
    text = text.replace(r"\[", "[").replace(r"\]", "]")
    text = text.replace(r"\/", "/")
    text = text.replace("zws", "")
    text = text.replace("dots.h", "...")
    text = text.replace("compose", "degree")
    text = clean_mitex_helpers(text)
    text = text.replace(r"\;", " ")
    text = re.sub(r"#textmath\[([^\]]*)\]", lambda m: f'"{m.group(1).strip()}"', text)
    text = re.sub(r"\blr\(", "(", text)
    text = compact_spaced_numbers(text)
    text = re.sub(
        r"(?<!\")_\(([^)]+)\)\s*C\s*_\(([^)]+)\)",
        lambda m: combination_typst(m.group(1), m.group(2)),
        text,
    )
    text = re.sub(r"^\s*aligned\((.*)\)\s*$", r"\1", text, flags=re.S)
    text = text.replace("aligned(", "(")
    text = re.sub(r"\bquad\b", " ", text)
    text = convert_absolute_bars(text)
    text = re.sub(
        r"\bbinom\(([^,()]+),\s*([^)]+)\)",
        lambda m: combination_typst(m.group(1), m.group(2)),
        text,
    )
    text = text.replace(";", "")
    text = re.sub(r"\s+,", ",", text)
    text = re.sub(r",\s*", ", ", text)
    text = re.sub(r"\s+\)", ")", text)
    text = re.sub(r"\(\s+", "(", text)
    text = re.sub(r"\s{2,}", " ", text)
    text = re.sub(r"(?:\\\s*)+$", "", text)
    text = re.sub(r"\\\s*\\", r"\\", text)
    return text.strip()


def clean_latex_math_fragment(text: str) -> str:
    text = text.replace(r"\left|", "|").replace(r"\right|", "|")
    text = text.replace(r"\lvert", "|").replace(r"\rvert", "|")
    text = text.replace(r"\left", "").replace(r"\right", "")
    text = re.sub(r"\\text\s*\{([^{}]*)\}", lambda m: f'"{m.group(1).strip()}"', text)
    text = re.sub(r"\\mathrm\s*\{([^{}]*)\}", lambda m: f'upright({m.group(1).strip()})', text)
    previous = None
    while previous != text:
        previous = text
        text = re.sub(r"\\frac\s*\{([^{}]+)\}\s*\{([^{}]+)\}", r"frac(\1, \2)", text)
    text = re.sub(
        r"\{\s*\}_\{([^{}]+)\}\s*C_\{([^{}]+)\}",
        lambda m: combination_typst(m.group(1), m.group(2)),
        text,
    )
    text = re.sub(
        r"_\{([^{}]+)\}\s*C_\{([^{}]+)\}",
        lambda m: combination_typst(m.group(1), m.group(2)),
        text,
    )
    replacements = {
        r"\theta": "theta",
        r"\alpha": "alpha",
        r"\beta": "beta",
        r"\pi": "pi",
        r"\sin": "sin",
        r"\cos": "cos",
        r"\tan": "tan",
        r"\sec": "sec",
        r"\csc": "csc",
        r"\log": "log",
        r"\ldots": "...",
        r"\therefore": "therefore",
        r"\neq": "!=",
        r"\leq": "<=",
        r"\geq": ">=",
        r"\circ": "degree",
        r"\cdot": "dot",
        r"\quad": " ",
        r"\bullet": "dot",
    }
    for source, target in replacements.items():
        text = text.replace(source, target)
    text = re.sub(r"\^\{([^{}]+)\}", r"^(\1)", text)
    text = re.sub(r"_\{([^{}]+)\}", r"_(\1)", text)
    text = text.replace("{", "(").replace("}", ")")
    text = convert_absolute_bars(text)
    return clean_math_fragment(text)


def latex_image_to_typst(match: re.Match[str]) -> str:
    opts = match.group(1) or ""
    path = match.group(2)
    width = "100%"
    width_match = re.search(r"width\s*=\s*([0-9.]+)\s*\\textwidth", opts)
    if width_match:
        width = f"{float(width_match.group(1)) * 100:.1f}%"
    return f'#image("{path}", width: {width})'


def latex_to_typst_fallback(text: str) -> str:
    text = re.sub(
        r"\\includegraphics(?:\[([^\]]*)\])?\{([^}]+)\}",
        latex_image_to_typst,
        text,
    )
    text = re.sub(r"\\multirow\{[^{}]*\}\{[^{}]*\}\{([^{}]*)\}", r"\1", text)
    text = re.sub(r"\\begin\{(?:tabular|array|aligned|gathered)\}(?:\{[^{}]*\})?", "", text)
    text = re.sub(r"\\end\{(?:tabular|array|aligned|gathered)\}", "", text)
    text = text.replace(r"\hline", "")
    text = text.replace("&", " | ")
    text = text.replace(r"\\", "\n")
    text = re.sub(r"\\\[(.*?)\\\]", lambda m: f"${clean_latex_math_fragment(m.group(1))}$", text, flags=re.S)
    text = re.sub(r"\\\((.*?)\\\)", lambda m: f"${clean_latex_math_fragment(m.group(1))}$", text, flags=re.S)
    text = re.sub(r"\\[a-zA-Z]+\*?", "", text)
    text = re.sub(r"\{\d+\}\{\*\}\{([^{}]*)\}", r"\1", text)
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return normalize_typst_paragraphs(text.strip())


def clean_typst_output(text: str) -> str:
    text = strip_mitex_preamble(text)
    if text.startswith("#[\n") and text.endswith("\n];"):
        text = text[3:-3].strip()

    text = re.sub(
        r"#math\.equation\(block:\s*false,\s*\$(.*?)\$\);",
        lambda m: f"${clean_math_fragment(m.group(1))}$",
        text,
        flags=re.S,
    )
    text = re.sub(
        r"#image\(width:\s*\*\s*100%,\s*\"([^\"]+)\"\)",
        r'#image("\1", width: 100%)',
        text,
    )
    text = re.sub(
        r"#image\(width:\s*([0-9.]+)\s*\*\s*100%,\s*\"([^\"]+)\"\)",
        lambda m: f'#image("{m.group(2)}", width: {float(m.group(1)) * 100:.1f}%)',
        text,
    )

    def clean_dollar_block(match: re.Match[str]) -> str:
        return f"${clean_math_fragment(match.group(1))}$"

    text = re.sub(r"\$(.*?)\$", clean_dollar_block, text, flags=re.S)
    text = text.replace(r"\,", ",")
    text = text.replace(r"\)", ")").replace(r"\(", "(")
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return normalize_typst_paragraphs(text.strip())


def is_standalone_math(block: str) -> bool:
    return bool(re.fullmatch(r"\$[^$]*\$", block.strip(), flags=re.S))


def is_separate_typst_block(block: str) -> bool:
    stripped = block.strip()
    return (
        not stripped
        or stripped.startswith("#image(")
        or stripped.startswith("#table(")
        or stripped.startswith("table.")
        or stripped.startswith("[")
        or re.match(r"^(?:\d+(?:/\d+)?\s+)?marks?\b", stripped, re.I)
        or re.match(r"^\d+\s+mark\b", stripped, re.I)
        or re.match(r"^(?:Note:|Deduct\b|Method\s+\d+)", stripped, re.I)
        or is_standalone_math(stripped)
    )


def join_paragraph_parts(parts: list[str]) -> str:
    text = " ".join(part.strip() for part in parts if part.strip())
    text = re.sub(r"\s+", " ", text)
    text = text.replace(" cm .", " cm.")
    text = text.replace(" ,", ",")
    return text.strip()


def normalize_typst_paragraphs(text: str) -> str:
    blocks = [block.strip() for block in re.split(r"\n\s*\n", text) if block.strip()]
    output: list[str] = []
    paragraph: list[str] = []

    def flush() -> None:
        if paragraph:
            output.append(join_paragraph_parts(paragraph))
            paragraph.clear()

    for block in blocks:
        if is_separate_typst_block(block):
            flush()
            output.append(block)
        else:
            paragraph.append(block)
    flush()
    return "\n\n".join(output)


def latex_to_typst(text: str) -> str:
    if not text.strip():
        return ""
    if not MITEX.exists():
        return text
    with tempfile.TemporaryDirectory(prefix="manitoba-mitex-") as tmpdir:
        tmp = Path(tmpdir)
        source = tmp / "input.tex"
        output = tmp / "output.typ"
        source.write_text(latex_document(text), encoding="utf-8")
        for image_path in re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", text):
            image_file = tmp / image_path
            image_file.parent.mkdir(parents=True, exist_ok=True)
            image_file.write_bytes(b"x")
        result = subprocess.run(
            [str(MITEX), "compile", "-i", str(source), "-o", str(output)],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        if result.returncode != 0 or not output.exists():
            return latex_to_typst_fallback(text)
        return clean_typst_output(output.read_text(encoding="utf-8"))


def doc_page_map(doc_id: str) -> dict[int, dict[str, Any]]:
    original_pages = load_filter_pages(doc_id)
    pages = load_lines(doc_id)
    return {original: pages[index] for index, original in enumerate(original_pages)}


def normalize_outcome_code(code: str) -> str | None:
    text = code.strip().upper()
    if not text:
        return None
    match = re.fullmatch(r"(?:12P\.)?([TRP])\.?(\d+)", text)
    if not match:
        return None
    return f"12P.{match.group(1)}.{int(match.group(2))}"


def outcome_codes(raw_outcomes: str) -> list[str]:
    codes: list[str] = []
    for raw_code in raw_outcomes.split(","):
        code = normalize_outcome_code(raw_code)
        if code and code not in codes:
            codes.append(code)
    return codes


def class_defs(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    units: list[dict[str, Any]] = []
    for unit in CURRICULUM_UNITS:
        units.append(
            {
                "id": unit["id"],
                "name": unit["name"],
                "sections": [
                    {
                        "id": section_id,
                        "name": f"{section_id}: {section_name}",
                    }
                    for section_id, section_name in unit["sections"]
                ],
                "extensions": {
                    "glo": unit["glo"],
                    "sourceUrl": CURRICULUM_SOURCE_URL,
                },
            }
        )
    return [
        {
            "id": COURSE_ID,
            "name": COURSE_NAME,
            "units": units,
            "extensions": {
                "courseCode": COURSE_CODE,
                "curriculumSourceUrl": CURRICULUM_SOURCE_URL,
            },
        }
    ]


def classification_for_row(row: dict[str, Any], session: str, booklet: int) -> dict[str, Any]:
    codes = outcome_codes(str(row.get("learningOutcome", "")))
    primary_code = codes[0] if codes else None
    primary = OUTCOMES.get(primary_code or "")
    classification: dict[str, Any] = {
        "questionType": row["kind"],
        "tags": [session, f"Booklet {booklet}", row["calculatorPolicy"], *codes],
        "classId": COURSE_ID,
        "className": COURSE_NAME,
        "extensions": {
            "learningOutcome": row.get("learningOutcome"),
            "curriculum": {
                "courseCode": COURSE_CODE,
                "sourceUrl": CURRICULUM_SOURCE_URL,
                "outcomeCodes": codes,
                "primaryOutcomeCode": primary_code,
                "inferenceConfidence": "high" if primary_code else "unknown",
                "inferenceReason": row.get("learningOutcomeSource"),
            },
        },
    }
    if primary:
        classification.update(
            {
                "unitId": primary["unitId"],
                "unitName": primary["unitName"],
                "sectionId": primary["sectionId"],
                "sectionName": primary["sectionName"],
            }
        )
        classification["extensions"]["curriculum"].update(
            {
                "glo": primary["glo"],
                "slo": primary["slo"],
                "outcomeCode": primary["sectionId"],
            }
        )
    if len(codes) > 1:
        classification["extensions"]["curriculum"]["additionalOutcomes"] = [
            {
                "unitId": OUTCOMES[code]["unitId"],
                "unitName": OUTCOMES[code]["unitName"],
                "sectionId": OUTCOMES[code]["sectionId"],
                "sectionName": OUTCOMES[code]["sectionName"],
                "glo": OUTCOMES[code]["glo"],
                "slo": OUTCOMES[code]["slo"],
            }
            for code in codes[1:]
            if code in OUTCOMES
        ]
    return classification


def export_sample(year: int, term: str, booklet: int) -> Path:
    rows = load_catalog(year, term, booklet)
    session = rows[0]["session"] if rows else f"{term.title()} {year}"
    sb_doc_id = f"pc_{year}_{term}_sb{booklet}"
    mg_doc_id = f"pc_{year}_{term}_mg"
    sb_pages = doc_page_map(sb_doc_id)
    mg_pages = doc_page_map(mg_doc_id)

    package_id = f"manitoba-pc40s-{year}-{term}-sb{booklet}-mathpix-sample"
    package_dir = OUT_DIR / package_id
    assets_dir = package_dir / "assets"
    extracted_images = extract_images([sb_doc_id, mg_doc_id], assets_dir)

    questions = []
    assets: dict[str, dict[str, Any]] = {}
    diagnostics = []
    for row in rows:
        qnum = int(row["question"])
        stem_items: list[dict[str, str | float]] = []
        stem_asset_files: list[str] = []
        for page_number in row["sourcePages"]:
            page_items_for_source = page_items_for_question(sb_pages[int(page_number)], qnum)
            _, image_files = items_to_text_and_images(page_items_for_source)
            stem_items.extend(page_items_for_source)
            stem_asset_files.extend(image_files)

        solution_items: list[dict[str, str | float]] = []
        solution_asset_files: list[str] = []
        for page_number in row["mgSourcePages"]:
            page = mg_pages.get(int(page_number))
            if not page:
                diagnostics.append(
                    {
                        "level": "warning",
                        "code": "missing-mg-page",
                        "message": f"Missing Mathpix page for marking-guide source page {page_number}.",
                        "questionId": f"mb-pc40s-{year}-{term}-q{qnum:02d}",
                    }
                )
                continue
            page_items_for_source = page_items_for_question(page, qnum)
            _, image_files = items_to_text_and_images(page_items_for_source)
            solution_items.extend(page_items_for_source)
            solution_asset_files.extend(image_files)

        stripped_solution_items = strip_repeated_question_items(stem_items, solution_items)
        choices: list[dict[str, Any]] = []
        choice_asset_files: list[str] = []
        if row["kind"] == "mcq":
            stem_items, choices, choice_asset_files = split_choice_items(stem_items)
        latex_stem, stem_asset_files = items_to_text_and_images(stem_items)
        latex_solution, solution_asset_files = items_to_text_and_images(stripped_solution_items)
        asset_ids = []
        for filename in stem_asset_files + solution_asset_files + choice_asset_files:
            if filename not in extracted_images:
                continue
            asset_id = f"asset_{Path(filename).stem}"
            asset_ids.append(asset_id)
            assets[asset_id] = {
                "id": asset_id,
                "kind": "image",
                "filename": filename,
                "mimeType": "image/jpeg",
                "storage": {"mode": "external", "path": f"assets/{filename}"},
                "source": {"originalPath": filename},
            }

        content: dict[str, Any] = {
            "stem": {
                "format": "typst",
                "text": latex_to_typst(latex_stem),
                "extensions": {"latexSource": latex_stem},
            },
            "solution": {
                "format": "typst",
                "text": latex_to_typst(latex_solution),
                "extensions": {"latexSource": latex_solution},
            },
        }
        if choices:
            content["choices"] = choices

        question = {
            "id": f"mb-pc40s-{year}-{term}-q{qnum:02d}",
            "kind": row["kind"],
            "content": content,
            "scoring": {"points": float(row["points"])},
            "classification": classification_for_row(row, session, booklet),
            "assets": sorted(set(asset_ids)),
            "provenance": {
                "sourceApp": "ocr-frq",
                "sourceLabel": f"Manitoba Pre-Calculus 40S {session}",
                "sourceQuestionNumber": str(qnum),
                "confidence": "medium",
                "originFiles": [f"{sb_doc_id}.lines.json", f"{mg_doc_id}.lines.json"],
                "extensions": {
                    "studentBooklet": sb_doc_id,
                    "markingGuide": mg_doc_id,
                    "sourcePages": row["sourcePages"],
                    "mgSourcePages": row["mgSourcePages"],
                    "mathpix": True,
                },
            },
            "extensions": {
                "booklet": booklet,
                "calculatorPolicy": row["calculatorPolicy"],
                "marksText": row["marksText"],
                "learningOutcomeSource": row["learningOutcomeSource"],
            },
        }
        if row.get("answer"):
            question["answer"] = {"type": "choice", "value": row["answer"]}
        questions.append(question)

    package = {
        "format": "portable-question-package",
        "version": "1.0",
        "producer": {
            "app": "ocr-frq",
            "appVersion": "manitoba-mathpix-sample-1",
            "exportedAt": utc_now(),
        },
        "source": {
            "kind": "pdf",
            "label": f"Manitoba Pre-Calculus 40S {session} Booklet {booklet}",
            "collection": "Manitoba Pre-Calculus 40S Provincial Exams",
            "publisher": "Manitoba Education and Early Childhood Learning",
            "year": year,
            "originFiles": [f"{sb_doc_id}.pdf", f"{mg_doc_id}.pdf"],
            "extensions": {"term": term, "session": session, "sample": True},
        },
        "classes": class_defs(rows),
        "questions": questions,
        "assets": sorted(assets.values(), key=lambda item: item["id"]),
        "diagnostics": diagnostics,
        "extensions": {
            "sample": True,
            "notes": [
                "Generated from Mathpix API lines.json and tex.zip artifacts.",
                "Primary content is best-effort Typst generated with mitex.",
                "Mathpix LaTeX is preserved in content.*.extensions.latexSource.",
                "Only the cached booklet is included in this sample.",
            ],
        },
    }

    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    errors = sorted(Draft202012Validator(schema).iter_errors(package), key=lambda error: error.path)
    if errors:
        raise RuntimeError("\n".join(error.message for error in errors[:20]))

    referenced_filenames = {asset["filename"] for asset in assets.values()}
    for path in assets_dir.glob("*"):
        if path.is_file() and path.name not in referenced_filenames:
            path.unlink()

    package_dir.mkdir(parents=True, exist_ok=True)
    out_path = package_dir / f"{package_id}.pqp.json"
    out_path.write_text(json.dumps(package, indent=2, ensure_ascii=False), encoding="utf-8")
    return out_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--year", type=int, default=2026)
    parser.add_argument("--term", default="jun", choices=["jan", "jun"])
    parser.add_argument("--booklet", type=int, default=1)
    args = parser.parse_args()

    out_path = export_sample(args.year, args.term, args.booklet)
    print(out_path)


if __name__ == "__main__":
    main()
