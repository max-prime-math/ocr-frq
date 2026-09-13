from __future__ import annotations

import sys
import unittest
from pathlib import Path

PQP = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PQP))

from build_tranche_catalog import build


class Tranche01ContractTests(unittest.TestCase):
    def test_exactly_twelve_cache_backed_questions(self) -> None:
        catalog = build()
        self.assertEqual(catalog["questionCount"], 12)
        self.assertEqual({row["course"] for row in catalog["questions"]}, {"BC"})
        self.assertEqual({row["year"] for row in catalog["questions"]}, {1999, 2000})

    def test_every_question_has_paired_source_and_legacy_hashes(self) -> None:
        for row in build()["questions"]:
            for document in (row["source"]["prompt"], row["source"]["scoringGuide"]):
                self.assertEqual(len(document["sha256"]), 64)
            for artifact in row["legacyMathpix"].values():
                self.assertEqual(len(artifact["sha256"]), 64)
                self.assertTrue(artifact["texMember"].endswith(".tex"))
            self.assertEqual(row["publishState"], "blocked")


if __name__ == "__main__":
    unittest.main()
