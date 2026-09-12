"""Offline segmentation regressions; cached fixtures require the Manitoba workspace."""
import importlib.util
import os
from pathlib import Path
import sys
import json
import tempfile
import unittest
from unittest.mock import patch

TOOLS = Path(os.environ.get("MANITOBA_PQP_TOOLS", Path(__file__).resolve().parent))
sys.path.insert(0, str(TOOLS))
SPEC = importlib.util.spec_from_file_location(
    "export_under_test", os.environ.get("MANITOBA_EXPORTER", str(TOOLS / "export_manitoba_pqp_mathpix.py")))
exporter = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(exporter)


class SegmentationTests(unittest.TestCase):
    def test_pdf_continuation_stops_at_next_question(self):
        self.assertEqual(exporter.pdf_question_segment(
            ["Question 26", "Solution", "ours", "Question 27", "theirs"], 26, False),
            (["Solution", "ours"], True, False))
        self.assertEqual(exporter.pdf_question_segment(
            ["ours", "Question 27", "theirs"], 26, True), (["ours"], False, False))

    def test_single_choice_diagram_stays_in_choice(self):
        items = [{"kind": "text", "text": "Choose."}]
        items += [{"kind": "text", "text": f"{letter}) value", "sourceY": y,
                   "sourceHeight": 10} for letter, y in zip("ABCD", [10, 30, 50, 70])]
        items.append({"kind": "image", "text": "uuid_20_30_75_50.jpg", "sourceY": 75, "width": 0.3})
        with patch.object(exporter, "latex_to_typst", side_effect=lambda text: text):
            stem, choices, assets = exporter.split_choice_items(items)
        self.assertFalse(any(item["kind"] == "image" for item in stem))
        self.assertIn("includegraphics", choices[-1]["body"]["text"])
        self.assertEqual(len(assets), 1)

    def test_four_image_choices_keep_all_images(self):
        items = [{"kind": "text", "text": "Choose the graph."}]
        for i, letter in enumerate("ABCD"):
            items.extend([{"kind": "text", "text": f"{letter})", "sourceY": i * 100},
                          {"kind": "image", "text": f"uuid_{i}_60_60_10_10.jpg", "width": 0.3}])
        with patch.object(exporter, "latex_to_typst", side_effect=lambda text: text):
            stem, choices, assets = exporter.split_choice_items(items)
        self.assertEqual(len(assets), 4)
        self.assertTrue(all("includegraphics" in choice["body"]["text"] for choice in choices))


@unittest.skipUnless(exporter.FILTER_REPORT_JSON.exists(), "real cached Mathpix workspace absent")
class CachedRegressionTests(unittest.TestCase):
    def test_june_2014_q9_pdf_glyph_fallback_is_quarantined(self):
        row = next(row for row in exporter.load_catalog(2014, "jun", None) if row["question"] == 9)
        candidate = exporter.items_to_text_and_images(exporter.pdf_fallback_solution_items(row))[0]
        self.assertIn("vertical stretch", candidate)
        # Exercise the real export rejection path without conversion, extraction,
        # or writes to the actual bank/PQP workspace.
        with tempfile.TemporaryDirectory() as directory, \
                patch.object(exporter, "load_catalog", return_value=[row]), \
                patch.object(exporter, "OUT_DIR", Path(directory)), \
                patch.object(exporter, "extract_images", return_value={}), \
                patch.object(exporter, "latex_to_typst", side_effect=lambda text: text), \
                patch.object(exporter, "solution_rejection_reason", return_value="empty-or-header-only"):
            package = json.loads(exporter.export_session(2014, "jun").read_text())
        solution = package["questions"][0]["content"]["solution"]
        # A reviewed editorial repair can intentionally populate this field
        # afterwards. The quarantine invariant is that rejected raw PDF text
        # never becomes the original extracted solution or its provenance.
        self.assertEqual(solution["extensions"]["latexSource"], "")
        self.assertNotEqual(solution["text"], candidate)
        diagnostic = next(d for d in package["diagnostics"] if d["code"] == "solution-source-pdf-text-requires-review")
        self.assertEqual(diagnostic["extensions"]["rejectedPdfText"], candidate)

    def test_shared_graphs_belong_to_stems(self):
        cases = [(2013, "jun", 23), (2013, "jun", 24), (2015, "jan", 24),
                 (2015, "jun", 17), (2024, "jan", 19), (2024, "jun", 25),
                 (2025, "jan", 23), (2025, "jun", 22), (2026, "jan", 21), (2026, "jun", 23)]
        for year, term, q in cases:
            row = next(r for r in exporter.load_catalog(year, term, None) if r["question"] == q)
            pages = exporter.doc_page_map(f"pc_{year}_{term}_sb{row['booklet']}")
            self.assertEqual(len(row["sourcePages"]), 1)
            page = pages[row["sourcePages"][0]]
            items = exporter.page_items_for_question(page, q)
            original_images = [item["text"] for item in items if item["kind"] == "image"]
            with patch.object(exporter, "latex_to_typst", side_effect=lambda text: text):
                stem, choices, assets = exporter.split_choice_items(items)
            self.assertEqual([item["text"] for item in stem if item["kind"] == "image"], original_images)
            self.assertEqual(len(original_images), 1)
            self.assertEqual(assets, [])
            self.assertEqual(len(choices), 4)
            self.assertFalse(any("includegraphics" in choice["body"]["text"] for choice in choices))
            self.assertNotIn("1 mark", exporter.items_to_text_and_images(stem)[0])

    def test_june_2013_missing_heading_does_not_mix_solutions(self):
        page = exporter.doc_page_map("pc_2013_jun_mg")[35]
        source = exporter.marking_guide_pdf_path(2013, "jun")
        q26, found26, continues26 = exporter.guide_solution_items_for_question(page, 26, False, source, 35)
        q27, found27, _ = exporter.guide_solution_items_for_question(page, 27, False, source, 35)
        text26 = exporter.items_to_text_and_images(q26)[0]
        text27 = exporter.items_to_text_and_images(q27)[0]
        self.assertTrue(found26 and found27)
        self.assertFalse(continues26)
        self.assertIn("Domain:", text26)
        self.assertIn("Range:", text26)
        self.assertNotIn("19", text26)
        self.assertIn("reciprocal", text27)
        self.assertIn("19", text27)
        self.assertNotIn("Domain:", text27)
        self.assertNotIn("domain", text27)


if __name__ == "__main__":
    unittest.main()
