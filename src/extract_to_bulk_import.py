#!/usr/bin/env python3
"""
Convert extracted MathPix questions to bulk-import format.
Creates:
1. DraftQuestion JSON for test-generator bulk importer
2. Compilable LaTeX exam document
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Optional
import shutil


class ExtractedToBulkImport:
    """Convert extracted questions to DraftQuestion format."""

    def __init__(self, extracted_json: str, images_source: Optional[str] = None, output_dir: Optional[str] = None):
        """Initialize with extracted questions JSON."""
        self.extracted_path = Path(extracted_json)
        self.images_source = Path(images_source) if images_source else self.extracted_path.parent.parent / "mathpix_input" / "images"
        self.output_dir = Path(output_dir) if output_dir else self.extracted_path.parent / "bulk_import_output"
        self.output_dir.mkdir(parents=True, exist_ok=True)

        with open(self.extracted_path) as f:
            self.data = json.load(f)

    def _clean_latex_body(self, text: str) -> str:
        """Clean LaTeX body by removing document markers and excess content."""
        # Remove \end{document} and \begin{document}
        text = re.sub(r'\\(?:end|begin)\{document\}', '', text)
        # Remove everything from \end{document} onwards (safety)
        text = text.split(r'\end{document}')[0]
        # Remove excessive \section* markers beyond the first
        lines = text.split('\n')
        cleaned = []
        section_count = 0
        for line in lines:
            if r'\section*{' in line:
                section_count += 1
                if section_count > 2:  # Keep first 2 sections at most
                    continue
            cleaned.append(line)
        return '\n'.join(cleaned).strip()

    def _detect_topic(self, question_text: str, solution_text: str) -> str:
        """Detect question topic for curriculum classification."""
        combined = (question_text + " " + solution_text).lower()

        patterns = {
            "trigonometric": r"(sin|cos|tan|radian|degree|θ)",
            "binomial": r"(binomial|expansion|combination|nCr)",
            "exponential": r"(exponential|growth|decay|e\^)",
            "logarithm": r"(logarithm|log|ln\()",
            "rational": r"(rational|fraction|asymptote)",
            "polynomial": r"(polynomial|factor|root|remainder)",
            "sequences": r"(sequence|series|arithmetic|geometric)",
        }

        scores = {topic: len(re.findall(pattern, combined)) for topic, pattern in patterns.items()}
        best = max(scores, key=scores.get) if max(scores.values()) > 0 else "general"
        return best

    def to_draft_questions(self) -> List[Dict]:
        """Convert to DraftQuestion format for bulk importer."""
        questions = self.data.get("questions", [])
        draft_questions = []

        for q in questions:
            # Clean solution text first (remove document markers)
            solution_raw = q.get("solution", "").strip()
            # Remove \end{document} and anything after
            solution = solution_raw.split(r'\end{document}')[0].strip()

            # Use cleaned solution for body (truncated)
            body = self._clean_latex_body(solution[:500])

            if not body or not solution:
                continue

            # Detect curriculum mapping
            topic = self._detect_topic(body, solution)
            unit_map = {
                "trigonometric": "unit-a-trig",
                "binomial": "unit-b-binomial",
                "exponential": "unit-c-exponential",
                "logarithm": "unit-d-logarithm",
                "rational": "unit-e-rational",
                "polynomial": "unit-f-polynomial",
                "sequences": "unit-g-sequences",
                "general": "unit-a-trig",
            }

            draft_q = {
                "body": body,
                "questionType": "frq",
                "answer": "",
                "solution": solution,
                "points": float(q.get("marks") or 0),
                "tagInput": f"Pre-Calculus 40S, Manitoba, {topic}",
                "classId": "pre-calc-40s",
                "unitId": unit_map.get(topic, "unit-a-trig"),
                "sectionId": topic,
            }

            if q.get("images"):
                draft_q["images"] = q["images"]

            draft_questions.append(draft_q)

        return draft_questions

    def save_bulk_import_json(self, output_path: Optional[str] = None) -> str:
        """Save bulk import JSON."""
        if output_path is None:
            output_path = str(self.output_dir / "bulk_import.json")

        draft_questions = self.to_draft_questions()

        output = {
            "source": self.data.get("source_file", "unknown"),
            "exam_type": self.data.get("exam_info", {}).get("type", "Unknown"),
            "total_questions": len(draft_questions),
            "questions": draft_questions,
        }

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(output, f, indent=2)

        return str(output_path)

    def generate_latex_exam(self, output_path: Optional[str] = None) -> str:
        """Generate clean LaTeX exam document."""
        if output_path is None:
            output_path = str(self.output_dir / "exam.tex")

        output_path = Path(output_path)
        draft_questions = self.to_draft_questions()

        latex = [
            r"\documentclass[addpoints]{exam}",
            r"\usepackage[utf8]{inputenc}",
            r"\usepackage[T1]{fontenc}",
            r"\usepackage{amsmath,amsfonts,amssymb}",
            r"\usepackage{graphicx}",
            r"\usepackage{geometry}",
            r"\geometry{margin=1in}",
            r"\graphicspath{{./images/}}",
            r"",
            r"\title{Manitoba Pre-Calculus 40S}",
            r"\author{}",
            r"\date{}",
            r"",
            r"\begin{document}",
            r"\maketitle",
            r"",
        ]

        for i, dq in enumerate(draft_questions, 1):
            points = int(dq["points"])
            latex.append(r"\begin{questions}")
            latex.append(rf"\question[{points}]")
            latex.append(dq["body"])
            latex.append("")
            latex.append(r"\begin{solution}")
            latex.append(dq["solution"])
            latex.append(r"\end{solution}")
            latex.append(r"\end{questions}")
            latex.append("")

        latex.append(r"\end{document}")

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w') as f:
            f.write("\n".join(latex))

        return str(output_path)

    def copy_images(self) -> int:
        """Copy images to output directory."""
        if not self.images_source.exists():
            return 0

        images_dest = self.output_dir / "images"
        images_dest.mkdir(parents=True, exist_ok=True)

        count = 0
        for img in self.images_source.glob("*"):
            if img.is_file():
                shutil.copy2(img, images_dest / img.name)
                count += 1

        return count

    def print_summary(self):
        """Print conversion summary."""
        questions = self.to_draft_questions()

        print(f"\n📋 Extracted to Bulk Import")
        print("=" * 70)
        print(f"Source: {self.extracted_path.name}")
        print(f"Questions: {len(questions)}")
        print(f"Output: {self.output_dir}")

        topics = {}
        for q in questions:
            topic = q["sectionId"]
            topics[topic] = topics.get(topic, 0) + 1

        print(f"\nTopics:")
        for topic, count in sorted(topics.items()):
            print(f"  {topic}: {count}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python extract_to_bulk_import.py <extracted.json> [images_dir] [output_dir]")
        sys.exit(1)

    json_file = sys.argv[1]
    images_dir = sys.argv[2] if len(sys.argv) > 2 else None
    output_dir = sys.argv[3] if len(sys.argv) > 3 else None

    converter = ExtractedToBulkImport(json_file, images_dir, output_dir)
    converter.print_summary()

    json_out = converter.save_bulk_import_json()
    latex_out = converter.generate_latex_exam()
    img_count = converter.copy_images()

    print(f"\n✓ Saved bulk import JSON: {json_out}")
    print(f"✓ Saved LaTeX exam: {latex_out}")
    print(f"✓ Copied {img_count} images")
