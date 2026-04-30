"""Tests for page classification logic in extracted results."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


def _make_extraction(page_type, skip_reason=None, flagged=False, flag_reason=None,
                     question_number=None, question=None, solution=None, grading_scheme=None):
    return {
        "page_type": page_type,
        "skip_reason": skip_reason,
        "question_number": question_number,
        "question": question,
        "solution": solution,
        "grading_scheme": grading_scheme,
        "figures": [],
        "tables": [],
        "unit": None,
        "section": None,
        "calculator": None,
        "flagged": flagged,
        "flag_reason": flag_reason,
    }


# ---------------------------------------------------------------------------
# Classification helpers
# These mirror the logic app.py uses to partition results into buckets.
# ---------------------------------------------------------------------------

def is_frq(extraction: dict) -> bool:
    return extraction.get("page_type") == "frq"


def is_skip(extraction: dict) -> bool:
    return extraction.get("page_type") == "skip"


def is_flagged(extraction: dict) -> bool:
    return bool(extraction.get("flagged"))


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_frq_page_classified_as_frq():
    ext = _make_extraction("frq", question_number=1, question="Find the derivative.")
    assert is_frq(ext)
    assert not is_skip(ext)


def test_skip_page_classified_as_skip():
    ext = _make_extraction("skip", skip_reason="title_page")
    assert is_skip(ext)
    assert not is_frq(ext)


def test_flagged_frq_page():
    ext = _make_extraction("frq", flagged=True, flag_reason="solution column unclear")
    assert is_frq(ext)
    assert is_flagged(ext)


def test_unflagged_frq_page():
    ext = _make_extraction("frq", question_number=2, question="Q", solution="S", grading_scheme="G")
    assert not is_flagged(ext)


def test_skip_reason_variants():
    for reason in ("title_page", "cover_sheet", "instructions", "section_separator", "other"):
        ext = _make_extraction("skip", skip_reason=reason)
        assert is_skip(ext)
        assert ext["skip_reason"] == reason


def test_frq_page_has_no_skip_reason():
    ext = _make_extraction("frq", question_number=3)
    assert ext.get("skip_reason") is None


def test_bucket_counts():
    extractions = [
        _make_extraction("frq", question_number=1),
        _make_extraction("frq", question_number=2, flagged=True, flag_reason="unclear"),
        _make_extraction("skip", skip_reason="title_page"),
        _make_extraction("skip", skip_reason="cover_sheet"),
        _make_extraction("frq", question_number=3),
    ]
    frq_pages = [e for e in extractions if is_frq(e)]
    skip_pages = [e for e in extractions if is_skip(e)]
    flagged_pages = [e for e in frq_pages if is_flagged(e)]

    assert len(frq_pages) == 3
    assert len(skip_pages) == 2
    assert len(flagged_pages) == 1
