#!/usr/bin/env python3
"""
Specialized parser for Manitoba Pre-Calculus 40S exams.
Handles both FRQ and MCQ content with proper styling.
"""

import re
import json
import zipfile
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass


@dataclass
class PreCalcQuestion:
    """Represents a Manitoba Pre-Calculus question."""
    number: int
    question_text: str
    solution: str
    question_type: str  # 'frq' or 'mcq'
    choices: List[str]  # For MCQs
    correct_choice: Optional[int]  # For MCQs (0-indexed)
    marks: Optional[int]
    images: List[str]
    raw_content: str


class ManitobaPrecalcParser:
    """Parse Manitoba Pre-Calculus exam from Mathpix zip export."""
    
    def __init__(self, zip_path: str):
        """Initialize with zip file path."""
        self.zip_path = Path(zip_path)
        self.questions = []
        self.tex_content = ""
        self.image_dir = None
        
        self._extract_and_parse()
    
    def _extract_and_parse(self):
        """Extract zip file and parse content."""
        with zipfile.ZipFile(self.zip_path, 'r') as zip_ref:
            # Find the tex file
            tex_files = [f for f in zip_ref.namelist() if f.endswith('.tex')]
            if not tex_files:
                raise ValueError("No .tex file found in zip")
            
            tex_file = tex_files[0]
            self.tex_content = zip_ref.read(tex_file).decode('utf-8')
            
            # Extract to temp directory to access images
            temp_dir = self.zip_path.parent / f"{self.zip_path.stem}_extracted"
            zip_ref.extractall(temp_dir)
            
            # Find image directory
            for root in temp_dir.iterdir():
                if root.is_dir():
                    img_dir = root / "images"
                    if img_dir.exists():
                        self.image_dir = img_dir
                        break
        
        self._parse_questions()
    
    def _parse_questions(self):
        """Parse questions from LaTeX content."""
        # Better approach: identify actual question markers
        # Based on the content, real questions seem to start with specific patterns
        
        # Define question start patterns
        question_patterns = [
            r'Gina correctly started',
            r'Find and simplify the \d+.*?term',
            r'The number of times a website',
            r'Solve algebraically:',
            r'A word contains',
            r'There is a group of \d+ boys',
            r'Claire correctly solves',
            r'Given the graph of the function',
            r'A school offers',
            r'Explain how Pascal',
            r'Prove the identity',
            r'Your classmate.*?was absent',
            r'Identify the value of the.*?intercept',
            r'Sketch the graph of',
            r'Given the following sinusoidal',
            r'Determine all non-permissible values',
            r'Given that.*?h\(x\)',
            r'Determine the exact value of:',
        ]
        
        # Find all potential question starts
        question_starts = []
        for pattern in question_patterns:
            for match in re.finditer(pattern, self.tex_content, re.IGNORECASE):
                question_starts.append(match.start())
        
        # Sort by position
        question_starts.sort()
        
        # Add document end
        question_starts.append(len(self.tex_content))
        
        # Extract questions based on these boundaries
        for i in range(len(question_starts) - 1):
            start_pos = question_starts[i]
            end_pos = question_starts[i + 1]
            
            section_content = self.tex_content[start_pos:end_pos].strip()
            
            # Skip if too short
            if len(section_content) < 50:
                continue
            
            # Look for solution marker
            solution_match = re.search(r'\\section\*\{Solution\}', section_content, re.IGNORECASE)
            
            if solution_match:
                question_part = section_content[:solution_match.start()].strip()
                solution_part = section_content[solution_match.end():].strip()
                
                # Clean question text
                question_text = self._clean_question_text(question_part)
                
                # Skip if question is too short or looks like notes
                if len(question_text) < 20 or 'Note(' in question_text:
                    continue
                
                # Extract solution
                solution = self._extract_solution(solution_part)
                
                # Extract marks
                marks = self._extract_marks(solution_part)
                
                # Find images
                images = self._find_images(section_content)
                
                question = PreCalcQuestion(
                    number=len(self.questions) + 1,
                    question_text=question_text,
                    solution=solution,
                    question_type='frq',  # All are FRQ for now
                    choices=[],
                    correct_choice=None,
                    marks=marks,
                    images=images,
                    raw_content=section_content
                )
                
                self.questions.append(question)
    
    def _clean_question_text(self, text: str) -> str:
        """Clean and format question text."""
        # Remove LaTeX preamble stuff
        text = re.sub(r'\\documentclass.*?\\begin\{document\}', '', text, flags=re.DOTALL)
        text = re.sub(r'\\captionsetup.*?$', '', text, flags=re.MULTILINE)
        
        # Fix max width issues in includegraphics
        text = re.sub(r'\\includegraphics\[max width=\\textwidth([^\]]*)\]', r'\\includegraphics[width=0.8\\textwidth\1]', text)
        
        # Clean up extra whitespace and newlines
        text = re.sub(r'\n\s*\n', '\n\n', text)
        text = re.sub(r'\\\\', '\n', text)
        
        return text.strip()
    
    def _detect_mcq(self, question_text: str, solution_text: str) -> Tuple[bool, List[str], Optional[int]]:
        """Detect if this might be a multiple choice question and extract choices."""
        # For now, we'll treat all as FRQ since the current file doesn't have clear MCQ patterns
        # This can be enhanced if we find MCQ-specific patterns in the content
        return False, [], None
    
    def _extract_solution(self, solution_text: str) -> str:
        """Extract and clean solution text."""
        # Remove excess section markers
        solution = re.sub(r'\\section\*\{[^}]+\}', '', solution_text)
        
        # Clean up method markers but keep the content
        solution = re.sub(r'\\section\*\{Method (\d+)\}', r'**Method \1:**', solution)
        
        # Fix max width issues in includegraphics
        solution = re.sub(r'\\includegraphics\[max width=\\textwidth([^\]]*)\]', r'\\includegraphics[width=0.8\\textwidth\1]', solution)
        
        # Remove excessive marks annotations that are scattered
        solution = re.sub(r'\d+\s+marks?\s*$', '', solution, flags=re.MULTILINE)
        solution = re.sub(r'\d+/\d+\s+mark.*$', '', solution, flags=re.MULTILINE)
        solution = re.sub(r'\\\\\s*\d+\s+marks?\s*$', '', solution, flags=re.MULTILINE)
        
        return solution.strip()
    
    def _extract_marks(self, text: str) -> Optional[int]:
        """Extract total marks from text."""
        # Look for final marks declaration
        marks_patterns = [
            r'(\d+)\s+marks?\s*$',
            r'\\\\?\s*(\d+)\s+marks?\s*$',
            r'\\section\*\{(\d+)\s+marks?\}',
        ]
        
        for pattern in marks_patterns:
            matches = re.findall(pattern, text, re.MULTILINE | re.IGNORECASE)
            if matches:
                try:
                    return int(matches[-1])
                except ValueError:
                    continue
        
        return None
    
    def _find_images(self, text: str) -> List[str]:
        """Find image references in text."""
        images = []
        # Look for includegraphics commands
        pattern = r'\\includegraphics\[.*?\]\{([^}]+)\}'
        
        for match in re.finditer(pattern, text):
            image_name = match.group(1)
            # Add extension if missing
            if not any(image_name.endswith(ext) for ext in ['.jpg', '.png', '.pdf']):
                image_name += '.jpg'  # Default to jpg since that's what we have
            images.append(image_name)
        
        # Remove duplicates while preserving order
        seen = set()
        unique_images = []
        for img in images:
            if img not in seen:
                seen.add(img)
                unique_images.append(img)
        
        return unique_images
    
    def to_latex_exam(self, output_path: Optional[str] = None) -> str:
        """Generate LaTeX exam document with proper styling."""
        if output_path is None:
            output_path = self.zip_path.parent / f"{self.zip_path.stem}_formatted.tex"
        
        latex_lines = [
            r"\documentclass[12pt,addpoints]{exam}",
            r"\usepackage[utf8]{inputenc}",
            r"\usepackage[T1]{fontenc}",
            r"\usepackage{amsmath,amsfonts,amssymb}",
            r"\usepackage{graphicx}",
            r"\usepackage{geometry}",

            r"\geometry{margin=1in}",
            r"\graphicspath{{./images/}}",
            r"",
            r"\title{Manitoba Pre-Calculus 40S Exam}",
            r"\author{}",
            r"\date{}",
            r"",
            r"\begin{document}",
            r"\maketitle",
            r"",
            r"\begin{questions}",
        ]
        
        for question in self.questions:
            if question.question_type == 'mcq':
                latex_lines.extend(self._format_mcq(question))
            else:
                latex_lines.extend(self._format_frq(question))
        
        latex_lines.extend([
            r"\end{questions}",
            r"\end{document}"
        ])
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(latex_lines))
        
        return str(output_path)
    
    def _format_frq(self, question: PreCalcQuestion) -> List[str]:
        """Format FRQ-style question."""
        lines = []
        
        # Question header with points
        points = question.marks or 3
        lines.append(f"\\question[{points}]")
        lines.append(question.question_text)
        lines.append("")
        
        # Add images if any
        for image in question.images:
            lines.append(f"\\includegraphics[width=0.8\\textwidth]{{{image}}}")
            lines.append("")
        
        # Solution environment
        lines.append("\\begin{solution}")
        lines.append(question.solution)
        lines.append("\\end{solution}")
        lines.append("")
        
        return lines
    
    def _format_mcq(self, question: PreCalcQuestion) -> List[str]:
        """Format MCQ-style question (for future use)."""
        lines = []
        
        points = question.marks or 1
        lines.append(f"\\question[{points}]")
        lines.append(question.question_text)
        lines.append("")
        
        if question.choices:
            lines.append("\\begin{choices}")
            for i, choice in enumerate(question.choices):
                if question.correct_choice == i:
                    lines.append(f"  \\CorrectChoice {choice}")
                else:
                    lines.append(f"  \\choice {choice}")
            lines.append("\\end{choices}")
        
        # Add images if any
        for image in question.images:
            lines.append(f"\\includegraphics[width=0.8\\textwidth]{{{image}}}")
            lines.append("")
        
        # Solution environment
        if question.solution:
            lines.append("\\begin{solution}")
            lines.append(question.solution)
            lines.append("\\end{solution}")
        
        lines.append("")
        return lines
    
    def to_json(self, output_path: Optional[str] = None) -> str:
        """Export to JSON format for bulk import."""
        if output_path is None:
            output_path = self.zip_path.parent / f"{self.zip_path.stem}_processed.json"
        
        questions_data = []
        
        for q in self.questions:
            question_data = {
                "number": q.number,
                "questionType": q.question_type,
                "body": q.question_text,
                "solution": q.solution,
                "points": float(q.marks or 0),
                "tagInput": "Pre-Calculus 40S, Manitoba, January 2013",
                "classId": "pre-calc-40s",
                "unitId": self._detect_unit(q.question_text, q.solution),
                "images": q.images,
            }
            
            if q.question_type == 'mcq':
                question_data["choices"] = q.choices
                question_data["correctChoice"] = q.correct_choice
            
            questions_data.append(question_data)
        
        output = {
            "source": str(self.zip_path),
            "exam_info": {
                "type": "Manitoba Pre-Calculus 40S",
                "date": "January 2013",
                "total_questions": len(self.questions),
            },
            "questions": questions_data,
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2)
        
        return str(output_path)
    
    def _detect_unit(self, question_text: str, solution_text: str) -> str:
        """Detect curriculum unit based on content."""
        combined = (question_text + " " + solution_text).lower()
        
        patterns = {
            "unit-a-trig": r"(sin|cos|tan|radian|degree|θ|trigonometric)",
            "unit-b-binomial": r"(binomial|expansion|combination|term)",
            "unit-c-exponential": r"(exponential|growth|decay|e\^|visitors)",
            "unit-d-logarithm": r"(logarithm|log|ln\()",
            "unit-e-rational": r"(rational|fraction|asymptote)",
            "unit-f-polynomial": r"(polynomial|factor|root|remainder)",
        }
        
        scores = {unit: len(re.findall(pattern, combined)) for unit, pattern in patterns.items()}
        best_unit = max(scores, key=scores.get) if max(scores.values()) > 0 else "unit-a-trig"
        
        return best_unit
    
    def print_summary(self):
        """Print parsing summary."""
        print(f"\n📄 Manitoba Pre-Calculus Parser Summary")
        print("=" * 70)
        print(f"Source: {self.zip_path.name}")
        print(f"Total questions: {len(self.questions)}")
        
        frq_count = sum(1 for q in self.questions if q.question_type == 'frq')
        mcq_count = sum(1 for q in self.questions if q.question_type == 'mcq')
        
        print(f"FRQ questions: {frq_count}")
        print(f"MCQ questions: {mcq_count}")
        print()
        
        for q in self.questions:
            print(f"Question {q.number} ({q.question_type.upper()}): {q.marks or 'N/A'} marks")
            print(f"  Text: {q.question_text[:60]}...")
            print(f"  Images: {len(q.images)}")
            if q.images:
                print(f"    - {', '.join(q.images)}")
            print()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python manitoba_precalc_parser.py <zip_file> [--latex] [--json]")
        sys.exit(1)
    
    zip_file = sys.argv[1]
    
    try:
        parser = ManitobaPrecalcParser(zip_file)
        parser.print_summary()
        
        if '--latex' in sys.argv:
            latex_path = parser.to_latex_exam()
            print(f"✓ Generated LaTeX: {latex_path}")
        
        if '--json' in sys.argv:
            json_path = parser.to_json()
            print(f"✓ Generated JSON: {json_path}")
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)