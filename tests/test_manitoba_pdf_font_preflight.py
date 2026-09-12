"""Unit checks, plus optional integration against the real June 2014 source.

Run with MT_EXTRA_SOURCE=/path/to/pc_14_jun_mg.pdf and
MT_EXTRA_REPLACEMENT_FONT=/path/to/NotoSansMath-Regular.ttf for integration.
"""
import importlib.util
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import fitz

MODULE = Path(__file__).resolve().parents[1] / "tools/manitoba-precalc-40s/pqp/manitoba_pdf_font_preflight.py"
if not MODULE.exists():
    MODULE = Path(__file__).with_name("manitoba_pdf_font_preflight.py")
spec = importlib.util.spec_from_file_location("font_preflight", MODULE)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class FontPreflightTests(unittest.TestCase):
    def test_face_matching_is_not_global_character_replacement(self):
        self.assertTrue(module.is_mt_extra("ABCDEF+MT-Extra"))
        self.assertFalse(module.is_mt_extra("TimesNewRomanPS-ItalicMT"))
        self.assertEqual(module.REVIEWED_MAPPING[0x67], 0x22C5)
        self.assertNotIn(ord("R"), module.REVIEWED_MAPPING)

    def test_unknown_codes_block_before_writing(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "new.pdf"
            with patch.object(module, "inspect_pdf", return_value={"unknown_codes": ["0x42"]}):
                with self.assertRaisesRegex(ValueError, "Unreviewed"):
                    module.normalize_pdf(Path("source.pdf"), output, Path("font.ttf"))
            self.assertFalse(output.exists())

    def test_no_missing_font_is_not_rewritten(self):
        with tempfile.TemporaryDirectory() as temp:
            with patch.object(module, "inspect_pdf", return_value={"unknown_codes": [], "missing_mt_extra": []}):
                with self.assertRaisesRegex(ValueError, "No missing"):
                    module.normalize_pdf(Path("source.pdf"), Path(temp) / "new.pdf", Path("font.ttf"))

    @unittest.skipUnless(os.environ.get("MT_EXTRA_SOURCE") and os.environ.get("MT_EXTRA_REPLACEMENT_FONT"),
                         "Set source/font environment paths for real-document integration")
    def test_real_june2014_glyphs_and_other_content(self):
        source = Path(os.environ["MT_EXTRA_SOURCE"])
        font = Path(os.environ["MT_EXTRA_REPLACEMENT_FONT"])
        original_hash = module.digest(source)
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "normalized.pdf"
            report = module.normalize_pdf(source, output, font)
            self.assertEqual(report["codes"], {"0x55": 1, "0x67": 33, "0x6F": 3, "0xA1": 8})
            self.assertEqual(module.digest(source), original_hash)
            old, new = fitz.open(source), fitz.open(output)
            unchanged_old, unchanged_new, repaired = [], [], []
            for p, q in zip(old, new):
                unchanged_old.extend((t["font"], t["chars"]) for t in p.get_texttrace() if t["font"] != "MT-Extra")
                unchanged_new.extend((t["font"], t["chars"]) for t in q.get_texttrace() if "NotoSansMath" not in t["font"])
                repaired.extend(chr(c[0]) for t in q.get_texttrace() if "NotoSansMath" in t["font"] for c in t["chars"])
            self.assertEqual(unchanged_old, unchanged_new)
            self.assertEqual(repaired.count("⋅"), 33)
            self.assertEqual(repaired.count("ℝ"), 8)
            self.assertFalse(module.inspect_pdf(output)["missing_mt_extra"])
            with self.assertRaisesRegex(ValueError, "new file"):
                module.normalize_pdf(source, output, font)


if __name__ == "__main__":
    unittest.main()
