# Manitoba Pre-Calculus 40S Source Audit

Verified: 2026-09-10

Official source: <https://www.edu.gov.mb.ca/k12/assess/archives/>

## Coverage

The repository contains every published English Pre-Calculus 40S achievement
test sitting under the curriculum introduced in 2012–2013:

- January and June 2013–2019
- January 2020
- January and June 2024–2026

There is no missing June 2020–June 2023 source set. Manitoba reports that the
provincial tests were suspended beginning in semester 2 of 2019–2020 through
the end of 2022–2023.

## Files Verified

- 42 student booklets: two per sitting. Every local file has the same byte size
  as its corresponding current Manitoba archive download.
- 21 marking guides: one per sitting. Every local file has the same page count
  and `pdftotext -layout` content hash as its corresponding current Manitoba
  archive download.
- Marking-guide binary sizes can differ because the local copies were
  repackaged/compressed; the page and extracted text comparisons match.
- All 63 corresponding official URLs were reachable during the audit.

The official archive permits reproduction for educational, non-commercial
purposes and asks that extracts cite the source.

## Local Completeness Gate

```sh
python3 tools/manitoba-precalc-40s/pqp/audit_manitoba_source_inventory.py --strict
```

This checks the expected 21 sittings, all 63 source documents, the question
catalog, manifest entries, and the three cached Mathpix output types for every
document. It does not replace periodic comparison with the official archive
when Manitoba publishes a new sitting.
