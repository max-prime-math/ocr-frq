import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from ap_calculus_curriculum import (BC_ONLY, TOPIC_NAMES, course_classes, curriculum, exam_tags,
                                    load_part_topics, organize, section_topic)

INVENTORY = Path(__file__).resolve().parents[4] / "data/ap-calculus/draft/source-inventory.json"


class ApCalculusCurriculumTests(unittest.TestCase):
    def test_ab_and_bc_curricula_match_course_scope(self):
        ab = curriculum("AB")
        bc = curriculum("BC")
        self.assertEqual([unit["id"] for unit in ab], [f"ap-unit-{n}" for n in range(1, 9)])
        self.assertEqual([unit["id"] for unit in bc], [f"ap-unit-{n}" for n in range(1, 11)])
        ab_topics = {section["id"].removeprefix("ap-topic-").replace("-", ".") for unit in ab for section in unit["sections"]}
        self.assertFalse(ab_topics & BC_ONLY)
        self.assertEqual(len({section["id"] for unit in bc for section in unit["sections"]}), len(TOPIC_NAMES))

    def test_classes_are_calculus_ab_and_bc(self):
        self.assertEqual([(c["id"], c["name"]) for c in course_classes()],
                         [("ap-calculus-ab", "Calculus AB"), ("ap-calculus-bc", "Calculus BC")])

    @unittest.skipUnless(INVENTORY.is_file(), "source inventory not present")
    def test_reviewed_topics_cover_every_question_and_part(self):
        inventory = {row["id"]: row["sourceSubparts"] for row in json.loads(INVENTORY.read_text())["questions"]}
        topics = load_part_topics()
        self.assertEqual(set(topics), set(inventory))
        for qid, parts in topics.items():
            with self.subTest(qid=qid):
                self.assertEqual(list(parts), inventory[qid])
                organize(qid, parts)

    def test_section_is_the_highest_numbered_part_topic(self):
        self.assertEqual(section_topic("ap-calc-ab-2001-frq-01", {"a": "8.4", "b": "8.10", "c": "8.9"}), "8.10")
        self.assertEqual(section_topic("ap-calc-bc-2001-frq-01", {"a": "10.2", "b": "9.6", "c": None}), "10.2")
        placement = organize("ap-calc-ab-2019-frq-01", {"a": "8.3", "b": "8.1", "c": "5.5", "d": "4.3"})
        self.assertEqual(placement["unitName"], "Unit 8: Applications of Integration")
        self.assertEqual(placement["sectionName"], "8.3 Using Accumulation Functions and Definite Integrals in Applied Contexts")

    def test_ab_rejects_bc_only_topics(self):
        with self.assertRaises(ValueError):
            section_topic("ap-calc-ab-2001-frq-01", {"a": "9.1"})
        self.assertEqual(section_topic("ap-calc-bc-2001-frq-01", {"a": "9.1"}), "9.1")

    def test_calculator_part_boundary_moved_in_2011(self):
        self.assertEqual(exam_tags("ap-calc-ab-2010-frq-03"), ["2010", "Part A", "Calculator Active"])
        self.assertEqual(exam_tags("ap-calc-ab-2011-frq-03"), ["2011", "Part B", "No Calculator"])
        self.assertEqual(exam_tags("ap-calc-bc-1998-frq-04"), ["1998", "Part B", "No Calculator"])
        self.assertEqual(exam_tags("ap-calc-bc-2024-frq-02"), ["2024", "Part A", "Calculator Active"])

    def test_form_b_is_tagged(self):
        self.assertEqual(exam_tags("ap-calc-bc-2009-form-b-frq-05"), ["2009", "Form B", "Part B", "No Calculator"])


if __name__ == "__main__":
    unittest.main()
