# Bulk Import Output Format

This document explains the bulk import files created by the extraction pipeline.

## Files Generated

### 1. `bulk_import.json`

JSON file containing an array of `DraftQuestion` objects compatible with test-generator's bulk importer.

**Structure:**
```json
{
  "source": "path/to/mathpix/latex/file.tex",
  "exam_type": "Manitoba Pre-Calculus 40S",
  "total_questions": 41,
  "questions": [
    {
      "body": "LaTeX equation/problem statement",
      "questionType": "frq",
      "answer": "",
      "solution": "LaTeX solution with working",
      "points": 3.0,
      "tagInput": "Pre-Calculus 40S, Manitoba, trigonometric",
      "classId": "pre-calc-40s",
      "unitId": "unit-a-trig",
      "sectionId": "trigonometric",
      "images": ["image1.png", "image2.png"]
    }
  ]
}
```

**Field Descriptions:**
- `body`: Question statement in LaTeX (truncated from solution for brevity)
- `questionType`: Always "frq" for free-response questions
- `answer`: Empty string (no single answer for FRQ)
- `solution`: Complete solution with working and marking rubric
- `points`: Point value (from extracted marks)
- `tagInput`: Comma-separated tags including subject, region, topic
- `classId`: Curriculum class identifier
- `unitId`: Manitoba Pre-Calc unit (unit-a through unit-h)
- `sectionId`: Topic classification
- `images`: Array of image filenames referenced in body/solution

### 2. `exam.tex`

Compilable LaTeX document using the `exam` document class. Can be compiled with:
```bash
pdflatex exam.tex
```

**Features:**
- Uses `exam` class with `addpoints` option for point tracking
- Includes `\begin{solution}...\end{solution}` blocks for instructor view
- All required packages (amsmath, graphicx, etc.)
- Images linked from `./images/` directory

### 3. `images/` Directory

All images referenced in questions and solutions are copied here. When importing to test-generator, ensure this directory is available at the expected path.

## Using with test-generator

### Import Process
1. Copy `bulk_import.json` and `images/` directory to test-generator's import location
2. Use test-generator's bulk import feature to load questions
3. Questions will be classified according to `classId`, `unitId`, and `sectionId`

### Curriculum Mapping
Questions are automatically classified into Manitoba Pre-Calculus 40S units:
- **unit-a-trig**: Trigonometric functions
- **unit-b-binomial**: Binomial theorem
- **unit-c-exponential**: Exponential functions  
- **unit-d-logarithm**: Logarithmic functions
- **unit-e-rational**: Rational functions
- **unit-f-polynomial**: Polynomial functions
- **unit-g-sequences**: Sequences and series
- **unit-h-combinatorics**: Combinatorics (if questions exist)

Unit classification is automatic based on keyword detection in the solution text.

## Data Quality Notes

### Question Body Limitation
Due to the way MathPix structures extracted LaTeX, the `body` field contains only the first 500 characters of the solution. For full question/solution context, refer to the `solution` field which contains complete working.

### Manual Review Recommended
Before importing to test-generator, review questions for:
- Correct point values (extracted from marking rubric)
- Appropriate curriculum unit assignment (keyword-based detection)
- Image references are intact (check `images/` directory contents)

### Image Handling
- All images are PNG format (converted during MathPix processing)
- Filename format: `<document-id>-<page>_<coords>.png`
- Update image paths in solution text if needed for different storage location

## Workflow

1. **MathPix Processing**: Original PDFs → LaTeX with images
2. **JSON Extraction**: MathPix LaTeX → structured JSON (via `mathpix_latex_parser.py`)
3. **Bulk Import Generation**: JSON → DraftQuestion format (via `extract_to_bulk_import.py`)
4. **Test-Generator Import**: Load `bulk_import.json` into test-generator app

## Related Scripts

- `mathpix_latex_parser.py`: Parse MathPix LaTeX and extract questions/solutions
- `extract_to_bulk_import.py`: Convert extracted JSON to bulk-import format
- `aggressive_clean_all.py`: Pre-process PDFs to reduce MathPix page count
