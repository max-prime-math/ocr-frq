"""Tests for extraction result handling (no live API calls)."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


def _make_extraction(**kwargs):
    defaults = {
        "page_type": "frq",
        "skip_reason": None,
        "question_number": None,
        "question": None,
        "solution": None,
        "grading_scheme": None,
        "figures": [],
        "tables": [],
        "unit": None,
        "section": None,
        "calculator": None,
        "flagged": False,
        "flag_reason": None,
    }
    defaults.update(kwargs)
    return defaults


# ---------------------------------------------------------------------------
# Schema completeness
# ---------------------------------------------------------------------------

REQUIRED_KEYS = {
    "page_type", "skip_reason", "question_number", "question",
    "solution", "grading_scheme", "figures", "tables",
    "unit", "section", "calculator", "flagged", "flag_reason",
}


def test_frq_extraction_has_all_keys():
    ext = _make_extraction(page_type="frq", question_number=1, question="Q")
    assert REQUIRED_KEYS.issubset(ext.keys())


def test_skip_extraction_has_all_keys():
    ext = _make_extraction(page_type="skip", skip_reason="title_page")
    assert REQUIRED_KEYS.issubset(ext.keys())


# ---------------------------------------------------------------------------
# Null handling for skip pages
# ---------------------------------------------------------------------------

def test_skip_page_fields_are_null():
    ext = _make_extraction(page_type="skip", skip_reason="cover_sheet")
    assert ext["question"] is None
    assert ext["solution"] is None
    assert ext["grading_scheme"] is None
    assert ext["question_number"] is None


# ---------------------------------------------------------------------------
# Partial extraction (missing fields should be null, not absent)
# ---------------------------------------------------------------------------

def test_frq_page_with_missing_solution():
    ext = _make_extraction(page_type="frq", question_number=1, question="Q", flagged=True,
                           flag_reason="left column unreadable")
    assert ext["solution"] is None
    assert ext["flagged"] is True
    assert ext["flag_reason"] is not None


def test_frq_page_all_fields_present():
    ext = _make_extraction(
        page_type="frq",
        question_number=2,
        question="Find the integral.",
        solution="The answer is \\(\\int_0^1 x\\,dx = \\frac{1}{2}\\).",
        grading_scheme="2 : { 1 : antiderivative / 1 : answer }",
    )
    assert ext["question_number"] == 2
    assert "integral" in ext["question"]
    assert ext["solution"] is not None
    assert ext["grading_scheme"] is not None
    assert not ext["flagged"]


# ---------------------------------------------------------------------------
# page_type values
# ---------------------------------------------------------------------------

def test_valid_page_types():
    for pt in ("frq", "skip"):
        ext = _make_extraction(page_type=pt)
        assert ext["page_type"] == pt


def test_frq_flagged_false_by_default():
    ext = _make_extraction(page_type="frq")
    assert ext["flagged"] is False
    assert ext["flag_reason"] is None


# ---------------------------------------------------------------------------
# Cache round-trip with FRQCache
# ---------------------------------------------------------------------------

def test_cache_stores_and_retrieves_extraction(tmp_path):
    from cache import FRQCache

    cache = FRQCache(cache_dir=str(tmp_path))
    img = tmp_path / "page.png"
    img.write_bytes(b"\x89PNG\r\n\x1a\n" + b"\x00" * 32)

    ext = _make_extraction(page_type="frq", question_number=5, question="Q text")
    cache.put(str(img), ext)
    retrieved = cache.get(str(img))

    assert retrieved == ext
    assert retrieved["question_number"] == 5
