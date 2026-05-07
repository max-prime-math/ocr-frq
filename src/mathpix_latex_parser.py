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

    def __init__(self, tex_file: str, manifest_path: Optional[str] = None):
        """
        Initialize with LaTeX file path and optional figure manifest.

        Args:
            tex_file: Path to the MathPix-generated LaTeX file
            manifest_path: Optional path to figure_manifest.json for resolving [figure N] references
        """
        self.tex_file = Path(tex_file)
        with open(self.tex_file) as f:
            self.content = f.read()

        # Extract image directory
        self.image_dir = self.tex_file.parent / "images"

        # Load figure manifest if provided
        self.figure_manifest = {}
        if manifest_path:
            try:
                with open(manifest_path) as f:
                    manifest_data = json.load(f)
                    # Build a lookup map from figure ID to image path
                    for fig in manifest_data.get("figures", []):
                        fig_id = fig.get("id")
                        img_path = fig.get("image_path")
                        if fig_id and img_path:
                            self.figure_manifest[fig_id] = img_path
                    if self.figure_manifest:
                        import logging
                        logging.debug(f"Loaded {len(self.figure_manifest)} figures from manifest")
            except Exception as e:
                import logging
                logging.warning(f"Failed to load figure manifest: {e}")

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
        """
        Find referenced images in this section.

        Supports both:
        1. Traditional \\includegraphics{...} references
        2. New [figure ID] placeholders from pre-extraction pipeline
        """
        images = []

        # Pattern 1: \includegraphics{...image_name...}
        for match in re.finditer(r'\\includegraphics\[.*?\]\{([^}]+)\}', text):
            image_name = match.group(1)
            # Add image extension if missing
            if not image_name.endswith(('.png', '.jpg', '.pdf')):
                image_name += '.png'
            images.append(image_name)

        # Pattern 2: [figure {ID}] placeholders from pre-extraction
        for match in re.finditer(r'\[figure\s+([\w_]+)\]', text):
            figure_id = match.group(1)
            if figure_id in self.figure_manifest:
                image_path = self.figure_manifest[figure_id]
                if image_path not in images:
                    images.append(image_path)
            else:
                # Keep the placeholder text if manifest lookup fails
                import logging
                logging.warning(f"Figure {figure_id} not found in manifest")

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
        print("Usage: python mathpix_latex_parser.py <tex_file> [output.json] [--manifest MANIFEST_PATH]")
        sys.exit(1)

    tex_file = sys.argv[1]
    output_file = None
    manifest_path = None

    # Parse optional arguments
    for i, arg in enumerate(sys.argv[2:], start=2):
        if arg == "--manifest" and i + 1 < len(sys.argv):
            manifest_path = sys.argv[i + 1]
        elif not arg.startswith("--") and output_file is None:
            output_file = arg

    parser = MathPixLatexParser(tex_file, manifest_path=manifest_path)
    parser.print_summary()

    if output_file:
        result = parser.to_json(output_file)
        print(f"✓ Saved to: {output_file}")
