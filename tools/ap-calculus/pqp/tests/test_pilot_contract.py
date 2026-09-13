from __future__ import annotations

import sys
import unittest
from pathlib import Path

PQP = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PQP))

from build_pilot_catalog import build


class PilotContractTests(unittest.TestCase):
    def test_exactly_twelve_source_locked_questions(self) -> None:
        catalog = build()
        self.assertEqual(catalog["questionCount"], 12)
        self.assertEqual(len(catalog["questions"]), 12)
        self.assertEqual({row["course"] for row in catalog["questions"]}, {"AB", "BC"})
        self.assertEqual(sum(row["course"] == "AB" for row in catalog["questions"]), 6)
        self.assertEqual(sum(row["course"] == "BC" for row in catalog["questions"]), 6)

    def test_every_question_has_a_prompt_and_scoring_source_hash(self) -> None:
        for row in build()["questions"]:
            for document in (row["source"]["prompt"], row["source"]["scoringGuide"]):
                self.assertEqual(len(document["sha256"]), 64)
                self.assertGreater(document["pages"], 0)

    def test_only_bc_relies_on_existing_mathpix_artifacts(self) -> None:
        for row in build()["questions"]:
            if row["course"] == "BC":
                self.assertEqual(row["status"], "legacy-artifacts-available")
            else:
                self.assertEqual(row["status"], "ready-for-pilot-mathpix")


if __name__ == "__main__":
    unittest.main()
