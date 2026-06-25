# Manitoba Pre-Calculus 40S Processing

This repository now supports processing Manitoba Pre-Calculus 40S exams from Mathpix OCR exports, in addition to the original AP Calculus BC functionality.

## Quick Start

To process a Manitoba Pre-Calculus exam:

```bash
python tools/manitoba-precalc-40s/process_manitoba_exam.py path/to/your_exam_file.zip
```

Example:
```bash
python tools/manitoba-precalc-40s/process_manitoba_exam.py data/legacy/manitoba-prototype-mathpix/raw-mathpix/pre-calc-40s_jan_13_mg-only_cleaned_aggressive.zip
```

## What It Does

The processor:

1. **Extracts and parses** Manitoba Pre-Calculus questions from Mathpix zip exports
2. **Generates a professional LaTeX exam** using the `exam` document class with:
   - Proper question numbering with point values
   - Solution environments (similar to AP exams)
   - Embedded images with proper sizing
   - Clean mathematical typesetting

3. **Creates JSON export** for bulk import to test-generator systems
4. **Compiles a PDF** automatically if LaTeX is available

## Output Files

For an input file `exam.zip`, the processor generates:

- `exam_formatted.tex` - LaTeX exam document with solutions
- `exam_formatted.pdf` - Compiled PDF (28+ pages for the sample exam)
- `exam_processed.json` - JSON export for bulk import

## Features

### FRQ Styling
- Uses the same solution environment style as AP Calculus BC exams
- Proper point allocation and marking
- Mathematical content preserved with LaTeX formatting
- Images automatically embedded and sized appropriately

### MCQ Support (Ready for Future Use)
- Framework in place for multiple choice questions
- Compatible with ocr-mcq styling using `\begin{choices}` environments
- Can be easily extended when MCQ content is available

### Content Processing
- Automatically detects and categorizes curriculum units:
  - Trigonometric functions
  - Binomial theorem
  - Exponential/logarithmic functions
  - Rational functions
  - Polynomial functions
- Proper image handling and path resolution
- Unicode character normalization
- LaTeX cleaning and formatting

## Integration with Existing Pipeline

This extends the existing Manitoba processing (`mathpix_latex_parser.py` and `extract_to_bulk_import.py`) with:

- Better question boundary detection
- Improved image handling
- Professional exam document generation
- Seamless integration with the existing cache and corrections system

## Sample Output

The processed Manitoba exam contains:
- **23 FRQ questions** covering various Pre-Calculus topics
- **Professional formatting** matching AP exam style
- **Complete solutions** with proper mathematical notation
- **Embedded figures** (29+ images properly integrated)
- **Point allocation** (48 total points across all questions)

## Technical Details

### Parser (`manitoba_precalc_parser.py`)
- Specialized parser for Manitoba Pre-Calc format
- Handles mixed content (questions + solutions)
- Intelligent question boundary detection
- Image extraction and path management

### Question Detection
Uses pattern matching to identify real question starts:
- "Gina correctly started to answer..."
- "Find and simplify the nth term..."
- "The number of times a website..."
- "Solve algebraically:"
- And many others specific to Pre-Calculus content

### LaTeX Generation
- Uses `exam` document class with `addpoints` option
- Solution environments for complete answers
- Proper mathematical formatting
- Image scaling and positioning

This provides a complete end-to-end solution for processing Manitoba Pre-Calculus 40S exams with the same professional quality as the AP Calculus BC pipeline.
