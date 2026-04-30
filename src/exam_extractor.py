"""
exam_extractor.py — Claude Vision extraction for raw AP exam free-response pages.

Processes single-column exam booklet pages (not scoring guides).
A page may contain 1–2 questions. Each question returns its number, text, and
figures with normalized bounding boxes.

Prompt caching is applied to the system prompt for efficiency.
"""

import base64
import json
import logging
from pathlib import Path
from typing import Optional

import anthropic

from cache import FRQCache

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# System prompt
# ---------------------------------------------------------------------------

_SYSTEM_PROMPT = """\
You are processing a scanned page from an AP exam free-response booklet (NOT a scoring guide).

Page layout for exam pages:
- Single column, full-width content
- May contain 1 or 2 complete questions
- Each question begins with a number followed by a period (e.g. "1. ", "2. ")
- No solution column, no grading rubric column, no "SCORING GUIDELINES" header

Extra pages that should be skipped:
- Title / cover pages (just title text, logos, no question content)
- Copyright / introductory pages
- Section separator pages ("SECTION II, Part A / Time—45 minutes / Number of problems—3")
- Instructions pages
- Any page with no actual question content

Your job for each page:
1. Decide if this is a page with question content (exam) or an ignorable extra page (skip).
2. If it is an exam page:
   a. Identify all distinct questions on the page (usually 1, sometimes 2).
   b. For each question:
      - Extract the question_number (integer) if visible (e.g. "1", "2"), or null
      - Extract the full question text (may include sub-parts a, b, c, d…)
      - Identify figures (diagrams, graphs, plots, geometric figures) and return normalized bounding boxes
      - Identify clearly rectangular text tables and return them as structured rows/cells
   c. Return one entry per question found.
3. If it is an ignorable extra page:
   a. Set page_type to "skip"
   b. Return an empty questions array

Math notation rules (Typst syntax):
- Use $...$ with no spaces inside the dollar signs for inline math.
- Use $ ... $ with a space after the opening $ and before the closing $ for display/block equations.
- Do NOT use LaTeX delimiters such as \\(...\\) or \\[...\\].
- Write math operators without backslashes: integral, sum, product, lim, sqrt(x), abs(x), floor(x), ceil(x).
- Write Greek letters without backslashes: alpha, beta, pi, theta, lambda, etc.
- Write fractions as a/b for simple cases or (numerator)/(denominator) for complex ones.
- Comparisons and special values: use <= for ≤, >= for ≥, != for ≠, approx for ≈, infinity for ∞, times for ×, dot for •.
- Do NOT write `cdot` — use `dot` (or `times` for multiplication). Example: `a dot b` or `a times b`.
- Always write function application with parentheses: `f(x)`, `g(t)`, not `fx` or `gt`.
- Always separate a constant from a variable with a space: `k x^2`, not `kx^2`.
- Derivatives: write as f'(x) or (dif y)/(dif x); integrals as integral_a^b f(x) dif x.
- Subscripts and superscripts work the same as LaTeX: x_0, e^x, a_(n+1).
- If a symbol cannot be reliably recovered, use a descriptive placeholder like [integral expression].

Figure detection rules:
- Scan the page for diagrams, graphs, plots, circuit diagrams, geometric figures, sketches, or any other non-text visual elements.
- Do not classify rectangular text tables as figures. Return those under `tables` instead.
- For each figure found, return a normalized bounding box [x, y, width, height] in [0,1] coordinates (origin = top-left of full page).
- Include any nearby caption or label, or null if no caption is visible.
- Figures should be associated with the question they appear in (by proximity and context).
- If no figures are present in a question, return an empty array.

Table extraction rules:
- Detect only clearly rectangular tables with visible rows and columns.
- Return `headers` as the top row if the table has a header row; otherwise return an empty array.
- Return `rows` as the body rows in reading order, preserving cell text in Typst-friendly notation.
- Do not include bounding boxes for tables.
- If no tables are present in a question, return an empty array.

Extraction rules:
- Do not guess or invent content. If a field is unclear or absent, return null.
- Return the full question text including all sub-parts.
- Preserve the structure of questions (sub-parts a, b, c, etc.)
- A page with 2 questions should return 2 question entries.

Unit and section identification:
- Identify the AP Calculus unit this question belongs to (e.g., "Unit 1: Limits and Continuity",
  "Unit 2: Differentiation", etc.). Use the full official title.
- Identify the section: "Part A" (calculator allowed) or "Part B" (calculator not allowed).
- If a question spans multiple units, use the highest-numbered unit (e.g., if Units 2 and 5,
  use Unit 5). Similarly for sections, use the latter one if applicable.
- Determine calculator status: "Calculator active" for Part A, "Calculator prohibited" for Part B.
\
"""

# ---------------------------------------------------------------------------
# JSON output schema
# ---------------------------------------------------------------------------

_OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "page_type": {
            "type": "string",
            "enum": ["exam", "skip"],
            "description": "Whether this is an exam question page or an ignorable extra page.",
        },
        "skip_reason": {
            "anyOf": [
                {
                    "type": "string",
                    "enum": [
                        "title_page",
                        "cover_sheet",
                        "instructions",
                        "section_separator",
                        "other",
                    ],
                },
                {"type": "null"},
            ],
            "description": "Why the page is skipped. Null when page_type is exam.",
        },
        "questions": {
            "type": "array",
            "description": "List of questions found on this page.",
            "items": {
                "type": "object",
                "properties": {
                    "question_number": {
                        "anyOf": [{"type": "integer"}, {"type": "null"}],
                        "description": "Question number (e.g. 1, 2, 3), or null if not visible.",
                    },
                    "question": {
                        "type": "string",
                        "description": "Full question text including all sub-parts (a, b, c, etc.).",
                    },
                    "figures": {
                        "type": "array",
                        "description": "List of figures/diagrams on this question.",
                        "items": {
                            "type": "object",
                            "properties": {
                                "x": {
                                    "type": "number",
                                    "description": "Normalized x-coordinate [0,1] of the left edge.",
                                },
                                "y": {
                                    "type": "number",
                                    "description": "Normalized y-coordinate [0,1] of the top edge.",
                                },
                                "width": {
                                    "type": "number",
                                    "description": "Normalized width [0,1].",
                                },
                                "height": {
                                    "type": "number",
                                    "description": "Normalized height [0,1].",
                                },
                                "caption": {
                                    "anyOf": [{"type": "string"}, {"type": "null"}],
                                    "description": "Any visible caption or label.",
                                },
                            },
                            "required": ["x", "y", "width", "height", "caption"],
                            "additionalProperties": False,
                        },
                    },
                    "tables": {
                        "type": "array",
                        "description": "List of rectangular text tables on this question.",
                        "items": {
                            "type": "object",
                            "properties": {
                                "headers": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                    "description": "Header row values, or an empty array if there is no header row.",
                                },
                                "rows": {
                                    "type": "array",
                                    "items": {
                                        "type": "array",
                                        "items": {"type": "string"},
                                    },
                                    "description": "Table body rows in reading order.",
                                },
                                "caption": {
                                    "anyOf": [{"type": "string"}, {"type": "null"}],
                                    "description": "Visible caption or title, if any.",
                                },
                            },
                            "required": ["headers", "rows", "caption"],
                            "additionalProperties": False,
                        },
                    },
                    "unit": {
                        "anyOf": [{"type": "string"}, {"type": "null"}],
                        "description": "AP Calculus unit (e.g., 'Unit 1: Limits and Continuity') or null.",
                    },
                    "section": {
                        "anyOf": [{"type": "string"}, {"type": "null"}],
                        "description": "Section identifier ('Part A' or 'Part B') or null.",
                    },
                    "calculator": {
                        "anyOf": [{"type": "string"}, {"type": "null"}],
                        "description": "'Calculator active' or 'Calculator prohibited' or null.",
                    },
                },
                "required": ["question_number", "question", "figures", "tables", "unit", "section", "calculator"],
                "additionalProperties": False,
            },
        },
    },
    "required": [
        "page_type",
        "skip_reason",
        "questions",
    ],
    "additionalProperties": False,
}

# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def extract_exam_page(
    image_path: str,
    client: anthropic.Anthropic,
    cache: Optional[FRQCache] = None,
    force: bool = False,
    model: str = "claude-haiku-4-5",
    usage_out: Optional[list] = None,
) -> dict:
    """
    Extract question(s) from one raw exam page.

    Returns a dict with keys:
        page_type, skip_reason, questions

    Each question entry has:
        question_number, question, figures

    Args:
        image_path: Path to a PNG of the rendered page.
        client:     Anthropic client instance.
        cache:      Optional FRQCache; pass None to disable caching.
        force:      Bypass cache and call the API even if a cached result exists.
        model:      Claude model ID.
        usage_out:  Optional list; a usage dict is appended for each live API call.
    """
    if cache is not None:
        if force:
            cache.invalidate(image_path)
        else:
            cached = cache.get(image_path)
            if cached is not None:
                return cached

    with open(image_path, "rb") as fh:
        image_b64 = base64.standard_b64encode(fh.read()).decode("ascii")

    logger.debug("Calling Claude Vision (%s) for exam page %s", model, image_path)

    response = client.messages.create(
        model=model,
        max_tokens=4096,
        system=[
            {
                "type": "text",
                "text": _SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"},
            }
        ],
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/png",
                            "data": image_b64,
                        },
                    },
                    {
                        "type": "text",
                        "text": (
                            "Extract all questions from this exam page. "
                            "For each question, provide its number (if visible), full text, and any figures. "
                            "Write all math in Typst syntax ($...$), using `dot` not `cdot`."
                        ),
                    },
                ],
            }
        ],
        output_config={
            "format": {
                "type": "json_schema",
                "schema": _OUTPUT_SCHEMA,
            }
        },
    )

    raw = next(b.text for b in response.content if b.type == "text")
    result = json.loads(raw)

    u = response.usage
    usage = {
        "input_tokens": u.input_tokens,
        "output_tokens": u.output_tokens,
        "cache_read_input_tokens": getattr(u, "cache_read_input_tokens", 0),
        "cache_creation_input_tokens": getattr(u, "cache_creation_input_tokens", 0),
    }
    logger.debug(
        "Tokens — input: %d  output: %d  cache_read: %d  cache_create: %d",
        usage["input_tokens"],
        usage["output_tokens"],
        usage["cache_read_input_tokens"],
        usage["cache_creation_input_tokens"],
    )

    if usage_out is not None:
        usage_out.append(usage)

    if cache is not None:
        cache.put(image_path, result)

    return result
