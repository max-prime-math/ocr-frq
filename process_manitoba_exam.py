#!/usr/bin/env python3
"""
Easy-to-use script for processing Manitoba Pre-Calculus 40S exams.
Usage: python process_manitoba_exam.py <zip_file>
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from manitoba_precalc_parser import ManitobaPrecalcParser
from pathlib import Path


def main():
    if len(sys.argv) < 2:
        print("Usage: python process_manitoba_exam.py <zip_file>")
        print("\nExample:")
        print("  python process_manitoba_exam.py mathpix/pre-calc-40s_jan_13_mg-only_cleaned_aggressive.zip")
        sys.exit(1)
    
    zip_file = sys.argv[1]
    
    if not Path(zip_file).exists():
        print(f"Error: File '{zip_file}' not found")
        sys.exit(1)
    
    print(f"Processing Manitoba Pre-Calculus 40S exam: {zip_file}")
    print("-" * 60)
    
    try:
        # Parse the exam
        parser = ManitobaPrecalcParser(zip_file)
        
        # Show summary
        parser.print_summary()
        
        # Generate outputs
        print("\nGenerating outputs...")
        
        # LaTeX exam document
        latex_path = parser.to_latex_exam()
        print(f"✓ LaTeX exam: {latex_path}")
        
        # JSON for bulk import
        json_path = parser.to_json()
        print(f"✓ JSON export: {json_path}")
        
        # Try to compile PDF
        latex_file = Path(latex_path)
        try:
            import subprocess
            result = subprocess.run(
                ['pdflatex', '-interaction=nonstopmode', latex_file.name],
                cwd=latex_file.parent,
                capture_output=True,
                text=True
            )
            if latex_file.with_suffix('.pdf').exists():
                print(f"✓ PDF compiled: {latex_file.with_suffix('.pdf')}")
            else:
                print("⚠ PDF compilation had issues (check LaTeX log)")
        except FileNotFoundError:
            print("⚠ pdflatex not found - LaTeX file generated but not compiled")
        
        print("\n" + "=" * 60)
        print("SUCCESS! Exam processing complete.")
        print("\nFiles generated:")
        print(f"  - LaTeX exam: {latex_path}")
        print(f"  - JSON export: {json_path}")
        
        if Path(latex_path).with_suffix('.pdf').exists():
            print(f"  - PDF document: {Path(latex_path).with_suffix('.pdf')}")
        
        print(f"\nTotal questions processed: {len(parser.questions)}")
        frq_count = sum(1 for q in parser.questions if q.question_type == 'frq')
        mcq_count = sum(1 for q in parser.questions if q.question_type == 'mcq')
        print(f"  - FRQ questions: {frq_count}")
        print(f"  - MCQ questions: {mcq_count}")
        
    except Exception as e:
        print(f"\nError processing exam: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()