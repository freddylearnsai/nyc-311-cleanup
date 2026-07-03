# Receipts — NYC 311 cleanup (May 2026 slice)

Measured from the actual run on this repo. Reproduce with `python run_all.py`.

| Receipt | Value |
| --- | --- |
| Rows in (raw) | 331976 |
| Rows out (clean) | 331976 |
| Duplicate keys removed | 0 |
| Boroughs normalized | 0 |
| Invalid zips nulled | 1 |
| Out-of-bbox coords nulled | 0 |
| % passing all rules — before | 99.99% |
| % passing all rules — after | 100.0% |
| Pipeline runtime (fetch excluded) | 0.0 min |

Rule-by-rule detail: [before](reports/before-report.md) · [after](reports/after-report.md)

Note: `Boroughs normalized` counts unmappable values (none existed); case-folding still standardized 397 'Unspecified' rows to canonical form. `Duplicate keys removed: 0` is a verified fact of this slice, not an unexecuted step.
