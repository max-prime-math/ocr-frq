"""
extractor.py — Claude Vision extraction for FRQ exam pages.

Each page is classified first (real FRQ question vs. ignorable extra page),
then the three content regions are extracted: question (top), solution (left
column), and grading scheme (right column).

Prompt caching is applied to the system prompt so repeated calls within the
cache TTL only pay for the image + user tokens, not the system prompt tokens.
"""

import base64
import json
import logging
import re
from pathlib import Path
from typing import Optional

import anthropic

from cache import FRQCache

logger = logging.getLogger(__name__)


def _parse_json_text(raw: str):
    text = raw.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
        text = re.sub(r"\s*```$", "", text)
        text = text.strip()

    decoder = json.JSONDecoder()
    for idx, ch in enumerate(text):
        if ch in "[{":
            try:
                obj, _ = decoder.raw_decode(text[idx:])
                return obj
            except json.JSONDecodeError:
                continue
    return json.loads(text)

# ---------------------------------------------------------------------------
# System prompt
# ---------------------------------------------------------------------------

_SYSTEM_PROMPT = """\
You are processing a scanned page from an AP exam scoring guidelines PDF.

Page layout for real FRQ question pages:
- The question prompt is at the top of the page (spanning both columns).
- The worked solution is in the LEFT column below the question.
- The grading scheme / rubric is in the RIGHT column below the question.
- There is usually a visible header like "AP® [SUBJECT] / [YEAR] SCORING GUIDELINES / Question N".

Extra pages that should be skipped include:
- Title / cover pages (just title text, logos, no question content)
- Copyright / introductory pages (organization description, copyright notice)
- Instructions pages
- Section separator pages
- Any other pages that do not contain a real FRQ question with solution and rubric

Your job for each page:
1. Decide whether this is a real FRQ question page or an ignorable extra page.
2. If it is a real FRQ page:
   a. Extract the question number (integer) from the header, or null if not visible.
   b. Extract the full question prompt from the top of the page (may contain sub-parts a, b, c, d…).
   c. Extract the worked solution from the LEFT column.
   d. Extract the grading rubric from the RIGHT column (usually point values with criteria).
   e. Flag the page if confidence is low, content is ambiguous, or any field is substantially unclear.
3. If it is an ignorable extra page:
   a. Set page_type to "skip".
   b. Choose the most fitting skip_reason.
   c. Set question, solution, and grading_scheme to null.

Math notation rules (LaTeX syntax):
- Use standard LaTeX math notation inside $...$ for inline math and $$...$$ for display math when needed.
- Use LaTeX commands such as \\int, \\sum, \\prod, \\lim, \\sqrt{...}, \\frac{...}{...}, \\cdot, \\times.
- Write Greek letters with backslashes: \\alpha, \\beta, \\pi, \\theta, \\lambda, etc.
- Use \\le, \\ge, \\ne, \\approx, \\infty for comparisons and special values.
- Always write function application with parentheses: f(x), g(t), not fx or gt.
- Derivatives may be written as f'(x), \\frac{dy}{dx}, or \\frac{dr}{d\\theta}; integrals as \\int_a^b f(x)\\,dx.
- Use \\text{...} for words that must appear inside math.
- If a symbol cannot be reliably recovered, use a descriptive placeholder in brackets.

Figure detection rules:
- Scan each region (question, solution, grading_scheme) for diagrams, graphs, plots, circuit diagrams, geometric figures, sketches, or any other non-text visual elements.
- Do not classify rectangular text tables as figures. If a region contains a table with rows and columns, return it under `tables` instead.
- For each figure found, return a normalized bounding box [x, y, width, height] in [0,1] coordinates (origin = top-left of full page).
- Include the section the figure belongs to ("question", "solution", or "grading_scheme").
- Include any nearby caption text, or null if no caption is visible.
- If no figures are present, return an empty array.

Table extraction rules:
- Detect only clearly rectangular tables with visible rows and columns.
- For each table, return the section it belongs to ("question", "solution", or "grading_scheme").
- Return `headers` as the top row if the table has a header row; otherwise return an empty array.
- Return `rows` as the body rows in reading order, preserving each cell's text as closely as possible in LaTeX-friendly notation.
- Do not include bounding boxes for tables.
- If no tables are present, return an empty array.

Extraction rules:
- Do not guess or invent content. If a field is unclear or absent, return null.
- Return every sub-part of the question in the question field (do not split by sub-part).
- Return the full solution text including all sub-part solutions.
- Return the full grading scheme text including all point-value annotations.
- Preserve the structure of the rubric (e.g. "2 : { 1 : criterion / 1 : criterion }").

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
            "enum": ["frq", "skip"],
            "description": "Whether this is a real FRQ question page or an ignorable extra page.",
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
            "description": "Why the page is skipped. Null when page_type is frq.",
        },
        "question_number": {
            "anyOf": [{"type": "integer"}, {"type": "null"}],
            "description": "Question number from the page header, or null if not visible.",
        },
        "question": {
            "anyOf": [{"type": "string"}, {"type": "null"}],
            "description": "Full question prompt (all sub-parts) from the top of the page.",
        },
        "solution": {
            "anyOf": [{"type": "string"}, {"type": "null"}],
            "description": "Worked solution from the left column.",
        },
        "grading_scheme": {
            "anyOf": [{"type": "string"}, {"type": "null"}],
            "description": "Grading rubric from the right column with point-value annotations.",
        },
        "figures": {
            "type": "array",
            "description": "List of detected figures/diagrams/graphs on the page.",
            "items": {
                "type": "object",
                "properties": {
                    "section": {
                        "type": "string",
                        "enum": ["question", "solution", "grading_scheme"],
                        "description": "Which section this figure belongs to.",
                    },
                    "x": {
                        "type": "number",
                        "description": "Normalized x-coordinate [0,1] of the left edge of the figure bounding box.",
                    },
                    "y": {
                        "type": "number",
                        "description": "Normalized y-coordinate [0,1] of the top edge of the figure bounding box.",
                    },
                    "width": {
                        "type": "number",
                        "description": "Normalized width [0,1] of the figure bounding box.",
                    },
                    "height": {
                        "type": "number",
                        "description": "Normalized height [0,1] of the figure bounding box.",
                    },
                    "caption": {
                        "anyOf": [{"type": "string"}, {"type": "null"}],
                        "description": "Any visible caption or label for the figure.",
                    },
                },
                "required": ["section", "x", "y", "width", "height", "caption"],
                "additionalProperties": False,
            },
        },
        "tables": {
            "type": "array",
            "description": "List of detected rectangular tables on the page.",
            "items": {
                "type": "object",
                "properties": {
                    "section": {
                        "type": "string",
                        "enum": ["question", "solution", "grading_scheme"],
                        "description": "Which section this table belongs to.",
                    },
                    "headers": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Header row values, or an empty array if there is no header row.",
                    },
                    "rows": {
                        "type": "array",
                        "description": "Table body rows in reading order.",
                        "items": {
                            "type": "array",
                            "items": {"type": "string"},
                        },
                    },
                    "caption": {
                        "anyOf": [{"type": "string"}, {"type": "null"}],
                        "description": "Visible caption or title for the table, if any.",
                    },
                },
                "required": ["section", "headers", "rows", "caption"],
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
        "flagged": {
            "type": "boolean",
            "description": "True if confidence is low, content is ambiguous, or a field is substantially unclear.",
        },
        "flag_reason": {
            "anyOf": [{"type": "string"}, {"type": "null"}],
            "description": "Explanation of why the page was flagged. Null if not flagged.",
        },
    },
    "required": [
        "page_type",
        "skip_reason",
        "question_number",
        "question",
        "solution",
        "grading_scheme",
        "figures",
        "tables",
        "unit",
        "section",
        "calculator",
        "flagged",
        "flag_reason",
    ],
    "additionalProperties": False,
}

# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def extract_page(
    image_path: str,
    client: anthropic.Anthropic,
    cache: Optional[FRQCache] = None,
    force: bool = False,
    model: str = "claude-haiku-4-5",
    usage_out: Optional[list] = None,
    debug_out: Optional[list] = None,
) -> dict:
    """
    Classify and extract content from one rendered FRQ page image.

    Returns a dict matching FRQExtraction with keys:
        page_type, skip_reason, question_number, question,
        solution, grading_scheme, flagged, flag_reason

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

    logger.debug("Calling Claude Vision (%s) for %s", model, image_path)

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
                            "Classify this page and extract its content. "
                            "Determine whether it is a real FRQ question page or an ignorable extra page. "
                            "If it is a real FRQ page, extract the question, left-column solution, and "
                            "right-column grading scheme. Write all math in LaTeX syntax. "
                            "Return only valid JSON matching the schema in your instructions."
                        ),
                    },
                ],
            }
        ],
    )

    raw = next(b.text for b in response.content if b.type == "text")
    result = _parse_json_text(raw)

    if debug_out is not None:
        debug_out.append({"raw": raw, "parsed": result})

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
