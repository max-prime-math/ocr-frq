# AP Calculus FRQ pilot retrospective

Date: 2026-09-13

## Result

The 12-question calibration pilot was published to the private TestGen
working bank after source, Typst, TestGen, visual, and mathematical review.
It contains six AB and six BC questions across old, Form B, and modern
layouts. The bank now contains all 12 questions and seven source-derived
image assets.

## What worked

- Source hashes and page references made every review decision traceable.
- Retained BC Mathpix ZIPs were sufficient for a low-cost first OCR pass.
- Small, manually approved publication batches kept unreviewed OCR out of
  TestGen.
- Native Typst compilation and a TestGen import/round-trip caught structural
  problems before publication.

## Corrections and safeguards that matter at scale

- BC 1998 Q2 required a substantive legacy-OCR repair (`z` to `x`) in two
  expressions. Retained OCR is therefore an input, never source truth.
- AB 2005 Form B Q6 began on a page containing the end of Q5. Page-level OCR
  does not establish question boundaries; each boundary needs source review.
- BC 2010 Form B Q3 initially lacked its essential table. A crop is usable
  only when it contains all information the question needs; source-page
  recovery is preferable to inventing a replacement diagram.
- Scoring guides are rubrics, not classroom solutions. They must be rewritten
  and checked as worked mathematics before publication.
- The 1999/2000 retained scoring-guide ZIP parser can return a nonempty block
  belonging to the wrong question. A nonempty legacy guide is not evidence of
  correct segmentation; scaled tranches require page-limited source recovery.

## Scaled operating rules

1. Build a source-locked tranche catalog before reading OCR.
2. Use retained BC OCR before any new Mathpix request; use Mathpix only for
   source-paired material that has no adequate retained artifact.
3. Keep OCR records and Typst candidates blocked by default.
4. Review prompt boundaries and every required table/graph before solution
   writing. Preserve source crops where an exact native reconstruction is not
   yet justified.
5. Publish only explicitly approved questions, then run Typst and TestGen
   import/round-trip checks on the candidate and live bank.

## Next tranche

`tranche-01` contains BC 1999 and BC 2000, six questions from each release.
It is intentionally cache-first: original PDFs and paired scoring guides are
present locally, and both releases have retained prompt and scoring ZIPs.
No new Mathpix submission is needed to stage it.
