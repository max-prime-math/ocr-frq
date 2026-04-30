"""Tests for the FRQCache disk cache."""

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from cache import FRQCache, _image_hash


@pytest.fixture
def tmp_cache(tmp_path):
    return FRQCache(cache_dir=str(tmp_path / "cache"))


@pytest.fixture
def sample_image(tmp_path):
    p = tmp_path / "page.png"
    p.write_bytes(b"\x89PNG\r\n\x1a\n" + b"\x00" * 64)
    return str(p)


def test_miss_returns_none(tmp_cache, sample_image):
    assert tmp_cache.get(sample_image) is None


def test_put_then_get(tmp_cache, sample_image):
    data = {"page_type": "frq", "question_number": 1, "question": "Q"}
    tmp_cache.put(sample_image, data)
    assert tmp_cache.get(sample_image) == data


def test_invalidate_removes_entry(tmp_cache, sample_image):
    tmp_cache.put(sample_image, {"page_type": "skip"})
    tmp_cache.invalidate(sample_image)
    assert tmp_cache.get(sample_image) is None


def test_different_images_different_keys(tmp_path, tmp_cache):
    img1 = tmp_path / "a.png"
    img2 = tmp_path / "b.png"
    img1.write_bytes(b"AAA")
    img2.write_bytes(b"BBB")

    tmp_cache.put(str(img1), {"page_type": "frq"})
    assert tmp_cache.get(str(img2)) is None


def test_hash_is_stable(sample_image):
    h1 = _image_hash(sample_image)
    h2 = _image_hash(sample_image)
    assert h1 == h2


def test_cache_dir_created_on_init(tmp_path):
    cache_dir = tmp_path / "nested" / "cache"
    assert not cache_dir.exists()
    FRQCache(cache_dir=str(cache_dir))
    assert cache_dir.exists()
