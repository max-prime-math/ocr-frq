# AP Calculus FRQ tranche 01 — staged status

Date: 2026-09-13

## Scope

Twelve BC FRQs are source-locked and staged: all six questions from 1999 and
all six from 2000. Each has an original prompt PDF, matching scoring-guide
PDF, exact source pages, SHA-256 fingerprints, and retained Mathpix ZIPs.
No Mathpix API request and no TestGen publication has occurred.

## Gates reached

- Source catalog: **12/12 file/hash/page-range checks passed**; editorial
  prompt-boundary review is still pending.
- Retained prompt OCR records: **12/12 staged**.
- Prompt image assets retained for review: **7**.
- Prompt Typst candidates: **12/12 compiled**.
- Page-limited Mathpix scoring-guide recovery: **12/12 completed**.
- Scoring-guide Typst candidates: **12/12 compiled**.

## Deliberate block

The old BC scoring-guide ZIP parser is not safe for this tranche. It returns
empty segments for some questions and a nonempty but wrong-question segment
for at least BC 2000 Q1. Therefore retained scoring-guide text is preserved
only as comparison evidence. Each candidate instead uses its completed,
page-limited Mathpix recovery artifact.

The twelve recovery documents were submitted and completed, but their artifacts
remain local and ignored. Each question still needs manual boundary, figure,
solution, Typst, and TestGen review before publication.
