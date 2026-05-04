#!/usr/bin/env python3
"""
Parse MathPix LaTeX output and extract structured question/solution content.
"""

import re
import json
from pathlib import Path
from typing import List, Dict, Optional


class MathPixLatexParser:
    """Parse MathPix LaTeX document and extract questions/solutions."""

    def __init__(self, tex_file: str):
        """Initialize with LaTeX file path."""
        self.tex_file = Path(tex_file)
        with open(self.tex_file) as f:
            self.content = f.read()

        # Extract image directory
        self.image_dir = self.tex_file.parent / "images"

    def extract_questions(self) -> List[Dict]:
        """
        Extract questions from the LaTeX document.

        Returns:
            List of question dictionaries with content, solution, and metadata
        """
        questions = []

        # Split by section headers (Solution indicates a new question)
        # Pattern: content followed by \section*{Solution}
        parts = re.split(r'\\section\*\{Solution\}', self.content)

        question_num = 0
        for i, part in enumerate(parts):
            if i == 0:
                # Skip preamble
                continue

            question_num += 1

            # Extract question text (everything before the first \section or $$)
            question_text = self._extract_question_text(part)

            # Extract solution (everything after question until next question)
            solution_text = self._extract_solution(part)

            # Extract marks/rubric
            marks = self._extract_marks(solution_text)

            # Find images in this section
            images = self._find_images_in_section(solution_text)

            questions.append({
                'number': question_num,
                'question_text': question_text.strip(),
                'solution': solution_text.strip(),
                'marks': marks,
                'images': images,
                'raw_latex': part.strip(),
            })

        return questions

    def _extract_question_text(self, section: str) -> str:
        """Extract the question statement from a section."""
        # Question ends at first \section or $$ or ends with Question: ...
        match = re.search(r'(.+?)(?:\\section|\$\$|$)', section, re.DOTALL)
        if match:
            text = match.group(1)
            # Remove markdown formatting
            text = re.sub(r'\\\\', ' ', text)
            text = re.sub(r'\n\s*\n', '\n', text)
            return text
        return section[:500]

    def _extract_solution(self, section: str) -> str:
        """Extract solution from a section."""
        # Solution starts after \section*{Solution} or first $$
        match = re.search(r'(?:\\section\*\{.*?\}|$\$)(.*?)(?:(?:^[A-Z].*?[?:]|$))',
                         section, re.DOTALL)
        if match:
            return match.group(1).strip()
        return section

    def _extract_marks(self, text: str) -> Optional[int]:
        """Extract total marks from solution text."""
        # Look for patterns like "3 marks", "2 marks", etc.
        matches = re.findall(r'(\d+)\s+marks?', text, re.IGNORECASE)
        if matches:
            # Return the last occurrence (usually the total)
            return int(matches[-1])
        return None

    def _find_images_in_section(self, text: str) -> List[str]:
        """Find referenced images in this section."""
        # Pattern: \includegraphics{...image_name...}
        images = []
        for match in re.finditer(r'\\includegraphics\[.*?\]\{([^}]+)\}', text):
            image_name = match.group(1)
            # Add image extension if missing
            if not image_name.endswith(('.png', '.jpg', '.pdf')):
                image_name += '.png'
            images.append(image_name)
        return images

    def to_json(self, output_file: Optional[str] = None) -> Dict:
        """Convert to JSON format for test generator."""
        questions = self.extract_questions()

        output = {
            'source_file': str(self.tex_file),
            'exam_info': {
                'type': 'Manitoba Pre-Calculus 40S',
                'total_questions': len(questions),
            },
            'questions': questions,
        }

        if output_file:
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'w') as f:
                json.dump(output, f, indent=2)

        return output

    def print_summary(self):
        """Print a summary of extracted content."""
        questions = self.extract_questions()

        print(f"\n📄 MathPix LaTeX Parsing Summary")
        print("=" * 70)
        print(f"File: {self.tex_file.name}")
        print(f"Total questions extracted: {len(questions)}\n")

        for q in questions:
            print(f"Question {q['number']}: {len(q['question_text'])} chars")
            print(f"  Solution: {len(q['solution'])} chars")
            print(f"  Marks: {q['marks']}")
            print(f"  Images: {len(q['images'])}")
            if q['images']:
                print(f"    - {', '.join(q['images'])}")
            print()


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python mathpix_latex_parser.py <tex_file> [output.json]")
        sys.exit(1)

    tex_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    parser = MathPixLatexParser(tex_file)
    parser.print_summary()

    if output_file:
        result = parser.to_json(output_file)
        print(f"✓ Saved to: {output_file}")
