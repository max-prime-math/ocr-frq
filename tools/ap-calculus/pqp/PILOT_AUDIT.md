# AP Calculus FRQ 12-question pilot — manual editorial audit

Date: 2026-09-13

This is an editorial, source-aware review of the pilot records. A successful
Typst compile is necessary but does not itself make a question publishable.
Each question remains blocked until its scoring guide is rewritten as a
classroom-facing solution and its rubric is separately retained.

| Question | Body / boundary | Mathematics and solution | Figure decision | Disposition |
| --- | --- | --- | --- | --- |
| BC 1998 Q1 | Correct | Correct calculus; solution rewritten | No body figure | Published |
| BC 1998 Q2 | Correct | `z` → `x` repaired; solution rewritten | None | Published |
| BC 1998 Q6 | Correct | Guide order repaired in solution | None | Published |
| BC 2010 Form B Q1 | Correct | Solution rewritten | Source region graph attached to body | Published |
| BC 2010 Form B Q3 | Correct | Correct work, but prompt crop omits the essential $P(t)$ table | **Blocked: recover complete table and attach it** | Held |
| BC 2010 Form B Q6 | Correct | Solution rewritten | None | Published |
| AB 2005 Form B Q1 | Correct | Solution rewritten | Source region graph attached to body | Published |
| AB 2005 Form B Q4 | Correct | Solution rewritten | Source piecewise graph attached to body | Published |
| AB 2005 Form B Q6 | **Boundary repaired:** source page begins with Q5, record starts at Q6 | Solution rewritten | Source slope-field axes attached to body | Published |
| AB 2019 Q1 | Correct | Solution rewritten | None | Published |
| AB 2019 Q3 | Correct; graph retained with Q3 | Solution rewritten | Source graph attached to body | Published |
| AB 2019 Q6 | Correct | Solution rewritten | None | Published |

## Outcome

- Source boundary review: **12/12 passed**.
- Typst body and scoring-guide compilation: **12/12 passed**.
- Substantive OCR repair identified: **BC 1998 Q2 `z` → `x`** in two scoring-guide expressions.
- Figure-free questions finalized: **6**.
- Diagram questions finalized with source crops: **5**.
- Held for incomplete source capture: **BC 2010 Form B Q3**.
- Published to the working bank: **11/12**. Each passed independent Typst plus TestGen import/round-trip validation.

## Next editorial tranche

Recover the missing $P(t)$ table for BC 2010 Form B Q3 from its original
source page, attach it together with the pool diagram, and then run the same
visual, solution, Typst, and TestGen gates.
