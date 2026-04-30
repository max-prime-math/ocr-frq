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
from pathlib import Path
from typing import Optional

import anthropic

from cache import FRQCache

logger = logging.getLogger(__name__)

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

Math notation rules (Typst syntax):
- Use $...$ with no spaces inside the dollar signs for inline math.
- Use $ ... $ with a space after the opening $ and before the closing $ for display/block equations.
- Do NOT use LaTeX delimiters such as \\(...\\) or \\[...\\].
- Write math operators without backslashes: integral, sum, product, lim, sqrt(x), abs(x), floor(x), ceil(x).
- Write Greek letters without backslashes: alpha, beta, pi, theta, lambda, etc.
- Write fractions as a/b for simple cases or (numerator)/(denominator) for complex ones.
- Comparisons and special values: use <= for ≤, >= for ≥, != for ≠, approx for ≈, infinity for ∞, times for ×, dot for •.
- Do NOT write `cdot` — use `dot` (or `times` for multiplication). Example: `a dot b` or `a times b`.
- Derivatives: write as f'(x) or (dif y)/(dif x); integrals as integral_a^b f(x) dif x.
- Subscripts and superscripts work the same as LaTeX: x_0, e^x, a_(n+1).
- If a symbol cannot be reliably recovered, use a descriptive placeholder like [integral expression].

Figure detection rules:
- Scan each region (question, solution, grading_scheme) for diagrams, graphs, plots, circuit diagrams, geometric figures, sketches, or any other non-text visual elements.
- For each figure found, return a normalized bounding box [x, y, width, height] in [0,1] coordinates (origin = top-left of full page).
- Include the section the figure belongs to ("question", "solution", or "grading_scheme").
- Include any nearby caption text, or null if no caption is visible.
- If no figures are present, return an empty array.

Extraction rules:
- Do not guess or invent content. If a field is unclear or absent, return null.
- Return every sub-part of the question in the question field (do not split by sub-part).
- Return the full solution text including all sub-part solutions.
- Return the full grading scheme text including all point-value annotations.
- Preserve the structure of the rubric (e.g. "2 : { 1 : criterion / 1 : criterion }").
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
                            "right-column grading scheme. Write all math in Typst syntax ($...$)."
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
