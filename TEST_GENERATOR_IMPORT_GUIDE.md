# Test-Generator Bulk Import Guide

This guide explains how to import the Manitoba Pre-Calculus 40S questions into test-generator.

## Quick Start

### File Locations
```
output_clean/
├── bulk_import.json    ← Main file for import
├── images/             ← All 58 referenced images
│   ├── 2795df6c-...png
│   └── ...
└── exam.tex            ← Optional LaTeX document (reference only)
```

### Import Steps

1. **Locate test-generator's bulk import feature**
   - In test-generator UI, find Bulk Import or Import Questions section
   - Upload `bulk_import.json`

2. **Verify image directory**
   - Test-generator will expect images at the configured image storage path
   - Copy contents of `output_clean/images/` to test-generator's image directory
   - Update image path references if needed

3. **Review imported questions**
   - Questions will appear in the Pre-Calculus 40S class
   - Review curriculum unit assignments (auto-classified A-H)
   - Edit if curriculum mapping needs adjustment

4. **Run bulk import**
   - Execute the import process
   - Questions should populate with solutions visible for instructors

## DraftQuestion JSON Format

The `bulk_import.json` follows test-generator's `DraftQuestion` interface:

```typescript
interface DraftQuestion {
  body: string;           // Question body in LaTeX/Typst
  questionType?: string;  // "frq" for free-response
  answer: string;         // Empty for FRQ
  solution: string;       // Solution in LaTeX
  points: number;         // Point value (from marks)
  tagInput: string;       // "Pre-Calculus 40S, Manitoba, trigonometric"
  classId: string;        // "pre-calc-40s"
  unitId: string;         // "unit-a-trig" through "unit-h"
  sectionId: string;      // Topic name
  images?: string[];      // Image filenames
}
```

## Curriculum Mapping

Questions are auto-classified into Manitoba Pre-Calculus 40S units based on content analysis:

| Unit | Questions | Topics |
|------|-----------|--------|
| A | 21 | Trigonometric functions, identities, equations |
| B | 1 | Binomial theorem, expansions |
| C | 2 | Exponential functions, growth/decay |
| D | 4 | Logarithmic functions, equations |
| E | 1 | Rational functions |
| F | 4 | Polynomial functions, remainder theorem |
| G | 0 | Sequences and series |
| H | 0 | Combinatorics |
| Other | 8 | Mixed/unclassified |

**Note**: Classification is automatic via keyword detection. You can manually adjust `unitId` and `sectionId` if needed.

## Post-Import Customization

### Image Path Updates
If test-generator stores images differently, update image references:
```json
{
  "images": ["relative/path/to/image.png"]
}
```

### Curriculum Assignment
Manually adjust for courses/units:
```json
{
  "classId": "pre-calc-40s",
  "unitId": "unit-a-trig",
  "sectionId": "trigonometric-functions"
}
```

### Solution Formatting
Solutions are in LaTeX. If test-generator requires Typst:
- Simpler equations convert automatically
- Complex `array` and multi-line environments may need manual conversion
- Use test-generator's LaTeX→Typst converter if available

## Troubleshooting

### Images Not Loading
- Verify image directory path matches test-generator's configuration
- Check image filenames in JSON match actual files in `images/`
- Format: `2795df6c-6e2d-4017-aae1-564aebe344d4-02_622_660_603_207.png`

### Points Not Assigned
- Points extracted from MathPix marking rubric marks
- Verify `points` field is numeric in JSON
- Adjust manually if marks were ambiguous in original PDF

### Curriculum Unit Mismatch
- Auto-classification based on solution keywords
- Manually adjust `unitId` for questions that don't fit
- Can batch update all questions for a unit

### Solution Text Formatting
- Solutions contain LaTeX mathematical notation
- Most exam class LaTeX converts to test-generator format
- Very complex or malformed environments may need editing

## Processing Additional Exam Years

To process all 20 Manitoba Pre-Calculus 40S exam years:

```bash
# 1. For each exam year:
python3 src/mathpix_latex_parser.py \
  mathpix_input/exam_2023_combined.tex \
  mathpix_output/exam_2023_questions.json

# 2. Convert to bulk import:
python3 src/extract_to_bulk_import.py \
  mathpix_output/exam_2023_questions.json \
  mathpix_input/images \
  output_2023

# 3. Upload to test-generator (UI or script)
```

Total projected: ~820 questions (41 questions × 20 exams)

## Data Quality

### What's Included
- ✓ Question statements and solutions
- ✓ Mathematical notation and equations
- ✓ Images referenced in questions
- ✓ Point values from marking rubric
- ✓ Curriculum unit classification
- ✓ Topic tags

### Limitations
- Body field truncated to 500 characters (full context in solution)
- Some complex LaTeX from MathPix may have formatting artifacts
- Image filenames are MathPix format (long hash-based names)
- Auto-classification may need manual review for mixed-topic questions

### Manual Review Checklist
Before final deployment:
- [ ] All 41 questions imported successfully
- [ ] Images load correctly in question view
- [ ] Curriculum unit assignments match Manitoba standards
- [ ] Point values appropriate for each question
- [ ] Solution math notation displays correctly

## Contact & Support

For issues with test-generator's bulk import feature, refer to test-generator documentation or contact development team.

For questions about the extraction process, see `BULK_IMPORT_README.md`.
