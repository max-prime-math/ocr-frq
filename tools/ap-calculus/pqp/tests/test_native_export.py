"""Native integration guards; run with python -m unittest discover -s .../tests."""
import importlib.util
import base64
import json
from pathlib import Path
import sys
import tempfile
import unittest

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
from export_ap_native_draft import build, PACKAGE_NAME, sha256


class NativeExportTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.base = self.root / "base"
        self.base.mkdir()
        self.candidates = self.root / "candidates"
        self.candidates.mkdir()
        self.records = self.root / "intermediate" / "records"
        self.records.mkdir(parents=True)
        self.write(self.records / "draft.json", {"id": "draft", "original": "source text"})
        self.output = self.root / "output"
        self.reviewed = {"id": "reviewed", "body": "Reviewed prompt.", "solution": "Reviewed solution.", "tags": ["reviewed"], "images": [], "points": 8, "createdAt": 100, "updatedAt": 100}
        self.draft = {"id": "draft", "body": '#image("/imgs/draft-source-01.png")', "solution": "Solution pending review.", "tags": ["draft", "source-image", "points-provisional"], "images": ["draft-source-01.png"], "points": 9, "createdAt": 100, "updatedAt": 100}
        self.write(self.base / "testgen-question-bank.json", {"format": "test-generator-question-bank", "version": 2, "questions": [self.reviewed, self.draft], "images": []})
        self.write(self.base / PACKAGE_NAME, {"questions": [{"id": question["id"], "content": {"stem": {"text": question["body"]}}, "classification": {"tags": question["tags"]}, "extensions": {"apCalculusDraft": {}}, "provenance": {"extensions": {"crops": []}}} for question in [self.reviewed, self.draft]], "assets": [], "producer": {}, "source": {}, "extensions": {"apCalculusDraft": {}}})
        self.write(self.base / "build-report.json", {"inventory": "inventory.json", "inventorySha256": "sha", "questions": [{"id": "reviewed", "status": "preserved-published"}, {"id": "draft", "status": "draft-source-image"}]})
        self.write(self.base / "repair-queue.json", {"questions": [{"id": "draft", "source": {}, "tasks": ["native-text"]}]})
        self.placements = {qid: {"classId": "ap-calculus-ab", "className": "Calculus AB", "unitId": "ap-unit-8", "unitName": "Unit 8", "sectionId": "ap-topic-8-3", "sectionName": "8.3", "tags": ["2019", "Part A", "Calculator Active"]} for qid in ("reviewed", "draft")}
        self.candidate = {"id": "draft", "bodyTypst": "Let the function be defined for all real numbers. Find the derivative at the given point.", "assets": [], "compile": {"body": True}, "quality": "native-draft", "source": {}, "issues": ["needs review"]}
        self.candidate["sourceRecordSha256"] = sha256(self.records / "draft.json")

    def write(self, path, data):
        path.write_text(json.dumps(data))

    def test_missing_candidate_blocks_before_output(self):
        with self.assertRaisesRegex(ValueError, "missing candidate"):
            build(self.base, self.candidates, self.output)
        self.assertFalse(self.output.exists())

    def test_stale_source_candidate_blocks_before_output(self):
        self.write(self.candidates / "draft.json", self.candidate)
        self.write(self.records / "draft.json", {"id": "draft", "original": "corrected source text"})
        with self.assertRaisesRegex(ValueError, "stale source-record hash"):
            build(self.base, self.candidates, self.output)
        self.assertFalse(self.output.exists())

    def test_image_only_candidate_is_not_native(self):
        self.candidate["bodyTypst"] = '#image("/imgs/figure.png", width: 90%)'
        self.write(self.candidates / "draft.json", self.candidate)
        with self.assertRaisesRegex(ValueError, "substantive editable prompt"):
            build(self.base, self.candidates, self.output)
        self.assertFalse(self.output.exists())

    def test_failed_compile_blocks(self):
        self.candidate["compile"]["body"] = False
        self.write(self.candidates / "draft.json", self.candidate)
        with self.assertRaisesRegex(ValueError, "has not compiled"):
            build(self.base, self.candidates, self.output)

    def test_placeholder_prompt_blocks(self):
        self.candidate["bodyTypst"] = "Question pending review. The original source document contains all information needed for this exercise."
        self.write(self.candidates / "draft.json", self.candidate)
        with self.assertRaisesRegex(ValueError, "placeholder prompt"):
            build(self.base, self.candidates, self.output)

    def test_missing_asset_blocks(self):
        self.candidate["bodyTypst"] += '\n#image("/imgs/figure.png")'
        self.candidate["assets"] = [{"name": "figure.png", "path": str(self.root / "absent.png")}]
        self.write(self.candidates / "draft.json", self.candidate)
        with self.assertRaisesRegex(ValueError, "missing asset"):
            build(self.base, self.candidates, self.output)
        self.assertFalse(self.output.exists())

    def test_unlisted_asset_blocks(self):
        self.candidate["bodyTypst"] += '\n#image("/imgs/figure.png")'
        self.write(self.candidates / "draft.json", self.candidate)
        with self.assertRaisesRegex(ValueError, "referenced assets differ"):
            build(self.base, self.candidates, self.output)

    def test_full_prompt_crop_blocks(self):
        asset = self.root / "draft-source-01.png"
        asset.write_bytes(b"fixture bytes")
        self.candidate["bodyTypst"] += '\n#image("/imgs/draft-source-01.png")'
        self.candidate["assets"] = [{"name": asset.name, "path": str(asset)}]
        self.write(self.candidates / "draft.json", self.candidate)
        with self.assertRaisesRegex(ValueError, "full-prompt source crop"):
            build(self.base, self.candidates, self.output)

    def test_native_asset_embedded_and_bundled_unchanged(self):
        asset = self.root / "figure.png"
        asset.write_bytes(b"fixture image bytes")
        self.candidate["bodyTypst"] += '\n#image("/imgs/figure.png")'
        self.candidate["assets"] = [{"name": asset.name, "path": str(asset)}]
        self.write(self.candidates / "draft.json", self.candidate)
        report = build(self.base, self.candidates, self.output, placements=self.placements)
        bank = json.loads((self.output / "testgen-question-bank.json").read_text())
        package = json.loads((self.output / PACKAGE_NAME).read_text())
        self.assertEqual(report["assetCount"], 1)
        self.assertEqual(bank["questions"][1]["images"], ["figure.png"])
        self.assertEqual(base64.b64decode(bank["images"][0]["data"]), asset.read_bytes())
        self.assertEqual((self.output / "imgs" / "figure.png").read_bytes(), asset.read_bytes())
        self.assertEqual(package["questions"][1]["assets"], ["figure"])
        self.assertEqual(package["assets"][0]["storage"]["path"], "imgs/figure.png")

    def test_duplicate_asset_name_blocks(self):
        asset = self.root / "figure.png"
        asset.write_bytes(b"fixture image bytes")
        self.candidate["bodyTypst"] += '\n#image("/imgs/figure.png")'
        self.candidate["assets"] = [{"name": asset.name, "path": str(asset)}] * 2
        self.write(self.candidates / "draft.json", self.candidate)
        with self.assertRaisesRegex(ValueError, "duplicate supplied asset"):
            build(self.base, self.candidates, self.output)

    def test_native_integration_preserves_reviewed_and_placeholder(self):
        self.write(self.candidates / "draft.json", self.candidate)
        report = build(self.base, self.candidates, self.output, placements=self.placements)
        self.assertEqual(report["nativeDraftCount"], 1)
        self.assertEqual(report["preservedPublishedCount"], 1)
        self.assertEqual(report["sourceImageFallbackCount"], 0)
        bank = json.loads((self.output / "testgen-question-bank.json").read_text())
        # Reviewed content is untouched; only the bank placement is applied.
        placement = {"classId": "ap-calculus-ab", "unitId": "ap-unit-8", "sectionId": "ap-topic-8-3", "tags": ["2019", "Part A", "Calculator Active"]}
        self.assertEqual(bank["questions"][0], {**self.reviewed, **placement})
        self.assertEqual(bank["questions"][1]["solution"], self.draft["solution"])
        self.assertEqual(bank["questions"][1]["body"], self.candidate["bodyTypst"])
        self.assertEqual(bank["questions"][1]["images"], [])
        for question in bank["questions"]:
            self.assertEqual(question["tags"], ["2019", "Part A", "Calculator Active"])
            self.assertEqual(question["classId"], "ap-calculus-ab")
        queue = json.loads((self.output / "repair-queue.json").read_text())
        self.assertNotIn("native-text", queue["questions"][0]["tasks"])
        self.assertIn("ocr-content-review", queue["questions"][0]["tasks"])

    def test_cannot_overwrite_base_or_local_folder(self):
        with self.assertRaisesRegex(ValueError, "overwrite the image-draft"):
            build(self.base, self.candidates, self.base)
        self.output.mkdir()
        self.write(self.output / "manifest.json", {"version": 1})
        with self.assertRaisesRegex(ValueError, "connected local-folder"):
            build(self.base, self.candidates, self.output)


if __name__ == "__main__":
    unittest.main()
