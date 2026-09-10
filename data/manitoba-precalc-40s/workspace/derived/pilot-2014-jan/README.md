# January 2014 staging pilot

This is a review candidate, not a classroom-approved release.

- `review.pdf`: rendered questions, choices, and solutions for visual review.
- `manitoba-pc40s-2014-jan.zip`: PQP JSON and its adjacent assets bundled together.
- `manitoba-pc40s-2014-jan.pqp.json` and `assets/`: unpacked import package.
- `pilot-report.json`: final rendering checks and fallback question numbers.
- `compile-report.json`: earlier conversion failures that motivated the fallbacks.

The package contains all 44 questions: 34 written-response questions and 10
MCQs. All stems and choices were retained from the existing export, except the
empty-base subscript syntax in Question 28, which was corrected for Typst.
All 10 answer-key answers were retained.

The new 43-page marking-guide OCR recovered all 34 written-response solution
segments. Twenty-nine convert to editable Typst. Questions 7, 12, 26, 28, and
29 display original marking-guide pages because their editable conversions have
graph, table, or notation problems. Those reference pages may include scoring
notes and exemplars. Original OCR and candidate Typst remain in extensions for
later repair.

Verification: all 44 complete question/choice/solution documents compile with
Typst; all 44 import through TestGen's parser; all 40 declared images exist;
all marking-guide and student-booklet page headers match the expected source
pages. Question 1 was visually spot-checked. Full mathematical and visual review
is still pending; successful compilation does not establish accuracy.

The dedicated scripts in `tools/manitoba-precalc-40s/pqp/pilots/` reproduce this
experiment. Run `build.py`, then `finalize.py`, from the OCR repository. They
require Node, Typst, Python dependencies used by the exporter, and the installed
`mitex-wasm` package at `/home/max/dev/typr/node_modules/mitex-wasm/`.
They are specific to January 2014; the general exporter still has stale schema
and native MiTeX paths that need repair before batch generation.

Mathpix job: `cc9001ad-6312-43bc-93f7-8b12c5460552`. The old cache is recoverable
from Git and `/tmp/mb-pc40s-2014-jan-before.rLFBeP/artifacts.tar.gz`.
