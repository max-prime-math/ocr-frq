# ocr-frq

Converts AP Calculus BC free-response exam PDFs into a single, typeset exam-class PDF containing every question, worked solution, and scoring rubric from 1998–2019 (including Form B variants).

The pipeline is **Mathpix-primary**: it reads Mathpix zip exports rather than calling any OCR or AI API, making it fast, deterministic, and free to run. The output is a single LaTeX/PDF document structured year-by-year with proper mathematical typesetting.

---

## Output

A single PDF (`output_latex/output_frq.pdf`) containing:
- **32 year/form sections** — 1998–2019 BC, plus Form B 2002–2011
- **192 questions** across all sections
- Each question has:
  - Question statement with sub-parts `(a)`–`(d)` in `\begin{parts}`
  - **Solution:** worked answers for each sub-part
  - **Rubric:** point-value annotations extracted from the scoring guide
- Year sections are separated by `\section*{YEAR AP Calculus BC}` with the `\question` counter resetting at each one
- Figures from the original exams embedded at 60% linewidth

---

## Setup

**Requirements:**
```
python -m pip install -r requirements.txt
```

Dependencies: `anthropic`, `pymupdf`, `Pillow`, `opencv-python`

**Also needed:** `pdflatex` with the `exam` document class and standard AMS packages.

**Data:** The `mathpix/` directory must contain the Mathpix zip exports:
- `BC-YEAR.zip` — exam booklet
- `SG-BC-YEAR.zip` — scoring guide
- `BC-YEAR-FORM-B.zip` / `SG-BC-YEAR-FORM-B.zip` — Form B (2002–2011)

---

## Usage

```bash
# All years (1998–2019 BC + Form B)
python -m src.main

# Specific years only
python -m src.main --years 2018,2019

# Skip Form B exams
python -m src.main --no-form-b

# Custom output directory
python -m src.main --output-dir my_output/
```

Output goes to `output_latex/` by default:
- `output_frq.tex` — LaTeX source
- `output_frq.pdf` — compiled PDF
- `figures/` — extracted figure images (JPEGs)

---

## Architecture

```
mathpix/BC-YEAR.zip          mathpix/SG-BC-YEAR.zip
        │                              │
        ▼                              ▼
  parse_exam_zip()             parse_sg_zip()
  • Extract figures             • Parse question sections
  • Center figure images        • Strip question preamble
  • Detect Part A/B             • Split solution/rubric
  • Find question starts        • Handle interleaved format
        │                              │
        └──────────┬───────────────────┘
                   ▼
            QuestionBlock
       (question_text, sg_text,
        figure_paths, part, year…)
                   │
                   ▼
         build_combined_document()
       • \section* per year
       • \question + \leavevmode
       • \begin{parts} for sub-parts
       • \begin{solution}
           \textbf{Solution:}
           \begin{parts}…\end{parts}
           \textbf{Rubric:}
           \begin{parts}…\end{parts}
         \end{solution}
                   │
                   ▼
             pdflatex
```

### Source files

| File | Purpose |
|------|---------|
| `src/main.py` | CLI entry point |
| `src/mathpix.py` | Parse Mathpix zip exports → structured data |
| `src/contracts.py` | `ExamQuestion`, `QuestionBlock` dataclasses |
| `src/latex_writer.py` | Render to exam-class LaTeX; solution/rubric splitting |
| `src/compile_gate.py` | Run pdflatex |

---

## LaTeX document structure

The generated document uses the `exam` document class with `\printanswers`. Each question follows this pattern:

```latex
\question
\leavevmode
% Q1 | 1998 Calculus BC | Part A | Calculator Active
[question intro / setup figure]
\begin{parts}
  \part Find the area of R.
  \part Find the volume when R is revolved about the x-axis.
\end{parts}
\begin{solution}
  \textbf{Solution:}\par
  \begin{parts}
    \part Area = \int_0^4 (8 - x^{3/2}) dx = 96/5
    \part Volume = 576π/5 ≈ 361.911
  \end{parts}
  \par\medskip
  \textbf{Rubric:}\par
  \begin{parts}
    \part $3:\left\{\begin{array}{l}1:\text{ integral}\\1:\text{ integrand}\\1:\text{ answer}\end{array}\right.$
  \end{parts}
\end{solution}
```

---

## Mathpix format handling

The pipeline handles several Mathpix-specific formatting variations:

**Exam zip formats (across years):**
- Question numbering via `\setcounter{enumi}{N}` + `\item`
- Plain-text question numbers (`3. The graph of f…`) in some years
- Part A/B detection from section header keywords
- Default: Q1–3 = Part A (calculator), Q4–6 = Part B (no calculator)

**SG zip formats:**
- 1998–1999: old `\begin{enumerate}\item` format
- 2000+: `\section*{Question N}` sections
- Some years: `\caption{Question N}` inside figure/table environments
- Interleaved rubric/solution (rubric for part a appears before solution for part b) — detected and re-split correctly

**Rubric annotation styles across years:**
```
$2:\left\{1: criterion \\ 1: criterion\end{array}\right.$  (modern)
$2\left\{…\right.$       (old, no colon)
3 $\left\{…\right.$      (1999 style, digit before $)
$$3\left\{…\right.$$     (display math)
1 : criterion text        (standalone point annotation)
Note: …                   (scoring note, line-start only)
```

---

## Figure extraction

Figures are extracted from both exam and SG zips:

- **Exam figures:** JPEGs bundled in the zip (slope field axes, region graphs, etc.) — saved to `figures/bc-YEAR_figN.jpg`
- **SG figures:** Completed slope fields, phase portraits, sketches — saved to `figures/sg-bc-YEAR_figN.jpg`
- Figures appearing before the first question in Mathpix are assigned to Q1 (orphan figure fix)
- LaTeX tabular tables appearing before Q1 (data tables) are also prepended to Q1
- "As shown in the figure above" language is corrected when no figure precedes the reference

---

## Known limitations

| Issue | Affected |
|-------|---------|
| 2000 BC Q2–Q6: free-form SG with no question markers — no solutions | 2000 BC Q2–Q6 |
| 2000 BC Q1: SG content is Q5's implicit-differentiation solution (old format artifact) | 2000 BC Q1 |
| Some `(b)–(d)` solutions still missing/truncated where Mathpix OCR was incomplete | Various years |
| 1998 Q2: `e^{2z}` typo should be `e^{2x}` (3 instances) | 1998 BC Q2 |
| 7 rubric criterion lines still appearing in solution section (deep interleaving) | Various |

---

## Adding new years

1. Add `BC-YEAR.zip` and `SG-BC-YEAR.zip` to `mathpix/`
2. For Form B: add `BC-YEAR-FORM-B.zip` and `SG-BC-YEAR-FORM-B.zip`
3. Add the year to `_ALL_YEARS` in `src/main.py` (currently hardcoded as `range(1998, 2020)`)
4. Run `python -m src.main --years YEAR`

---

## Related repos

- **ocr-mcq** (`../ocr-mcq/`) — Same approach for AP Calculus BC/AB multiple-choice sections. Produces an exam-class PDF with questions, answer choices, and solutions.
- **bnk-decoder** (`../bnk-decoder/`) — Companion tooling.
- **test-generator** (`../test-generator/`) — Downstream consumer of this pipeline's output.
