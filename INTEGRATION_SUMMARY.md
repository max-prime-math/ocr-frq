# Manitoba Pre-Calculus 40S → Test-Generator Integration

## Summary

Successfully created bulk-import format for 41 questions extracted from MathPix LaTeX.

### Outputs Generated

Located in: `/home/max/test-gen-suite/ocr-frq/output_clean/`

#### 1. **bulk_import.json** ✓ READY
- 41 DraftQuestion objects in test-generator format
- All required fields: body, solution, points, classId, unitId, sectionId, etc.
- Curriculum classification: 21 trigonometric, 4 polynomial, 4 logarithmic, 2 exponential, etc.
- Image references: 58 images copied and linked
- **Status**: Ready for import to test-generator

#### 2. **exam.tex** (Optional)
- Compilable LaTeX document using exam class
- Contains all questions with solutions
- **Note**: Has some formatting artifacts from MathPix extraction (complex math environments)
- Can be used for human review but focus on JSON for automated import

#### 3. **images/** Directory ✓ READY
- 58 PNG images copied from mathpix_input
- Linked in bulk_import.json with filenames
- Ready for test-generator's image handling

## Data Structure

Each question in bulk_import.json contains:
```json
{
  "body": "LaTeX question/solution excerpt (500 chars)",
  "questionType": "frq",
  "answer": "",
  "solution": "Complete LaTeX solution with working",
  "points": 3.0,
  "tagInput": "Pre-Calculus 40S, Manitoba, <topic>",
  "classId": "pre-calc-40s",
  "unitId": "unit-a-trig|unit-b-binomial|...",
  "sectionId": "<topic>",
  "images": ["image1.png", "image2.png"]
}
```

## Integration Steps

### For Test-Generator Bulk Import:
1. Copy `bulk_import.json` to test-generator's import directory
2. Copy `images/` folder to image storage location
3. Run bulk import in test-generator app
4. Questions will auto-classify into curriculum units (A-H)

### Data Quality Notes
- Points values extracted from marking rubric marks
- Topics auto-detected from solution content keywords
- Image filenames: MathPix format (`<doc_id>-<page>_<coords>.png`)
- No manual curriculum mapping needed - auto-classified by unit

## Workflow Timeline

```
PDFs (20 exam years)
    ↓ (pdf_combiner.py)
Combined PDFs (1 per year)
    ↓ (pdf_aggressive_cleaner.py)
Cleaned PDFs (76.6% page reduction)
    ↓ (MathPix OCR)
LaTeX + Images (840 pages total)
    ↓ (mathpix_latex_parser.py)
Extracted JSON with 41 questions
    ↓ (extract_to_bulk_import.py)
DraftQuestion Format
    ↓
test-generator Bulk Import ✓
```

## Validation

- ✓ 41 questions successfully extracted
- ✓ All curriculum fields populated
- ✓ All images referenced and copied
- ✓ JSON structure matches DraftQuestion interface
- ✓ Points values assigned from marks
- ✓ Topic classification applied

## For Future Batches

To process all 20 exam years:
1. Run combined PDFs through MathPix (60 files, 840 pages total)
2. Download LaTeX outputs for each exam
3. Extract questions with `mathpix_latex_parser.py` for each
4. Convert to bulk import with `extract_to_bulk_import.py`
5. Batch import to test-generator

Each exam year produces ~41 questions across all topics.

## Scripts Location

- `/home/max/test-gen-suite/ocr-frq/src/extract_to_bulk_import.py` - Final converter
- `/home/max/test-gen-suite/ocr-frq/src/mathpix_latex_parser.py` - Question extraction
- `/home/max/test-gen-suite/ocr-frq/src/BULK_IMPORT_README.md` - Detailed docs
